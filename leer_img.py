import math 
import cv2
import numpy as np
class imagen:

    def __init__(self, directorio=None):
        self.img = cv2.imread(directorio)
        self.conts = self.img.copy()
        if self.img is None:
            raise ValueError(f"Error al cargar la imagen desde la ruta: {directorio}")
        
        # Pasar a escala de grises la imagen obtenida
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        self.conts = cv2.cvtColor(self.conts, cv2.COLOR_BGR2GRAY)

        # Redimensionar la imagen a 600x600
        self.img = cv2.resize(self.img, (600, 600))
        self.conts = cv2.resize(self.conts, (600, 600))
        self.es_tornillo = False
        self.es_clavo = False

        self.momentos_hu = [0] * 7
        self.preprocesar()
        return None

    def preprocesar(self):
        self.img = contraste(self.img)
        self.img = eliminar_ruido(self.img)
        self.img = histogramas(self.img)
        self.img = binarizar(self.img)
        #Detección de contornos
        cnts,_ = cv2.findContours(self.img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.conts = cv2.drawContours(self.conts, cnts, -1, (0, 0, 255), 2)


        '''cv2.imshow("imagen",self.img)
        cv2.imshow("contornos",self.conts)
        cv2.waitKey(0)
        cv2.destroyAllWindows()'''


        HU = calc_momentos_HU(self.img)  
        # En tu método preprocesar:
        for c in cnts:
            if len(c) > 0:  # Asegúrate de que el contorno no esté vacío
                hu1, circularity = analizar_objeto(c)

                if hu1 < - 0.225:
                    HU[1] += 5
                if HU[1] > 13:
                    HU[1] -=3

                if HU[1] < 6 and circularity > 0.6:
                    circularity -= 0.4

                if HU[1] < 4.6 and circularity > 0.2:
                    circularity += 0.6

                if HU[1] < 6.5 and circularity > 0.6:
                    circularity -= 0.35
                # Ajusta estos umbrales según tus datos específicos
                if circularity < 0.115:
                   HU[1] = HU[1] + 0.3
                elif circularity > 0.6 and HU[1] > 6.35:
                    HU[1] = HU[1] + 2
            else:
                print("Contorno inválido")

        self.momentos_hu[0] = HU[1]/15
        self.momentos_hu[5] = circularity
        return self.img


#Esto redistribuye los valores de intensidad de los píxeles de manera que las intensidades se distribuyan más uniformemente, lo que resulta en una imagen con mejor contraste.
def histogramas(img):
    img2 = cv2.equalizeHist(img)
    return img2


#Se suma a los valores de intensidad, el valor 170. Es decir, estamos haciendo toda la imagen más brillante
def contraste(img):
    img2 = cv2.convertScaleAbs(img, alpha=1, beta= 170)
    return img2


#Usa un Kernel de 3x3 para eliminar el ruido de la imagen.  
# El filtro de desenfoque gaussiano utiliza una función gaussiana para calcular los valores del kernel, 
# lo que da más peso a los píxeles cercanos al centro del kernel y menos peso a los píxeles más alejados.
def eliminar_ruido(img):
    img = cv2.GaussianBlur(img, (3,3), 0)
    return img

# Binarizar la imagen utilizando el método de Otsu. Este método calcula automáticamente el umbral óptimo para separar el fondo y el primer plano basado en el histograma de la imagen.
# Convierte cada píxel en blanco (255) si su valor de intensidad es mayor que el umbral, o en negro (0) si es menor o igual al umbral.
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



def analizar_objeto(contorno):
    if contorno is None or len(contorno) == 0:
        return 0, 0, 0  # Retorna valores por defecto si el contorno es inválido

    # Calcular Momentos de Hu
    moments = cv2.moments(contorno)
    huMoments = cv2.HuMoments(moments)
    
    # Convertir a escala logarítmica
    for i in range(7):
        if huMoments[i] != 0:
            huMoments[i] = -1 * math.copysign(1.0, huMoments[i]) * math.log10(abs(huMoments[i]))
    
    hu1 = huMoments[0][0]  # Primer momento de Hu
    
    # Calcular área y perímetro
    area = cv2.contourArea(contorno)
    perimeter = cv2.arcLength(contorno, True)
    
    # Calcular circularidad
    circularity = 4 * math.pi * area / (perimeter * perimeter) if perimeter > 0 else 0
    
    return hu1, circularity