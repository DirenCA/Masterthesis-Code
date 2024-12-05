from PIL import Image
import tifffile as tiff

# TIFF-Datei laden
depth_map = Image.open(r"C:\Users\Diren\exiftool\test2.tiff")
print(type(depth_map))
