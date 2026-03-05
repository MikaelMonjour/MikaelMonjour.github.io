Title: Programmation socket en Python : le guide complet
Date: 2026-03-05 20:00
Category: tech
Tags: python, reseau, tech
Slug: programmation-socket-python-guide-complet
Author: Mikael Monjour
Summary: Vous construisez un outil interne qui doit envoyer des données à un autre service sur le réseau. Pas un appel HTTP classique — quelque chose de plus bas niveau. Ce guide couvre tout : de l'echo server jusqu'à une application client-serveur complète avec protocole personnalisé.

Les sockets et l'API socket sont utilisés pour envoyer des messages sur un réseau. Ils fournissent une forme de communication inter-processus (IPC).

Le réseau peut être logique et local pour l'ordinateur, ou physiquement connecté à un réseau externe, avec ses propres connexions à d'autres réseaux. L'exemple le plus évident est l'Internet, auquel vous vous connectez par l'intermédiaire de votre fournisseur d'accès.

Ce tutoriel comporte trois étapes successives de la construction d'un serveur et d'un client socket avec Python :

1. Nous commencerons le tutoriel en examinant un simple serveur et un client de socket.
2. Une fois que vous aurez vu l'API et la façon dont les choses fonctionnent dans ce premier exemple, nous examinerons une version améliorée qui gère plusieurs connexions simultanément.
3. Enfin, nous passerons à la construction à titre d'exemple d'un serveur et d'un client qui fonctionne comme une véritable application de socket, avec son propre en-tête et son propre contenu personnalisé.

À la fin de ce tutoriel, vous comprendrez comment utiliser les principales fonctions et méthodes du module socket de Python pour écrire vos propres applications client-serveur. Vous apprendrez notamment à utiliser une classe personnalisée pour envoyer des messages et des données entre des terminaux, que vous pourrez utiliser pour vos propres applications.

Les exemples de ce tutoriel utilisent Python 3.6.

## Contexte

Les sockets ont une longue histoire. Leur utilisation a commencé avec ARPANET en 1971 et est devenue plus tard une API dans le système d'exploitation Berkeley Software Distribution (BSD) publié en 1983, appelé "Berkeley sockets".

Lorsque l'Internet a pris son essor dans les années 1990 avec le World Wide Web, la programmation des réseaux a fait de même. Les serveurs et les navigateurs Web n'étaient pas les seules applications à tirer parti des réseaux nouvellement connectés et à utiliser des sockets. Des applications client-serveur de tous types et de toutes tailles se sont répandues.

Aujourd'hui, bien que les protocoles sous-jacents utilisés par l'API socket aient évolué au fil des ans, et que nous en ayons vu de nouveaux, l'API de bas niveau est restée la même.

Le type le plus courant d'applications socket est l'application client-serveur, dans laquelle un côté fait office de serveur et attend les connexions des clients. C'est ce type d'application que je vais aborder dans ce tutoriel.

> Il existe également des sockets de domaine Unix, qui ne peuvent être utilisés que pour communiquer entre des processus sur un même hôte.

## Aperçu de l'API de socket

Le module de socket de Python fournit une interface avec l'API socket de Berkeley. C'est ce module que nous utiliserons et dont nous parlerons dans ce tutoriel.

Les fonctions et méthodes de l'API de socket primaire dans ce module sont :

- `socket()`
- `bind()`
- `listen()`
- `accept()`
- `connect()`
- `connect_ex()`
- `send()`
- `recv()`
- `close()`

Python fournit une API pratique et cohérente qui correspond directement à ces appels système (syscalls), leurs équivalents en C. Nous verrons comment ils sont utilisés ensemble dans la prochaine section.

Dans le cadre de sa bibliothèque standard, Python dispose également de classes qui facilitent l'utilisation de ces fonctions socket de bas niveau. Bien que le sujet ne soit pas abordé dans ce tutoriel, visitez le module `socketserver`, un framework pour les serveurs réseau.

Il existe également de nombreux modules qui mettent en œuvre des protocoles Internet de niveau supérieur comme HTTP et SMTP. Pour une vue d'ensemble, voir les [protocoles Internet et leur support](https://docs.python.org/3/library/internet.html).

## TCP Sockets

Comme vous allez le voir, nous allons créer un objet socket en utilisant `socket.socket()` et indiquer le type de socket en tant que `socket.SOCK_STREAM`.

Dans ce cas, le protocole par défaut utilisé est le protocole de contrôle de transmission (TCP). C'est un bon choix par défaut et probablement ce que vous voulez.

Pourquoi devriez-vous utiliser le TCP ? Le protocole de contrôle de transmission (TCP) :

- **Est fiable :** les paquets déposés dans le réseau sont détectés et retransmis par l'expéditeur.
- **A une livraison de données en ordre :** les données sont lues par votre application dans l'ordre où elles ont été écrites par l'expéditeur.

En revanche, les sockets User Datagram Protocol (UDP) créées avec `socket.SOCK_DGRAM` ne sont pas fiables, et les données lues par le récepteur peuvent être désordonnées par rapport aux écritures de l'émetteur.

Pourquoi est-ce important ? Les réseaux sont un système de livraison de la meilleure qualité possible. Il n'y a aucune garantie que vos données parviendront à leur destination ou que vous recevrez ce qui vous a été envoyé.

Le TCP vous évite de vous soucier des pertes de paquets, des données qui arrivent en mauvais état et de bien d'autres choses qui se produisent invariablement lorsque vous communiquez sur un réseau.

### Flux TCP : séquence des appels API

Le diagramme ci-dessous illustre la séquence des appels API de socket et le flux de données pour TCP :

