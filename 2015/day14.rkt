#lang racket

(require rackunit)

(define (repeat x n)
  (for/list ([i n]) x))

(define (zeros n)
  (repeat 0 n))

(define (cycle xs n)
  (for/list ([i n]
             [j (in-cycle xs)])
    j))

(define (race deer n)
  (define seq (append (repeat (first deer) (second deer)) (zeros (third deer))))
  (rest
   (reverse
    (for/fold ([acc (list 0)])
              ([x (cycle seq n)])
     (cons (+ (first acc) x) acc)))))

(define (winner round)
  (filter identity (for/list ([i (length round)]
                              [j round])
                      (if (= (apply max round) j) i #f)))) 

(define (part1 input n)
  (apply max (map (λ (deer) (last (race deer n))) input)))

(define (part2 input n)
  (define deer-pos (map (λ (deer) (race deer n)) input))
  (define relative-pos (apply map list deer-pos))
  (define winners (apply append (map winner relative-pos)))
  (apply max (for/list ([i 9]) (length (filter (λ (x) (= i x)) winners)))))

(define (parse line)
  (let ([xs (rest (regexp-match #px".+ (\\d+) .+ (\\d+) .+ (\\d+)" line))])
    (map string->number (list (first xs) (second xs) (third xs)))))

(check-equal? (repeat 42 0) '())
(check-equal? (repeat 1 3) '(1 1 1))
(check-equal? (zeros 5) '(0 0 0 0 0))
(check-equal? (cycle '(1 2) 5) '(1 2 1 2 1))
(check-equal? (cycle (append (repeat 1 2) (zeros 2)) 7) '(1 1 0 0 1 1 0))
(check-equal? (last (race '(16 11 162) 1000)) 1056)
(check-equal? (winner (list 1 3 2 2 3 1)) '(1 4))


;; data
(define challenge (map parse (file->lines "day14.txt")))

;; challenge
(check-equal? (part1 challenge 2503) 2660)
(check-equal? (part2 challenge 2503) 1256)
