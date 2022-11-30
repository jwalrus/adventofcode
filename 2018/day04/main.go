package main

import (
	"aoc2018/util"
	"fmt"
	"os"
	"regexp"
	"sort"
	"strconv"
	"strings"
	"time"
)

func main() {
	part := os.Args[1]
	filename := os.Args[2]

	lines := util.ReadInput(filename)
	ts := parseLines(lines)

	fmt.Println("Day 04, 2018")
	switch part {
	case "1":
		fmt.Printf("part1: %v\n", part1(ts))
	case "2":
		fmt.Printf("part2: %v\n", part2(ts))
	default:
		x := parseLine("[1518-11-01 23:58] Guard #99 begins shift")
		fmt.Println(x)
	}
}

func part1(records []Record) string {

	var cur int64
	var sleep int

	for _, r := range records {
		fmt.Printf("%s\n", r.date)

		switch r.msg[:5] {
		case "Guard":
			cur = guardNumber(r.msg)
			fmt.Printf("current guard is %d\n", cur)
		case "falls":
			sleep = r.minute
			fmt.Printf("Guard %d falls asleep at %d\n", cur, r.minute)
		case "wakes":
			fmt.Printf("Guard %d slept from %d to %d\n", cur, sleep, r.minute)
		}
	}
	return ""
}

func part2(records []Record) string {
	return ""
}

type Record struct {
	time   time.Time
	date   string
	minute int
	msg    string
}

type Gaurd struct {
	ID            int
	sleepCalendar SleepCalendar
}

type SleepCalendar struct {
	cal map[time.Time][]bool
}

func (sc SleepCalendar) add(t time.Time) {
	cal, ok := sc.cal[t]
	if !ok {
		cal = make([]bool, 60)
		sc.cal[t] = cal
	}

	cal[t.Minute()] = true
}

func (sc SleepCalendar) totalMinutesSleeping() int {
	result := 0

	for _, arr := range sc.cal {
		for _, min := range arr {
			if min {
				result++
			}
		}
	}

	return result
}

func parseLines(lines []string) []Record {
	result := make([]Record, 0)
	for _, line := range lines {
		result = append(result, parseLine(line))
	}

	sort.Slice(result, func(i, j int) bool {
		return result[i].time.Before(result[j].time)
	})

	return result
}

func parseLine(line string) Record {
	t, err := time.Parse(`2006-01-02 15:04`, line[1:17])
	if err != nil {
		panic(err)
	}
	date := strings.Trim(line[1:11], " ")
	msg := strings.Trim(line[19:], " ")
	return Record{time: t, date: date, minute: t.Minute(), msg: msg}
}

func guardNumber(s string) int64 {
	regex := regexp.MustCompile("Guard #(?P<id>\\d+) begins shift")
	match := regex.FindStringSubmatch(s)
	id, _ := strconv.ParseInt(match[1], 10, 64)
	return id
}
