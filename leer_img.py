import matplotlib.pyplot as pltcd
import numpy as np
import cv2



class imagen:


    def __init__(self):

        self.img = cv2.imread('D:\\Facu\\IA1\\Proyecto\\Reconocimiento_de_imagenes\\Imagenes\\tornillo1.jpeg')
        #pasar a escala de grises la imagen obetenida
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        #Redimensionar la imagen a 600x400
        self.img = cv2.resize(self.img, (600, 600))

        return None


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


def main():
    imgg = imagen()
    imgg.img = contraste(imgg.img)
    imgg.img = eliminar_ruido(imgg.img)
    imgg.img = histogramas(imgg.img)
    imgg.img = binarizar(imgg.img)
    imgg.img = detectar_contornos(imgg.img)


    cv2.imshow('Tornillo Preprocesado', imgg.img)
    cv2.waitKey(0)

if __name__ == '__main__':
    main()