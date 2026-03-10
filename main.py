import pandas as pd

#Cargar el archivo csv
fileInput = "Series.csv"
outputFile = "episodes_clean.csv"

df = pd.read_csv(fileInput,delimiter=',')

for i, row in df.iterrows():
    if type(row["SeriesName"]) != str or row["SeriesName"] is None:
        continue
    else:
        print(row["SeriesName"].strip().lower().replace(" ",""))



#Mostrar las primeras lineas del archivo
#print(df.head())


