from exiftool import ExifToolHelper, ExifTool
import os
from urllib.parse import urlparse
from pathlib import Path
import shlex

# ------Variablen------
#url_iphone = r"C:\Users\Diren\Nextcloud\HTW\4.Semester-Masterarbeit\Masterarbeit\Code\TestBilder\ja.jpg"  # maybe change the way we add the url in the future -> make it easier to use other images
# picture_name_iphone = Path(url).stem  # Quelle: https://stackoverflow.com/questions/678236/how-do-i-get-the-filename-without-the-extension-from-a-path-in-python
# output_path_iphone = f"C:/Users/Diren/Nextcloud/HTW/4.Semester-Masterarbeit/Masterarbeit/Code/Tiefenkarten/{picture_name}_DepthMap.tiff"  # this will be the same for every picture


# ------Funktionen------

# we will use this function to extract all the metadata from the picture(url) that is inserted
def extract_metadata(url:str):
    with ExifToolHelper() as et:
        for d in et.get_metadata(f"{url}"):
            for k, v in d.items():
                print(f"Dict: {k} = {v}")


def transform_jpeg_to_depthmap_samsungs20(url: str, output_dir: str = None) -> tuple:
    """
        Wandelt ein JPEG-Bild in eine Tiefenkarte um und speichert diese als TIFF-Datei.

        Args:
            url (str): Pfad zur Eingabedatei (JPEG).
            output_dir (str, optional): Zielverzeichnis für die Tiefenkarte. Standardmäßig wird ein Ordner "Tiefenkarten" im aktuellen Arbeitsverzeichnis verwendet.

        Returns:
            tuple: Ursprünglicher Bildpfad und Pfad zur gespeicherten Tiefenkarte.
    """

    #picture_name = Path(url).stem  # Quelle: https://stackoverflow.com/questions/678236/how-do-i-get-the-filename-without-the-extension-from-a-path-in-python
    #output_path = f"C:/Users/Diren/Nextcloud/HTW/4.Semester-Masterarbeit/Masterarbeit/Code/Tiefenkarten/{picture_name}_DepthMap.tiff"  # this will be the same for every picture

    # Pfade und Verzeichnisse vorbereiten
    input_path = Path(url)
    if not input_path.exists():
        raise FileNotFoundError(f"Die Datei {url} existiert nicht.")

    picture_name = input_path.stem
    output_dir = Path(output_dir or "SamsungTiefenkarten")
    output_dir.mkdir(parents=True, exist_ok=True)  # Zielordner erstellen, falls nicht vorhanden
    output_path = output_dir / f"{picture_name}_DepthMap.tiff"

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

    return str(input_path), str(output_path)

def transform_jpeg_to_depthmap_iphone(url: str, output_dir: str = None) -> tuple:

    # Pfade und Verzeichnisse vorbereiten
    input_path = Path(url)
    if not input_path.exists():
        raise FileNotFoundError(f"Die Datei {url} existiert nicht.")

    picture_name = input_path.stem
    output_dir = Path(output_dir or "IPhoneTiefenkarten")
    output_dir.mkdir(parents=True, exist_ok=True)  # Zielordner erstellen, falls nicht vorhanden
    output_path = output_dir / f"{picture_name}_DepthMap.jpg"

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

    return str(input_path), str(output_path)


# ------Aufruf von Funktionen------
url = r"C:\Users\Diren\Nextcloud\HTW\4.Semester-Masterarbeit\Masterarbeit\Code\SamsungTestBilder\20250105_164600.jpg"
output_dir = r"C:\Users\Diren\Nextcloud\HTW\4.Semester-Masterarbeit\Masterarbeit\Code\Tiefenkarten"

url_iphone = r"C:\Users\Diren\Nextcloud\HTW\4.Semester-Masterarbeit\Masterarbeit\Code\IphoneTestBilder\IMG_8173.jpg"
output_dir_iphone = r"C:\Users\Diren\Nextcloud\HTW\4.Semester-Masterarbeit\Masterarbeit\Code\IPhoneTiefenkarten"

input_path, output_path = transform_jpeg_to_depthmap_samsungs20(url, output_dir)

input_path_iphone, output_path_iphone = transform_jpeg_to_depthmap_iphone(url_iphone, output_dir_iphone)
