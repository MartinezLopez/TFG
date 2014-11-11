#!/usr/bin/python

import sys
from PySide import QtGui, QtCore
from Osciloscopio import *
from Display import *
from Modbus import *

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
    
    #Por si hay que volver al grid anterior
    '''grid.addWidget(tit_tiempo, 1, 1)
    grid.addWidget(desp_tiempo, 1, 2)
    grid.addWidget(tit_display, 1, 3)
    grid.addWidget(desp_disp, 1, 4)
    
    grid.addWidget(ch1, 2, 0)
    grid.addWidget(tit_vdiv1, 2, 1)
    grid.addWidget(desp_vdiv1, 2, 2)
    grid.addWidget(tit_acop1, 2, 3)
    grid.addWidget(desp_acop1, 2, 4)
    grid.addWidget(tit_att1, 2, 5)
    grid.addWidget(desp_att1, 2, 6)
    
    grid.addWidget(ch2, 3, 0)
    grid.addWidget(tit_vdiv2, 3, 1)
    grid.addWidget(desp_vdiv2, 3, 2)
    grid.addWidget(tit_acop2, 3, 3)
    grid.addWidget(desp_acop2, 3, 4)
    grid.addWidget(tit_att2, 3, 5)
    grid.addWidget(desp_att2, 3, 6)
    
    grid.addWidget(bot_aceptar, 4, 2)
    grid.addWidget(bot_medir, 4, 3)
    grid.addWidget(bot_medidas, 4, 4)
    grid.addWidget(bot_ojo, 4, 5)
    grid.addWidget(bot_cerrar, 4, 6)
    grid.addWidget(tit_ojo, 6, 1)
    grid.addWidget(tit_tbit, 6, 3)
    grid.addWidget(desp_ojo, 6,4)
    #grid.addWidget(bot_ojo, 6, 6)'''
    
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
    self.osc.set_horizontal(t)
    if(ch1):
      self.osc.disp_channel(True, '1')
      self.osc.set_vertical('1', vdiv1, acop1, att1.strip('x'))
    else:
      self.osc.disp_channel(False, '1')
    
    if(ch2):
      self.osc.disp_channel(True, '2')
      self.osc.set_vertical('2', vdiv2, acop2, att2.strip('x'))
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
    #Ocultamos la ventana de configuracion mientras mostramos los datos
    self.hide()
    plot = Display()
    plot.pintar(medida1, tiempo1, medida2, tiempo2)
    self.show()
  
  def diagramaOjo(self, t_bit):
    '''Crea on objeto de la clase Display en el que representa el diagrama de ojo del canal 1.
    
    '''
    tiempos_bit = {"200 ns":0x00, "50 ns":0x01, "14.3 ns":0x02, "6.67 ns":0x03}
    base_tiempos = {"200 ns":'50ns', "50 ns":'25ns', "14.3 ns":'5ns', "6.67 ns":'2.5ns'}
    # Configuramos base de tiempos y amplitud
    self.osc.set_horizontal(base_tiempos[t_bit])
    self.osc.set_vertical("1", "20mv", "AC", "1")
    # Llamada a modbus
    mb = Modbus()
    mb.write_registers(0x02, 1, [tiempos_bit[t_bit]]) #direccion, primer registro, datos
    # Configuramos el disparo
    self.osc.set_trigger('ext', 0)
    aviso = VentanaInfo('El proceso de adquisicion de datos puede llevar algun tiempo.\nPor favor, pulse el boton Aceptar y espere.')
    self.hide()
    plot = DisplayOjo()
    plot.pintar(self.osc)
    self.show()
    # Quitamos el diparo externo
    self.osc.set_trigger('1', 0)
  
  def medidas(self):
    '''Crea un objeto de la clase VentanaMedidas.
    
    '''
    #Llamar a una ventana nueva'''
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
    win.setWindowIcon(QtGui.QIcon('/home/debian/Desktop/Aplicacion/img/icono.gif'))
    win.exec_()

'''
def main():
  app = QtGui.QApplication(sys.argv) 
  win = VentanaInfo()
  sys.exit(app.exec_())

if __name__ == '__main__':
  main()
'''
