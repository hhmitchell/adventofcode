package main

import (
	"bufio"
	"flag"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Card struct {
	winning_numbers map[int]bool
	played_numbers  map[int]bool
}

func newCard(line string) *Card {
	parts := strings.SplitAfterN(line, "|", 2)
	winning_part := strings.SplitAfterN(parts[0][:len(parts[0])-1], ":", 2)

	numbers := strings.Split(winning_part[1], " ")
	winning_numbers := make(map[int]bool)
	for i := 0; i < len(numbers); i++ {
		if numbers[i] != "" {
			value, _ := strconv.ParseInt(strings.TrimSpace(numbers[i]), 10, 0)
			winning_numbers[int(value)] = true
		}
	}

	numbers = strings.Split(parts[1], " ")
	played_numbers := make(map[int]bool)
	for i := 0; i < len(numbers); i++ {
		if numbers[i] != "" {
			value, _ := strconv.ParseInt(strings.TrimSpace(numbers[i]), 10, 0)
			played_numbers[int(value)] = true
		}
	}

	return &Card{winning_numbers, played_numbers}
}

func (c *Card) get_value() int {
	value := 0
	for played_number := range c.played_numbers {
		if c.winning_numbers[played_number] {
			if value == 0 {
				value = 1
			} else {
				value *= 2
			}
		}
	}

	return value
}

func main() {
	input_file := flag.String("input_file", "", "Input filename.")
	flag.Parse()

	f, _ := os.Open(*input_file)
	r := bufio.NewScanner(f)

	sum := 0
	for r.Scan() {
		var line string = r.Text()
		c := newCard(line)
		value := c.get_value()
		sum += value
	}
	fmt.Println("Sum =", sum)
}
