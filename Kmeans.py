# Kmeans.py
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

    def colocar(self, X, etiquetas, it=150):

        clases = np.unique(etiquetas)
        if len(clases) < self.k:
            raise ValueError(f'Número de clases ({len(clases)}) es menor que k ({self.k}).')
        
        self.centroides = []  #Lista para almacenar los centroides de los clusters
        self.cluster_names = []  # Lista para almacenar los nombres de los clusters
        
        #Agregamos los centroides iniciales, que serán el primer dato ingresado de cada clase
        for clase in clases[:self.k]:
            indices = np.where(etiquetas == clase)[0]
            if len(indices) > 0:
                self.centroides.append(X[indices[0]])  # Elige el primer punto de cada clase
                self.cluster_names.append(self.bd.etiquetas[clase])  # Asignar el nombre del cluster
        self.centroides = np.array(self.centroides)

        
        for _ in range(it):
            y = []
            #Se calculan las distancias desde el punto que estamos evaluando,
            #Hasta los centroides de los clusters. 
            #Luego se toma el dato como perteneciente el cluster con la menor distancia
            for data_point in X:
                distancias = Kmeans.distancia_euclediana(data_point, self.centroides)
                numero_cluster = np.argmin(distancias)
                y.append(numero_cluster)
            y = np.array(y)


            #Inicializa indice_de_cluster para almacenar los índices de los puntos asignados a cada cluster.
            #Encuentra los índices de los puntos asignados a ese cluster y los guarda en indice_de_cluster.
            indice_de_cluster = []
            for i in range(self.k):
                indice_de_cluster.append(np.argwhere(y == i))  # Obtener los indices de los clusters
            

            #Inicializa centro_clusters para almacenar los nuevos centroides.
            #Para cada cluster y sus índices en indice_de_cluster:
            #Si no hay puntos asignados al cluster, mantiene el centroide actual.
            #Si hay puntos asignados, calcula el nuevo centroide como la media de los puntos asignados.
            centro_clusters = []
            for i, indice in enumerate(indice_de_cluster):
                if len(indice) == 0:
                    centro_clusters.append(self.centroides[i])
                else:
                    centro_clusters.append(np.mean(X[indice], axis=0)[0])
                
            if np.max(self.centroides - np.array(centro_clusters)) < 1e-4:
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
    
    # Generar etiquetas para los datos
    etiquetas = np.array([0] * len(km.bd.tornillos) +
                         [1] * len(km.bd.tuercas) +
                         [2] * len(km.bd.arandelas) +
                         [3] * len(km.bd.clavos))
    
    etiquetas_clusters = km.colocar(km.momentos_Hu_np, etiquetas)
    

    fig = plt.figure()
    ax = fig.add_subplot(111)

    # Asignar colores a cada clúster
    colores = ['b', 'g', 'r', 'c']  # Definir colores para cada cluster (modifícalos según tus necesidades)
    colores_clusters = [colores[etiqueta] for etiqueta in etiquetas_clusters]

    scatter = ax.scatter(km.momentos_Hu_np[:, 0], km.momentos_Hu_np[:, 5], c=colores_clusters)
    
    ax.set_xlabel('Momento de Hu 1')
    ax.set_ylabel('Circularidad')
    ax.set_title('K-means en 2D')

    # Predecir el cluster al que pertenece el nuevo dato
    direc_prueba = 'D:\\Facu\\IA1\\Proyecto\\Reconocimiento_de_imagenes\\Imagenes\\Test\\t2.jpeg'
    img1 = leer_img.imagen(direc_prueba)
    ax.scatter(img1.momentos_hu[0], img1.momentos_hu[5], color='black', label='Imagen de test')

    nuevo_dato = img1.momentos_hu
    cluster_asignado = km.predecir(nuevo_dato)
    print(f'El nuevo dato pertenece al clúster: {km.cluster_names[cluster_asignado]}')

    # Agregar leyenda para los clusters
    etiquetas_unicas = np.unique(etiquetas_clusters)
    for i, etiqueta in enumerate(etiquetas_unicas):
        ax.scatter([], [], c=colores[i], label=f'{km.cluster_names[etiqueta]}')

    # Graficar los centroides finales
    ax.scatter(km.centroides[:, 0], km.centroides[:, 5], color='yellow', marker='*', s=200, label='Centroides')

    ax.legend()

    plt.show()

    return None

if __name__ == '__main__':
    main()
