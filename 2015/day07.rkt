#lang racket

(require rackunit)

(define rx-not #px"^NOT ([a-z]+) -> ([a-z]+)$")
(struct op-not (src dest) #:transparent)
(define (op-not-exec op map)
  (define input (hash-ref map (op-not-src op) #f))
  (if input
      (hash-set map (op-not-dest op) (+ 65536 (bitwise-not input)))
      #f))

(define rx-and #px"^([a-z1]+) AND ([a-z]+) -> ([a-z]+)$")
(struct op-and (left right dest) #:transparent)
(define (op-and-exec op map)
  (define l (hash-ref map (op-and-left op) #f))
  (define r (hash-ref map (op-and-right op) #f))
  (if (and l r)
      (hash-set map (op-and-dest op) (bitwise-and l r))
      #f))

(define rx-or  #px"^([a-z]+) OR ([a-z]+) -> ([a-z]+)$")
(struct op-or  (left right dest) #:transparent)
(define (op-or-exec op map)
  (define l (hash-ref map (op-or-left op) #f))
  (define r (hash-ref map (op-or-right op) #f))
  (if (and l r)
      (hash-set map (op-or-dest op) (bitwise-ior l r))
      #f))

(define rx-assign #px"^([0-9]+) -> ([a-z]+)$")
(struct op-assign (val dest) #:transparent)
(define (op-assign-exec op map)
  (hash-set map (op-assign-dest op) (op-assign-val op)))

(define rx-lshift #px"^([a-z]+) LSHIFT ([0-9]+) -> ([a-z]+)$")
(struct op-lshift (src val dest) #:transparent)
(define (op-lshift-exec op map)
  (define l (hash-ref map (op-lshift-src op) #f))
  (define v (op-lshift-val op))
  (if (and l v)
      (hash-set map (op-lshift-dest op) (arithmetic-shift l v))
      #f))

(define rx-rshift #px"^([a-z]+) RSHIFT ([0-9]+) -> ([a-z]+)$")
(struct op-rshift (src val dest) #:transparent)
(define (op-rshift-exec op map)
  (define l (hash-ref map (op-rshift-src op) #f))
  (define v (op-rshift-val op))
  (if (and l v)
      (hash-set map (op-rshift-dest op) (arithmetic-shift l (- v)))
      #f))

(define (parse line)
  (cond [(regexp-match rx-not line) => (λ (lst) (op-not (second lst) (third lst)))]
        [(regexp-match rx-and line) => (λ (lst) (op-and (second lst) (third lst) (fourth lst)))]
        [(regexp-match rx-or line) => (λ (lst) (op-or (second lst) (third lst) (fourth lst)))]
        [(regexp-match rx-lshift line) => (λ (lst) (op-lshift (second lst) (string->number (third lst)) (fourth lst)))]
        [(regexp-match rx-rshift line) => (λ (lst) (op-rshift (second lst) (string->number (third lst)) (fourth lst)))]
        [(regexp-match rx-assign line) => (λ (lst) (op-assign (string->number (second lst)) (third lst)))]
        [else (error (format "could not parse ~a" line))]))


(define (part1 input)

  (define (execute? map inst)
    (cond [(op-not? inst) (op-not-exec inst map)]
          [(op-and? inst) (op-and-exec inst map)]
          [(op-or? inst) (op-or-exec inst map)]
          [(op-assign? inst) (op-assign-exec inst map)]
          [(op-lshift? inst) (op-lshift-exec inst map)]
          [(op-rshift? inst) (op-rshift-exec inst map)]
          [else #f]))
  
  ;; execute loop
  (define (loop acc remaining)
    (cond [(set-empty? remaining) acc]
          [(execute? acc (first remaining)) => (λ (new-acc) (loop new-acc (rest remaining)))]
          [else (loop acc (append (rest remaining) (list (first remaining))))]))
  
  ;; go!
  (define estart (make-immutable-hash))
  (define start-acc (hash-set estart "1" 1))
  (loop start-acc input))


; challenge
(define sample
  (map parse (file->lines "day07-sample.txt")))
(define challenge
  (map parse (file->lines "day07.txt")))
(define challenge-b
  (map parse (file->lines "day07b.txt")))

(check-equal? (hash-ref (part1 sample) "y") 456)
(check-equal? (hash-ref (part1 challenge) "lx") 956)
(check-equal? (hash-ref (part1 challenge-b) "lx") 40149)
