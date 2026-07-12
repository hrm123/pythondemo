(define (domain sokoban-sequential)
  (:requirements :typing)
  (:types direction locatable - object
          player stone - locatable
          location - object)
  
  (:predicates 
    (clear ?l - location)
    (at ?o - locatable ?l - location)
    (next ?l1 - location ?l2 - location ?d - direction)
    (is-goal ?l - location)
  )

  ;; Action for the player moving into an empty adjacent cell
  (:action move
    :parameters (?p - player ?from - location ?to - location ?dir - direction)
    :precondition (and 
                    (at ?p ?from)
                    (next ?from ?to ?dir)
                    (clear ?to)
                  )
    :effect (and 
              (not (at ?p ?from))
              (at ?p ?to)
              (clear ?from)
              (not (clear ?to))
            )
  )

  ;; Action for the player pushing a stone into an empty adjacent cell
  (:action push
    :parameters (?p - player ?s - stone ?p-from - location ?s-from - location ?s-to - location ?dir - direction)
    :precondition (and 
                    (at ?p ?p-from)
                    (at ?s ?s-from)
                    (next ?p-from ?s-from ?dir)
                    (next ?s-from ?s-to ?dir)
                    (clear ?s-to)
                  )
    :effect (and 
              (not (at ?p ?p-from))
              (at ?p ?s-from)
              (not (at ?s ?s-from))
              (at ?s ?s-to)
              (clear ?p-from)
              (not (clear ?s-to))
            )
  )
)