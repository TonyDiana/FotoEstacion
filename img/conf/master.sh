#!/bin/sh
curl https://raw.githubusercontent.com/TonyDiana/imagen/master/img/conf/install.sh | bash

# --- Actualizar el repertorio
INIT=/home/pi/zeus
cd $INIT
git pull origin master


# --- Lanzar el asistente
bash $INIT/img/conf/conf.sh


# --- Último lanzador y limpieza
mv -pf $INIT/img/conf/lanzadores/zeusMaster.sh $INIT/img/zeus.sh
chmod +x $INIT/img/zeus.sh

sudo rm -r $INIT/img/conf
sudo reboot
