package main

import (
	"bufio"
	"flag"
	"fmt"
	"os"
	"regexp"
	"strconv"
	"strings"
)

func main() {
	input_file := flag.String("input_file", "", "Input filename.")
	flag.Parse()

	f, _ := os.Open(*input_file)
	r := bufio.NewScanner(f)
	re := regexp.MustCompile("Game ([0-9]+): (.*)")
	var sum int
	bag := map[string]int{
		"red":   12,
		"green": 13,
		"blue":  14}
	for r.Scan() {
		line := r.Text()

		parts := re.FindStringSubmatch(line)
		if len(parts) != 3 {
			fmt.Println("WHAT")
			return
		}
		temp, _ := strconv.ParseInt(parts[1], 10, 0)
		game_num := int(temp)
		draws := strings.Split(parts[2], ";")
		var possible bool = true
		index := 0
		for possible && index < len(draws) {
			draw := draws[index]
			cube_counts := strings.Split(draw, ",")
			for _, cube_count := range cube_counts {
				cube_count_parts := strings.Split(strings.TrimSpace(cube_count), " ")
				temp, _ := strconv.ParseInt(cube_count_parts[0], 10, 0)
				num_cubes := int(temp)
				if num_cubes > bag[cube_count_parts[1]] {
					possible = false
					break
				}
			}
			index++
		}
		if possible {
			sum += game_num
		}
	}
	fmt.Println("sum =", sum)
}
