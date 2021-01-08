#lang racket

(require rackunit)

(define (string-rest s) (substring s 1 (string-length s)))

(define (conseq? abc)
  (define vals (map char->integer (string->list abc)))
  (and (= 1 (- (second vals) (first vals))) (= 2 (- (third vals) (first vals)))))

(define (three-letters? password)
  (define abc (if (< (string-length password) 3) #f (substring password 0 3)))
  (cond [(not abc) #f]
        [(conseq? abc) #t]
        [else (three-letters? (string-rest password))]))

(define (no-bad-letters? s)
  (not (regexp-match #rx"[iol]" s)))

(define (two-doubles? s)
  (regexp-match #px"([a-z])\\1.*([a-z])\\2" s))

(define (good-pass? p)
  (and (three-letters? p) (no-bad-letters? p) (two-doubles? p)))

(define (next-char c)
  (if (equal? #\z c)
      #\a
      (integer->char (add1 (char->integer c)))))

(define (next pass new-pass)
  (define c (first pass))
  (cond [(or (empty? new-pass) (for/and ([ch new-pass]) (equal? #\a ch))) (next-char c)] ;; need to check (car new-pass) all #\a
        [else c]))

(define (iter pass-list)
  (define pass (if (list? pass-list) pass-list (string->list pass-list)))
  (cond [(empty? pass) pass]
        [else (let ([x (iter (rest pass))])
                (cons (next pass x) x))]))

(define (next-pass pass)
  (let ([next (string-append* (map ~a (iter pass)))])
    (cond [(good-pass? next) next]
          [else (next-pass next)])))


(check-not-false (good-pass? "abcdffaa"))
(check-not-false (good-pass? "ghjaabcc"))
(check-equal? (next-pass "abcdefgh") "abcdffaa")
(check-equal? (next-pass "ghijklmn") "ghjaabcc")

; challenge
(check-equal? (next-pass "hxbxwxba") "hxbxxyzz")
(check-equal? (next-pass "hxbxxyzz") "hxcaabcc")
  
