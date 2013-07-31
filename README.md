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

It is very convenient to see the output of your program as soon as you save it in your editor. But remember: Your actions might put Sisyphus in an existential crisis where it is faced with questions about the absurdity of life.

Both Python 2.x and 3.x are supported.

Ignore patterns
---------------

Sisyphus will ignore changes in files matching any regex pattern found in the following files:

 * /etc/sisignore
 * ~/.sisignore
 * .sisignore

Installation
------------

    git clone https://github.com/lordi/sisyphus
    cd sisyphus
    ln -s $PWD/sisyphus.py ~/bin/sisyphus

Examples
--------

    sisyphus make
    sisyphus cabal test

