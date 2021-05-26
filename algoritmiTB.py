def red_elementa(broj, modulo):
    """
    Funkcija koja računa red elementa nekog broja po nekom modulu.

    Parameters
    ----------
    broj : int
        prirodni broj čiji se red računa
    modulo : int
        prirodni broj po čijem se modulu red računa

    Returns
    -------
    int
        red elementa po danom modulu
    """

    red = 1
    ostatak = (broj**red)%modulo
    while ostatak != 1:
        red += 1
        ostatak = (broj**red)%modulo
    return red

def primitivni_korijen(modulo):
    """ 
    Funkcija koja računa najmanji primitivni korijen po nekom modulu.

    Koristi se funkcija :func:`algoritmiTB.red_elementa`
    kako bi se našao najmanji broj čiji je red upravo :math:`\\text{modulo}-1`
    uz pretpostavku da je riječ o prostom broju.

    Parameters
    ----------
    modulo : int
        prost broj za koji se računa najmanji primitivni korijen

    Returns
    -------
    int
        najmanji primitivni korijen po danom modulu
    """

    korijen = 1
    red = red_elementa(korijen, modulo)
    while red != modulo-1:
        korijen += 1
        red = red_elementa(korijen, modulo)
    return korijen

def inverz(broj, modulo):
    """
    Funkcija koja računa multiplikativni inverz nekog broja po nekom modulu.

    Za dane brojeve :math:`\\text{modulo}` i :math:`\\text{broj}` se traži broj :math:`\\text{inverz}` tako da vrijedi

    .. math::
        \\text{broj} \\cdot \\text{inverz} \\equiv 1\\ \\text{mod}\\ \\text{modulo}

    Parameters
    ----------
    broj : int
        prirodan broj čiji se inverz računa
    modulo : int
        prirodan broj po kojem se računa inverz
    
    Returns
    -------
    int
        multiplikativni inverz od :math:`\\text{broj}` modulo :math:`\\text{modulo}`
    """
    for i in range(modulo**2):
        if i*broj % modulo == 1: return i
    return -1

def rastavNaZnamenke(broj):
    """
    Funkcija koja rastavlja broj na znamenke.

    Parameters
    ----------
    broj : int
        prirodan broj koji se rastavlja na znamenke
    
    Returns
    -------
    int[]
        lista znamenki danog broja
    """

    lista = []
    while broj>0: 
        lista.append(broj%10)
        broj //= 10
    lista.reverse()
    return lista