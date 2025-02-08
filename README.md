# YTD


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