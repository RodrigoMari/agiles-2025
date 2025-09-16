import pytest
from ahorca2 import Ahorcado

def testInicializaJuego():
    palabras = ['python']
    juego = Ahorcado(palabras, vidas=5) # instancia de la clase Ahorcado, nueva partida
    assert juego.palabra_secreta in palabras
    assert juego.vidas == 5
    assert juego.palabra_oculta == ['_'] * len(juego.palabra_secreta)
    assert juego.letras_adivinadas == []
    assert juego.letras_intentadas == []
    assert juego.terminado is False
    assert juego.victoria is False

def testLetraCorrectaYNoDescuentaVida():
    juego = Ahorcado(['python'], vidas=5)
    juego.adivinar_letra('p')
    assert 'p' in juego.letras_adivinadas
    assert juego.vidas == 5

def testLetraIncorrectaYDescuentaVida():
    juego = Ahorcado(['python'], vidas=5)
    juego.adivinar_letra('r')
    assert 'r' not in juego.letras_adivinadas
    assert juego.vidas == 4

def testLetraCorrectaYActualizaPalabraOculta():
    juego = Ahorcado(['python'], vidas=5)
    juego.adivinar_letra('y')
    assert 'y' in juego.letras_adivinadas
    assert juego.palabra_oculta[1] == 'y'
    assert juego.vidas == 5

def testLetraIncorrectaYNoActualizaPalabraOculta():
    juego = Ahorcado(['python'], vidas=5)
    juego.adivinar_letra('z')
    assert 'z' not in juego.letras_adivinadas
    assert juego.palabra_oculta == ['_'] * len(juego.palabra_secreta)

def testPalabraCorrectaYGana():
    juego = Ahorcado(['python'], vidas=5)
    juego.adivinar_palabra('python')
    assert juego.victoria is True
    assert juego.terminado is True
    assert juego.palabra_oculta == list(juego.palabra_secreta)

def testPalabraIncorrectaYPierdeVida():
    juego = Ahorcado(['python'], vidas=5)
    juego.adivinar_palabra('java')
    assert juego.vidas == 4