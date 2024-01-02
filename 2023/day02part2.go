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
	for r.Scan() {
		line := r.Text()

		parts := re.FindStringSubmatch(line)
		if len(parts) != 3 {
			fmt.Println("WHAT")
			return
		}
		draws := strings.Split(parts[2], ";")
		var possible bool = true
		var game_bag = map[string]int{
			"red":   0,
			"green": 0,
			"blue":  0}
		index := 0
		for possible && index < len(draws) {
			draw := draws[index]
			cube_counts := strings.Split(draw, ",")
			for _, cube_count := range cube_counts {
				cube_count_parts := strings.Split(strings.TrimSpace(cube_count), " ")
				temp, _ := strconv.ParseInt(cube_count_parts[0], 10, 0)
				num_cubes := int(temp)
				if game_bag[cube_count_parts[1]] < num_cubes {
					game_bag[cube_count_parts[1]] = num_cubes
				}
			}
			index++
		}
		sum += game_bag["red"] * game_bag["green"] * game_bag["blue"]
	}
	fmt.Println("sum =", sum)
}
