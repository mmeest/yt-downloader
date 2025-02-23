# YTY.py -> YTY.exe <- viimane versioon
## Youtube Downloader

Python: Programmi vajab, et oleks paigaldatud Python(soovitavalt Python 3.x)

FFmpeg: Audio ja video striimid liidetakse kokku FFmpeg abil. 
Seega kasutuseks vajalik paigaldada: https://www.ffmpeg.org/


Enne download'i kontrollitakse faili olemasolu.

---

## Resolutions

* best
* 720p
* 1080p
* 1440p
* 2160p
* worst
* MP3

Videod talletatakse "downloads" kataloogi.  

----
yt-dlp: Rakendus kasutab yt-dlp downloader libraries https://www.pythoncentral.io/yt-dlp-download-youtube-videos/

```
pip install yt-dlp
```

FFmpeg paigaldamine:

    Windows:
        Laadige alla FFmpeg ametlikult veebilehelt: https://ffmpeg.org/download.html.
        Pakkige välja ja lisage FFmpeg-i kaust PATH keskkonnamuutujatesse, et saaksite FFmpeg-i käske terminalis kasutada.

    Linux (Ubuntu):

```
sudo apt update
sudo apt install ffmpeg
```

Mac (Homebrew kasutades):

```
brew install ffmpeg
```
Kui kõik need asjad on paigaldatud ja konfiguratsioonid õiged, siis peaks programm ilma probleemideta töötama!



----

To generate executable

```
python -m PyInstaller --onefile yt.py
```

To generate application that hides terminal window

```
pyinstaller --onefile --windowed yt.py

OR

python -m pyinstaller --onefile --windowed yt.py
```

Or use virtual env:
```
python -m venv venv
venv\Scripts\activate
pip install pyinstaller
pyinstaller --onefile --windowed yt.py
```

From 2024 Youtube does'nt allow high resolution (720p) videos to download with audio.
To overcome it FFmpeg open source software.

FFmpeg homepage: https://ffmpeg.org/download.html

Extract FFmpeg and add path:

system variables > Advanced > User variables > New > C:\ffmpeg\bin


---

Where Python is installed:

```
python -c "import sys; print(sys.executable)"
python -m site --user-site
```

Pyinstaller

If Pyinstaller is correctly installed:

```
pip show pyinstaller
```

Check:

```
where pyinstaller
```

```
python -c "import pyinstaller; print(pyinstaller.__file__)"
```

Reinstall Pyinstaller
```
python -m pip install --upgrade --force-reinstall pyinstaller
```

Add path
```
python -c "import os; print(os.path.dirname(os.__file__))"
```

-------

To change Python site-package:

```
python -c "import site; print(site.getsitepackages())"
```

Add site-package:

```
setx PYTHONPATH "C:\Python39\Lib\site-packages"
```

Install Pyinstaller globally:

```
python -m pip install --force-reinstall pyinstaller
```

test:

```
python -m pyinstaller --version
```
