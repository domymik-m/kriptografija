import elGamal as eg
import sifriranje
import desifriranje
import numpy as np
from PIL import Image
import time

if __name__ == "__main__":
    ## start = time.time()
    
    šifra = sifriranje.šifrat("conv.png", 7)
    slova = šifra.kodirajSliku()
    šifra.spremiKodSlike("_sample_")

    ## end = time.time()
    ## print("kodiranje", end-start)

    ## start = time.time()


    # dešifra = desifriranje.dešifrat("_sample_")
    # dešifra.spremiSliku()

    ## end = time.time()
    ## print("dekodiranje", end-start)