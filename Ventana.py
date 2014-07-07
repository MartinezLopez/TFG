#!/usr/bin/python

import sys
from PyQt4 import QtGui, QtCore
from Osciloscopio import *
#from Display import *
from Modbus import *
import numpy as np
import time
import math
import pylab
from scipy.special import erfc
import logging

import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
import matplotlib.pyplot as plt
from matplotlib.ticker import EngFormatter, MultipleLocator
from matplotlib.widgets import Cursor, Slider
from matplotlib.patches import Rectangle

class VentanaPrincipal(QtGui.QWidget):
  global osc
  
  def __init__(self, osciloscopio):
    '''Constructor de la ventana principal de la aplicacion.
    
    Parametros:
      osciloscopio: Objeto de la clase Osciloscopio
    
    '''
    super(VentanaPrincipal, self).__init__()
    self.osc = osciloscopio
    grid = QtGui.QGridLayout()
    grid.setSpacing(5)
    
    bot_osciloscopio = QtGui.QPushButton('Osciloscopio', self)
    bot_med_pot = QtGui.QPushButton('Medidor de potencia optica', self) #Tilde
    bot_salir = QtGui.QPushButton('Salir', self)
    
    grid.addWidget(bot_osciloscopio, 1, 1)
    grid.addWidget(bot_med_pot, 1, 2)
    grid.addWidget(bot_salir, 2, 2)
    
    bot_salir.clicked.connect(QtCore.QCoreApplication.instance().quit)
    bot_osciloscopio.clicked.connect(lambda: self.init_ventana_osc())
    bot_med_pot.clicked.connect(lambda: self.init_ventana_pot())
    
    self.setLayout(grid)        
    self.setGeometry(100, 100, 500, 500)
    self.setWindowTitle('Laboratorio de Comunicaciones Opticas')
    self.setWindowIcon(QtGui.QIcon('/home/debian/Desktop/Aplicacion/img/icono.gif'))
    #self.showMaximized()
    self.show()
    
  def init_ventana_osc(self):
    '''Crea un objeto de la clase VentanaConfiguracion.
    
    '''
    v = VentanaConfiguracion(self.osc)
  
  def init_ventana_pot(self):
    '''Crea un objeto de la clase VentanaMedidorPotencia.
    
    '''
    print 'medidor de potencia'
    #v = VentanaMedidorPotencia()

