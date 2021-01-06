#lang racket

(require rackunit)

(struct route (city-a city-b dist) #:transparent)

(define (parse line)
  (define tmp  (regexp-match #px"([A-Za-z]+) to ([A-Za-z]+) = ([0-9]+)" line))
  (route (second tmp) (third tmp) (string->number (fourth tmp))))

(define (city-set routes)
  (for*/set ([route routes]
             [city (list (route-city-a route) (route-city-b route))])
    city))

(define (make-dist-lookup routes)
  (define a-b (map (λ (route) (cons (cons (route-city-a route) (route-city-b route)) (route-dist route))) routes))
  (define b-a (map (λ (route) (cons (cons (route-city-b route) (route-city-a route)) (route-dist route))) routes))
  (make-hash (append a-b b-a)))

(define (tsp f routes)
  (define cities (set->list (city-set routes)))
  (define distances (make-dist-lookup routes))
  (define (distance a b) (hash-ref distances (cons a b) 0))
  (define (recur loc remaining)
    (cond [(empty? remaining) 0]
          [else (apply f (map (λ (x) (+ (distance loc x) (recur x (remq x remaining)))) remaining))]))
  ; run
  (recur 'none cities))    


;; tests
(check-equal? (route-city-a (route "London" "Fooburgh" 100)) "London")
(check-equal? (route-dist (route "London" "Fooburgh" 100)) 100)
(check-equal? (parse "Foo to Bar = 123") (route "Foo" "Bar" 123))

;; challenge
(define sample (map parse (file->lines "day09-sample.txt")))
(define challenge (map parse (file->lines "day09.txt")))
(check-equal? (tsp min sample) 605)
(check-equal? (tsp min challenge) 251)
(check-equal? (tsp max sample) 982)
(check-equal? (tsp max challenge) 898)
