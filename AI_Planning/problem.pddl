(define (problem sokoban-local-minimum)
  (:domain sokoban-sequential)
  (:objects
    dir-down dir-left dir-right dir-up - direction
    p1 - player
    s1 s2 - stone
    loc1-1 loc1-2 loc1-3 loc1-4 loc1-5 loc2-2 loc2-3 - location
  )
  (:init
    ;; Grid Topology (Corridor: 1-1 -> 1-2 -> 1-3 -> 1-4 -> 1-5)
    (next loc1-1 loc1-2 dir-right)
    (next loc1-2 loc1-1 dir-left)
    
    (next loc1-2 loc1-3 dir-right)
    (next loc1-3 loc1-2 dir-left)
    
    (next loc1-3 loc1-4 dir-right)
    (next loc1-4 loc1-3 dir-left)
    
    (next loc1-4 loc1-5 dir-right)
    (next loc1-5 loc1-4 dir-left)

    ;; Side pocket / Deadlock Trap branching off loc1-2
    ;; loc1-2 (corridor) -> loc2-2 -> loc2-3 (dead corner)
    (next loc1-2 loc2-2 dir-down)
    (next loc2-2 loc1-2 dir-up)
    
    (next loc2-2 loc2-3 dir-right)
    (next loc2-3 loc2-2 dir-left)

    ;; --- INITIAL STATE ---
    ;; Player starting at the far left of the corridor
    (at p1 loc1-1)
    
    ;; Stone 1 blocks the corridor at loc1-2
    (at s1 loc1-2)
    
    ;; Stone 2 is sitting in the intermediate pocket at loc2-2
    (at s2 loc2-2)
    
    ;; Clear spaces (locations without stones or players)
    (clear loc1-3)
    (clear loc1-4)
    (clear loc1-5)
    (clear loc2-3)

    ;; Goals definition mapping
    (is-goal loc1-5)
    (is-goal loc2-3)
  )
  (:goal
    (and
      (at s1 loc1-5)
      (at s2 loc2-3)
    )
  )
)