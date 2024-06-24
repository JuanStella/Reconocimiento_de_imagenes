import math 
import numpy as np
import cv2

class imagen:

    def __init__(self, directorio=None):
        self.img = cv2.imread(directorio)
        if self.img is None:
            raise ValueError(f"Error al cargar la imagen desde la ruta: {directorio}")
        # Pasar a escala de grises la imagen obtenida
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        # Redimensionar la imagen a 600x600
        self.img = cv2.resize(self.img, (600, 600))
        self.momentos_hu = [0] * 2
        self.circularidad = 0
        self.perimetro = 0
        self.preprocesar()
        return None

    def preprocesar(self):
        self.img = contraste(self.img)
        self.img = eliminar_ruido(self.img)
        self.img = histogramas(self.img)
        self.img = binarizar(self.img)
        self.img, self.circularidad, self.perimetro = detectar_contorno_principal(self.img)

        '''cv2.imshow('Imagen', self.img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()'''

        HU = calc_momentos_HU(self.img)
    
        self.momentos_hu[0] = HU[0]
        self.momentos_hu[1] = self.circularidad

        return self.img

def detectar_contorno_principal(img):
    contornos, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    img2 = cv2.drawContours(np.zeros_like(img), contornos, -1, (255, 255, 255), 1)
    
    # Encontrar el contorno con mayor área
    max_area = 0
    circularidad = 0
    
    for contorno in contornos:
        area = cv2.contourArea(contorno)
        perimetro = cv2.arcLength(contorno, True)
        
        max_area = area
        perimetro = cv2.arcLength(contorno, True)
        if perimetro != 0:
            circularidad = (4 * np.pi * area) / (perimetro * perimetro)
    
    return img2, circularidad, perimetro

def histogramas(img):
    img2 = cv2.equalizeHist(img)
    return img2

def contraste(img):
    img2 = cv2.convertScaleAbs(img, alpha=2, beta=-40)
    return img2

def eliminar_ruido(img):
    img = cv2.GaussianBlur(img, (5, 5), 0)
    return img

def binarizar(img):
    _, img2 = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # Invertir la imagen binarizada para resaltar el tornillo en blanco y el fondo en negro
    img2 = cv2.bitwise_not(img2)
    return img2

def calc_momentos_HU(im):
    # Calcular Momentos
    moments = cv2.moments(im)
    # Calcular Hu Moments
    huMoments = cv2.HuMoments(moments)
    # Convertir los valores de huMoments a escalares antes de realizar las operaciones matemáticas
    huMoments = [moment[0] for moment in huMoments]
    for i in range(0, 7):
        huMoments[i] = -1 * math.copysign(1.0, huMoments[i]) * math.log10(abs(huMoments[i]))
    return huMoments
