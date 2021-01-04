#lang racket

 (require rackunit)


(define (next direction p)
  (cond [(equal? direction #\^) (+ p 0.0+1.0i)]
        [(equal? direction #\>) (+ p 1.0+0.0i)]
        [(equal? direction #\v) (+ p 0.0-1.0i)]
        [(equal? direction #\<) (+ p -1.0+0.0i)]))


(define (path input)
  (for/fold ([position 0.0+0.0i]
             [acc '(0.0+0.0i)]
             #:result acc)
            ([i input])
   (values (next i position) (cons (next i position) acc))))


(define (robo-path input)
  (for/fold ([santa-position 0.0+0.0i]
             [robot-position 0.0+0.0i]
             [acc '(0.0+0.0i)]
             [ix 0]
             #:result acc)
            ([i input])
    (cond [(odd? ix) (values (next i santa-position)
                             robot-position
                             (cons (next i santa-position) acc)
                             (add1 ix))]
          [else      (values santa-position
                             (next i robot-position)
                             (cons (next i robot-position) acc)
                             (add1 ix))])))
 

(define (part1 input)
  (set-count
     (list->set
       (path input))))


(define (part2 input)
  (set-count
    (list->set
       (robo-path input))))

 
(check-equal? (path "^>v<") '(0.0+0.0i 1.0+0.0i 1.0+1.0i 0.0+1.0i 0.0+0.0i))
(check-equal? (part1 "^v^v^v^v^v") 2)
(check-equal? (part1 "^>v<^>v<^>v<") 4)
(check-equal? (part1 "^^^^^^^^^") 10)
(check-equal? (part1 "^") 2)

;; challenge
(check-equal? (part1 (file->string "day03.txt")) 2592)
(check-equal? (part2 (file->string "day03.txt")) 2360)