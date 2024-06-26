(define (problem reordenar-cajas)
  (:domain reorganizar-cajas)
  (:objects arandelas tuercas clavos tornillos piso)
  (:init
    (caja arandelas) 
    (caja tuercas) 
    (caja clavos) 
    (caja tornillos) 
    (posicion piso)
    (sobre tuercas tornillos) 
    (sobre tornillos clavos) 
    (sobre clavos arandelas)
    (base arandelas) 
    (libre tuercas) 
    (not (despejado piso)))
  (:goal
    (and
      (sobre arandelas tornillos) 
      (sobre tornillos tuercas) 
      (sobre tuercas clavos) 
      (base clavos)))
)