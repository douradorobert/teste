# -*- coding: utf-8 -*-
"""
Created on Mon May 31 16:24:46 2021

@author: robert.dourado
"""
from datetime import timedelta, date
import pandas as pd
import os
import sys
import time

def next_du(dia, quantidade = 1, previous = False):
    """
    

    Parameters
    ----------
    dia : string
        data inicial, no formato dd/mm/yyyy.
    quantidade : int, optional
        quantidade de dias úteis que se deseja avançar ou retroceder. The default is 1.
    previous : bool, optional
        caso necessário, o usuário poderá optar por retroceder os dias úteis. The default is False.

    Returns
    -------
    nextDU : string
        data para x dias úteis no tempo, conforme solicitado.

    """
        
    try:
        cwd = os.getcwd() + '\ '.strip()
        feriados = pd.read_csv(cwd + "feriados.csv" , sep = ",")
    except KeyError:
        print("Mês de vencimento não existe!")
        sys.exit(-1)
    except FileNotFoundError:
        print("Caminho inexistente para o CSV de feriados!")
        sys.exit(-1)
        
    try:
        nextDU = time.strptime(dia,"%d/%m/%Y")
        nextDU = date(nextDU.tm_year, nextDU.tm_mon, nextDU.tm_mday)
    except:
        print("Formato de data errado, o correto é dd/mm/yyyy")
        sys.exit(-1)
    
    contagem = 0
 
    if previous == False:
        while contagem < quantidade:
            nextDU = nextDU + timedelta(days = 1)
            if nextDU.isoweekday()  in [6,7] or nextDU.strftime("%d/%m/%Y") in feriados.values:
                pass
            else:
                quantidade -= 1
        while nextDU.isoweekday() in [6,7] or nextDU.strftime("%d/%m/%Y") in feriados.values:
            nextDU = nextDU + timedelta(days = 1)
    else:
        while contagem < quantidade:
            nextDU = nextDU - timedelta(days = 1)
            if nextDU.isoweekday() in [6,7] or nextDU.strftime("%d/%m/%Y") in feriados.values:
                pass
            else:
                quantidade -= 1
        while nextDU.isoweekday() in [6,7] or nextDU.strftime("%d/%m/%Y") in feriados.values:
            nextDU = nextDU - timedelta(days = 1)
            
    nextDU = nextDU.strftime("%d/%m/%Y")
    
    return nextDU

def dias_uteis(data_inicial,data_final):
    """
    Parameters
    ----------
    data_inicial : string
        data inicial, no formato dd/mm/yyyy
    data_final : string
        data final, no formato dd/mm/yyyy

    Returns
    -------
    du : int
        quantidade de dias úteis entre as duas datas, baseado no calendário de feriados fornecido.

    """
    try:
        cwd = os.getcwd() + '\ '.strip()
    
    except:
        print("Não foi possível obter o calendário de feriados, verfique seu diretório")
        sys.exit(-1)
        
    feriados = pd.read_csv(cwd + "feriados.csv" , sep = ",").apply(lambda x: time.strptime(x[0], "%d/%m/%Y"),axis =1)
    feriados = feriados.apply(lambda x: date(x.tm_year, x.tm_mon, x.tm_mday))
    feriados_DU = feriados[feriados.apply(lambda x : x.isoweekday() not in [6,7])]
    
    try:
        data0 = time.strptime(data_inicial,"%d/%m/%Y")
        data0 = date(data0.tm_year, data0.tm_mon, data0.tm_mday)    
        data1 = time.strptime(data_final,"%d/%m/%Y")
        data1 = date(data1.tm_year, data1.tm_mon, data1.tm_mday)  
        if data1 < data0:
            data1, data0 = data0, data1
    except:
        print("Formato de data errado, o correto é dd/mm/yyyy")
        sys.exit(-1)
        
    daygenerator = (data0 + timedelta(x + 1) for x in range((data1 - data0).days))
    du = sum(1 for day in daygenerator if day.weekday() < 5) -len(feriados_DU[data0 < feriados_DU][feriados_DU < data1])
    
    return du

