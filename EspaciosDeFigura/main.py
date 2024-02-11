import cv2
import numpy as np

ancho = 200
alto = 250

imagen_path = 'assets/discovery.jpg'
imagen = cv2.imread(imagen_path)

imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
imagen_rgb = cv2.resize(imagen_rgb, (ancho, alto))
cv2.putText(imagen_rgb, 'RGB', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

imagen_rgb_norm = imagen_rgb / 255.0
c = 1 - imagen_rgb_norm[..., 0]
m = 1 - imagen_rgb_norm[..., 1]
y = 1 - imagen_rgb_norm[..., 2]
k = np.min([c, m, y], axis=0)
c = (c - k) / (1 - k + 1e-7)
m = (m - k) / (1 - k + 1e-7)
y = (y - k) / (1 - k + 1e-7)
imagen_cmyk = (np.dstack((c, m, y, k)) * 255).astype(np.uint8)
imagen_cmyk = cv2.resize(imagen_cmyk, (ancho, alto))
cv2.putText(imagen_cmyk, 'CMYK', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

imagen_lab = cv2.cvtColor(imagen, cv2.COLOR_BGR2LAB)
imagen_lab = cv2.resize(imagen_lab, (ancho, alto))
cv2.putText(imagen_lab, 'LAB', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

imagen_luv = cv2.cvtColor(imagen, cv2.COLOR_BGR2LUV)
imagen_luv = cv2.resize(imagen_luv, (ancho, alto))
cv2.putText(imagen_luv, 'LUV', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

imagen_hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
imagen_hsv = cv2.resize(imagen_hsv, (ancho, alto))
cv2.putText(imagen_hsv, 'HSV', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

imagen_hsl = cv2.cvtColor(imagen, cv2.COLOR_BGR2HLS)
imagen_hsl = cv2.resize(imagen_hsl, (ancho, alto))
cv2.putText(imagen_hsl, 'HSL', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

imagen_rgb_espectral = cv2.cvtColor(imagen_rgb, cv2.COLOR_RGB2HSV)
imagen_rgb_espectral = cv2.resize(imagen_rgb_espectral, (ancho, alto))
cv2.putText(imagen_rgb_espectral, 'Espacio Espectral', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

imagen_concatenada = np.hstack((imagen_rgb, imagen_cmyk[..., :3], imagen_lab, imagen_luv, imagen_hsv, imagen_hsl, imagen_rgb_espectral))

cv2.imshow('Imagenes Concatenadas', imagen_concatenada)

cv2.waitKey(0)
cv2.destroyAllWindows()