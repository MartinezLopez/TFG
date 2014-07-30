#!/usr/bin/python

from Osciloscopio import *
from Ventana import *
import os

def get_osc_id():
  usb = os.popen("lsusb | grep Tektronix") #Vemos los dispositivos conectados y elegimos el Tektronix
  id = usb.read()
  id = id[23:32] #Nos quedamos con el id del fabricante y del aparato
  id = id.replace(':', '::0x') #Ajustamos el formato al que necesitamos
  id = '0x' + id
  return id

def main():
  osc_id = get_osc_id()
  app = QtGui.QApplication(sys.argv)
  osc = Osciloscopio(osc_id)
  win_conf = VentanaConfiguracion(osc)
  #win_measure = VentanaMedida(osc)
  sys.exit(app.exec_())

if __name__ == '__main__':
  main()
