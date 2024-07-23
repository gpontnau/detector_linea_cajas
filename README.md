# Detector de Líneas Blancas en Cartones

Este proyecto implementa un sistema de detección de líneas blancas en cartones que pasan por una cinta transportadora, utilizando procesamiento de video. (Como objetivo final, video en tiempo real)

## Descripción

En una fábrica de cartón donde trabaja un amigo mío, me pidió ayuda ya que en su área tenian planeado implementar un sistema para mejorar su produccion. Por lo tanto, cree este sistema que utiliza una cámara apuntando a la cinta transportadora para detectar la presencia o ausencia de una línea blanca en los cartones que pasan, a la vez, un contador. El objetivo es mejorar la producción identificando rápidamente cuando falta la línea blanca en un cartón. 

El script realiza las siguientes tareas:
- Procesa el video en tiempo real de la cinta transportadora
- Detecta la presencia de líneas blancas en cada fotograma
- Notifica visualmente cuando no se detecta una línea blanca
- Muestra el contador al finalizar el video

## Tecnologías Utilizadas

- Python 3.x
- OpenCV para procesamiento de imágenes y video
- NumPy para operaciones numéricas

## Instalación

1. Asegúrate de tener Python 3.x instalado.
2. Instala las dependencias
   - pip install opencv
   - python numpy
   
## Configuración

3. Conecta una cámara apuntando a la cinta transportadora.
4. Ajusta la variable `ruta_video` en el script para que apunte a la fuente de video de tu cámara.

## Uso

1. Ejecuta el script: `python detector_lineas.py`
2. El sistema mostrará el video en tiempo real con la detección de líneas.
3. Se mostrará "Línea detectada" en verde cuando se encuentre una línea blanca, y "Línea no detectada" en rojo cuando no se encuentre.
4. Presiona 'q' para salir del programa.

## Personalización

Puedes ajustar los siguientes parámetros según las condiciones específicas de tu fábrica:

- `umbral`: Ajusta la sensibilidad de detección de blanco.
- `min_longitud_linea`: Cambia la longitud mínima de línea a detectar.
- `slowdown_factor`: Modifica la velocidad de procesamiento si es necesario.

## Mantenimiento

- Revisa regularmente la posición y enfoque de la cámara.
- Ajusta los parámetros si cambian las condiciones de iluminación o el tipo de cartón.

## Aporte Comunidad

Si tienes alguna idea para mejorar el código o el programa, no dudes en contribuir. 

Puedes hacerlo de las siguientes formas:

1. Abriendo un issue en el repositorio para discutir tus ideas y sugerencias.
2. Realizando un pull request con tus cambios propuestos.
3. Compartiendo tus experiencias y consejos en la sección de comentarios.

¡Estamos emocionados de escuchar tus ideas y trabajar juntos para hacer que este proyecto sea aún mejor!

