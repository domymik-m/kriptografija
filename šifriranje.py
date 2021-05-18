import cv2
import numpy as np
from PIL import Image
import random
import elGamal as eg
import algoritmiTB as tb
import multiprocessing as mp

ABECEDA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ#$&"

class šifrat:
    tajniKljuč = 5
    prostBroj = 29
    path = ""
    kod = ""
    startić = 0
    threadovi = []

    def __init__(self, lokacija):
        self.slika = Image.open(lokacija)
        self.stroj = eg.ElGamal(29, 5)
        manager = mp.Manager()
        self.kodovi = manager.dict()
    
    def __init__(self, lokacija, tK):
        self.slika = Image.open(lokacija)
        self.prostBroj = 29
        self.tajniKljuč = tK
        self.stroj = eg.ElGamal(29, tK)
        manager = mp.Manager()
        self.kodovi = manager.dict()

    def simpleKodiranjeListe(self, lista):
        kod = ""
        for broj in lista:
            kod += ABECEDA[broj].lower()
        return kod

    def kodirajElGamal(self, visina, duljina):
        kod = ""
        alfa = tb.rastavNaZnamenke(self.stroj.alfa)
        beta = tb.rastavNaZnamenke(self.stroj.beta)
        ključ = tb.rastavNaZnamenke(self.stroj.tajniKljuč)
        v = tb.rastavNaZnamenke(visina)
        d = tb.rastavNaZnamenke(duljina)
        if len(alfa) < 2: alfa.insert(0, 0)
        if len(beta) < 2: beta.insert(0, 0)
        kod += ABECEDA[alfa[0]] + self.simpleKodiranjeListe(ključ)
        kod += ABECEDA[alfa[1]] + self.simpleKodiranjeListe(v)
        kod += ABECEDA[beta[0]] + self.simpleKodiranjeListe(d)
        kod += ABECEDA[beta[1]]
        return kod

    def kodirajBroj(self, broj):
        rand = random.choice([i for i in range(1, 11)])
        dio1 = broj//10
        dio2 = broj - dio1*10
        kod1 = self.stroj.šifriraj(dio1, rand)
        kod2 = self.stroj.šifriraj(dio2, rand)
        slova = self.randomVelikoMaloSlovo(ABECEDA[kod1[0]])
        slova += self.randomVelikoMaloSlovo(ABECEDA[kod1[1]])
        slova += self.randomVelikoMaloSlovo(ABECEDA[kod2[1]])
        return slova
    
    def randomVelikoMaloSlovo(self, slovo):
        boolean = random.choice([True, False])
        if boolean: return slovo.upper()
        else: return slovo.lower()
    
    def kodirajRGB(self, RGB):
        kod = ""
        kod += self.kodirajBroj(RGB[0])
        kod += self.kodirajBroj(RGB[1])
        kod += self.kodirajBroj(RGB[2])
        return kod
    
    def kodirajListuRGBa(self, lista):
        kod = ""
        for RGB in lista:
            kod += self.kodirajRGB(RGB)
        return kod
    
    def kodirajNumpyRGBa(self, numpy, koji):
        kod = ""
        for lista in numpy:
            kod += self.kodirajListuRGBa(lista)
        self.kodovi[koji] = kod
        #print(kodovi[koji])
        return kod
    
    def kodirajSliku(self):
        data = np.asarray(self.slika, dtype='int64')
        kodEG = self.kodirajElGamal(data.shape[0], data.shape[1])
        visina = data.shape[0]//4
        for i in range(4):
            if i == 3: dio = data[3*visina:, :]
            dio = data[i*visina:(i+1)*visina, :]
            t = mp.Process(target=self.kodirajNumpyRGBa, args=(dio, i))
            self.threadovi.append(t)
        for t in self.threadovi: t.start()
        self.startić = len(kodEG)
        self.kod = kodEG
        for t in self.threadovi:
            t.join()
        for i in range(4):
            self.kod += self.kodovi.values()[i]
        return self.kod
    
    def spremiKodSlike(self, name):
        if len(name) < 4 or name[-4:]!= ".txt":
            name += ".txt"
        file = open(name, 'w')
        duljina = len(self.kod)
        file.write(self.kod[:self.startić])
        duljinaReda = len(self.kod)//4
        while duljinaReda%9 != 0: duljinaReda -= 1
        brojač = self.startić
        for i in range(3):
            file.write(self.kod[brojač:brojač+duljinaReda])
            file.write('\n')
            brojač += duljinaReda
        file.write(self.kod[brojač:])
        file.close()
        


        



