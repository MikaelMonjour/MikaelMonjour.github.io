Title: tcpdump : guide complet de l'analyseur de paquets réseau
Date: 2026-03-05 18:00
Category: tech
Tags: securite, reseau, outils, tech
Slug: tcpdump-guide-complet
Author: Mikael Monjour
Summary: Guide complet de tcpdump, le puissant outil en ligne de commande pour l'analyse des paquets réseau sous Linux. Couvre les commandes de base, les filtres avancés, l'analyse de protocoles, les requêtes HTTP, les drapeaux TCP, et l'intégration avec Wireshark.

[TOC]

## Introduction

**tcpdump** est un puissant outil en ligne de commande pour l'analyse des paquets réseau. Il permet d'afficher les paquets TCP/IP et autres protocoles qui sont reçus et transmis sur une interface réseau.

tcpdump a été initialement développé en **1988** par Van Jacobson, Sally Floyd, Vern Paxson et Steven McCanne au **Lawrence Berkeley Laboratory** (Network Research Group). Il fonctionne sur la plupart des systèmes d'exploitation basés sur Linux et utilise la bibliothèque **libpcap** (C/C++) pour capturer les paquets.

> **Note :** l'équivalent Windows s'appelle **WinDump** et utilise la bibliothèque WinPcap/Npcap.

### Cas d'utilisation

tcpdump est indispensable pour :

- **Diagnostiquer** les problèmes réseau (perte de paquets, latence, erreurs de routage)
- **Analyser** le fonctionnement d'outils de sécurité (pare-feu, IDS/IPS)
- **Capturer** du trafic pour analyse ultérieure (fichiers `.pcap`)
- **Déboguer** des applications réseau (API, services web, DNS)
- **Auditer** la sécurité d'un réseau (reniflage, détection d'anomalies)

<div class="mermaid">
graph LR
    A[Interface réseau<br/>eth0, wlan0...] -->|libpcap| B[tcpdump]
    B --> C[Affichage terminal]
    B --> D[Fichier .pcap]
    D --> E[Wireshark]
    D --> F[Analyse offline<br/>tcpdump -r]
    style B fill:#2196F3,stroke:#1565C0,color:#fff
    style D fill:#FF9800,stroke:#E65100,color:#fff
    style E fill:#4CAF50,stroke:#2E7D32,color:#fff
</div>

---

## Partie 1 — Commandes de base

### Options et aide

Pour afficher les options disponibles ou la version :

```bash
# Afficher l'aide
tcpdump -h
tcpdump --help

# Afficher la version de tcpdump, libpcap et OpenSSL
tcpdump --version
```

### Lister les interfaces réseau

Une **interface** est le point d'interconnexion entre un ordinateur et un réseau. On peut lister les interfaces disponibles avec :

```bash
tcpdump --list-interfaces
tcpdump -D
```

Chaque interface reçoit un numéro qui peut être utilisé avec le paramètre `-i` pour cibler une interface particulière.

> **Astuce :** si `ifconfig -a` ne fonctionne pas, `tcpdump -D` reste une alternative fiable pour lister les interfaces.

### Capture par défaut

La forme la plus simple lance une capture sur l'interface par défaut :

```bash
tcpdump
```

Par défaut, tcpdump capture sur la première interface active et affiche les paquets en continu jusqu'à interruption (`Ctrl+C`).

### Capturer sur une interface spécifique (`-i`)

Pour capturer le trafic sur une interface particulière (par exemple `eth0` pour Ethernet) :

```bash
tcpdump -i eth0
```

### Limiter le nombre de paquets (`-c`)

Le paramètre `-c` permet de capturer un nombre précis de paquets, puis de s'arrêter :

```bash
# Capturer exactement 10 paquets sur eth0
tcpdump -i eth0 -c 10
```

### Mode verbeux (`-v`, `-vv`, `-vvv`)

Le mode verbeux fournit des informations supplémentaires sur les paquets capturés.

| Paramètre | Niveau | Informations |
|-----------|--------|--------------|
| `-v` | Verbeux | TTL, identification, longueur totale, options IP, checksums IP/ICMP |
| `-vv` | Très verbeux | + champs NFS, décodage complet des paquets SMB |
| `-vvv` | Maximum | + options Telnet et données supplémentaires |

```bash
# Mode verbeux simple
tcpdump -i eth0 -c 5 -v

# Mode très verbeux
tcpdump -i eth0 -c 5 -vv

# Mode maximum
tcpdump -i eth0 -c 5 -vvv
```

