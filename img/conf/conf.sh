#!/bin/sh
HOME=/home/pi/zeus/img/conf

# --- Declaración de funciones
ra_co() {
    clear
    sudo raspi-config
}




# --- Presentación del asistente
dialog --exit-label Seguir --title "Estación fotográfica" --textbox $HOME/msg/M01.txt 0 0




# --- Actualización del sistema y las dependencias
clear
sudo apt-get clean
sudo apt update -y 
sudo apt upgrade -y
sudo apt dist-upgrade -y
sudo apt-get autoremove -y

# --- Apagamos el bluetooth para ahorrar batería
sudo apt install rfkill -y
rfkill block 1

# --- Actualizar las dependencias Python
sudo apt-get install gir1.2-webkit2-4.0 -y
sudo pip3 install PyYAML



# --------------------------
#          Aspecto
# --------------------------

# --- Fuentes Ubuntu
sudo rm -r /usr/share/fonts/truetype/Ubuntu
sudo mv $HOME/Ubuntu /usr/share/fonts/truetype/

# --- Escritorio y barra del menú
sudo cp -pf $HOME/system/fondo.jpg /usr/share/rpd-wallpaper
sudo cp -pf $HOME/system/desktop-items-0.conf /etc/xdg/pcmanfm/LXDE-pi/
cp -pf $HOME/system/desktop-items-0.conf /home/pi/.config/pcmanfm/LXDE-pi

sudo cp -pf $HOME/system/desktop-items-1.conf /etc/xdg/pcmanfm/LXDE-pi/
cp -pf $HOME/system/desktop-items-1.conf /home/pi/.config/pcmanfm/LXDE-pi

sudo cp -f $HOME/system/config.txt /boot

sudo cp -pf $HOME/system/panel /home/pi/.config/lxpanel/LXDE-pi/panels
sudo cp -pf $HOME/system/desktop.conf /home/pi/.config/lxsession/LXDE-pi
sudo cp -pf $HOME/system/settings.ini /home/pi/.config/gtk-3.0

# --- Explorador de archivos y lanzador de ejecutables
sudo cp -pf $HOME/system/pcmanfm.conf /etc/xdg/pcmanfm/default
sudo cp -pf $HOME/system/pcmanfm.conf /etc/xdg/pcmanfm/LXDE
sudo cp -pf $HOME/system/pcmanfm.conf /etc/xdg/pcmanfm/LXDE-pi
cp -pf $HOME/system/pcmanfm.conf /home/pi/.config/pcmanfm/LXDE-pi
# --- Aun no funciona pese a cambiarlos todos




# --------------------------
#       raspi-config
# --------------------------

# --- Diferenciar usuarios avanzados
dialog --title "FotoEstación"  --yesno "¿Desea ejecutar el asistente 'raspi-config' paso a paso?" 0 0
asistente=$?

# --- Presentación
if [ $asistente -eq 0 ]
then
    # --- Actualizar y contraseña
    dialog --exit-label Seguir --title "Contraseña" --textbox $HOME/msg/M02-1.txt 0 0
    ra_co

    # --- Activar los protocolos
    dialog --exit-label Seguir --title "Comunicación" --textbox $HOME/msg/M02-2.txt 0 0
fi
# --- Esta última ocasión es tanto para usuarios avanzados como noveles
ra_co




# --------------------------
#          Batería
# --------------------------
dialog --title "Batería"  --yesno "¿Está instalada la batería recomendada?" 0 0
bateria=$?

if [ $bateria -eq 0 ]
then
    clear
    curl http://cdn.pisugar.com/release/Pisugar-power-manager.sh | sudo bash
fi




# --------------------------
#        Lanzadores
# --------------------------
mkdir /home/pi/.config/autostart
cp -pf $HOME/lanzadores/zeus_system.desktop /home/pi/.config/autostart
chmod +x /home/pi/.config/autostart/zeus_system.desktop

sudo cp -pf $HOME/lanzadores/zeus.desktop /usr/share/applications/
sudo chmod +x /usr/share/applications/zeus.desktop

ln -s /usr/share/applications/zeus.desktop /home/pi/Desktop




# --------------------------
#         Tema Dark
# --------------------------
dialog --exit-label Seguir --title "Cambio de tema" --textbox $HOME/msg/M10.txt 0 0
clear
lxappearance




# --------------------------
#          Despedirse
# --------------------------
dialog --exit-label Salir --title "Nube" --textbox $HOME/msg/M11.txt 0 0

dialog --exit-label Salir --title "Proceso finalizado" --textbox $HOME/msg/MEND.txt 0 0
