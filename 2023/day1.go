package main

import (
  "bufio"
  "fmt"
  "flag"
  "os"
  "strconv"
)

func main() {
  input_file := flag.String("input_file", "", "Input filename.")
  flag.Parse()

  f, _ := os.Open(*input_file)
  r := bufio.NewScanner(f)
  var sum int
  for r.Scan() {
    var begin, end *int
    line := r.Text()
    for _, char := range line {
      if char >= '0' && char <= '9' {
        if begin == nil {
          begin = new(int)
          temp, _ := strconv.ParseInt(string(char), 10, 0)
          *begin = int(temp)
        } else {
          if end == nil {
            end = new(int)
          }
          temp, _ := strconv.ParseInt(string(char), 10, 0)
          *end = int(temp)
        }
      }
    }
    if end == nil {
      end = new(int)
      *end = *begin
    }
    sum = sum + *begin * 10 + *end
  }
  fmt.Println("sum = ", sum)
}
