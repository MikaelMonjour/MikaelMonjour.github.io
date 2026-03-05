# Blog de Mikael

Blog personnel de **Mikael Monjour** — développeur Python, Growth Engineer chez SumUp et professeur à Eduba.

## Aperçu

Un blog statique construit avec [Pelican](https://getpelican.com/), avec un thème moderne et minimaliste : fond blanc, accents verts, typographie Inter, cartes arrondies et mise en page responsive.

## Articles

- **Mes lectures tech incontournables : top 10** — Une sélection de 10 livres techniques qui ont marqué mon parcours de développeur.
- **My first post** — Le tout premier article du blog.

## Structure du projet

```
├── index.html                # Page d'accueil
├── mes-lectures-tech-*.html  # Article lectures tech
├── My-first-post.html        # Premier article
├── archives.html             # Archives
├── tags.html                 # Index des tags
├── categories.html           # Index des catégories
├── authors.html              # Index des auteurs
├── theme/
│   ├── css/main.css          # Feuille de style principale
│   ├── css/reset.css         # Reset CSS
│   └── fonts/                # Polices locales
├── images/                   # Images du blog
├── feeds/                    # Flux Atom/RSS
├── category/                 # Pages par catégorie
├── tag/                      # Pages par tag
└── author/                   # Pages par auteur
```

## Lancer en local

```bash
python3 -m http.server 5000 --bind 0.0.0.0
```

Puis ouvrir [http://localhost:5000](http://localhost:5000).

## Technologies

- HTML5 / CSS3
- [Pelican](https://getpelican.com/) (générateur de site statique)
- [Inter](https://fonts.google.com/specimen/Inter) (Google Fonts)
- Python (serveur de développement)

## Auteur

**Mikael Monjour**
- Growth Engineer @ [SumUp](https://sumup.com)
- Professeur Python @ [Eduba](https://eduba.school)
- [LinkedIn](https://fr.linkedin.com/in/mikaelmonjour)
