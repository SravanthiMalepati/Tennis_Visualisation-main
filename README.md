# Tennis_Visualisation

# Setup (windows):

## Install python3
- Install python3 and then install pip. Once the installation is complete install the virtualenv
```bash
$ pip install virtualenv
```
- Once the virtualenv is installed create a virtual environment in this folder as follows
```bash
$ python3 -m virtualenv venv
		or
$ python3 -m venv venv
```
- Activate the virtual environment as follows
windows - cmd
```bash
$ .\venv\Scripts\activate
```
Linux or Mac
```bash
$ source venv/bin/activate
```
- Install the required packages using requirements.txt
```bash
$ pip install -r requirements.txt
```
<b> How to run the project </b>
- Download the elastic search https://www.elastic.co/downloads/elasticsearch choosing required platform.
- Run elastic search using the command bin/elasticsearch
- Run app.py and tennis.py files in two separate terminals
- To scrape the data run scrapper.py file with specified arguments and view the website that is running in localhost. example:http://127.0.0.1:8080/ 
