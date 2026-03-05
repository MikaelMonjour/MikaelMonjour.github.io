Title: Le module Regex Python : Guide Complet
Date: 2026-03-05 17:00
Category: tech
Tags: python, regex, tech
Slug: le-module-regex-python-guide-complet
Author: Mikael Monjour
Summary: Le module re de Python est un outil essentiel pour la manipulation de texte et la recherche de motifs. Ce guide couvre les bases du module re, les fonctions principales, et les cas d'utilisation courants.

## Les Expressions Régulières : C'est Quoi ?

Les expressions régulières (ou **regex**) sont un langage de motifs utilisé pour rechercher, valider ou manipuler du texte. Elles permettent de décrire des modèles complexes en quelques caractères.

En Python, le module `re` fournit toutes les fonctions nécessaires pour travailler avec les regex.

```python
import re
```

## Les Caractères Spéciaux (Métacaractères)

Voici les caractères qui ont une signification particulière dans les regex :

| Métacaractère | Description |
|---|---|
| `.` | N'importe quel caractère (sauf `\n`) |
| `^` | Début de chaîne |
| `$` | Fin de chaîne |
| `*` | 0 ou plusieurs répétitions |
| `+` | 1 ou plusieurs répétitions |
| `?` | 0 ou 1 répétition |
| `{}` | Nombre exact de répétitions |
| `[]` | Ensemble de caractères |
| `\` | Séquence spéciale ou échappement |
| `\|` | Ou (alternance) |
| `()` | Groupe de capture |

## Les Séquences Spéciales

Les séquences spéciales commencent par `\` et ont une signification prédéfinie :

| Séquence | Description | Exemple |
|---|---|---|
| `\d` | Un chiffre [0-9] | `\d+` → "123" |
| `\D` | Tout sauf un chiffre | `\D+` → "abc" |
| `\w` | Un caractère alphanumérique [a-zA-Z0-9_] | `\w+` → "hello_42" |
| `\W` | Tout sauf un alphanumérique | `\W+` → "!@#" |
| `\s` | Un espace blanc (espace, tab, newline) | `\s+` → " " |
| `\S` | Tout sauf un espace blanc | `\S+` → "hello" |
| `\b` | Frontière de mot | `\bcat\b` → "cat" dans "the cat sat" |
| `\B` | Pas une frontière de mot | `\Bcat\B` → "cat" dans "concatenate" |

## La Fonction `re.match()`

`re.match()` vérifie si le **début** de la chaîne correspond au motif. Si oui, elle retourne un objet `Match`. Sinon, elle retourne `None`.

```python
import re

pattern = r"Hello"
text = "Hello, World!"

result = re.match(pattern, text)

if result:
    print(f"Match trouvé : {result.group()}")  # "Hello"
    print(f"Position : {result.start()} à {result.end()}")  # 0 à 5
else:
    print("Pas de match")
```

**Attention :** `re.match()` ne cherche qu'au début de la chaîne. Pour chercher partout, utilisez `re.search()`.

```python
# match() ne trouve rien ici car "World" n'est pas au début
result = re.match(r"World", "Hello, World!")
print(result)  # None
```

## La Fonction `re.search()`

`re.search()` parcourt **toute** la chaîne et retourne le premier match trouvé.

```python
import re

text = "Mon numéro est 06-12-34-56-78"
result = re.search(r"\d{2}-\d{2}-\d{2}-\d{2}-\d{2}", text)

if result:
    print(f"Numéro trouvé : {result.group()}")  # "06-12-34-56-78"
    print(f"Position : {result.start()} à {result.end()}")
```

### Différence entre `match()` et `search()`

```python
text = "Le prix est 42 euros"

# match() cherche au début → pas de résultat pour un nombre
print(re.match(r"\d+", text))   # None

# search() cherche partout → trouve "42"
print(re.search(r"\d+", text))  # <re.Match object; span=(13, 15), match='42'>
```

## La Fonction `re.findall()`

`re.findall()` retourne **tous** les matches sous forme de liste de chaînes.

```python
import re

text = "Les prix sont : 10€, 25€, 42€ et 100€"
prices = re.findall(r"\d+", text)
print(prices)  # ['10', '25', '42', '100']
```

Avec des groupes de capture, `findall()` retourne les groupes :

```python
text = "Contact : alice@mail.com et bob@company.org"
emails = re.findall(r"(\w+)@(\w+\.\w+)", text)
print(emails)  # [('alice', 'mail.com'), ('bob', 'company.org')]
```

## La Fonction `re.finditer()`

`re.finditer()` retourne un **itérateur** d'objets `Match`, ce qui permet d'accéder aux positions et aux groupes de chaque match.

```python
import re

text = "Dates : 2024-01-15, 2024-03-20, 2024-12-31"
pattern = r"(\d{4})-(\d{2})-(\d{2})"

