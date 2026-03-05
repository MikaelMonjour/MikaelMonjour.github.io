Title: La librairie regex Python : guide complet
Date: 2026-03-05 17:00
Category: tech
Tags: python, regex, tech
Slug: le-module-regex-python-guide-complet
Author: Mikael Monjour
Summary: La librairie regex (pip install regex) est une implémentation avancée et rétrocompatible avec le module standard re de Python. Ce guide couvre toutes ses fonctionnalités : matching flou, patterns récursifs, propriétés Unicode, ensembles imbriqués, lookbehind de longueur variable, et bien plus.

[TOC]

## Introduction

La librairie **`regex`** (disponible via `pip install regex`) est une implémentation avancée des expressions régulières pour Python, **rétrocompatible** avec le module standard `re`, mais offrant de nombreuses fonctionnalités supplémentaires.

Parmi les ajouts majeurs :

- Le **matching flou** (approximatif)
- Les **patterns récursifs**
- Les **propriétés Unicode** étendues (`\p{...}`)
- Les **ensembles imbriqués** et opérations de set
- Le **lookbehind de longueur variable**
- Les **groupes atomiques** et quantificateurs possessifs
- Le matching **POSIX** (le plus long, le plus à gauche)
- Les **listes nommées**
- La **recherche inversée**
- Les **timeouts**
- Et bien d'autres...

```python
# Installation
# pip install regex

import regex

# Utilisation identique à re
m = regex.search(r'\w+', 'Bonjour le monde')
print(m.group())  # 'Bonjour'
```

---

## Ancien et nouveau comportement (version 0 et version 1)

Afin d'être compatible avec le module `re`, le module `regex` possède **deux comportements** :

### Comportement version 0 (ancien, compatible `re`)

Indiqué par le flag `VERSION0` ou `V0`, ou `(?V0)` dans le pattern.

- Les correspondances de largeur zéro ne sont pas gérées correctement (avant Python 3.7).
- `.split` ne divisera pas une chaîne à une largeur égale à zéro.
- `.sub` avancera d'un caractère après une correspondance de largeur zéro.
- Les flags en ligne s'appliquent à l'ensemble du pattern et ne peuvent pas être désactivés.
- Seuls les ensembles simples sont supportés.
- Les correspondances insensibles à la casse en Unicode utilisent une mise en forme simple des majuscules par défaut.

### Comportement version 1 (nouveau, amélioré)

Indiqué par le flag `VERSION1` ou `V1`, ou `(?V1)` dans le pattern.

- Les correspondances de largeur zéro sont **gérées correctement**.
- Les drapeaux en ligne s'appliquent à la fin du groupe ou du motif et **peuvent être désactivés**.
- Les **ensembles imbriqués** et les **opérations de set** sont pris en charge.
- Les correspondances insensibles à la casse en Unicode utilisent le **pliage complet** (full case-folding) par défaut.

Si aucune version n'est spécifiée, le module utilisera `regex.DEFAULT_VERSION`.

```python
import regex

# Forcer la version 1
m = regex.search(r'(?V1)[[a-z]--[aeiou]]', 'b')
print(m.group())  # 'b' (consonnes uniquement)
```

---

## Correspondances insensibles à la casse en Unicode

Le module `regex` prend en charge la conversion **simple** et **complète** (full case-folding) des majuscules et minuscules pour les correspondances insensibles à la casse en Unicode.

L'utilisation complète peut être activée à l'aide du flag `FULLCASE` ou `F`, ou `(?f)` dans le pattern.

> **Note :** Ce flag affecte le fonctionnement du flag `IGNORECASE` ; le flag `FULLCASE` lui-même n'active pas la correspondance insensible à la casse.

- **Version 0 :** le flag `FULLCASE` est **désactivé** par défaut.
- **Version 1 :** le flag `FULLCASE` est **activé** par défaut.

```python
import regex

# Le caractère allemand ß correspond à "SS" en full case-folding
m = regex.search(r'(?fi)strasse', 'die Straße')
print(m.group())  # 'Straße'
```

---

## Ensembles imbriqués et opérations de set

Il n'est pas possible de supporter à la fois des ensembles simples (comme dans `re`) et des ensembles imbriqués en même temps, à cause d'une différence dans la signification d'un `[` non échappé dans un set.

Par exemple, le pattern `[[a-z]--[aeiou]]` est traité :