<figure class="diagram">
<pre class="mermaid">
sequenceDiagram
    participant S as Serveur
    participant C as Client
    Note over S: socket()
    Note over S: bind()
    Note over S: listen()
    S->>S: accept() — bloque en attente
    Note over C: socket()
    C->>S: connect() — handshake TCP 3-way
    S-->>C: Connexion acceptée
    loop Échange de données
        C->>S: send()
        S->>S: recv()
        S->>C: send()
        C->>C: recv()
    end
    C->>S: close()
    S->>S: close()
</pre>
<figcaption>Flux TCP : séquence des appels API socket entre serveur et client</figcaption>
</figure>

La colonne de gauche représente le serveur. La colonne de droite représente le client.

En commençant par le serveur, notez les appels API pour configurer une socket "d'écoute" :

1. `socket()` — crée l'objet socket
2. `bind()` — associe la socket à une adresse et un port
3. `listen()` — met la socket en mode écoute
4. `accept()` — bloque et attend une connexion entrante

Un socket d'écoute fait exactement ce à quoi il ressemble. Il écoute les connexions des clients. Lorsqu'un client se connecte, le serveur appelle `accept()` pour accepter, ou terminer, la connexion.

Le client utilise `connect()` pour établir une connexion avec le serveur et initier un **handshake à trois** (SYN → SYN-ACK → ACK). L'étape du handshake est importante car elle garantit que chaque côté de la connexion est accessible dans le réseau.

Au milieu se trouve la section aller-retour, où les données sont échangées entre le client et le serveur à l'aide des appels `send()` et `recv()`.

En bas, le client et le serveur ferment leurs sockets respectifs avec `close()`.

## Faire un Echo, entre Client et Serveur

Maintenant que vous avez vu un aperçu de l'API de socket et de la façon dont le client et le serveur communiquent, créons notre premier client et serveur.

Nous commencerons par une implémentation simple. Le serveur va simplement renvoyer au client ce qu'il reçoit.

### Echo Server

Voici le serveur, `echo-server.py` :

```python
#!/usr/bin/env python3

import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
```

Passons en revue chaque appel API et voyons ce qui se passe.

`socket.socket()` crée un objet socket qui supporte le type de gestionnaire de contexte, vous pouvez donc l'utiliser dans une instruction `with`. Il n'est pas nécessaire d'appeler `s.close()` :

```python
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    pass  # Use the socket object without calling s.close().
```

Les arguments passés à `socket()` précisent la famille d'adresses et le type de socket. **AF_INET** est la famille d'adresses Internet pour IPv4. **SOCK_STREAM** est le type de socket pour TCP, le protocole qui sera utilisé pour transporter nos messages dans le réseau.

`bind()` est utilisé pour associer la socket à une interface réseau et un numéro de port spécifiques :

```python
HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

# ...

s.bind((HOST, PORT))
```

Les valeurs passées à `bind()` dépendent de la famille d'adresses de la socket. Dans cet exemple, nous utilisons `socket.AF_INET` (IPv4). Il s'attend donc à un 2-tuple : `(hôte, port)`.

L'hôte peut être un nom d'hôte, une adresse IP ou une chaîne vide. Si une adresse IP est utilisée, l'hôte doit être une chaîne d'adresses au format IPv4. L'adresse IP `127.0.0.1` est l'adresse IPv4 standard pour l'interface de bouclage (loopback), de sorte que seuls les processus sur l'hôte pourront se connecter au serveur. Si vous passez une chaîne vide, le serveur acceptera les connexions sur toutes les interfaces IPv4 disponibles.

Le port doit être un nombre entier compris entre 1 et 65535 (0 est réservé). Il s'agit du numéro de port TCP sur lequel les clients peuvent se connecter. Certains systèmes peuvent exiger des privilèges de super-utilisateur si le port est < 1024.

> **Note sur les noms d'hôtes :** "Si vous utilisez un nom d'hôte dans la partie hôte de l'adresse de socket IPv4/v6, le programme peut présenter un comportement non déterministe, car Python utilise la première adresse renvoyée par la résolution DNS. L'adresse socket sera résolue différemment en une adresse IPv4/v6 réelle, en fonction des résultats de la résolution DNS et/ou de la configuration de l'hôte. Pour un comportement déterministe, utilisez une adresse numérique dans la partie hôte."

Pour continuer avec l'exemple du serveur, `listen()` ouvre le serveur aux connexions. Cela en fait une socket "d'écoute" :

```python
s.listen()
conn, addr = s.accept()
```

`listen()` a un paramètre `backlog`. Il précise le nombre de connexions non acceptées que le système autorisera avant de refuser de nouvelles connexions. À partir de Python 3.5, il est facultatif. S'il n'est pas spécifié, une valeur par défaut est choisie.

`accept()` bloque et attend une connexion entrante. Lorsqu'un client se connecte, il renvoie un nouvel objet socket représentant la connexion et un tuple contenant l'adresse du client. Le tuple contiendra `(host, port)` pour les connexions IPv4.

Une chose qu'il est impératif de comprendre, c'est que nous avons maintenant un **nouvel objet socket** à partir de `accept()`. C'est important car c'est le socket que vous utiliserez pour communiquer avec le client. Il est distinct du socket d'écoute que le serveur utilise pour accepter de nouvelles connexions :

```python
conn, addr = s.accept()
with conn:
    print('Connected by', addr)
    while True:
        data = conn.recv(1024)
        if not data:
            break
        conn.sendall(data)
```

Après avoir récupéré l'objet socket client `conn` de `accept()`, une boucle infinie est utilisée pour boucler les appels bloquants vers `conn.recv()`. Cette boucle lit les données envoyées par le client et les renvoie à l'aide de `conn.sendall()`.

Si `conn.recv()` renvoie un objet de bytes vide, `b''`, alors le client a fermé la connexion et la boucle est terminée. L'instruction `with` est utilisée avec `conn` pour fermer automatiquement la socket à la fin du bloc.

