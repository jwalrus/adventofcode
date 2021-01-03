#lang racket

(require rackunit)

; create x-by-x grid of 0s
(define (make-grid x)
  (for/vector ([i x])
    (make-vector x 0)))

; create block of coordinates
(define (coords pair1 pair2)
  (for*/list ([i (range (car pair1) (add1 (car pair2)))]
              [j (range (cdr pair1) (add1 (cdr pair2)))])
    (cons i j)))

; update point in grid
(define (grid-set f grid pair)
  (define x (car pair))
  (define y (cdr pair))
  (define value (f (vector-ref (vector-ref grid y) x)))
  (vector-set!
    (vector-ref grid y) x value))

; update section of grid
(define (grid-set-section update-func grid bottom-left top-right)
  (for-each (λ (pair) (grid-set update-func grid pair)) (coords bottom-left top-right)))

; supplies the update function (bit -> bit)
(define (update-func x)
  (cond [(equal? "turn on" x)  (λ (x) 1)]
        [(equal? "turn off" x) (λ (x) 0)]
        [else                  (λ (x) (if (= x 0) 1 0))]))

(define (update-part2 x)
  (cond [(equal? "turn on" x)  (λ (x) (add1 x))]
        [(equal? "turn off" x) (λ (x) (if (= x 0) 0 (sub1 x)))]
        [else                  (λ (x) (+ x 2))]))

; parse input
(define (parse line)
  (define xs (regexp-match #px"(turn on|turn off|toggle) ([\\d]+),([\\d]+) through ([\\d]+),([\\d]+)" line))
  (define (to-pair s1 s2) (cons (string->number s1) (string->number s2)))
  (define action (second xs))
  (define pair1 (to-pair (third xs) (fourth xs)))
  (define pair2 (to-pair (fifth xs) (sixth xs)))
  (list action pair1 pair2))

(define (grid-sum grid)
  (for/fold ([acc 0])
            ([i grid])
    (cond [(vector? i) (+ acc (grid-sum i))]
          [else        (+ acc i)]))) 

(define (day6 input fs)
  (define grid (make-grid 1000))
  (define (loop round)
    (define f (fs (first round)))
    (define pair1 (second round))
    (define pair2 (third round))
    (grid-set-section f grid pair1 pair2))
  (for-each (λ (line) (loop line)) input)
  (grid-sum grid))

(define (part1 input) (day6 input update-func))
(define (part2 input) (day6 input update-part2))

;; tests
(define test (make-grid 3))
(grid-set (λ (x) 1) test (cons 2 1))
(grid-set (λ (x) 1) test (cons 1 0))

(define test1 (make-grid 5))
(grid-set-section (update-func "turn-on") test1 (cons 1 1) (cons 2 4))
; test
; test1

;; challenge
(define challenge (map parse (file->lines "day06.txt")))
(check-equal? (part1 challenge) 569999)
(part2 challenge)

