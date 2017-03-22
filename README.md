# show-and-tell
An application to allow CS majors to show off their CS projects on the ACM TV in Brown

# Installation and Setup
Install `show-and-tell` using the `setup.py` script::

    $ cd show-and-tell
    $ python setup.py develop

Create the project database for any model classes defined::

    $ gearbox setup-app

Start the paste http server::

    $ gearbox serve

While developing you may want the server to reload after changes in package
files (or its dependencies) are saved. This can be achieved easily by adding the
`--reload` option::

    $ gearbox serve --reload --debug

Then you are ready to go.
