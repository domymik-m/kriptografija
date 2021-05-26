import algoritmiTB as tb

class ElGamal:
    """
    Klasa koja predstavlja ElGamalov kriptosustav.

    Omogućuje šifriranje prirodnog broja parom prirodnih brojeva i, obratno, dešifriranje para prirodnih brojeva u jedan prirodan broj.

    Attributes
    ----------
    prostBroj : int
        proizvoljan prost broj
    tajniKljuč : int
        proizvoljan prirodan broj koji služi kao tajni ključ pri šifriranju
    alfa : int
        prirodan broj koji mora biti primitivni korijen odabranog prostog broja
    beta : int
        prirodan broj za koji vrijedi :math:`\\beta \\equiv \\alpha ^ {\\text{tajniKljuč}}\\ \\text{mod} \\ \\text{prostBroj}`
    šifrat : pair(int, int)
        uređen par prirodnih brojeva u koji se sprema šifrat
    """

    def __init__(self, *args): 
        """
        Konstruktor.

        Prima proizvoljan broj argumenata, ali točno funkcionira samo ukoliko je broj argumenata točno dva ili točno četiri.
        Sprema prost broj i tajni ključ.
        Ukoliko su dana samo dva argumenta, postavlja alfa na najmanji primitivni korijen prostog broja i izračuna beta.
        Ukoliko su dana četiri argumenta, postavlja alfa i beta na dane vrijednosti.

        Attributes
        ----------
        *args : int[]*
            proizvoljan broj prirodnih brojeva
        
        Returns
        -------
        None
        """
        self.šifrat = (-1, -1)
        if len(args) == 0:
            self.prostBroj = 7
            self.tajniKljuč = 5
            self.postaviAlfa()
            self.postaviBeta()
        elif len(args) == 2:
            self.prostBroj = args[0]
            self.tajniKljuč = args[1]
            self.postaviAlfa()
            self.postaviBeta()
        elif len(args) == 4:
            self.prostBroj = args[0]
            self.tajniKljuč = args[1]
            self.alfa = args[2]
            self.beta = args[3]
    
    def postaviAlfa(self):
        """
        Funkcija koja računa vrijednost alfa i sprema je u varijablu :math:`\\text{alfa}`.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        self.alfa = tb.primitivni_korijen(self.prostBroj)
    
    def postaviBeta(self):
        """
        Funkcija koja računa vrijednost beta i sprema je u varijablu :math:`\\text{beta}`.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.beta = (self.alfa**self.tajniKljuč) % self.prostBroj

    def šifriraj(self, broj, tajniBroj):
        """
        Funkcija koja šifrira proizvoljan prirodni broj kao uređeni par prirodnih brojeva.

        Osoba koja šifrira podatak zna vrijednost prostog broja, alfe i bete.
        Usto, bira proizvoljan tajni broj i šifrira željenu vrijednost.

        Parameters
        ----------
        broj : int
            prirodan broj koji se šifrira
        tajniBroj : int
            proizvoljan prirodan broj

        Returns
        -------
        pair(int, int)
            uređeni par prirodnih brojeva koji predstavlja šifrat
        """

        prvi = (self.alfa**tajniBroj) % self.prostBroj
        drugi = (broj * (self.beta**tajniBroj)) % self.prostBroj
        self.šifrat = (prvi, drugi)
        return (prvi, drugi)
    
    def dešifriraj(self):
        """
        Funkcija koja dešifrira proizvoljan uređeni par prirodnih brojeva.

        Osoba koja dešifrira podatak zna vrijednost prostog broja, tajnog ključa, alfe i bete.
        Pomoću toga, može doći do vrijednosti tajnog broja i dobiti šifriranu vrijednost.

        Parameters
        ----------
        None

        Returns
        -------
        int
            prirodan broj koji se skriva iza šifrata
        """
        dio1 = (self.šifrat[0]**self.tajniKljuč) % self.prostBroj
        dio2 = tb.inverz(dio1, self.prostBroj)
        return (dio2*self.šifrat[1])% self.prostBroj

