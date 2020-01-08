# etlWebScraper
Web scrapper project

Aplikacja webowa pozwalająca na wykonanie procesu ETL.
Aplikcja scrapuje/ekstrahuje dane w witryny otodom.pl w postaci ofert wynajmu mieszkań. Dane trafiają do tabeli w której przechowywane
są do czasu wykonania operacji Transform. Podczas 'Transform' dane zastają poddane przeobrażeniu, wycięte zostają tylko interesujące 
częsci oraz zmianie ulega typ danych.
Przeobrażone dane podczas operacji 'Load' zasilają baze danych gdzie zostają zapisane. Możliwa jest późniejsza aktualizacja danych, 
ich przechlądanie oraz filtracja. Dostępne są także podstawowe statystyki jak ilość rekordów w bazie danych czy ilość nowo dodanych.


# Instalacja
1. Sklonuj repozytorium: `git clone https://github.com/pniedziela/etlWebScraper.git`
2. Przejdź do repozytorium `cd etlWebScraper`
3. Zainstaluj wymagane biblioteki `pip install -r requirements.txt`
4. Stwórz tabele w bazie danych: `from app import db` a nastepnie `db.create_all()`
5. Uruchom aplikację poprzez: `python ./app.py`
