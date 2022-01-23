Pentru a face deploy local aveti nevoie de :

- serverul oracle
- instantierea bazei de date in SQLDeveloper cu urmatoarele credentiale:
 PORT: 1521
 HOST: localhost
 SID: XE
 SCHEMA: system
 PAROLA: Unudoitrei.123

ATENTIE !!! Daca schimbati datele de mai sus , acestea trebuie modificate si in fiserul
forms.py din directorul app, in fuctia de initializare a clasei DBC !!!

Pentru crearea bazei de date scripturile la gasiti in fisierul building scripts.
Se ruleaza in urmatoarea ordine:

	building_database.sql
	sequences.sql
	populate_database.sql
	functions.sql
	procedures.sql

Pentru conexiunea cu baza de date trebuie sa aveti instalat cx_Oracle, precum este 
indicat mai jos:
https://cx-oracle.readthedocs.io/en/latest/user_guide/installation.html

Inlocuiti in linia 3 din fisierul database.py cu directorul vostru de oracle instant 
client

Pentru a rula aplicatia este nevoie sa instalati suportul de Flask:

	pip install Flask

Precum si dependentele din fisierele python

	pip install flask_wtf 
	pip install wtforms 
	pip install wtforms.validators 


Run app
Trebuie sa porneasca consola de debugg, iar in browser puteti deschide aplicatia la 
adresa:  http://127.0.0.1:5000/