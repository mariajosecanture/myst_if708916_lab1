"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: data.py : python script for data collection                                                 -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

import time as time
from os import listdir, path
from os.path import isfile, join

import numpy as np
import pandas as pd
import yfinance as yf
import functions as fn

pd.set_option('display.max_rows', None)  # sin limite de renglones maximos
pd.set_option('display.max_columns', None)  # sin limite de columnas maximas
pd.set_option('display.width', None)  # sin limite al ancho del display
pd.set_option('display.expand_frame_repr', None)  # visualizar todas las columnas


# -- Obtener la lista de los archivos a leer-------------------------------------------------------

# Obtener la ruta absoluta de la carpeta donde estan los archivos
abspath = path.abspath('NAFTRAC_holdings/')

archivos = [f[:-4] for f in listdir(abspath) if isfile(join(abspath, f))]

#---------------------------------------------------------------------------------------------------
# leer todos los archivos y guardarlos en un diccionario----------------------------


# crear un diccionario para almacenar todos los datos
data_archivos = {}
for i in archivos:
    #i = archivos[0]
    # leer archivo despues de los primeros 2 renglones
    data = pd.read_csv('NAFTRAC_holdings/' + i + '.csv', skiprows=2, header=None)
    #data = pd.read_csv('NAFTRAC_holdings/NAFTRAC_310720.csv', skiprows=2, header=None)
    # renombrar las columnas con lo que tiene el 1er renglon
    data.columns = list(data.iloc[0, :])
    # quitar columnas que no sean nan
    data = data.loc[:, pd.notnull(data.columns)]
    # resetear el indice
    data = data.iloc[1:-1].reset_index(drop=True, inplace=False)
    # convertir a numerico la columna precio

    # quitar las comas en la columna de precios
    # primero lo hacemos para un dato y luego lo generalizamos
    data['Precio'] = [i.replace(',' , '') for i in data['Precio']]

    # quitar el asterisco de columna ticker
    data['Ticker'] = [i.replace('*', '') for i in data['Ticker']]

    # convertir a numerico la columna precio
    convert_dict = {'Ticker': str, 'Nombre': str, 'Peso (%)': float, 'Precio': float}
    data = data.astype(convert_dict)

    # convertir a decimal la columna de peso (%)
    data['Peso (%)'] = data['Peso (%)'] / 100
    # guardar en diccionario
    data_archivos[i] = data

# DATA FRAME FINAL


# ---------------------------------------------------------------------------------
# construir el vector de fechas a partir del vector de nombres de archivos--------
#fechas = fn.f_fechas(p_archivos=archivos)
# aproximacion de los pasos: tener la lista minuto 44
# estas serviran como etiquetas en dataframe y para yfinance
t_fechas = [i.strftime('%d-%m-%Y') for i in sorted([pd.to_datetime(i[8:]).date() for i in archivos])]
# lista con fechas ordenadas (para usarse como indexadores de archivo)
i_fechas = [j.strftime('%Y-%m-%d') for j in sorted([pd.to_datetime(i[8:]).date() for i in archivos])]
archivos = ['NAFTRAC_' + i.strftime('%d%m%y') for i in sorted(pd.to_datetime(i_fechas))]
#final data to return
r_f_fechas = {'i_fechas': i_fechas, 't_fechas': t_fechas}
# ------------------------------------------------------------------------
# ------ Construir el vector de tickers utilizables en yahoo finance


ticker = []
for i in archivos:
    # i =archivos[0]
    l_ticker = list(data_archivos[i]['Ticker'])
    [ticker.append(i + '.MX') for i in l_ticker]
global_ticker = np.unique(ticker).tolist()

# ajuste de nombre de tickers
global_ticker = [i.replace('GFREGIOO.MX', 'RA.MX') for i in global_ticker]
global_ticker = [i.replace('MEXCHEM.MX', 'ORBIA.MX') for i in global_ticker]
global_ticker = [i.replace('LIVEPOLC.1.MX', 'LIVEPOLC-1.MX') for i in global_ticker]
# eliminar MXN, USD, KOFL
[global_ticker.remove(i) for i in ['MXN.MX', 'USD.MX', 'KOFL.MX', 'BSMXB.MX', 'KOFUBL.MX']]



