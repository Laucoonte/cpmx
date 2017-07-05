# StreamTection

A real-time object recognition application using [Google's TensorFlow Object Detection API](https://github.com/tensorflow/models/tree/master/object_detection) and [OpenCV](http://opencv.org/). Gstreamer and a Raspberry Pi

## Requirements
- OpenCV 3.0
- Python pip
- Python Numpy
- Gstreamer
- [TensorFlow 1.2](https://www.tensorflow.org/)
- OpenCV 3.0--> [How to install](http://www.pyimagesearch.com/2016/10/24/ubuntu-16-04-how-to-install-opencv/)

- To Start Gstreamer in Raspberry: raspivid -t 0 -h 360 -w 480 -fps 60 -hf -b 2000000 -o - | gst-launch-1.0 -v fdsrc ! h264parse !  rtph264pay config-interval=1 pt=96 ! gdppay ! tcpserversink host= $RASP_IP port=5000

- Start Gstreamer client in PC : gst-launch-1.0 -v tcpclientsrc host=$RASP_IP port=5000  ! gdpdepay !  rtph264depay ! avdec_h264 ! videoconvert ! autovideosink sync=false



## Instrucciones para Ubuntu
1. Clona este repositorio en tu carpeta de usuario.
2. Saca los archivos de "iBike" y déjalos en tu carpeta de usuario.
3. Ingresa a tu terminal >> Ctrl+Alt+T
4. Ingresa en la terminal lo siguiente:
	´chmod 700 script.sh´
	´sudo ./script.sh´
5. Espera a que el script se ejecute y mientras disfruta de la presentación
6. Espera a que el script finalice
7. Si ha finalizado, comprueba que dentro de la ventana de la terminal aparezca algo similar a lo mostrado en la imagen jpg incluida en la carpeta de "iBike" llamada "comprobacion"
8. Si aparece algo similar debes ahora ejecutar las siguientes líneas de comandos
	make
	sudo make install
	sudo ldconfig
9. Ingresa ahora en la linea de comandos:
	´cd cpmx´
	´python mDesktopDetect.py´



## Notes
- OpenCV 3.1 might crash on OSX after a while, so that's why I had to switch to version 3.0. See open issue and solution [here](https://github.com/opencv/opencv/issues/5874).
- Moving the `.read()` part of the video stream in a multiple child processes did not work. However, it was possible to move it to a separate thread.
