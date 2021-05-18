import elGamal as eg
import šifriranje
import dešifriranje
import numpy as np
from PIL import Image
import time

if __name__ == "__main__":
    #start = time.time()
    #šifra = šifriranje.šifrat("zad.jpg", 7)
    #slova = šifra.kodirajSliku()
    #šifra.spremiKodSlike("zad")

    #end = time.time()
    #print("kodiranje", end-start)

    start = time.time()
    dešifra = dešifriranje.dešifrat("zad")
    dešifra.spremiSliku()
    end = time.time()
    print("dekodiranje", end-start)

### TODO:
"""
Treba u .txt datoteku smjestiti 4 reda teksta!
Svaki red treba biti približno jednake duljine.
Dakle, napisati funkciju koja će određeni broj
rastaviti na zbroj četiriju približno jednaka broja
od kojih je svaki djeljiv s 9.
(Logično, ako su tri sumanda djeljiva s 9, bit će i četvrti
- ne uključujemo kod elGamala! To nadoštukamo na poč. prvog reda.)
Koristeći tako dobivene brojeve, formiramo .txt datoteku.

Onda u dešifratu koristimo 4 'dretve' od kojih svaka
dešifrira po jedan red .txt datoteke!
(Samo na početku izdvojimo prvih n charova do četvrtog uppercase.)
Na taj način bi se trebalo minimizirati vrijeme dešifriranja sveukupno.

I, naravno, koristiti 4 dretve i za šifriranje, logično.
(Al zapravo, možda se pomoću tok dijela može automatski
formirati 4 reda... Razmisli o tome.)
"""


