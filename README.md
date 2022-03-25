# CIPSafety l5x IO viewer
 Extract digitals IO (safety and standard) from a .l5x file

## Requirements
- Python 3.10
- PIP

> See requirements.txt file for the PIP dependencies.

## Run application
To run application with Python run this command :
```Shell
python main.py
```

## Compile Windows .exe file
To compile .exe file run this command :
```Shell
python compile.py
```

## Export pattern
You can use theses four tags in the export window :

- [x] **{byte}** : Represent the BYTE
- [x] **{module}** : Name of the module eg: "Module 00: PSS u2 P0 F/S EIP"
- [x] **{address}** : The bit address eg: ".2"
- [x] **{name}** : The bit name eg: "I 02"

