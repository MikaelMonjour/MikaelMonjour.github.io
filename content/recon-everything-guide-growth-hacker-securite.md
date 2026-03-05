Title: Recon Everything : le guide complet de la reconnaissance en sécurité offensive
Date: 2026-03-05 14:00
Category: tech
Tags: securite, recon, bug-bounty, outils, tech
Slug: recon-everything-guide-growth-hacker-securite
Author: Mikael Monjour
Summary: La reconnaissance, c'est 80% du travail. Voici un guide complet et technique sur la reconnaissance en sécurité offensive : outils, commandes et méthodologie.

Il y a une image qui revient souvent dans le monde du bug bounty : celle du chasseur solitaire, capuche sur la tête, qui tape frénétiquement des commandes dans un terminal sombre. La réalité est beaucoup moins romantique. La plupart du temps, un bon chasseur de bugs passe **80 % de son temps à observer, cartographier, comprendre** — et seulement 20 % à attaquer. C'est la phase de reconnaissance, et c'est elle qui sépare les amateurs des professionnels.

Ce guide est un condensé de tout ce qu'il faut savoir pour mener une reconnaissance efficace. Il est dense, technique, et volontairement exhaustif. Si vous êtes patient et que vous aimez creuser, vous allez y trouver votre compte.

## La philosophie : comprendre avant de frapper

**Toujours lire le code source.** C'est la règle numéro un. Choisissez un programme offrant un large scope. Explorez les informations sur les domaines, les serveurs de messagerie, les connexions aux réseaux sociaux. Fouillez le site web, interceptez chaque requête et réponse via un proxy comme Burp, analysez-les. Comprenez leur infrastructure : comment ils gèrent les sessions, l'authentification, quel type de protection CSRF ils ont.

Utilisez des **tests négatifs** pour provoquer des erreurs. Les messages d'erreur sont une mine d'or : ils révèlent des chemins internes, des technologies cachées, des noms de variables. Prenez le temps de comprendre le flux de l'application pour savoir quel type de vulnérabilités chercher.

Commencez tôt. Dès qu'un programme est lancé, foncez dessus. Puis choisissez une fonctionnalité précise et creusez-la à fond. Arrêtez de courir après les outils qui brillent — Burp Suite est un couteau suisse, et c'est souvent le seul outil nécessaire pour tester une application web.

## L'art de casser les paramètres

Supposons qu'une application possède un champ qui prend un numéro (appelons-le ID). Voici la checklist systématique :

- Mettre un chiffre négatif
- Augmenter ou diminuer le nombre
- Mettre un nombre astronomique
- Remplacer par une chaîne de caractères ou un symbole
- Tenter un path traversal avec `../`
- Injecter des vecteurs XSS
- Injecter des vecteurs SQLi
- Utiliser des caractères non-ASCII
- Se tromper de type : envoyer une string dans un tableau
- Utiliser des caractères nuls ou sans valeur

Dans 80 % des cas, vous finirez par remarquer un comportement étrange. Ce comportement ne signifie pas forcément un bug reportable — mais ça signifie que vous êtes sur la bonne piste. Creusez. Et si après quelques heures vous n'en tirez rien, notez vos observations et passez à autre chose. S'accrocher à une piste morte est le plus grand tueur de motivation.

## Les questions à se poser face à chaque fonctionnalité

- **Affichage :** La page affiche-t-elle quelque chose pour les utilisateurs ? → XSS, usurpation de contenu
- **Données stockées :** La page fait-elle appel à des données persistantes ? → Injections, IDOR, stockage côté client
- **Système de fichiers :** Interagit-elle avec le serveur de fichiers ? → Upload vulnérable, LFI
- **Transactions :** Est-ce une fonction digne d'être sécurisée ? → CSRF, mode mixte
- **Privilèges :** Cette fonction est-elle privilégiée ? → Défauts de logique, escalade de privilèges
- **Entrées :** La saisie est-elle acceptée et potentiellement affichée à l'utilisateur ?
- **Persistance :** Quels endpoints sauvegardent des données ?
- **Upload :** Y a-t-il une fonctionnalité de téléchargement de fichiers ?
- **Auth :** Quel type d'authentification est utilisé ?

