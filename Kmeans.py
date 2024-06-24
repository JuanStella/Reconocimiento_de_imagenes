# Kmeans.py
from typing import Counter
import BD as bd
import numpy as np
import matplotlib.pyplot as plt
import leer_img

class Kmeans:
    def __init__(self, k=4):
        self.k = k
        self.centroides = None
        self.bd = bd.BD()
        self.bd.cargar_imagenes()
        self.bd.guardar_momentos_en_archivo('momentos_hu.txt')
        self.momentos_Hu_np = np.array(self.bd.momentos_Hu)  # Convertir momentos_Hu a una matriz numpy

    def colocar(self, X, it=1000):
        self.centroides = np.random.uniform(np.amin(X, axis=0), np.amax(X, axis=0), (self.k, X.shape[1]))  # Inicializar los centroides 

        for _ in range(it):
            y = []

            for data_point in X:
                distancias = Kmeans.distancia_euclediana(data_point, self.centroides)
                numero_cluster = np.argmin(distancias)
                y.append(numero_cluster)
            y = np.array(y)

            indice_de_cluster = []
            for i in range(self.k):
                indice_de_cluster.append(np.argwhere(y == i))  # Obtener los indices de los clusters
            
            centro_clusters = []

            for i, indice in enumerate(indice_de_cluster):
                if len(indice) == 0:
                    centro_clusters.append(self.centroides[i])
                else:
                    centro_clusters.append(np.mean(X[indice], axis=0)[0])
                
            if np.max(self.centroides - np.array(centro_clusters)) < 1e-6:
                break

            else:
                self.centroides = np.array(centro_clusters)
        return y

    @staticmethod
    def distancia_euclediana(datos, centroides):
        distancias = np.sqrt(np.sum((centroides - datos) ** 2, axis=1))
        return distancias
    
    def predecir(self, nuevo_dato):
        distancias = Kmeans.distancia_euclediana(nuevo_dato, self.centroides)
        return np.argmin(distancias)



def main():
    km = Kmeans(4)
    etiquetas_clusters = km.colocar(km.momentos_Hu_np)
    
    fig = plt.figure()
    ax = fig.add_subplot(111)

    # Asignar colores a cada clúster
    colores = ['b', 'g', 'r', 'c']  # Definir colores para cada cluster (modifícalos según tus necesidades)
    colores_clusters = [colores[etiqueta] for etiqueta in etiquetas_clusters]

    scatter = ax.scatter(km.momentos_Hu_np[:, 5], km.momentos_Hu_np[:, 4], c=colores_clusters)
    
    ax.set_xlabel('Momento de Hu 4')
    ax.set_ylabel('Momento de Hu 5')
    ax.set_title('K-means en 2D')

    # Predecir el cluster al que pertenece el nuevo dato
    direc_prueba = 'D:\\Facu\\IA1\\Proyecto\\Reconocimiento_de_imagenes\\Imagenes\\Test\\tortest1.jpeg'
    img1 = leer_img.imagen(direc_prueba)
    ax.scatter(img1.momentos_hu[5], img1.momentos_hu[4], color='black', label='Imagen de test')

    nuevo_dato = img1.momentos_hu
    cluster_asignado = km.predecir(nuevo_dato)
    print(f'El nuevo dato pertenece al clúster: {cluster_asignado}')

    # Agregar leyenda para los clusters
    etiquetas_unicas = np.unique(etiquetas_clusters)
    for i, etiqueta in enumerate(etiquetas_unicas):
        ax.scatter([], [], c=colores[i], label=f'Cluster {etiqueta}')

    ax.legend()

    plt.show()

    return None

if __name__ == '__main__':
    main()