for match in re.finditer(pattern, text):
    print(f"Date : {match.group()}")
    print(f"  Année : {match.group(1)}")
    print(f"  Mois  : {match.group(2)}")
    print(f"  Jour  : {match.group(3)}")
    print(f"  Position : {match.start()}-{match.end()}")
```

## La Fonction `re.sub()`

`re.sub()` remplace les occurrences du motif par une chaîne de remplacement.

```python
import re

text = "Mon numéro est 06 12 34 56 78"

# Remplacer les espaces dans le numéro par des tirets
# On cible spécifiquement les espaces entre chiffres
clean = re.sub(r"(\d{2})\s", r"\1-", text)
print(clean)  # "Mon numéro est 06-12-34-56-78"
```

On peut aussi utiliser une **fonction** comme remplacement :

```python
def double_number(match):
    return str(int(match.group()) * 2)

text = "Les scores sont 10, 25 et 42"
result = re.sub(r"\d+", double_number, text)
print(result)  # "Les scores sont 20, 50 et 84"
```

## La Fonction `re.split()`

`re.split()` découpe une chaîne selon un motif regex.

```python
import re

text = "pomme, orange;  banane   kiwi"

# Découper par virgule, point-virgule ou espaces
fruits = re.split(r"[,;\s]+", text)
print(fruits)  # ['pomme', 'orange', 'banane', 'kiwi']
```

Avec `maxsplit` pour limiter le nombre de découpes :

```python
result = re.split(r"[,;\s]+", text, maxsplit=2)
print(result)  # ['pomme', 'orange', 'banane   kiwi']
```

## La Fonction `re.compile()`

`re.compile()` pré-compile un motif regex en objet `Pattern`. Utile quand on réutilise le même motif plusieurs fois.

```python
import re

# Compiler le motif une seule fois
email_pattern = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

texts = [
    "Contact : alice@example.com",
    "Pas d'email ici",
    "Écrivez à bob.smith@company.co.uk",
]

for text in texts:
    match = email_pattern.search(text)
    if match:
        print(f"Email trouvé : {match.group()}")
    else:
        print("Pas d'email")
```

## Les Groupes de Capture

Les parenthèses `()` créent des **groupes de capture** qui permettent d'extraire des parties spécifiques du match.

```python
import re

text = "2024-03-15 10:30:45"
pattern = r"(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})"

match = re.search(pattern, text)
if match:
    print(f"Match complet : {match.group(0)}")  # "2024-03-15 10:30:45"
    print(f"Année : {match.group(1)}")           # "2024"
    print(f"Mois : {match.group(2)}")            # "03"
    print(f"Jour : {match.group(3)}")            # "15"
    print(f"Heure : {match.group(4)}")           # "10"
    print(f"Minute : {match.group(5)}")          # "30"
    print(f"Seconde : {match.group(6)}")         # "45"
```

### Groupes Nommés

Les groupes nommés utilisent la syntaxe `(?P<nom>...)` pour donner un nom au groupe :

```python
import re

log = "2024-03-15 ERROR [auth] Login failed for user admin"
pattern = r"(?P<date>\d{4}-\d{2}-\d{2}) (?P<level>\w+) \[(?P<module>\w+)\] (?P<message>.+)"

match = re.search(pattern, log)
if match:
    print(f"Date : {match.group('date')}")       # "2024-03-15"
    print(f"Niveau : {match.group('level')}")     # "ERROR"
    print(f"Module : {match.group('module')}")    # "auth"
    print(f"Message : {match.group('message')}")  # "Login failed for user admin"
```

### Groupes Non-Capturants

`(?:...)` crée un groupe sans le capturer (utile pour le regroupement logique) :

```python
import re

# On veut matcher "http" ou "https" sans capturer le "s" optionnel
urls = "http://example.com et https://secure.com"
pattern = r"(?:https?://\S+)"

matches = re.findall(pattern, urls)
print(matches)  # ['http://example.com', 'https://secure.com']
```

## Les Drapeaux (Flags)

Les drapeaux modifient le comportement de la regex :

| Drapeau | Version courte | Description |
|---|---|---|
| `re.IGNORECASE` | `re.I` | Ignore la casse |
| `re.MULTILINE` | `re.M` | `^` et `$` matchent début/fin de chaque ligne |
| `re.DOTALL` | `re.S` | `.` matche aussi `\n` |
| `re.VERBOSE` | `re.X` | Permet les commentaires dans la regex |

```python
import re

# IGNORECASE : chercher sans distinction majuscule/minuscule
text = "Python est génial. PYTHON est puissant."
matches = re.findall(r"python", text, re.IGNORECASE)
print(matches)  # ['Python', 'PYTHON']

# VERBOSE : écrire une regex lisible avec des commentaires
email_pattern = re.compile(r"""
    [a-zA-Z0-9._%+-]+    # Nom d'utilisateur
    @                     # Arobase
    [a-zA-Z0-9.-]+        # Nom de domaine
    \.                    # Point
    [a-zA-Z]{2,}          # Extension (com, org, fr...)
""", re.VERBOSE)

print(email_pattern.search("test@example.com").group())  # "test@example.com"