Concentrez-vous sur les fonctionnalités qui ont été redessinées ou modifiées récemment. Les nouvelles features sont souvent moins testées. Et n'oubliez pas : **les développeurs soulignent souvent leurs propres faiblesses**, que ce soit dans leur gestion du code ou dans les commentaires.

## Mesures à prendre à l'approche d'une cible

1. Contrôler la portée (scope) de la cible (`*.example.com`)
2. Trouver les sous-domaines
3. Exécuter masscan
4. Vérifier quels domaines sont résolus
5. Prendre des screenshots
6. Faire de la découverte de contenu (directory bruteforce)

## Outils web pour commencer

Avant de sortir le terminal, ces outils en ligne donnent déjà énormément d'informations :

- [pentest-tools.com](https://pentest-tools.com/)
- [VirusTotal](https://www.virustotal.com/)
- [Shodan](https://www.shodan.io/)
- [crt.sh](https://crt.sh/?q=%25target.com)
- [DNSDumpster](https://dnsdumpster.com/)
- [Censys](https://censys.io)

---

## ATTENTION : avant de commencer

- Certains outils demandent une connaissance avancée
- La majorité des configurations sont faites sur Linux (Kali, Ubuntu, Debian) — toute utilisation sur Windows ou Mac risque d'endommager votre système. Utilisez un container Docker ou une machine virtuelle
- Les lignes commençant par `$` indiquent une exécution sur le terminal
- Certaines commandes ne fonctionnent pas en copier-coller
- Sachez utiliser `chmod` et comprendre le fonctionnement des chemins (path) sur votre OS
- Certains outils ont pu être mis à jour ou ne sont plus maintenus
- Installer des outils hors environnement virtuel peut casser vos dépendances — **préférez toujours un venv**
- Vérifiez les versions des langages de programmation utilisés
- **Si vous n'êtes pas patient et que vous ne vous préparez pas à avoir des galères, ce qui suit n'est pas pour vous**

---

## 1. Énumération des sous-domaines

Comme le dit **NahamSec** : *"La reconnaissance ne doit pas se limiter à la recherche de biens et de choses périmées. Il s'agit aussi de comprendre l'application et de trouver des fonctionnalités qui ne sont pas facilement accessibles."*

Deux types de corrélation :

- **Corrélation verticale** : tous les sous-domaines d'un domaine (`maps.google.com`, `mail.google.com`...)
- **Corrélation horizontale** : tout ce qui est acquis par une même entité (`google.com`, `youtube.com`, `blogger.com`...)

**Rappel :** préférez l'utilisation des outils dans un environnement virtuel :

    :::bash
    $ cd home/user/dossier/
    $ python3 -m venv venv
    $ source venv/bin/activate
    $ pip install toolname

### Sublist3r

[github.com/aboul3la/Sublist3r](https://github.com/aboul3la/Sublist3r)

    :::bash
    $ git clone https://github.com/aboul3la/Sublist3r.git
    $ sudo pip install -r requirements.txt
    $ python sublist3r.py -d example.com

Alias utile :

    :::bash
    $ alias sublist3r='python /path/to/Sublist3r/sublist3r.py -d '

### subfinder

[github.com/subfinder/subfinder](https://github.com/subfinder/subfinder)

    :::bash
    $ go get github.com/subfinder/subfinder
    $ subfinder -d freelancer.com
    $ subfinder -d <domain> -recursive -silent -t 200 -v -o <outfile>

### findomain

[github.com/Edu4rdSHL/findomain](https://github.com/Edu4rdSHL/findomain) — Surveillance de sous-domaines avec webhooks Slack/Discord.

    :::bash
    $ wget https://github.com/Edu4rdSHL/findomain/releases/latest/download/findomain-linux
    $ chmod +x findomain-linux
    $ findomain -t example.com

### assetfinder

[github.com/tomnomnom/assetfinder](https://github.com/tomnomnom/assetfinder)

    :::bash
    $ go get -u github.com/tomnomnom/assetfinder
    $ assetfinder --subs-only <domain>
    $ cat domains | assetfinder --subs-only

### Amass (OWASP)

[github.com/OWASP/Amass](https://github.com/OWASP/Amass)

    :::bash
    $ go get -u github.com/OWASP/Amass/...
    $ amass enum -o subdomains.txt -d output_file.txt
    $ amass intel -whois -d example.com

### censys-enumeration

[github.com/0xbharath/censys-enumeration](https://github.com/0xbharath/censys-enumeration) — L'étape la plus importante : les sous-domaines trouvés ici sont souvent invisibles aux autres outils car votre wordlist n'a pas les patterns nécessaires.

    :::bash
    $ git clone git@github.com:yamakira/censys-enumeration.git
    $ pip install -r requirements.txt
    $ python censys_enumeration.py --no-emails --verbose --outfile results.json domains.txt

### altdns

[github.com/infosec-au/altdns](https://github.com/infosec-au/altdns) — Génère les combinaisons possibles du domaine d'origine avec les mots d'une wordlist.

    :::bash
    $ pip install py-altdns
    $ altdns -i subdomains.txt -o data_output -w words.txt -s results_output.txt

### massdns

[github.com/blechschmidt/massdns](https://github.com/blechschmidt/massdns)

    :::bash
    $ git clone https://github.com/blechschmidt/massdns.git
    $ cd massdns && make
    $ ./bin/massdns -r lists/resolvers.txt -t A domains.txt > results.txt

### domains-from-csp

[github.com/0xbharath/domains-from-csp](https://github.com/0xbharath/domains-from-csp) — Extrait les domaines autorisés depuis l'en-tête Content-Security-Policy.

    :::bash
    $ python csp_parser.py target_url
    $ python csp_parser.py target_url --resolve

### SPF Records

[github.com/0xbharath/assets-from-spf](https://github.com/0xbharath/assets-from-spf/) — Analyse les netblocks et noms de domaine depuis l'enregistrement DNS SPF.

    :::bash
    $ python assets_from_spf.py target_url
    $ python assets_from_spf.py target_url --asn

### Récupérer les numéros ASN

    :::bash
    $ curl -s http://ip-api.com/json/192.30.253.113 | jq -r .as
    $ whois -h whois.radb.net -- '-i origin AS36459' | grep -Eo "([0-9.]+){4}/[0-9]+" | uniq
    $ nmap --script targets-asn --script-args targets-asn.asn=17012 > paypal.txt

### Autres outils d'énumération

- **Certspotter** — [certspotter.com](https://certspotter.com/api/v0/certs?domain=hackerone.com) — Corrélation verticale et horizontale via les certificats
- **crt.sh** — [crt.sh](https://crt.sh/?q=%25domain.com)
- **knockpy** — [github.com/guelfoweb/knock](https://github.com/guelfoweb/knock.git)
- **Shodan** — Recherche par ports (8443, 8080), titre ("Dashboard[Jenkins]"), hostname, org, ssl
- **Viewdns.info** — Recherche inversée de whois pour l'énumération horizontale
- **Sublert** — [github.com/yassineaboukir/sublert](https://github.com/yassineaboukir/sublert) — Surveillance automatique des nouveaux sous-domaines via la transparence des certificats

## 2. Découverte de contenu (Directory Bruteforcing)

- Utilisez `robots.txt` pour déterminer les répertoires cachés
- Scrapez l'hôte pour découvrir les endpoints d'API
- Vérifiez le port 8443
- Vérifiez si `/admin/` renvoie un 403, puis énumérez son contenu
- Regardez si `/admin/users.php` renvoie un 200

### ffuf

[github.com/ffuf/ffuf](https://github.com/ffuf/ffuf) — Fuzzer web ultra-rapide écrit en Go.

    :::bash
    $ go get github.com/ffuf/ffuf

    # Découverte de répertoires
    $ ffuf -w /path/to/wordlist -u https://target/FUZZ

    # Multi-hôtes
    $ ffuf -w hosts.txt:HOSTS -w content.txt:FUZZ -u https://HOSTS/FUZZ

    # Découverte de virtual hosts
    $ ffuf -c -w /path/to/wordlist -u http://example.com -H "Host: FUZZ.example.com" -fs <length>

    # Fuzzing de paramètres GET
    $ ffuf -w /path/to/paramnames.txt -u https://target/script.php?FUZZ=test_value -fs 4242

    # Fuzzing POST
    $ ffuf -w /path/to/postdata.txt -X POST -d "username=admin\&password=FUZZ" -u https://target/login.php -fc 401

### dirsearch

[github.com/maurosoria/dirsearch](https://github.com/maurosoria/dirsearch)

    :::bash
    $ git clone https://github.com/maurosoria/dirsearch.git
    $ python3 dirsearch.py -e php,txt,zip -u https://target -w db/dicc.txt --recursive -R 2

### Gobuster

    :::bash
    $ go get github.com/OJ/gobuster
    $ gobuster dir -u https://mysite.com/path -c 'session=123456' -t 50 -w common-files.txt -x .php,.html

### wfuzz

    :::bash
    $ pip install wfuzz
    $ wfuzz -w raft-large-directories.txt --sc 200,403,302 http://testphp.vulnweb.com/FUZZ

## 3. Screenshots et cartographie visuelle

Regardez les en-têtes pour voir quelles mesures de sécurité sont en place : `X-XSS-Protection`, `X-Frame-Options: deny`. Connaître ses limites, c'est connaître ses opportunités.

### Aquatone

    :::bash
    $ go get -u github.com/michenriksen/aquatone
    $ cat hosts.txt | aquatone -out ~/aquatone/example.com

### EyeWitness

    :::bash
    $ git clone https://github.com/FortyNorthSecurity/EyeWitness.git
    $ ./EyeWitness -f urls.txt --web
    $ ./EyeWitness -x urls.xml --timeout 8 --headless

### Webscreenshot

    :::bash
    $ pip install webscreenshot
    $ python webscreenshot.py -i list.txt -v

## 4. Vérifier le CMS et les WAF

- **Wappalyzer** — Extension navigateur pour identifier les technologies
- **Builtwith** — [builtwith.com](https://builtwith.com/)
- **Retire.js** — Détecte les bibliothèques JS obsolètes
- **WafW00f** — [github.com/sandrogauci/wafw00f](https://github.com/sandrogauci/wafw00f) — Détection des WAF

## 5. Google Dorks

Quelques dorks utiles pour la reconnaissance :

    :::bash
    # Trouver des programmes de bug bounty
    site:.eu responsible disclosure
    site:.nl bug bounty

    # Identifier des CMS
    "index of" inurl:wp-content/
    inurl:"q=user/password"

    # Chercher dans du code
    site:github.com "company" password
    site:pastebin.com "keyword"
    site:trello.com "keyword"

    # Chercher des infos sensibles
    site:codepad.co "company"
    site:npmjs.com "keyword"
    site:gitlab "keyword"

## 6. GitHub Recon — la mine d'or

GitHub est extrêmement utile pour trouver des informations sensibles : clés d'accès, mots de passe, endpoints ouverts, buckets S3, fichiers de sauvegarde.

Recherchez dans les repos de votre cible :

- `API`, `key`, `token`, `secret`, `password`, `vulnerable`
- `TODO`, `CSRF`, `random`, `hash`, `MD5`, `HMAC`
- Les **Issues** — les équipes partagent énormément d'infos sur leur infra dans les discussions

### gitrob

    :::bash
    $ go get github.com/michenriksen/gitrob
    $ gitrob [options] target [target2] ... [targetN]

### shhgit

Trouve les secrets en temps réel en écoutant l'API GitHub Events.

    :::bash
    $ go get github.com/eth0izzle/shhgit
    $ shhgit
    $ shhgit --search-query AWS_ACCESS_KEY_ID=AKIA

### TruffleHog

Fouille l'historique des commits à la recherche de secrets.

    :::bash
    $ pip install truffleHog
    $ truffleHog --regex --entropy=False https://github.com/dxa4481/truffleHog.git

### gitGraber

Surveillance en temps réel pour Google, Amazon, Paypal, Github, Mailgun, Facebook, Twitter, Heroku, Stripe...

    :::bash
    $ git clone https://github.com/hisxo/gitGraber.git
    $ pip3 install -r requirements.txt
    $ python3 gitGraber.py -k wordlists/keywords.txt -q "uber" -s

## 7. Fichiers JavaScript

Les fichiers JS contiennent souvent des informations sensibles : secrets, jetons hardcodés, clés d'accès AWS, buckets S3 ouverts, endpoints internes.

### LinkFinder

Découvre les endpoints et leurs paramètres dans les fichiers JS.

    :::bash
    $ git clone https://github.com/GerbenJavado/LinkFinder.git
    $ pip3 install -r requirements.txt
    $ python linkfinder.py -i https://example.com/1.js -o results.html
    $ python linkfinder.py -i https://example.com -d

### getJS

    :::bash
    $ go get github.com/003random/getJS
    $ cat domains.txt | getJS | tojson
    $ getJS -input=domains.txt

## 8. Wayback Machine

En cherchant dans la Wayback Machine, on peut trouver : des fichiers JS anciens et abandonnés, d'anciens endpoints d'API, des endpoints de staging avec des commentaires juteux dans le code source. Si vous obtenez un 403 sur une page, cherchez-la dans la Wayback Machine — parfois elle y est exposée.

### waybackurls

    :::bash
    $ go get github.com/tomnomnom/waybackurls
    $ cat domains.txt | waybackurls > urls

### Générer une wordlist depuis le Wayback

    :::bash
    $ curl -s "http://web.archive.org/cdx/search/cdx?url=hackerone.com/*&output=text&fl=original&collapse=urlkey" \
      | sed 's/\//\n/g' | sort -u \
      | grep -v 'svg\|.png\|.img\|.ttf\|http:\|:\|.eot\|woff\|ico\|css\|bootstrap\|wordpress\|.jpg\|.jpeg' > wordlist.txt

## 9. Port Scanning

Analysez chaque adresse IP associée aux sous-domaines. Recherchez les services sur des ports inhabituels et les versions obsolètes potentiellement vulnérables.

### Masscan

Scanner de ports à l'échelle d'Internet — peut scanner tout Internet en moins de 6 minutes.

    :::bash
    $ sudo apt-get install git gcc make libpcap-dev
    $ git clone https://github.com/robertdavidgraham/masscan
    $ cd masscan && make -j8

    # Usage
    $ masscan -p1-65535 -iL $TARGET_LIST --max-rate 10000 -oG $TARGET_OUTPUT
    $ masscan -p80,8000-8100 10.0.0.0/8

### Nmap

    :::bash
    $ nmap -p- -sV -iL targets.txt -oX output.xml
    $ sudo nmap -sS -T4 -sC -oA report --stylesheet \
      https://raw.githubusercontent.com/honze-net/nmap-bootstrap-xsl/master/nmap-bootstrap.xsl -iL subdomain.txt

## 10. Subdomain Takeover

### SubOver

    :::bash
    $ go get github.com/Ice3man543/SubOver
    $ ./SubOver -l subdomains.txt

### subjack

    :::bash
    $ go get github.com/haccer/subjack
    $ ./subjack -w subdomains.txt -t 100 -timeout 30 -o results.txt -ssl

## 11. Outils complémentaires

### Parameth — Découverte de paramètres

    :::bash
    $ git clone https://github.com/maK-/parameth.git
    $ ./parameth.py -u http://example.com/test.php

### Arjun — Suite de découverte de paramètres HTTP

    :::bash
    $ git clone https://github.com/s0md3v/Arjun.git
    $ python3 arjun.py -u https://api.example.com/endpoint --get
    $ python3 arjun.py --urls targets.txt --get

### XSStrike — Scanner XSS avancé

    :::bash
    $ git clone https://github.com/s0md3v/XSStrike.git
    $ python xsstrike.py -u "http://example.com/search.php?q=query"

### Commix — Injection de commandes OS

    :::bash
    $ git clone https://github.com/commixproject/commix.git commix
    $ python commix.py --url="http://target/vuln.php" --data="param=value"

### Bolt — Scanner CSRF

    :::bash
    $ git clone https://github.com/s0md3v/Bolt.git
    $ python3 bolt.py -u https://github.com -l 2

### CORS Scanner

    :::bash
    $ git clone https://github.com/chenjj/CORScanner.git
    $ python cors_scan.py -u example.com
    $ python cors_scan.py -i top_100_domains.txt -t 100

### SSRFmap

    :::bash
    $ git clone https://github.com/swisskyrepo/SSRFmap
    $ pip3 install -r requirements.txt
    $ python ssrfmap.py -r data/request.txt -p url -m readfiles,portscan

## 12. Wordlists et Payloads

- [SecLists](https://github.com/danielmiessler/SecLists) — raft-large-words.txt et bien plus
- [contentdiscoveryall.txt](https://gist.github.com/jhaddix/b80ea67d85c13206125806f0828f4d10) de jhaddix
- [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings)
- [XSS Payloads](http://www.xss-payloads.com/)
- [SQL Injection Payloads](https://github.com/trietptm/SQL-Injection-Payloads)

## Le workflow complet de bout en bout

1. **Énumérer les sous-domaines** avec amass, assetfinder, subfinder
2. **Générer les permutations** avec la wordlist CommonSpeak2
3. **Résoudre avec massdns** : `./bin/massdns -r lists/resolvers.txt -t A domains.txt > results.txt`
4. **Récupérer les resolvers** avec bass : `python3 bass.py -d target.com -o resolvers.txt`
5. **Générer les combinaisons** avec dnsgen : `cat domains.txt | dnsgen -- | massdns -r resolvers.txt -t A -o J --flush 2>/dev/null`
6. **Port scan** avec masscan + nmap pour la version
7. **Recon GitHub**
8. **Screenshots** avec aquatone
9. **Directory bruteforce** avec ffuf
10. **Analyser les fichiers JS**, chercher les tokens et clés secrètes
11. **Wayback Machine** pour les anciens fichiers JS et les pages 403
12. **Importer dans Burp** : `cat file | parallel -j 200 curl -L -o /dev/null {} -x 127.0.0.1:8080 -k -s`

## Lectures recommandées

- [Subdomain Takeover](https://0xpatrik.com/subdomain-takeover/) par Patrik
- [Subdomain Enumeration](https://0xpatrik.com/subdomain-enumeration-2019/)
- [Can-I-take-over-xyz](https://github.com/EdOverflow/can-i-take-over-xyz)
- [Serverless Toolkit for Pentesters](https://blog.ropnop.com/serverless-toolkit-for-pentesters/)
- [Docker for Pentesters](https://blog.ropnop.com/docker-for-pentesters/)
- [HTTP Desync Attacks](https://portswigger.net/research/http-desync-attacks-request-smuggling-reborn)

*Cet article est inspiré et adapté du guide "Recon Everything", traduit de l'anglais avec des précisions et modifications.*
