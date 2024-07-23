import cv2
import numpy as np
import os

def detectar_linea_blanca(imagen, umbral=200, min_longitud_linea=100):
    # Convertir la imagen a escala de grises
    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    
    # Aplicar un umbral para obtener una imagen binaria
    _, binaria = cv2.threshold(gris, umbral, 255, cv2.THRESH_BINARY)
    
    # Detectar bordes
    bordes = cv2.Canny(binaria, 50, 150, apertureSize=3)
    
    # Detectar líneas
    lineas = cv2.HoughLinesP(bordes, 1, np.pi/180, 100, minLineLength=min_longitud_linea, maxLineGap=10)
    
    if lineas is not None:
        for linea in lineas:
            x1, y1, x2, y2 = linea[0]
            cv2.line(imagen, (x1, y1), (x2, y2), (0, 255, 0), 2)
        return True
    else:
        return False

# Cargar el archivo de video
ruta_video = 'ruta/video-prueba.mp4'  # Asegúrese de que esta ruta es correcta
if not os.path.exists(ruta_video):
    print(f"Error: No se pudo encontrar el archivo de video en {ruta_video}")
    exit()

cap = cv2.VideoCapture(ruta_video)

if not cap.isOpened():
    print("Error: No se pudo abrir el archivo de video.")
    exit()

# Obtener la información del video
fps_original = cap.get(cv2.CAP_PROP_FPS)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
duration = frame_count / fps_original

print(f"FPS originales: {fps_original}")
print(f"Número total de frames: {frame_count}")
print(f"Duración del video: {duration} segundos")

# Factor de ralentización (ajústelo según sea necesario)
slowdown_factor = 0.25  # Reproduce el video al 25% de la velocidad original
fps_desired = fps_original * slowdown_factor

frame_time = int(1000 / fps_desired)  # Tiempo en milisegundos entre frames

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Fin del video")
        break
    
    linea_detectada = detectar_linea_blanca(frame)
    
    if linea_detectada:
        cv2.putText(frame, "Linea detectada", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    else:
        cv2.putText(frame, "Linea no detectada", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    cv2.imshow('Deteccion de linea blanca', frame)
    
    # Espera entre frames y chequea si se presiona 'q' para salir
    if cv2.waitKey(frame_time) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()