## Blurb App

The blurb app allows you to manage static text within the database. Here, we
refer to each piece of static text as _blurbs_.

You can use the _blurb_ template tag to add blurbs in your template. The first
time you render the template, the corresponding Blurb objects will be created
in the database. Then, you can go to the admin console to fill out the text
content.

Note that rendering an incomplete blurb in non debug-mode will result in an
internal server error.

### Usage

Create and render a template such as the following

```html
{% load blurb %}

<h1>Intro</h1>

<p>
  {% blurb 'intro:content' %}
</p>
```

Then, a Blurb object will be created with (page=intro, name=content).
Go to the admin console and fill out the static text content. Reload your template,
and the blurb should display the text.

### Data Export/Import

Since the static text is stored in the database, each environment will have a
different set of blurbs. We recommend that you

1. Write new blurbs in your local development deployment
2. Export changes from your production deployment and import them to your
   development deployment.
3. Export changes (the new blurbs) from your development deployment and import
   them to your production deployment.

Refer to the Django docs on [data import/export](https://docs.djangoproject.com/en/2.2/ref/django-admin/#dumpdata)

```shell
python manage.py dumpdata blurb > data.json
```

```shell
python manage.py loaddata data.json
```
