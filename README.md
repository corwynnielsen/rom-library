# ROM Library for Emudeck + Emulation Station

Emudeck with Emulation Station must be installed first.

### Prerequisites before running the python script:

1. Go to Desktop mode
2. Open Konsole
3. Check that Python is installed:

```
python -V
```

4. Clone the repository:

```
git clone https://github.com/corwynnielsen/rom-library.git && cd rom-library
```

5. Create and source Python venv:

```
python -m venv venv && source venv/bin/activate
```

6. Install required libraries to venv:

```
python -m pip install -r requirements.txt
```

### Once the libraries are successfully installed, you can run the python script in Konsole.

```
python rom-library.py
```

After running the script, the ROM Library will be available as a new Emulator in Emulation Station. When a ROM is selected from the ROM Library, the screen will turn black while the ROM downloads. Once the download completes, it will be placed in the appropriate roms folder and can be played.
<br />
<br />
NOTE: Make sure to change the "XXXXXX" with the correct URLs in the python script.
