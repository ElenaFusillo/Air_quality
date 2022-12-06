import pandas as pd
import glob
import os

# Get CSV files list from a folder
path = 'C:/Users/Elena/Documents/UNIVERSITA/2_Pattern Recognition/Project_exam/Air_quality/CSV Stazione_Parametro_AnnoMese'
all_files = glob.glob(path + "/*.csv")
#lista di stringhe lunga 2702