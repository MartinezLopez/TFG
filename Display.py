import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import EngFormatter

class Display:
  
  def pintar(self, lista_medidas1, inc_tiempo1, lista_medidas2, inc_tiempo2):
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
    mng.resize(*mng.window.maxsize())
    
    # Representamos el canal 1
    ax1.plot(lista_tiempo1, lista_medidas1, 'y')
    ax1.set_xlabel('tiempo')
    ax1.set_ylabel('amplitud')
    ax1.xaxis.set_major_formatter(formatter_tiempo)
    ax1.yaxis.set_major_formatter(formatter_amp)
    
    # Representamos el canal 2
    ax2.plot(lista_tiempo2, lista_medidas2, 'c')
    ax2.set_xlabel('tiempo')
    ax2.set_ylabel('amplitud')
    ax2.xaxis.set_major_formatter(formatter_tiempo)
    ax2.yaxis.set_major_formatter(formatter_amp)
    
    plt.show(block=True)
