#TODO ci sono delle etichette TIPO_STAZ che sono "nan" ---> guess them!
import pandas as pd
import numpy as np
import glob
import os

#NECESSARIO AVERE UNA CERTA "FOLDER ORGANIZATION"
#Get CSV files list from a folder
path = os.getcwd()
all_files = glob.glob(path + "/CSV Stazione_Parametro_AnnoMese/*.csv")
#all_files: lista di 2702 stringhe

#LOAD THE DATA
all_dfs = []
for file in all_files:
    my_data = pd.read_csv(file, header = 0)
    all_dfs.append(my_data)
#all_dfs: lista di 2702 elementi, ciascun elemento è un Pandas dataframe

#LOAD THE LOOK UP TABLES
params_lut = pd.read_excel(path+'/parametri.xlsx')
stations_lut = pd.read_excel(path+'/QARIA_Stazioni.xlsx')
Cod_staz = stations_lut['Cod_staz'].unique()
#Cod_staz: <class 'numpy.ndarray'> pieno di <class 'numpy.int64'>
IdParametro = params_lut['IdParametro'].unique()
#IdParametro: <class 'numpy.ndarray'> pieno di <class 'numpy.float64'>

