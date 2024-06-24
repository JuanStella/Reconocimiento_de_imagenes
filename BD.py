from leer_img import imagen

class BD:
    def __init__(self):
        self.tornillos = []
        self.tuercas = []
        self.arandelas = []
        self.clavos = []
        self.momentos_Hu = []
        self.etiquetas = ['Tornillos', 'Tuercas', 'Arandelas', 'Clavos']

        self.direc_tornillos = [
            'D:\\Facu\\IA1\\Proyecto\\Reconocimiento_de_imagenes\\Imagenes\\tornillos\\11.jpeg',
            'D:\\Facu\\IA1\\Proyecto\\Reconocimiento_de_imagenes\\Imagenes\\tornillos\\2.jpeg',
            'D:\\Facu\\IA1\\Proyecto\\Reconocimiento_de_imagenes\\Imagenes\\tornillos\\3.jpeg',
            'D:\\Facu\\IA1\\Proyecto\\Reconocimiento_de_imagenes\\Imagenes\\tornillos\\4.jpeg',
            'D:\\Facu\\IA1\\Proyecto\\Reconocimiento_de_imagenes\\Imagenes\\tornillos\\5.jpeg'
        ]
        
        self.direc_tuercas = [
            'D:\\Facu\\IA1\\Proyecto\\Reconocimiento_de_imagenes\\Imagenes\\tuercas\\tuer1.jpeg',
            'D:\\Facu\\IA1\\Proyecto\\Reconocimiento_de_imagenes\\Imagenes\\tuercas\\tuer2.jpeg',
            'D:\\Facu\\IA1\\Proyecto\\Reconocimiento_de_imagenes\\Imagenes\\tuercas\\tuer3.jpeg',
            'D:\\Facu\\IA1\\Proyecto\\Reconocimiento_de_imagenes\\Imagenes\\tuercas\\tuer4.jpeg',
            'D:\\Facu\\IA1\\Proyecto\\Reconocimiento_de_imagenes\\Imagenes\\tuercas\\tuer5.jpeg'
        ]
        
        self.direc_arandelas = [
            'D:\\Facu\\IA1\\Proyecto\\Reconocimiento_de_imagenes\\Imagenes\\arandelas\\a1.jpeg',
            'D:\\Facu\\IA1\\Proyecto\\Reconocimiento_de_imagenes\\Imagenes\\arandelas\\a2.jpeg',
            'D:\\Facu\\IA1\\Proyecto\\Reconocimiento_de_imagenes\\Imagenes\\arandelas\\a3.jpeg',
            'D:\\Facu\\IA1\\Proyecto\\Reconocimiento_de_imagenes\\Imagenes\\arandelas\\a4.jpeg',
            'D:\\Facu\\IA1\\Proyecto\\Reconocimiento_de_imagenes\\Imagenes\\arandelas\\a5.jpeg'
        ]
        
        self.direc_clavos = [
            'D:\\Facu\\IA1\\Proyecto\\Reconocimiento_de_imagenes\\Imagenes\\clavos\\c1.jpeg',
            'D:\\Facu\\IA1\\Proyecto\\Reconocimiento_de_imagenes\\Imagenes\\clavos\\c2.jpeg',
            'D:\\Facu\\IA1\\Proyecto\\Reconocimiento_de_imagenes\\Imagenes\\clavos\\c3.jpeg',
            'D:\\Facu\\IA1\\Proyecto\\Reconocimiento_de_imagenes\\Imagenes\\clavos\\c4.jpeg',
            'D:\\Facu\\IA1\\Proyecto\\Reconocimiento_de_imagenes\\Imagenes\\clavos\\c5.jpeg'
        ]

    def cargar_imagenes(self):
        for i in range(5):
            try:
                img = imagen(self.direc_tornillos[i])
                self.tornillos.append(img.momentos_hu)
            except ValueError as e:
                print(e)

        for i in range(5):
            try:
                img = imagen(self.direc_tuercas[i])
                self.tuercas.append(img.momentos_hu)
            except ValueError as e:
                print(e)

        for i in range(5):
            try:
                img = imagen(self.direc_arandelas[i])
                self.arandelas.append(img.momentos_hu)
            except ValueError as e:
                print(e)

        for i in range(5):
            try:
                img = imagen(self.direc_clavos[i])
                self.clavos.append(img.momentos_hu)
            except ValueError as e:
                print(e)

        self.momentos_Hu = self.tornillos + self.tuercas + self.arandelas + self.clavos

        return None
    
        
    
    def guardar_momentos_en_archivo(self, archivo):
        with open(archivo, 'w') as f:
            f.write("Momentos de Hu de las imagenes de los tornillos:\n\n")
            for i, momentos in enumerate(self.tornillos):
                f.write(f"Imagen {i+1}:\n")
                for j, momento in enumerate(momentos):
                    f.write(f"  Hu[{j+1}]: {momento:.6f}\n")
                f.write("\n")

            f.write("Momentos de Hu de las imagenes de las tuercas:\n\n")
            for i, momentos in enumerate(self.tuercas):
                f.write(f"Imagen {i+1}:\n")
                for j, momento in enumerate(momentos):
                    f.write(f"  Hu[{j+1}]: {momento:.6f}\n")
                f.write("\n")

            f.write("Momentos de Hu de las imagenes de las arandelas:\n\n")
            for i, momentos in enumerate(self.arandelas):
                f.write(f"Imagen {i+1}:\n")
                for j, momento in enumerate(momentos):
                    f.write(f"  Hu[{j+1}]: {momento:.6f}\n")
                f.write("\n")

            f.write("Momentos de Hu de las imagenes de los clavos:\n\n")
            for i, momentos in enumerate(self.clavos):
                f.write(f"Imagen {i+1}:\n")
                for j, momento in enumerate(momentos):
                    f.write(f"  Hu[{j+1}]: {momento:.6f}\n")
                f.write("\n")
        return None
    

