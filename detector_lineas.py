import cv2
import numpy as np
import os
import winsound  # Para reproducir un sonido en Windows

def detectar_linea_blanca(imagen, umbral_bajo=150, umbral_alto=255, min_longitud_linea=50, max_gap_linea=20):
    # Convertir la imagen a escala de grises
    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    
    # Aplicar un filtro Gaussiano para reducir el ruido
    gris = cv2.GaussianBlur(gris, (5, 5), 0)
    
    # Aplicar umbral adaptativo para manejar variaciones de iluminación
    binaria = cv2.adaptiveThreshold(gris, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    
    # Aplicar una máscara para centrarse en la parte superior de la caja
    height, width = binaria.shape
    mask = np.zeros_like(binaria)
    mask[int(height * 0.3):int(height * 0.7), :] = 255
    binaria = cv2.bitwise_and(binaria, mask)
    
    # Detectar bordes
    bordes = cv2.Canny(binaria, umbral_bajo, umbral_alto)
    
    # Dilatación para conectar bordes cercanos
    kernel = np.ones((3,3), np.uint8)
    bordes_dilatados = cv2.dilate(bordes, kernel, iterations=1)
    
    # Detectar líneas
    lineas = cv2.HoughLinesP(bordes_dilatados, 1, np.pi/180, threshold=30, minLineLength=min_longitud_linea, maxLineGap=max_gap_linea)
    
    lineas_detectadas = []
    if lineas is not None:
        for linea in lineas:
            x1, y1, x2, y2 = linea[0]
            if abs(y1 - y2) < 20:  # Permitir líneas ligeramente inclinadas
                # Verificar si la línea es suficientemente blanca
                roi = gris[max(0, min(y1,y2)-5):min(height, max(y1,y2)+5), min(x1,x2):max(x1,x2)]
                if np.mean(roi) > umbral_bajo:
                    lineas_detectadas.append((x1, y1, x2, y2))
                    cv2.line(imagen, (x1, y1), (x2, y2), (0, 255, 0), 2)
    
    return len(lineas_detectadas) > 0

def procesar_video(ruta_video, output_path=None):
    if not os.path.exists(ruta_video):
        print(f"Error: No se pudo encontrar el archivo de video en {ruta_video}")
        return

    cap = cv2.VideoCapture(ruta_video)

    if not cap.isOpened():
        print("Error: No se pudo abrir el archivo de video.")
        return

    fps_original = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    if output_path:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps_original, (width, height))

    slowdown_factor = 0.25
    fps_desired = fps_original * slowdown_factor
    frame_time = int(1000 / fps_desired)

    frames_sin_linea = 0
    umbral_alarma = 10  # Número de frames consecutivos sin línea para activar la alarma
    alarma_activada = False

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Fin del video")
            break
        
        linea_detectada = detectar_linea_blanca(frame)
        
        if linea_detectada:
            cv2.putText(frame, "Linea detectada", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            frames_sin_linea = 0
            alarma_activada = False
        else:
            cv2.putText(frame, "Linea no detectada", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            frames_sin_linea += 1

        # Activar alarma si no se detecta línea por varios frames consecutivos
        if frames_sin_linea >= umbral_alarma and not alarma_activada:
            cv2.putText(frame, "ALARMA: CAJA SIN LINEA", (10, height - 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.rectangle(frame, (0, 0), (width, height), (0, 0, 255), 10)  # Borde rojo
            alarma_activada = True
            # Reproducir sonido de alarma (solo en Windows)
            winsound.Beep(1000, 500)  # Frecuencia de 1000 Hz durante 500 ms

        cv2.imshow('Deteccion de linea blanca', frame)
        
        if output_path:
            out.write(frame)
        
        if cv2.waitKey(frame_time) & 0xFF == ord('q'):
            break

    cap.release()
    if output_path:
        out.release()
    cv2.destroyAllWindows()

# Uso de la función
ruta_video = 'C:/Users/gonzalo/Desktop/detector_lineas_blancas/detector_linea_cajas/aparece_caja_sinlinea.mp4'
output_path = 'C:/Users/gonzalo/Desktop/detector_lineas_blancas/detector_linea_cajas/output_video_con_alarma.mp4'
procesar_video(ruta_video, output_path)