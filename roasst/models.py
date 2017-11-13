import pandas as pd

from roasst.configs import DATA_FOLDER_PATH


df_acr_large = pd.read_csv(DATA_FOLDER_PATH + '/df_acr_small.csv')
df_acr_large = pd.read_csv(DATA_FOLDER_PATH + '/df_acr_large.csv')