class VentanaConfiguracion(QtGui.QWidget):
  global osc
    
  def __init__(self, osciloscopio):
    '''Constructor de la ventana de configuracion del osciloscopio.
    
    Parametros:
      osciloscopio: Objeto de la clase Osciloscopio
    
    '''
    #Inicializacion de la ventana y de la variable osciloscopio con el objeto osciloscopio pasado como parametro
    super(VentanaConfiguracion, self).__init__()
    self.osc = osciloscopio
    self.conf_osc()
  
  def conf_osc(self):
    '''Anade funcionalidades a la ventana de configuracion del osciloscopio.
    
    '''
    #Se crean los elementos de la ventana y se les anaden funcionalidades
    grid = QtGui.QGridLayout()
    grid.setSpacing(5)
    
    bot_aceptar = QtGui.QPushButton('Configurar', self)
    bot_medir = QtGui.QPushButton('Mostrar\nosciloscopio', self)
    bot_medidas = QtGui.QPushButton('Medidas', self)
    bot_ojo = QtGui.QPushButton('Ver', self)
    bot_cerrar = QtGui.QPushButton('Cerrar', self)
    
    tit_tiempo = QtGui.QLabel('Base de\ntiempos')
    tit_display = QtGui.QLabel('Modo del display')
    tit_vdiv1 = QtGui.QLabel('V/div')
    tit_acop1 = QtGui.QLabel('Coupling')
    tit_att1 = QtGui.QLabel('Atenuacion de\nla sonda')
    tit_vdiv2 = QtGui.QLabel('V/div')
    tit_acop2 = QtGui.QLabel('Coupling')
    tit_att2 = QtGui.QLabel('Atenuacion de\nla sonda')
    tit_ojo = QtGui.QLabel('Diagrama\nde ojo')
    tit_tbit = QtGui.QLabel('Tiempo de\nbit')
    
    ch1 = QtGui.QCheckBox('Ch 1', self)
    ch2 = QtGui.QCheckBox('Ch 2', self)
    
    desp_tiempo = QtGui.QComboBox(self)
    desp_tiempo.addItem("100ms")
    desp_tiempo.addItem("100ns")
    desp_tiempo.addItem("100us")
    desp_tiempo.addItem("10ms")
    desp_tiempo.addItem("10ns")
    desp_tiempo.addItem("10s")
    desp_tiempo.addItem("10us")
    desp_tiempo.addItem("1ms")
    desp_tiempo.addItem("1s")
    desp_tiempo.addItem("1us")
    desp_tiempo.addItem("2.5ms")
    desp_tiempo.addItem("2.5ns")
    desp_tiempo.addItem("2.5s")
    desp_tiempo.addItem("2.5us")
    desp_tiempo.addItem("250ms")
    desp_tiempo.addItem("250ns")
    desp_tiempo.addItem("250us")
    desp_tiempo.addItem("25ms")
    desp_tiempo.addItem("25ns")
    desp_tiempo.addItem("25s")
    desp_tiempo.addItem("25us")
    desp_tiempo.addItem("500ms")
    desp_tiempo.addItem("500ns")
    desp_tiempo.addItem("500us")
    desp_tiempo.addItem("50ms")
    desp_tiempo.addItem("50ns")
    desp_tiempo.addItem("50s")
    desp_tiempo.addItem("50us")
    desp_tiempo.addItem("5ms")
    desp_tiempo.addItem("5ns")
    desp_tiempo.addItem("5s")
    desp_tiempo.addItem("5us")
    
    desp_disp = QtGui.QComboBox(self)
    desp_disp.addItem("YT")
    desp_disp.addItem("XY")
    
    desp_vdiv1 = QtGui.QComboBox(self)
    desp_vdiv1.addItem("100mv")
    desp_vdiv1.addItem("10mv")
    desp_vdiv1.addItem("1v")
    desp_vdiv1.addItem("200mv")
    desp_vdiv1.addItem("20mv")
    desp_vdiv1.addItem("2mv")
    desp_vdiv1.addItem("2v")
    desp_vdiv1.addItem("500mv")
    desp_vdiv1.addItem("50mv")
    desp_vdiv1.addItem("5mv")
    desp_vdiv1.addItem("5v")
    
    desp_vdiv2 = QtGui.QComboBox(self)
    desp_vdiv2.addItem("100mv")
    desp_vdiv2.addItem("10mv")
    desp_vdiv2.addItem("1v")
    desp_vdiv2.addItem("200mv")
    desp_vdiv2.addItem("20mv")
    desp_vdiv2.addItem("2mv")
    desp_vdiv2.addItem("2v")
    desp_vdiv2.addItem("500mv")
    desp_vdiv2.addItem("50mv")
    desp_vdiv2.addItem("5mv")
    desp_vdiv2.addItem("5v")
    
    desp_acop1 = QtGui.QComboBox(self)
    desp_acop1.addItem("AC")
    desp_acop1.addItem("DC")
    desp_acop1.addItem("GND")
        
    desp_acop2 = QtGui.QComboBox(self)
    desp_acop2.addItem("AC")
    desp_acop2.addItem("DC")
    desp_acop2.addItem("GND")
        
    desp_att1 = QtGui.QComboBox(self)
    desp_att1.addItem("x1")
    desp_att1.addItem("x10")
    
    desp_att2 = QtGui.QComboBox(self)
    desp_att2.addItem("x1")
    desp_att2.addItem("x10")
    
    desp_ojo = QtGui.QComboBox(self)
    desp_ojo.addItem("200 ns")
    desp_ojo.addItem("50 ns")
    desp_ojo.addItem("14.3 ns")
    desp_ojo.addItem("6.67 ns")
    
    #grid.addWidget(widget, r, c, [num_r, num_c])
    grid.addWidget(ch1, 1, 0)
    grid.addWidget(tit_vdiv1, 1, 1)
    grid.addWidget(desp_vdiv1, 1, 2)
    grid.addWidget(tit_acop1, 1, 3)
    grid.addWidget(desp_acop1, 1, 4)
    grid.addWidget(tit_att1, 1, 5)
    grid.addWidget(desp_att1, 1, 6)
    
    grid.addWidget(ch2, 2, 0)
    grid.addWidget(tit_vdiv2, 2, 1)
    grid.addWidget(desp_vdiv2, 2, 2)
    grid.addWidget(tit_acop2, 2, 3)
    grid.addWidget(desp_acop2, 2, 4)
    grid.addWidget(tit_att2, 2, 5)
    grid.addWidget(desp_att2, 2, 6)
    
    grid.addWidget(tit_tiempo, 3, 1)
    grid.addWidget(desp_tiempo, 3, 2)
    grid.addWidget(tit_display, 3, 4)
    grid.addWidget(desp_disp, 3, 5)
    
    grid.addWidget(bot_aceptar, 4, 4)
    grid.addWidget(bot_medir, 4, 5)
    grid.addWidget(bot_medidas, 4, 6)
    
    grid.addWidget(tit_ojo, 6, 1)
    grid.addWidget(tit_tbit, 6, 3)
    grid.addWidget(desp_ojo, 6,4)
    grid.addWidget(bot_ojo, 6, 6)
    
    grid.addWidget(bot_cerrar, 8, 5)
    
    bot_cerrar.clicked.connect(self.close)
    bot_aceptar.clicked.connect(lambda: self.aceptar_conf(desp_tiempo.currentText(), desp_disp.currentText(), ch1.isChecked(), desp_vdiv1.currentText(), desp_acop1.currentText(), desp_att1.currentText(), ch2.isChecked(), desp_vdiv2.currentText(), desp_acop2.currentText(), desp_att2.currentText()))
    bot_medir.clicked.connect(lambda: self.medida(ch1.isChecked(), ch2.isChecked()))
    bot_medidas.clicked.connect(lambda: self.medidas())
    bot_ojo.clicked.connect(lambda: self.diagramaOjo(desp_ojo.currentText()))
    self.setLayout(grid)
        
    self.setGeometry(100, 100, 500, 500)
    self.setWindowTitle('Osciloscopio')
    self.setWindowIcon(QtGui.QIcon('/home/debian/Desktop/Aplicacion/img/icono.gif'))
    self.show()
  
  def aceptar_conf(self, t, display, ch1, vdiv1, acop1, att1, ch2, vdiv2, acop2, att2):
    '''Configura el osciloscopio con los valores que se han seleccionado en la ventana.
    
    Parametros:
      t: Base de tiempos del osciloscopio
      display: Modo del display (XY o YT).
      ch1: Muestra o no el canal uno.
      vdiv1: Escala vertical del canal uno.
      acop1: Acoplamiento del canal uno.
      att1: Atenuacion de la sonda del canal uno.
      ch2: Muestra o no el canal dos.
      vdiv2: Escala vertical del canal dos.
      acop2: Acoplamiento del canal dos.
      att2: Atenuacion de la sonda del canal dos.
    
    '''
    #Cuando se acepta, se envian las configuraciones al osciloscopio que se ha pasado como parametro
    self.osc.set_display(display)
    self.osc.set_horizontal(str(t))
    if(ch1):
      self.osc.disp_channel(True, '1')
      self.osc.set_vertical('1', str(vdiv1), str(acop1), str(att1).strip('x'))
    else:
      self.osc.disp_channel(False, '1')
    
    if(ch2):
      self.osc.disp_channel(True, '2')
      self.osc.set_vertical('2', str(vdiv2), str(acop2), str(att2).strip('x'))
    else:
      self.osc.disp_channel(False, '2')
  
  def medida(self, ch1, ch2):
    '''Crea un objeto de la clase Display en el que representa las senales que muestra el osciloscopio. Solo muestra los canales que esten seleccionados.
    Pide todos los puntos disponibles del osciloscopio. Oculta la pantalla de configuracion mientras muestra el osciloscopio.
    
    Parametros:
      ch1: Booleano. Muestra o no el canal uno.
      ch2: Booleano. Muestra o no el canal dos.
    
    '''
    #Si los canales estan seleccionados se cogen sus datos, si no se dejan a cero
    if(ch1):
      self.osc.disp_channel(True, '1')
      medida1, tiempo1 = self.osc.get_data('1', 1, 2500, '1')
    else:
      medida1 = []
      tiempo1 = []
    if(ch2):
      self.osc.disp_channel(True, '2')
      medida2, tiempo2 = self.osc.get_data('2', 1, 2500, '1')
    else:
      medida2 = []
      tiempo2 = []
    
    self.disp = Display(medida1, tiempo1, medida2, tiempo2)
    self.disp.show()
  
  def diagramaOjo(self, t_bit):
    '''Crea on objeto de la clase Display en el que representa el diagrama de ojo del canal 1.
    
    '''
    tiempos_bit = {"200 ns":0x00, "50 ns":0x01, "14.3 ns":0x02, "6.67 ns":0x03}
    base_tiempos = {"200 ns":'50ns', "50 ns":'10ns', "14.3 ns":'5ns', "6.67 ns":'2.5ns'}
    
    # Configuramos base de tiempos y amplitud
    self.osc.set_horizontal(base_tiempos[str(t_bit)]) #Por los qstring de qt4
    self.osc.set_vertical("1", "500mv", "DC", "1")
    
    # Llamada a modbus
    #mb = Modbus()
    #mb.write_registers(0x02, 1, [tiempos_bit[t_bit]]) #direccion, primer registro, datos
    
    # Configuramos el disparo
    self.osc.set_trigger('ext', 0)
    aviso = VentanaInfo('La adquisicion de datos puede tardar un tiempo.\nPulse el boton "Ok" y espere, por favor.')
    lista_medidas = []
    
    # Toma 32 trazas del osciloscopio
    for i in range(32):
      medidas , inc_tiempo = self.osc.get_data('1', 500, 2000, '1')
      lista_medidas.append(medidas)
    
    self.ojo = DisplayOjo(lista_medidas, inc_tiempo)
    self.ojo.show()
    
    # Quitamos el disiparo externo
    self.osc.set_trigger('1', 0)
  
  def medidas(self):
    '''Crea un objeto de la clase VentanaMedidas.
    
    '''
    #Llamar a una ventana nueva
    v = VentanaMedidas(self.osc)

