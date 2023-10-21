# RTL SDR - NF S 32002

Réimplémentation du protocole NF S 32002 utilisé par les balises sonores des feux piétons. Permet de détecter le signal d'une télécommande à partir d'un RTL SDR.

## Installer la librairie

Il faut tout d'abord installer librtlsdr utilisé pour communiquer avec le RTL SDR. 

Sous Debian/Ubuntu:

```bash
sudo apt install librtlsdr
```

Sous macOS avec Homebrew:

```bash
brew install librtlsdr
```

Puis installer la librairie depuis Pypi:

```bash
pip install rtlsdr-nfs32002
```

## Utiliser la librairie

Importer le module protocol:

```python
from rtlsdr_nfs32002.protocol import *
```

Créer une fonction qui sera appelée lors de la détection d'une télécommande :

```python
def detect():
    print("Ouistici !")
```

Instancier la classe RtlSdr_NFS3200 puis appeler la méthode startDetection en lui indiquant en paramètre la fonction à appeler lors de la détection.

```python
sdr = RtlSdr_NFS32002()
sdr.startDetection(callback=detect)
```
ou :
```python
sdr = RtlSdr_NFS32002()
sdr.startDetection(callback=detect, simple_detect=True)
```