def first_DU(vencimento, last_day = False):
    """
    Parameters
    ----------
    vencimento : string.
        data de vencimento do vértice.    
    last_day : bool.
        O usuário pode optar por pegar o útimo dia do mês. The default is False.

    Returns
    -------
    Primeiro(Último) dia útil do mês, considerando feriados definidos pelo utilizador em um formato CSV, dentro da pasta do Script

    """
    
    
    dicionario = {'F':1, 'G':2, 'H':3, 'J':4,'K':5,'M':6,'N':7 ,'Q':8, 'U':9, 'V':10, 'X':11, 'Z':12}
    mes = dicionario[vencimento[0]]
    ano = int("20"+vencimento[1:3])
    if last_day:
        if mes == 12:
            mes = 1
            ano += 1
        else:
            mes += 1
    try:
        cwd = os.getcwd() + '\ '.strip()
        feriados = pd.read_csv(cwd + "feriados.csv" , sep = ",")
        firstDU = date(ano, mes, 1)
        # feriados = feriados.apply(lambda x: time.strptime(x[0], "%d/%m/%Y"),axis =1)
    except KeyError:
        print("Mês de vencimento não existe!")
        sys.exit(-1)
    except FileNotFoundError:
        print("Caminho inexistente para o CSV de feriados!")
        sys.exit(-1)
    except NameError:
        print("Alguma biblioteca não foi importada.")
        
    if last_day:
        firstDU = firstDU - timedelta(days = 1)
        while firstDU.isoweekday() in [6,7] or firstDU.strftime("%d/%m/%Y") in feriados.values:
            firstDU = firstDU - timedelta(days = 1)
    else:
        while firstDU.isoweekday() in [6,7] or firstDU.strftime("%d/%m/%Y") in feriados.values:
            firstDU = firstDU + timedelta(days = 1)
            
    firstDU = firstDU.strftime("%d/%m/%Y")
    
    return firstDU

def CRVBRABMF_RATE_DI1(dia, df_di1, cdi):
    """
    Parameters
    ----------
    dia : string
        data de analise, no formato dd/mm/yyyy.

    Returns
    -------
    df_di1 : PandasDataFrame
        DataFrame com informações úteis.

    """
    
    df_di1["fator_desconto"] = (100000/df_di1["AdjstdQt"])
    df_di1 = df_di1.append(pd.DataFrame([["CDI", next_du(dia),cdi,(1+cdi/100)**(1/252),1],],columns = df_di1.columns))
    df_di1 = df_di1.sort_values(by=["dias_uteis"])
    df_di1 = df_di1.reset_index(drop = True)
    df_di1["taxa_spot"] = (df_di1["fator_desconto"]**(252/df_di1["dias_uteis"])-1)*100
    return df_di1

def gerarXML(data, curva, dataframe, coluna_dataframe):
    """
    Parameters
    ----------
    data : string
        dia de análise, no formato dd/mm/yyyy.
    curva : string
        nome da curva a qual se deseja preencher os buracos.
    dataframe : dataframe
        DataFrame com as informações a serem usadas para a geração do XML.
    coluna_dataframe : string
        nome da coluna a qual o valor deve ser preenchido no XML


    Returns
    -------
    None.

    """
    
    cwd = os.getcwd()
    try:
        if not os.path.exists(cwd + "\Output"):
            os.mkdir(cwd + "\Output")
        os.mkdir(cwd + "\Output\ ".strip() + curva)
    except:
        pass
    
    series_buraco = [data]
    
    for buraco in series_buraco:
        print("\nGerando vértice {}.".format(buraco))
        Xmlstr = "<?xml version=\"1.0\" encoding=\"iso-8859-1\"?><MARKETCURVES><CURVAS data=\""
        'Manipulando strings das datas '
        date_formatted = time.strftime("%Y-%m-%d",time.strptime(buraco,"%d/%m/%Y"))
    
        'Preenchendo a data do XML '
        Xmlstr = Xmlstr + date_formatted + "\" private=\"false\">"
        
        df = dataframe
        
        ' Loop para todos os vértices '
        for i in range(0,len(df.index)):
            Xmlcurve = "<CURVA code=\"" + curva + "\" maturity=\"" 
            try:
                Xmlcurve = Xmlcurve + time.strftime("%Y-%m-%d",time.strptime(df["maturity"][i],"%d/%m/%Y")) + "\" value=\"" + str(df[coluna_dataframe][i]) + "\"/>"
                Xmlstr = Xmlstr + Xmlcurve
            except:
                pass
        Xmlstr = Xmlstr + "</CURVAS></MARKETCURVES>"
        
        Archive = cwd + "\Output\ ".strip() + curva + "\Curves_" + str(time.strftime("%Y%m%d",time.strptime(buraco,"%d/%m/%Y"))) + ".xml"
        with open(Archive, "w") as f:
            f.write(Xmlstr)
    
        print("\n{} para a data {} gerada com sucesso.".format(curva, buraco))