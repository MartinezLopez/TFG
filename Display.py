import numpy as np
import matplotlib.pyplot as plt
import time
import math
import pylab
from scipy.special import erfc
from matplotlib.ticker import EngFormatter, MultipleLocator
from matplotlib.widgets import Cursor, Slider
from matplotlib.patches import Rectangle
from Tkinter import PhotoImage

class Display:
  
  def pintar(self, lista_medidas1, inc_tiempo1, lista_medidas2, inc_tiempo2):
    '''Crea una ventana con el estilo de las de matlab, con matplotlib, para mostrar las dos senales representadas en el osciloscopio. Bloquea al resto de la aplicacion porque si no da problemas en la representacion de la ventana.
    
    Representa las unidades con sus magnitudes en formato ingenieril. Para pintar las senales utiliza como datos del eje Y los valores que se le pasan en los argumentos lista_medidas y les asigna su posicion en el eje X segun el incremento de tiempo entre medidas que obtiene de los argumentos inc_tiempo y la posicion que ocupan en lista_medidas. 
    
    Parametros:
      lista_medidas1: Valores de amplitud de los puntos del canal 1.
      inc_tiempo1: Diferencia de tiempo entre medidas.
      lista_medidas2: Valores de amplitud de los puntos del canal 2.
      inc_tiempo2: Diferencia de tiempo entre medidas.
    
    '''
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
    fig, (ax1, ax2) = plt.subplots(2, 1)
    mng = plt.get_current_fig_manager() # Maximizamos la ventana (TkAgg backend)
    icono = PhotoImage(file='/home/debian/Desktop/Aplicacion/img/icono.gif')
    mng.window.tk.call('wm', 'iconphoto', mng.window._w, icono)
    mng.resize(*mng.window.maxsize())
    
    # Representamos el canal 1
    ax1.plot(lista_tiempo1, lista_medidas1, 'y')
    ax1.set_xlabel('tiempo')
    ax1.set_ylabel('amplitud')
    ax1.xaxis.set_major_formatter(formatter_tiempo)
    ax1.yaxis.set_major_formatter(formatter_amp)
    cursor1 = Cursor(ax1, useblit=True)
    
    # Representamos el canal 2
    ax2.plot(lista_tiempo2, lista_medidas2, 'c')
    ax2.set_xlabel('tiempo')
    ax2.set_ylabel('amplitud')
    ax2.xaxis.set_major_formatter(formatter_tiempo)
    ax2.yaxis.set_major_formatter(formatter_amp)
    cursor2 = Cursor(ax2, useblit=True)
    
    plt.show(block=True)

