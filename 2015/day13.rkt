#lang racket

(require rackunit)

(define (people-set input)
  (set->list (apply set (map first input))))

(define (happiness-map input)
  (let ([entries (map (λ (x) (list (take x 2) (third x))) input)])
    (make-hash entries)))

(define (parse line)
  (let ([x (rest (regexp-match #px"^(.+) would (.+) (\\d+) happiness units by sitting next to (.+)\\.$" line))])
    (list (first x) (fourth x) (* (string->number (third x)) (if (equal? (second x) "gain") 1 -1)))))

(define (seating-utility input)
  (define people (people-set input))
  (define lookup-map (happiness-map input))
  (define (lookup a b) (car (hash-ref lookup-map (list a b) '(0))))
  (define (score a b) (+ (lookup a b) (lookup b a)))
  (define head-of-table (first people))
  (define arrangements (permutations people))

  (define (utility arrangement)
    (let ([pairs (map cons arrangement (append (rest arrangement) (list (first arrangement))))])
      (apply + (map (λ (pr) (score (car pr) (cdr pr))) pairs))))

  (apply max (map utility arrangements)))

;; data
(define sample (map parse (file->lines "day13-sample.txt")))
(define challenge (map parse (file->lines "day13.txt")))

;; part 1
(check-equal? (seating-utility sample) 330)
(check-equal? (seating-utility challenge) 709)

;; part 2
(define challenge2 (cons '('me 'any 0) challenge))
(check-equal? (seating-utility challenge2) 668)