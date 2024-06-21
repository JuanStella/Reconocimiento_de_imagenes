from leer_img import imagen


class BD():

    def __init__(self):


        self.tornillos = []
        self.tuercas = []
        self.arandelas = []
        self.clavos = []

        direc_tornillos = ['D:\\Facu\\IA1\\Proyecto\\Reconocimiento_de_imagenes\\Imagenes\\tornillos\\1', 'D:\\Facu\\IA1\\Proyecto\\Reconocimiento_de_imagenes\\Imagenes\\tornillos\\2'
                           , 'D:\\Facu\\IA1\\Proyecto\\Reconocimiento_de_imagenes\\Imagenes\\tornillos\\3', 'D:\\Facu\\IA1\\Proyecto\\Reconocimiento_de_imagenes\\Imagenes\\tornillos\\4', 
                           'D:\\Facu\\IA1\\Proyecto\\Reconocimiento_de_imagenes\\Imagenes\\tornillos\\5'] 
        
        direc_tuercas = ['D:\\Facu\\IA1\\Proyecto\\Reconocimiento_de_imagenes\\Imagenes\\tuercas\\tuer1', 'D:\\Facu\\IA1\\Proyecto\\Reconocimiento_de_imagenes\\Imagenes\\tuercas\\tuer2',
                         'D:\\Facu\\IA1\\Proyecto\\Reconocimiento_de_imagenes\\Imagenes\\tuercas\\tuer3', 'D:\\Facu\\IA1\\Proyecto\\Reconocimiento_de_imagenes\\Imagenes\\tuercas\\tuer4',
                         'D:\\Facu\\IA1\\Proyecto\\Reconocimiento_de_imagenes\\Imagenes\\tuercas\\tuer5']
        
        direc_arandelas = ['D:\\Facu\\IA1\\Proyecto\\Reconocimiento_de_imagenes\\Imagenes\\arandelas\\a1', 'D:\\Facu\\IA1\\Proyecto\\Reconocimiento_de_imagenes\\Imagenes\\arandelas\\a2',
                           'D:\\Facu\\IA1\\Proyecto\\Reconocimiento_de_imagenes\\Imagenes\\arandelas\\a3', 'D:\\Facu\\IA1\\Proyecto\\Reconocimiento_de_imagenes\\Imagenes\\arandelas\\a4',
                           'D:\\Facu\\IA1\\Proyecto\\Reconocimiento_de_imagenes\\Imagenes\\arandelas\\a5']
        
        direc_clavos = ['D:\\Facu\\IA1\\Proyecto\\Reconocimiento_de_imagenes\\Imagenes\\clavos\\c1', 'D:\\Facu\\IA1\\Proyecto\\Reconocimiento_de_imagenes\\Imagenes\\clavos\\c2',
                        'D:\\Facu\\IA1\\Proyecto\\Reconocimiento_de_imagenes\\Imagenes\\clavos\\c3', 'D:\\Facu\\IA1\\Proyecto\\Reconocimiento_de_imagenes\\Imagenes\\clavos\\c4',
                        'D:\\Facu\\IA1\\Proyecto\\Reconocimiento_de_imagenes\\Imagenes\\clavos\\c5']


        return None
    