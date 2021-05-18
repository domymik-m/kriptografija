import cv2
import numpy as np
from PIL import Image
import random
import elGamal as eg
import time
import multiprocessing as mp

ABECEDA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ#$&"

class dešifrat:
    name = ""
    kod = ""
    odsječak = 0
    duljina = 0
    visina = 0
    threadovi = []

    def __init__(self, ime):
        self.name = ime
        manager = mp.Manager()
        self.RGBovi = manager.dict()
    
    def dekodirajSlova(self, slova):
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
        R = self.dekodirajSlova(slova[:3])
        G = self.dekodirajSlova(slova[3:6])
        B = self.dekodirajSlova(slova[6:])
        vrati = [R, G, B]
        vrati.reverse()
        return vrati
    
    

    def dohvatiRGBove(self, dioKoda, broj, lock):
        print(broj)
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
        lock.acquire()
        try: self.RGBovi[broj] = matrica
        finally: lock.release()

    def spremiSliku(self):
        newname = self.name
        if len(self.name) < 4 or self.name[-4:]!= ".txt":
            newname += ".txt"
        file = open(newname, 'r')
        lista = file.readlines()
        #for linija in lista: linija.strip()
        self.dohvatiVarijableElGamal(lista[0])
        for i in range(4):
            lock = mp.Lock()
            if i == 0: dio = lista[0].strip()[self.odsječak:]
            else: dio = lista[i].strip()
            print(i)
            t = mp.Process(target=self.dohvatiRGBove, args=(dio, i, lock))
            self.threadovi.append(t)
        for t in self.threadovi: t.start()
        for t in self.threadovi:
            t.join()
        RGBi = []
        for i in range(4):
            RGBi += self.RGBovi.values()[i]
        cv2.imwrite(self.name + ".jpg", np.asarray(RGBi, dtype='int64'))
    
    def dohvatiKodIzDatoteke(self, name):
        if len(name) < 4 or name[-4:]!= ".txt":
            name += ".txt"
        file = open(name, 'r')
        lista = file.readlines()
        for linija in lista:
            self.kod += linija.strip()
        return self.kod
    
    def dohvatiVarijableElGamal(self, dioKoda):
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

            