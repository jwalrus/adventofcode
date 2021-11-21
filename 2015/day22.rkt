#lang racket

(require rackunit)


(struct player (name hit-pts damage mana mana-spent) #:transparent)


(define (mk-player name hit-pts damage [mana -1] [mana-spent 0])
  (player name hit-pts damage mana mana-spent))


(define (heal p pts)
  (player (player-name p) (+ (player-hit-pts p) pts) (player-damage p) (player-mana p) (player-mana-spent p)))


(define (spend-mana p cost)
  (player (player-name p) (player-hit-pts p) (player-damage p) (- (player-mana p) cost) (+ (player-mana-spent p) cost)))


(define (attack p damage armor)
  (let ([new-pts (- (player-hit-pts p) (max 1 (- damage armor)))])
    (player (player-name p) new-pts (player-damage p) (player-mana p) (player-mana-spent p))))


(define (attack-player boss p [player-armor 0])
  (attack p (player-damage boss) player-armor))


(define (attack-boss p boss pts)
  (attack boss pts 0))


(define (magic-missile p b )
  (list (spend-mana p 53) (attack-boss p b 4)))


(define (drain p b)
  (list (heal (spend-mana p 73) 2) (attack-boss p b 2)))




;; tests
(define test-player (mk-player 'test-p 10 0 100))
(define test-boss (mk-player 'boss 15 9))

(check-equal? (attack-player test-boss test-player) (player 'test-p 1 0 100 0))
(check-equal? (magic-missile test-player test-boss) (list (player 'test-p 10 0 47 53) (player 'boss 11 9 -1 0)))
(check-equal? (drain test-player test-boss) (list (player 'test-p 12 0 27 73) (player 'boss 13 9 -1 0)))

  
