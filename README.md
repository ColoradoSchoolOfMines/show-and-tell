# show-and-tell
An application to allow CS majors to show off their CS projects on the ACM TV in Brown

## Setting up a Development Environment
### Linux
1. Ensure that you have the following packages installed:

        postgresql
        ruby
        python3

2. Enable and start the postgresql service.

3. Run `su - postgres -c "initdb --locale en_US.UTF-8 -D '/var/lib/postgres/data'"`

4. As the `postgres` user, run the following commands:

        createdb showandtell
        createuser sam

5. Run the following commands to install the necessary SASS plugins:

        gem install compass
        gem install font-awesome-sass
        gem install bootstrap-sass

6. Install the following Python libraries. (Pip is probably the easiest way to
   do this.)

        sqlalchemy
        kajiki
        bottle
        PyYaml
        validators
        markupsafe
        Pillow

7. Run the app by running `app.py` and navigating in your browser to
   `localhost:8080`
