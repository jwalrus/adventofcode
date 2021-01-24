#lang racket

(require rackunit)

(define (subs s)
  (reverse
    (for/fold ([acc '()])
              ([i (string-length s)])
      (cons (substring s i) acc))))
              

(define (gen-molecules replacements molecule)
  (for/set ([c (subs molecule)]
            [i (string-length molecule)]
            #:when #t
            [r replacements]
            #:when (string-prefix? c (first r)))
    (string-append
      (substring molecule 0 i)
      (second r)
      (substring molecule (+ i (string-length (first r)))))))

(define (string->replacement s)
  (map string-trim (string-split s "=>")))



;; data
(define sample
  '(("H" "HO") ("H" "OH") ("O" "HH")))

(define raw-input (file->string "day19.txt"))

(define replacements
  (let ([rs (first (string-split raw-input "\n\n"))])
    (map string->replacement (string-split rs "\n"))))

(define challenge
  (string-trim (second (string-split raw-input "\n\n")) "\n"))

;; tests
(check-equal?
 (gen-molecules sample "HOH")
 (set "HOOH" "HOHO" "OHOH" "HHHH"))

(check-equal?
 (length (set->list (gen-molecules sample "HOHOHO")))
 7)

(check-equal?
 (map string->replacement '("H => HO" "O => OO"))
 '(("H" "HO") ("O" "OO")))

(check-equal?
 (length (set->list (gen-molecules replacements challenge)))
 518)



