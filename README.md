# Django Templates

## Requirements

Python 3.6.x or 3.7.x should work without problems. This template is being built mainly on 3.6.5.

## Getting Started

### Initialize `.env`

For now, just copy the example file.

```
cp .env.example .env
```

### Initialize Virtual Environment Via `venv`

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Runserver

```
python manage.py runserver
```

## Environment Variables

### Deployment Stage

Django only provides the boolean variable `DEBUG` for differentiating deployment stages. In this template, we provide a `DJANGO_ENV` variable in `settings.py`, which is read from your environment variable: `DJANGO_IVR_ENV` (default is `'DEV'`).

Note that you can use any value for `DJANGO_ENV` and it is your choice on how to set the value of `DEBUG` for each value of `DJANGO_ENV`. This is the default.

```
if DJANGO_ENV == 'DEV':
  DEBUG = True
else:
  DEBUG = True
```

You don't need to set `DEBUG = False` for production at the beginning of your project IMHO.

> This pattern is inspired by Node's `NODE_ENV`.

### Other Environment Variables

For other environment variables such as SECRET_KEY, social authentication keys, etc., we use the `.env` pattern. Refer to the `.env.example` file.

You should have a `.env` file at the root of your project, with the same format as `.env.example`. This file should not be checked into version control, and each deployment may have different `.env` files.

> This pattern is inspired by `dotenv` from Node.

## Apache + `mod-wsgi` Deployment

I might make a script for this. For now, refer to [this article in my very very useful wiki](https://github.com/itsnamgyu/ugh/wiki/Django-Deployment-on-Apache) or [my older wiki](https://github.com/itsnamgyu/django-two/wiki) for additional info.

## Blurb App

Don't you just hate writing long paragraphs inside HTML? You could put it inside the code or use some external text file, but who's got time for that?.i

The blurb app provides models and template tags that allow you to easily include DB-stored static strings in templates and edit those strings from the admin console. Here, we call these static strings, `blurb`s.

> Drawback: It doesn't support formatted text yet. It does support linebreaks tho!

### Usage: Adding A Blurb

1. Load the blurb tag at the start of a template
```django-html
{% load blurb %}
```

2. Add a blurb to the page with some meaningful identifier.
```django-html
{% blurb 'index/title' %}
```

3. Attempt to load the template in debug mode. This automatically creates a null blurb in your DB associated with that identifier. The template will now show a message, telling you that you need to fill in the contents of that blurb.

4. Go to the admin console and edit the content of that blurb.

5. Load the template again, and you'll see your content, right there! You can edit the text at any time!

### Usage: Migrating To Another Environment

Since the blurbs are stored in the DB, you need to migrate them for each environment. This should be your typical flow.

1. Add a blurb with initial content in your local development environment.

2. Migrate your initial blurb content to production and deploy.

3. Edit the blurbs from the production admin console.

4. (Optional) migrate the production changes back to your local environment.

5. Continue development in your local environment.

Here, you can use Django's fixtures feature. Just do this:

1. Export blurbs
```
python manage.py exportdata blurb > blurbs.json  # blurb refers to the name of the Django app
```

2. Import blurbs
```
python manage.py loaddata blurbs.json
```

## Guess What?

Ur done. Thank me later.
