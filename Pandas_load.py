#TODO ci sono delle etichette TIPO_STAZ che sono "nan" ---> guess them!
import pandas as pd
import numpy as np
import glob
import os
import time

#NECESSARIO AVERE UNA CERTA "FOLDER ORGANIZATION"
#LOAD THE LOOK UP TABLES

start_time = time.time()


path = os.getcwd()
params_lut = pd.read_excel(path+'/parametri.xlsx')
stations_lut = pd.read_excel(path+'/QARIA_Stazioni.xlsx')
Cod_staz = stations_lut['Cod_staz'].unique()
Cod_staz = np.sort(Cod_staz)
#Cod_staz: <class 'numpy.ndarray'> pieno di <class 'numpy.int64'> lunghi 7 o 8 cifre
IdParametro = params_lut['IdParametro'].unique()
IdParametro = np.sort(IdParametro)
#IdParametro: <class 'numpy.ndarray'> pieno di <class 'numpy.float64'> lunghi 1 o 3 cifre (con punto perché float)

#LOAD THE DATA
multidim_list = []
anno = 2009
for year in range(12):
    anno += 1
    multidim_list.append([])
    for station in range(54):
        stazione_scelta = Cod_staz[station] #<class 'numpy.int64'> lunghi 7 o 8 cifre
        multidim_list[year].append([])
        contatore_inq = 0
        for inquinante in range(21):
            inq_scelto = int(IdParametro[inquinante])
            stazione_scelta_str = str(stazione_scelta)
            stazione_scelta_str = stazione_scelta_str.rjust(8, '0')
            inq_scelto_str = str(inq_scelto)
            inq_scelto_str = inq_scelto_str.rjust(3, '0')
            nome_file_import = path + "/CSV Stazione_Parametro_AnnoMese/storico_"+str(anno)+'_'+stazione_scelta_str+'_'+inq_scelto_str+'.csv'
            if not os.path.exists(nome_file_import):
                continue
            my_data = pd.read_csv(nome_file_import, header = 0)
            multidim_list[year][station].append([])
            multidim_list[year][station][contatore_inq] = my_data
            contatore_inq += 1

print("--- %s seconds ---" % (time.time() - start_time))