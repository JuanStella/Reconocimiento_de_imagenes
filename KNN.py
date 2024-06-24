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
            dist_tornillo = math.sqrt(abs((momentos_hu[0] - tornillo[0])**2 + (momentos_hu[1] - tornillo[1])**2 + (momentos_hu[2] - tornillo[2])**2 
                                          + (momentos_hu[3] - tornillo[3])**2 + (momentos_hu[4] - tornillo[4])**2) + (momentos_hu[5] - tornillo[5])**2 + (momentos_hu[6] - tornillo[6])**2)
            distancias.append((dist_tornillo, "Tornillos"))

        for tuerca in self.bd.tuercas:
            dist_tuerca = math.sqrt(abs((momentos_hu[0] - tuerca[0])**2 + (momentos_hu[1] - tuerca[1])**2 + (momentos_hu[2] - tuerca[2])**2 
                                        + (momentos_hu[3] - tuerca[3])**2 + (momentos_hu[4] - tuerca[4])**2) + (momentos_hu[5] - tuerca[5])**2 + (momentos_hu[6] - tuerca[6])**2)
            distancias.append((dist_tuerca, "Tuercas"))

        for arandela in self.bd.arandelas:
            dist_arandela = math.sqrt(abs((momentos_hu[0] - arandela[0])**2 + (momentos_hu[1] - arandela[1])**2 + (momentos_hu[2] - arandela[2])**2 
                                        + (momentos_hu[3] - arandela[3])**2 + (momentos_hu[4] - arandela[4])**2) + (momentos_hu[5] - arandela[5])**2 + (momentos_hu[6] - arandela[6])**2)
            distancias.append((dist_arandela, "Arandelas"))

        for clavo in self.bd.clavos:
            dist_clavo = math.sqrt(abs((momentos_hu[0] - clavo[0])**2 + (momentos_hu[1] - clavo[1])**2 + (momentos_hu[2] - clavo[2])**2 
                                    + (momentos_hu[3] - clavo[3])**2 + (momentos_hu[4] - clavo[4])**2) + (momentos_hu[5] - clavo[5])**2 + (momentos_hu[6] - clavo[6])**2)
            distancias.append((dist_clavo, "Clavos"))

        distancias.sort(key=lambda x: x[0])  # Ordenar por distancia ascendente

        return distancias

    def graficar_momentos(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        for i in range(5):
            ax.scatter(self.bd.tornillos[i][0], self.bd.tornillos[i][4], self.bd.tornillos[i][5], color='red', label='Tornillos' if i == 0 else "")
            ax.scatter(self.bd.tuercas[i][0], self.bd.tuercas[i][4], self.bd.tuercas[i][5], color='blue', label='Tuercas' if i == 0 else "")
            ax.scatter(self.bd.arandelas[i][0], self.bd.arandelas[i][4], self.bd.arandelas[i][5], color='green', label='Arandelas' if i == 0 else "")
            ax.scatter(self.bd.clavos[i][0], self.bd.clavos[i][4], self.bd.clavos[i][5], color='purple', label='Clavos' if i == 0 else "")

        img = leer_img.imagen(direc_prueba)
        ax.scatter(img.momentos_hu[0], img.momentos_hu[4], img.momentos_hu[5], color='black', label='Imagen de test')

        ax.set_xlabel('Momento de Hu 1')
        ax.set_ylabel('Momento de Hu 4')
        ax.set_zlabel('Circularidad')
        ax.set_title('Momentos de Hu de las imágenes de la base de datos')

        handles, labels = ax.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        ax.legend(by_label.values(), by_label.keys())

        plt.show()
        return None
    
    def graficar_2D (self):
        for i in range(5):
            plt.scatter(self.bd.tornillos[i][5], self.bd.tornillos[i][4], color='red')
            plt.scatter(self.bd.tuercas[i][5], self.bd.tuercas[i][4], color='blue')
            plt.scatter(self.bd.arandelas[i][5], self.bd.arandelas[i][4], color='green')
            plt.scatter(self.bd.clavos[i][5], self.bd.clavos[i][4], color='purple')

        img1 = leer_img.imagen(direc_prueba)
        plt.scatter(img1.momentos_hu[5], img1.momentos_hu[4], color='black')


        plt.xlabel('Momento de Hu 4')
        plt.ylabel('Circ')
        plt.title('Momentos de Hu de las imágenes de la base de datos')
        plt.show()
        return None



    def distancia_a_cada_imagen(self):
        img = leer_img.imagen(direc_prueba)
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

direc_prueba = 'D:\\Facu\\IA1\\Proyecto\\Reconocimiento_de_imagenes\\Imagenes\\Test\\atest3.jpeg'
    
def main():
    knn = Knn(5)
    knn.distancia_a_cada_imagen()
    #knn.graficar_momentos()
    knn.graficar_2D()

if __name__ == '__main__':
    main()
