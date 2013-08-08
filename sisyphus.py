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

class Sisyphus(pyinotify.ProcessEvent):
    def __init__(self, options, *args, **kwargs):
        self.options = options
        if self.options.silent:
            self.options.verbose = False
        self._load_excl_patterns()
        self.directory = os.path.abspath(self.options.directory)
        super(Sisyphus, self).__init__(*args, **kwargs)
        self.wm = pyinotify.WatchManager()
        self.notifier = pyinotify.Notifier(self.wm, default_proc_fun=self)
        self.wm.add_watch(self.directory, MASK, rec=True, auto_add=True)
        signal.signal(signal.SIGINT, self.on_sigint)

    def run(self):
        self.notifier.loop()

    def my_init(self, cmd): # called from pyinotify.ProcessEvent
        self.cmd = cmd
        self.proc = None
        self.pool = Pool(max_workers=1)
        self.future = None
        self.dirty = True
        self.start_if_dirty()

    def on_sigint(self, signum, frame):
        self.terminate()
        sys.exit(130)

    def on_done(self, future):
        self.proc = None
        if self.options.verbose:
            print("<==", future, future.result())
        self.start_if_dirty()

    def terminate(self):
        if self.proc != None and self.proc.pid != None:
            os.killpg(self.proc.pid, signal.SIGTERM)

    def worker_thread(self):
        self.proc = subprocess.Popen(self.cmd, preexec_fn=os.setpgrp)
        self.proc.wait()
        return self.proc.returncode

    def start_if_dirty(self):
        if self.dirty and (self.future == None or not self.future.running()):
            if self.options.verbose:
                print("==> Executing command: ", self.cmd)

            self.future = self.pool.submit(self.worker_thread)
            self.future.add_done_callback(self.on_done)
            self.dirty = False
            if self.options.verbose:
                print("==>", self.future)

    def process_IN_MODIFY(self, event):
        if len(self.incl_re) > 0 and not any([rgx.search(event.pathname) for rgx in self.incl_re]):
            return
        if any([rgx.search(event.pathname) for rgx in self.excl_re]):
            return
        else:
            if not self.options.silent:
                print("<*> Detected change in:", event.pathname, event)
            self.terminate()
            self.dirty = True
            self.start_if_dirty()

    def _load_excl_patterns(self):
        excl_lines = [open(f).readlines() for f in EXCL_FILES if os.path.exists(f)]
        excl_patterns = [s.strip() for s in set(itertools.chain(*excl_lines)) if len(s) > 0]
        self.excl_re = [re.compile(s) for s in excl_patterns]
        incl_ext = [ext.strip('.,') for ext in self.options.extensions.split(',')]
        incl_patterns = ['\.{0}$'.format(ext) for ext in incl_ext if len(ext) > 0]
        self.incl_re = [re.compile(s) for s in incl_patterns]

if __name__ == '__main__':
    parser = OptionParser("usage: %prog [options] cmd")
    parser.allow_interspersed_args = False
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true",
            default=False,
            help="be verbose")
    parser.add_option("-s", "--silent", dest="silent", action="store_true",
            default=False,
            help="output nothing besides the child's output")
    parser.add_option("-d", "--dir", dest="directory", action="store",
            default='.',
            help="directory to monitor recursively [default=%default]")
    parser.add_option("-e", "--ext", dest="extensions", action="store",
            default='',
            help="file extensions to monitor, comma-separated list")

    (options, args) = parser.parse_args()

    if len(args) == 0:
        parser.print_help()
        sys.exit(1)

    sisyphus = Sisyphus(options, cmd=args)
    sisyphus.run()

