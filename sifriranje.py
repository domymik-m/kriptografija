import cv2
import numpy as np
from PIL import Image
import random
import elGamal as eg
import algoritmiTB as tb
import multiprocessing as mp

ABECEDA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ#$&"

class šifrat:
    """
    Klasa koja reprezentira proces šifriranja fotografije u niz znakova koji se sprema u :math:`\\text{.txt}` datoteku.

    Njezin konstruktor prima lokaciju fotografije pomoću koje se sprema slika i tajni ključ pomoću kojeg se konstruira ElGamalov 'stroj'.
    U tom se slučaju kao prost broj uzima 29, što predstavlja broj znakova engleske abecede i još tri pridružena znaka: #, $ i &.

    Attributes
    ----------
    slika : Image
        fotografija koja se šifrira
    prostBroj : int
        prost broj pomoću kojeg se stvara ElGamalov stroj (29)
    tajniKljuč : int
        prirodan broj pomoću kojeg se stvara ElGamalov stroj
    stroj : ElGamal
        ElGamalov stroj kojim će se šifrirati brojevi
    kodovi : dict
        rječnik koji kao ključeve ima prirodne brojeve od nula do tri, a kao vrijednosti isječke koda (stringovi)        
    """


    threadovi = []
    
    def __init__(self, lokacija, tK):
        image = Image.open(lokacija)
        image.save('_temp.png')
        self.slika = Image.open('_temp.png')
        self.prostBroj = 29
        self.tajniKljuč = tK
        self.stroj = eg.ElGamal(29, tK)
        manager = mp.Manager()
        self.kodovi = manager.dict()
        self.startić = 0


    def simpleKodiranjeListe(self, lista):
        """
        Funkcija koja listu brojeva šifrira kao niz znakova.

        Parameters
        ----------
        lista : int[]
            niz brojeva koji se šifrira
        
        Returns
        -------
        str
            šifra, to jest niz znakova
        """

        kod = ""
        for broj in lista:
            kod += ABECEDA[broj].lower()
        return kod

    def kodirajElGamal(self, visina, duljina):
        """
        Funkcija koja šifrira parametre ElGamalovog stroja te visinu i duljinu slike kao niz znakova.

        Parameters
        ----------
        visina : int
            visina slike koja se želi šifrirati
        duljina : int
            duljina slike koja se želi šifrirati
        
        Returns
        -------
        str
            šifra, to jest niz znakova
        """
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
        """
        Funkcija koja šifrira broj kao niz znakova.

        Parameters
        ----------
        broj : int
            broj koji se šifrira
        
        Returns
        -------
        str
            šifra, to jest niz od tri znaka
        """
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
        """
        Funkcija koja nasumice pretvori dano slovo u veliko ili malo.

        Parameters
        ----------
        slovo : str
            slovo koje se pretvara
        
        Returns
        -------
        str
            veliku ili malu inačicu danog slova
        """
        boolean = random.choice([True, False])
        if boolean: return slovo.upper()
        else: return slovo.lower()
    
    def kodirajRGB(self, RGB):
        """
        Funkcija koja šifrira RGB kod kao niz znakova,
        koristeći metodu :meth:`sifriranje.šifrat.kodirajBroj`.

        Parameters
        ----------
        RGB : int[]
            RGB kod koji se šifrira
        
        Returns
        -------
        str
            šifra, to jest niz od devet znakova
        """
        kod = ""
        kod += self.kodirajBroj(RGB[0])
        kod += self.kodirajBroj(RGB[1])
        kod += self.kodirajBroj(RGB[2])
        return kod
    
    def kodirajListuRGBa(self, lista):
        """
        Funkcija koja šifrira listu RGB-ova kao niz znakova,
        koristeći metodu :meth:`sifriranje.šifrat.kodirajRGB`.

        Parameters
        ----------
        lista : int[][]
            lista RGB kodova koja se šifrira
        
        Returns
        -------
        str
            šifra, to jest niz znakova
        """
        kod = ""
        for RGB in lista:
            kod += self.kodirajRGB(RGB)
        return kod
    
    def kodirajNumpyRGBa(self, numpy, koji):
        """
        Funkcija koja šifrira numpy RGB-ova kao niz znakova,
        koristeći metodu :meth:`sifriranje.šifrat.kodirajListuRGBa`.
        Dobiveni kod sprema u rječnik s kodovima.

        Parameters
        ----------
        numpy : numpy.array
            numpy RGB kodova koji se šifrira
        koji : int
            ključ za rječnik kodova, čija vrijednost će biti dobiveni kod
        
        Returns
        -------
        str
            šifra, to jest niz znakova
        """
        kod = ""
        for lista in numpy:
            kod += self.kodirajListuRGBa(lista)
        self.kodovi[koji] = kod
        return kod
    
    def kodirajSliku(self):
        """
        Funkcija koja šifrira sliku kao niz znakova,
        koristeći metodu :meth:`sifriranje.šifrat.kodirajNumpyRGBa`.

        Parameters
        ----------
        None
        
        Returns
        -------
        str
            šifra, to jest niz znakova
        """
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
        """
        Funkcija koja kod slike sprema u :math:`\\text{.txt}` datoteku.

        Parameters
        ----------
        name : str
            ime datoteke u koju se sprema kod
        
        Returns
        -------
        None
        """
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
        


        



