# affiche-interactive

## A propos

Affichage de vidéos / images et sons en fonction des frappes du clavier.

Idée : Damien Muti

Code : Olivier Boesch

Projet sur le site TonerKebab du DSAA design graphique Marseille 

[www.tonerkebab.fr/wiki/doku.php/wiki:tutoriels:affiche-interactive:accueil](www.tonerkebab.fr/wiki/doku.php/wiki:tutoriels:affiche-interactive:accueil)

## Configuration par défaut
les fichiers media et de configuration sont dans le dossier [media](https://github.com/olivier-boesch/affiche-interactive/blob/master/src/media)  

l'association touche <-> media se fait dans le fichier [config.json](https://github.com/olivier-boesch/affiche-interactive/blob/master/src/media/config.json)

pour chaque touche définie, on peut donner les paramètres:
    media_type : type de medium (sound,video,image)
    src: chemin relatif au répertoire principal
    loop : valable pour les sons et les videos. doit-on le jouer en boucle ?

le configuration par défaut (pour les exemples) est :
* "e" son yeah.mp3 (loop on)
* "r": image hud.png
* "u": video text.mp4 (1280x720)
* "t": image lena_polcorrect.jpg (la légende...)
* "y": image Mona_Lisa.jpg
* "up" (flèche haut): son ohno.mp3
* "down" (flèche bas): ada.jpg (un autre légende)
* "left" (flèche gauche): video sample.mp4 (video + son) (loop on)
* "right" (flèche droite): video star_trails.mp4 (1280x720)

## Attention
* Pour les vidéos sur un raspberry pi3b/pi3b+, ne pas dépasser 1280x720 pour les mp4.

## fichiers supplémentaires

* un fichier d'installation de kivy pour le rpi3
* un fichier spec buildozer pour packager cette application pour android et ios (non testé sur ios). 