### Echo Client

Regardons maintenant le client, `echo-client.py` :

```python
#!/usr/bin/env python3

import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'Hello, world')
    data = s.recv(1024)

print('Received', repr(data))
```

Par rapport au serveur, le client est assez simple. Il crée un objet socket, se connecte au serveur et appelle `s.sendall()` pour envoyer son message. Enfin, il appelle `s.recv()` pour lire la réponse du serveur et l'imprimer.

### Lancement de l'Echo client et du serveur

Ouvrez un terminal ou une invite de commande, naviguez jusqu'au répertoire qui contient vos scripts et lancez le serveur :

```bash
$ ./echo-server.py
```

Votre terminal semblera suspendu. C'est parce que le serveur est bloqué (suspendu) lors de l'appel `accept()` — il attend une connexion client.

Ouvrez maintenant une autre fenêtre de terminal et lancez le client :

```bash
$ ./echo-client.py
Received b'Hello, world'
```

Dans la fenêtre du serveur, vous devriez voir :

```bash
$ ./echo-server.py
Connected by ('127.0.0.1', 64623)
```

Le serveur a affiché le tuple `addr` renvoyé par `s.accept()`. Il s'agit de l'adresse IP et du numéro de port TCP du client.

## Voir l'état des lieux

Pour connaître l'état actuel des sockets sur votre hôte, utilisez `netstat`. Il est disponible par défaut sur MacOS, Linux et Windows.

```bash
$ netstat -an
Active Internet connections (including servers)
Proto Recv-Q Send-Q  Local Address     Foreign Address   (state)
tcp4       0      0  127.0.0.1.65432   *.*               LISTEN
```

Si `echo-server.py` avait utilisé `HOST = ''` au lieu de `HOST = '127.0.0.1'`, netstat montrerait :

```bash
Proto Recv-Q Send-Q  Local Address     Foreign Address   (state)
tcp4       0      0  *.65432           *.*               LISTEN
```

L'adresse locale est `*.65432`, ce qui signifie que toutes les interfaces hôtes disponibles seront utilisées pour accepter les connexions entrantes.

Une autre façon de voir cela est d'utiliser `lsof` (liste des fichiers ouverts) :

```bash
$ lsof -i -n
COMMAND  PID   USER  FD  TYPE   DEVICE SIZE/OFF NODE NAME
Python  67982 nathan  3u  IPv4 0xecf272      0t0  TCP *:65432 (LISTEN)
```

Voici une erreur courante lorsqu'une tentative de connexion est faite sur un port sans prise d'écoute :

```python
$ ./echo-client.py
Traceback (most recent call last):
  File "./echo-client.py", line 9, in <module>
    s.connect((HOST, PORT))
ConnectionRefusedError: [Errno 61] Connection refused
```

Soit le numéro de port spécifié est erroné, soit le serveur ne fonctionne pas. Ou bien il y a un pare-feu sur le chemin qui bloque la connexion.

## Détail des communications

Examinons de plus près la façon dont le client et le serveur ont communiqué entre eux.

### Interface de bouclage (loopback)

<figure class="diagram">
<pre class="mermaid">
graph TB
    subgraph Hôte["Hôte (votre machine)"]
        subgraph Loopback["Interface de bouclage (127.0.0.1)"]
            S["Serveur<br/>port 65432"]
            C["Client<br/>port éphémère"]
            C -->|"données"| S
            S -->|"données"| C
        end
    end
    style Loopback fill:#1a1a2e,stroke:#16a34a,stroke-width:2px,color:#e2e8f0
    style Hôte fill:#0f0f23,stroke:#334155,stroke-width:1px,color:#e2e8f0
    style S fill:#16a34a,stroke:#16a34a,color:#fff
    style C fill:#2563eb,stroke:#2563eb,color:#fff
</pre>
<figcaption>Communication via l'interface de bouclage — les données ne quittent jamais l'hôte</figcaption>
</figure>

Lorsque l'on utilise l'interface de bouclage (adresse IPv4 `127.0.0.1` ou adresse IPv6 `::1`), les données ne quittent jamais l'hôte ou ne touchent pas le réseau externe.

L'interface de bouclage est contenue dans l'hôte. Cela représente la nature interne de l'interface de bouclage et le caractère local des connexions et des données qui transitent par l'hôte.

C'est pourquoi vous entendrez également l'interface de bouclage et l'adresse IP `127.0.0.1` ou `::1` appelée "localhost".

Les applications utilisent l'interface de bouclage pour communiquer avec d'autres processus s'exécutant sur l'hôte, et aussi pour améliorer la sécurité et l'isolation du réseau externe. Comme elle est interne et accessible uniquement depuis l'intérieur de l'hôte, elle n'est pas exposée.

### Interface réseau externe

<figure class="diagram">
<pre class="mermaid">
graph LR
    subgraph Host["Votre hôte"]
        S2["Serveur / Client<br/>eth0: 10.1.2.3"]
    end
    subgraph Network["Réseau externe"]
        R["Routeur /<br/>Passerelle"]
        Remote["Hôte distant<br/>10.1.2.50"]
    end
    S2 <-->|"TCP"| R
    R <-->|"TCP"| Remote
    style Host fill:#0f0f23,stroke:#334155,color:#e2e8f0
    style Network fill:#1a1a2e,stroke:#334155,color:#e2e8f0
    style S2 fill:#16a34a,stroke:#16a34a,color:#fff
    style R fill:#f59e0b,stroke:#f59e0b,color:#000
    style Remote fill:#2563eb,stroke:#2563eb,color:#fff
</pre>
<figcaption>Communication via une interface réseau connectée à un réseau externe</figcaption>
</figure>

