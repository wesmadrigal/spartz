spartz
======

spartz preliminary project


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


Developer dependencies:
  language: python
  database: sqlite3

  
The module I built takes the csv file to be converted's path as a command line argument to the "main.py"
python file and reads in the csv, hits the API with data extracted from the csv, retrieves the new data
from the API and parses pertinent, then adds the new information to our database with the desired columns
continent, country, state/province, city added.

