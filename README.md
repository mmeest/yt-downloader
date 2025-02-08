﻿# YTD

Python: Kõigepealt peab kasutaja oma arvutisse paigaldama Python (soovitavalt Python 3.x versiooni), kuna see on programmi tööks vajalik.

yt-dlp: Kuna kasutate yt-dlp teeki YouTube'i videote allalaadimiseks, peab see olema paigaldatud. Selle saab paigaldada järgmise käsu abil:

```
pip install yt-dlp
```

FFmpeg: Kui videosse on sisseehitatud mitu meediumivoogu (nt video ja heli eraldi), siis on FFmpeg vajalik, et neid ühendada. Kui teie süsteemis ei ole FFmpeg installitud, siis võib programm hakata teavitama, et vajab FFmpeg-i. FFmpeg-i saab paigaldada järgmistel viisidel:

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
