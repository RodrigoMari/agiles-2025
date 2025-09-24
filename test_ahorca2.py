import pytest
from ahorca2 import Ahorcado

def testInicializaJuego():
    palabras = ['python']
    juego = Ahorcado(palabras, vidas=5) # instancia de la clase Ahorcado, nueva partida
    assert juego.palabra_secreta in palabras
    assert juego.vidas == 5
    assert juego.palabra_oculta == ['_'] * len(juego.palabra_secreta)
    assert juego.letras_adivinadas == []
    assert juego.palabras_intentadas == []
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

def testLetraNoRepetida():
    juego = Ahorcado(['python'], vidas=5)
    juego.letras_intentadas = ['p', 'y']
    assert juego.letra_repetida('t') is False
    assert juego.vidas == 5  # no debe descontar vida

def testLetraRepetida():
    juego = Ahorcado(['python'], vidas=5)
    juego.letras_intentadas = ['p', 'y']
    assert juego.letra_repetida('p') is True
    assert juego.vidas == 5  # no debe descontar vida

def testPalabraNoRepetida():
    juego = Ahorcado(['python'], vidas=5)
    juego.palabras_intentadas = ['java', 'script']
    assert juego.palabra_repetida('master') is False
    assert juego.vidas == 5  # no debe descontar vida

def testPalabraRepetida():
    juego = Ahorcado(['python'], vidas=5)
    juego.palabras_intentadas = ['java', 'script']
    assert juego.palabra_repetida('java') is True
    assert juego.vidas == 5  # no debe descontar vida

def testMostrarPalabraFinal():
    juego = Ahorcado(['python'], vidas=5)
    assert juego.termina_juego() == juego.palabra_secreta # en un futuro podemos actualizar la palabra_oculta para que muestre la palabra_secreta

def testLetraCorrectaYGana():
    juego = Ahorcado(['hi'], vidas=5)
    juego.adivinar_letra('h')
    assert juego.victoria is False
    assert juego.terminado is False
    juego.adivinar_letra('i')
    assert juego.victoria is True
    assert juego.terminado is True
    assert juego.palabra_oculta == list(juego.palabra_secreta)

def testSinVidasRestantesYPierde():
    juego = Ahorcado(['hi'], vidas=1)
    juego.adivinar_letra('x')  # letra incorrecta
    assert juego.vidas == 0
    assert juego.victoria is False
    assert juego.terminado is True