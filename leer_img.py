import math 
import cv2

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
        self.momentos_hu = [0] * 7
        self.circularidad = 0
        self.preprocesar()
        return None

    def preprocesar(self):
        self.img = contraste(self.img)
        self.img = eliminar_ruido(self.img)
        self.img = histogramas(self.img)
        self.img = binarizar(self.img)
        cnts,_ = cv2.findContours(self.img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.conts = cv2.drawContours(self.conts, cnts, -1, (0, 0, 255), 2)
        for c in cnts:
            epsilon = 0.01*cv2.arcLength(c,True)
            approx = cv2.approxPolyDP(c,epsilon,True)

    
        self.circularidad = len(approx)/25

        '''cv2.imshow("imagen",self.img)
        cv2.imshow("contornos",self.conts)
        cv2.waitKey(0)
        cv2.destroyAllWindows()'''

     
        HU = calc_momentos_HU(self.img)       

        #Procesado manual 
        if HU[0] > 2.9:
            HU[0] = HU[0] * 1.2
            self.circularidad = self.circularidad * 1.2


        if HU[0] > 2.2 and HU[0] < 2.8 and self.circularidad < 0.205:
            self.circularidad = self.circularidad + 0.35
        elif HU[0] < 2.17 and self.circularidad < 0.315:
            self.circularidad = self.circularidad + 0.2
        elif HU[0] < 2.155:
            HU[0] = HU[0] + 0.15
        elif HU[0] > 2.2 and HU[0] < 2.4 and self.circularidad < 0.315:
            HU[0] = HU[0] + 0.25
            

        self.momentos_hu[0] = HU[0]
        self.momentos_hu[5] = self.circularidad

        return self.img


def histogramas(img):
    img2 = cv2.equalizeHist(img)
    return img2

def contraste(img):
    img2 = cv2.convertScaleAbs(img, alpha=1, beta= 170)
    return img2

def eliminar_ruido(img):
    img = cv2.GaussianBlur(img, (3,3), 0)
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
