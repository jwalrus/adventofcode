#lang racket


(require rackunit)


(define (upper-bound n)
  (inexact->exact (ceiling (sqrt n))))


(define (factors n)
  (cond [(= 1 n) '(1)]
        [else
         (let ([xs (for/list ([m (in-range 1 (add1 (upper-bound n)))]  #:when (= 0 (modulo n m))) m)])
           (remove-duplicates (append xs (reverse (map (λ (x) (/ n x)) xs)))))]))


(define (part1 target [i 0])
  (let ([num-presents (apply + (map (λ (x) (* 10 x)) (factors i)))])
    (cond [(num-presents . >= . target) i]
          [else (part1 target (add1 i))])))


(define (part2 target [i 1])
  (define workers (filter (λ (x) ((quotient i x) . <= . 50)) (factors i)))
  (define num-presents (apply + (map (λ (x) (* 11 x)) workers)))
  (cond [(num-presents . >= . target) i]
        [else (part2 target (add1 i))]))


;; tests
(check-equal? (factors 4) '(1 2 4))
(check-equal? (factors 5) '(1 5))
(check-equal? (factors 8) '(1 2 4 8))
(check-equal? (factors 12) '(1 2 3 4 6 12))
(check-equal? (part1 120) 6)
(check-equal? (part1 80) 6)
(check-equal? (part1 130) 8)

;; challenge
(check-equal? (part1 33100000) 776160)
(check-equal? (part2 33100000) 786240)
