import BD 
import leer_img
import math
import matplotlib.pyplot as plt
import numpy as np
class Knn : 

    def __init__(self, k):
        self.k = k
        self.bd = BD.BD()
        self.bd.cargar_imagenes()
        self.bd.guardar_momentos_en_archivo('momentos_hu.txt')

    #Suma de las diferencias absolutas de las características de las imágenes
    def distancia_puntos(self, momentos_hu):
        
        distancias = []
       
        for tornillo in self.bd.tornillos:
            dist = abs(tornillo[0] - momentos_hu[0]) + abs(tornillo[5] - momentos_hu[5]) + abs (tornillo[6] - momentos_hu[6])
            distancias.append((dist, "Tornillos"))
        
        for tuerca in self.bd.tuercas:
            dist = abs(tuerca[0] - momentos_hu[0]) + abs(tuerca[5] - momentos_hu[5]) + abs (tuerca[6] - momentos_hu[6])
            distancias.append((dist, "Tuercas"))
        
        for arandela in self.bd.arandelas:
            dist = abs(arandela[0] - momentos_hu[0]) + abs(arandela[5] - momentos_hu[5]) + abs (arandela[6] - momentos_hu[6])
            distancias.append((dist, "Arandelas"))

        for clavo in self.bd.clavos:
            dist = abs(clavo[0] - momentos_hu[0]) + abs(clavo[5] - momentos_hu[5]) + abs (clavo[6] - momentos_hu[6])
            distancias.append((dist, "Clavos"))
        

        distancias.sort(key=lambda x: x[0])  # Ordenar por distancia ascendente

        return distancias

    
    def graficar_2D(self, direc_prueba):
        for i in range(5):
            plt.scatter(self.bd.tornillos[i][0], self.bd.tornillos[i][5], color='red', label='Tornillos' if i == 0 else "")
            plt.scatter(self.bd.tuercas[i][0], self.bd.tuercas[i][5], color='blue', label='Tuercas' if i == 0 else "")
            plt.scatter(self.bd.arandelas[i][0], self.bd.arandelas[i][5], color='green', label='Arandelas' if i == 0 else "")
            plt.scatter(self.bd.clavos[i][0], self.bd.clavos[i][5], color='purple', label='Clavos' if i == 0 else "")

        img1 = leer_img.imagen(direc_prueba)
        plt.scatter(img1.momentos_hu[0], img1.momentos_hu[5], color='black', label='Imagen de test')

        plt.xlabel('Momento de Hu 1')
        plt.ylabel('Circularidad')
        plt.title('Momentos de Hu de las imágenes de la base de datos')

        plt.legend()  # Agregar la leyenda
        plt.show()
        return None



    def distancia_a_cada_imagen(self):
        img = leer_img.imagen(direc_prueba)
        distancias = self.distancia_puntos(img.momentos_hu)
        
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
        cont = 0
        for dist, clase in primeras_5:
            
            conteo_clases[clase] += 1
            
    
        # Determinar la clase predominante
        clase_predominante = max(conteo_clases, key=conteo_clases.get)
        valores = list(conteo_clases.values())
        print("Primeras 5 distancias ordenadas por clase:")
        for dist, clase in primeras_5:
            cont +=1
            print(f"Clase: {clase}, Distancia: {dist:.6f}")
            if cont == 1:
                clasee = clase

        valores.sort()
        print(valores)
        if valores[3] == valores[2]:
            clase_predominante = clasee

        print(f"\nClase predominante: {clase_predominante}")

        return clase_predominante

direc_prueba = 'D:\\Facu\\IA1\\Proyecto\\Reconocimiento_de_imagenes\\Imagenes\\Test\\tortest3.jpeg'
    
def main():
    knn = Knn(5)
    knn.distancia_a_cada_imagen()
    knn.graficar_2D(direc_prueba)

if __name__ == '__main__':
    main()
