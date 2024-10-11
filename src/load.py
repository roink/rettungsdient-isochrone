from src.download import download_and_unzip
import pandas as pd
import os


def load_Hauskoordinaten():
    download_and_unzip('Hauskoordinaten')
    current_dir = os.getcwd()
    raw_data_dir = os.path.join(os.path.dirname(current_dir), "data", "raw")
    
    file_path = os.path.join(os.path.dirname(current_dir), "data", "raw", "Hauskoordinaten.csv")
    df = pd.read_csv(file_path,encoding='iso-8859-15', sep=';')
    columns_to_drop = ["Stand: 28.09.2024", "URL", "Unnamed: 17"]
    df = df.drop(columns=columns_to_drop, errors='ignore')
    
    return df
    