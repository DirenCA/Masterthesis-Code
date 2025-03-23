# 📘 Masterarbeit – *Volumenbestimmung von Lebensmitteln mittels Computer Vision*

## ✍️ Autor

    Name: Diren Can Akkaya

    Hochschule: Hochschule für Technik und Wirtschaft Berlin

    Erstgutachter: Prof. Dr. Martin Spott

    Zweitgutachter: Prof. Dr.-Ing. Ingo Claßen

    Abgabedatum: 26.03.2025

## 📌 Überblick

Kurze Beschreibung der Masterarbeit:  
- Thema:
Die Arbeit befasst sich mit der Volumenschätzung von Lebensmitteln auf Basis von Tiefendaten, die mit einem Smartphone erfasst werden. Zum Einsatz kommt dabei ein iPhone 16 Pro Max, dessen Tiefendaten in Punktwolken umgewandelt und anschließend zur Volumenberechnung genutzt werden. Ziel ist es, verschiedene Methoden wie Convex Hull, Alpha Shapes, Voxelization und Oriented Bounding Box hinsichtlich ihrer Eignung zu untersuchen.
- Zielsetzung:
Ziel der Arbeit ist es, ein Verfahren zur Volumenberechnung basierend auf Daten von mobilen Geräten zu entwickeln und zu evaluieren. Dabei wird untersucht, wie genau und zuverlässig die jeweiligen Berechnungsmethoden arbeiten und welche Faktoren die Ergebnisse beeinflussen.

## 🗂️ Projektstruktur

```plaintext
📁 AppleSDKCode/     # Hier befidnet sich die CameraController-Klasse und die von mir hinzugefügten Funktionen
📁 Data/             # Hier liegen alle genutzten Daten
├── LidarData/       # Alle Tiefen- und Bilddaten der Lebensmittel
│   └── [Ordner mit .bin und .jpg für jedes Lebensmittel]
├── camera_intrinsics.json      # Die genutzte intrinsische Matrix
└── Zusammenfassung Daten.xlsx  # Hier stehen die erfassten Daten, die zur Analyse genutzt wurden
📁 DeprecatedCode    # Veraltete und archivierte Notebooks oder Skripte
├── FoodClassification.ipynb    # Ansatz, um ein Segmentierungsmodell auf den Food103-Datensatz zu trainieren
├── testing.py                  # Hier habe ich Code vor der Implementierung im Notebbook getestet 
├── Testing and analyzing_20250124.ipynb    # Spezieller Fokus das Entzerren der Bilder
├── ValueEstBinary.ipynb    # Erster Ansatz, um binäre Daten in Tiefenkarten umzuwandeln
├── ValueEstBinary_withBottomEdgeFunction.ipynb # Erster Ansatz, um die Punktwolken auszufüllen
└── VolumeEstimation.ipynb # Veraltete Implementierung in der viele Funktionen fehlen
📁 Functions/           # In dem Ordner werden die Funktionen gesammelt, die für die Anwendung geschrieben wurden
├── camera_intrinsic.py    # Funktion aus OpenCV, um die intrinsische Matrix der Kamera zu erhalten (Wird nicht genutzt in der finalen Impelementierung)
├── exif_extract.py        # Enthält Funktionen, um das ExifTool zu nutzen für das Extrahieren der Tiefenkarte aus einem Bild (Wird nicht genutzt in der finalen Impelementierung)
├── processing_depthmap_pc.py    # Enthält Funktion, um die binären Daten umzuwandeln und die Punktwolke auszufüllen
└── volume_estimation.py         # Enthält Funktionen, die die Implementierung der Volumschätzungsmethoden vereinfacht
📁 Notebooks/             # In dem Ordner liegen die finalen Notebooks
├── Dataanalysis.ipynb    # Für die Analse der Ergebnisse
├── ValueEst_Plane.ipynb  # Implementierung ohne Segmentierung durch R-CNN. Reine Nutztung von RANSAC und SOR.
└── ValueEst_Seg.ipynb          # Das ist die final genutzte Implementierung, die auch die Segmentierung mit R-CNN nutzt.
📄 requirements.txt  # Python-Abhängigkeiten
```


## ⚙️ Setup & Installation


1. Repository klonen  
```
git clone https://github.com/DirenCA/Masterthesis-Code
cd Masterthesis-Code
```
2. Abhängigkeiten installieren
```
pip install -r requirements.txt
```

## 🚀 Nutzung

- `Notebooks/ValueEst_Seg.ipynb`: Hauptnotebook mit Segmentierung mit R-CNN und Volumenschätzung  
- `Notebooks/Dataanalysis.ipynb`: Analyse der Schätzgenauigkeit  
- Beschreibung:
  - Die Nutzung des Notebooks ist einfach gestaltet und benötigt die binäre Datei aus Data/LidarData. Hier kann das Lebensmittel ausgewählt werden und die Datei als Pfad übergeben werden.
    Bspw. "Data\BinaryLidarData\Mango\DepthMap.bin". Zusätzlich muss für die Segmentierung das Farbbild angegeben werden "Data\BinaryLidarData\Mango\color_image.jpg". Der Code kann ab dann einfach ausgeführt werden.
  - **Hinweis!:** 
    - Die Volumenschätzung und damit der Abschnitt *Volumenschätzung mehrerer Objekte* funktioniert nur, wenn die Masken aus "Smallest Mask" und "Best Mask" manuell parametrisiert werden.
    - Der Abschnitt *Test* ist für die eigentliche Umsetzung nicht relevant, sondern besitzt die Funktion, um Punktwolken zu speichern und die spezifischen Methoden, um das Reis-Objekt zu segmentieren.
  
## 🌐 Quellen
- https://stackoverflow.com/questions/678236/how-do-i-get-the-filename-without-the-extension-from-a-path-in-python
- https://sylikc.github.io/pyexiftool/index.html
- https://stackoverflow.com/questions/63587617/how-to-create-a-rgbd-image-from-numpy-rgb-array-and-depth-array
- https://numpy.org/doc/stable/
- https://www.open3d.org/docs/release/
- https://docs.opencv.org/4.x/
- https://pytorch.org/docs/stable/index.html
- https://stackoverflow.com/a/67346474
- https://stackoverflow.com/questions/73067231/how-to-convert-uint8-image-to-uint16-python
- https://stackoverflow.com/questions/65774814/adding-new-points-to-point-cloud-in-real-time-open3d
- https://stackoverflow.com/questions/1406029/how-to-calculate-the-volume-of-a-3d-mesh-object-the-surface-of-which-is-made-up