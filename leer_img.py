import math 
import numpy as np
import cv2

class imagen:


    def __init__(self , directorio = None):
        self.img = cv2.imread(directorio)
        if self.img is None:
            raise ValueError(f"Error al cargar la imagen desde la ruta: {directorio}")
        #pasar a escala de grises la imagen obetenida
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        #Redimensionar la imagen a 600x400
        self.img = cv2.resize(self.img, (600, 600))
        self.momentos_hu = [0] * 7
        self.preprocesar()
        return None

    def preprocesar(self):

        self.img = contraste(self.img)
        self.img = eliminar_ruido(self.img)
        self.img = histogramas(self.img)
        self.img = binarizar(self.img)
        self.img = detectar_contornos(self.img)

        cv2.imshow('Tornillo Preprocesado', self.img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
        HU = calc_momentos_HU(self.img)
    
        for i in range(len(HU)):
            self.momentos_hu[i] = HU [i]
        return self.img

def detectar_contornos(img):
    contornos, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    img2 = cv2.drawContours(np.zeros_like(img), contornos, -1, (255, 255, 255), 1)
    return img2

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


