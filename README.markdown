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
3. Install Python 3: `brew install python`. This also gets you `pip`, Python's package manager.
4. Install Virtualenv: `pip install virtualenv`. This is a library for managing the dependencies in your
Python project. It lets you install different versions of packages for specific projects.
5. Clone the Hyp repo. If you have SSH keys added to GitHub run `git clone git@github.com:Murphydbuffalo/hyp2.git`, otherwise run `git clone https://github.com/Murphydbuffalo/hyp2.git`
6. `cd hyp2` (the original Hyp was a very terrible Ruby Gem, thus the name "Hyp2").
7. `source/bin/activate`. This "activates" the virtual env, meaning commands you
run will use the version of Python and dependencies specified by the project.
The Python version is specified by `pyvenv.cfg` and the dependencies by `requirements.txt`. You can always run `deactivate` to get out of the virtual env.
8. Install the dependencies: `pip install -r requirements.txt`.
9. `cd web`. Most of the work you do will be inside this directory. The top level
directory is mainly for configuration files.
10. Install and run PostgreSQL: `brew install postgresql` and then `brew services start postgresql`.
If everything is set up correctly you should be able to run the server with `python manage.py runserver`. Congrats!
11. Debugging issues with your Postgres setup. If something is not working with Postgres you can
investigate by looking at the log file: `tail -n 500 /usr/local/var/log/postgres.log`.

### Useful Django commands
Django provides `manage.py` script inside `web` that can be used to do things
like start the development server, run tests, open up REPLs, create and run migrations, create superusers, etc. Check out the [full list of commands here](https://docs.djangoproject.com/en/3.1/ref/django-admin/#available-commands).

1. Run `python manage.py migrate` to run database migrations.
2. Run `python manage.py runserver` to start your development server.
3. Run `python manage.py test hyp/tests` to run the test suite.
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
deploy to Heroku will run whenever changes are merged into `master`.

See `Procfile`, `runtime.txt`, and `heroku.sh` for Heroku-related scripts and config

We also have GitHub's Dependabot set up to automatically make PRs for fixing
security vulnerabilities by upgrading dependencies. See `.github/dependabot.yml`
for details.

## Postman
Postman is great for playing around with the API.

## Documentation
Every API endpoint should be documented (in Apiary? Postman? It's a TODO) and have tests written for it.

## Accessibility
We aim to make all of our UI accessible. This means writing semantic HTML, adding
`tabindex` attributes where necessary, and (hopefully rarely) adding ARIA attributes
for JS-heavy code.

## Internationalization
We aim to make it easy to provide translations for all of our copy. Via I18n and Google Translate? It's a TODO.
