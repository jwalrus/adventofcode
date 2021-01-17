#lang racket

(require rackunit)

(struct ingredient (name capacity durability flavor texture calories) #:transparent)

(define (string->ingredient s)
  (define ptrn #px"([A-Za-z]+): capacity ([-\\d]+), durability ([-\\d]+), flavor ([-\\d]+), texture ([-\\d]+), calories ([-\\d]+)")
  (define (f g xs) (string->number (g xs)))
  (let ([m (regexp-match ptrn s)])
    (ingredient (second m) (f third m) (f fourth m) (f fifth m) (f sixth m) (f seventh m))))  

(define (score ingredients weights)
  (define zipped (map list ingredients weights))
  (define getters (list ingredient-capacity ingredient-durability ingredient-flavor ingredient-texture))
  (for*/product ([getter getters])
    (let ([score (apply + (map (λ (pair) (* (getter (first pair)) (second pair))) zipped))])
      (if (score . > . 0) score 0))))

(define (calories ingredients weights)
  (define zipped (map list ingredients weights))
  (apply + (map (λ (pair) (* (ingredient-calories (first pair)) (second pair))) zipped)))

(define (part1 ingredients)
  (for*/fold ([mx 0])
            ([a 100]
             [b 100]
             [c 100]
             [d 100]
             #:when (= 100 (+ a b c d)))
    (define weights (list a b c d))
    ;; was lazy -> remove the cond to run part 1
    (cond [(= 500 (calories ingredients weights))
             (let ([x (score ingredients weights)])
               (if (x . > . mx) x mx))]
          [else mx])))  

;; data
(define sample
  (map string->ingredient
    '("Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8"
      "Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3")))

(define challenge
  (map string->ingredient
    '("Sprinkles: capacity 2, durability 0, flavor -2, texture 0, calories 3"
      "Butterscotch: capacity 0, durability 5, flavor -3, texture 0, calories 3"
      "Chocolate: capacity 0, durability 0, flavor 5, texture -1, calories 8"
      "Candy: capacity 0, durability -1, flavor 0, texture 5, calories 8")))

;; tests
(check-equal? (score sample '(44 56)) 62842880)
;(check-equal? (part1 sample) 62842880)
;(check-equal? (part1 challenge) 21367368)
(check-equal? (part1 challenge) 1766400)