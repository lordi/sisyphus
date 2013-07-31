#!/usr/bin/python
from __future__ import print_function
import subprocess
import sys
import signal
import os.path
import os
import pyinotify
import re
import time
import itertools
from optparse import OptionParser
# to install run `pip install futures` on Python <3.2
from concurrent.futures import ThreadPoolExecutor as Pool
import logging
logging.basicConfig()

MASK = pyinotify.IN_MODIFY
EXCL_FILES = [
    '/etc/sisignore',
    os.path.expanduser('~/.sisignore'),
    os.path.join(os.getcwd(), '.sisignore')
]
EXCL_PATTERNS = set(itertools.chain(*[open(f).readlines() for f in EXCL_FILES if os.path.exists(f)]))
EXCL_RE = [re.compile(s.strip()) for s in EXCL_PATTERNS]

class Sisyphus(pyinotify.ProcessEvent):
    def __init__(self, options, *args, **kwargs):
        self.options = options
        super(Sisyphus, self).__init__(*args, **kwargs)
        self.wm = pyinotify.WatchManager()
        self.notifier = pyinotify.Notifier(self.wm, default_proc_fun=self)
        self.wm.add_watch(os.getcwd(), MASK, rec=True, auto_add=True)

    def run(self):
        self.notifier.loop()

    def my_init(self, cmd): # called from pyinotify.ProcessEvent
        self.cmd = cmd
        self.proc = None
        self.pool = Pool(max_workers=1)
        self.future = None
        self.dirty = True
        self.start_if_dirty()

    def _terminate(self):
        if self.proc != None and self.proc.pid != None:
            os.killpg(self.proc.pid, signal.SIGTERM)

    def on_done(self, future):
        self.proc = None
        if self.options.verbose:
            print("<==", future, future.result())
        self.start_if_dirty()

    def worker_thread(self, *args, **kwargs):
        self.proc = subprocess.Popen(self.cmd, preexec_fn=os.setpgrp)
        self.proc.wait()
        return self.proc.returncode

    def start_if_dirty(self):
        if self.dirty and (self.future == None or not self.future.running()):
            if self.options.verbose:
                print("==> Executing command: ", self.cmd)

            self.future = self.pool.submit(self.worker_thread, \
                    self.cmd, preexec_fn=os.setpgrp, shell=True)
            self.future.add_done_callback(self.on_done)
            self.dirty = False
            if self.options.verbose:
                print("==>", self.future)

    def process_IN_MODIFY(self, event):
        if any([rgx.search(event.pathname) for rgx in EXCL_RE]):
            return
        else:
            print("<*> Detected change in:", event.pathname)
            self._terminate()
            self.dirty = True
            self.start_if_dirty()

if __name__ == '__main__':
    parser = OptionParser("usage: %prog [options] cmd")
    parser.allow_interspersed_args = False
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true",
            default=False, help="be verbose [default: false]")

    (options, args) = parser.parse_args()

    if len(args) == 0:
        parser.print_help()
        sys.exit(1)

    sisyphus = Sisyphus(options, cmd=args)

    def on_sigint(signum, frame):
        sisyphus._terminate()
        sys.exit(130)

    signal.signal(signal.SIGINT, on_sigint)

    sisyphus.run()

