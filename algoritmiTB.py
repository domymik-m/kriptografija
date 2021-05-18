def red_elementa(broj, modulo):
    red = 1
    ostatak = (broj**red)%modulo
    while ostatak != 1:
        red += 1
        ostatak = (broj**red)%modulo
    return red

def primitivni_korijen(modulo):
    korijen = 1
    red = red_elementa(korijen, modulo)
    while red != modulo-1:
        korijen += 1
        red = red_elementa(korijen, modulo)
    return korijen

def inverz(broj, modulo):
    for i in range(modulo**2):
        if i*broj % modulo == 1: return i
    return -1

def rastavNaZnamenke(broj):
    lista = []
    while broj>0: 
        lista.append(broj%10)
        broj //= 10
    lista.reverse()
    return lista