Lorsque vous utilisez une adresse IP autre que `127.0.0.1` ou `::1` dans vos applications, elle est probablement liée à une interface Ethernet connectée à un réseau externe. C'est votre passerelle vers d'autres hôtes en dehors de votre "localhost".

> **Attention.** C'est un monde méchant et cruel. Assurez-vous de lire la section Utilisation des noms d'hôtes avant de vous aventurer au-delà des limites de sécurité de "localhost".

## Gestion de connexions multiples

Le serveur écho a certainement ses limites. La plus importante est qu'il ne dessert qu'un seul client et qu'il se termine ensuite. Le client écho a aussi cette limitation, mais il y a un problème supplémentaire.

Lorsque le client effectue l'appel suivant, il est possible que `s.recv()` ne renvoie qu'un octet, `b'H'` de `b'Hello, world'` :

```python
data = s.recv(1024)
```

L'argument `bufsize` de 1024 est la quantité **maximale** de données à recevoir en une fois. Cela ne signifie pas que `recv()` renverra 1024 octets.

`send()` se comporte également de cette manière. `send()` renvoie le nombre d'octets envoyés, qui peut être inférieur à la taille des données transmises. Il vous appartient de vérifier cela et d'appeler `send()` autant de fois que nécessaire pour envoyer toutes les données.

Nous avons évité d'avoir à le faire en utilisant `sendall()` :

> "Contrairement à send(), cette méthode continue à envoyer des données à partir d'octets jusqu'à ce que toutes les données aient été envoyées ou qu'une erreur se produise."

Nous avons deux problèmes à ce stade :

- Comment gérer **plusieurs connexions** en même temps ?
- Nous devons appeler `send()` et `recv()` jusqu'à ce que **toutes les données** soient envoyées ou reçues.

### Pourquoi select() ?

Il existe de nombreuses approches de la concurrence. Plus récemment, une approche populaire consiste à utiliser des E/S asynchrones. `asyncio` a été introduit dans la bibliothèque standard en Python 3.4. Le choix traditionnel est d'utiliser des threads.

Cependant, pour ce tutoriel, nous utiliserons quelque chose de plus traditionnel et plus facile à raisonner : `select()`.

`select()` vous permet de vérifier la finalisation des entrées/sorties sur plus d'un socket. Vous pouvez donc appeler `select()` pour voir quelles sockets ont des entrées/sorties prêtes à être lues et/ou écrites.

Nous allons utiliser le module `selectors` de la bibliothèque standard afin d'utiliser l'implémentation la plus efficace, quel que soit le système d'exploitation :

> "Ce module permet un multiplexage des entrées/sorties de haut niveau et efficace, basé sur les primitives du module sélectionné. Les utilisateurs sont encouragés à utiliser ce module à la place, à moins qu'ils ne souhaitent un contrôle précis des primitives au niveau du système d'exploitation utilisé."

## Client et serveur multi-connexion

### Serveur multi-connexion

Examinons d'abord le serveur multi-connexion, `multiconn-server.py`. Voici la première partie qui met en place la socket d'écoute :

```python
import selectors
sel = selectors.DefaultSelector()
# ...
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print('listening on', (host, port))
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)
```

La plus grande différence entre ce serveur et le serveur écho est l'appel à `lsock.setblocking(False)` pour configurer la socket en **mode non-bloquant**. Les appels effectués sur ce socket ne seront plus bloquants.

`sel.register()` enregistre la socket à surveiller avec `sel.select()` pour les événements qui vous intéressent. Pour la socket d'écoute, nous voulons des événements en lecture : `selectors.EVENT_READ`.

Ensuite, il y a la **boucle d'événements** :

```python
while True:
    events = sel.select(timeout=None)
    for key, mask in events:
        if key.data is None:
            accept_wrapper(key.fileobj)
        else:
            service_connection(key, mask)
```

`sel.select(timeout=None)` bloque jusqu'à ce que les sockets soient prêtes pour l'entrée/sortie. Il renvoie une liste de tuples `(key, events)`, un pour chaque socket.

Si `key.data` est égal à `None`, alors nous savons qu'il provient du socket d'écoute et nous devons `accept()` la connexion. Sinon, c'est un socket client déjà accepté, et nous devons le servir.

Voici la fonction `accept_wrapper()` :

```python
def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print('accepted connection from', addr)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)
```

Puisque le socket d'écoute a été enregistré pour `selectors.EVENT_READ`, il devrait être prêt à être lu. Nous appelons `sock.accept()` puis immédiatement `conn.setblocking(False)` pour mettre la socket en mode non-bloquant.

C'est l'objectif principal de cette version du serveur : nous ne voulons pas qu'il bloque. S'il bloque, alors le serveur entier est bloqué jusqu'à ce qu'il revienne.

Ensuite, nous créons un objet pour contenir les données avec `types.SimpleNamespace`. Comme nous voulons savoir quand la connexion client est prête à être lue *et* écrite, ces deux événements sont définis :

```python
events = selectors.EVENT_READ | selectors.EVENT_WRITE
```

Et la fonction `service_connection()` :

```python
def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            data.outb += recv_data
        else:
            print('closing connection to', data.addr)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print('echoing', repr(data.outb), 'to', data.addr)
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]
```

C'est le cœur du serveur multi-connexion. Si le socket est prêt à être lu, `sock.recv()` est appelé. Si aucune donnée n'est reçue, cela signifie que le client a fermé son socket, et le serveur fait de même. N'oubliez pas d'appeler `sel.unregister()` pour qu'il ne soit plus surveillé par `select()`.

### Client multi-connexion

Le client multi-connexion, `multiconn-client.py`, est très similaire au serveur. Au lieu d'écouter les connexions, il commence par les initier via `start_connections()` :

