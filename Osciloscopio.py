#!/usr/bin/python

import usbtmc
from struct import unpack
import time

class Osciloscopio:
    
  def __init__(self, id):
    # Inicializamos los diccionarios para que tengan los valores validos para el osciloscopio
    self.vol_div = {"5v":'5', "2v":'2', "1v":'1', "500mv":'500e-3', "200mv":'200e-3', "100mv":'100e-3', "50mv":'50e-3', "20mv":'20e-3', "10mv":'10e-3', "5mv":'5e-3', "2mv":'2e-3'}
    self.sec_div = {"50s":'50', "25s":'25', "10s":'10', "5s":'5', "2.5s":'2.5', "1s":'1',"500ms":'500e-3', "250ms":'250e-3', "100ms":'100e-3',"50ms":'50e-3', "25ms":'25e-3', "10ms":'10e-3', "5ms":'5e-3', "2.5ms":'2.5e-3', "1ms":'1e-3', "500us":'500e-6', "250us":'250e-6', "100us":'100e-6',"50us":'50e-6', "25us":'25e-6', "10us":'10e-6', "5us":'5e-6', "2.5us":'2.5e-6', "1us":'1e-6', "500ns":'500e-9', "250ns":'250e-9', "100ns":'100e-9',"50ns":'50e-9', "25ns":'25e-9', "10ns":'10e-9', "5ns":'5e-9', "2.5ns":'2.5e-9'}
    self.acoplamiento = {"AC":'AC', "DC":'DC', "GND":'GND'}
    self.canal = {"1":'CH1', "2":'CH2'}
    self.atenuacion = {"1":'1', "10":'10'} 
    self.bytes_medida = {"2":'2', "1":'1'}
    self.medidas = {"frecuencia":'FREQ', "periodo":'PERI', "vmedio":'MEAN', "vpp":'PK2', "vrms":'CRM', "vmin":'MINI', "vmax":'MAXI', "tsubida":'RIS', "tbajada":'FALL'}
    
    # Inicializamos el osciloscopio
    self.ins = usbtmc.Instrument("USB::" + id + "::INSTR")

  def set_display(self, mode):
    if mode == "XY":
      self.ins.write("DIS:FORM XY")
    else:
      self.ins.write("DIS:FORM YT")
  
  def set_horizontal(self, tiempo):
    escala = self.sec_div[tiempo]
    self.ins.write("HOR:SCA " + escala)
  
  def set_vertical(self, channel, v_d, coupling, probe):
    ch = self.canal[channel]
    vdiv = self.vol_div[v_d]
    acoplo = self.acoplamiento[coupling]
    att = self.atenuacion[probe]
    
    self.ins.write(ch + ":COUP " + acoplo + ";PRO " + probe + ";VOL " + vdiv)
  
  def get_data(self, source, start, stop, width):
    codificacion = "RIB" #Entre 127 y -128 con un byte
    ch = self.canal[source]
    if start < 1:
      start = 1
    if stop > 2500:
      stop = 2500
    prec = self.bytes_medida[width]
    self.ins.write("DAT:ENC " + codificacion +";SOU " + ch + ";STAR " + str(start) + ";STOP " + str(stop) + ";WID " + prec)
    
    incremento_tiempo = float(self.ins.ask("HOR:MAI:SCA?"))/250 #*10divisiones/2500 puntos
    v_div = float(self.ins.ask(ch + ":SCA?"))
    
    puntos = self.ins.ask_raw("CURV?")
    header_length = 2 + int(puntos[1]) #Calculamos el tamano de la cabecera para no cogerla
    puntos = puntos[header_length:-1]
    puntos = unpack('%sb' % len(puntos), puntos) #Los convertimos desde enteros con signo
    
    if prec == '2': #Si la resolucion no es dos la consideramos uno
      escala = 6553.4 #32767/5
    else:
      escala = 25.4 #127/5
    
    tension =[]
    for dato in puntos:
      dato = dato*v_div/escala
      tension.append(dato)
    return tension, incremento_tiempo
  
  def disp_channel(self, state, channel):
    ch = self.canal[channel]
    if(state == True):
      self.ins.write("SEL:" + ch + " ON")
    else:
      self.ins.write("SEL:" + ch + " OFF")
  
  def get_measure(self, channel, medida):
    # Los sleep despues de cada escritura son necesarios porque al osciloscopio no le da tiempo a configurarse tan rapido y devuelve un error
    ch = self.canal[channel]
    tipo_medida = self.medidas[medida]
    
    self.ins.write_raw("MEASU:IMM:SOU " + ch)
    time.sleep(0.5)
    self.ins.write_raw("MEASU:IMM:TYP " + tipo_medida)
    time.sleep(0.5)
    value = self.ins.ask_raw("MEASU:IMM:VAL?")
    value = self.formatter(value)
    units = self.ins.ask_raw("MEASU:IMM:UNI?")
    value = value + units[1:-2] #para quitar las comillas
    
    return value
  
  def formatter(self, value):
    # numero de decimales + punto
    prec = 3
    
    index = value.find('E')
    number = float(value[0:index])
    exp = value[index:-1]
    
    # Por si no esta definido luego
    new_exp = exp
    mult = 1
    
    if(exp == 'E-12'):
      mult = 1
      new_exp = 'p'
    if(exp == 'E-11'):
      mult = 10
      new_exp = 'p'
    if(exp == 'E-10'):
      mult == 100
      new_exp = 'p'
    if(exp == 'E-9'):
      mult = 1
      new_exp = 'n'
    if(exp == 'E-8'):
      mult = 10
      new_exp = 'n'
    if(exp == 'E-7'):
      mult = 100
      new_exp = 'n'
    if(exp == 'E-6'):
      mult = 1
      new_exp = 'u'
    if(exp == 'E-5'):
      mult = 10
      new_exp = 'u'
    if(exp == 'E-4'):
      mult = 100
      new_exp = 'u'
    if(exp == 'E-3'):
      mult = 1
      new_exp = 'm'
    if(exp == 'E-2'):
      mult = 10
      new_exp = 'm'
    if(exp == 'E-1'):
      mult = 100
      new_exp = 'm'
    if(exp == 'E0'):
      mult = 1
      new_exp = ''
    if(exp == 'E1'):
      mult = 10
      new_exp = ''
    if(exp == 'E2'):
      mult = 100
      new_exp = ''
    if(exp == 'E3'):
      mult = 1
      new_exp = 'K'
    if(exp == 'E4'):
      mult = 10
      new_exp = 'K'
    if(exp == 'E5'):
      mult = 100
      new_exp = 'K'
    if(exp == 'E6'):
      mult = 1
      new_exp = 'M'
    if(exp == 'E7'):
      mult = 10
      new_exp = 'M'
    if(exp == 'E8'):
      mult = 100
      new_exp = 'M'
    if(exp == 'E9'):
      mult = 1
      new_exp = 'G'
    if(exp == 'E10'):
      mult = 10
      new_exp = 'G'
    if(exp == 'E11'):
      mult = 100
      new_exp = 'G'
    if(exp == 'E12'):
      mult = 1
      new_exp = 'T'
    
    num = str(number * mult)
    dot = num.find('.')
    num = num[0:(dot+prec)]
    num = num + ' ' + new_exp
    return num
    


'''  
def main(): 
  osc = Osciloscopio("0x0699::0x0369")
  osc.set_vertical("1", "2v", "AC", "1")
  osc.set_horizontal('250us')
  print osc.get_data("1", 1, 150, '1')

if __name__ == '__main__':
  main()
'''
