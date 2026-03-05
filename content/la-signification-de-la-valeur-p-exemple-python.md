Title: La signification de la valeur p (p-value) — Exemple avec Python
Date: 2026-03-05 16:00
Category: tech
Tags: python, data, statistiques, tech
Slug: la-signification-de-la-valeur-p-exemple-python
Author: Mikael Monjour
Summary: Lundi matin, réunion d'équipe. Le product manager annonce : "p-value de 0.03, on déploie en prod." Tout le monde applaudit. Sauf vous. Car cette p-value ne prouve probablement pas ce que tout le monde croit.

Imaginez la scène. Lundi matin, 9 h 30, réunion d'équipe. Le product manager (la personne responsable du produit) affiche un graphique et annonce fièrement :

*"Notre nouveau bouton vert a augmenté le taux de conversion de 12 %. La p-value est de 0.03. C'est statistiquement significatif. On déploie en production."*

Traduction : il pense avoir prouvé que le bouton vert fait acheter plus de clients. Tout le monde applaudit.

Sauf vous. Parce que vous savez que ce test a été lancé un vendredi soir, sur seulement 200 visiteurs. Et qu'une p-value de 0.03 dans ces conditions ne prouve pas grand-chose.

Pourtant, des décisions à plusieurs millions d'euros sont prises chaque jour sur la base de ce petit nombre mal compris. **La p-value est le concept statistique le plus utilisé — et le plus mal interprété — dans le monde de la tech.**

## Qu'est-ce que la valeur p, en termes simples ?

Avant d'aller plus loin, posons quelques définitions :

- **Test A/B :** on montre deux versions d'une page (A et B) à des groupes différents de visiteurs pour voir laquelle fonctionne le mieux.
- **Taux de conversion :** le pourcentage de visiteurs qui font l'action souhaitée (acheter, s'inscrire, cliquer).
- **Hypothèse nulle :** l'idée de départ qu'on cherche à tester. Par exemple : "le bouton vert ne change rien au comportement des visiteurs".

La p-value, c'est un chiffre entre 0 et 1 qui répond à une question simple :

**Si rien n'a changé (si l'hypothèse nulle est vraie), quelle est la probabilité d'observer un résultat aussi extrême que celui qu'on a mesuré ?**

Plus la p-value est petite, plus le résultat observé serait surprenant si rien n'avait changé. Mais attention : "surprenant" ne veut pas dire "impossible". C'est toute la subtilité.

## Un exemple concret : le panier moyen

Prenons un cas que tout growth engineer connaît bien.

Vous travaillez sur une plateforme e-commerce. Après des mois d'observation, vous savez que vos clients dépensent en moyenne **170 €** par commande. C'est votre référence — votre hypothèse nulle.

Deux notions importantes ici :

- **La moyenne :** la somme de toutes les valeurs divisée par le nombre de valeurs. Si 3 clients dépensent 150 €, 170 € et 190 €, la moyenne est (150 + 170 + 190) / 3 = 170 €.
- **L'écart type :** il mesure à quel point les valeurs sont dispersées autour de la moyenne. Un écart type faible (par exemple 5 €) signifie que la plupart des clients dépensent entre 165 € et 175 €. Un écart type élevé signifierait des montants très variés. Ici, notre écart type est de **5 €**.

Vous lancez un test. Vous prenez un groupe de clients au hasard. Et vous observez que leur panier moyen est de **183 €**.

La question : *est-ce que ce groupe dépense vraiment plus, ou est-ce juste le hasard qui a sélectionné des clients plus dépensiers ?*

C'est exactement la question à laquelle la p-value va répondre.

## Pourquoi un seul échantillon ne suffit pas

Un **échantillon**, c'est un sous-groupe tiré au hasard dans une population plus large. Si votre site a 500 000 clients, un échantillon pourrait être un groupe de 1 000 clients pris au hasard.

Le problème : chaque fois que vous tirez un échantillon différent, vous obtenez une moyenne légèrement différente. Un groupe tombera sur 168 €, un autre sur 172 €, un autre sur 175 €. C'est normal — c'est la **variabilité d'échantillonnage**.