# Combiner plusieurs drapeaux avec |
result = re.findall(r"^hello", "Hello\nhello\nHELLO", re.IGNORECASE | re.MULTILINE)
print(result)  # ['Hello', 'hello', 'HELLO']
```

## Les Assertions (Lookahead et Lookbehind)

Les assertions vérifient une condition sans consommer de caractères.

### Lookahead Positif `(?=...)`

Vérifie que le motif est **suivi** par quelque chose :

```python
import re

# Trouver les montants suivis de "€"
text = "Prix : 42€, 100$, 25€"
matches = re.findall(r"\d+(?=€)", text)
print(matches)  # ['42', '25']
```

### Lookahead Négatif `(?!...)`

Vérifie que le motif n'est **pas suivi** par quelque chose :

```python
# Trouver les nombres qui ne sont PAS suivis de "€"
matches = re.findall(r"\d+(?!€)", text)
print(matches)  # ['100']
```

### Lookbehind Positif `(?<=...)`

Vérifie que le motif est **précédé** par quelque chose :

```python
# Trouver les montants précédés de "Prix : "
text = "Prix : 42, Remise : 10"
matches = re.findall(r"(?<=Prix : )\d+", text)
print(matches)  # ['42']
```

### Lookbehind Négatif `(?<!...)`

Vérifie que le motif n'est **pas précédé** par quelque chose :

```python
# Trouver les nombres non précédés de "Prix : "
matches = re.findall(r"(?<!Prix : )\d+", text)
print(matches)  # ['10']
```

## Quantificateurs Gourmands vs Paresseux

Par défaut, les quantificateurs (`*`, `+`, `?`) sont **gourmands** : ils matchent le plus de caractères possible.

```python
import re

html = "<b>Gras</b> et <i>Italique</i>"

# Gourmand : matche tout entre le premier < et le dernier >
greedy = re.findall(r"<.+>", html)
print(greedy)  # ['<b>Gras</b> et <i>Italique</i>']

# Paresseux (ajouter ?) : matche le minimum
lazy = re.findall(r"<.+?>", html)
print(lazy)  # ['<b>', '</b>', '<i>', '</i>']
```

## Cas d'Utilisation Courants

### Valider un email

```python
import re

def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))

print(is_valid_email("user@example.com"))    # True
print(is_valid_email("invalid@.com"))         # False
print(is_valid_email("no-at-sign.com"))       # False
```

### Extraire des URLs

```python
import re

text = """
Visitez https://www.example.com ou http://blog.test.org/page?id=42
pour plus d'informations.
"""

urls = re.findall(r"https?://[^\s]+", text)
print(urls)  # ['https://www.example.com', 'http://blog.test.org/page?id=42']
```

### Nettoyer du texte

```python
import re

text = "  Trop   d'espaces    partout  "

# Remplacer les espaces multiples par un seul espace
clean = re.sub(r"\s+", " ", text).strip()
print(clean)  # "Trop d'espaces partout"
```

### Parser des logs

```python
import re

logs = """
2024-03-15 10:30:45 ERROR [database] Connection timeout after 30s
2024-03-15 10:31:02 INFO [api] Request processed in 150ms
2024-03-15 10:31:15 WARNING [auth] Failed login attempt from 192.168.1.42
"""

pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (\w+) \[(\w+)\] (.+)"

for match in re.finditer(pattern, logs):
    timestamp, level, module, message = match.groups()
    if level in ("ERROR", "WARNING"):
        print(f"⚠️ [{level}] {timestamp} - {module}: {message}")
```

## Comparaison Rapide des Fonctions

| Fonction | Recherche où ? | Retourne quoi ? | Cas d'usage |
|---|---|---|---|
| `match()` | Début de chaîne | 1 Match ou None | Validation de format |
| `search()` | Toute la chaîne | 1 Match ou None | Trouver la première occurrence |
| `findall()` | Toute la chaîne | Liste de strings | Extraire toutes les occurrences |
| `finditer()` | Toute la chaîne | Itérateur de Match | Accès aux positions et groupes |
| `sub()` | Toute la chaîne | String modifiée | Remplacement |
| `split()` | Toute la chaîne | Liste de strings | Découpage |
| `compile()` | — | Objet Pattern | Réutilisation du motif |

## Bonnes Pratiques

1. **Utilisez les raw strings** (`r"..."`) pour éviter les problèmes d'échappement.
2. **Compilez** vos regex si vous les utilisez plusieurs fois dans votre code.
3. **Préférez `re.VERBOSE`** pour les regex complexes — la lisibilité est cruciale.
4. **Testez** vos regex sur [regex101.com](https://regex101.com/) avant de les intégrer dans votre code.
5. **Attention aux quantificateurs gourmands** : utilisez `?` après `*` ou `+` pour les rendre paresseux quand nécessaire.
6. **N'utilisez pas les regex pour parser du HTML/XML** : utilisez plutôt `BeautifulSoup` ou `lxml`.