class VentanaMedidas(QtGui.QWidget):
  global osc
  
  def __init__(self, osciloscopio):
    '''Constructor de la ventana que muestra las medidas del osciloscopio.
    
    Parametros:
      osciloscopio: Objeto de la clase Osciloscopio
    
    '''
    super(VentanaMedidas, self).__init__()
    self.osc = osciloscopio
    self.inicializa()
  
  def inicializa(self):
    '''Anade funcionalidades a la ventana de medidas.
    
    '''
    grid = QtGui.QGridLayout()
    grid.setSpacing(10)
    
    bot_cerrar = QtGui.QPushButton('Cerrar', self)
    ch1_label = QtGui.QLabel('Canal 1')
    ch2_label = QtGui.QLabel('Canal 2')
    
    freq_label = QtGui.QLabel('Frecuencia')
    per_label = QtGui.QLabel('Periodo')
    vmedio_label = QtGui.QLabel('Valor medio')
    vpp_label = QtGui.QLabel('Vpp')
    vrms_label = QtGui.QLabel('Vrms')
    vmin_label = QtGui.QLabel('Minimo') #Falta la tilde
    vmax_label = QtGui.QLabel('Maximo') #Falta la tilde
    tsubida_label = QtGui.QLabel('Tiempo de subida')
    tbajada_label = QtGui.QLabel('Tiempo de bajada')
    
    self.ch1_freq_label = QtGui.QLabel(self)
    self.ch1_per_label = QtGui.QLabel(self)
    self.ch1_vmedio_label = QtGui.QLabel(self)
    self.ch1_vpp_label = QtGui.QLabel(self)
    self.ch1_vrms_label = QtGui.QLabel(self)
    self.ch1_vmin_label = QtGui.QLabel(self)
    self.ch1_vmax_label = QtGui.QLabel(self)
    self.ch1_tsubida_label = QtGui.QLabel(self)
    self.ch1_tbajada_label = QtGui.QLabel(self)
    
    ch1_freq_button = QtGui.QPushButton('Medir', self)
    ch1_per_button = QtGui.QPushButton('Medir', self)
    ch1_vmedio_button = QtGui.QPushButton('Medir', self)
    ch1_vpp_button = QtGui.QPushButton('Medir', self)
    ch1_vrms_button = QtGui.QPushButton('Medir', self)
    ch1_vmin_button = QtGui.QPushButton('Medir', self)
    ch1_vmax_button = QtGui.QPushButton('Medir', self)
    ch1_tsubida_button = QtGui.QPushButton('Medir', self)
    ch1_tbajada_button = QtGui.QPushButton('Medir', self)
    
    self.ch2_freq_label = QtGui.QLabel(self)
    self.ch2_per_label = QtGui.QLabel(self)
    self.ch2_vmedio_label = QtGui.QLabel(self)
    self.ch2_vpp_label = QtGui.QLabel(self)
    self.ch2_vrms_label = QtGui.QLabel(self)
    self.ch2_vmin_label = QtGui.QLabel(self)
    self.ch2_vmax_label = QtGui.QLabel(self)
    self.ch2_tsubida_label = QtGui.QLabel(self)
    self.ch2_tbajada_label = QtGui.QLabel(self)
    
    ch2_freq_button = QtGui.QPushButton('Medir', self)
    ch2_per_button = QtGui.QPushButton('Medir', self)
    ch2_vmedio_button = QtGui.QPushButton('Medir', self)
    ch2_vpp_button = QtGui.QPushButton('Medir', self)
    ch2_vrms_button = QtGui.QPushButton('Medir', self)
    ch2_vmin_button = QtGui.QPushButton('Medir', self)
    ch2_vmax_button = QtGui.QPushButton('Medir', self)
    ch2_tsubida_button = QtGui.QPushButton('Medir', self)
    ch2_tbajada_button = QtGui.QPushButton('Medir', self)
    
    grid.addWidget(ch1_label, 1, 2)
    grid.addWidget(ch2_label, 1, 4)
    
    grid.addWidget(freq_label, 2, 1)
    grid.addWidget(self.ch1_freq_label, 2, 2)
    grid.addWidget(ch1_freq_button, 2, 3)
    grid.addWidget(self.ch2_freq_label, 2, 4)
    grid.addWidget(ch2_freq_button, 2, 5)
    
    grid.addWidget(per_label, 3, 1)
    grid.addWidget(self.ch1_per_label, 3, 2)
    grid.addWidget(ch1_per_button, 3, 3)
    grid.addWidget(self.ch2_per_label, 3, 4)
    grid.addWidget(ch2_per_button, 3, 5)
    
    grid.addWidget(vmedio_label, 4, 1)
    grid.addWidget(self.ch1_vmedio_label, 4, 2)
    grid.addWidget(ch1_vmedio_button, 4, 3)
    grid.addWidget(self.ch2_vmedio_label, 4, 4)
    grid.addWidget(ch2_vmedio_button, 4, 5)
    
    grid.addWidget(vpp_label, 5, 1)
    grid.addWidget(self.ch1_vpp_label, 5, 2)
    grid.addWidget(ch1_vpp_button, 5, 3)
    grid.addWidget(self.ch2_vpp_label, 5, 4)
    grid.addWidget(ch2_vpp_button, 5, 5)
    
    grid.addWidget(vrms_label, 6, 1)
    grid.addWidget(self.ch1_vrms_label, 6, 2)
    grid.addWidget(ch1_vrms_button, 6, 3)
    grid.addWidget(self.ch2_vrms_label, 6, 4)
    grid.addWidget(ch2_vrms_button, 6, 5)
    
    grid.addWidget(vmin_label, 7, 1)
    grid.addWidget(self.ch1_vmin_label, 7, 2)
    grid.addWidget(ch1_vmin_button, 7, 3)
    grid.addWidget(self.ch2_vmin_label, 7, 4)
    grid.addWidget(ch2_vmin_button, 7, 5)
    
    grid.addWidget(vmax_label, 8, 1)
    grid.addWidget(self.ch1_vmax_label, 8, 2)
    grid.addWidget(ch1_vmax_button, 8, 3)
    grid.addWidget(self.ch2_vmax_label, 8, 4)
    grid.addWidget(ch2_vmax_button, 8, 5)
    
    grid.addWidget(tsubida_label, 9, 1)
    grid.addWidget(self.ch1_tsubida_label, 9, 2)
    grid.addWidget(ch1_tsubida_button, 9, 3)
    grid.addWidget(self.ch2_tsubida_label, 9, 4)
    grid.addWidget(ch2_tsubida_button, 9, 5)
    
    grid.addWidget(tbajada_label, 10, 1)
    grid.addWidget(self.ch1_tbajada_label, 10, 2)
    grid.addWidget(ch1_tbajada_button, 10, 3)
    grid.addWidget(self.ch2_tbajada_label, 10, 4)
    grid.addWidget(ch2_tbajada_button, 10, 5)
    
    grid.addWidget(bot_cerrar, 11, 4)
    
    bot_cerrar.clicked.connect(self.close)
    
    ch1_freq_button.clicked.connect(lambda: self.actualizar('1','frecuencia'))
    ch1_per_button.clicked.connect(lambda: self.actualizar('1','periodo'))
    ch1_vmedio_button.clicked.connect(lambda: self.actualizar('1','vmedio'))
    ch1_vpp_button.clicked.connect(lambda: self.actualizar('1','vpp'))
    ch1_vrms_button.clicked.connect(lambda: self.actualizar('1','vrms'))
    ch1_vmin_button.clicked.connect(lambda: self.actualizar('1','vmin'))
    ch1_vmax_button.clicked.connect(lambda: self.actualizar('1','vmax'))
    ch1_tsubida_button.clicked.connect(lambda: self.actualizar('1','tsubida'))
    ch1_tbajada_button.clicked.connect(lambda: self.actualizar('1','tbajada'))
    
    ch2_freq_button.clicked.connect(lambda: self.actualizar('2','frecuencia'))
    ch2_per_button.clicked.connect(lambda: self.actualizar('2','periodo'))
    ch2_vmedio_button.clicked.connect(lambda: self.actualizar('2','vmedio'))
    ch2_vpp_button.clicked.connect(lambda: self.actualizar('2','vpp'))
    ch2_vrms_button.clicked.connect(lambda: self.actualizar('2','vrms'))
    ch2_vmin_button.clicked.connect(lambda: self.actualizar('2','vmin'))
    ch2_vmax_button.clicked.connect(lambda: self.actualizar('2','vmax'))
    ch2_tsubida_button.clicked.connect(lambda: self.actualizar('2','tsubida'))
    ch2_tbajada_button.clicked.connect(lambda: self.actualizar('2','tbajada'))
    
    self.setGeometry(100, 100, 500, 500)
    self.setLayout(grid)
    self.setWindowTitle('Medidas')
    self.setWindowIcon(QtGui.QIcon('/home/debian/Desktop/Aplicacion/img/icono.gif'))
    self.show()
  
  
  def actualizar(self, canal, medida):
    '''Actualiza la medida del canal seleccionado y la muestra en la ventana.
    
    Parametros:
      canal: Canal del que se quiere actualizar la medida.
      medida: Tipo de medida que se quiere actualizar.
    
    '''
    channel1= {"frecuencia":self.ch1_freq_label, "periodo":self.ch1_per_label, "vmedio":self.ch1_vmedio_label, "vpp":self.ch1_vpp_label, "vrms":self.ch1_vrms_label, "vmin":self.ch1_vmin_label, "vmax":self.ch1_vmax_label, "tsubida":self.ch1_tsubida_label, "tbajada":self.ch1_tbajada_label}
    channel2= {"frecuencia":self.ch2_freq_label, "periodo":self.ch2_per_label, "vmedio":self.ch2_vmedio_label, "vpp":self.ch2_vpp_label, "vrms":self.ch2_vrms_label, "vmin":self.ch2_vmin_label, "vmax":self.ch2_vmax_label, "tsubida":self.ch2_tsubida_label, "tbajada":self.ch2_tbajada_label}
    
    valor_medida = self.osc.get_measure(canal, medida)
    if canal == '1':
      channel1[medida].setText(valor_medida)
    else:
      channel2[medida].setText(valor_medida)
    self.update()


