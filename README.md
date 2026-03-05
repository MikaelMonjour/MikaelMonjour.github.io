# Blog de Mikael

[![GitHub Pages](https://img.shields.io/badge/Live-mikaelmonjour.github.io-16a34a?style=flat&logo=github)](https://mikaelmonjour.github.io/)
[![Pelican](https://img.shields.io/badge/Pelican-4.11-3776AB?style=flat&logo=python&logoColor=white)](https://getpelican.com/)
[![Articles](https://img.shields.io/badge/Articles-7-blue?style=flat)]()

Blog technique de **Mikael Monjour** — développeur Python et passionné de sécurité offensive.

> Python, data, sécurité offensive, analyse réseau, regex, statistiques — des articles techniques avec des exemples concrets et du code prêt à l'emploi.

---

## Articles

### Python & data

- **[La librairie regex en Python : guide complet](https://mikaelmonjour.github.io/le-module-regex-python-guide-complet.html)** — Fuzzy matching, patterns récursifs, captures multiples, ensembles imbriqués, correspondances partielles, propriétés Unicode : tout ce que le package `regex` (`pip install regex`) apporte au-delà du module standard `re`.

- **[La signification de la valeur p (p-value) — Exemple avec Python](https://mikaelmonjour.github.io/la-signification-de-la-valeur-p-exemple-python.html)** — Ce que la p-value mesure vraiment, les pièges à éviter (peeking, comparaisons multiples), un exemple CRM avec du code Python, et une checklist complète avant/pendant/après un test.

### Réseau & sécurité offensive

- **[tcpdump : guide complet de l'analyseur de paquets réseau](https://mikaelmonjour.github.io/tcpdump-guide-complet.html)** — Commandes de base, filtres avancés, horodatage, requêtes HTTP, drapeaux TCP, mode promiscuous, intégration Wireshark, et aide-mémoire complet. Inclut des diagrammes Mermaid.

- **[Programmation socket en Python : guide complet](https://mikaelmonjour.github.io/programmation-socket-python-guide-complet.html)** — Sockets TCP/UDP, gestion de connexions multiples avec `select()`, ordre des octets, protocoles applicatifs, et exemples client/serveur prêts à l'emploi.

- **[Recon Everything : guide complet de la reconnaissance en sécurité](https://mikaelmonjour.github.io/recon-everything-guide-growth-hacker-securite.html)** — Méthodologie, outils (Amass, Subfinder, Nmap, Nuclei…) et commandes pour la phase de reconnaissance en bug bounty et pentest.

### Lectures & culture tech

- **[Mes lectures tech incontournables : top 10](https://mikaelmonjour.github.io/mes-lectures-tech-incontournables-top-10.html)** — 10 livres techniques qui m'ont marqué : Clean Code, The Pragmatic Programmer, Hacking: The Art of Exploitation, et d'autres.

---

## Stack technique

| Composant | Technologie |
|-----------|-------------|
| Générateur | [Pelican 4.11](https://getpelican.com/) (Python) |
| Hébergement | [GitHub Pages](https://pages.github.com/) |
| Thème | Custom — minimaliste, responsive |
| Typographie | [Inter](https://fonts.google.com/specimen/Inter) (Google Fonts) |
| Diagrammes | [Mermaid.js](https://mermaid.js.org/) |
| Coloration | [Highlight.js](https://highlightjs.org/) |
| Design | Fond blanc, accents verts `#16a34a`, cartes arrondies |

---

## Structure du projet

```
├── content/                                 # Articles en Markdown (source)
│   ├── le-module-regex-python-guide-complet.md
│   ├── tcpdump-guide-complet.md
│   ├── programmation-socket-python-guide-complet.md
│   ├── la-signification-de-la-valeur-p-exemple-python.md
│   ├── recon-everything-guide-growth-hacker-securite.md
│   ├── mes-lectures-tech-incontournables-top-10.md
│   ├── my-first-post.md
│   └── images/
├── theme/
│   ├── templates/                           # Templates Jinja2
│   │   ├── base.html
│   │   ├── article.html
│   │   ├── index.html
│   │   └── ...
│   └── css/
│       ├── main.css                         # Styles principaux
│       ├── pygment.css                      # Coloration syntaxique
│       └── reset.css                        # Reset CSS
├── pelicanconf.py                           # Configuration Pelican
├── publishconf.py                           # Configuration de publication
├── Makefile                                 # Commandes de build
├── *.html                                   # Pages générées (output à la racine)
├── category/                                # Pages par catégorie
├── tag/                                     # Pages par tag
├── author/                                  # Pages par auteur
└── feeds/                                   # Flux Atom
```

---

## Lancer en local

### Avec Pelican (recommandé)

```bash
git clone git@github.com:MikaelMonjour/MikaelMonjour.github.io.git
cd MikaelMonjour.github.io

# Créer l'environnement virtuel
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Builder le site
pelican content -s pelicanconf.py

# Servir en local
python3 -m http.server 5000
```

Ouvrir [http://localhost:5000](http://localhost:5000).

### Serveur statique simple

```bash
# Sans Pelican — juste servir les HTML existants
python3 -m http.server 5000
```

---

## Ajouter un article

1. Créer un fichier `.md` dans `content/` avec les métadonnées Pelican :

```markdown
Title: Mon titre
Date: 2026-03-05 18:00
Category: tech
Tags: python, tech
Slug: mon-slug
Author: Mikael Monjour
Summary: Description courte de l'article.

## Contenu de l'article...
```

2. Builder :

```bash
source .venv/bin/activate
pelican content -s pelicanconf.py
```

3. Commit et push :

```bash
git add -A
git commit -m "Ajout article : Mon titre"
git push origin master
```

---

## Tags

`python` · `regex` · `data` · `statistiques` · `securite` · `reseau` · `outils` · `bug-bounty` · `recon` · `tech` · `livres`

## Auteur

**Mikael Monjour** — [mikaelmonjour.github.io](https://mikaelmonjour.github.io/)

---

*Site statique généré avec [Pelican](https://getpelican.com/) à partir d'articles Markdown, hébergé sur GitHub Pages.*
