
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: main.py : python script with the main functionality                                         -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

import functions as fn
from data import archivos, data_archivos

#import visualizations as vs
#90 por ciento de procesos de tu notebook



#Paso 1--------------------------------------------------------------------
#Obtener la lista de los archivos a leer

archivos = archivos

#data.py

#Paso 2----------------------------------------------------------------
#Leer todos los archivos y guardarlos en un diccionario

data_archivos = data_archivos

#functions.py

#Paso 3------------------------------------------------------------------
#Construir el vector de fechas a partir del vector de nombres de archivos

fechas = fn.f_fechas(p_archivos= archivos)
print(fechas['i_fechas'][0:4])
print(fechas['t_fechas'][0:4])

#functions.py

#Paso 4------------------------------------------------------------------
#Construir el vector de tickets utilizables en yahoo finance

global_ticker = fn.f_ticker(p_archivos= archivos, p_data_archivos= data_archivos)
print(global_ticker[0:4])
#functions.py

#Paso 5-------------------------------------------------------------------
#Descargar y acomodar todos los precios historicos

precios = fn.obtener_precios(p_ticker=global_ticker, p_fechas=fechas['i_fechas'])
precios = precios['precios']

print(precios,head[5])


#main.py

#Paso 6--------------------------------------------------------------------
#Postura inicial
# indice,
# posicion inicial
k = 1000000
# comision por transaccion
c = 0.00125
# vector de comisiones historicas
comisiones = []

# obtener posicion inicial
# los % para KOFL, KOFUBL, BSMXB, MXN, USD asignarlos a cash (eliminados)
c_activos = ['KOFL', 'KOFUBL', 'BSMXB', 'MXN', 'USD']
# diccionario para resultado final
inv_pasiva = {'timestamp': ['30-01-2018'], 'capital': [k]}

# dejar 'archivo' ordenado por fechas
pos_datos = data_archivos[archivos[0]].copy().sort_values('Ticker')[['Ticker', 'Nombre', 'Peso (%)']]
# lista de activos a elminiar

i_activos = list(pos_datos[list(pos_datos['Ticker'].isin(c_activos))].index)
# eliminar activos del dataframe
pos_datos.drop(i_activos, inplace=True)
# resetear index
pos_datos.reset_index(inplace=True, drop=True)
# agregar .MX para empatar precios
pos_datos['Ticker'] = pos_datos['Ticker'] + '.MX'
# corregir tickers en datos
pos_datos['Ticker'] = pos_datos['Ticker'].replace('LIVEPOLC.1.MX', 'LIVEPOLC-1.MX')
pos_datos['Ticker'] = pos_datos['Ticker'].replace('MEXCHEM.MX', 'ORBIA.MX')
pos_datos['Ticker'] = pos_datos['Ticker'].replace('GFREGIOO.MX', 'RA.MX')

#main.py

#Paso 7----------------------------------------------------------------------
#Evolución de la postura (Inversión Pasiva)



#visualizations.py

#Paso 8----------------------------------------------------------------------
#Evolución de la postura (Inversión Activa)


#main.py

#Paso 9-----------------------------------------------------------------------
#Medidas de atribución


#Paso 9-----------------------------------------------------------------------
#Plot de comparación entre estrategias
#plot de evolucion del capital (invrsion pasova)