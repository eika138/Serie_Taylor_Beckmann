# Serie_Taylor_Beckmann
Series  de Taylor(Maclaurin) en forma expandida en python para la practica de calculo.
# Taylor Series Interactive Visualizer

Visualizador interactivo de series de Taylor desarrollado en Python con Matplotlib.

##  Descripción

Esta aplicación permite comparar una función matemática con su aproximación mediante series de Taylor. Incluye controles interactivos para modificar el número de términos y el punto de expansión.

##  Características

- Visualización de:
  - Función original
  - Aproximación de Taylor
  - Error absoluto
- Controles interactivos:
  - Grado de la serie (n)
  - Centro de expansión (a)
  - Selección de función
- Funciones disponibles:
  - sin(x), cos(x), exp(x)
  - ln(1+x), 1/(1-x), arctan(x)

##  Interpretación

- La aproximación mejora al aumentar el número de términos
- El error es menor cerca del centro de expansión
- Permite observar el comportamiento local de las funciones

##  Requisitos

Instalar dependencias:

pip install numpy matplotlib

##  Uso

Ejecutar el script en Python:

python taylor_series.py

##  Objetivo

Facilitar la comprensión visual de las series de Taylor y su comportamiento en distintos puntos del dominio.