class VentanaInfo(QtGui.QWidget):
  '''Tiene un boton aceptar para volver al orden de ejecucion'''
  
  def __init__(self, texto):
    '''Constructor de una ventana de informacion
    
    Parametros:
      texto: Texto que mostrar'a la ventana
    
    '''
    super(VentanaInfo, self).__init__()
    self.inicializa(texto)
  
  def inicializa(self, texto):
    win = QtGui.QMessageBox()
    win.setInformativeText(texto)
    win.setWindowTitle('Aviso')
    win.setWindowIcon(QtGui.QIcon('/home/debian/Desktop/Aplicacion/img/icono.gif'))
    win.exec_()

class VentanaAviso(QtGui.QWidget):
  '''No tiene boton'''
  
  def __init__(self, texto):
    super(VentanaAviso, self).__init__()
    self.inicializa(texto)
  
  def inicializa(self, texto):
    #QtGui.QMessageBox.about(self, 'Aviso', texto)
    grid = QtGui.QGridLayout()
    grid.setSpacing(5)
    
    aviso = QtGui.QLabel(texto)
    grid.addWidget(aviso, 1, 1)
    
    self.setLayout(grid) 
    self.setGeometry(200, 200, 200, 200)
    self.setWindowTitle('Aviso')
    #self.setWindowIcon(QtGui.QIcon('/home/debian/Desktop/Aplicacion/img/icono.gif'))
    self.show()
  
  def cerrar(self):
    self.close
    

