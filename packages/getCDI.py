# -*- coding: utf-8 -*-
"""
Created on Mon May 31 16:24:46 2021

@author: robert.dourado
"""
from io import BytesIO, TextIOWrapper
from urllib.request import urlopen
from zipfile import ZipFile
import json
import time
import urllib

class cdi():
    def __init__(self):
        self.len_methods = 3
     
    def try_method(self, method:int, date:str):
        """
        Auxilio na função loop_teste
        """
        if method == 1:
            return self.method_1(date)
        elif method == 2:
            return self.method_2(date)
        elif method == 3:
            return self.method_3(date)

    "GetCDI"
    #1° tentativa
    @staticmethod
    def method_1(date:str):
        """
        Função que capta o CDI da página inicial da B3 (http://www.b3.com.br/pt_br/)
    
        Parameters
        ----------
        date : str
            Data de análise, no formato "dd/mm/yyyy".
    
        Returns
        -------
        cdi : float
            Taxa CDI.
    
        """
        fp = urllib.request.urlopen("https://www2.cetip.com.br/ConsultarTaxaDi/ConsultarTaxaDICetip.aspx")
        mybytes = fp.read()
        mystr = mybytes.decode("utf8")      #formato JSON
        fp.close()
        rate = json.loads(mystr)
        if rate["dataTaxa"] == date:
            cdi = float(rate["taxa"].replace(",","."))
        else:
            print("ERRO: O dia extraído não é o mesmo de hoje.\n"+
                  "Data extraída: {}\nData de hoje: {}".format(rate["dataTaxa"], date))
            raise()
        return cdi
    
    #2° tentativa
    @staticmethod
    def method_2(date):
        """
        Função que capta o CDI de um FTP, servindo como método alternativo.
    
        Parameters
        ----------
        date : str
            Data de análise, no formato "dd/mm/yyyy".
    
        Returns
        -------
        cdi : float
            Taxa CDI.
    
        """
        date_formatted = time.strftime("%Y%m%d",time.strptime(date,"%d/%m/%Y"))   #yyyymmdd
        
        url = "http://www.bmf.com.br/Ftp/IndicadoresEconomicos/ID" + time.strftime("%y%m%d",time.strptime(date,"%d/%m/%Y")) + ".ex_"
        
        try:
            resp = urlopen(url)
        except:
            print("ERRO: Não foi possível encontrar o arquivo zip para a data {}.\n".format(date))
            raise()
        
        #Read file inside zip without downloading  it
        try:
            zfile = ZipFile(BytesIO(resp.read()))
            file = zfile.namelist()[0]              #Getting the name of the file
            indic = TextIOWrapper(zfile.open(file), encoding="utf-8")
        except:
            print("ERRO: Não foi possível extrair o arquivo.\n"+
                  "Formato padrão pode ter sido alterado, ou o arquivo está corrompido.")
            raise()
            
        # Lendo arquivo e procurando selic
        try:
            lines = indic.readlines()
            for i in range(0,len(lines)):
                #Achando a linha correspondente
                if lines[i][11:24] == date_formatted +  "RTDI1":
                    #Achando o numero de decimais
                    numberofdecimals = int(lines[i][71:73])
                    #Capturando as strings dos numeros
                    integer = lines[i][47:71-numberofdecimals]
                    decimal = lines[i][71-numberofdecimals:71]
                    #Juntando as strings dos numeros e fazendo a transformacao
                    number = integer + "." + decimal
                    number = float(number)
                    cdi = number
        except:
            print("ERRO: Não foi possível salvar o arquivo, ou a taxa para o dia solicitado ({}).".format(date))
            raise()
        return cdi
    
    #3° tentativa
    @staticmethod
    def method_3(date):
        """
        Função que capta o CDI de um outro FTP, servindo como uma terceira alternativa.
    
        Parameters
        ----------
        date : str
            Data de análise, no formato "dd/mm/yyyy".
    
        Returns
        -------
        cdi : float
            Taxa CDI.
    
        """
        date_formatted = time.strftime("%Y%m%d",time.strptime(date,"%d/%m/%Y"))   #yyyymmdd
        try:
            fp = urllib.request.urlopen("ftp://ftp.cetip.com.br/MediaCDI/"+ date_formatted +".txt")
            mybytes = fp.read()
            mystr = mybytes.decode("utf8").strip()
            fp.close()
            cdi = float(mystr[:-2] + "." + mystr[-2:])
        except:
            print("ERRO: Não existe arquivo FTP da CDI para a data {}.\n".format(date))
            raise()
            
        return cdi