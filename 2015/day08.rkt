#lang racket

(require rackunit)

(define (num-code s)
  (string-length s))

(define (num-mem s)
  (string-length (read (open-input-string s))))

(define (num-enc s)
  (string-length (format "~v" s)))

(define (string-counts s)
  (cons (num-code s) (num-mem s)))

(define (string-count-diff s)
  (define counts (string-counts s))
  (- (car counts) (cdr counts)))

(define (part1 input)
  (for/fold ([acc 0])
            ([i input])
    (+ acc (string-count-diff i))))

(define (part2 input)
  (- (apply + (map num-enc input)) (apply + (map num-code input))))

;; samples
(check-equal? (string-counts "\"\"") '(2 . 0))
(check-equal? (string-counts "\"abc\"") '(5 . 3))
(check-equal? (string-counts "\"aaa\\\"aaa\"") '(10 . 7))
(check-equal? (string-counts "\"\\x27\"") '(6 . 1))

;; data
(define sample (file->lines "day08-sample.txt"))
(define challenge (file->lines "day08.txt"))

;; part1
(check-equal? (part1 sample) 12)
(check-equal? (part1 challenge) 1350)

;; part2
(check-equal? (part2 sample) 19)
(check-equal? (part2 challenge) 2085)