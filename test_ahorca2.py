import pytest
from ahorca2 import Ahorcado

def test_inicializa_juego():
    palabras = ['python']
    juego = Ahorcado(palabras, vidas=5) # instancia de la clase Ahorcado, nueva partida
    assert juego.palabra_secreta in palabras
    assert juego.vidas == 5
    assert juego.palabra_oculta == ['_'] * len(juego.palabra_secreta)
    assert juego.letras_adivinadas == []
    assert juego.letras_intentadas == []
    assert juego.terminado is False
    assert juego.victoria is False