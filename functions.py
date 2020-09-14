
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: functions.py : python script with general functions                                         -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

import numpy as np
from data import archivos, data_archivos
import pandas as pd


#functions.py
#Paso 3------------------------------------------------------------------
#Construir el vector de fechas a partir del vector de nombres de archivos

def f_fechas(p_archivos):

    # estas serviran como etiquetas en dataframe y para yfinance
    t_fechas = [i.strftime('%d-%m-%Y') for i in sorted([pd.to_datetime(i[8:]).date() for i in p_archivos])]
    # lista con fechas ordenadas (para usarse como indexadores de archivo)
    i_fechas = [j.strftime('%Y-%m-%d') for j in sorted([pd.to_datetime(i[8:]).date() for i in p_archivos])]

    #final data to return
    r_f_fechas = {'i_fechas': i_fechas, 't_fechas': t_fechas}
    return r_f_fechas
fechas = f_fechas(p_archivos=archivos)
#functions.py

#Paso 4------------------------------------------------------------------
#Construir el vector de tickets utilizables en yahoo finance


def f_ticker(p_archivos, p_data_archivos):
    ticker = []
    for i in p_archivos:
        # i =archivos[0]
        l_ticker = list(p_data_archivos[i]['Ticker'])
        [ticker.append(i + '.MX') for i in l_ticker]
    global_ticker = np.unique(ticker).tolist()

    # ajuste de nombre de tickers
    global_ticker = [i.replace('GFREGIOO.MX', 'RA.MX') for i in global_ticker]
    global_ticker = [i.replace('MEXCHEM.MX', 'ORBIA.MX') for i in global_ticker]
    global_ticker = [i.replace('LIVEPOLC.1.MX', 'LIVEPOLC-1.MX') for i in global_ticker]
    # eliminar MXN, USD, KOFL
    [global_ticker.remove(i) for i in ['MXN.MX', 'USD.MX', 'KOFL.MX', 'BSMXB.MX', 'KOFUBL.MX']]

    return global_ticker





#functions.py

#Paso 5-------------------------------------------------------------------
#Descargar y acomodar todos los precios historicos

def obtener_precios(p_ticker, p_fechas):
    inicio = time.time()

    # descarga masiva de precios de yahoo.finance
    data = yf.download(p_ticker, start="2017-08-21", end="2020-08-24", actions=False,
                       group_by="close", interval='1d', auto_adjust=False, prepost=False, threads=True)
    # tiempo que se tarda
    print('se tardo', round(time.time() - inicio, 2), 'segundos')

    # data_archivos[archivos[0]]['Peso (%)']*(k//data_archivos[archivos[0]]['Precio'])

    # convertir columna de fechas
    data_close = pd.DataFrame({i: data[i]['Close'] for i in p_ticker})

    # -- NOTA: un gran supuesto. La hora del día en el que reporta NAFTRAC el rebalanceo es la misma hora
    # del día que yahoo finance reporta el precio de cierre ( y es al mismo huso horario)

    # tomar solo las fechas de interes (utilizando teoria de conjuntos)
    ic_fechas = sorted(list(set(data_close.index.astype(str).tolist()) & set(p_fechas)))

    # localizar todos los precios
    precios = data_close.iloc[[int(np.where(data_close.index.astype(str) == i)[0]) for i in ic_fechas]]

    # ordenar columnas lexicograficamente
    precios = precios.reindex(sorted(precios.columns), axis=1)

    return precios