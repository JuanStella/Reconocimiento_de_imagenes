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
        self.momentos_hu = [0] * 7
        self.circularidad = 0
        self.perimetro = 0
        self.preprocesar()
        return None

    def preprocesar(self):
        self.img = contraste(self.img)
        self.img = eliminar_ruido(self.img)
        self.img = histogramas(self.img)
        self.img = binarizar(self.img)
        cnts,_ = cv2.findContours(self.img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for c in cnts:
            epsilon = 0.01*cv2.arcLength(c,True)
            approx = cv2.approxPolyDP(c,epsilon,True)
            #print(len(approx))
            x,y,w,h = cv2.boundingRect(approx)

       
        if len(approx) >= 10.5 and len(approx) < 15:
            self.circularidad = len(approx)*2
        elif len (approx) >= 15:
            self.circularidad = len(approx)*4
        else:
            self.circularidad = len(approx)/2


        '''cv2.imshow('Imagen', self.img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()'''

        HU = calc_momentos_HU(self.img)

            

        self.momentos_hu[0] = HU[0]
        self.momentos_hu[4] = self.circularidad
        self.momentos_hu[5] = HU[3] 

        return self.img

def detectar_contorno_principal(img):
    contornos, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Encontrar el perimetro del contorno principal
    perimetro = 0
    for contorno in contornos:
        perimetro = cv2.arcLength(contorno, True)

    return perimetro

def histogramas(img):
    img2 = cv2.equalizeHist(img)
    return img2

def contraste(img):
    img2 = cv2.convertScaleAbs(img, alpha=2.5, beta=1)
    return img2

def eliminar_ruido(img):
    img = cv2.GaussianBlur(img, (5, 5), 0)
    return img

def binarizar(img):
    _, img2 = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # Invertir la imagen binarizada para resaltar el tornillo en blanco y el fondo en negro
    img2 = cv2.bitwise_not(img2)
    return img2

def detectar_contornos(img):
    img2 = cv2.Canny(img, 100, 200)
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
