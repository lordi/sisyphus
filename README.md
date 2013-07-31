Sisyphus
========

About
-----

Sisyphus is a little helper script to re-run arbitrary commands over and over again. Poor Sisyphus will execute the argument list as a command, monitor the current directory for changes and re-run the command each time a modification is detected. Also, it will terminate a long-running command when a modification is detected and start over.

It is based on the pyinotify example script "autocompile.py".

You can use Sisyphus to

 * auto-compile your program
 * auto-run your test suite
 * auto-restart your development server
 * auto-restart your unsuccessful shell command until it succeeds.

Both Python 2.x and 3.x are supported.

Ignore patterns
---------------

Sisyphus will ignore changes in files matching any regex pattern found in the following files:

 * /etc/sisignore
 * ~/.sisignore
 * .sisignore

Installation
------------

    git clone https://github.com/lordi/sisyphus.git
    cd sisyphus
    ln -s sisyphus.py ~/bin/sisyphus

Examples
--------

    sisyphus make
    sisyphus cabal test