# --------------------------------------------PASO 1.5
# Descargar y acomodar todos los precios historicos

#global_ticker = fn.f_ticker(p_archivos=archivos, p_data_archivos=data_archivos)
inicio = time.time()

# descarga masiva de precios de yahoo.finance
data = yf.download(global_ticker, start="2017-08-21", end="2020-08-24", actions=False,
                   group_by="close", interval='1d', auto_adjust=False, prepost=False, threads=True)
# tiempo que se tarda
print('se tardo', round(time.time() - inicio, 2), 'segundos')

# data_archivos[archivos[0]]['Peso (%)']*(k//data_archivos[archivos[0]]['Precio'])

# convertir columna de fechas
data_close = pd.DataFrame({i: data[i]['Close'] for i in global_ticker})

# -- NOTA: un gran supuesto. La hora del día en el que reporta NAFTRAC el rebalanceo es la misma hora
# del día que yahoo finance reporta el precio de cierre ( y es al mismo huso horario)

# tomar solo las fechas de interes (utilizando teoria de conjuntos)
ic_fechas = sorted(list(set(data_close.index.astype(str).tolist()) & set(i_fechas)))

# localizar todos los precios
precios = data_close.iloc[[int(np.where(data_close.index.astype(str) == i)[0]) for i in ic_fechas]]

# ordenar columnas lexicograficamente
precios = precios.reindex(sorted(precios.columns), axis=1)


# ---------------------------------------------------------------------------------


# ---------------------------------------------------------------------paso 1.6
# inversion pasiva, hacer un dataframe, una evolucion de lo que le pasa a un portafolio que al incio propongas,
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
df_pasiva = {'timestamp': ['30-01-2018'], 'capital': [k]}






pos_datos = data_archivos[archivos[0]].copy().sort_values('Ticker')[
    ['Ticker', 'Nombre', 'Peso (%)']]
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
match = precios.index[precios.index == t_fechas[0]][0]

# precios necesarios para la posicion metodo 1# capital destinado por accion = proporcion de capital - comision por la posicion
n1 = np.array(precios.loc[match, [i in pos_datos['Ticker'].to_list()
                                    for i in precios.columns.to_list()]])
pos_datos['Precios'] = n1
pos_datos['Capital'] = pos_datos['Peso (%)'] * k - pos_datos['Peso (%)'] * k * c
pos_datos['Titulos'] = pos_datos['Capital'] // pos_datos['Precios']
pos_datos['Postura'] = pos_datos['Titulos'] * pos_datos['Precios']
pos_datos['Comision'] = pos_datos['Postura'] * c
pos_cash = k - pos_datos['Postura'].sum() - pos_datos['Comision'].sum()

    # -- Valor de la postura por accion
for i in range(1, len(ic_fechas)):
    match = precios.index[precios.index == ic_fechas[i]][0]

    # precios necesarios para la posicion metodo 1# capital destinado por accion = proporcion de capital - comision por la posicion
    n1 = np.array(precios.loc[match, [i in pos_datos['Ticker'].to_list()
                                    for i in precios.columns.to_list()]])
    # cantidad de titulos por acción
    pos_datos['Precios'] = n1
    pos_datos['Postura'] = pos_datos['Titulos'] * pos_datos['Precios']

    # --- Comision pagada
    pos_comision = 0
    # ---- efectivo libre en la posicion

    # ---valor de la posicion
    pos_value = pos_datos['Postura'].sum()

    # actualizar lista de valores de cada llave en el diccionario
    df_pasiva['timestamp'].append(t_fechas[i])
    df_pasiva['capital'].append(pos_value + pos_cash)
capital = list(df_pasiva['capital'])
rendimiento = [0] + [(capital[i] - capital[i-1])/capital[i] for i in range(1,len(capital))]
df_pasiva['rendimiento'] = rendimiento
rend_acum = [0]
for i in rendimiento[1:]:
    rend_acum.append(rend_acum[-1] + i)

df_pasiva['rend_acum'] = rend_acum
df_pasiva = pd.DataFrame(df_pasiva)