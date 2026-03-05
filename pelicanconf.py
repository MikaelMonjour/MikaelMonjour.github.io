#!/usr/bin/env python
"""Pelican configuration file for Blog de Mikael."""

AUTHOR = 'Mikael Monjour'
SITENAME = 'Blog de Mikael'
SITEURL = ''

PATH = 'content'
OUTPUT_PATH = '.'

TIMEZONE = 'Europe/Paris'
DEFAULT_LANG = 'fr'
LOCALE = ('fr_FR.UTF-8',)

# Feed generation
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/{slug}.atom.xml'
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Theme
THEME = 'theme'

# Static paths — copier les images dans output/
STATIC_PATHS = ['images']

# URL settings — articles à la racine (pas de sous-dossier)
ARTICLE_URL = '{slug}.html'
ARTICLE_SAVE_AS = '{slug}.html'
PAGE_URL = 'pages/{slug}.html'
PAGE_SAVE_AS = 'pages/{slug}.html'
CATEGORY_URL = 'category/{slug}.html'
CATEGORY_SAVE_AS = 'category/{slug}.html'
TAG_URL = 'tag/{slug}.html'
TAG_SAVE_AS = 'tag/{slug}.html'
AUTHOR_URL = 'author/{slug}.html'
AUTHOR_SAVE_AS = 'author/{slug}.html'
ARCHIVES_SAVE_AS = 'archives.html'
AUTHORS_SAVE_AS = 'authors.html'
CATEGORIES_SAVE_AS = 'categories.html'
TAGS_SAVE_AS = 'tags.html'

# Social links
SOCIAL = (('atom feed', '/feeds/all.atom.xml'),)

# Pagination
DEFAULT_PAGINATION = False

# Plugins
PLUGINS = []

# Markdown extensions
MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {'css_class': 'highlight'},
        'markdown.extensions.extra': {},
        'markdown.extensions.meta': {},
        'markdown.extensions.toc': {},
    },
    'output_format': 'html5',
}

# Don't process these files
READERS = {'html': None}
