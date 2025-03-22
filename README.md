# Masterthesis-Code
#Quellen für den Code:
https://stackoverflow.com/questions/678236/how-do-i-get-the-filename-without-the-extension-from-a-path-in-python
https://sylikc.github.io/pyexiftool/index.html

## Beschreibung der Files, Skripte, Notebooks, etc.:
- *testing.py*: Hier teste ich generelle Ideen und Funktionen
- *Testing and analyzing.ipynb*: In diesem Notebook werde ich Plots und Visualisierungen einfügen, damit ich diese in bspw. testing.py nicht auskommentieren muss oder immer wieder plotte.

# 📘 Masterarbeit – *Titel deiner Arbeit*

## ✍️ Autor

    Name: Diren Can Akkaya

    Hochschule: Hochschule für Technik und Wirtschaft Berlin

    Erstgutachter: Prof. Dr. Martin Spott

    Zweitgutachter: Prof. Dr.-Ing. Ingo Claßen

    Abgabedatum: 26.03.2025

## 🧠 Überblick

Kurze Beschreibung der Masterarbeit:  
- Thema  
- Zielsetzung  
- Relevanz / Problemstellung  

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
├── Testing and analyzing_20250124.ipynb    # Altes Notebook: Spezieller Fokus das Entzerren der Bilder
└── ValueEstBinary.ipynb    # Altes Notebook: Spezieller Fokus 
📁 models/           # (Optional) gespeicherte Modelle oder Trainingsdaten
📄 requirements.txt  # Python-Abhängigkeiten
📄 main.py           # Einstiegspunkt des Projekts
