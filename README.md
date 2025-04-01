# Engeto Projekt 3 – Election Scraper
election_scraper.py je třetí projekt v rámci Engeto Online Python Akademie.

Popis projektu

Tento skript slouží ke stažení výsledků parlamentních voleb v roce 2017 z veřejného portálu volby.cz.
Skript načte volební výsledky pro zvolený územní celek (např. okres) a uloží je do přehledného CSV souboru.

Instalace knihoven

Projekt využívá knihovny:

- requests
- beautifulsoup4

1. Ověř verzi správce balíčků:

   pip3 --version
   
2. Instalace knihoven ze souboru requirements.txt:

   pip3 install -r requirements.txt

Spuštění projektu

Skript se spouští z příkazové řádky a očekává dva argumenty:

URL – adresa konkrétního územního celku (např. okres Praha-západ)

název_souboru.csv – výstupní soubor pro uložení dat

Oba argumenty musí být zadány, URL v uvozovkách, název souboru s příponou .csv

python election_scraper.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2110" vysledky_praha_zapad.csv

Průběh skriptu

Skript:

- ověří argumenty,

- stáhne a zpracuje všechny obce v daném územním celku,

- uloží výsledky do .csv souboru.

Výstupní soubor obsahuje:

částecný výstup:

kód obce	název obce	voliči	obálky	platné hlasy	politické strany...
539104	Bojanovice	372	268	267	ODS, ANO, ČSSD, ...
571199	Bratřínov	149	121	121	ODS, ANO, ČSSD, ...

Ošetření chyb

- vypíše upozornění při špatném formátu URL,
- kontroluje počet argumentů,
- ignoruje obce, u kterých se data nepodaří načíst.


