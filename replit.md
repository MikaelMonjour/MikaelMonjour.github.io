# Blog de Mikael

## Overview
A static HTML blog generated with Pelican (Python static site generator). This is a pre-built static site — no build step is required.

## Project Structure
- `index.html` — Home page
- `My-first-post.html` — Blog post
- `theme/` — CSS stylesheets and fonts
- `images/` — Blog images
- `feeds/` — Atom RSS feeds
- `category/`, `tag/`, `author/` — Generated category/tag/author pages

## Running the Project
The site is served using Python's built-in HTTP server:
```
python3 -m http.server 5000 --bind 0.0.0.0
```

## Deployment
Configured as a **static** deployment with `publicDir: "."`.
