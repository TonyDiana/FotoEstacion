#!/bin/sh
HOME=/home/pi/zeus

# --- Asegurarnos que 'diagog' está disponible
sudo apt-get install dialog -y

# --- Aviso de desinstalación
clear
dialog --title "Estación fotográfica" --msgbox "
SI YA TIENE INSTALADA LA FOTOESTACIÓN, ESTE PROCESO BORRARÁ POR COMPLETO SU INSTALACIÓN ANTERIOR Y PERDERÁ TODOS SUS DATOS, NO UTILICE ESTE PROCESO PARA ACTUALIZAR LA FOTOESTACIÓN A LA ÚLTIMA VERSIÓN, ESTE PROCESO ES EXCLUSIVO PARA LA INSTALACIÓN INICIAL.

Si no desea ejecutarlo, símplemente cierre la ventana del terminal" 0 0

# --- Eliminar cualquier instalación anterior
clear
sudo rm -r $HOME
sudo rm /home/pi/.config/autostart/zeus_system.desktop
sudo rm /usr/share/applications/zeus.desktop
sudo rm /home/pi/Desktop/zeus.desktop

# --- Crear la carpeta
mkdir $HOME
cd $HOME

# --- Preparar el repositorio
git init
git config core.sparsecheckout true
echo img >> .git/info/sparse-checkout
git remote add -f origin https://github.com/TonyDiana/imagen.git
git config user.email zeus@tonydiana.es
git config user.name zeus
