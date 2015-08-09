from __future__ import unicode_literals
from os import environ
import json


SUMMARY_MAX_LENGTH = 90

AUTHOR = 'Kyle Fuller'
SITENAME = 'Kyle Fuller'
EMAIL = 'kyle@fuller.li'
SITEURL = environ.get('PELICAN_SITEURL', 'https://fuller.li')

THEME = 'theme'

TIMEZONE = 'Europe/London'
DISQUS_SITENAME = 'kylefuller'

DEFAULT_PAGINATION = 0

RELATIVE_URLS = False

DIRECT_TEMPLATES = ('index', 'posts_index', 'tags', 'speaking', 'slides', 'talks',)
PAGINATED_DIRECT_TEMPLATES = ('posts_index',)

POSTS_URL = 'posts/'
POSTS_INDEX_SAVE_AS = 'posts/index.html'

ARTICLE_PATHS = ('posts',)
ARTICLE_URL = 'posts/{slug}/'
ARTICLE_SAVE_AS = 'posts/{slug}/index.html'
TAG_URL = 'posts/tags/{slug}/'
TAG_SAVE_AS = 'posts/tags/{slug}/index.html'
TAGS_SAVE_AS = 'posts/tags/index.html'

PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'

FEED_RSS = 'posts/feed/latest'
FEED_ATOM = 'posts/feed/latest.atom'

PLUGIN_PATHS = ('plugins',)
PLUGINS = ['assets', 'summary']
SUMMARY_END_MARKER = '---'

# Assets (plugins)
ASSET_SOURCE_PATHS = ('static',)

MIXPANEL = 'a688ce764b5d3ca9f51898b03783a4e6'

# Speaking

SPEAKING_SAVE_AS = 'speaking/index.html'
TALKS_SAVE_AS = 'talks/index.html'
SLIDES_SAVE_AS = 'slides/index.html'

with open('talks.json', 'r') as fp:
    TALKS = json.load(fp)
    PAST_TALKS = filter(lambda talk: talk.get('status') != 'upcoming', TALKS)
    UPCOMING_TALKS = filter(lambda talk: talk.get('status') == 'upcoming', TALKS)
    RECENT_TALKS = TALKS[:5]

