import pandas as pd
import numpy as np

#BUG: è computer-specific, trova un modo per renderlo fruibile da ovunque
path = 'C:/Users/Elena/Documents/UNIVERSITA/2_Pattern Recognition/Project_exam/Air_quality/'

#LOAD THE LOOK UP TABLES
params_lut = pd.read_excel(path+'/parametri.xlsx')
stations_lut = pd.read_excel(path+'/QARIA_Stazioni.xlsx')
#print(stations_lut.columns)
Cod_staz = stations_lut['Cod_staz'].unique()
IdParametro = params_lut['IdParametro'].unique()

#print(stations_lut['TIPO_STAZ'].unique())
#ci sono delle etichette TIPO_STAZ che sono "nan" ---> guess them!

#LOAD THE DATA
#using string interpolation
'''
year: 2010----2021
cod_staz: loop su Cod_staz - manca lo zero davanti a volte
num_inq: IdParametro
'''
for year in np.arange(2010, 2022, 1):
    for cod_staz in Cod_staz:
        for num_inq in IdParametro:
            my_data = pd.read_csv(path+f'/CSV Stazione_Parametro_AnnoMese/storico_{year}_{cod_staz}_{num_inq}.csv')
#BUG: al momento sovrascrive sempre my_data. Crea un totale di 2702 tabelle.

#FUNZIONA MA è SOLO UNA TABELLA
""" year = '2010'
cod_staz = '02000003'
num_inq = '005'
my_data = pd.read_csv(path+f'/CSV Stazione_Parametro_AnnoMese/storico_{year}_{cod_staz}_{num_inq}.csv')
print(my_data[0:5]) """
