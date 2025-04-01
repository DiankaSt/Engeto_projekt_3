"""
election_scraper.py: třetí projekt do Engeto Online Python Akademie

author: Diana Stiborová
email: stiborovadiana@seznam.cz
discord: dianastiborova
"""

import requests
from bs4 import BeautifulSoup
import csv
import sys

def nacti_stranku(url):
    """Načte HTML stránku a vrátí objekt BeautifulSoup."""
    try:
        odpoved = requests.get(url)
        odpoved.raise_for_status()
        return BeautifulSoup(odpoved.text, "html.parser")
    except requests.exceptions.RequestException as e:
        print(f"Chyba při načítání stránky: {e}")
        sys.exit(1)

def nacti_vsechny_stranky(url):
    """Načte všechny stránky s obcemi a vrátí jejich obsah jako seznam."""
    soup_list = []
    while url:
        soup = nacti_stranku(url)
        soup_list.append(soup)

        dalsi = soup.find("a", string="Další")
        if dalsi:
            url = "https://www.volby.cz/pls/ps2017nss/" + dalsi["href"]
        else:
            url = None
    return soup_list

def ziskej_obce(soup_list):
    """Získá seznam obcí (kód a název) ze všech načtených stránek."""
    obce = []
    for soup in soup_list:
        tabulky = soup.find_all("table")
        for tabulka in tabulky:
            radky = tabulka.find_all("tr")[2:]
            for radek in radky:
                bunky = radek.find_all("td")
                for i in range(0, len(bunky), 3):
                    if i + 1 < len(bunky):
                        kod_td = bunky[i].find("a")
                        if kod_td:
                            kod = kod_td.text.strip()
                            nazev = bunky[i + 1].text.strip()
                            obce.append((kod, nazev))
    return obce

def ziskej_nazvy_stran(url_vzoru):
    """Získá názvy všech politických stran ze vzorové obce."""
    soup = nacti_stranku(url_vzoru)
    strany = []
    for td in soup.find_all("td", class_="overflow_name"):
        strany.append(td.text.strip())
    return strany

def ziskej_vysledky_obce(kod_obce, nazev_obce, kraj, uzemni_celek):
    """Získá výsledky pro jednu obec."""
    url = f"https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj={kraj}&xobec={kod_obce}&xvyber={uzemni_celek}"
    soup = nacti_stranku(url)
    tabulky = soup.find_all("table")

    if len(tabulky) < 2:
        return []

    try:
        volici = soup.find("td", headers="sa2").text.strip().replace("\xa0", "")
        obalky = soup.find("td", headers="sa5").text.strip().replace("\xa0", "")
        platne = soup.find("td", headers="sa6").text.strip().replace("\xa0", "")
    except AttributeError:
        return []

    vysledky = [kod_obce, nazev_obce, volici, obalky, platne]

    # Získání hlasů pro každou stranu
    for tr in soup.find_all("tr"):
        nazev_td = tr.find("td", class_="overflow_name")
        hlas_td = tr.find("td", headers="t1sa2 t1sb3") or tr.find("td", headers="t2sa2 t2sb3")
        if nazev_td and hlas_td:
            hlas = hlas_td.text.strip().replace("\xa0", "")
            vysledky.append(hlas)

    return vysledky

def uloz_do_csv(data, vystupni_soubor, hlavicky_stran):
    """Uloží výsledek do CSV souboru."""
    if not data:
        print("Nebyla získána žádná data.")
        return

    hlavicka = ["kód", "obec", "voliči", "obálky", "platné"] + hlavicky_stran

    with open(vystupni_soubor, mode="w", newline="", encoding="utf-8") as soubor:
        zapisovac = csv.writer(soubor)
        zapisovac.writerow(hlavicka)
        zapisovac.writerows(data)

    print(f"Data byla uložena do {vystupni_soubor}")

def main():
    if len(sys.argv) != 3:
        print("⚠️ Nesprávný počet argumentů.")
        print("Správné použití: python election_scraper.py \"https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2110\" vysledky.csv")
        sys.exit(1)

    url = sys.argv[1]
    vystupni_soubor = sys.argv[2]

    if "xkraj=" not in url or "xnumnuts=" not in url:
        print("⚠️ Nesprávný formát URL – chybí parametry xkraj a xnumnuts.")
        print("Příklad: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2110")
        sys.exit(1)

    # Získání čísel z URL jednoduše
    kraj = url.split("xkraj=")[1].split("&")[0]
    uzemni_celek = url.split("xnumnuts=")[1]

    soup_list = nacti_vsechny_stranky(url)
    obce = ziskej_obce(soup_list)

    if not obce:
        print("⚠️ Nebyly nalezeny žádné obce.")
        sys.exit(1)

    # Zjistíme názvy stran z první obce
    vzor_url = f"https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj={kraj}&xobec={obce[0][0]}&xvyber={uzemni_celek}"
    hlavicky_stran = ziskej_nazvy_stran(vzor_url)

    data = []
    for kod, nazev in obce:
        vysledky = ziskej_vysledky_obce(kod, nazev, kraj, uzemni_celek)
        if vysledky:
            data.append(vysledky)

    uloz_do_csv(data, vystupni_soubor, hlavicky_stran)

if __name__ == "__main__":
    main()


