#lang racket

(require rackunit)
(require file/md5)


(define (target-hash? secret-key num target)
  (define key (string-append secret-key (number->string num)))
  (define md5-hash (md5 key))
  (equal? target (subbytes md5-hash 0 (bytes-length target))))


(define (day4 secret-key target)
  (define (go n)
    (cond [(target-hash? secret-key n target) n]
          [else (go (add1 n))]))
  (go 1))


;; tests
(check-equal? (target-hash? "abcdef" 609043 #"00000") #t)
(check-equal? (target-hash? "abcdef" 609042 #"00000") #f)
(check-equal? (target-hash? "pqrstuv" 1048970 #"00000") #t)
(check-equal? (day4 "abcdef" #"00000") 609043 )

;; challenge
(define CHALLENGE "yzbqklnj")
(check-equal? (day4 CHALLENGE #"00000") 282749)
(check-equal? (day4 CHALLENGE #"000000") 9962624)