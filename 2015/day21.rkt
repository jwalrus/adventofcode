#lang racket

(require rackunit)

;; structs
(struct weapon (name cost damage armor) #:transparent)
(struct armor (name cost damage armor) #:transparent)
(struct ring (name cost damage armor) #:transparent)
(struct player (name hit-pts damage armor cost) #:transparent)

;; store
(define weapons
  (list (weapon 'dagger 8 4 0)
    (weapon 'shortsword 10 5 0)
    (weapon 'warhammer 25 6 0)
    (weapon 'longsword 40 7 0)
    (weapon 'greataxe 74 8 0)))

(define armors
  (list (armor 'none 0 0 0)
    (armor 'leather 13 0 1)
    (armor 'chainmail 31 0 2)
    (armor 'splintmail 53 0 3)
    (armor 'bandedmail 75 0 4)
    (armor 'platemail 102 0 5)))

(define rings
  (list (ring 'none 0 0 0)
    (ring 'damage1 25 1 0)
    (ring 'damage2 50 2 0)
    (ring 'damage3 100 3 0)
    (ring 'defense1 20 0 1)
    (ring 'defense2 40 0 2)
    (ring 'defense3 80 0 3)))
            
;; funcs

;; (player1, player2) -> player2' 
(define (attack p1 p2)
  (let ([new-hit-pts (- (player-hit-pts p2) (max 1 (- (player-damage p1) (player-armor p2))))])
    (player (player-name p2) new-hit-pts (player-damage p2) (player-armor p2) (player-cost p2))))

;; (player1, player2) -> (winner, loser)
(define (play p1 p2)
  (cond [(0 . >= . (player-hit-pts p1)) (list p2 p1)]
        [(0 . >= . (player-hit-pts p2)) (list p1 p2)]
        [else                       (play (attack p1 p2) p1)]))

(define (build-player name hit-pts weapon armor . rings)
  (define damage (+ (weapon-damage weapon) (apply + (map ring-damage rings))))
  (define defense (+ (armor-armor armor) (apply + (map ring-armor rings))))
  (define cost (+ (weapon-cost weapon) (armor-cost armor) (apply + (map ring-cost rings))))
  (player name hit-pts damage defense cost))


(define (simulate me-hit-pts boss)
  (for*/list ([weapon weapons]
              [armor armors]
              [ring1 rings]
              [ring2 rings]
              #:unless (and (equal? ring1 ring2) (not (equal? 'none (ring-name ring1)))))
    (let ([me (build-player 'me me-hit-pts weapon armor ring1 ring2)])
      (play me boss))))


(define (part1 my-hit-pts boss)
  (for/fold ([min (player 'dummy 0 0 0 99999999999)])
            ([p (simulate my-hit-pts boss)]
             #:when (equal? 'me (player-name (first p))))
    (cond [(< (player-cost (first p)) (player-cost min)) (first p)]
          [else                min])))


(define (part2 my-hit-pts boss)
  (for/fold ([mx (player 'dummy 0 0 0 -1)])
            ([p (simulate my-hit-pts boss)]
             #:when (equal? 'boss (player-name (first p))))
    (cond [((player-cost (second p)) . >= . (player-cost mx)) (second p)]
          [else mx])))
  


;; tests
(define me (player 'me 8 5 5 1))
(define boss (player 'boss 12 7 2 -1))
(define test-weapon (weapon 'warhammer 25 6 0))
(define test-armor (armor 'starter-jac 50 0 1))
(define test-ring1 (ring 'foo 25 1 0))
(define test-ring2 (ring 'bar 25 0 1))

(check-equal? (attack me boss) (player 'boss 9 7 2 -1))
(check-equal? (attack boss me) (player 'me 6 5 5 1))
(check-equal? (play me boss) (list (player 'me 2 5 5 1) (player 'boss 0 7 2 -1)))
(check-equal? (build-player 'test 100 test-weapon test-armor test-ring1 test-ring2) (player 'test 100 7 2 125))

;; challenge
(check-equal? (player-cost (part1 100 (player 'boss 109 8 2 -1))) 111)
(check-equal? (player-cost (part2 100 (player 'boss 109 8 2 -1))) 188)

