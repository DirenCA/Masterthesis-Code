from exiftool import ExifToolHelper, ExifTool
import os
from urllib.parse import urlparse
from pathlib import Path
import shlex

# ------Variablen------
url = r"C:\Users\Diren\Nextcloud\HTW\4.Semester-Masterarbeit\Masterarbeit\Code\TestBilder\20241207_171339.jpg"  # maybe change the way we add the url in the future -> make it easier to use other images
picture_name = Path(
    url).stem  # Quelle: https://stackoverflow.com/questions/678236/how-do-i-get-the-filename-without-the-extension-from-a-path-in-python
output_path = f"C:/Users/Diren/Nextcloud/HTW/4.Semester-Masterarbeit/Masterarbeit/Code/Tiefenkarten/{picture_name}_DepthMap.tiff"  # this will be the same for every picture


# ------Funktionen------

# we will use this function to extract all the metadata from the picture(url) that is inserted
def extract_metadata(url:str):
    with ExifToolHelper() as et:
        for d in et.get_metadata(f"{url}"):
            for k, v in d.items():
                print(f"Dict: {k} = {v}")


def transform_jpeg_to_depthmap(url:str):
    # Use ExifTool
    with ExifTool() as et:
        et.execute("-b", "-DepthMapTiff", url,
                   raw_bytes=True)  # without "raw_bytes = True" the data would be a string and give us en error while encoding the data
        binary_data = et.last_stdout  # it seems that the direct transformation like in the Shell is not working, so I have to get the raw bytes first

    # Überprüfe, ob Daten extrahiert wurden
    if binary_data:
        with open(output_path, "wb") as f:
            f.write(binary_data)
        print(f"Tiefenkarte wurde erfolgreich in {output_path} gespeichert.")
    else:
        print("Keine Tiefenkarte gefunden oder extrahiert.")


# ------Aufruf von Funktionen------

transform_jpeg_to_depthmap(url)