- En **version 0** comme : un set contenant `[` et les lettres `a-z`, suivi du littéral `--`, etc.
- En **version 1** comme : un set contenant les lettres `a-z` **en excluant** les lettres `a, e, i, o, u` (c'est-à-dire les **consonnes**).

### Opérateurs de set (version 1 uniquement)

Les opérateurs, par ordre de priorité croissant :

| Opérateur | Signification | Exemple |
|-----------|---------------|---------|
| `\|\|` | Union | `x\|\|y` → « x ou y » |
| `~~` | Différence symétrique | `x~~y` → « x ou y, mais pas les deux » |
| `&&` | Intersection | `x&&y` → « x et y » |
| `--` | Différence | `x--y` → « x mais pas y » |

L'union implicite (juxtaposition comme `[ab]`) a la **plus haute priorité**. Ainsi `[ab&&cd]` équivaut à `[[a||b]&&[c||d]]`.

```python
import regex

# Consonnes minuscules : lettres a-z MOINS les voyelles
m = regex.findall(r'(?V1)[[a-z]--[aeiou]]', 'bonjour')
print(m)  # ['b', 'n', 'j', 'r']

# Intersection : caractères qui sont à la fois dans a-m ET dans des voyelles
m = regex.findall(r'(?V1)[[a-m]&&[aeiou]]', 'abcdefghijklm')
print(m)  # ['a', 'e', 'i']
```

---

## Flags (drapeaux)

Il existe deux types de flags : les **scopés** et les **globaux**.

### Flags scopés

Ils ne s'appliquent qu'à **une partie** du pattern et peuvent être **activés ou désactivés** :

`FULLCASE`, `IGNORECASE`, `MULTILINE`, `DOTALL`, `VERBOSE`, `WORD`

### Flags globaux

Ils s'appliquent au **pattern entier** et ne peuvent être **qu'activés** :

`ASCII`, `BESTMATCH`, `ENHANCEMATCH`, `LOCALE`, `POSIX`, `REVERSE`, `UNICODE`, `VERSION0`, `VERSION1`

Si ni `ASCII`, `LOCALE` ni `UNICODE` n'est spécifié, la valeur par défaut sera `UNICODE` pour une chaîne Unicode et `ASCII` pour une chaîne de bytes.

```python
import regex

# Flag scopé : IGNORECASE uniquement sur une partie
m = regex.search(r'(?i:hello) world', 'HELLO world')
print(m.group())  # 'HELLO world'

# Le flag ENHANCEMATCH améliore l'ajustement du matching flou
m = regex.search(r'(?e)(chien){e<=2}', 'le chine est beau')
print(m.group(1))  # 'chine'
```

---

## Drapeaux à portée réduite (scoped flags)

Les drapeaux peuvent être limités à un **sous-motif** uniquement. Ils peuvent être activés ou désactivés au sein du sous-motif, sans affecter le reste du pattern.

```python
import regex

# IGNORECASE uniquement dans le groupe
m = regex.search(r'(?i:abc)def', 'ABCdef')
print(m.group())  # 'ABCdef'

# Désactiver dans un sous-groupe
m = regex.search(r'(?i)abc(?-i:def)', 'ABCdef')
print(m.group())  # 'ABCdef'
```

---

## Groupes de capture nommés

Tous les groupes de capture ont un numéro de groupe, à partir de 1.

### Règles clés

- Les groupes avec le **même nom** auront le **même numéro** de groupe.
- Les groupes avec un **nom différent** auront un **numéro différent**.
- Le même nom peut être utilisé par plus d'un groupe : les captures ultérieures **écrasent** les captures antérieures. Toutes les captures restent disponibles via la méthode `captures()` de l'objet match.

### Syntaxes supportées

Les groupes peuvent être nommés avec `(?<nom>...)` ainsi que la syntaxe classique `(?P<nom>...)`.

Les groupes peuvent être référencés avec `\g<nom>`, ce qui permet d'avoir **plus de 99 groupes**.

```python
import regex

# Noms de groupes dupliqués
m = regex.match(r'(?P<item>\w+) and (?P<item>\w+)', 'chat and chien')
print(m.group('item'))     # 'chien' (dernière capture)
print(m.captures('item'))  # ['chat', 'chien'] (toutes les captures)
```

---

## Réinitialisation de branche (branch reset)

La syntaxe `(?|...|...)` réutilise les numéros de groupe de capture dans toutes les alternatives.

```python
import regex

# Les deux alternatives partagent le groupe 1
m = regex.match(r'(?|(premier)|(second))', 'second')
print(m.group(1))  # 'second'

# Avec noms différents : numéros différents
m = regex.match(r'(?|(?P<a>premier)|(?P<b>second))', 'second')
print(m.group('b'))  # 'second'
```

Dans la regex `(\s+)(?|(?P<foo>[A-Z]+)|(\w+) (?P<foo>[0-9]+))` :

- `(\s+)` → groupe 1
- `(?P<foo>[A-Z]+)` → groupe 2, aussi appelé « foo »
- `(\w+)` → groupe 2 (à cause de la réinitialisation de branche)
- `(?P<foo>[0-9]+)` → groupe 2 (parce qu'il s'appelle « foo »)

---

## Multithreading

Le module `regex` **libère le GIL** lors de la mise en correspondance sur les instances de classes de chaînes intégrées (immuables), ce qui permet à d'autres threads Python de fonctionner simultanément.

Il est aussi possible de **forcer** la libération du GIL en utilisant l'argument `concurrent=True` :

```python
import regex

# Recherche concurrente (libère le GIL)
m = regex.search(r'\w+', texte, concurrent=True)
```

> **Attention :** le comportement n'est pas défini si la chaîne change pendant la recherche. N'utilisez `concurrent=True` que si vous êtes sûr que la chaîne ne sera pas modifiée.

---

## Matching POSIX (le plus long, le plus à gauche)

La norme POSIX pour les regex consiste à retourner le **match le plus long le plus à gauche**. Ceci peut être activé avec le flag `POSIX` ou `(?p)` dans le pattern.

```python
import regex

# Sans POSIX : premier match trouvé
m = regex.search(r'Mr|Mrs', 'Mrs Smith')
print(m.group())  # 'Mr'

# Avec POSIX : match le plus long
m = regex.search(r'(?p)Mr|Mrs', 'Mrs Smith')
print(m.group())  # 'Mrs'

# Autre exemple
m = regex.search(r'(?p)a\w*?b|a\w*?c', 'axxbxxc')
print(m.group())  # 'axxbxxc' (le plus long match possible)
```

> **Note :** le matching POSIX prend plus de temps car, même après avoir trouvé une correspondance, il continue à chercher s'il en existe une plus longue à la même position.

---

## Matching flou (fuzzy matching)

Le `regex` tente généralement d'obtenir une correspondance exacte, mais parfois un résultat **approximatif** (« fuzzy ») est nécessaire, pour les cas où le texte recherché peut contenir des erreurs.

### Les trois types d'erreurs

| Type | Indicateur | Description |
|------|-----------|-------------|
| Insertion | `i` | Un caractère en trop dans le texte |
| Suppression | `d` | Un caractère manquant dans le texte |
| Substitution | `s` | Un caractère remplacé par un autre |
| Toute erreur | `e` | N'importe quel type d'erreur |

Le flou est spécifié entre `{` et `}` après l'élément :

```python
import regex

# Correspondance exacte
regex.search(r'(foo)', 'foo')

# Avec insertions autorisées
regex.search(r'(foo){i}', 'floo')

# Avec suppressions autorisées
regex.search(r'(foo){d}', 'fo')

# Avec substitutions autorisées
regex.search(r'(foo){s}', 'fao')

# Avec tout type d'erreur autorisé
regex.search(r'(foo){e}', 'fax')
```

### Limites d'erreurs

```python
# Au maximum 3 suppressions, aucun autre type
regex.search(r'(mot){d<=3}', texte)

# Au maximum 1 insertion et 2 substitutions, aucune suppression
regex.search(r'(mot){i<=1,s<=2}', texte)

# Au moins 1 et au plus 3 erreurs
regex.search(r'(mot){1<=e<=3}', texte)

# Combinaison avec maximum total
regex.search(r'(mot){i<=2,d<=2,e<=3}', texte)
```

### Coûts d'erreurs

Il est possible d'attribuer un **coût** à chaque type d'erreur et de définir un coût total maximum :

```python
# Chaque insertion coûte 2, chaque suppression coûte 2,
# chaque substitution coûte 1, coût total max 4
regex.search(r'(mot){2i+2d+1s<=4}', texte)

# Combinaison de limites et de coûts
regex.search(r'(mot){i<=1,d<=1,s<=1,2i+2d+1s<=4}', texte)
```

### Flags pour le matching flou

- **`ENHANCEMATCH`** (`(?e)`) : tente d'**améliorer l'ajustement** du match trouvé (réduire le nombre d'erreurs).
- **`BESTMATCH`** (`(?b)`) : recherche le **meilleur match** au lieu du prochain match.

```python
import regex

# Sans amélioration : premier match flou trouvé
m = regex.search(r'(dog){e}', 'cat and dog')
print(m[1])  # 'cat' (3 erreurs, nombre illimité autorisé)

# Avec limite d'erreurs
m = regex.search(r'(dog){e<=1}', 'cat and dog')
print(m[1])  # ' dog' (1 erreur, avec espace en tête)

# Avec ENHANCEMATCH : améliore l'ajustement
m = regex.search(r'(?e)(dog){e<=1}', 'cat and dog')
print(m[1])  # 'dog' (sans espace, meilleur ajustement)
```

### Attributs fuzzy de l'objet match

L'objet match possède deux attributs spéciaux :

- **`fuzzy_counts`** : tuple `(substitutions, insertions, suppressions)` donnant le nombre total de chaque type d'erreur.
- **`fuzzy_changes`** : tuple de tuples donnant les **positions** des substitutions, insertions et suppressions.

```python
import regex

m = regex.search(r'(?:magnifique){e<=3}', 'le manigfique')
print(m.fuzzy_counts)   # (1, 0, 0) par exemple
print(m.fuzzy_changes)  # positions des erreurs
```

---

## `(?(DEFINE)...)` : définir des sous-patterns réutilisables

Si il n'y a pas de groupe appelé `DEFINE`, alors le contenu sera ignoré lors du matching, mais toutes les définitions de groupes qui s'y trouvent seront disponibles pour référence.

C'est très utile pour **factoriser** des sous-motifs complexes utilisés à plusieurs endroits :

```python
import regex

# Définir un sous-pattern pour les montants en dollars
pattern = r'''(?x)
    (?(DEFINE)
        (?P<montant>\$\d+(?:\.\d{2})?)
    )
    Total:\s*(?P>montant)
'''

m = regex.search(pattern, 'Total: $42.50')
print(m.group())  # 'Total: $42.50'
```

---

## `(*PRUNE)`, `(*SKIP)` et `(*FAIL)`

Trois verbes de contrôle du backtracking :

- **`(*PRUNE)`** : supprime les informations de retour en arrière jusqu'à ce point.
- **`(*SKIP)`** : comme `(*PRUNE)`, mais définit aussi **où** dans le texte la prochaine tentative de correspondance commencera.
- **`(*FAIL)`** (ou `(*F)`) : provoque un retour en arrière **immédiat**.

> Lorsqu'ils sont utilisés dans un groupe atomique ou dans un lookaround, ces verbes n'affectent pas le pattern environnant.

---

## `\K` : garder une partie du match

`\K` garde la partie du match entier **après** la position où `\K` s'est produit ; la partie avant est défaussée. Cela n'affecte **pas** le retour des groupes de capture.

```python
import regex

# Trouver le mot après "foo " sans l'inclure dans le match
m = regex.search(r'foo \K\w+', 'foo bar')
print(m.group())  # 'bar'

# Remplacer uniquement ce qui suit \K
result = regex.sub(r'foo \K\w+', 'baz', 'foo bar')
print(result)  # 'foo baz'
```

---

## `captures()`, `capturesdict()` et `groupdict()`

L'objet match dispose de méthodes supplémentaires pour accéder à **toutes les captures** d'un groupe répété :

- **`groupdict()`** : retourne un dictionnaire des groupes nommés avec la **dernière** capture.
- **`captures(group)`** : retourne une **liste** de toutes les captures d'un groupe.
- **`capturesdict()`** : retourne un dictionnaire des groupes nommés avec la **liste complète** de toutes les captures.

```python
import regex

m = regex.match(r'(?P<mot>\w+) (?P<mot>\w+) (?P<mot>\w+)', 'un deux trois')

print(m.group('mot'))        # 'trois' (dernière capture)
print(m.captures('mot'))     # ['un', 'deux', 'trois']
print(m.capturesdict())      # {'mot': ['un', 'deux', 'trois']}
print(m.groupdict())         # {'mot': 'trois'}
```

---

## Noms de groupes dupliqués

Les noms de groupes peuvent être **dupliqués** dans le pattern. Les captures ultérieures écrasent les précédentes, mais toutes restent accessibles via `captures()`.

```python
import regex

m = regex.match(r'(?P<item>\w+) et (?P<item>\w+)', 'pain et beurre')
print(m.group('item'))      # 'beurre'
print(m.captures('item'))   # ['pain', 'beurre']
```

---

## `fullmatch()`

`fullmatch` se comporte comme `match`, sauf qu'il doit correspondre à **toute la chaîne**.

```python
import regex

print(regex.fullmatch(r'\d{4}', '1234'))    # Match
print(regex.fullmatch(r'\d{4}', '12345'))   # None
print(regex.fullmatch(r'\d{4}', '123'))     # None
```

---

## `subf()`, `subfn()` et `expandf()`

`subf` et `subfn` sont des alternatives à `sub` et `subn`. Lorsqu'une chaîne de remplacement est passée, ils la traitent comme une **chaîne de format** (f-string style).

`expandf` est l'équivalent pour l'objet match.

```python
import regex

# subf : remplacement avec chaîne de format
result = regex.subf(r'(?P<mot>\w+)', '{0} ({mot})', 'bonjour monde', count=1)
print(result)  # 'bonjour (bonjour) monde'

# expandf sur un objet match
m = regex.search(r'(?P<prenom>\w+) (?P<nom>\w+)', 'Jean Dupont')
print(m.expandf('{prenom} - {nom}'))  # 'Jean - Dupont'
```

### Indice de capture dans `expandf` et `subf`/`subfn`

Vous pouvez utiliser l'écriture en **indice** pour obtenir les captures d'un groupe de capture répété :

```python
import regex

m = regex.match(r'(?P<x>\w+) (?P<x>\w+)', 'abc def')
print(m.expandf('{x[0]} {x[1]}'))  # 'abc def'
```

---

## Détacher la chaîne recherchée (`detach_string`)

Un objet match contient une **référence** à la chaîne recherchée via son attribut `string`. La méthode `detach_string()` « détache » cette chaîne, la rendant disponible pour le garbage collector — utile pour **économiser la mémoire** si la chaîne est très grande.

```python
import regex

texte = 'un très long texte...' * 10000
m = regex.search(r'\w+', texte)
print(m.group())  # 'un'
m.detach_string()
print(m.group())  # 'un' (toujours accessible)
# Mais m.string est maintenant None
```

---

## Patterns récursifs

Les motifs récursifs et répétés sont pris en charge :

- **`(?R)`** ou **`(?0)`** : essaie de faire correspondre l'**ensemble** du regex de façon récursive.
- **`(?1)`**, **`(?2)`**, etc. : essaie de faire correspondre le **groupe de capture** correspondant.
- **`(?&nom)`** : essaie de faire correspondre le **groupe de capture nommé**.

Les formes alternatives `(?P>nom)` et `(?P&nom)` sont aussi supportées.

```python
import regex

# Correspondance de parenthèses imbriquées
m = regex.search(r'\((?:[^()]*|(?R))*\)', '(a(b)c)')
print(m.group())  # '(a(b)c)'

# Réutilisation d'un sous-pattern
m = regex.match(r'(Tarzan|Jane) aime (?1)', 'Tarzan aime Jane')
print(m.group())  # 'Tarzan aime Jane'

# (?1) est équivalent à (?:Tarzan|Jane) — réutilise le motif, pas le groupe
```

> **Note :** Il est possible de revenir en arrière (backtracker) dans un groupe récursif. Vous ne pouvez pas appeler un groupe s'il y a plus d'un groupe avec ce nom ou numéro (« référence ambiguë »).

---

## Correspondances partielles (partial matches)

Une correspondance partielle est une correspondance qui atteint la **fin de la chaîne** — si la chaîne avait été plus longue, un match complet aurait été possible.

Les correspondances partielles sont acceptées avec `match`, `search`, `fullmatch` et `finditer` via l'argument `partial=True`.

L'objet match possède un attribut `partial` qui vaut `True` s'il s'agit d'un match partiel.

```python
import regex

# Vérification caractère par caractère (ex: saisie utilisateur)
pattern = regex.compile(r'\d{4}')

for saisie in ['1', '12', '123', '1234', '12345']:
    m = pattern.fullmatch(saisie, partial=True)
    if m is None:
        print(f'{saisie} → rejeté')
    elif m.partial:
        print(f'{saisie} → partiel (continuer)')
    else:
        print(f'{saisie} → complet !')

# Sortie :
# 1 → partiel (continuer)
# 12 → partiel (continuer)
# 123 → partiel (continuer)
# 1234 → complet !
# 12345 → rejeté
```

---

## Lookaround dans les motifs conditionnels

Le test d'un motif conditionnel peut maintenant être un **lookaround** (lookahead ou lookbehind).

```python
import regex

# Conditionnel avec lookahead
m = regex.search(r'(?(?=\d)\d{3}|\w{3})', '123abc')
print(m.group())  # '123'

m = regex.search(r'(?(?=\d)\d{3}|\w{3})', 'abc123')
print(m.group())  # 'abc'
```

> **Attention :** ce n'est pas la même chose qu'un lookaround dans la première branche d'une paire d'alternatives. Avec le conditionnel, si la condition échoue, la seconde branche est tentée. Avec les alternatives, si le lookaround réussit mais que la première branche échoue, la seconde branche est tout de même essayée.

---

## Lookbehind de longueur variable

Contrairement au module `re` standard, la librairie `regex` supporte les **lookbehind de longueur variable** :

```python
import regex

# Lookbehind avec longueur variable — impossible avec re !
m = regex.search(r'(?<=\d+)\w+', '123abc')
print(m.group())  # 'abc'

# Lookbehind négatif de longueur variable
m = regex.search(r'(?<!\d{2,4})\b\w+', 'abc 123def')
print(m.group())  # 'abc'
```

---

## Groupes atomiques

Si le motif suivant échoue, le sous-motif dans un groupe atomique **échoue dans son ensemble**, sans backtracking.

```python
import regex

# Groupe atomique : pas de backtracking
m = regex.search(r'(?>abc|ab)c', 'abc')
print(m)  # None — 'abc' est consommé par le groupe atomique, il ne reste rien pour 'c'

m = regex.search(r'(?>abc|ab)c', 'abcc')
print(m.group())  # 'abcc'
```

---

## Quantificateurs possessifs

Les quantificateurs possessifs fonctionnent comme les groupes atomiques appliqués aux quantificateurs :

- `(?:...)?+`
- `(?:...)*+`
- `(?:...)++`
- `(?:...){min,max}+`

Le sous-motif est adapté au maximum. Si le motif suivant échoue, tous les sous-motifs répétés échouent **dans leur ensemble**.

```python
import regex

# Sans possessif : backtracking possible
m = regex.search(r'".+"', '"abc"def"')
print(m.group())  # '"abc"def"'

# Avec quantificateur possessif : pas de backtracking sur le +
m = regex.search(r'".++"', '"abc"')
print(m)  # None — le ++ consomme tout y compris le dernier ", pas de backtracking
```

---

## Listes nommées

Il est parfois nécessaire d'inclure une liste d'options dans un regex. Plutôt que de construire un pattern d'alternation (qui peut être lent à parser pour de longues listes), utilisez les **listes nommées** :

```python
import regex

# Méthode classique (alternation)
p = regex.compile(r'chat|chien|oiseau|poisson')

# Méthode avec listes nommées
animaux = ['chat', 'chien', 'oiseau', 'poisson']
p = regex.compile(r'\L<animaux>', animaux=animaux)

m = p.search('Mon chien est mignon')
print(m.group())  # 'chien'

# L'ordre des items n'est pas pertinent (traités comme un ensemble)
# Disponibles via l'attribut .named_lists du pattern compilé
print(p.named_lists)  # {'animaux': frozenset({...})}
```

---

## Début et fin de mot

Deux ancres supplémentaires pour les limites de mots :

- **`\m`** : correspond au **début** d'un mot.
- **`\M`** : correspond à la **fin** d'un mot.

Comparez avec `\b`, qui correspond au début **ou** à la fin d'un mot.

```python
import regex

# \m : début de mot uniquement
m = regex.findall(r'\m\w', 'un deux trois')
print(m)  # ['u', 'd', 't']

# \M : fin de mot uniquement
m = regex.findall(r'\w\M', 'un deux trois')
print(m)  # ['n', 'x', 's']
```

---

## Séparateurs de ligne Unicode

Normalement, le seul séparateur de ligne est `\n` (`\x0A`). Mais si le drapeau **`WORD`** est activé, les séparateurs de ligne deviennent : `\x0D\x0A`, `\x0A`, `\x0B`, `\x0C`, `\x0D`, plus `\x85`, `\u2028` et `\u2029` en Unicode.

Ceci affecte :

- Le point `.` (quand `DOTALL` est désactivé) : correspond à tout sauf un séparateur de ligne.
- Les ancres `^` et `$` en mode multiligne.

---

## Propriétés Unicode, scripts et blocs

De nombreuses propriétés Unicode sont supportées, y compris les **blocs** et les **scripts**.

```python
import regex

# Propriété générale
m = regex.findall(r'\p{L}', 'abc 123 àéî')  # Lettres Unicode
print(m)  # ['a', 'b', 'c', 'à', 'é', 'î']

# Script
m = regex.findall(r'\p{Script=Greek}', 'αβγ abc')
print(m)  # ['α', 'β', 'γ']

# Bloc
m = regex.findall(r'\p{Block=BasicLatin}', 'abc αβγ')
print(m)  # ['a', 'b', 'c']

# Inverse
m = regex.findall(r'\P{L}', 'abc 123')  # Non-lettres
print(m)  # [' ', '1', '2', '3']

# Forme courte : \p{value} cherche dans General_Category, puis Script, puis Block
m = regex.findall(r'\p{Lu}', 'Bonjour MONDE')  # Uppercase letters
print(m)  # ['B', 'M', 'O', 'N', 'D', 'E']
```

---

## Caractères nommés Unicode

Les caractères nommés Unicode sont pris en charge :

```python
import regex

m = regex.search(r'\N{SNOWMAN}', '☃ bonhomme de neige')
print(m.group())  # '☃'

m = regex.search(r'\N{HEAVY BLACK HEART}', 'Je t❤aime')
print(m.group())  # '❤'
```

> **Note :** seuls les noms connus par la base de données Unicode de Python sont supportés.

---

## Classes de caractères POSIX

Les classes de caractères POSIX sont supportées et traitées comme une forme alternative de `\p{...}` :

```python
import regex

# [:alpha:] — lettres
m = regex.findall(r'[[:alpha:]]', 'abc 123')
print(m)  # ['a', 'b', 'c']

# [:digit:] — chiffres
m = regex.findall(r'[[:digit:]]', 'abc 123')
print(m)  # ['1', '2', '3']

# [:alnum:] — alphanumériques
m = regex.findall(r'[[:alnum:]]', 'a1 b2!')
print(m)  # ['a', '1', 'b', '2']
```

> **Note :** les définitions de `alnum`, `digit`, `punct` et `xdigit` sont différentes de celles d'Unicode.

---

## Ancre de recherche (`\G`)

L'ancre `\G` correspond à l'endroit où chaque recherche a **commencé ou s'est poursuivie**. Elle est utile pour des **correspondances contiguës** :

```python
import regex

# Correspondances contiguës de 2 lettres
m = regex.findall(r'\G[a-z]{2}', 'abcdef123')
print(m)  # ['ab', 'cd', 'ef']
# S'arrête à '123' car la correspondance n'est plus contiguë
```

La recherche commence à la position 0 pour correspondre à `ab`. La recherche se poursuit à la position 2 et correspond à `cd`. Elle se poursuit à la position 4 et correspond à `ef`. À la position 6, pas de correspondance de 2 lettres → l'ancre empêche de continuer.

---

## Recherche inversée

Les recherches peuvent se faire **à l'envers** avec le flag `REVERSE` ou `(?r)` :

```python
import regex

# Recherche inversée : du dernier au premier
m = regex.search(r'(?r)chat', 'le chat du chat noir')
print(m.group())  # 'chat'
print(m.start())  # 13 (le dernier 'chat')

# Avec findall en mode inversé
m = regex.findall(r'(?r)\w+', 'un deux trois')
print(m)  # ['trois', 'deux', 'un']
```

> **Note :** le résultat d'une recherche inversée n'est pas nécessairement l'inverse d'une recherche directe.

---

## Correspondance de graphèmes Unicode

L'appariement des **graphèmes** est pris en charge avec `\X`, conforme à la spécification Unicode :

```python
import regex

# Un graphème peut être composé de plusieurs points de code
texte = 'e\u0301'  # é (e + accent aigu combinant)
m = regex.findall(r'\X', texte)
print(m)    # ['é'] — un seul graphème
print(len(texte))  # 2 points de code
```

---

## Limite de mot Unicode par défaut

Le flag **`WORD`** change la définition d'une « limite de mot » en celle d'une **limite de mot Unicode par défaut** (conforme à la spécification Unicode). Ceci s'applique à `\b` et `\B`.

---

## `regex.escape()` amélioré

La fonction `regex.escape` possède deux paramètres supplémentaires :

- **`special_only=True`** : n'échappe que les caractères « spéciaux » regex (comme `?`, `*`, etc.).
- **`literal_spaces=True`** : les espaces ne sont **pas** échappés.

```python
import regex

print(regex.escape('hello world?', special_only=True))
# 'hello world\?'

print(regex.escape('hello world', literal_spaces=True))
# 'hello world'  (les espaces ne sont pas échappés)
```

---

## Captures répétées (repeated captures)

Un objet match possède des méthodes supplémentaires qui renvoient des informations sur **toutes les correspondances réussies** d'un groupe de capture répété :

```python
import regex

m = regex.match(r'(\w)+', 'abcdef')

# group() retourne la dernière capture
print(m.group(1))      # 'f'

# captures() retourne TOUTES les captures
print(m.captures(1))   # ['a', 'b', 'c', 'd', 'e', 'f']

# spans() retourne les positions de toutes les captures
print(m.spans(1))      # [(0,1), (1,2), (2,3), (3,4), (4,5), (5,6)]
```

---

## `splititer()`

`regex.splititer` est un **générateur** équivalent de `regex.split` :

```python
import regex

# split retourne une liste
print(regex.split(r'\s+', 'un deux trois'))
# ['un', 'deux', 'trois']

# splititer retourne un générateur (plus économe en mémoire)
for mot in regex.splititer(r'\s+', 'un deux trois'):
    print(mot)
```

---

## Indexation d'un objet match (subscripting)

Un objet match accepte l'accès aux groupes via l'**indexation** et les **slices** :

```python
import regex

m = regex.search(r'(\w+) (\w+) (\w+)', 'un deux trois')

# Accès par index
print(m[0])    # 'un deux trois'
print(m[1])    # 'un'
print(m[2])    # 'deux'

# Slice
print(m[1:3])  # ('un', 'deux')
```

---

## Arguments supplémentaires

### Flag `flags` pour `split`, `sub` et `subn`

```python
import regex

# Passer des flags directement
result = regex.split(r'[aeiou]', 'Bonjour', flags=regex.IGNORECASE)
print(result)  # ['', 'nj', '', 'r']
```

### Arguments `pos` et `endpos` pour `sub` et `subn`

```python
import regex

# Remplacer uniquement dans une sous-partie
result = regex.sub(r'\w', '*', 'abcdef', pos=2, endpos=4)
print(result)  # 'ab**ef'
```

### Argument `overlapped` pour `findall` et `finditer`

```python
import regex

# Sans overlapped
print(regex.findall(r'\w{3}', 'abcdef'))
# ['abc', 'def']

# Avec overlapped : correspondances chevauchantes
print(regex.findall(r'\w{3}', 'abcdef', overlapped=True))
# ['abc', 'bcd', 'cde', 'def']
```

---

## Timeout (Python 3)

Les méthodes et fonctions de correspondance prennent en charge les **délais d'attente**. Le timeout (en secondes) s'applique à l'ensemble de l'opération :

```python
import regex

try:
    # Timeout de 1 seconde
    m = regex.search(r'(a+)+b', 'a' * 30, timeout=1)
except TimeoutError:
    print("Le matching a pris trop de temps !")
```

> **Note :** le timeout est particulièrement utile pour se protéger contre les expressions régulières malveillantes ou les cas de backtracking exponentiel (ReDoS).

---

## Résumé des fonctionnalités exclusives à `regex`

| Fonctionnalité | Syntaxe | Description |
|----------------|---------|-------------|
| Matching flou | `{e<=n}` | Correspondance approximative |
| Patterns récursifs | `(?R)`, `(?1)`, `(?&nom)` | Réutilisation de motifs |
| Propriétés Unicode | `\p{Script=Latin}` | Filtrage par propriété |
| Ensembles imbriqués | `[[a-z]--[aeiou]]` | Opérations sur les sets |
| Lookbehind variable | `(?<=\d+)` | Lookbehind de longueur variable |
| Groupes atomiques | `(?>...)` | Pas de backtracking |
| Quantificateurs possessifs | `a++`, `a*+` | Quantificateurs sans backtracking |
| Matching POSIX | `(?p)` | Match le plus long |
| Listes nommées | `\L<nom>` | Ensembles dynamiques |
| Branch reset | `(?|...\|...)` | Numéros de groupe partagés |
| `\K` | `\K` | Garder une partie du match |
| `captures()` | `m.captures(1)` | Toutes les captures d'un groupe |
| Recherche inversée | `(?r)` | Recherche de droite à gauche |
| Correspondances partielles | `partial=True` | Match partiel |
| Timeout | `timeout=1` | Protection contre le ReDoS |
| `subf()`/`expandf()` | `{nom}` dans le remplacement | Remplacement avec format |
| `detach_string()` | `m.detach_string()` | Libération mémoire |
| Multithreading | `concurrent=True` | Libération du GIL |
| `\m`, `\M` | `\m`, `\M` | Début/fin de mot |
| `\G` | `\G` | Ancre de recherche |
| `(*PRUNE)`, `(*SKIP)`, `(*FAIL)` | Verbes de contrôle | Contrôle du backtracking |
| `(?(DEFINE)...)` | Définitions | Sous-patterns réutilisables |

---

## Conclusion

La librairie `regex` est un **remplacement direct** du module `re` avec des fonctionnalités considérablement étendues. Elle est particulièrement utile pour :

- Le **traitement de texte avancé** (matching flou, patterns récursifs)
- Le travail avec **Unicode** (propriétés, scripts, blocs, full case-folding)
- Les **performances** (listes nommées, groupes atomiques, libération du GIL)
- La **sécurité** (timeout contre le ReDoS)
- L'**analyse syntaxique** complexe (patterns récursifs, branch reset, `(?(DEFINE)...)`)

Pour l'installer :

```bash
pip install regex
```

Et pour l'utiliser en remplacement de `re` :

```python
import regex
# Toutes les fonctions de re sont disponibles :
# regex.search(), regex.match(), regex.findall(), regex.sub(), etc.
# Plus toutes les fonctionnalités avancées décrites dans ce guide !
```
