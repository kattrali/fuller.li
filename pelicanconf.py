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

DIRECT_TEMPLATES = ('index', 'posts_index', 'tags',)
PAGINATED_DIRECT_TEMPLATES = ('posts_index',)

POSTS_URL = 'posts/'
POSTS_INDEX_SAVE_AS = 'posts/index.html'

ARTICLE_DIR = 'posts'
ARTICLE_URL = 'posts/{slug}/'
ARTICLE_SAVE_AS = 'posts/{slug}/index.html'
TAG_URL = 'posts/tags/{slug}/'
TAG_SAVE_AS = 'posts/tags/{slug}/index.html'
TAGS_SAVE_AS = 'posts/tags/index.html'

PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'

FEED_RSS = 'posts/feed/latest'

PLUGIN_PATH = 'plugins'
PLUGINS = ['assets', 'summary']
SUMMARY_END_MARKER = '---'

MIXPANEL = 'a688ce764b5d3ca9f51898b03783a4e6'