class Display(QtGui.QWidget):
  
  def __init__(self, lista_medidas1, inc_tiempo1, lista_medidas2, inc_tiempo2):
    '''Crea una ventana con el estilo de las de matlab, con matplotlib, para mostrar las dos senales representadas en el osciloscopio. Bloquea al resto de la aplicacion porque si no da problemas en la representacion de la ventana.
    
    Representa las unidades con sus magnitudes en formato ingenieril. Para pintar las senales utiliza como datos del eje Y los valores que se le pasan en los argumentos lista_medidas y les asigna su posicion en el eje		 X segun el incremento de tiempo entre medidas que obtiene de los argumentos inc_tiempo y la posicion que ocupan en lista_medidas. 
    
    Parametros:
      lista_medidas1: Valores de amplitud de los puntos del canal 1.
      inc_tiempo1: Diferencia de tiempo entre medidas.
      lista_medidas2: Valores de amplitud de los puntos del canal 2.
      inc_tiempo2: Diferencia de tiempo entre medidas.
    
    '''
    
    super(Display, self).__init__()
    
    self.figure = plt.figure()
    self.canvas = FigureCanvas(self.figure)
    self.toolbar = NavigationToolbar(self.canvas, self)
    layout = QtGui.QVBoxLayout()
    layout.addWidget(self.toolbar)
    layout.addWidget(self.canvas)
    self.setLayout(layout)
    self.setFixedSize(1600,900)
    self.setWindowTitle('Osciloscopio')
    self.setWindowIcon(QtGui.QIcon('/home/debian/Desktop/Aplicacion/img/icono.gif'))
    self.plot(lista_medidas1, inc_tiempo1, lista_medidas2, inc_tiempo2)
    
    
  def plot(self, lista_medidas1, inc_tiempo1, lista_medidas2, inc_tiempo2):
    
    # Creamos los formatos que van a mostrar las unidades que se pintan
    formatter_tiempo = EngFormatter(unit='s', places=1)
    formatter_amp = EngFormatter(unit='v', places=1)
    lista_tiempo1 = []
    lista_tiempo2 = []
    # Sabemos la diferencia de tiempos entre medidas, asi que multiplicando la posicion
    # de cada dato por el incremento de tiempo sabemos su posicion en el eje X
    for i in range(len(lista_medidas1)):
      lista_tiempo1.append(inc_tiempo1*i)

    for i in range(len(lista_medidas2)):
      lista_tiempo2.append(inc_tiempo2*i)
    
    
    # Creamos dos subplots
    ax1 = self.figure.add_subplot(211)
    ax2 = self.figure.add_subplot(212)
    
    # Representamos el canal 1
    ax1.plot(lista_tiempo1, lista_medidas1, 'y')
    ax1.set_xlabel('tiempo')
    ax1.set_ylabel('amplitud')
    ax1.xaxis.set_major_formatter(formatter_tiempo)
    ax1.yaxis.set_major_formatter(formatter_amp)
    cursor1 = Cursor(ax1)#, useblit=True)
    
    # Representamos el canal 2
    ax2.plot(lista_tiempo2, lista_medidas2, 'c')
    ax2.set_xlabel('tiempo')
    ax2.set_ylabel('amplitud')
    ax2.xaxis.set_major_formatter(formatter_tiempo)
    ax2.yaxis.set_major_formatter(formatter_amp)
    cursor2 = Cursor(ax2)#, useblit=True)
    
    self.canvas.update()
    self.canvas.flush_events()