class DisplayOjo:
  
  def pintar(self, osc):
    '''Crea una ventana con el estilo de las de matlab, con matplotlib, para mostrar las dos senales representadas en el osciloscopio
     en el mismo plot. Bloquea al resto de la aplicacion porque si no da problemas en la representacion de la ventana.
    
    Representa las unidades con sus magnitudes en formato ingenieril. Para pintar las senales utiliza como datos del eje Y los valores que se le pasan en los argumentos lista_medidas y les asigna su posicion en el eje X segun el incremento de tiempo entre medidas que obtiene de los argumentos inc_tiempo y la posicion que ocupan en lista_medidas. 
    
    Parametros:
      osc: Osciloscopio que se va a usar
    
    '''
    fig_aux = plt.figure(1)
    lista_medidas = []
    # Toma 32 trazas del osciloscopio
    for i in range(32):
      medidas , inc_tiempo = osc.get_data('1', 500, 2000, '1')
      lista_medidas.append(medidas)
      time.sleep(0.2)
    
    # Creamos los formatos que van a mostrar las unidades que se pintan
    formatter_tiempo = EngFormatter(unit='s', places=1)
    formatter_amp = EngFormatter(unit='v', places=1)
    lista_tiempo = []
    
    # Sabemos la diferencia de tiempos entre medidas, asi que multiplicando la posicion
    # de cada dato por el incremento de tiempo sabemos su posicion en el eje X
    for i in range(len(lista_medidas[1])):
      lista_tiempo.append(inc_tiempo*i)
    
    # Creamos los plots
    ax = plt.subplot2grid((2,2),(0,0), colspan=2) #Diagrama de ojo
    ax2 = plt.subplot2grid((2,2),(1,0))           #Histogramas
    ax3 = plt.subplot2grid((2,2),(1,1))           #erfc
    
    plt.subplots_adjust(left=0.25, right=0.9, bottom=0.05, top=0.95, hspace=0.25)#top=1, bottom=0.55)
    mng = plt.get_current_fig_manager() # Maximizamos la ventana (TkAgg backend)
    icono = PhotoImage(file='/home/debian/Desktop/Aplicacion/img/icono.gif')
    mng.window.tk.call('wm', 'iconphoto', mng.window._w, icono)
    mng.resize(*mng.window.maxsize())
    
    # Representamos el diagrama
    ax.hold(True)
    for i in range(len(lista_medidas)):
      ax.plot(lista_tiempo, lista_medidas[i], 'y')
    ax.hold(False)
    ax.set_xlabel('tiempo')
    ax.set_ylabel('amplitud')
    ax.xaxis.set_major_formatter(formatter_tiempo)
    ax.yaxis.set_major_formatter(formatter_amp)
    ax.xaxis.set_minor_locator(MultipleLocator(inc_tiempo * 25))
    ax.yaxis.set_minor_locator(MultipleLocator(0.5))
    
    # Etiquetas del plot con los histogramas
    ax2.set_xlabel('amplitud')
    
    # Creamos los sliders y las barras de muestreo y umbral y sus ejes
    intervalo_amplitud = ax.yaxis.get_data_interval()
    umbralInit = (intervalo_amplitud[0]+intervalo_amplitud[1])/2
    muestreoInit = lista_tiempo[len(lista_tiempo)-1]/2
    
    axsu = plt.axes([0.25, 0.5, 0.65, 0.01], axisbg='green')
    axsm = plt.axes([0.25, 0.48, 0.65, 0.01], axisbg='green')
    sliderUmbral = Slider(axsu, 'Umbral de decision', intervalo_amplitud[0], intervalo_amplitud[1], valinit=umbralInit, dragging=False)
    sliderMuestreo = Slider(axsm, 'Punto de muestreo', 0, lista_tiempo[len(lista_tiempo)-1], valinit=muestreoInit, dragging=False)
    
    # Creamos las barras horizontales y verticales del subplot1
    var = 25*inc_tiempo
    barMuestreo = ax.axvline(x=muestreoInit, color='green')
    barMuestreoMas = ax.axvline(x=muestreoInit + var, color='green', linestyle='--')
    barMuestreoMenos = ax.axvline(x=muestreoInit - var, color='green', linestyle='--')
    barUmbral = ax.axhline(y=umbralInit, color='blue')
    
    # Barra de umbral de decision en los subplots 2 y 3
    barDecision2 = ax2.axvline(x=umbralInit, color='blue')
    #barDecision3 = ax3.axvline(x=umbralInit, color='blue')
    
    # Creamos el rectangulo donde vamos a poner el texto y sus ejes
    axtexto = plt.axes([0.025, 0.6, 0.15, 0.15])
    axtexto.xaxis.set_visible(False)
    axtexto.yaxis.set_visible(False)
    i = 'fde'
    axtexto.text(0.1,0.2, r'$v_0$' + ': \n' + r'$v_1$' + ': \n' + r'$\sigma_0$' + ': \n' + r'$\sigma_1$' + ': \n' + 'Q: \n' + 'BER: \n' )
    
    # Rutinas de actualizacion de los sliders
    def updateSliderMuestra(val):
      barMuestreo.set_xdata(sliderMuestreo.val)
      barMuestreoMas.set_xdata(sliderMuestreo.val + var)
      barMuestreoMenos.set_xdata(sliderMuestreo.val - var)
      pideMuestras()
    
    def updateSliderUmbral(val):
      barUmbral.set_ydata(sliderUmbral.val)
      barDecision2.set_xdata(sliderUmbral.val)
      #barDecision3.set_xdata(sliderUmbral.val)
    
    sliderUmbral.on_changed(updateSliderUmbral)
    sliderMuestreo.on_changed(updateSliderMuestra) #Son dos diferentes porque era un horror pedir muestras nuevas al mover el umbral
    
    # Calcula el numero de muestra en el que esta y llama a la actualizacion de subplots
    def pideMuestras():
      muestra = int(sliderMuestreo.val / inc_tiempo) + 1 # Valores enteros desde 1 hasta 2500
      actualizaSubplots(muestra)
    
    # Actualiza la informacion de los subplots 2 y 3
    def actualizaSubplots(numMuestra):
      amp = []
      for i in range(len(lista_medidas)): 
        for j in range(-25, 25):
          amp.append(lista_medidas[i][numMuestra + j])
      
      # Discriminamos segun el umbral
      val0 = []
      val1 = []
      for i in range(len(amp)):
        if(amp[i] < sliderUmbral.val):
          val0.append(amp[i])
        else:
          val1.append(amp[i])  
      
      # Pintamos los histogramas y las gaussianas
      ax2.hold(False)
      norm0, bins, patches = ax2.hist(val0, bins=200,range=[(5/4)*intervalo_amplitud[0], (5/4)*intervalo_amplitud[1]], normed=True, histtype='stepfilled', color='#ced8f6', rwidth=100)
      ax2.hold(True)
      norm1, bins, patches = ax2.hist(val1, bins=200,range=[(5/4)*intervalo_amplitud[0], (5/4)*intervalo_amplitud[1]], normed=True, histtype='stepfilled', color='#f5a9a9', rwidth=100)
      ax2.add_line(barDecision2) # Vuelve a pintar la barra del umbral cuando se redibuja
      
      v0, sigma0 = media_y_varianza(val0)
      gauss0 = pylab.normpdf(bins, v0, sigma0)
      ax2.plot(bins, gauss0, linewidth=2, color='#08088a')#azul
      
      v1, sigma1 = media_y_varianza(val1)
      gauss1 = pylab.normpdf(bins, v1, sigma1)
      ax2.plot(bins, gauss1, linewidth=2, color='#8a0808')#rojo
      
      # Calculamos la ber
      q = math.fabs(v1-v0)/(sigma1+sigma0)
      ber = 0.5*erfc(q/math.sqrt(2))
      axtexto.cla()
      axtexto.text(0.05,0.15, r'$v_0$' + ': ' + str(round(v0,3)) + '\n' + r'$v_1$' + ': ' + str(round(v1,3)) + '\n' + r'$\sigma_0$' + ': ' + str(round(sigma0,3)) + '\n' + r'$\sigma_1$' + ': ' + str(round(sigma1,3)) + '\n' + 'Q: ' + str(round(q,2)) +'\n' + 'BER: ' + str(ber) + '\n')
      
      # Pintamos las erfc
      paso = ((5/4)*intervalo_amplitud[1] - (5/4)*intervalo_amplitud[0])/len(bins)
      eje = []
      for i in range(len(bins)):
        eje.append((paso * i) + ((5/4)*intervalo_amplitud[0]))
      
      '''ax3.hold(False)
      ax3.plot(eje, erfc(gauss0), color='#08088a')
      ax3.hold(True)
      ax3.plot(eje, erfc(gauss1), color='#8a0808')
      ax3.add_line(barDecision3) # Vuelve a pintar la barra del umbral cuando se redibuja
      '''
      #Pintamos la erfc
      eje_x = np.arange(0, q, q/10)
      bar_q = ax3.axvline(x=q, color='blue')
      bar_ber = ax3.axvline(x=ber, color='blue')
      ax3.hold(False)
      ax3.plot(0.5*erfc(eje_x/math.sqrt(2)), color='#08088a')
      ax3.hold(True)
      ax3.add_line(bar_q)
      ax3.add_line(bar_ber)
      ax3.set_yscale('log')
    
    def media_y_varianza(data): 
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
    
    pideMuestras() #Para que cargue los subplots nada mas empezar
      
    #plt.show(block=True)
    plt.show()
