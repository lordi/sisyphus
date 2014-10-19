Sisyphus
========

Sisyphus is a little helper script to re-run arbitrary commands over and over again. Poor Sisyphus will execute the argument list as a command, monitor the current directory for changes and re-run the command each time a modification is detected. Also, it will terminate a long-running command when a modification is detected and start over.

It is based on the pyinotify example script "[autocompile.py](https://github.com/seb-m/pyinotify/blob/master/python2/examples/autocompile.py)".

You can use Sisyphus to

 * auto-compile your program
 * auto-run your test suite
 * auto-restart your development server
 * auto-refresh your browser (i.e., via [MozRepl](https://github.com/bard/mozrepl/wiki)) when doing web development
 * auto-restart your unsuccessful shell command until it succeeds.

It can be convenient to see the output of your program as soon as you save it, without leaving your editor. But remember: Your actions might put Sisyphus in an existential crisis where it is faced with questions about the absurdity of life.

Requirements
------------

 * Linux ≥ 2.6.13
 * [pyinotify](https://github.com/seb-m/pyinotify)
 * Both Python 2.x and 3.x are supported

Installation
------------

    pip install sis

Examples
--------

    sis -d src make

    sis -e hs cabal test

    sis -s 'lynx -dump http://my-web-app/'

Ignore patterns
---------------

Sisyphus will ignore changes in files matching any regex pattern found in the following files:

 * /etc/sisignore
 * ~/.sisignore
 * .sisignore


