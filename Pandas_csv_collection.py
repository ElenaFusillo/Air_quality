#TODO ci sono delle etichette TIPO_STAZ che sono "nan" ---> guess them!
#TODO Air Quality Index? proposta
import os
import time
import numpy as np
import pandas as pd

#NECESSARIO AVERE UNA CERTA "FOLDER ORGANIZATION"
#LOAD THE LOOK UP TABLES

start_time = time.time()

path = os.getcwd()
params_lut = pd.read_excel(path+'/parametri.xlsx', usecols="A:D", dtype={'IdParametro': np.int16, 'Tmed (min)': np.int16})
stations_lut = pd.read_excel(path+'/QARIA_Stazioni.xlsx', dtype={'Cod_staz':str, 'Id_Param': str})
Cod_staz = sorted(stations_lut['Cod_staz'].drop_duplicates()) # lista python di stringhe
for i in range(len(Cod_staz)):
    Cod_staz[i] = Cod_staz[i].rjust(8, '0')
IdParametro = sorted(params_lut['IdParametro'].drop_duplicates()) # lista python di interi
for i in range(len(IdParametro)):
    IdParametro[i] = str(IdParametro[i]).rjust(3, '0')
index_inq_day = [1, 11] #indici degli inquinanti che ci sono veramente dentro i .csv
index_inq_hour = [0, 2, 3, 4, 5, 6, 7, 9, 10] #indici degli inquinanti che ci sono veramente dentro i .csv

def create_rif_serie(stazione_scelta, year, freq=['D','H']):
    if freq=='D':
        cadenza = 1
    elif freq=='H':
        cadenza = 24
    else:
        raise Exception('Frequenza errata, valido solo D oppure H.')
    num_periods = (366 if (year in [2012, 2016, 2020]) else 365)*cadenza
    rif_num_staz = pd.Series(int(stazione_scelta), index=range(num_periods))
    if freq=='D':
        rif_time_inizio = pd.Series(pd.date_range(start=str(year)+'/01/01', periods=num_periods, freq=freq))
        rif_time_fine =pd.Series(pd.date_range(start=str(year)+'/01/02', periods=num_periods, freq=freq))
        rif_dict = {'DATA_INIZIO':rif_time_inizio, 'DATA_FINE':rif_time_fine, 'COD_STAZ':rif_num_staz}
        rif_df = pd.DataFrame(data=rif_dict)
    elif freq=='H':
        rif_time_inizio = pd.Series(pd.date_range(start=str(year)+'/01/01 00:00:00', periods=num_periods, freq=freq))
        rif_time_fine =pd.Series(pd.date_range(start=str(year)+'/01/01 01:00:00', periods=num_periods, freq=freq))
        rif_dict = {'DATA_INIZIO':rif_time_inizio, 'DATA_FINE':rif_time_fine, 'COD_STAZ':rif_num_staz}
        rif_df = pd.DataFrame(data=rif_dict)
    else:
        raise Exception('Frequenza errata, valido solo D oppure H.')
    return rif_df

#LOAD THE DATA
#solo valori day, molto veloce
for station in range(0, len(Cod_staz)):
    stazione_scelta = Cod_staz[station]
    risultato_day = pd.DataFrame()
    for year in range(2010, 2022):
        rif_df_day = create_rif_serie(stazione_scelta, year, freq='D')
        for index in index_inq_day:
            nome_file_import = path + "/CSV Stazione_Parametro_AnnoMese/storico_"+str(year)+'_'+stazione_scelta+'_'+IdParametro[index]+'.csv'
            if not os.path.exists(nome_file_import):
                continue
            my_data = pd.read_csv(nome_file_import, parse_dates=[1, 2], dayfirst=True, usecols=[0,2,3,4])
            my_data.rename(columns={'VALORE':'INQ_'+IdParametro[index]}, inplace=True)
            rif_df_day = pd.merge(rif_df_day, my_data, on=['COD_STAZ', 'DATA_INIZIO', 'DATA_FINE'], how='left')
        risultato_day = pd.concat([risultato_day, rif_df_day])
    risultato_day.to_csv(path + "/CSV Stazione_Parametro_AnnoMese/DAY/"+stazione_scelta+'_day.csv', index=False)

#solo valori hour, lento
for station in range(0, len(Cod_staz)):
    stazione_scelta = Cod_staz[station]
    risultato_hour = pd.DataFrame()
    for year in range(2010, 2022):
        rif_df_hour = create_rif_serie(stazione_scelta, year, freq='H')
        for index in index_inq_hour:
            nome_file_import = path + "/CSV Stazione_Parametro_AnnoMese/storico_"+str(year)+'_'+stazione_scelta+'_'+IdParametro[index]+'.csv'
            if not os.path.exists(nome_file_import):
                continue
            my_data = pd.read_csv(nome_file_import, parse_dates=[1, 2], dayfirst=True, usecols=[0,2,3,4])
            my_data.rename(columns={'VALORE':'INQ_'+IdParametro[index]}, inplace=True)
            rif_df_hour = pd.merge(rif_df_hour, my_data, on=['COD_STAZ', 'DATA_INIZIO', 'DATA_FINE'], how='left')
        risultato_hour = pd.concat([risultato_hour, rif_df_hour])
    risultato_hour.to_csv(path + "/CSV Stazione_Parametro_AnnoMese/HOUR/"+stazione_scelta+'_hour.csv', index=False)

print("--- %s seconds ---" % (time.time() - start_time))