Il existe un théorème fondamental en statistiques — le **théorème de la limite centrale** — qui dit ceci : si vous tirez suffisamment d'échantillons et que vous tracez toutes leurs moyennes sur un graphique, vous obtenez une courbe en forme de cloche (une **distribution normale**). Le sommet de cette cloche se situe à la vraie moyenne de la population.

Concrètement, si on tire **10 000 échantillons** de notre base clients :

- La plupart des moyennes d'échantillon seront proches de 170 €.
- Quelques-unes seront à 160 € ou 180 €.
- Très peu seront à 150 € ou 190 €.

La question devient alors : **quelle est la probabilité de tomber sur une moyenne de 183 € ou plus, si la vraie moyenne est bien de 170 € ?** C'est la p-value.

## Calculons-le avec Python

Le code ci-dessous simule exactement ce scénario. Il tire 10 000 échantillons d'une population dont la moyenne est 170 € (paramètre `mu`) et l'écart type est 5 € (paramètre `sigma`), puis il compte combien de ces échantillons ont une moyenne supérieure à 183 € :

```python
import numpy as np
import matplotlib.pyplot as plt

def pvalue_101(mu, sigma, samp_size, samp_mean=0, deltam=0):
    np.random.seed(1234)
    s1 = np.random.normal(mu, sigma, samp_size)

    if samp_mean > 0:
        print(len(s1[s1>samp_mean]))
        outliers = float(len(s1[s1>samp_mean])*100) / float(len(s1))
        print('Percentage of numbers larger than {} is {}%'
              .format(samp_mean, outliers))

    if deltam == 0:
        deltam = abs(mu - samp_mean)

    if deltam > 0:
        outliers = (float(len(s1[s1>(mu+deltam)]))
                    + float(len(s1[s1<(mu-deltam)]))) * 100.0 / float(len(s1))
        print("""Percentage of numbers further than the population mean
              of {} by +/-{} is {}%""".format(mu, deltam, outliers))

    fig, ax = plt.subplots(figsize=(8, 8))
    fig.suptitle('Normal Distribution: population_mean={}'.format(mu))
    plt.hist(s1)
    plt.axvline(x=mu+deltam, color='red')
    plt.axvline(x=mu-deltam, color='green')
    plt.show()
```

On lance le test :

```python
pvalue_101(170.0, 5.0, 10000, 183.0)
```

Résultat : **seulement 0,35 % des échantillons ont une moyenne supérieure à 183 €**.

C'est très peu. Mais ce n'est pas zéro. Sur 10 000 tirages, environ 35 tombent au-dessus de 183 €. Le hasard peut produire ce résultat — rarement, mais il le peut.

## Test unilatéral ou bilatéral : pourquoi c'est important

Deux termes à comprendre :

- **Test unilatéral :** on cherche un écart dans une seule direction. "Est-ce que la moyenne est *supérieure* à 170 € ?" On ne regarde que le côté droit de la courbe.
- **Test bilatéral :** on cherche un écart dans les deux directions. "Est-ce que la moyenne est *différente* de 170 €, que ce soit en plus ou en moins ?" On regarde les deux côtés.

Si on pose la question en bilatéral — quelle est la probabilité d'obtenir une moyenne éloignée de plus de 13 € de 170 €, soit inférieure à 157 € **ou** supérieure à 183 € — la réponse est **0,77 %**. Environ le double, car la courbe en cloche est symétrique.

En pratique, on utilise presque toujours un test bilatéral. Pourquoi ? Parce qu'un changement peut être positif *ou* négatif, et il faut mesurer les deux possibilités.

## La règle 68-95-99,7 : où tombent la plupart des résultats

Cette règle permet de visualiser rapidement la répartition des moyennes d'échantillon autour de la vraie moyenne. Le symbole **σ** (sigma) représente l'écart type :

- **68,2 %** des moyennes tombent à moins de 1 écart type de la moyenne (entre 165 € et 175 €). C'est la zone "normale".
- **95,4 %** tombent à moins de 2 écarts types (entre 160 € et 180 €). Presque tout est là.
- **99,7 %** tombent à moins de 3 écarts types (entre 155 € et 185 €). Au-delà, c'est exceptionnel.

Notre échantillon à 183 € se situe au-delà de 2 écarts types. C'est rare — mais le hasard le permet.

## L'erreur que 90 % des équipes commettent

Voici le raisonnement que l'on entend dans presque toutes les équipes produit et marketing :

