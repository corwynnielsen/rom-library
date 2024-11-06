# ROM Library for Emulation Station

You must have Emulation Station installed first

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

After running the script, open Steam in Desktop mode or go back to Game mode, then run Emulation Station. You will now see "ROM Library" in the main menu.<br />
<br />
NOTE: Make sure to change the "XXXXXX" with the correct URLs in the python script.