class DisplayOjo(QtGui.QWidget):
  
  def __init__(self, medidas, tiempo):
    super(DisplayOjo, self).__init__()
    
    logging.basicConfig(level=logging.DEBUG) # Se mantienen las trazas hasta comprobar que desaparece el problema 
    self.setWindowTitle('Diagrama de ojo')
    self.setWindowIcon(QtGui.QIcon('/home/debian/Desktop/Aplicacion/img/icono.gif'))
    self.setFixedSize(900,700)
    
    self.creaInterfaz(medidas, tiempo)
  
  def creaInterfaz(self, medidas, tiempo):
    
    self.figure = plt.figure()
    self.canvas = FigureCanvas(self.figure)
    self.canvas.setParent(self)
    
    # Creamos los plots
    self.ax = plt.subplot2grid((2,2),(0,0), colspan=2) #Diagrama de ojo
    self.ax2 = plt.subplot2grid((2,2),(1,0))           #Histogramas
    self.ax3 = plt.subplot2grid((2,2),(1,1))           #erfc
    plt.subplots_adjust(left=0.15, right=0.85, bottom=0.1, top=0.9, hspace=0.25)#top=1, bottom=0.55)
    
    # Hacemos las medidas disponibles para todo el objeto
    self.lista_medidas = medidas
    self.inc_tiempo = tiempo
    
    # Creamos los formatos que van a mostrar las unidades que se pintan
    formatter_tiempo = EngFormatter(unit='s', places=1)
    formatter_amp = EngFormatter(unit='v', places=1)
    self.lista_tiempo = []
    
    # Sabemos la diferencia de tiempos entre medidas, asi que multiplicando la posicion
    # de cada dato por el incremento de tiempo sabemos su posicion en el eje X
    for i in range(len(self.lista_medidas[1])):
      self.lista_tiempo.append(self.inc_tiempo*i)
    
    # Representamos el diagrama
    self.ax.hold(True)
    for i in range(len(self.lista_medidas)):
      self.ax.plot(self.lista_tiempo, self.lista_medidas[i], 'y')
    self.ax.hold(False)
    self.ax.set_xlabel('tiempo')
    self.ax.set_ylabel('amplitud')
    self.ax.xaxis.set_major_formatter(formatter_tiempo)
    self.ax.yaxis.set_major_formatter(formatter_amp)
    self.ax.xaxis.set_minor_locator(MultipleLocator(self.inc_tiempo * 25))
    self.ax.yaxis.set_minor_locator(MultipleLocator(0.5))
    
    # Creamos las barras de muestreo y umbral
    self.intervalo_amplitud = self.ax.yaxis.get_data_interval()
    umbralInit = (self.intervalo_amplitud[0]+self.intervalo_amplitud[1])/2
    muestreoInit = self.lista_tiempo[len(self.lista_tiempo)-1]/2
    
    # Pintamos la erfc
    eje_x = np.arange(0, 10, 0.5)
    #self.ax3.plot(eje_x, 0.5*erfc(eje_x/math.sqrt(2)), color='#08088a')
    self.ax3.semilogy(eje_x, 0.5*erfc(eje_x/math.sqrt(2)), color='#08088a')
    
    logging.debug('se crea el eje semilogaritmico')
    
    self.ax3.set_xlabel('q')
    self.ax3.set_ylabel('BER')
    #self.ax3.set_yscale(u'log', nonposy='clip')
    
    # Creamos las barras horizontales y verticales de los subplots
    self.var = 25*self.inc_tiempo
    self.barMuestreo = self.ax.axvline(x=muestreoInit, color='green')
    self.barMuestreoMas = self.ax.axvline(x=muestreoInit + self.var, color='green', linestyle='--')
    self.barMuestreoMenos = self.ax.axvline(x=muestreoInit - self.var, color='green', linestyle='--')
    self.barUmbral = self.ax.axhline(y=umbralInit, color='blue')
    self.barDecision2 = self.ax2.axvline(x=umbralInit, color='blue')
    self.bar_q = self.ax3.axvline(x=10, color='blue') # Puede ser que no funcionara al empezar en cero haciendo infinito el logaritmo
    self.bar_ber = self.ax3.axhline(y=10, color='blue')
    
    # Esto hay que hacerlo antes de dibujar para que pueda poner los valores medios, q y la ber
    self.resultados_label = QtGui.QLabel(self)
    
    # Pintamos el resto de subplots
    self.dibuja(muestreoInit, umbralInit)
    
    # Barra de herramientas de matplotlib
    self.mpl_toolbar = NavigationToolbar(self.canvas, self)
    
    self.box1 = QtGui.QLineEdit(self)
    self.box2 = QtGui.QLineEdit(self)
    self.muestreo_label = QtGui.QLabel('Punto de muestreo', self)
    self.umbral_label = QtGui.QLabel('Umbral', self)
    
    self.boton = QtGui.QPushButton("Pintar", self)
    self.connect(self.boton, QtCore.SIGNAL('clicked()'), self.botonClick)
    
    hbox = QtGui.QHBoxLayout()
    
    for w in [self.muestreo_label, self.box1, self.umbral_label, self.box2, self.boton]:
      hbox.addWidget(w)
      hbox.setAlignment(w, QtCore.Qt.AlignVCenter)
    
    vbox = QtGui.QVBoxLayout()
    vbox.addWidget(self.canvas)
    vbox.addWidget(self.mpl_toolbar)
    vbox.addWidget(self.resultados_label)
    vbox.addLayout(hbox)
    
    self.setLayout(vbox)
    
  
  def botonClick(self):
    logging.debug('entramos en la rutina botonclick')
    muestreo = int(self.box1.text()) # Cogemos los valores de los porcentajes como enteros de las cajas de texto
    umbral = int(self.box2.text())
    
    if muestreo > 100: # Nos aseguramos de que estan entre cero y cien
      muestreo = 100
    if muestreo < 0:
      muestreo = 0
    muestreo = muestreo/100.0 # Los ponemos en tanto por uno y los convertimos a decimales
    
    if umbral > 100: # Nos aseguramos de que estan entre cero y cien
      umbral = 100
    if umbral < 0:
      umbral = 0
    umbral = umbral/100.0 # Los ponemos en tanto por uno y los convertimos a decimales
    
    # Calculamos con que valores corresponden los porcentajes
    valMuestreo = (muestreo*self.lista_tiempo[len(self.lista_tiempo)-1])
    valUmbral = ((self.intervalo_amplitud[1] - self.intervalo_amplitud[0]) * umbral) + self.intervalo_amplitud[0]
    logging.debug('muestreo %s umbral %s', str(valMuestreo), str(valUmbral))    
    self.dibuja(valMuestreo, valUmbral)
  
  def dibuja(self, muestreo, umbral):
    logging.debug('entramos en dibuja')
    puntoMuestreo = int(muestreo/self.inc_tiempo)
    amp = []
    
    for i in range(len(self.lista_medidas)): # Guardamos los puntos entre mas y menos 25 posiciones del punto de muestreo de todas las tramas guardadas
      for j in range(-25, 25):
        try:
          amp.append(self.lista_medidas[i][puntoMuestreo + j])
        except IndexError:
          logging.debug('oob')
    
    # Discriminamos segun el umbral
    val0 = []
    val1 = []
    
    for i in range(len(amp)):
      if(amp[i] < umbral):
        val0.append(amp[i])
      else:
        val1.append(amp[i])  
    
    # Pintamos los histogramas y las gaussianas
    self.ax2.cla()
    self.ax2.set_xlabel('amplitud')
    norm0, bins, patches = self.ax2.hist(val0, bins=200,range=[(5/4)*self.intervalo_amplitud[0], (5/4)*self.intervalo_amplitud[1]], normed=True, histtype='stepfilled', color='#ced8f6', rwidth=100)
    
    norm1, bins, patches = self.ax2.hist(val1, bins=200,range=[(5/4)*self.intervalo_amplitud[0], (5/4)*self.intervalo_amplitud[1]], normed=True, histtype='stepfilled', color='#f5a9a9', rwidth=100)
    
    v0, sigma0 = self.media_y_varianza(val0)
    gauss0 = pylab.normpdf(bins, v0, sigma0)
    self.ax2.plot(bins, gauss0, linewidth=2, color='#08088a')#azul
    
    v1, sigma1 = self.media_y_varianza(val1)
    gauss1 = pylab.normpdf(bins, v1, sigma1)
    self.ax2.plot(bins, gauss1, linewidth=2, color='#8a0808')#rojo
    
    # Calculamos la ber
    q = math.fabs(v1-v0)/(sigma1+sigma0)
    ber = 0.5*erfc(q/math.sqrt(2))
    
    self.muestra_resultados(v0, sigma0, v1, sigma1, q, ber, len(val0), len(val1))
    
    #Pintamos la erfc
    #self.ax3.cla()
    #self.ax3.set_xlabel('q')
    #self.ax3.set_ylabel('BER')
    #self.ax3.set_yscale('log')
    #eje_x = np.arange(0, 10, 0.5)
    #bar_q = self.ax3.axvline(x=q, color='blue')
    #bar_ber = self.ax3.axvline(x=ber, color='blue') hline
    #self.ax3.hold(False)
    '''plt.subplot(224)
    plt.cla()
    plt.semilogy(eje_x, 0.5*erfc(eje_x/math.sqrt(2)), color='#08088a') #parece que asi funciona mejor aunque no es definitivo
    if q < 9.4:
      plt.axhline(ber)
      plt.axvline(q)
    self.ax3.set_xlabel('q')
    self.ax3.set_ylabel('BER')'''
    #self.ax3.plot(eje_x, 0.5*erfc(eje_x/math.sqrt(2)), color='#08088a')
    #self.ax3.set_yscale('log')
    #self.ax3.hold(True)
    #self.ax3.add_line(bar_q)
    #self.ax3.add_line(bar_ber)
    #self.ax3.set_yscale('log')
    
    # Recolocamos todas las barras
    self.ax2.add_line(self.barDecision2) # Vuelve a pintar la barra del umbral cuando se redibuja
    self.ax3.add_line(self.bar_q)
    self.ax3.add_line(self.bar_ber)
    self.barMuestreo.set_xdata(muestreo)
    self.barMuestreoMas.set_xdata(muestreo + self.var)
    self.barMuestreoMenos.set_xdata(muestreo - self.var)
    self.barUmbral.set_ydata(umbral)
    self.barDecision2.set_xdata(umbral)
    logging.debug('colocamos las barras en ax3')
    self.bar_q.set_xdata(q)
    self.bar_ber.set_ydata(ber)
    logging.debug('colocadas')
    
    self.canvas.draw()
    logging.debug('ya se ha redibujado')
  
  def media_y_varianza(self, data): 
    media = 0.0
    var = 0.0
    n = len(data)
    for i in range(n):
      media = media + data[i]
    media = media/n
    for i in range(n):
      var = var + math.pow(media - data[i], 2)
    var = math.sqrt(var / (n-1))
    return media, var
  
  def muestra_resultados(self, v0, sigma0, v1, sigma1, q, ber, num0, num1):
    string = 'v0: ' + str(round(v0,3)) + '\tsigma0: ' + str(round(sigma0,3)) + '\tnumero de muestras0: ' + str(num0) + '\tQ: ' + str(round(q,2)) + '\n\n' + 'v1: ' + str(round(v1,3)) + '\tsigma1: ' + str(round(sigma1,3)) + '\tnumero de muestras1: ' + str(num1) + '\tBER: ' + '%.2e' % ber
    self.resultados_label.setText(string)

'''
def main():
  app = QtGui.QApplication(sys.argv) 
  win = Display([1,2,3,4],1,[1,2,3,4],1)
  sys.exit(app.exec_())

if __name__ == '__main__':
  main()
'''
