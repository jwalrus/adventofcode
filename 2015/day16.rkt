#lang racket

(require rackunit)

(define compounds '("children" "cats" "samoyeds" "pomeranians" "akitas"
                    "vizslas" "goldfish" "trees" "cars" "perfumes"))

(define (number-of compound s)
  (cond [(regexp-match (gen-regex compound) s) => (λ (x) (cons compound (string->number (second x))))]
        [else #f]))

(define (gen-regex compound)
  (pregexp (format "~a: ([\\d]+)" compound)))

(define (mfcsam s)
  (make-immutable-hash
    (filter identity
      (map (λ (c) (number-of c s)) compounds))))

(define (sender? aunt scan comps)
  (define aunt-hash (second aunt))
  (for/and ([cat (hash-keys aunt-hash)])
    (let ([num (hash-ref aunt-hash cat)])
      (num . (comps cat) . (hash-ref scan cat)))))

(define (part1 aunts)
  (define (comps x) =)
  (car (car (filter (λ (aunt) (sender? aunt scan comps)) challenge))))

(define (part2 aunts)
  (define (comps x)
    (cond [(equal? x "cats")        >]
          [(equal? x "trees")       >]
          [(equal? x "pomeranians") <]
          [(equal? x "goldfish")    <]
          [else                     =]))
  (car (car (filter (λ (aunt) (sender? aunt scan comps)) challenge))))
  
(define (string->aunt-sue s)
  (let ([m (regexp-match #px"Sue (\\d+): (.+)" s)])
    (list (string->number (second m)) (mfcsam (third m)))))

;; data
(define scan
  (make-immutable-hash
    (list '("children" . 3)
          '("cats" . 7)
          '("samoyeds" . 2)
          '("pomeranians" . 3)
          '("akitas" . 0)
          '("vizslas" . 0)
          '("goldfish" . 5)
          '("trees" . 3)
          '("cars" . 2)
          '("perfumes" . 1))))

(define challenge
  (map string->aunt-sue (file->lines "day16.txt")))

;; tests
(check-equal? (number-of "cats" "cats: 42") '("cats" . 42))
(check-equal? (number-of "cats" "foos: 1") #f)
(check-equal? (mfcsam "cats: 3, cars: 4, trees: 5") #hash(("cats" . 3) ("cars" . 4) ("trees" . 5)))
(check-equal? (string->aunt-sue "Sue 123: cats: 3, cars: 2") '(123 #hash(("cats" . 3) ("cars" . 2))))

;; day 16
(check-equal? (part1 challenge) 103)
(check-equal? (part2 challenge) 405)