```python
messages = [b'Message 1 from client.', b'Message 2 from client.']

def start_connections(host, port, num_conns):
    server_addr = (host, port)
    for i in range(0, num_conns):
        connid = i + 1
        print('starting connection', connid, 'to', server_addr)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(server_addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        data = types.SimpleNamespace(connid=connid,
                                     msg_total=sum(len(m) for m in messages),
                                     recv_total=0,
                                     messages=list(messages),
                                     outb=b'')
        sel.register(sock, events, data=data)
```

`connect_ex()` est utilisé à la place de `connect()` car `connect()` lèverait immédiatement une exception `BlockingIOError`. `connect_ex()` renvoie initialement un indicateur d'erreur, `errno.EINPROGRESS`, au lieu de lever une exception pendant que la connexion est en cours.

Le client `service_connection()` :

```python
def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            print('received', repr(recv_data), 'from connection', data.connid)
            data.recv_total += len(recv_data)
        if not recv_data or data.recv_total == data.msg_total:
            print('closing connection', data.connid)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if not data.outb and data.messages:
            data.outb = data.messages.pop(0)
        if data.outb:
            print('sending', repr(data.outb), 'to connection', data.connid)
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]
```

La différence importante : le client garde une trace du nombre d'octets reçus du serveur afin de pouvoir fermer son côté de la connexion.

### Exécution du client et du serveur multi-connexion

Pour le serveur :

```bash
$ ./multiconn-server.py 127.0.0.1 65432
listening on ('127.0.0.1', 65432)
accepted connection from ('127.0.0.1', 61354)
accepted connection from ('127.0.0.1', 61355)
echoing b'Message 1 from client.Message 2 from client.' to ('127.0.0.1', 61354)
echoing b'Message 1 from client.Message 2 from client.' to ('127.0.0.1', 61355)
closing connection to ('127.0.0.1', 61354)
closing connection to ('127.0.0.1', 61355)
```

Pour le client avec 2 connexions :

```bash
$ ./multiconn-client.py 127.0.0.1 65432 2
starting connection 1 to ('127.0.0.1', 65432)
starting connection 2 to ('127.0.0.1', 65432)
sending b'Message 1 from client.' to connection 1
sending b'Message 2 from client.' to connection 1
received b'Message 1 from client.Message 2 from client.' from connection 1
closing connection 1
received b'Message 1 from client.Message 2 from client.' from connection 2
closing connection 2
```

## Client et serveur d'application

L'exemple du client et du serveur multi-connexion est une amélioration par rapport au serveur écho, mais il faut aller plus loin et corriger les défauts dans une implémentation finale.

Nous voulons un client et un serveur qui :

- **Traite les erreurs** de manière appropriée
- **Ne s'effondre pas** si une exception n'est pas prise en compte
- **Gère les limites de message** correctement

### Le problème des limites de message

Comme l'indique le type de socket `socket.SOCK_STREAM`, lorsque vous utilisez TCP, vous lisez un **flux continu d'octets**. C'est comme lire un fichier sur un disque, mais vous lisez des octets sur le réseau.

Contrairement à un fichier, vous ne pouvez pas repositionner le pointeur. Lorsque les octets arrivent, il y a des tampons réseau impliqués. Une fois lus, ils doivent être sauvegardés quelque part. Vous devez appeler `recv()` et sauvegarder les données dans une mémoire tampon jusqu'à ce que vous ayez un message complet.

**C'est à vous de définir les limites du message et d'en assurer le suivi.** La socket TCP ne sait rien de la signification des octets bruts.

Cela nous amène à définir un **protocole de couche application**.

### Approche par en-tête préfixé

L'un des moyens consiste à toujours envoyer des messages de longueur fixe. Mais c'est inefficace pour les petits messages.

Dans ce tutoriel, nous adopterons une approche générique utilisée par de nombreux protocoles, y compris HTTP : **nous préfixerons les messages avec un en-tête** qui comprendra la longueur du contenu ainsi que tous les autres champs dont nous aurons besoin.

### Structure du message

<figure class="diagram">
<pre class="mermaid">
block-beta
    columns 3
    A["En-tête fixe<br/>2 octets<br/>(longueur de l'en-tête JSON)"]:1
    B["En-tête JSON<br/>longueur variable<br/>(content-length, type, encoding)"]:1
    C["Contenu (payload)<br/>longueur variable<br/>(texte ou binaire)"]:1
    style A fill:#16a34a,stroke:#16a34a,color:#fff
    style B fill:#2563eb,stroke:#2563eb,color:#fff
    style C fill:#f59e0b,stroke:#f59e0b,color:#000
</pre>
<figcaption>Structure d'un message : en-tête fixe → en-tête JSON → contenu</figcaption>
</figure>

Un message commence par un **en-tête de longueur fixe de 2 octets** qui est un entier dans l'ordre des octets du réseau (big-endian). C'est la longueur de l'en-tête JSON suivant.

Une fois que nous avons lu 2 octets avec `recv()`, nous pouvons traiter ces 2 octets comme un nombre entier et ensuite lire ce nombre d'octets pour décoder l'en-tête JSON UTF-8.

L'en-tête JSON contient un dictionnaire d'en-têtes supplémentaires. L'un d'entre eux est le `content-length`, qui est le nombre d'octets du contenu du message. Une fois que nous avons lu ces octets, nous avons un message entier.

### En-tête du protocole d'application

L'en-tête de protocole contient :

- Du texte de longueur variable
- De l'Unicode avec encodage UTF-8
- Un dictionnaire Python sérialisé en utilisant JSON

Les en-têtes requis dans le dictionnaire sont :

