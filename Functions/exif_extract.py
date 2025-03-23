import pathlib

from exiftool import ExifToolHelper, ExifTool
import os
from urllib.parse import urlparse
from pathlib import Path
import shlex

# ------Variablen------
# picture_name_iphone = Path(url).stem  # Quelle: https://stackoverflow.com/questions/678236/how-do-i-get-the-filename-without-the-extension-from-a-path-in-python
# output_path_iphone = f"C:/Users/Diren/Tiefenkarten/{picture_name}_DepthMap.tiff"  # this will be the same for every picture


# ------Funktionen------

# we will use this function to extract all the metadata from the picture(url) that is inserted
def extract_metadata(url:str):
    with ExifToolHelper() as et:
        for d in et.get_metadata(f"{url}"):
            for k, v in d.items():
                print(f"Dict: {k} = {v}")


def transform_jpeg_to_depthmap_samsungs20(url: str, output_dir: str = None) -> tuple:

    #picture_name = Path(url).stem  # Quelle: https://stackoverflow.com/questions/678236/how-do-i-get-the-filename-without-the-extension-from-a-path-in-python
    #output_path = f"C:/Users/Diren/Code/Tiefenkarten/{picture_name}_DepthMap.tiff"  # this will be the same for every picture

    # Pfade und Verzeichnisse vorbereiten
    input_path = Path(url)
    if not input_path.exists():
        raise FileNotFoundError(f"Die Datei {url} existiert nicht.")

    picture_name = input_path.stem
    output_dir = Path(output_dir or "SamsungTiefenkarten")
    #output_dir.mkdir(parents=True, exist_ok=True)  # Zielordner erstellen, falls nicht vorhanden
    output_path = output_dir / f"{picture_name}_DepthMap.jpg"

    file_exists = pathlib.Path.exists(output_path)

    if file_exists == False:
        # ExifTool verwenden, um die Tiefenkarte zu extrahieren
        try:
            with ExifTool() as et:
                et.execute("-b", "-DepthMapTiff", str(input_path), raw_bytes=True)
                binary_data = et.last_stdout
        except Exception as e:
            raise RuntimeError(f"Fehler beim Ausführen von ExifTool: {e}")

        # Überprüfen, ob Daten extrahiert wurden
        if binary_data:
            try:
                with open(output_path, "wb") as f:
                    f.write(binary_data)
                print(f"Tiefenkarte erfolgreich gespeichert: {output_path}")
            except Exception as e:
                raise RuntimeError(f"Fehler beim Schreiben der Tiefenkarte: {e}")
        else:
            print("Keine Tiefenkarte gefunden oder extrahiert.")
            return url, None
    else:
        print("Die Tiefenkarte existiert bereits")

    return str(input_path), str(output_path)

def transform_jpeg_to_depthmap_iphone(url: str, output_dir: str = None) -> tuple:

    # Pfade und Verzeichnisse vorbereiten
    input_path = Path(url)
    if not input_path.exists():
        raise FileNotFoundError(f"Die Datei {url} existiert nicht.")

    picture_name = input_path.stem
    output_dir = Path(output_dir or "IPhoneTiefenkarten")
    #output_dir.mkdir(parents=True, exist_ok=True)  # Zielordner erstellen, falls nicht vorhanden
    output_path = output_dir / f"{picture_name}_DepthMap.png"

    file_exists = pathlib.Path.exists(output_path)
    print(file_exists)

    if file_exists == False:
        # ExifTool verwenden, um die Tiefenkarte zu extrahieren
        try:
            with ExifTool() as et:
                et.execute("-b", "-MPImage3", str(input_path), raw_bytes=True)
                binary_data = et.last_stdout
        except Exception as e:
            raise RuntimeError(f"Fehler beim Ausführen von ExifTool: {e}")

        # Überprüfen, ob Daten extrahiert wurden
        if binary_data:
            try:
                with open(output_path, "wb") as f:
                    f.write(binary_data)
                print(f"Tiefenkarte erfolgreich gespeichert: {output_path}")
            except Exception as e:
                raise RuntimeError(f"Fehler beim Schreiben der Tiefenkarte: {e}")
        else:
            print("Keine Tiefenkarte gefunden oder extrahiert.")
            return url, None
    else:
        print("Die Tiefenkarte existiert bereits")

    return str(input_path), str(output_path)


# ------Aufruf von Funktionen------
