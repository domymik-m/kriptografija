import cv2
import numpy as np
from PIL import Image
import random
import elGamal as eg
import time
import multiprocessing as mp

ABECEDA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ#$&"

class dešifrat:
    """
    Klasa koja reprezentira proces dešifriranja teksutalne datoteke i proces rekreacije fotografije iz niza znakova u datoteci.

    Njezin konstruktor prima samo ime tekstutalne datoteke s kodom.
    Attributes
    ----------
    name : str
        ime tekstualne datoteke u kojoj se nalazi kod
    kod : str
        niz znakova u datoteci, iz kojeg se rekreira slika
    duljina : int
        duljina slike (u pikselima)
    visina : int
        visina slike (u pikselima)
    odsječak : int
        indeks na kojem u kodu počinje dio šifre koji se odnosi na samu fotografiju (dio do tog indeksa kodira osnovne informacije o slici i ElGamalovom stroju)
    stroj : ElGamal
        ElGamalov stroj koji je služio za šifriranje slike i pomoću kojeg se dešifrira kod
    """
    threadovi = []

    def __init__(self, ime):
        self.name = ime
        manager = mp.Manager()
        self.part0 = manager.dict()
        self.part1 = manager.dict()
        self.part2 = manager.dict()
        self.part3 = manager.dict()
        self.kod = ""
        self.odsječak = 0
        self.duljina = 0
        self.visina = 0
    
    def dekodirajSlova(self, slova):
        """
        Funkcija koja niz od tri znaka dekodira u jedan broj.

        Parameters
        ----------
        slova : str
            niz od tri znaka koji se dekodira
        
        Returns
        -------
        int
            prirodan broj čija šifra je uneseni niz
        """
        slova = slova.upper()
        kod1 = (ABECEDA.index(slova[0]), ABECEDA.index(slova[1]))
        kod2 = (ABECEDA.index(slova[0]), ABECEDA.index(slova[2]))
        self.stroj.šifrat = kod1
        dio1 = self.stroj.dešifriraj()
        self.stroj.šifrat = kod2
        dio2 = self.stroj.dešifriraj()
        broj = dio1*10+dio2
        return broj
    
    def dobijRGB(self, slova):
        """
        Funkcija koja niz od devet znakova dekodira u RGB kod.

        Parameters
        ----------
        slova : str
            niz od devet znakova koji se dekodira
        
        Returns
        -------
        int[]
            lista s tri prirodna broja koja predstavlja RGB kod piksela
        """
        R = self.dekodirajSlova(slova[:3])
        G = self.dekodirajSlova(slova[3:6])
        B = self.dekodirajSlova(slova[6:])
        vrati = [R, G, B]
        vrati.reverse()
        return vrati

    def dohvatiRGBove(self, dioKoda, broj):
        """
        Funkcija koja niz znakova dekodira u niz RGB kodova.

        Parameters
        ----------
        dioKoda : str
            niz znakova (dio koda) koji se dekodira
        broj : int
            indeks na čije se mjesto u memoriji spremaju dobiveni RGB-ovi

        Returns
        -------
        None
        """

        matrica = []
        veličina = len(dioKoda)
        pozicija = 0
        red = []
        while pozicija < veličina:
            red.append(self.dobijRGB(dioKoda[pozicija:pozicija+9]))
            if ((pozicija+1)//9 +1) % self.duljina == 0:
                matrica.append(red)
                red = []
            pozicija += 9
        if broj == 0: self.part0[0] = matrica
        elif broj == 1: self.part1[0] = matrica
        elif broj == 2: self.part2[0] = matrica
        elif broj == 3: self.part3[0] = matrica

    def spremiSliku(self):
        """
        Funkcija koja rekreira sliku iz niza znakova u tekstualnoj datoteci.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        newname = self.name
        if len(self.name) < 4 or self.name[-4:]!= ".txt":
            newname += ".txt"
        file = open(newname, 'r')
        lista = file.readlines()
        #for linija in lista: linija.strip()
        self.dohvatiVarijableElGamal(lista[0])
        for i in range(4):
            if i == 0: dio = lista[0].strip()[self.odsječak:]
            else: dio = lista[i].strip()
            t = mp.Process(target=self.dohvatiRGBove, args=(dio, i))
            self.threadovi.append(t)
        for t in self.threadovi: t.start()
        for t in self.threadovi:
            t.join()
        RGBi = []
        RGBi += self.part0.values()[0]
        RGBi += self.part1.values()[0]
        RGBi += self.part2.values()[0]
        RGBi += self.part3.values()[0]
        cv2.imwrite(self.name + ".png", np.asarray(RGBi, dtype='int64'))
    
    def dohvatiKodIzDatoteke(self, name):
        """
        Funkcija koja dohvaća kod slike iz tekstualne datoteke.

        Parameters
        ----------
        name : str
            ime datoteke u kojoj se nalazi kod slike

        Returns
        -------
        str
            kod slike, to jest niz znakova
        """
        if len(name) < 4 or name[-4:]!= ".txt":
            name += ".txt"
        file = open(name, 'r')
        lista = file.readlines()
        for linija in lista:
            self.kod += linija.strip()
        return self.kod
    
    def dohvatiVarijableElGamal(self, dioKoda):
        """
        Funkcija koja iz odgovarajućeg dijela koda dohvaća varijable ElGamalova stroja i osnovne informacije o slici.

        Parameters
        ----------
        dioKoda : str
            odgovarajući dio koda u kojem su smještene šifra traženih varijabli
        
        Returns
        -------
        None
        """
        countVelika = 0
        pozicija = 0
        alfa = 0
        beta = 0
        tajniKljuč = 0
        visina = 0
        duljina = 0
        while countVelika < 4:
            temp = dioKoda[pozicija]
            if countVelika == 0 and temp.isupper():
                alfa += 10*ABECEDA.index(temp)
                countVelika += 1
            elif countVelika == 1:
                if temp.isupper():
                    alfa += ABECEDA.index(temp)
                    countVelika += 1
                else:
                    tajniKljuč *= 10
                    tajniKljuč += ABECEDA.index(temp.upper())
            elif countVelika == 2:
                if temp.isupper():
                    beta += 10*ABECEDA.index(temp)
                    countVelika += 1
                else:
                    visina *= 10
                    visina += ABECEDA.index(temp.upper())
            elif countVelika == 3:
                if temp.isupper():
                    beta += ABECEDA.index(temp)
                    countVelika += 1
                else:
                    duljina *= 10
                    duljina += ABECEDA.index(temp.upper())
            pozicija += 1
        self.visina = visina
        self.duljina = duljina
        self.stroj = eg.ElGamal(29, tajniKljuč, alfa, beta)
        self.odsječak = pozicija

            