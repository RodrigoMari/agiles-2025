import sys
import os
from behave import given, when, then

# Importamos la clase real Ahorcado
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from ahorca2 import Ahorcado


@given('la palabra secreta es "{palabra}" y el jugador tiene {vidas:d} vidas')
def step_inicializar_juego(context, palabra, vidas):
    # Creamos una instancia del juego con una única palabra fija
    context.juego = Ahorcado([palabra], vidas=vidas)
    # Forzamos que la palabra elegida sea exactamente la que queremos (sin random)
    context.juego.palabra_secreta = palabra
    context.juego.palabra_oculta = ['_'] * len(palabra)


@when('el jugador intenta las letras "{lista_letras}"')
def step_intentar_letras(context, lista_letras):
    letras = [l.strip() for l in lista_letras.split(",")]
    for letra in letras:
        context.juego.adivinar_letra(letra)


@then('el jugador gana el juego')
def step_verificar_gana(context):
    assert context.juego.victoria is True, "El jugador no ganó como se esperaba"
    assert context.juego.terminado is True, "El juego debería estar terminado"


@then('el jugador pierde el juego')
def step_verificar_pierde(context):
    assert context.juego.victoria is False, "El jugador no debería haber ganado"
    assert context.juego.terminado is True, "El juego debería estar terminado"


@then('le quedan {vidas_restantes:d} vidas')
def step_verificar_vidas(context, vidas_restantes):
    assert context.juego.vidas == vidas_restantes, f"Se esperaban {vidas_restantes} vidas, pero quedaron {context.juego.vidas}"
