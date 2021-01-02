#lang racket

(require rackunit)

;; predicates
(define (two-in-a-row? s)
  (regexp-match #px"([a-z])\\1" s))

(define (three-vowels? s)
  ((string-length
   (string-join (regexp-split #rx"[^aeiou]" s) "")) . > . 2))

(define (not-bad-str? x)
  (not (regexp-match #rx"(ab|cd|pq|xy)" x)))

(define predicates-one
  (list two-in-a-row? three-vowels? not-bad-str?))

;; string -> boolean
(define (nice? str predicates)
  (for/and ([p predicates])
    (p str)))

(define (nice-one? str)
  (nice? str predicates-one))

(define (part1 words)
  (length (filter nice-one? words)))

;; sample
(check-true (nice-one? "ugknbfddgicrmopn"))
(check-true (nice-one? "aaa"))
(check-false (nice-one? "jchzalrnumimnmhp"))
(check-false (nice-one? "haegwjzuvuyypxyu"))
(check-false (nice-one? "dvszwmarrgswjxmb"))

;; part1 - challenge
(define challenge (file->lines "day05.txt"))
(check-equal? (part1 challenge) 255)

;; predicates - part 2
(define (has-pair? s)
  (regexp-match #px"([a-z]{2}).*\\1" s))

(define (letter-repeat? s)
  (regexp-match #px"([a-z]).\\1" s))

(define predicates-two
  (list has-pair? letter-repeat?))

(define (nice-two? str)
  (nice? str predicates-two))

(define (part2 words)
  (length (filter nice-two? words)))

;; sample
(check-not-false (nice-two? "qjhvhtzxzqqjkmpb"))
(check-not-false (nice-two? "xxyxx"))
(check-false (nice-two? "uurcxstgmygtbstg"))
(check-false (nice-two? "ieodomkazucvgmuy"))

;; part2 - challenge
(check-equal? (part2 challenge) 55)