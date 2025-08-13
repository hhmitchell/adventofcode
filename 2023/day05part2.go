package main

import (
  //"bufio"
  //"flag"
  "fmt"
  //"os"
  "strconv"
  "strings"
)

type Span struct {
  start int
  end int
}

func newSpan(start int, size int) *Span {
  return &Span{start, start + size - 1}
}

func (s *Span) printf() {
  fmt.Printf("Span(%d, %d)", s.start, s.end)
}

type Range struct {
  source_span Span
  dest_start int
}
type RangeMap struct {
  ranges []*Range
}

func newRangeMap() *RangeMap {
  ranges := make([]*Range, 0)
  return &RangeMap{ranges}
}

func (this *Span) get_chunk_spans(other *Span) []*Span {
  fmt.Printf("Chunking ")
  this.printf()
  fmt.Printf(" with ")
  other.printf()
  fmt.Println()
  result := make([]*Span, 0)

  // this ends before the start of other OR this starts after the end of other
  if this.end < other.start || other.end < this.start {
    fmt.Println("1")
    // this is the only span
    result = append(result, &Span{this.start, this.end})
    return result
  }

  // this starts before other
  if this.start < other.start {
    fmt.Println("2")
    // first span is start of this up to start of other
    result = append(result, &Span{this.start, other.start - 1})

    // this ends before end of other
    if this.end < other.end {
      fmt.Println("3")
      // next span is start of other through end of this
      result = append(result, &Span{other.start, this.end})
      return result
    } else {
      fmt.Println("4")
      // next span is the entirety of other
      result = append(result, &Span{other.start, other.end})
      // this ends after the end of other
      if this.end > other.end {
        fmt.Println("5")
        // last span is end of other to end of this
        result = append(result, &Span{other.end + 1, this.end})
      }
      return result
    }
  }
  // this starts after other

  // this ends before other
  if this.end < other.end {
    fmt.Println("6")
    // this is the only span
    result = append(result, &Span{this.start, this.end})
    return result
  }

  // first span is start of this to end of other
  result = append(result, &Span{this.start, other.end})

  // this ends after other
  if this.end > other.end {
    fmt.Println("7")
    // last span is end of other to end of this
    result = append(result, &Span{other.end + 1, this.end})
  }

  return result
}

//func (r *Range) intersect(rmap *RangeMap) *Span[] {
//  result := make([]*Span, 0)
//  for i, range := range rmap.ranges:
//    fmt.Println(
//}

func (rm *RangeMap) add_range(range_text string) {
  parts := strings.Split(range_text, " ")
  dest_start, _ := strconv.ParseInt(parts[0], 10, 0)
  source_start, _ := strconv.ParseInt(parts[1], 10, 0)
  range_size, _ := strconv.ParseInt(parts[2], 10, 0)
  rm.ranges = append(rm.ranges, &Range{Span{int(source_start), int(range_size)}, int(dest_start)})
}

func (rm *RangeMap) get_dest(source int) int {
  for _, r := range rm.ranges {
    if source >= r.source_span.start && source < r.source_span.end {
      return r.dest_start + (source - r.source_span.start)
    }
  }
  return source
}

