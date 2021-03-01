#!/bin/sh
curl https://raw.githubusercontent.com/TonyDiana/imagen/beta/img/conf/install.sh | bash

# --- Actualizar el repertorio
INIT=/home/pi/zeus
cd $INIT
git pull origin beta


# --- Lanzar el asistente
bash $INIT/img/conf/conf.sh


# --- Último lanzador y limpieza
mv -f $INIT/img/conf/lanzadores/zeusBeta.sh $INIT/img/zeus.sh
chmod +x $INIT/img/zeus.sh

sudo rm -r $INIT/img/conf
sudo reboot
