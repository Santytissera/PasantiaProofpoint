import pandas as pd
import datetime

fileinput = "Series.csv"
fileoutput = "Episodes_clean.csv"

df = pd.read_csv(fileinput)

valid_rows = []

df["SeasonNumber"] = (pd.to_numeric(df["SeasonNumber"],"coerce").fillna(0).clip(lower=0).astype(int))
df["EpisodeNumber"] = (pd.to_numeric(df["EpisodeNumber"],"coerce").fillna(0).clip(lower=0).astype(int))
df["AirDate"] = pd.to_datetime(df["AirDate"],format="%Y-%m-%d",errors="coerce")
df["AirDate"] = df["AirDate"].dt.strftime("%Y-%m-%d")

lastRow = None
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

    if not isinstance(row["EpisodeTitle"],str):
        row["EpisodeTitle"] = "Untitled Episode"
    else:
        row["EpisodeTitle"] = (row["EpisodeTitle"].strip()
                             .lower()
                             .replace(" ", "")
                             .encode("ascii", "ignore")
                             .decode("utf-8"))
    if not isinstance(row["AirDate"],str):
        row["AirDate"]  = "Unknown"

    if lastRow is not None:
        if row["SeriesName"] == lastRow["SeriesName"]:

            print("Fila Duplicada")

    lastRow = row

#    valid_rows.append(row)
#df_valid = pd.DataFrame(valid_rows)
#df_valid.to_csv(fileoutput,index=False)

#print(valid_rows)