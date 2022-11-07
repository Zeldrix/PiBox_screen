# PiBox_screen
Affichage personnalisé sur l'écran de la PiBox
## Fonctionnement
Le script Python (stats.py) est lancé en tant que service (daemon) sur le PiBox.
Il utilise la librairie Python "adafruit_rgb_display" pour un affichage personnalisé sur l'écran.

Le script à une période de raffraichissement de 5 secondes.

  - Il récupère le status de chaque disque dans le RAID :
    - Le script diskStatus.sh récupére le status du disque entré en paramètre
    - Le script chechDisks.sh enregistre le status de chaque disque dans un fichier disk[numéroDisque].txt en appelant diskStatus.sh X fois
    - Le script stats.py vient lire les fichiers .txt pour changer la couleur de l'icone des disques en fonction du status
    
  - Il récupère des informations système afin de les afficher :
    - L'adresse IP
    - Le pourcentage d'utilisation et la température (°C) du CPU
    - Le pourcentage de stockage utilisé sur le RAID
    - Le pourcentage d'utilisation de la RAM
## Matériel utilisé
  - [PiBox](https://pibox.io/)
  - [Adafruit 1.3" 240x240 (inclus dans PiBox)](https://www.adafruit.com/product/4520)
## Sources (Documentation et Guides)
  - [PiBox Modifying the Display](https://docs.kubesail.com/guides/pibox/os/#download-pibox-framebuffer-binary)
  - [Adafruit Screen Guide](https://learn.adafruit.com/adafruit-mini-pitft-135x240-color-tft-add-on-for-raspberry-pi/python-setup)
## Résultat d'affichage
<img src="https://user-images.githubusercontent.com/52959021/199784653-ec577159-2610-45ac-9ff2-3201ed7d92c3.jpg" width=50% height=50%>
