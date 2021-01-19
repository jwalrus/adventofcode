#lang racket

(require rackunit)

(define (powerset xs)
  (if (empty? xs)
      (list empty)
      (append-map (λ (x) (list (cons (first xs) x) x)) (powerset (rest xs)))))

(check-equal? (powerset '()) '(()) )
(check-equal? (powerset '(1)) '((1) ()))
(check-equal? (powerset '(1 2)) '((1 2) (2) (1) ()))
(check-equal? (powerset '(1 2 3)) '((1 2 3) (2 3) (1 3) (3) (1 2) (2) (1) ()))

;; part 1
(define (part1 xs n)
    (filter (λ (x) (= (apply + x) n))
      (powerset xs)))

(check-equal? (length (part1 '(5 5 10 15 20) 25)) 4)

(define combos (part1 '(11 30 47 31 32 36 3 1 5 3 32 36 15 11 46 26 28 1 19 3) 150))
(check-equal? (length combos) 4372)


;; part 2
(define min-len
  (apply min (map (λ (x) (length x)) combos)))

(check-equal?
  (length
    (filter (λ (x) (= min-len (length x))) combos))
      4)

