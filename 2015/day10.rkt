#lang racket

(require rackunit)

(define (separate s)
  (regexp-match* #px"([0-9])\\1*" s))

(define (head s) (substring s 0 1))
(define (tail s) (substring s 1 (string-length s)))

(define (evolve s)
  (define (appd acc count char) (string-append acc (string-append (number->string count) char)))
  (define (loop acc str char count)
    (cond [(= 0 (string-length str)) (appd acc count char)]
          [(equal? char (head str))  (loop acc (tail str) char (add1 count))]
          [else (loop (appd acc count char) (tail str) (head str) 1)]))
  (loop "" (tail s) (head s) 1))

(define (char-count cs)
  (list (string-length cs) (substring cs 0 1)))

(define (char-counts s)
  (map (λ (c) (list (string-length c) (substring c 0 1))) (separate s)))

;(define (look-and-say s)
;  (for/fold ([acc ""])
;             ([p (char-counts s)])
;    (string-append acc (string-append (number->string (car p)) (cdr p)))))

(define (look-and-say s)
    (string-append*
      (map ~a (append-map char-count (separate s)))))
                     

(check-equal? (look-and-say "1") "11")
(check-equal? (look-and-say "11") "21")
(check-equal? (look-and-say "21") "1211")
(check-equal? (look-and-say "1211") "111221")
(check-equal? (look-and-say "111221") "312211")

(check-equal? (evolve "1") "11")
(check-equal? (evolve "11") "21")
(check-equal? (evolve "21") "1211")
(check-equal? (evolve "1211") "111221")
(check-equal? (evolve "111221") "312211")

(define (part1 s n)
  (for/fold ([acc s])
            ([i n])
    (look-and-say acc)))

(check-equal? (string-length (part1 "1" 5)) 6)
(check-equal? (string-length (part1 "1113122113" 40)) 360154)
(check-equal? (string-length (part1 "1113122113" 50)) 5103798)