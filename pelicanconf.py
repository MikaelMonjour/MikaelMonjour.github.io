#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = "Mikael Monjour"
SITENAME = "Blog de Mikael"
SITEURL = ""

PATH = "content"

TIMEZONE = "Europe/Paris"

DEFAULT_LANG = "fr"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None


# Social widget
SOCIAL = (("You can add links in your config file", "#"),
          ("Another social link", "#"),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

# NEST Template
THEME = "nest"
SITESUBTITLE = "My Awesome Blog"
# Minified CSS
NEST_CSS_MINIFY = True
# Add items to top menu before pages
MENUITEMS = [("Homepage", "/"),("Categories","/categories.html")]
# Add header background image from content/images : "background.jpg"
NEST_HEADER_IMAGES = ""
NEST_HEADER_LOGO = "/images/logo.png"
# Footer
NEST_SITEMAP_COLUMN_TITLE = "Sitemap"
NEST_SITEMAP_MENU = [("Archives", "/archives.html"),("Tags","/tags.html"), ("Authors","/authors.html")]
NEST_SITEMAP_ATOM_LINK = "Atom Feed"
NEST_SITEMAP_RSS_LINK = "RSS Feed"
NEST_SOCIAL_COLUMN_TITLE = "Social"
NEST_LINKS_COLUMN_TITLE = "Links"
NEST_COPYRIGHT = "&copy; blogname 2015"
# Footer optional
NEST_FOOTER_HTML = ""
# index.html
NEST_INDEX_HEAD_TITLE = "Acceuil"
NEST_INDEX_HEADER_TITLE = "My Awesome Blog"
NEST_INDEX_HEADER_SUBTITLE = "Smashing The Stack For Fun And Profit"
NEST_INDEX_CONTENT_TITLE = "Last Posts"
# archives.html
NEST_ARCHIVES_HEAD_TITLE = "Archives"
NEST_ARCHIVES_HEAD_DESCRIPTION = "Posts Archives"
NEST_ARCHIVES_HEADER_TITLE = "Archives"
NEST_ARCHIVES_HEADER_SUBTITLE = "Archives for all posts"
NEST_ARCHIVES_CONTENT_TITLE = "Archives"
# article.html
NEST_ARTICLE_HEADER_BY = "By"
NEST_ARTICLE_HEADER_MODIFIED = "modified"
NEST_ARTICLE_HEADER_IN = "in category"
# author.html
NEST_AUTHOR_HEAD_TITLE = "Posts by"
NEST_AUTHOR_HEAD_DESCRIPTION = "Posts by"
NEST_AUTHOR_HEADER_SUBTITLE = "Posts archives"
NEST_AUTHOR_CONTENT_TITLE = "Posts"
# authors.html
NEST_AUTHORS_HEAD_TITLE = "Author list"
NEST_AUTHORS_HEAD_DESCRIPTION = "Author list"
NEST_AUTHORS_HEADER_TITLE = "Author list"
NEST_AUTHORS_HEADER_SUBTITLE = "Archives listed by author"
# categories.html
NEST_CATEGORIES_HEAD_TITLE = "Categories"
NEST_CATEGORIES_HEAD_DESCRIPTION = "Archives listed by category"
NEST_CATEGORIES_HEADER_TITLE = "Categories"
NEST_CATEGORIES_HEADER_SUBTITLE = "Archives listed by category"
# category.html
NEST_CATEGORY_HEAD_TITLE = "Category Archive"
NEST_CATEGORY_HEAD_DESCRIPTION = "Category Archive"
NEST_CATEGORY_HEADER_TITLE = "Category"
NEST_CATEGORY_HEADER_SUBTITLE = "Category Archive"
# pagination.html
NEST_PAGINATION_PREVIOUS = "Previous"
NEST_PAGINATION_NEXT = "Next"
# period_archives.html
NEST_PERIOD_ARCHIVES_HEAD_TITLE = "Archives for"
NEST_PERIOD_ARCHIVES_HEAD_DESCRIPTION = "Archives for"
NEST_PERIOD_ARCHIVES_HEADER_TITLE = "Archives"
NEST_PERIOD_ARCHIVES_HEADER_SUBTITLE = "Archives for"
NEST_PERIOD_ARCHIVES_CONTENT_TITLE = "Archives for"
# tag.html
NEST_TAG_HEAD_TITLE = "Tag archives"
NEST_TAG_HEAD_DESCRIPTION = "Tag archives"
NEST_TAG_HEADER_TITLE = "Tag"
NEST_TAG_HEADER_SUBTITLE = "Tag archives"
# tags.html
NEST_TAGS_HEAD_TITLE = "Tags"
NEST_TAGS_HEAD_DESCRIPTION = "Tags List"
NEST_TAGS_HEADER_TITLE = "Tags"
NEST_TAGS_HEADER_SUBTITLE = "Tags List"
NEST_TAGS_CONTENT_TITLE = "Tags List"
NEST_TAGS_CONTENT_LIST = "tagged"
# Static files
STATIC_PATHS = ["content/images", "extra/robots.txt", "extra/favicon.ico", "extra/logo.svg"]
EXTRA_PATH_METADATA = {
    "extra/robots.txt": {"path": "robots.txt"},
    "extra/favicon.ico": {"path": "favicon.ico"}, 
}