| Nom | Description |
|-----|-------------|
| `byteorder` | L'ordre des octets de la machine (utilise `sys.byteorder`) |
| `content-length` | La longueur du contenu en octets |
| `content-type` | Le type de contenu, par exemple `text/json` ou `binary/my-binary-type` |
| `content-encoding` | L'encodage utilisé par le contenu, par exemple `utf-8` ou `binary` |

Ces en-têtes informent le destinataire du contenu de la charge utile du message. Cela vous permet d'envoyer des données arbitraires tout en fournissant suffisamment d'informations pour que le contenu puisse être décodé et interprété correctement.

### Considérations sur l'endianness

Si vous recevez des données et souhaitez les utiliser comme un entier multi-octets, vous devrez tenir compte de l'**endianness** — l'ordre dans lequel les octets sont stockés en mémoire par le processeur.

Nous éviterons ce problème en utilisant l'Unicode pour l'en-tête de notre message et le codage UTF-8. Comme l'UTF-8 utilise un codage de 8 bits, il n'y a pas de problème d'ordre d'octet.

```python
$ python3 -c 'import sys; print(repr(sys.byteorder))'
'little'
```

## Classe applicative du message (Message Class)

Examinons la classe `Message` et voyons comment elle est utilisée avec `select()`.

Pour cet exemple, j'ai créé un protocole d'application qui met en œuvre une fonction de **recherche simple**. Le client envoie une demande de recherche et le serveur recherche une correspondance. Si la requête n'est pas reconnue comme une recherche, le serveur suppose qu'il s'agit d'une requête binaire et renvoie une réponse binaire.

### Architecture des fichiers

<figure class="diagram">
<pre class="mermaid">
graph TB
    subgraph Serveur
        AS["app-server.py<br/>(script principal)"]
        LS["libserver.py<br/>(classe Message)"]
        AS --> LS
    end
    subgraph Client
        AC["app-client.py<br/>(script principal)"]
        LC["libclient.py<br/>(classe Message)"]
        AC --> LC
    end
    Client <-->|"TCP socket"| Serveur
    style AS fill:#16a34a,stroke:#16a34a,color:#fff
    style LS fill:#16a34a,stroke:#16a34a,color:#fff,stroke-dasharray: 5 5
    style AC fill:#2563eb,stroke:#2563eb,color:#fff
    style LC fill:#2563eb,stroke:#2563eb,color:#fff,stroke-dasharray: 5 5
</pre>
<figcaption>Architecture des fichiers de l'application client-serveur</figcaption>
</figure>

| Application | Fichier | Contenu |
|-------------|---------|---------|
| Serveur | `app-server.py` | Script principal du serveur |
| Serveur | `libserver.py` | Classe Message du serveur |
| Client | `app-client.py` | Script principal du client |
| Client | `libclient.py` | Classe Message du client |

### Séquence de communication

| Étape | Endpoint | Action |
|-------|----------|--------|
| 1 | Client | Envoie un Message contenant la requête |
| 2 | Serveur | Reçoit et traite le Message de requête du client |
| 3 | Serveur | Envoie un Message contenant la réponse |
| 4 | Client | Reçoit et traite le Message de réponse du serveur |

### Point d'entrée du message (process_events)

La méthode `process_events()` est le point d'entrée :

```python
def process_events(self, mask):
    if mask & selectors.EVENT_READ:
        self.read()
    if mask & selectors.EVENT_WRITE:
        self.write()
```

### La méthode read()

Voici la version du serveur (le client utilise `process_response()` au lieu de `process_request()`) :

```python
def read(self):
    self._read()

    if self._jsonheader_len is None:
        self.process_protoheader()

    if self._jsonheader_len is not None:
        if self.jsonheader is None:
            self.process_jsonheader()

    if self.jsonheader:
        if self.request is None:
            self.process_request()
```

La méthode `_read()` est appelée en premier. Elle appelle `socket.recv()` pour lire les données et les stocker dans un tampon de réception.

N'oubliez pas que `socket.recv()` peut ne pas retourner toutes les données d'un message complet. C'est pourquoi il y a des contrôles d'état pour chaque partie du message.

Les trois étapes de traitement :

| Composant du message | Méthode | Sortie |
|---------------------|---------|--------|
| En-tête de longueur fixe | `process_protoheader()` | `self._jsonheader_len` |
| En-tête JSON | `process_jsonheader()` | `self.jsonheader` |
| Contenu | `process_request()` | `self.request` |

### La méthode write()

Version du serveur :

```python
def write(self):
    if self.request:
        if not self.response_created:
            self.create_response()

    self._write()
```

`write()` vérifie si une requête existe et si une réponse n'a pas encore été créée. `create_response()` définit la variable d'état `response_created` et écrit la réponse dans le tampon d'envoi.

Version du client :

```python
def write(self):
    if not self._request_queued:
        self.queue_request()

    self._write()

    if self._request_queued:
        if not self._send_buffer:
            # Set selector to listen for read events, we're done writing.
            self._set_selector_events_mask('r')
```

### Traitement de l'en-tête fixe (protoheader)

```python
def process_protoheader(self):
    hdrlen = 2
    if len(self._recv_buffer) >= hdrlen:
        self._jsonheader_len = struct.unpack('>H',
                                self._recv_buffer[:hdrlen])[0]
        self._recv_buffer = self._recv_buffer[hdrlen:]
```

L'en-tête de longueur fixe est un entier de 2 octets dans l'ordre des octets du réseau (big-endian) qui contient la longueur de l'en-tête JSON. `struct.unpack()` est utilisé pour lire la valeur.

### Traitement de l'en-tête JSON

