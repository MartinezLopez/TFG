App.py

Punto de entrada de la aplicación.

get_osc_id():
  
  Consulta todos los dispositivos USB conectados y elige el dispositivo de Tektronix, que presumiblemente será el osciloscopio.
  Una vez seleccionado el osciloscopio obtiene su id_vendor e id_device y lo ajusta al formato que espera recibir python-usbtmc

  Devuelve la id del osciloscopio en formato esperado por python-usbtmc

main():
  
  Ejecuta la aplicación.
  Conecta con el osciloscopio y carga la ventana principal.

---------------------------------------------------------------------------------

Display.py

clase Display
  
  pintar(self, lista_medidas1, incremento_de_tiempo1, lista_medidas2, incremento_de_tiempo2):
    
    lista_medidas1 ---------- Valores de amplitud de las medidas del Canal1 del osciloscopio
    incremento_de_tiempo1 --- Diferencia de tiempos entre valores de amplitud del Canal1 del osciloscopio
    lista_medidas2 ---------- Valores de amplitud de las medidas del Canal2 del osciloscopio
    incremento_de_tiempo2 --- Diferencia de tiempos entre valores de amplitud del Canal1 del osciloscopio

    Como sabemos el número de medidas de cada canal y la diferencia de tiempo que hay entre una medida y otra, podemos establecer el instante de tiempo que corresponde a una medida multiplicando el incremento de tiempo de su canal por la posición que ocupa en la lista de medidas, de esta forma tenemos cada valor localizado en el eje de amplitud(vertical) y en el de tiempos(horizontal).
    
    Creamos una ventana de pyplot con dos subplots, la maximizamos y en el primer subplot representamos los valores del canal 1 del osciloscopio y en el segundo los del canal 2.
    
    Mientras esta ventana se encuentra activa el resto de la aplicación está bloqueada.

---------------------------------------------------------------------------------

Osciloscopio.py

clase Osciloscopio

  __init__(self, id)
    
    id --- id_vedor e id_device del osciloscopio en el formato esperado por python-usbtmc
    
    Inicializa los diccionarios que se aseguran de que todos los valores que se envíen al osciloscopio sean valores válidos. También inicializa la variable que se refiere al osciloscopio.
    
    Los diccionarios son:
        vol_div = {"5v":'5', "2v":'2', "1v":'1', "500mv":'500e-3', "200mv":'200e-3', "100mv":'100e-3', "50mv":'50e-3', "20mv":'20e-3', "10mv":'10e-3', "5mv":'5e-3', "2mv":'2e-3'}
        sec_div = {"50s":'50', "25s":'25', "10s":'10', "5s":'5', "2.5s":'2.5', "1s":'1',"500ms":'500e-3', "250ms":'250e-3', "100ms":'100e-3',"50ms":'50e-3', "25ms":'25e-3', "10ms":'10e-3', "5ms":'5e-3', "2.5ms":'2.5e-3', "1ms":'1e-3', "500us":'500e-6', "250us":'250e-6', "100us":'100e-6',"50us":'50e-6', "25us":'25e-6', "10us":'10e-6', "5us":'5e-6', "2.5us":'2.5e-6', "1us":'1e-6', "500ns":'500e-9', "250ns":'250e-9', "100ns":'100e-9',"50ns":'50e-9', "25ns":'25e-9', "10ns":'10e-9', "5ns":'5e-9', "2.5ns":'2.5e-9'}
        acoplamiento = {"AC":'AC', "DC":'DC', "GND":'GND'}
        canal = {"1":'CH1', "2":'CH2'}
        atenuacion = {"1":'1', "10":'10'} 
        bytes_medida = {"2":'2', "1":'1'}
        medidas = {"frecuencia":'FREQ', "periodo":'PERI', "vmedio":'MEAN', "vpp":'PK2', "vrms":'CRM', "vmin":'MINI', "vmax":'MAXI', "tsubida":'RIS', "tbajada":'FALL'}

  set_display(self, mode)
    
    mode --- modo de del formato del display.
    
    Cambia el formato del display entre XY e YT. Si se introduce un valor erróneo se pone formato YT. 

  set_horizontal(self, tiempo)
    
    tiempo --- clave del diccionario sec_div
    
    Ajusta la base de tiempos del oscilosopio

  set_vertical(self, channel, v_d, coupling, probe)
    
    channel ---- clave del diccionario canal. Canal que se quiere ajustar
    v_d -------- clave del diccionario vol_div. Voltios/División que se quiere obtener.
    coupling --- clave del diccionario acoplamiento. Tipo de acoplamiento deseado.
    probe ------ clave del diccionario atenuacion. Factor de atenuación de la sonda.
    
    Ajusta por canal el número de voltios que corresponden a cada división, el tipo de acoplamiento y la atenuación de la sonda empleada.

  get_data(self, source, start, stop, width)
    
    source --- clave del diccionario canal. Canal del que se leen los datos.
    start ---- Primer punto. (>= 1)
    stop ----- Último punto. (<= 2500)
    width ---- clave del diccionario bytes_medida. Precisión de la medida.
    
    Obtiene los valores de amplitud y la diferencia de tiempos entre valores del canal seleccionado, pudiendo elegir la precisión con la que se hace la medida.
    
    Utiliza una codificación binaria de entero con signo que con un byte admite números entre 127 y -128 y con dos bytes entre 32767 y -32768.
    Primero configura el número de puntos, el canal y la precisión de la medida, obtiene la escala de tiempos y calcula la distancia entre puntos. Cómo el valor de los puntos está referido a su posición en el display, so obtiene el valor de voltios/división configurado para el canal de la medida.
    Una vez hecho esto, se piden los puntos que queremos, quitamos la cabecera que lleva el mensaje y los convertimos desde binario para poder utilizarlos.
    Dependiendo de la precisión que hayamos empleado el valor máximo será uno u otro, así que teniendo eso en cuenta y el valor de los voltios/división se calcula la amplitud de cada punto.

    Devuelve los valores de amplitud y su diferencia de tiempos.

  disp_channel(self, state, channel)
    
    state ----- Si el canal esta visible True, si no False
    channel --- clave del diccionario canal. Canal al que se le quiere cambiar el estado.
    
    Muestra u oculta un canal seleccionado.
  
  get_measure(self, channel, medida)
    
    channel --- clave del diccionario canal. Canal del que se quiere conocer una medida.
    medida ---- clave del diccionario canal medidas. Medida que se quiere conocer
    
    Permite obtener una medida determinada de un canal.
    
    Devuelve la medida en formato String con unidades, ajustando la magnitud y mostrando dos decimales.

  formatter(self, value)
    
    value --- Valor al que se quiere dar formato (String)
    
    Ajusta el formato de un valor numérico para mostrarlo con su magnitud y dos cifras decimales.
    
    Devuelve el número en formato String

