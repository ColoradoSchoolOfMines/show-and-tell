# show-and-tell
An application to allow CS majors to show off their CS projects on the ACM TV in Brown

## Setting up a Development Environment
### Linux
1. Ensure that you have the following packages installed:

        postgresql
        ruby
        python3

2. Enable and start the postgresql service.

3. Run `createdb showandtell`

3. Run the following commands to install the necessary SASS plugins:

        gem install compass
        gem install font-awesome-sass
        gem install bootstrap-sass

4. Install the following Python libraries:

        sqlalchemy
        kajiki
        bottle

Run the app by running `app.py` and navigating in your browser to
`localhost:8080`
