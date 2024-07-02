(define (domain reorganizar-cajas)
  (:requirements :negative-preconditions :strips)
  (:predicates
    (caja ?x)     ; ?x es una caja
    (sobre ?x ?y) ; ?x está sobre ?y
    (mesa ?x)     ; ?x está en la mesa
    (libre ?x)    ; ?x está libre (sin nada encima)
    (base ?x)     ; ?x es una base (es la caja más baja de una pila)
    (posicion ?x) ; ?x es una posición (ej. mesa)
    (despejado ?x)); ?x está despejado (sin nada encima)

  (:action mover                               ;Funcion que mueve una caja que esté libre y no sea la base, a la mesa
    :parameters (?caja1 ?caja2)
    :precondition (and (caja ?caja1) 
                       (caja ?caja2) 
                       (sobre ?caja1 ?caja2)
                       (libre ?caja1) 
                       (not (base ?caja1)))
    :effect (and (not (sobre ?caja1 ?caja2)) 
                 (mesa ?caja1) 
                 (libre ?caja2)))


  (:action quitar-ultimo                      ;Funcion que mueve una caja que esté libre y sea la base, a la mesa
    :parameters (?caja ?base)
    :precondition (and (caja ?caja) 
                       (posicion ?base) 
                       (base ?caja) 
                       (not (despejado ?base)) 
                       (libre ?caja))
    :effect (and (mesa ?caja) 
                 (not (base ?caja)) 
                 (despejado ?base)))
                 

  (:action juntar                             ;Funcion que mueve una caja que esté libre y no sea la base, a la pila
    :parameters (?caja1 ?caja2)
    :precondition (and 
                   (caja ?caja1) 
                   (caja ?caja2) 
                   (mesa ?caja1) 
                   (libre ?caja2))
    :effect (and (sobre ?caja1 ?caja2) 
                 (not (mesa ?caja1)) 
                 (not (libre ?caja2))))


  (:action poner-ultimo                     ;Funcion que mueve una caja que esté libre y que sea la base, a la base de la pila
    :parameters (?caja ?base)
    :precondition (and 
                   (caja ?caja) 
                   (posicion ?base) 
                   (mesa ?caja) 
                   (libre ?caja) 
                   (despejado ?base))
    :effect (and (not (mesa ?caja)) 
                 (base ?caja) 
                 (not (despejado ?base))))
)