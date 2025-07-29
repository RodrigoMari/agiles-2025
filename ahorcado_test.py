import pytest
from ahorcado import actualizar_palabra_oculta, letra_en_palabra, solo_letras

def test_actualizar_palabra_oculta():
    palabra_secreta = 'python'
    palabra_oculta = ['_'] * len(palabra_secreta)
    resultado = actualizar_palabra_oculta(palabra_secreta, palabra_oculta, 'p')
    assert resultado == ['p', '_', '_', '_', '_', '_']

def test_no_actualizar_palabra_oculta():
    palabra_secreta = 'python'
    palabra_oculta = ['_'] * len(palabra_secreta)
    resultado = actualizar_palabra_oculta(palabra_secreta, palabra_oculta, 'z')
    assert resultado == ['_', '_', '_', '_', '_', '_']

def test_letra_en_palabra():
    assert letra_en_palabra('p', 'python') is True
    assert letra_en_palabra('z', 'python') is False

def test_solo_letras():
    assert solo_letras('j') is True
    assert solo_letras('ab') is False
    assert solo_letras('3') is False
    assert solo_letras('*') is False
