package main

import (
	"bufio"
	"flag"
	"fmt"
	"os"
	"regexp"
	"strconv"
)

func store(value int, begin **int, end **int) {
	if *begin == nil {
		*begin = new(int)
		**begin = value
	} else {
		if *end == nil {
			*end = new(int)
		}
		**end = value
	}
}

func main() {
	input_file := flag.String("input_file", "", "Input filename.")
	flag.Parse()

	f, _ := os.Open(*input_file)
	r := bufio.NewScanner(f)
	digits := map[string]int{
		"one":   1,
		"two":   2,
		"three": 3,
		"four":  4,
		"five":  5,
		"six":   6,
		"seven": 7,
		"eight": 8,
		"nine":  9}
	re := regexp.MustCompile("[1-9]|one|two|three|four|five|six|seven|eight|nine")
	var sum int
	for r.Scan() {
		line := r.Bytes()
		var begin, end *int

		for index := 0; index < len(string(line)); index += 1 {
			match := re.Find(line[index:])
			if match == nil {
				break
			}
			digit := string(match)
			if value, ok := digits[digit]; ok {
				store(value, &begin, &end)
			} else {
				value, _ := strconv.ParseInt(digit, 10, 0)
				store(int(value), &begin, &end)
			}
		}
		if end == nil {
			end = new(int)
			*end = *begin
		}
		sum = sum + *begin*10 + *end
	}
	fmt.Println("sum = ", sum)
}
