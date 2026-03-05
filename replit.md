# Blog de Mikael

## Overview
A static HTML blog by Mikael Monjour, originally generated with Pelican (Python static site generator). The theme has been redesigned with a modern, minimal aesthetic inspired by baselinedesign.io (clean white, green accents, Inter font).

## Project Structure
- `index.html` — Home page with featured article and posts list
- `le-module-regex-python-guide-complet.html` — Module regex Python : guide complet (fuzzy matching, patterns récursifs, captures multiples, etc.)
- `la-signification-de-la-valeur-p-exemple-python.html` — P-value expliquée avec Python (AIDA + growth storytelling)
- `recon-everything-guide-growth-hacker-securite.html` — Recon Everything security guide article
- `mes-lectures-tech-incontournables-top-10.html` — Top 10 tech reads article
- `My-first-post.html` — Original blog post
- `theme/css/main.css` — Main stylesheet (modern redesign)
- `theme/css/reset.css` — CSS reset
- `theme/css/wide.css` — Wide layout (imports main.css)
- `theme/fonts/` — Yanone Kaffeesatz font files
- `images/` — Blog images (eduba.png)
- `feeds/` — Atom RSS feeds
- `category/` — Category pages (misc, tech)
- `tag/` — Tag pages (first, misc, python, livres, tech, lectures, securite, recon, bug-bounty, outils, data, statistiques, regex)
- `author/` — Author pages (your-name, mikael-monjour)
- `archives.html`, `tags.html`, `categories.html`, `authors.html` — Index pages

## Categories
- **misc** — Original miscellaneous category
- **tech** — Technical articles (lectures, Python, etc.)

## Running the Project
The site is served using Python's built-in HTTP server:
```
python3 -m http.server 5000 --bind 0.0.0.0
```

## Deployment
Configured as a **static** deployment with `publicDir: "."`.

## Design
- Font: Inter (Google Fonts) + Yanone Kaffeesatz (local)
- Colors: white background, green accents (#16a34a), gray text hierarchy
- Layout: 720px max-width, responsive with mobile breakpoints
- Components: pill-shaped nav buttons, card-style featured articles, clean footer
