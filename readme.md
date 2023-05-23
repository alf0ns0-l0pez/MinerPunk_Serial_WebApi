# MINER PUNK - Serial Web Api
![logo](https://raw.githubusercontent.com/alf0ns0-l0pez/MinerPunk_Serial_WebApi/main/img/logo_corn.png)
## Introduction
---
### Serial Web Api is a web service code developed to gave web access to multiples serial ports which are connect to **The MinerPunk Boards** and so through web requests handle peripherals.

## Dependencies
---
### You can take a look in the file **requirements.txt** which is attached in this project to know every library used in this App. 

### To install in a virtual environment in your current project:
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
## Setup
---
### There is a file named startup.yaml where the main settings are located, the following are the most important parameters:
* Ip Address and Port.
    ```yaml
    #Web server setup
    app:
        ipaddr: 'localhost'
        port: 9000
    ```
* It is necessary to add every serial port that our boards are using in the next list, ***Note. do not add ports that we are not using!.***
    ```yaml
    serialport:
        timeout : 5
        baudrate : 115200
        ports :
          - 'COM6' #Board 1
          - 'COM7' #Board 2
    ```
## Usage Example
---
### **Python Example:**
### If you wish to test it, there is an example named **example/app_test.py** which makes a request to one of our web apis http://localhost:9000/get_complete and returns the next.
```json
{
	"data": {
		"description": {
			"BOARD": "RELAY_MATRIX",
			"SUPPLIER": "MINERPUNK",
			"VERSION": "1.1"
		},
		"inputs": {
			"INP_OPT1": false,
			"INP_OPT2": false,
			"INP_OPT3": false,
			"INP_OPT4": false
		},
		"outputs": {
			"OUT_REL1": false,
			"OUT_REL2": true,
			"OUT_REL3": true,
			"OUT_REL4": false,
			"OUT_REL5": true,
			"OUT_REL6": false,
			"OUT_REL7": true,
			"OUT_REL8": true
		},
		"receive": [],
		"status": true
	},
	"status": true
}
```
### **Using Insomnia:**
### This Repository counts with a **Request Collection**, using this tool you be able to interact with the Web Apis.
* First of all, Insomia installed is required, [DOWNLOAD PAGE](https://insomnia.rest/download)
* Then import the file **Insomnia.json** to open our **Request Collection**.
* Now you can test each of our Web Apis.
#### ***Example Gif***
![insomnia_example](https://raw.githubusercontent.com/alf0ns0-l0pez/MinerPunk_Serial_WebApi/main/img/insomnia_example.gif)