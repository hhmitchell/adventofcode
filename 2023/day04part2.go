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

func get_num_cards(cards []*Card) int {
	num_cards := 0
	num_copies := make([]int, len(cards))

	for i := 0; i < len(cards); i++ {
		num_cards += num_copies[i] + 1
		num_matches := cards[i].get_num_matches()
		for j := 0; j < num_matches; j++ {
			num_copies[i+j+1] += (num_copies[i] + 1)
		}
	}

	return num_cards
}

func (c *Card) get_num_matches() int {
	num_matches := 0
	for played_number := range c.played_numbers {
		if c.winning_numbers[played_number] {
			num_matches++
		}
	}

	return num_matches
}

func main() {
	input_file := flag.String("input_file", "", "Input filename.")
	flag.Parse()

	f, _ := os.Open(*input_file)
	r := bufio.NewScanner(f)

	var cards []*Card = make([]*Card, 0)
	for r.Scan() {
		var line string = r.Text()
		c := newCard(line)
		cards = append(cards, c)
	}
	fmt.Printf("Total cards = %d\n", get_num_cards(cards))
}