### Affichage ASCII (`-A`)

Le paramètre `-A` affiche le contenu de chaque paquet en **code ASCII**, ce qui est utile pour lire le contenu textuel des échanges (requêtes HTTP, en-têtes, etc.) :

```bash
tcpdump -i eth0 -c 5 -A
```

### Ne pas convertir les adresses (`-nn`)

Par défaut, tcpdump tente de résoudre les adresses IP en noms d'hôtes et les numéros de port en noms de services. Le paramètre `-nn` désactive cette résolution pour afficher les **adresses et ports bruts** :

```bash
# Avec résolution (par défaut)
tcpdump -i eth0 -c 5

# Sans résolution — adresses IP et ports numériques
tcpdump -i eth0 -c 5 -nn
```

### Mode rapide (`-q`)

Le paramètre `-q` (quick) affiche moins d'informations par paquet, ce qui accélère l'affichage :

```bash
tcpdump -i eth0 -c 5 -q
```

---

## Partie 2 — Filtres

Les filtres sont au cœur de la puissance de tcpdump. Ils permettent de cibler précisément le trafic à analyser.

<div class="mermaid">
graph TD
    A[Filtres tcpdump] --> B[Par hôte]
    A --> C[Par port]
    A --> D[Par protocole]
    A --> E[Par réseau]
    A --> F[Par direction]
    B --> B1["host 192.168.1.1"]
    B --> B2["src / dst"]
    C --> C1["port 80"]
    C --> C2["portrange 21-80"]
    D --> D1["tcp / udp / icmp"]
    E --> E1["net 192.168.0.0/24"]
    F --> F1["-Q in / -Q out"]
    style A fill:#9C27B0,stroke:#6A1B9A,color:#fff
</div>

### Filtre de port

Pour analyser le trafic sur un **port spécifique** :

```bash
# Trafic HTTP (port 80)
tcpdump -i eth0 -c 5 -v port 80

# Trafic HTTPS (port 443)
tcpdump -i eth0 -c 5 port 443

# Trafic DNS (port 53)
tcpdump -i eth0 -c 5 port 53
```

### Plage de ports (`portrange`)

Pour surveiller une **gamme de ports** :

```bash
# Surveiller les ports 21 à 80
tcpdump -i eth0 portrange 21-80
```

### Filtre d'hôte

Pour analyser le trafic **vers ou depuis** un hôte particulier :

```bash
# Tout le trafic lié à un hôte
tcpdump host 104.28.6.89 -c 10 -A -n

# Uniquement le trafic VERS une destination
tcpdump -i eth0 dst google.com

# Uniquement le trafic DEPUIS une source
tcpdump -i eth0 src google.com
```

### Filtre de réseau

Pour capturer les paquets en provenance ou à destination d'un **réseau entier** :

```bash
tcpdump net 192.168.0.0/24 -c 5
```

### Filtre de protocole

Pour filtrer par **protocole** (ICMP, TCP, UDP, etc.) :

```bash
# Paquets ICMP uniquement (ping)
tcpdump -i eth0 icmp -c 10

# Paquets UDP uniquement
tcpdump -i eth0 udp -c 10
```

### Direction des paquets (`-Q`)

Pour filtrer par **direction** du flux de données :

```bash
# Paquets entrants uniquement
tcpdump -i eth0 icmp -c 5 -Q in

# Paquets sortants uniquement
tcpdump -i eth0 icmp -c 5 -Q out
```

---

## Partie 3 — Affichage avancé des paquets

### En-tête de chaque paquet (`-X`)

Le paramètre `-X` affiche les en-têtes et le contenu des paquets en **hexadécimal et ASCII** simultanément :

```bash
tcpdump -i eth0 -c 3 -X
```

Les en-têtes contiennent les informations de contrôle : longueur du paquet, drapeaux de synchronisation, valeurs hexadécimales, etc.

### Numéro de séquence TCP (`-S`)

Le paramètre `-S` affiche les **numéros de séquence TCP absolus** au lieu des numéros relatifs :

```bash
tcpdump -i eth0 -nnXS
```

> Chaque connexion TCP commence avec un numéro de séquence initial (ISN) choisi aléatoirement. Les données commencent à ISN+1.

### Comptage en direct (`--number`)

Le paramètre `--number` numérote chaque paquet capturé en temps réel :

```bash
tcpdump -i eth0 --number
```

### En-tête de niveau liaison (`-e`)

