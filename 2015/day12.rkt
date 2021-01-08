#lang racket

(require json)
(require rackunit)

(define (part1 s)
  (apply + (map string->number
              (regexp-match* #px"([-]?\\d+)" s))))

(define (filter-reds js)
  (flatten 
    (cond [(list? js) (map filter-reds js)]
          [(hash? js) (if (member "red" (hash-values js)) empty (map filter-reds (hash-values js)))]
          [else js])))

(define (part2 s)
  (define no-reds (filter-reds (string->jsexpr s)))
  (apply + (filter number? no-reds)))


;; challenge
(define challenge (file->string "day12.txt"))
(check-equal? (part1 challenge) 156366)
(check-equal? (part2 "[1,2,3]") 6)
(check-equal? (part2 "[1,{\"c\":\"red\",\"b\":2},3]") 4)
(check-equal? (part2 "{\"d\":\"red\",\"e\":[1,2,3,4],\"f\":5}") 0)
(check-equal? (part2 challenge) 96852)
