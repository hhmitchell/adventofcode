package main

import (
	"bufio"
	"flag"
	"fmt"
	"os"
	"strconv"
)

type Gear struct {
	i, j      int
	parts     []int
	num_parts int
}

type Schematic struct {
	num_rows  int
	capacity  int
	schematic []string
	gears     []*Gear
	num_gears int
}

func newSchematic() Schematic {
	init_capacity := 2
	return Schematic{0, init_capacity, make([]string, init_capacity), nil, 0}
}

func newGear(i, j int) *Gear {
	return &Gear{i, j, make([]int, 8), 0}
}

func (s *Schematic) get_num_rows() int {
	return s.num_rows
}

func (s *Schematic) add_row(row string) {
	if s.num_rows == s.capacity {
		var temp = make([]string, 2*s.capacity)
		for i := 0; i < s.capacity; i++ {
			temp[i] = s.schematic[i]
		}
		s.schematic = temp
		s.capacity *= 2
	}
	s.schematic[s.num_rows] = row
	s.num_rows = s.num_rows + 1
}

func (g *Gear) add_part(part_number int) {
	g.parts[g.num_parts] = part_number
	g.num_parts = g.num_parts + 1
}

func (s *Schematic) add_gear_part(i, j, part_number int) {
	if s.gears == nil {
		s.gears = make([]*Gear, s.num_rows*len(s.schematic[0]))
		s.num_gears = 0
	}

	for index := 0; index < s.num_gears; index++ {
		gear := s.gears[index]
		if gear.i == i && gear.j == j {
			gear.add_part(part_number)
			return
		}
	}

	gear := newGear(i, j)
	gear.add_part(part_number)
	s.gears[s.num_gears] = gear
	s.num_gears++
}

func (s *Schematic) read_schematic() int {
	for i := 0; i < s.num_rows; i++ {
		row := s.schematic[i]
		start := 0
		end := 0
		for start < len(row) {
			char := row[start]
			if is_digit(char) {
				if start < len(row)-1 {
					end = start + 1
					for end < len(row) {
						char := row[end]
						if is_digit(char) {
							end++
						} else {
							break
						}
					}
				} else {
					end = start
				}
				part_number, _ := strconv.ParseInt(row[start:end], 10, 0)
				s.check_gear(i, start, end-1, int(part_number))
				start = end + 1
			} else {
				start++
			}
		}
	}

	var sum int
	for i := 0; i < s.num_gears; i++ {
		gear := s.gears[i]
		if gear.num_parts == 2 {
			sum += gear.parts[0] * gear.parts[1]
		}
	}

	return sum
}

func is_gear(char byte) bool {
	return char == '*'
}
func is_digit(char byte) bool {
	return char >= '0' && char <= '9'
}

func (s *Schematic) check_gear(row_num, start, end, part_number int) {
	if row_num > 0 {
		i := row_num - 1
		j_start := start
		j_end := end
		if start > 0 {
			j_start = start - 1
		}
		if end < len(s.schematic[i])-1 {
			j_end = end + 1
		}
		for j := j_start; j <= j_end; j++ {
			if is_gear(s.schematic[i][j]) {
				s.add_gear_part(i, j, part_number)
			}
		}
	}
	if row_num < s.num_rows-1 {
		i := row_num + 1
		var j_start, j_end int
		if start > 0 {
			j_start = start - 1
		}
		if end < len(s.schematic[i])-1 {
			j_end = end + 1
		}
		for j := j_start; j <= j_end; j++ {
			if is_gear(s.schematic[i][j]) {
				s.add_gear_part(i, j, part_number)
			}
		}
	}

	if start > 0 {
		if is_gear(s.schematic[row_num][start-1]) {
			s.add_gear_part(row_num, start-1, part_number)
		}
	}
	if end < len(s.schematic[row_num])-1 {
		if is_gear(s.schematic[row_num][end+1]) {
			s.add_gear_part(row_num, end+1, part_number)
		}
	}
}

func main() {
	input_file := flag.String("input_file", "", "Input filename.")
	flag.Parse()

	s := newSchematic()

	f, _ := os.Open(*input_file)
	r := bufio.NewScanner(f)
	for r.Scan() {
		var line string = r.Text()
		s.add_row(line)
	}
	fmt.Printf("Sum = %d\n", s.read_schematic())
}
