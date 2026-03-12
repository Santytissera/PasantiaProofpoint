import pandas as pd
import unicodedata

#Funcion para eliminar los acentos  del texto
def normalize_text(text):
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("utf-8")
    return text

def normalize_csv(df):

    inputRecord = len(df)
    discardEntry = 0
    correctedEntry = 0

# Normalizar Columnas de texto series name
    df["SeriesName"] = (df["SeriesName"].fillna("").str.strip().
                                str.lower().
                                str.replace(" ","")
                                .apply(normalize_text)
                                .str.replace(r"[^a-z0-9 ]","",regex=True))
    df = df[df["SeriesName"] != ""]
#Normalizar columnas de numeros
    Sea_number = pd.to_numeric(df["SeasonNumber"],"coerce")
    df["SeasonNumber"] = (Sea_number.where(Sea_number % 1 == 0).fillna(0).clip(lower=0).astype(int))

    Epi_number = pd.to_numeric(df["EpisodeNumber"],"coerce")
    df["EpisodeNumber"] = (Epi_number.where(Epi_number % 1 == 0).fillna(0).clip(lower=0).astype(int))

#Normalizar episodios
    df["EpisodeTitle"] = (df["EpisodeTitle"].fillna("").
                                replace("", "Untitled Episode").
                                str.strip().
                                str.lower().
                                replace(r"[^a-z0-9 ]","",regex=True).
                                apply(normalize_text).
                                str.encode("ascii","ignore").
                                str.decode("utf-8"))
    df = df[df["EpisodeTitle"] != ""]
#    df["EpisodeTitle"] = df["EpisodeTitle"].fillna("").replace("","Untitled Episode")

#Normalizar fechas
    df["AirDate"] = pd.to_datetime(df["AirDate"],format="%Y-%m-%d",errors="coerce")
    df["AirDate"] = df["AirDate"].dt.strftime("%Y-%m-%d")
    df["AirDate"] = df["AirDate"].fillna("").str.strip().replace("","Unknown")

#Contar entradas descartadas y entradas corregidas
    for i,row in df.iterrows():
        if not isinstance(row["SeriesName"],str):
            discardEntry += 1
            continue
        else:
            correctedEntry += 1
#Eliminar filas que no tienen SerieName
    df = df.dropna(subset=["SeriesName"])

    return df, inputRecord, discardEntry, correctedEntry


def elimin_duplicates(df):
#Filas de validacion para crear puntaje
    df["validDate"] = df["AirDate"].str.lower() != "Unknown"
    df["validEpisode"] = df["EpisodeTitle"].str.lower() != "Untitled Episode"
    df["validSeason"] = df["SeasonNumber"] > 0
    df["validEpisodeNumber"] = df["EpisodeNumber"] > 0

#Fila que otoga puntaje segun informacion perdida
    df["score"] = (
        df["validDate"].astype(int) * 4 +
        df["validEpisode"].astype(int) * 3 +
        df["validSeason"].astype(int) * 2 +
        df["validEpisodeNumber"].astype(int) * 1
    )

    df = df.sort_values(by="score", ascending=False)
#contar cantidad de registros antes y dps de eliminar filas duplicadas
    before = len(df)
    outputrec = 0

#Rule1 para deteccion de duplicados
    df = df.drop_duplicates(subset=["SeriesName","SeasonNumber","EpisodeNumber"], keep="first")

#Rule2
    mask = df["SeasonNumber"] == 0
    df_season0 = df[mask].drop_duplicates(subset=["SeriesName","EpisodeNumber","EpisodeTitle"], keep="first")
    df_rest = df[~mask]

    df = pd.concat([df_rest, df_season0])

#Rule3
    mask = df["EpisodeNumber"] == 0
    df_season0 = df[mask].drop_duplicates(subset=["SeriesName","SeasonNumber","EpisodeTitle"], keep="first")
    df_rest = df[~mask]

    df = pd.concat([df_rest, df_season0])

    df = df.drop(columns = ["validDate","validEpisode","validSeason","validEpisodeNumber","score"])

    duplicated_entries = before - len(df)
    for i, row in df.iterrows():
        outputrec +=1

    return df,duplicated_entries,outputrec


def generateReport(reportfile,inputrec,outputrec, discardentry, correctedentry, duplicated_entries):
    with open(reportfile,"w") as file:
        file.write("#Data Quality Report \n\n")
        file.write(f"Input Records: {inputrec}\n")
        file.write(f"Output Records: {outputrec}\n")
        file.write(f"Discarded Entries: {discardentry}\n")
        file.write(f"Corrected Entries: {correctedentry}\n")
        file.write(f"Duplicated Entries: {duplicated_entries}\n")
        file.write(f"Method used to remove duplicates: \n"
                   f"Once the data frame fields are normalized, i added a score column to each row.\n"
                   f" This column indicates whether all fields are valid or if some have missing data.\n"
                   f"i then sorted the rows from lowest to highest score to keep the first record that meets all the requirements.\n"
                   f"Next, i created the comparison rules to detect duplicates:\n"
                   f"Rule1: (Normalized Series Name, Season Number, Episode Number)\n"
                   f"Rule2: (Normalized Series Name, 0, Episode Number, Normalized Episode Title)\n"
                   f"Rule3: (Normalized Series Name, Season Number, 0, Normalized Episode Title)\n"
                   f"For each rule, i removed the record that met the condition and had the lowest score.\n"
                   f"For rules 2 and 3, which state that Season Number or Episode Number must be 0\n"
                   f"i used a variable 'mask' and compared the records that had that column set to 0.\n"
                   f"This is because if i included 0 within the subset, the program might interpret 0 as empty or invalid.\n"
                   f"Then i removed the added auxiliary columns.\n")


    return reportfile




def main():
    fileinput = "data/Series.csv"
    fileoutput = "data/Episodes_clean.csv"
    reportfile = "data/report.md"

    df = pd.read_csv(fileinput)
#funcion que normaliza las filas del dataframe
    normalized_Df,inputrec,discardentry,correctedentry = normalize_csv(df)

#funcion que elimina los duplicados del dataframe
    df_valid,duplicated_entries,outputrec = elimin_duplicates(normalized_Df)

#Funcion que genera el reporte de calidad
    generateReport(reportfile,inputrec,outputrec,discardentry,correctedentry,duplicated_entries)

    valid_fileoutput = pd.DataFrame(df_valid)
    valid_fileoutput.to_csv(fileoutput,index=False)

main()