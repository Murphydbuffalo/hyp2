# Hyp
## Table of contents
1. [Intro](#intro)
2. [How is work organized?](#how-is-work-organized)
3. [Setting up your local environment](#setting-up-your-local-environment)
4. [Running tests](#running-tests)
5. [Linting](#linting)
6. [Continuous Integration](#continuous-integration)
7. [Postman](#postman)
8. [Accessibility](#accessibility)
9. [Internationalization](#internationalization)

## Intro
Low risk, intuitive product experimentation. Inform your product decisions with evidence from your users by trying out multiple variations of your features.

Works with whatever amount of data you have - more data is better, but you can
still learn from a small amount of data.

Traffic flow to variants is adjusted in real time based on their performance.
As a result poorly performing variants are quickly starved of traffic while high-performing variants are rewarded with more.

Specify the value of particular actions within your product, so that Hyp can
measure success based on the total value provided by variants, rather than
just conversion rates.

We aim for:
+ Transparent pricing that's affordable for startups.
+ Helping customers leverage the data they actually have, rather than waiting
until they have a massive amount of traffic or users to start doing so.
+ Offering clear, intuitive explanations of experiment results.
+ Providing a great developer experience through thorough documentation, a robust sandbox environment, visibility into logs and events via a dashboard, security
best practices, and a fast API.

## How is work organized?
We do almost everything in GitHub. It's nice to have a single place for
Kanban boards (GitHub Projects), continuous integration (Github Actions), code
review, and high level product discussions (GitHub Projects, again).

Generally speaking we decide what to work on and when by writing up proposals,
discussing those proposals as a group, and prioritizing those proposals based
on consideration of how much effort they will take and how much value they will
provide, relative to other work we want to do.

We don't have substantive product discussions in instant messaging tools like
Slack, preferring to write in long-form and respond asynchronously.

Check out the description of our [product proposals board](https://github.com/Murphydbuffalo/hyp2/projects) for a detailed explanation.

## Setting up your local environment
Right now, Hyp is a [Django monolith](https://www.djangoproject.com/) hosted on
Heroku and backed by a PostgreSQL database. It uses `numpy` for fancy math.
Django has good docs and guides and is conceptually similar to Ruby on Rails.

Here's what you need to do to get Hyp running locally on a Mac:
1. Make sure you have XCode installed and up to date: `xcode-select --install`
2. Install Homebrew: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
3. Install Python 3: `brew install python3`. This should also gets you `pip3`, Python's package manager, but if not you can try `python3 -m ensurepip --upgrade`.
4. Clone the Hyp repo. If you have SSH keys added to GitHub run `git clone git@github.com:Murphydbuffalo/hyp2.git`, otherwise run `git clone https://github.com/Murphydbuffalo/hyp2.git`
5. `cd hyp2` (the original Hyp was a very terrible Ruby Gem, thus the name "Hyp2").
6. Set up a *virtual env* for the project: `python3 -m venv .`. A virtual env does two things. First, it allows us to install the dependencies we need for Hyp into a directory specific to this project, which means installing those same dependencies globally or for another project won't overwrite a dependency with a different version. Second, it allows us to use a specific version of Python and Pip for the project. After running this command you should see a `./lib/python3.9/site-packages` directory. This is where our Hyp-specific installations of dependencies will live (as opposed to some global `site-packages` directory). You should also see a `./bin` directory, including among other things executables for `pip` and `python` that symlink to the version of Python you used to run the `python3 -m venv.` command earlier.
7. Run `source ./bin/activate`. This tells your computer to use the executables in `./bin` by prepending that directory to your `PATH`. You can check that this worked by running `echo $PATH`, or by running `python -V` and seeing that your `python` executable points to some version of Python 3, not the system default of Python 2.
8. Install the dependencies: `pip install -r requirements.txt`.
9. I highly recommend making a shell alias so you don't forget to active your virtual env. I have something like `alias hyp="cd ~/Code/hyp2 && source ./bin/activate"` in my shell config file.
10. `cd ./web`. Most of the work you do will be inside this directory. The top level directory is mainly for configuration files.
11. Install and run PostgreSQL: `brew install postgresql` and then `brew services start postgresql`.
If everything is set up correctly you should be able to run the server with `python manage.py runserver`. Congrats! If there are issues with your Postgres setup you can investigate by looking at the log file: `tail -n 500 /usr/local/var/log/postgres.log`.
12. Install and run Redis: `brew install redis` and then `brew services start redis`. Redis is the back-end for the job processing tool we use, RQ. RQ is very similar to Resque from the Ruby world.
13. Create the development database: `createdb hyp2`. `createdb` is a command provided by Postgres.
14. Run the database migrations: `./helper_scripts/migrate`. By the way, this `helper_scripts` directory is something I added for convenience. Feel free to make PRs that add new scripts or update existing ones.
15. Create a superuser for yourself: `./helper_scripts/user`
16. Start the app by running `./helper_scripts/app`. You should be able to login as the superuser you just created. Under the hood this helper script is actually doing three things: starting the Django server, starting an RQ worker process, and watching all of the files in `web/hyp/static/scss` for changes. If any of the Sass files changes they'll get compiled to CSS in `web/hyp/static/css`, which is what we actually serve to clients.
17. Run the tests `./helper_scripts/test`. If you see a warning about a `web/staticfiles` directory it's nothing to worry about. We include that directory `.gitignore` because it is meant to contain our compiled production static assets. You can make the warning go away by running `mkdir ./web/staticfiles`.
18. Fire up a Python REPL with all of the Hyp code available for import: `./helper_scripts/shell`.

If you're on a Linux system things should largely be the same, with some key differences being:
1. You'll be using something like `apt` to fetch dependencies.
2. You'll need to use something like Ubuntu's `service` command to run Postgres, rather than Homebrew services.
3. *You'll need to install the Python dev package so that dependencies with native code can compile successfully.* To do this you can run `sudo apt-get install python3-dev`.

### Useful Django commands
Django provides `manage.py` script inside `web` that can be used to do things
like start the development server, run tests, open up REPLs, create and run migrations, create superusers, etc. Check out the [full list of commands here](https://docs.djangoproject.com/en/3.1/ref/django-admin/#available-commands).

Most of the time you can just use the relevant script in `web/helper_scripts`,
which will call these commands with some added conveniences. However, feel free
to experiment with running the django commands yourself, eg:
1. Run `python manage.py migrate` to run database migrations.
2. Run `python manage.py runserver` to start your development server.
3. Run `python manage.py test hyp/tests --settings web.settings.testing` to run the test suite.
4. Run `python manage.py shell` to run a Python REPL from which you can `import`
any code you want to play around with.

## Debug toolbar
We use a package called `django-debug-toolbar` that is loaded up on any non-superuser
HTML page. On those pages you'll see a little `DjDT` icon on the right-hand side
of the page. Click on that to see things like database queries, static assets on
the page, and errors.

## Linting
We use Flake8, and will eventually use ESlint, to lint our Python and JS code, respectively. Install the necessary plugins to have these linters run in your text editor.

See `.flake8` and `.eslintrc` for the relevant configurations for those tools.

## Continuous Integration
We use GitHub Actions for continuous integration. See `.github/workflows` for
how that is set up.

The test suite and linter will run every time you push to a branch. A script to
deploy to Heroku will run whenever changes are merged into `main`.

See `Procfile`, `runtime.txt`, and `heroku.sh` for Heroku-related scripts and config

We also have GitHub's Dependabot set up to automatically make PRs for fixing
security vulnerabilities by upgrading dependencies. See `.github/dependabot.yml`
for details.

## Postman
Postman is great for playing around with the API. We have a team account with
some ready-to-go requests against the API.

## Documentation
Every API endpoint should be documented (in Apiary? Postman? It's a TODO) and have tests written for it.

## Accessibility
We aim to make all of our UI accessible. This means writing semantic HTML, adding
`tabindex` attributes where necessary, and (hopefully rarely) adding ARIA attributes
for JS-heavy code.

## Internationalization
We aim to make it easy to provide translations for all of our copy. Via I18n and Google Translate? It's a TODO.