Le paramètre `-e` affiche les **en-têtes de couche liaison** (layer 2), notamment les adresses MAC pour Ethernet et IEEE 802.11 :

```bash
# Sans en-tête de liaison
tcpdump -i eth0 -c 5

# Avec en-tête de liaison (adresses MAC)
tcpdump -i eth0 -c 5 -e
```

### Affichage hexadécimal (`-x`, `-xx`, `-X`, `-XX`)

tcpdump propose plusieurs niveaux d'affichage hexadécimal :

| Paramètre | Affichage |
|-----------|-----------|
| `-x` | En-têtes en hexadécimal |
| `-xx` | En-têtes + en-tête de liaison en hexadécimal |
| `-X` | En-têtes en hexadécimal **+ ASCII** |
| `-XX` | En-têtes + en-tête de liaison en hexadécimal **+ ASCII** |

```bash
tcpdump -i eth0 -c 2 -x
tcpdump -i eth0 -c 2 -xx
tcpdump -i eth0 -c 2 -X
tcpdump -i eth0 -c 2 -XX
```

---

## Partie 4 — Horodatage (timestamp)

tcpdump offre un contrôle précis sur l'affichage des **timestamps** :

| Paramètre | Comportement |
|-----------|-------------|
| `-t` | Pas de timestamp |
| `-tt` | Timestamp Unix (secondes depuis l'epoch) |
| `-ttt` | Delta depuis le paquet **précédent** (microsecondes) |
| `-tttt` | Date et heure complètes (lisible) |
| `-ttttt` | Delta depuis le **premier paquet** |

```bash
# Pas de timestamp
tcpdump -i eth0 -c 2 -t

# Timestamp Unix
tcpdump -i eth0 -c 2 -tt

# Delta entre paquets
tcpdump -i eth0 -c 2 -ttt

# Date et heure lisibles
tcpdump -i eth0 -c 2 -tttt

# Delta depuis le début de la capture
tcpdump -i eth0 -c 2 -ttttt
```

<div class="mermaid">
graph LR
    subgraph "Formats de timestamp"
    A["-t<br/>(aucun)"] ~~~ B["-tt<br/>1709654321.123456"]
    B ~~~ C["-ttt<br/>0.003215"]
    C ~~~ D["-tttt<br/>2026-03-05 14:25:21"]
    D ~~~ E["-ttttt<br/>0.125432"]
    end
</div>

---

## Partie 5 — Lecture, écriture et snaplen

### Écrire dans un fichier `.pcap` (`-w`)

Pour sauvegarder les paquets bruts dans un fichier pour analyse ultérieure :

```bash
# Sauvegarder 10 paquets ICMP dans un fichier
tcpdump -i eth0 icmp -c 10 -w capture.pcap
```

### Lire un fichier `.pcap` (`-r`)

Pour relire un fichier de capture :

```bash
tcpdump -r capture.pcap
```

> **Astuce :** les fichiers `.pcap` peuvent aussi être ouverts dans **Wireshark** pour une analyse graphique.

### Longueur de capture — snaplen (`-s`)

Le **snaplen** (snapshot length) définit le nombre d'octets capturés par paquet. Par défaut : **262 144 octets**.

Réduire le snaplen accélère la capture et réduit la taille des fichiers, mais tronque les données :

```bash
# Capturer seulement 10 octets par paquet
tcpdump -i eth0 icmp -s 10 -c 2

# Capturer 25 octets
tcpdump -i eth0 icmp -s 25 -c 2

# Capturer 96 octets (en-têtes uniquement pour la plupart des protocoles)
tcpdump -i eth0 icmp -s 96 -c 2

# Capturer le paquet complet (snaplen 0 = illimité)
tcpdump -i eth0 -s 0 -c 2
```

<div class="mermaid">
graph LR
    A["Paquet complet<br/>1500 octets"] --> B{"-s snaplen"}
    B -->|"-s 10"| C["10 octets<br/>⚡ Rapide"]
    B -->|"-s 96"| D["96 octets<br/>En-têtes"]
    B -->|"-s 0"| E["Tout<br/>📦 Complet"]
    style C fill:#4CAF50,color:#fff
    style D fill:#FF9800,color:#fff
    style E fill:#F44336,color:#fff
</div>

---

## Partie 6 — Mode dump et scan utilisateur

### Mode dump (`-d`, `-dd`, `-ddd`)

Le mode dump permet de visualiser le **filtre BPF** (Berkeley Packet Filter) compilé :

| Paramètre | Format de sortie |
|-----------|-----------------|
| `-d` | Code assembleur lisible |
| `-dd` | Fragment de programme C |
| `-ddd` | Nombres décimaux avec compteur |

```bash
tcpdump -i eth0 -c 5 -d
tcpdump -i eth0 -c 5 -dd
tcpdump -i eth0 -c 5 -ddd
```

### Changement d'utilisateur (`-Z`)

Lorsque tcpdump est exécuté en tant que `root`, il peut changer d'utilisateur après l'ouverture de l'interface de capture (sécurité par moindre privilège) :

```bash
# Exécuter en tant que root, puis passer à l'utilisateur kali
tcpdump -i eth0 -c 2 -Z kali

# Alternative avec --relinquish-privileges
tcpdump -i eth0 -c 2 --relinquish-privileges=kali
```

---

## Partie 7 — Forcer l'interprétation de protocoles (`-T`)

Le paramètre `-T` force tcpdump à interpréter les paquets selon un **protocole spécifique**. Cela permet d'analyser du trafic encapsulé ou non standard.

```bash
tcpdump -i eth0 -c 5 -T <protocole>
```

### Protocoles supportés

| Protocole | Description | Commande |
|-----------|------------|----------|
| **RADIUS** | Remote Authentication Dial-in User Service (port 1812). Authentification centralisée | `tcpdump -i eth0 -c5 -T radius` |
| **AODV** | Ad-hoc On-demand Distance Vector. Routage pour réseaux sans fil ad hoc | `tcpdump -i eth0 -c5 -T aodv` |
| **RPC** | Remote Procedure Call. Appel de procédure à distance | `tcpdump -i eth0 -c5 -T rpc` |
| **CNFP** | Cisco NetFlow Protocol. Collecte et surveillance du trafic réseau | `tcpdump -i eth0 -c5 -T cnfp` |
| **LMP** | Link Management Protocol. Configuration de périphériques réseau optiques | `tcpdump -i eth0 -c5 -T lmp` |
| **PGM** | Pragmatic General Multicast. Transport multicast fiable | `tcpdump -i eth0 -c5 -T pgm` |
| **RTP** | Real-Time Protocol. Flux multimédia (audio/vidéo) | `tcpdump -i eth0 -c5 -T rtp` |
| **RTCP** | Real-Time Control Protocol. Contrôle pour RTP | `tcpdump -i eth0 -c5 -T rtcp` |
| **SNMP** | Simple Network Management Protocol. Gestion de dispositifs réseau | `tcpdump -i eth0 -c5 -T snmp` |
| **TFTP** | Trivial File Transfer Protocol. Transfert de fichiers simple (boot réseau) | `tcpdump -i eth0 -c5 -T tftp` |
| **VAT** | Visual Audio Tool. Média audio/visuel | `tcpdump -i eth0 -c5 -T vat` |
| **WB** | Distributed White Board. Tableau blanc partagé en réseau | `tcpdump -i eth0 -c5 -T wb` |
| **VXLAN** | Virtual Xtensible LAN. Virtualisation réseau pour le cloud (encapsulation L3) | `tcpdump -i eth0 -c5 -T vxlan` |

<div class="mermaid">
graph TB
    T["-T protocole"] --> L4["Couche 4 — Transport"]
    T --> L7["Couche 7 — Application"]
    T --> VIRT["Virtualisation"]
    L4 --> RTP2["RTP / RTCP"]
    L4 --> PGM2["PGM"]
    L7 --> RADIUS2["RADIUS"]
    L7 --> SNMP2["SNMP"]
    L7 --> TFTP2["TFTP"]
    L7 --> RPC2["RPC"]
    VIRT --> VXLAN2["VXLAN"]
    style T fill:#673AB7,stroke:#4527A0,color:#fff
    style L4 fill:#0288D1,color:#fff
    style L7 fill:#388E3C,color:#fff
    style VIRT fill:#F57C00,color:#fff
</div>

---

## Partie 8 — Mode promiscuous

### Activer le mode promiscuous

En mode **promiscuous**, la carte réseau transmet **tous les paquets** reçus au système d'exploitation, pas seulement ceux destinés à son adresse MAC. C'est essentiel pour le reniflage de paquets sur un réseau local :

```bash
# Activer le mode promiscuous sur eth0
ifconfig eth0 promisc

# Vérifier l'état
ifconfig eth0

# Capturer en mode promiscuous
tcpdump -i eth0 -c 10
```

### Désactiver le mode promiscuous

Pour capturer en mode **non-promiscuous** (multicast uniquement) sans modifier les paramètres de l'interface :

```bash
tcpdump -i eth0 -c 5 --no-promiscuous-mode
```

<div class="mermaid">
graph LR
    subgraph "Mode normal"
    A1[Paquet pour<br/>notre MAC] -->|✅ Capturé| B1[Système]
    A2[Paquet pour<br/>autre MAC] -->|❌ Ignoré| C1[Rejeté]
    end
    subgraph "Mode promiscuous"
    A3[Paquet pour<br/>notre MAC] -->|✅ Capturé| B2[Système]
    A4[Paquet pour<br/>autre MAC] -->|✅ Capturé| B2
    end
    style B1 fill:#4CAF50,color:#fff
    style C1 fill:#F44336,color:#fff
    style B2 fill:#4CAF50,color:#fff
</div>

---

## Partie 9 — Capturer les requêtes HTTP

tcpdump peut capturer et décoder les **requêtes HTTP** en utilisant des filtres sur les octets TCP.

### Requêtes GET

La méthode GET récupère des données depuis un serveur. Le filtre cherche la signature hexadécimale `0x47455420` (« GET ») dans le payload TCP :

```bash
tcpdump -s 0 -A -vv 'tcp[((tcp[12:1] & 0xf0) >> 2):4] = 0x47455420'
```

### Requêtes POST

La méthode POST envoie des données au serveur. La signature hexadécimale est `0x504f5354` (« POST ») :

```bash
tcpdump -s 0 -A -vv 'tcp[((tcp[12:1] & 0xf0) >> 2):4] = 0x504f5354'
```

### Capturer toutes les requêtes HTTP (GET + POST + Host)

```bash
tcpdump -v -n -l | egrep -i "POST /|GET /|Host:"
```

### Identifier le User-Agent

Pour voir quelle **application** génère le trafic :

```bash
tcpdump -nn -A -s 150 -l | grep "User-Agent:"
```

<div class="mermaid">
sequenceDiagram
    participant C as Client
    participant T as tcpdump
    participant S as Serveur

    C->>S: GET /index.html HTTP/1.1
    Note over T: Capture GET<br/>0x47455420
    S-->>C: 200 OK + HTML

    C->>S: POST /api/login HTTP/1.1
    Note over T: Capture POST<br/>0x504f5354
    S-->>C: 200 OK + JSON

    Note over T: Filtrage par<br/>User-Agent, Host
</div>

---

## Partie 10 — Drapeaux TCP

Le paquet TCP utilise des **drapeaux** (flags) pour contrôler l'état des connexions. tcpdump permet de filtrer par drapeau spécifique.

### SYN — Synchronisation

Le drapeau **SYN** initie une connexion TCP (premier paquet du three-way handshake) :

```bash
tcpdump 'tcp[tcpflags] == tcp-syn'
```

### RST — Réinitialisation

Le drapeau **RST** (reset) réinitialise une connexion, envoyé quand un paquet arrive pour un port fermé ou une connexion invalide :

```bash
tcpdump 'tcp[tcpflags] == tcp-rst'
```

### ACK — Accusé de réception

Le drapeau **ACK** confirme la bonne réception d'un paquet :

```bash
tcpdump 'tcp[tcpflags] == tcp-ack' -c 5
```

### Combinaisons courantes

```bash
# SYN-ACK (réponse au SYN)
tcpdump 'tcp[tcpflags] & (tcp-syn|tcp-ack) != 0'

# Paquets FIN (fermeture de connexion)
tcpdump 'tcp[tcpflags] & tcp-fin != 0'

# SYN sans ACK (nouvelles connexions uniquement)
tcpdump 'tcp[tcpflags] & tcp-syn != 0 and tcp[tcpflags] & tcp-ack == 0'
```

<div class="mermaid">
sequenceDiagram
    participant C as Client
    participant S as Serveur

    Note over C,S: Three-way Handshake TCP
    C->>S: SYN (seq=x)
    Note right of S: tcp-syn
    S->>C: SYN-ACK (seq=y, ack=x+1)
    Note left of C: tcp-syn + tcp-ack
    C->>S: ACK (ack=y+1)
    Note right of S: tcp-ack

    Note over C,S: Transfert de données...

    C->>S: FIN
    Note right of S: tcp-fin
    S->>C: ACK
    S->>C: FIN
    C->>S: ACK
    Note over C,S: Connexion fermée
</div>

---

## Partie 11 — tcpdump vers Wireshark

**Wireshark** est l'équivalent graphique de tcpdump. On peut capturer avec tcpdump sur une machine distante et visualiser en temps réel dans Wireshark :

```bash
# Capture distante via SSH, affichage local dans Wireshark
ssh root@machine-distante 'tcpdump -c 20 -nn -w - not port 22' | wireshark -k -i -
```

Cette commande :

1. Se connecte en SSH à la machine distante
2. Lance tcpdump qui écrit sur la sortie standard (`-w -`)
3. Exclut le trafic SSH lui-même (`not port 22`)
4. Pipe le résultat vers Wireshark qui l'affiche en temps réel (`-k -i -`)

### Workflow recommandé

Pour une analyse approfondie, il est souvent préférable de capturer d'abord, puis d'analyser :

```bash
# 1. Capturer sur le serveur
tcpdump -i eth0 -w capture.pcap -c 1000

# 2. Transférer le fichier
scp serveur:/tmp/capture.pcap .

# 3. Ouvrir dans Wireshark
wireshark capture.pcap
```

---

## Aide-mémoire (cheat sheet)

### Capture de base

| Commande | Description |
|----------|------------|
| `tcpdump -D` | Lister les interfaces |
| `tcpdump -i eth0` | Capturer sur eth0 |
| `tcpdump -i eth0 -c 10` | Capturer 10 paquets |
| `tcpdump -i eth0 -nn` | Sans résolution DNS/ports |
| `tcpdump -i eth0 -q` | Mode rapide (moins de détails) |
| `tcpdump -i eth0 -v` | Mode verbeux |
| `tcpdump -i eth0 -A` | Affichage ASCII |
| `tcpdump -i eth0 -X` | Affichage hex + ASCII |
| `tcpdump -i eth0 -e` | Afficher les en-têtes L2 (MAC) |
| `tcpdump -i eth0 -S` | Numéros de séquence absolus |

### Filtres

| Commande | Description |
|----------|------------|
| `tcpdump host 1.2.3.4` | Trafic vers/depuis un hôte |
| `tcpdump src 1.2.3.4` | Trafic depuis une source |
| `tcpdump dst 1.2.3.4` | Trafic vers une destination |
| `tcpdump net 192.168.0.0/24` | Trafic d'un réseau |
| `tcpdump port 80` | Trafic sur un port |
| `tcpdump portrange 21-80` | Trafic sur une plage de ports |
| `tcpdump icmp` | Trafic ICMP |
| `tcpdump tcp` | Trafic TCP |
| `tcpdump udp` | Trafic UDP |
| `tcpdump -Q in` | Trafic entrant |
| `tcpdump -Q out` | Trafic sortant |

### Fichiers et timestamps

| Commande | Description |
|----------|------------|
| `tcpdump -w fichier.pcap` | Écrire dans un fichier |
| `tcpdump -r fichier.pcap` | Lire un fichier |
| `tcpdump -s 96` | Snaplen de 96 octets |
| `tcpdump -t` | Pas de timestamp |
| `tcpdump -tttt` | Timestamp lisible (date + heure) |

### Drapeaux TCP et HTTP

| Commande | Description |
|----------|------------|
| `tcpdump 'tcp[tcpflags] == tcp-syn'` | Paquets SYN |
| `tcpdump 'tcp[tcpflags] == tcp-rst'` | Paquets RST |
| `tcpdump 'tcp[tcpflags] == tcp-ack'` | Paquets ACK |
| `tcpdump -s0 -A 'tcp[..] = 0x47455420'` | Requêtes GET |
| `tcpdump -s0 -A 'tcp[..] = 0x504f5354'` | Requêtes POST |

---

## Conclusion

tcpdump est un outil **indispensable** pour tout administrateur réseau ou professionnel de la sécurité. Sa force réside dans :

- Sa **disponibilité** sur quasiment tous les systèmes Linux/Unix
- Sa **légèreté** (pas d'interface graphique nécessaire)
- La **puissance** de ses filtres BPF
- Sa **compatibilité** avec Wireshark via les fichiers `.pcap`

Pour aller plus loin :

- La **page de manuel** : `man tcpdump`
- La documentation des **filtres BPF** : `man pcap-filter`
- Combinaison avec d'autres outils : `tshark`, `ngrep`, `tcpflow`
