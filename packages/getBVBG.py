# -*- coding: utf-8 -*-
"""
Created on Mon May 31 16:24:46 2021

@author: robert.dourado
"""

from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile
import re
import sys
import time
import xml.etree.ElementTree as ET
import zipfile


def loop_teste(getfile_class, date:str, arquivo = "requerido"):
    
    print("Obtendo o arquivo {}".format(arquivo))
    for method in range(1, getfile_class.len_methods + 1):
        print("Tentando o {}° método".format(method))
        try:
            return getfile_class.try_method(method, date)
        except:
            if method == getfile_class.len_methods:
                print("Não foi possível obter o arquivo {}.".format(arquivo))
                sys.exit(-1)
                
                
def ErroCuringa(Exception):
    """
    Apenas para auxiliar a exibição de erros.
    """
    pass

# =============================================================================
class getBVBG():
    """
    Este módulo faz o download do arquivo BVBG de diferentes fontes, baseado em uma data fornecida dentro de seus métodos.\n
    Retorna um objeto "etree.ElementTree.Element"
    """
    def __init__(self, name:str, code:str, url_ftp = "None"):
        self.name = name
        self.code = code 
        self.url_ftp = url_ftp
        self.len_methods = 2
        
# =============================================================================
#     @staticmethod
#     def __doc__():
#         return "Esta classe {}".format("teste")
# =============================================================================
     
    def try_method(self, method:int, date:str):
        """
        Auxilio na função loop_teste
        """
        if method == 1:
            return self.method_1(date)
        elif method == 2:
            return self.method_2(date)
        
    "GetBVBG"
    #1° tentativa
    def method_1(self, date:str):
        """
        Função que realiza a leitura do BVBG, do "pesquisa pregão" da B3, sem escrever no disco.
    
        Parameters
        ----------
        date : str
            Data de análise, no formato "dd/mm/yyyy".
    
        Returns
        -------
        root : xml.etree.ElementTree.Element
            leitura em xml do BVBG.
        """
        date_formatted = time.strftime("%y%m%d",time.strptime(date,"%d/%m/%Y"))   #yymmdd
        try:
            resp = urlopen("http://www.b3.com.br/pesquisapregao/download?filelist="+ self.code + date_formatted+ ".zip")
        except:
            print("ERRO: Não foi possível baixar o arquivo para a data {}.\n".format(date))
            raise()
            
        try:
            #zip superior
            zfile = (BytesIO(resp.read()))
            with zipfile.ZipFile(zfile) as zfile:
                if len(zfile.namelist()) == 0:
                    print("Não há arquivo no link especificado")
                    raise ErroCuringa()
                else:
                    for fileBMF in zfile.namelist():
                        if re.search(r'\.zip$', fileBMF) is not None:
                            # We have a zip within a zip
                            zfileBMF = BytesIO(zfile.read(fileBMF))
                            with zipfile.ZipFile(zfileBMF) as zfile2:
                                # ordenamos. Como o inicio do arquivo é identico, a hora tem formato 24h, 
                                # e o arquivo respeita o padrão "BVBG.086.0.1 ... yyyymmdd .... hhmm ... .xml,
                                # o último arquivo é o mais recente.
                                filelist = zfile2.namelist()
                                filelist.sort()
                                file = filelist[-1]
                                tree = ET.parse(zfile2.open(file))
                                root = tree.getroot()
                                return root
        except ErroCuringa:
            print("ERRO: Não foi possível obter o arquivo.\n"+
                  "O arquivo ainda não foi disponibilizado\n")
            raise()
        except:
            print("ERRO: Não foi possível obter o arquivo.\n"+
                  "Formato padrão pode ter sido alterado, ou o arquivo está corrompido.\n")
            raise()
    
        
        
    
    # 2° tentativa
    def method_2(self, date:str):
        """
        Função que realiza a leitura do BVBG, em um FTP alternativo da B3, sem escrever no disco.
    
        Parameters
        ----------
        date : str
            Data de análise, no formato "dd/mm/yyyy".
    
        Returns
        -------
        root : xml.etree.ElementTree.Element
            leitura em xml do BVBG.
        """
        if self.url_ftp != None:
            date_formatted = time.strftime("%y%m%d",time.strptime(date,"%d/%m/%Y"))   #yymmdd
            try:
                resp = urlopen(self.url_ftp + self.name+"/"+self.code+ date_formatted+ ".zip")
            except:
                print("ERRO: Não foi possível baixar o arquivo para a data {}.\n".format(date))
                raise()
            try:
                # ordenamos. Como o inicio do arquivo é identico, a hora tem formato 24h, 
                # e o arquivo respeita o padrão "BVBG.086.0.1 ... yyyymmdd .... hhmm ... .xml,
                # o último arquivo é o mais recente.
                zipfile = ZipFile(BytesIO(resp.read()))
                if len(zipfile.namelist()) == 0:
                    raise() #não há arquivo no link especificado
                else:
                    filelist = zipfile.namelist()
                    filelist.sort()
                    file = filelist[-1]
                    tree = ET.parse(zipfile.open(file))
                    root = tree.getroot()
                    return root
            except:
                print("ERRO: Não foi possível extrair o arquivo.\n"+
                      "Formato padrão pode ter sido alterado, ou o arquivo está corrompido.")
                raise()
            
        else:
            print("Não há segundo método para este arquivo")
            raise()
    
class bvbgPR(getBVBG):
    def __init__(self):
        super().__init__("BVBG.086.01", "PR", "http://www.bmf.com.br/Ftp/IPN/TRS/")
        
class bvbgIN(getBVBG):
    def __init__(self):
        super().__init__("BVBG.028.02", "IN", "http://www.bmf.com.br/Ftp/IPN/TS/")
        
c = bvbgIN()
        