---------------------------------------------------------------------------------

Ventana.py

clase VentanaConfiguracion(Qt.QWidget)
  
  global osc --- variable global del osciloscopio sobre el que se trabaja.
  
  __init__(self, osciloscopio)
    osciloscopio --- Osciloscopio sobre el que se trabaja.
    
    Inicializa la variable global osc y llama a conf_osc() para inicializar la ventana principal de la aplicación.
  
  conf_osc(self)
    
    Crea la ventana principal de la aplicación. En ella se puede configurar la base de tiempos del osciloscopio, el formato del diplay (XY o YT), que canales se muestran, con que amplitud/división trabaja cada canal, el tipo de acoplamiento del canal y la atenuación de la sonda, llamando a la función aceptar().
    También permite abrir la pantalla que muestra el osciloscopio (clase Display) con la función medida() y permite abrir la pantalla de medidas de cada canal llamando a medidas()
  
  aceptar_conf(self, t, display, ch1, vdiv1, acop1, att1, ch2, vdiv2, acop2, att2)
    
    t --------- Valor de la base de tiempos.
    display --- Formato del display.
    ch1 ------- Si se muestra o no el canal 1 (boolean).
    vdiv1 ----- Voltios/división del canal 1.
    acop1 ----- Tipo de acoplamiento del canal 1.
    att1 ------ Atenuación de la sonda del canal 1.
    ch2 ------- Si se muestra o no el canal 2 (boolean).
    vdiv2 ----- Voltios/división del canal 2.
    acop2 ----- Tipo de acoplamiento del canal 2.
    att2 ------ Atenuación de la sonda del canal 2.
    
    Configura el ociloscopio llamando a los métodos de la clase Osciloscopio
    
  medida(self, ch1, ch2)
    
    ch1 --- Si se muestra o no el canal 1 (boolean).
    ch2 --- Si se muestra o no el canal 2 (boolean).
    
    Si el canal está seleccionado pide los 2500 puntos del osciloscopio y los muestra llamando a la clase Display().
    Si el canal no esta seleccionado no pinta nada en su subplot.
    
  medidas(self)
     Llama a la clase VentanaMedidas

clase VentanaMedidas(Qt.QWidget)
  
  global osc --- variable global del osciloscopio sobre el que se trabaja
  
  __init__(self, osciloscopio)

    osciloscopio --- Osciloscopio sobre el que se trabaja.
    
    Inicializa la variable global osc y llama a inicializa() para inicializar la ventana principal de medidas.
  
  inicializa(self)
    
    Crea la ventana con columnas para cada canal y filas para cada tipo de medida.
    Pulsando el botón de cada medida y canal se muestra la medida. Es probable que haya que hacer click un par de veces.
  
  cerrar(self)
    
    Cierra la ventana de medidas.

  actualizar(self, canal, medida)
    
    canal ---- Canal sobre el que se quiere medir
    medida --- Tipo de medida que se va a hacer
    
    Cada vez que se presiona un botón se llama a este método que pide la medida al osciloscopio mediante la clase Osciloscopio y la muestra en su lugar correspondiente.