```python
def process_jsonheader(self):
    hdrlen = self._jsonheader_len
    if len(self._recv_buffer) >= hdrlen:
        self.jsonheader = self._json_decode(self._recv_buffer[:hdrlen], 'utf-8')
        self._recv_buffer = self._recv_buffer[hdrlen:]
        for reqhdr in ('byteorder', 'content-length', 'content-type',
                        'content-encoding'):
            if reqhdr not in self.jsonheader:
                raise ValueError(f'Missing required header "{reqhdr}".')
```

### Traitement de la requête

```python
def process_request(self):
    content_len = self.jsonheader['content-length']
    if not len(self._recv_buffer) >= content_len:
        return
    data = self._recv_buffer[:content_len]
    self._recv_buffer = self._recv_buffer[content_len:]
    if self.jsonheader['content-type'] == 'text/json':
        encoding = self.jsonheader['content-encoding']
        self.request = self._json_decode(data, encoding)
        print('received request', repr(self.request), 'from', self.addr)
    else:
        # Binary or unknown content-type
        self.request = data
        print(f'received {self.jsonheader["content-type"]} request from',
              self.addr)
    # Set selector to listen for write events, we're done reading.
    self._set_selector_events_mask('w')
```

### Création de la réponse

```python
def create_response(self):
    if self.jsonheader['content-type'] == 'text/json':
        response = self._create_response_json_content()
    else:
        # Binary or unknown content-type
        response = self._create_response_binary_content()
    message = self._create_message(**response)
    self.response_created = True
    self._send_buffer += message
```

### Fermeture de la connexion dans _write()

```python
def _write(self):
    if self._send_buffer:
        print('sending', repr(self._send_buffer), 'to', self.addr)
        try:
            sent = self.sock.send(self._send_buffer)
        except BlockingIOError:
            # Resource temporarily unavailable (errno EWOULDBLOCK)
            pass
        else:
            self._send_buffer = self._send_buffer[sent:]
            # Close when the buffer is drained. The response has been sent.
            if sent and not self._send_buffer:
                self.close()
```

### Gestion des erreurs dans _read()

```python
def _read(self):
    try:
        data = self.sock.recv(4096)
    except BlockingIOError:
        # Resource temporarily unavailable (errno EWOULDBLOCK)
        pass
    else:
        if data:
            self._recv_buffer += data
        else:
            raise RuntimeError('Peer closed.')
```

Notez le `except BlockingIOError:` suivi de `pass`. C'est une erreur temporaire qui se produit lorsque la socket se bloque (en attente sur le réseau). `select()` finira par nous rappeler.

### Script principal du serveur (app-server.py)

```python
$ ./app-server.py 127.0.0.1 65432
listening on ('127.0.0.1', 65432)
```

La boucle d'événements détecte toute erreur afin que le serveur puisse rester en marche :

```python
while True:
    events = sel.select(timeout=None)
    for key, mask in events:
        if key.data is None:
            accept_wrapper(key.fileobj)
        else:
            message = key.data
            try:
                message.process_events(mask)
            except Exception:
                print('main: error: exception for',
                      f'{message.addr}:\n{traceback.format_exc()}')
                message.close()
```

L'option `socket.SO_REUSEADDR` évite l'erreur "Address already in use" au redémarrage :

```python
lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
```

### Exécution de l'application

Recherche de texte :

```bash
$ ./app-client.py 10.0.1.1 65432 search morpheus
starting connection to ('10.0.1.1', 65432)
sending b'\x00d{"byteorder": "big", "content-type": "text/json", ...}
         {"action": "search", "value": "morpheus"}' to ('10.0.1.1', 65432)
received response {'result': 'Follow the white rabbit. 🐰'} from ('10.0.1.1', 65432)
got result: Follow the white rabbit. 🐰
closing connection to ('10.0.1.1', 65432)
```

Requête binaire :

```bash
$ ./app-client.py 10.0.1.1 65432 binary 😃
starting connection to ('10.0.1.1', 65432)
received binary/custom-server-binary-type response from ('10.0.1.1', 65432)
got response: b'First 10 bytes of request: binary\xf0\x9f\x98\x83'
closing connection to ('10.0.1.1', 65432)
```

## Troubleshooting

### ping

`ping` vérifiera si un hôte est vivant et connecté au réseau en envoyant une demande d'écho ICMP :

```bash
$ ping -c 3 127.0.0.1
PING 127.0.0.1 (127.0.0.1): 56 data bytes
64 bytes from 127.0.0.1: icmp_seq=0 ttl=64 time=0.058 ms
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.165 ms
64 bytes from 127.0.0.1: icmp_seq=2 ttl=64 time=0.164 ms
--- 127.0.0.1 ping statistics ---
3 packets transmitted, 3 packets received, 0.0% packet loss
```

### netstat

Les colonnes `Recv-Q` et `Send-Q` vous indiqueront le nombre d'octets conservés dans les tampons du réseau en file d'attente pour l'émission ou la réception.

```bash
$ netstat -an | grep 65432
Proto Recv-Q Send-Q  Local Address        Foreign Address     (state)
tcp4  408300      0  127.0.0.1.65432      127.0.0.1.53225     ESTABLISHED
tcp4       0 269868  127.0.0.1.53225      127.0.0.1.65432     ESTABLISHED
```

### Wireshark

Wireshark est un analyseur de protocole réseau. Voici un exemple avec `tshark` :

```bash
$ tshark -i lo0 'tcp port 65432'
Capturing on 'Loopback'
 1  0.000000  127.0.0.1 → 127.0.0.1  TCP  68  53942 → 65432 [SYN]
 2  0.000057  127.0.0.1 → 127.0.0.1  TCP  68  65432 → 53942 [SYN, ACK]
 3  0.000068  127.0.0.1 → 127.0.0.1  TCP  56  53942 → 65432 [ACK]
 5  0.000216  127.0.0.1 → 127.0.0.1  TCP  202 53942 → 65432 [PSH, ACK]
 7  0.000627  127.0.0.1 → 127.0.0.1  TCP  204 65432 → 53942 [PSH, ACK]
 9  0.000668  127.0.0.1 → 127.0.0.1  TCP  56  65432 → 53942 [FIN, ACK]
12  0.000848  127.0.0.1 → 127.0.0.1  TCP  56  53942 → 65432 [FIN, ACK]
```

