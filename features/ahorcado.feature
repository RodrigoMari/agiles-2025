Feature: Juego del Ahorcado

  #--------------------------------------------------------
  # El Juego Perfecto
  #--------------------------------------------------------
  Scenario: El jugador adivina todas las letras sin errores
    Given la palabra secreta es "python" y el jugador tiene 5 vidas
    When el jugador intenta las letras "p,y,t,h,o,n"
    Then el jugador gana el juego
    And le quedan 5 vidas

  #--------------------------------------------------------
  # El Peor Juego
  #--------------------------------------------------------
  Scenario: El jugador falla todas las letras
    Given la palabra secreta es "python" y el jugador tiene 5 vidas
    When el jugador intenta las letras "a,e,i,u,s"
    Then el jugador pierde el juego
    And le quedan 0 vidas

  #--------------------------------------------------------
  # Gano con algunos errores
  #--------------------------------------------------------
  Scenario: El jugador gana con algunos errores
    Given la palabra secreta es "python" y el jugador tiene 5 vidas
    When el jugador intenta las letras "a,p,y,t,o,h,n"
    Then el jugador gana el juego
    And le quedan 4 vidas

  #--------------------------------------------------------
  # Pierdo con algunos aciertos
  #--------------------------------------------------------
  Scenario: El jugador pierde con algunos aciertos
    Given la palabra secreta es "python" y el jugador tiene 5 vidas
    When el jugador intenta las letras "p,a,e,i,u,s"
    Then el jugador pierde el juego
    And le quedan 0 vidas