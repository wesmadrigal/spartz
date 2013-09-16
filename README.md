spartz
======

<b>Spartz</b> preliminary project

<b>Clone me</b><br>
<tr><b>git clone https://github.com/wesmadrigal/spartz.git</b><br>


The Spartz preliminary project to take a csv file with columns:
  - id
  - fbid
  - name
  - latitude
  - longitude

And utilize a publically available API to use the existing data and generate four new columns:
  - continent
  - country
  - state/province
  - city


<b>Developer Dependencies:</b><br>
  language: <b>python</b><br>
  database: <b>sqlite3</b>


<b>Build Data</b>:
  - clone this repo <b>git clone https://github.com/wesmadrigal/spartz.git</b>
  - if which sqlite3 reveals nothing, install sqlite3
    <b>sudo apt-get install sqlite3</b>
  - inside the newly cloned repo execute
    <b>python main.py /path/to/data.txt</b>


<b>Daemonize</b>:
  - in a shell:<br>
<tr><b>crontab -e</b><br>
  - execute the data module every night at 1:00 a.m.<br>
<tr><b>0 1 * * * python /path/to/spartz/main.py data.txt 2>&1 /var/log/geodata.log</b>

  
The module I built takes the csv file to be converted's path as a command line argument to the "main.py"
python file and reads in the csv, hits the API with data extracted from the csv, retrieves the new data
from the API and parses pertinent, then adds the new information to our database with the desired columns
continent, country, state/province, city added.

