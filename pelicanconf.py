from __future__ import unicode_literals
from os import environ


SUMMARY_MAX_LENGTH = 90

AUTHOR = 'Kyle Fuller'
SITENAME = 'Kyle Fuller'
SITEURL = environ.get('PELICAN_SITEURL', 'http://kylefuller.co.uk')

THEME = 'theme'

TIMEZONE = 'Europe/London'
DISQUS_SITENAME = 'kylefuller'

DEFAULT_PAGINATION = 0

RELATIVE_URLS = False

ARTICLE_DIR = 'posts'
ARTICLE_URL = 'posts/{slug}/'
ARTICLE_SAVE_AS = 'posts/{slug}/index.html'

PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'

FEED_RSS = 'posts/feed/latest'

PLUGIN_PATH = 'plugins'
PLUGINS = ['assets']