func main() {
  //span_values := [1][2][2]int{{{0, 10}, {100, 10}}}
  span_values := [17][2][2]int{
    {{0, 10}, {100, 10}},
    {{100, 10}, {0, 10}},
    {{0, 10}, {10, 20}},
    {{0, 10}, {9, 20}},
    {{0, 10}, {5, 20}},
    {{0, 10}, {5, 5}},
    {{0, 20}, {5, 5}},
    {{5, 20}, {5, 5}},
    {{6, 20}, {5, 5}},
    {{9, 20}, {5, 5}},
    {{10, 20}, {5, 5}},
    {{10, 10}, {10, 10}},
    {{10, 9}, {10, 10}},
    {{10, 5}, {10, 10}},
    {{11, 5}, {10, 10}},
    {{11, 9}, {10, 10}},
    {{19, 1}, {10, 10}},
  }
  for _, spans := range span_values {
    fmt.Printf("!!! this span = %d, other span = %d\n", spans[0], spans[1])
    this := newSpan(spans[0][0], spans[0][1])
    other := newSpan(spans[1][0], spans[1][1])
    chunks := this.get_chunk_spans(other)
    fmt.Println("this =", *this)
    fmt.Println("other =", *other)

    for i, chunk := range chunks {
      fmt.Printf("chunk[%d] = ", i)
      chunk.printf()
      fmt.Println()
    }
    fmt.Println()
  }


//  input_file := flag.String("input_file", "", "Input filename.")
//  flag.Parse()
//
//  f, _ := os.Open(*input_file)
//  r := bufio.NewScanner(f)
//
//  var seeds *string
//  range_maps := make(map[string]*RangeMap)
//  for r.Scan() {
//    var line string = r.Text()
//    if strings.HasPrefix(line, "seeds: ") {
//      parts := strings.SplitAfterN(line, ":", 2)
//      seeds = &parts[1]
//      r.Scan()
//      continue
//    } else if line == "seed-to-soil map:" || line == "soil-to-fertilizer map:" ||
//    line == "fertilizer-to-water map:" || line == "water-to-light map:" ||
//    line == "light-to-temperature map:" || line == "temperature-to-humidity map:" ||
//    line == "humidity-to-location map:" {
//      parts := strings.SplitAfterN(line, " ", 2)
//      range_name := parts[0][0:len(parts[0])-1]
//      //fmt.Printf("range_name = %s\n", range_name)
//      range_map := newRangeMap()
//      for r.Scan() {
//        line = r.Text()
//        if line == "" {
//          break
//        }
//        //fmt.Println("appending line:", line)
//        range_map.add_range(line)
//      }
//      //fmt.Printf("range_map = %q\n", range_map)
//      range_maps[range_name] = range_map
//      //fmt.Printf("range_maps = %q\n", range_maps)
//    }
//  }
//  fmt.Println("seeds:", *seeds)
//  //fmt.Printf("range_maps = %q\n", range_maps)
//  //for k := range range_maps {
//    //fmt.Printf("k = %s, map = %q\n", k, range_maps[k])
//  //}
//
//  seed_parts := strings.Split((*seeds)[1:], " ")
//  //fmt.Println(seed_parts)
//  var min_location int
//  min_location_set := false
//  for i := 0; i < len(seed_parts); i+=2 {
//    raw_int, _ := strconv.ParseInt(seed_parts[i], 10, 0)
//    seed_start := int(raw_int)
//    raw_int, _ = strconv.ParseInt(seed_parts[i + 1], 10, 0)
//    seed_range := int(raw_int)
//    for seed_num := seed_start; seed_num < seed_start + seed_range; seed_num++ {
//      soil_num := range_maps["seed-to-soil"].get_dest(seed_num)
//      fert_num := range_maps["soil-to-fertilizer"].get_dest(soil_num)
//      water_num := range_maps["fertilizer-to-water"].get_dest(fert_num)
//      light_num := range_maps["water-to-light"].get_dest(water_num)
//      temp_num := range_maps["light-to-temperature"].get_dest(light_num)
//      humidity_num := range_maps["temperature-to-humidity"].get_dest(temp_num)
//      loc_num := range_maps["humidity-to-location"].get_dest(humidity_num)
//      //fmt.Printf("seed = %d, soil = %d, fert = %d, water = %d, light = %d, temp = %d, humidity = %d, loc = %d\n", seed_num, soil_num, fert_num, water_num, light_num, temp_num, humidity_num, loc_num)
//      if min_location_set {
//        if loc_num < min_location {
//          min_location = loc_num
//        }
//      } else {
//        min_location = loc_num
//        min_location_set = true
//      }
//    }
//  }
//  fmt.Printf("Closest location = %d\n", min_location)
}