*"On veut un niveau de confiance de 95 %. Notre seuil est donc une p-value de 5 %. La moyenne d'échantillon est de 183 € et sa p-value est de 0,35 %. Comme 0,35 % est inférieur à 5 %, on rejette l'hypothèse que la moyenne de la population est de 170 €."*

**Cette conclusion est fausse.**

Pourquoi ? Parce que dans notre simulation, nous avons *nous-mêmes* tiré cet échantillon d'une population dont la moyenne EST 170 €. L'échantillon à 183 € est rare, mais il existe bel et bien dans cette population.

Rejeter l'hypothèse sur la base d'un seul échantillon, c'est comme retourner une seule carte au poker et décider que vous avez gagné la partie.

La p-value nous dit : **"Si l'hypothèse de départ est vraie, voici la probabilité d'observer ce résultat."** Elle ne nous dit **pas** : "Voici la probabilité que l'hypothèse soit vraie." C'est la nuance la plus importante de cet article.

## Exemple concret : l'ingestion de leads dans un CRM

Un **lead**, c'est un contact commercial potentiel — quelqu'un qui a rempli un formulaire, téléchargé un livre blanc, ou laissé ses coordonnées. Un **CRM** (Customer Relationship Management) est le logiciel qui centralise et suit tous ces contacts (HubSpot, Salesforce, Pipedrive, etc.).

Imaginons une équipe growth qui travaille sur l'ingestion de leads. Le pipeline actuel fonctionne comme ceci : un visiteur remplit un formulaire sur le site, ses données sont envoyées au CRM via une API, et un commercial le recontacte sous 24 h.

L'équipe observe que le **taux de qualification** des leads (le pourcentage de leads qui deviennent de vrais prospects qualifiés) est de **18 %** en moyenne. L'écart type, calculé sur 6 mois de données, est de **3 %**.

