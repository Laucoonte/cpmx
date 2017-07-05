#!/bin/bash
# -*- ENCODING: UTF-8 -*-
echo "Inicio: Actualizaciones del sistema"
sleep 1s
apt-get update #sudo
apt-get upgrade #sudo
echo "Hecho"
sleep 1s
#
echo "Instalacion de herramientas de desarrollo"
sleep 1s
apt-get install build-essential cmake pkg-config #sudo
echo "Hecho"
sleep 1s
#
echo "Interprete de imagenes"
sleep 1s
apt-get install libjpeg8-dev libtiff5-dev libjasper-dev libpng12-dev #sudo
echo "Hecho"
sleep 1s
#
echo "Bibliotecas de streaming de video y captura de frames"
sleep 1s
apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev #sudo
apt-get install libxvidcore-dev libx264-dev #sudo
echo "Hecho"
sleep 1s
#
echo "Operaciones GUI de OpenCV"
sleep 1s
apt-get install libgtk-3-dev #sudo
echo "Hecho"
sleep 1s
#
echo "Optimizacion de funciones"
sleep 1s
apt-get install libatlas-base-dev gfortran #sudo
echo "Hecho"
sleep 1s
#
echo "Instalacion de python 2.7"
sleep 1s
apt-get install python2.7-dev #sudo
echo "Hecho"
sleep 1s
#
# Parte de descarga de OpenCV y descompresion, ya hecho
#
echo "Instalacion de pip"
sleep 1s
cd ~
wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py #sudo
echo "Hecho"
sleep 1s
#
echo "Instalacion de numpy"
sleep 1s
pip install numpy #sudo
echo "Hecho"
sleep 1s
#
echo "Compilacion de OpenCV"
sleep 1s
cd ~/opencv-3.1.0/
mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE \ -D CMAKE_INSTALL_PREFIX=/usr/local \ -D INSTALL_PYTHON_EXAMPLES=ON \ -D INSTALL_C_EXAMPLES=OFF \ -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-3.1.0/modules \ -D PYTHON_EXECUTABLE=~/.virtualenvs/cv/bin/python \ -D BUILD_EXAMPLES=ON ..
echo "Hecho"
sleep 1s
# """
# echo "Instalacion de OpenCV"
# sleep 1s
# make
# make install #sudo
# ldconfig #sudo
# echo "Instalacion finalizada""""
# Fuente: http://www.pyimagesearch.com/2016/10/24/ubuntu-16-04-how-to-install-opencv/
exit
