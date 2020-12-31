#lang racket

(require rackunit)


(define (day1 input cutoff)
  (for/fold ([floor 0]
             [iter  0])
            ([i input])
            #:break (floor . < . cutoff)
    (cond [(equal? i #\() (values (add1 floor) (add1 iter))]
          [else           (values (sub1 floor) (add1 iter))])))

(define (part1 input)
  (let-values ([(floor iter) (day1 input -100000)]) floor))

(define (part2 input)
  (let-values ([(floor iter) (day1 input 0)]) iter))
  
;; SAMPLES
(check-equal? 0 (part1 "(())"))
(check-equal? 0 (part1"()()"))
(check-equal? 3 (part1 "(()(()("))
(check-equal? -3 (part1 ")())())"))


;; PART 1 & 2
(define challenge-input (string-trim (file->string "day01.txt")))
(check-equal? 138 (part1 challenge-input))
(check-equal? 1771 (part2 challenge-input))


