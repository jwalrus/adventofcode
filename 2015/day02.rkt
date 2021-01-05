#lang racket

(require rackunit)

(struct gift (x y z) #:transparent)


(define (gift-area g)
  (let* ([x (gift-x g)]
         [y (gift-y g)]
         [z (gift-z g)]
         [area (* 2 (+ (* x y) (* y z) (* x z)))]
         [slack (min (* x y) (* y z) (* x z))])
    (+ area slack)))

 
(define (ribbon-len g)
  (let* ([x (gift-x g)]
         [y (gift-y g)]
         [z (gift-z g)]
         [ribbon (* 2 (min (+ x y) (+ y z) (+ x z)))]
         [bow (* x y z)])
     (+ ribbon bow)))

 
(check-equal? (gift-area (gift 2 3 4)) 58)
(check-equal? (gift-area (gift 1 1 10)) 43) 


(define (list->gift xs)
  (gift (first xs) (second xs) (third xs)))

 
(define (line->gift line)
  (list->gift
    (map string->number
      (string-split line "x"))))

 
(define challenge
  (map line->gift (file->lines "day02.txt")))

 
(define part1
  (for/fold ([acc 0])
            ([gift challenge])
    (+ acc (gift-area gift))))

 
(define part2
  (for/fold ([acc 0])
            ([gift challenge])
    (+ acc (ribbon-len gift))))


(check-equal? part1 1586300)
(check-equal? part2 3737498)
