# Blog de Mikael

[![GitHub Pages](https://img.shields.io/badge/Live-mikaelmonjour.github.io-16a34a?style=flat&logo=github)](https://mikaelmonjour.github.io/)

Blog technique de **Mikael Monjour** — developpeur Python et passionné de bug bounty.

> Python, data, sécurité offensive, regex, statistiques — des articles techniques avec des exemples concrets et du code prêt à l'emploi.

## Articles

### Python & Data

- [Le module regex en Python : le guide complet pour aller au-delà de re](https://mikaelmonjour.github.io/le-module-regex-python-guide-complet.html) — Fuzzy matching, patterns récursifs, captures multiples, ensembles imbriqués, correspondances partielles : tout ce que le module `regex` apporte de plus que `re`, avec des exemples concrets.

- [La signification de la valeur p (p-value) — Exemple avec Python](https://mikaelmonjour.github.io/la-signification-de-la-valeur-p-exemple-python.html) — Ce que la p-value mesure vraiment, les pièges à éviter (peeking, comparaisons multiples), un exemple CRM avec du code Python, et une checklist complète avant/pendant/après un test.

### Sécurité offensive

- [Recon Everything : le guide complet de la reconnaissance en sécurité offensive](https://mikaelmonjour.github.io/recon-everything-guide-growth-hacker-securite.html) — Méthodologie, outils (Amass, Subfinder, Nmap, Nuclei...) et commandes pour la phase de reconnaissance en bug bounty et pentest.

### Lectures & culture tech

- [Mes lectures tech incontournables : top 10](https://mikaelmonjour.github.io/mes-lectures-tech-incontournables-top-10.html) — 10 livres techniques qui m'ont marqué : Clean Code, The Pragmatic Programmer, Hacking: The Art of Exploitation, et d'autres.

## Stack technique

| Composant | Technologie |
|---|---|
| Générateur | [Pelican](https://getpelican.com/) (Python) |
| Hébergement | [GitHub Pages](https://pages.github.com/) |
| Thème | Custom — minimaliste, responsive |
| Typographie | [Inter](https://fonts.google.com/specimen/Inter) (Google Fonts) |
| Design | Fond blanc, accents verts `#16a34a`, cartes arrondies |

## Structure du projet

```
├── index.html                              # Page d'accueil
├── le-module-regex-python-guide-complet.html
├── la-signification-de-la-valeur-p-exemple-python.html
├── recon-everything-guide-growth-hacker-securite.html
├── mes-lectures-tech-incontournables-top-10.html
├── archives.html
├── theme/
│   ├── css/main.css                        # Styles principaux
│   └── css/reset.css                       # Reset CSS
├── category/                               # Pages par catégorie
├── tag/                                    # Pages par tag
├── author/                                 # Pages par auteur
└── feeds/                                  # Flux Atom/RSS
```

## Lancer en local

```bash
git clone https://github.com/mikaelmonjour/mikaelmonjour.github.io.git
cd mikaelmonjour.github.io
python3 -m http.server 5000
```

Ouvrir [http://localhost:5000](http://localhost:5000).

## Tags

`python` · `regex` · `data` · `statistiques` · `securite` · `bug-bounty` · `recon` · `tech` · `livres`

## Auteur

**Mikael Monjour** — [mikaelmonjour.github.io](https://mikaelmonjour.github.io/)

---

*Ce blog est un site statique hébergé sur GitHub Pages. Les articles sont écrits en HTML et servis directement sans build côté serveur.*
