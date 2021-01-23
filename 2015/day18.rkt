#lang racket

(require rackunit)
 

(define (neighbors pt)
  (define vecs '(-1 0 1))
  (define (add pt1 pt2)
   (list (+ (first pt1) (first pt2)) (+ (second pt1) (second pt2))))
  (define foos
    (for*/list ([i vecs]
                [j vecs]
                #:unless (and (= 0 i) (= 0 j)))
      (list i j)))
  (map (lambda (x) (add pt x)) foos))

 
(define (on-set xs always-on)
  (define n (length xs))
  (for*/set  ([i n]
              [j n]
              #:when (or (equal? #\# (string-ref (list-ref xs i) j)) (set-member? always-on (list i j))))
    (list i j)))

 
(define (on? pt lights always-on)
  (define n-on (length (filter (lambda (x) (set-member? lights x))  (neighbors pt))))
  (cond [(set-member? always-on pt) #t]
        [(set-member? lights pt)    (or (= 2 n-on) (= 3 n-on))]
        [else                       (= 3 n-on)]))


(define (evolve lights dim always-on)
 (for*/set ([i dim]
            [j dim]
            #:when (on? (list i j) lights always-on))
  (list i j)))


(define (part1 data iter)
  (define always-on (set))
  (for/fold ([acc (on-set data always-on)])
            ([i iter])
    (evolve acc (length data) always-on)))

(define (part2 data iter)
  (define n (length data))
  (define m (sub1 n))
  (define always-on (set (list 0 0) (list 0 m) (list m 0) (list m m)))
  (for/fold ([acc (on-set data always-on)])
            ([i iter])
    (evolve acc (length data) always-on)))


(define sample
  '(".#.#.#"
    "...##."
    "#....#"
    "..#..."
    "#.#..#"
    "####.."))

(define challenge (file->lines "day18.txt"))


(check-equal? (length (set->list (part1 sample 1))) 11)
(check-equal? (length (set->list (part1 sample 2))) 8)
(check-equal? (length (set->list (part1 sample 3))) 4)
(check-equal? (length (set->list (part1 sample 4))) 4)
(check-equal? (length (set->list (part1 challenge 100))) 768)

(check-equal? (length (set->list (part2 sample 1))) 18)
(check-equal? (length (set->list (part2 sample 2))) 18)
(check-equal? (length (set->list (part2 sample 3))) 18)
(check-equal? (length (set->list (part2 sample 4))) 14)
(check-equal? (length (set->list (part2 sample 5))) 17)
(check-equal? (length (set->list (part2 challenge 100))) 781)
