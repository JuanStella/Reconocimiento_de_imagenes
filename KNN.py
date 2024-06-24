import BD 
import leer_img
import math
import matplotlib.pyplot as plt
import cv2
class Knn : 

    def __init__(self, k):
        self.k = k
        self.bd = BD.BD()
        self.bd.cargar_imagenes()
        self.bd.guardar_momentos_en_archivo('momentos_hu.txt')


    def distancia_euclediana(self, momentos_hu):
        distancias = []

        for tornillo in self.bd.tornillos:
            dist_tornillo = math.sqrt((momentos_hu[0] - tornillo[0])**2 + (momentos_hu[1] - tornillo[1])**2)
            distancias.append((dist_tornillo, "Tornillos"))

        for tuerca in self.bd.tuercas:
            dist_tuerca = math.sqrt((momentos_hu[0] - tuerca[0])**2 + (momentos_hu[1] - tuerca[1])**2)
            distancias.append((dist_tuerca, "Tuercas"))

        for arandela in self.bd.arandelas:
            dist_arandela = math.sqrt((momentos_hu[0] - arandela[0])**2 + (momentos_hu[1] - arandela[1])**2)
            distancias.append((dist_arandela, "Arandelas"))

        for clavo in self.bd.clavos:
            dist_clavo = math.sqrt((momentos_hu[0] - clavo[0])**2 + (momentos_hu[1] - clavo[1])**2)
            distancias.append((dist_clavo, "Clavos"))

        distancias.sort(key=lambda x: x[0])  # Ordenar por distancia ascendente

        return distancias

    def graficar_momentos(self):

        for i in range(5):
            plt.scatter(self.bd.tornillos[i][0], self.bd.tornillos[i][1], color='red')
            plt.scatter(self.bd.tuercas[i][0], self.bd.tuercas[i][1], color='blue')
            plt.scatter(self.bd.arandelas[i][0], self.bd.arandelas[i][1], color='green')
            plt.scatter(self.bd.clavos[i][0], self.bd.clavos[i][1], color='purple')

            img = leer_img.imagen('D:\\Facu\\IA1\\Proyecto\\Reconocimiento_de_imagenes\\Imagenes\\Test\\torntest1.jpeg')
            plt.scatter(img.momentos_hu[0], img.momentos_hu[1], color='black')

        plt.xlabel('Momento de Hu 1')
        plt.ylabel('Momento de Hu 6')
        plt.title('Momentos de Hu de las imágenes de la base de datos')
        plt.show()
        return None


    def distancia_a_cada_imagen(self):
        img = leer_img.imagen('D:\\Facu\\IA1\\Proyecto\\Reconocimiento_de_imagenes\\Imagenes\\Test\\torntest1.jpeg')
        distancias = self.distancia_euclediana(img.momentos_hu)

        with open('momentos_hu.txt', 'a') as f:
            f.write("\n\nImagen test\n")
            for i, momento in enumerate(img.momentos_hu, 1):
                f.write(f"Momento de HU {i}: {momento}\n")

        # Crear una lista de tuplas (distancia, clase)
        lista_distancias_clases = [(dist, clase) for dist, clase in distancias]

        # Ordenar la lista de tuplas por la distancia
        lista_distancias_clases.sort()

        # Obtener las primeras 5 distancias
        primeras_5 = lista_distancias_clases[:5]

        # Contar las ocurrencias de cada clase en las primeras 5 distancias
        conteo_clases = {"Tornillos": 0, "Tuercas": 0, "Arandelas": 0, "Clavos": 0}
        for dist, clase in primeras_5:
            conteo_clases[clase] += 1

        # Determinar la clase predominante
        clase_predominante = max(conteo_clases, key=conteo_clases.get)

        print("Primeras 5 distancias ordenadas por clase:")
        for dist, clase in primeras_5:
            print(f"Clase: {clase}, Distancia: {dist:.6f}")

        print(f"\nClase predominante: {clase_predominante}")

        return clase_predominante

    
def main():
    knn = Knn(5)
    knn.distancia_a_cada_imagen()
    knn.graficar_momentos()

if __name__ == '__main__':
    main()