Les messages ICMP importants :

| ICMP Type | ICMP Code | Description |
|-----------|-----------|-------------|
| 8 | 0 | Echo request |
| 0 | 0 | Echo reply |
| 3 | 0 | Destination network unreachable |
| 3 | 1 | Destination host unreachable |
| 3 | 3 | Destination port unreachable |
| 11 | 0 | TTL expired in transit |

## Référence

### Erreurs courantes

| Exception | errno | Description |
|-----------|-------|-------------|
| `BlockingIOError` | `EWOULDBLOCK` | Ressource temporairement indisponible. En mode non-bloquant, quand `send()` est appelé et le pair est occupé. |
| `OSError` | `EADDRINUSE` | Adresse déjà utilisée. Utilisez l'option `socket.SO_REUSEADDR`. |
| `ConnectionResetError` | `ECONNRESET` | Connexion réinitialisée par le pair. Le processus distant a crashé ou n'a pas fermé sa socket proprement. |
| `TimeoutError` | `ETIMEDOUT` | Opération expirée. Pas de réponse du pair. |
| `ConnectionRefusedError` | `ECONNREFUSED` | Connexion refusée. Aucune application n'écoute sur le port spécifié. |

### Familles d'adresses de socket

| Famille d'adresses | Protocole | Tuple d'adresse | Description |
|--------------------|-----------|-----------------|-------------|
| `socket.AF_INET` | IPv4 | `(host, port)` | `host` est un nom d'hôte ou une adresse IPv4. `port` est un entier. |
| `socket.AF_INET6` | IPv6 | `(host, port, flowinfo, scopeid)` | `host` est un nom d'hôte ou une adresse IPv6. |

### Utilisation des noms d'hôtes

> "Si vous utilisez un nom d'hôte dans la partie hôte de l'adresse de socket IPv4/v6, le programme peut présenter un comportement non déterministe, car Python utilise la première adresse renvoyée par la résolution DNS."

| Application | Usage | Recommandation |
|-------------|-------|----------------|
| Serveur | loopback | Utiliser une adresse IP, par exemple `127.0.0.1` ou `::1` |
| Serveur | ethernet | Utiliser une adresse IP, par exemple `10.1.2.3`. Chaîne vide pour toutes les interfaces. |
| Client | loopback | Utiliser une adresse IP, par exemple `127.0.0.1` ou `::1` |
| Client | ethernet | Utiliser une adresse IP pour la cohérence. Pour le cas typique, un nom d'hôte. |

### Appels bloquants

Une fonction de socket qui suspend temporairement votre application est un **appel bloquant**. Par exemple, `accept()`, `connect()`, `send()` et `recv()` "bloquent". Ils ne reviennent pas immédiatement.

Les appels bloquants peuvent être mis en mode non-bloquant avec `setblocking(False)` afin qu'ils reviennent immédiatement. Si c'est le cas, il se peut que les données ne soient pas prêtes — l'état actuel est `errno.EWOULDBLOCK`.

### Fermeture des connexions

Avec le protocole TCP, il est légal pour le client ou le serveur de fermer son côté de la connexion alors que l'autre côté reste ouvert. C'est une connexion "semi-ouverte".

Lors de la conception de votre application, déterminez comment les connexions seront fermées. Assurez-vous que les sockets sont toujours fermées en temps voulu.

### Ordre des octets (endianness)

L'ordre des octets utilisé dans le TCP/IP est **big-endian** et est appelé **ordre de réseau**.

Fonctions de conversion :

| Fonction | Description |
|----------|-------------|
| `socket.ntohl(x)` | Convertir 32 bits de l'ordre réseau à l'ordre hôte |
| `socket.ntohs(x)` | Convertir 16 bits de l'ordre réseau à l'ordre hôte |
| `socket.htonl(x)` | Convertir 32 bits de l'ordre hôte à l'ordre réseau |
| `socket.htons(x)` | Convertir 16 bits de l'ordre hôte à l'ordre réseau |

Avec le module `struct` :

```python
import struct
network_byteorder_int = struct.pack('>H', 256)
python_int = struct.unpack('>H', network_byteorder_int)[0]
```

### Sécurité réseau

Si votre application accède au réseau, elle doit être sécurisée et maintenue :

- Les mises à jour et correctifs de sécurité sont appliqués régulièrement, y compris Python et les bibliothèques tierces.
- Si possible, utilisez un pare-feu pour limiter les connexions aux seuls systèmes de confiance.
- Veillez à ce que les données soient aseptisées et validées avant traitement.
- Pour les connexions sécurisées, utilisez TLS (voir le module `ssl` de Python).

## Conclusion

Nous avons couvert beaucoup de terrain dans ce tutoriel. Nous avons examiné l'API socket de bas niveau du module socket de Python et avons vu comment elle peut être utilisée pour créer des applications client-serveur. Nous avons également créé notre propre classe personnalisée et l'avons utilisée comme un protocole de couche application pour échanger des messages et des données entre les terminaux.

Vous pouvez utiliser cette classe et vous en inspirer pour apprendre et aider à créer vos propres applications socket plus facilement et plus rapidement.

Félicitations pour être allé jusqu'au bout ! Vous êtes maintenant en bonne voie pour utiliser les sockets dans vos propres applications.

<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
<script>mermaid.initialize({startOnLoad: true, theme: 'dark'});</script>