Un développeur propose un changement : enrichir automatiquement chaque lead avec des données publiques (taille d'entreprise, secteur, poste) *avant* qu'il arrive dans le CRM. L'idée est que les commerciaux, mieux informés, qualifient mieux les leads.

Après 2 semaines de test sur un échantillon de leads, le taux de qualification grimpe à **26 %**.

L'équipe est enthousiaste. Le Head of Sales veut généraliser immédiatement. Mais posons-nous la question :

**Quelle est la probabilité d'observer un taux de 26 % ou plus, si en réalité l'enrichissement n'a rien changé et que la vraie moyenne est toujours de 18 % ?**

```python
pvalue_101(18.0, 3.0, 10000, 26.0)
```

Résultat : **pratiquement 0 %**. La différence est de plus de 2,5 écarts types. Il est extrêmement improbable d'observer un tel écart par le seul hasard.

Mais avant de célébrer, il faut vérifier plusieurs choses :

- **La durée du test :** 2 semaines, est-ce suffisant ? Si le cycle de vente est de 30 jours, on n'a vu qu'une partie du tableau.
- **La taille de l'échantillon :** combien de leads ont été testés ? 50 leads enrichis contre 50 non enrichis, c'est trop peu. 500 contre 500, c'est plus solide.
- **Le biais de sélection :** les leads enrichis venaient-ils de la même source que les autres ? Si l'enrichissement a été testé uniquement sur les leads entrants de Google Ads (souvent plus qualifiés que ceux venant des réseaux sociaux), la comparaison est faussée.
- **La saisonnalité :** la période de test correspond-elle à un pic naturel d'activité (rentrée, Black Friday, fin de trimestre) qui gonfle artificiellement les résultats ?

Ici, la p-value est rassurante — le signal est fort. Mais elle ne remplace pas un design expérimental rigoureux. Si le test avait été lancé uniquement pendant la dernière semaine du trimestre (quand les commerciaux poussent pour atteindre leurs objectifs), le taux de qualification serait naturellement plus élevé, enrichissement ou pas.

## Le test A/B qui a presque tout cassé

Autre situation classique. Une équipe growth lance un test A/B sur la page de tarification de leur SaaS. La version B affiche le prix barré avec une réduction de 20 %. Après seulement 3 jours, la p-value tombe sous 0,05. Le product manager veut déployer immédiatement.

Mais en analysant les données de plus près, on découvre que le test a été lancé un vendredi soir. Le trafic du week-end est dominé par un profil de visiteurs différent : des particuliers qui achètent plus facilement que les professionnels en semaine. La "significativité statistique" n'était que du bruit lié à la composition du trafic.

Si l'équipe avait attendu un cycle complet — au moins 7 jours, pour couvrir tous les profils de visiteurs — elle aurait vu que l'effet disparaissait complètement.

**Leçon :** une p-value basse ne signifie rien si la conception du test est bancale.

## Ce que la p-value nous dit — et ce qu'elle ne dit pas

Résumons en termes simples :

- Une p-value de **0,35 %** signifie : "Si la vraie moyenne est de 170 €, il n'y a que 0,35 % de chance d'observer une moyenne d'échantillon supérieure à 183 €."
- Une p-value de **0,77 %** signifie : "Si la vraie moyenne est de 170 €, il n'y a que 0,77 % de chance d'observer une moyenne qui s'en éloigne de plus de 13 €, dans un sens ou dans l'autre."
- La p-value **ne nous dit pas** si l'hypothèse de départ est vraie ou fausse.
- On **ne peut pas** rejeter une hypothèse de manière fiable sur la base d'un seul échantillon.

## Les 5 questions à poser avant de conclure

La prochaine fois que quelqu'un brandit une p-value en réunion, posez ces questions :

1. **Combien de personnes ont été testées ?** — Un test sur 200 visiteurs ou 50 leads ne prouve rien. Il faut un volume suffisant pour que les résultats soient fiables.
2. **Pendant combien de temps le test a-t-il tourné ?** — Il faut couvrir au moins un cycle business complet : 7 jours minimum pour du B2C (vente aux particuliers), souvent 14 jours ou plus pour du B2B (vente aux entreprises).
3. **Le test est-il bilatéral ?** — On doit mesurer si le changement est meilleur *ou* pire, pas seulement meilleur. Un test unilatéral surestime la significativité.
4. **Les groupes sont-ils comparables ?** — Si le groupe A vient de Google Ads et le groupe B vient des réseaux sociaux, la comparaison n'a aucun sens. C'est un **biais de segmentation**.
5. **A-t-on regardé les résultats une seule fois ou plusieurs ?** — Vérifier la p-value tous les jours (le **"peeking"**) gonfle artificiellement les chances de trouver un résultat significatif. Il faut définir la durée du test à l'avance et ne regarder qu'à la fin.

## Le code complet pour reproduire les calculs

Ce code Python génère les graphiques et calcule les p-values présentées dans cet article. Vous pouvez le copier-coller dans un notebook Jupyter ou un script Python :

```python
import numpy as np
import matplotlib.pyplot as plt

def pvalue_101(mu, sigma, samp_size, samp_mean=0, deltam=0):
    np.random.seed(1234)
    s1 = np.random.normal(mu, sigma, samp_size)

    if samp_mean > 0:
        print(len(s1[s1>samp_mean]))
        outliers = float(len(s1[s1>samp_mean])*100) / float(len(s1))
        print('Percentage of numbers larger than {} is {}%'
              .format(samp_mean, outliers))

    if deltam == 0:
        deltam = abs(mu - samp_mean)

    if deltam > 0:
        outliers = (float(len(s1[s1>(mu+deltam)]))
                    + float(len(s1[s1<(mu-deltam)]))) * 100.0 / float(len(s1))
        print("""Percentage of numbers further than the population mean
              of {} by +/-{} is {}%""".format(mu, deltam, outliers))

    fig, ax = plt.subplots(figsize=(8, 8))
    fig.suptitle('Normal Distribution: population_mean={}'.format(mu))
    plt.hist(s1)
    plt.axvline(x=mu+deltam, color='red')
    plt.axvline(x=mu-deltam, color='green')
    plt.show()

# Exemple e-commerce : probabilité d'un panier moyen > 183 €
pvalue_101(170.0, 5.0, 10000, 183.0)

# Exemple e-commerce : probabilité d'un écart de +/- 13 € autour de 170 €
pvalue_101(170.0, 5.0, 10000, 0, 13.0)

# Exemple CRM : probabilité d'un taux de qualification > 26 %
pvalue_101(18.0, 3.0, 10000, 26.0)
```

## Checklist complète : les étapes pour tester correctement une p-value

Avant de lancer un test, pendant le test, et après le test — voici la liste des étapes à respecter pour que votre p-value ait réellement du sens.

### Avant le test

1. **Formuler une hypothèse claire.** Écrivez noir sur blanc ce que vous testez. Exemple : "L'enrichissement automatique des leads augmente le taux de qualification." Sans hypothèse précise, vous ne saurez pas quoi mesurer.
2. **Choisir la métrique principale.** Une seule métrique par test. Taux de conversion ? Panier moyen ? Taux de qualification ? Si vous mesurez 10 choses en même temps, vous trouverez forcément un résultat "significatif" par pur hasard (c'est le problème des **comparaisons multiples**).
3. **Calculer la taille d'échantillon nécessaire.** Utilisez un calculateur de puissance statistique (comme celui de [Evan Miller](https://www.evanmiller.org/ab-testing/sample-size.html)). Un test sur 50 personnes ne prouvera rien. La taille dépend de l'effet minimum que vous voulez détecter et de la variabilité de vos données.
4. **Définir le seuil de significativité (α).** En général, on fixe α à 0,05 (soit 5 %). Cela signifie qu'on accepte 5 % de risque de conclure à tort qu'il y a un effet alors qu'il n'y en a pas. Ce seuil doit être décidé *avant* de regarder les résultats.
5. **Choisir entre test unilatéral et bilatéral.** Si vous voulez savoir si le changement est meilleur *ou* pire, utilisez un test bilatéral (c'est le cas le plus courant). Un test unilatéral ne se justifie que si vous êtes certain que l'effet ne peut aller que dans un sens.
6. **Fixer la durée du test à l'avance.** Un cycle business complet au minimum : 7 jours pour couvrir les variations jour/week-end, 14 jours ou plus si votre cycle de vente est long (B2B par exemple).

### Pendant le test

1. **Ne pas regarder les résultats avant la fin.** Vérifier la p-value tous les jours (le "peeking") augmente artificiellement vos chances de trouver un faux positif. Si vous devez absolument surveiller le test en cours, utilisez des méthodes de correction comme le **test séquentiel** ou la **correction de Bonferroni**.
2. **Vérifier que les groupes sont comparables.** Le groupe A et le groupe B doivent recevoir le même type de trafic. Si un groupe reçoit surtout des visiteurs mobiles et l'autre des visiteurs desktop, la comparaison est biaisée.
3. **Ne rien changer en cours de route.** Si vous modifiez la page, le ciblage ou les critères pendant le test, les résultats ne sont plus interprétables. Relancez un nouveau test propre.

### Après le test

1. **Lire la p-value correctement.** Une p-value de 0,03 signifie : "Si rien n'a changé, il y a 3 % de chance d'observer un résultat aussi extrême." Ça ne signifie *pas* : "Il y a 97 % de chance que notre changement fonctionne."
2. **Vérifier la taille de l'effet.** La p-value vous dit si le résultat est statistiquement significatif, mais pas s'il est *important*. Un test peut être significatif avec un effet de +0,1 % de conversion — trop faible pour justifier le coût du changement. Regardez aussi l'**intervalle de confiance** pour connaître la fourchette probable de l'effet réel.
3. **Chercher les biais.** Posez-vous ces questions : le test a-t-il couvert un cycle complet ? Les groupes étaient-ils homogènes ? Y a-t-il eu un événement extérieur (promotion, bug, pic de trafic) qui fausse les résultats ?
4. **Reproduire avant de généraliser.** Un seul test positif ne suffit pas. Si l'enjeu est important, relancez le test sur une autre période ou un autre segment pour confirmer le résultat. La reproductibilité est la base de toute démarche scientifique.
5. **Documenter le test.** Notez l'hypothèse, la métrique, la taille d'échantillon, la durée, la p-value, la taille de l'effet et votre conclusion. Un test non documenté est un test perdu — pour vous et pour votre équipe.

*La p-value est un outil puissant — à condition de comprendre ce qu'elle mesure et ce qu'elle ne mesure pas. La prochaine fois que vous voyez "p < 0.05" dans un rapport ou un dashboard, reprenez cette checklist et vérifiez si le test qui se cache derrière mérite vraiment qu'on lui fasse confiance.*
