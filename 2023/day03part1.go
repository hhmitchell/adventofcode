package main

import (
  "bufio"
  "flag"
  "fmt"
  "os"
  "strconv"
)

type Schematic struct {
  num_rows int
  capacity int
  schematic []string
}

func newSchematic() Schematic {
  init_capacity := 2
  return Schematic{0, init_capacity, make([]string, init_capacity)}
}

func (s *Schematic) get_num_rows() int {
  return s.num_rows
}

func (s *Schematic) add_row(row string) {
  if s.num_rows == s.capacity {
    var temp = make([]string, 2 * s.capacity)
    for i := 0; i < s.capacity; i++ {
      temp[i] = s.schematic[i]
    }
    s.schematic = temp
    s.capacity *= 2
  }
  s.schematic[s.num_rows] = row
  s.num_rows = s.num_rows + 1
}

func (s *Schematic) foo() int {
  var sum int
  for i:=0; i < s.num_rows; i++ {
    row := s.schematic[i]
    start := 0
    end := 0
    for start < len(row) {
      char := row[start]
      if is_digit(char) {
        if start < len(row) - 1 {
          end = start +1
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
        if s.is_part_number(i, start, end - 1) {
          part_number, _ := strconv.ParseInt(row[start:end], 10, 0)
          sum += int(part_number)
        }
        start = end +1
      } else {
        start++
      }
    }
  }
  return sum
}

func is_symbol(char byte) bool {
  return !is_digit(char) && char != '.'
}
func is_digit(char byte) bool {
  return char >= '0' && char <= '9'
}
func (s *Schematic) is_part_number(row_num, start, end int) bool {
  if row_num > 0 {
    i := row_num - 1
    j_start := start
    j_end := end
    if start > 0 {
      j_start = start -1
    }
    if end < len(s.schematic[i]) - 1 {
      j_end = end + 1
    }
    for j := j_start; j <= j_end; j++ {
      if is_symbol(s.schematic[i][j]) {
        return true
      }
    }
  }
  if row_num < len(s.schematic) - 1 {
    i := row_num + 1
    var j_start, j_end int
    if start > 0 {
      j_start = start -1
    }
    if end < len(s.schematic[i]) - 1 {
      j_end = end + 1
    }
    for j := j_start; j <= j_end; j++ {
      if is_symbol(s.schematic[i][j]) {
        return true
      }
    }
  }

  if start > 0 {
    if is_symbol(s.schematic[row_num][start-1]) {
      return true
    }
  }
  if end < len(s.schematic[row_num]) - 1 {
    if is_symbol(s.schematic[row_num][end+1]) {
      return true
    }
  }
  return false
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
  fmt.Printf("Sum = %d\n", s.foo())
}
