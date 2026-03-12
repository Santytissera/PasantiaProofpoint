import pandas as pd
import datetime


def normalize_csv(fileinput):
    df = pd.read_csv(fileinput)

    referencia = set()
    referencia2 = set()
    referencia3 = set()

    Snumber = pd.to_numeric(df["SeasonNumber"],"coerce")
    df["SeasonNumber"] = (Snumber.where(Snumber % 1 == 0).fillna(0).clip(lower=0).astype(int))
    Enumber = pd.to_numeric(df["EpisodeNumber"],"coerce")
    df["EpisodeNumber"] = (Enumber.where(Enumber % 1 == 0).fillna(0).clip(lower=0).astype(int))
    df["AirDate"] = pd.to_datetime(df["AirDate"],format="%Y-%m-%d",errors="coerce")
    df["AirDate"] = df["AirDate"].dt.strftime("%Y-%m-%d")
    
    valid_rows=[]
    for i,row in df.iterrows():
        
    #Validacion de nombres de series
        if not isinstance(row["SeriesName"],str):
            continue
        else:
            row["SeriesName"] = (row["SeriesName"].strip()
                                .lower()
                                .replace(" ","")
                                .encode("ascii","ignore")
                                .decode("utf-8"))  
    #Validacion de Nombre de episodio
        if not isinstance(row["EpisodeTitle"],str):
            row["EpisodeTitle"] = "Untitled Episode"
        else:
            row["EpisodeTitle"] = (row["EpisodeTitle"].strip()
                                .lower()
                                .replace(" ", "")
                                .encode("ascii", "ignore")
                                .decode("utf-8"))
    #Validacion de fecha de emision
        if not isinstance(row["AirDate"],str):
            row["AirDate"]  = "Unknown"

        key1 = (row["SeriesName"],row["SeasonNumber"],row["EpisodeNumber"])
        key2 = (row["SeriesName"],0,row["EpisodeNumber"],row["EpisodeTitle"])
        key3 = (row["SeriesName"],row["SeasonNumber"],0,row["EpisodeTitle"])

        if (key1 not in referencia) or (key2 not in referencia2) or (key3 not in referencia3):
            valid_rows.append(row)

        referencia.add(key1)
        referencia2.add(key2)
        referencia3.add(key3)

        
    return valid_rows



def main():
    fileinput = "PythonProject\data\Series.csv"
    fileoutput = "PythonProject\data\Episodes_clean.csv"
    
    norma = normalize_csv(fileinput)

    print(norma)
    #    df_valid = pd.DataFrame(validcsv)
    #    df_valid.to_csv(fileoutput,index=False)

main()