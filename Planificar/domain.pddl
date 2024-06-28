(define (domain reorganizar-cajas)
  (:requirements :negative-preconditions :strips)
  (:predicates
    (caja ?x)
    (sobre ?x ?y)
    (mesa ?x)
    (libre ?x)
    (base ?x)
    (posbase ?x)
    (despejado ?x))

  (:action quitar
    :parameters (?caja1 ?caja2)
    :precondition (and (caja ?caja1) 
                       (caja ?caja2) 
                       (sobre ?caja1 ?caja2)
                       (libre ?caja1) 
                       (not (base ?caja1)))
    :effect (and (not (sobre ?caja1 ?caja2)) 
                 (mesa ?caja1) 
                 (libre ?caja2)))

  (:action quitar-base
    :parameters (?caja ?base)
    :precondition (and (caja ?caja) 
                       (posbase ?base) 
                       (base ?caja) 
                       (not (despejado ?base)) 
                       (libre ?caja))
    :effect (and (mesa ?caja) 
                 (not (base ?caja)) 
                 (despejado ?base)))

  (:action apilar
    :parameters (?caja1 ?caja2)
    :precondition (and 
                   (caja ?caja1) 
                   (caja ?caja2) 
                   (mesa ?caja1) 
                   (libre ?caja2))
    :effect (and (sobre ?caja1 ?caja2) 
                 (not (mesa ?caja1)) 
                 (not (libre ?caja2))))

  (:action apilar-base
    :parameters (?caja ?base)
    :precondition (and 
                   (caja ?caja) 
                   (posbase ?base) 
                   (mesa ?caja) 
                   (libre ?caja) 
                   (despejado ?base))
    :effect (and (not (mesa ?caja)) 
                 (base ?caja) 
                 (not (despejado ?base))))
)
