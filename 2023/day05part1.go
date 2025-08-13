package main

import (
  "bufio"
  "flag"
  "fmt"
  "os"
  "strconv"
  "strings"
)

type Range struct {
  source_start int
  dest_start int
  range_size int
}
type RangeMap struct {
  ranges []*Range
}

func newRangeMap() *RangeMap {
  ranges := make([]*Range, 0)
  return &RangeMap{ranges}
}

func (rm *RangeMap) add_range(range_text string) {
  parts := strings.Split(range_text, " ")
  dest_start, _ := strconv.ParseInt(parts[0], 10, 0)
  source_start, _ := strconv.ParseInt(parts[1], 10, 0)
  range_size, _ := strconv.ParseInt(parts[2], 10, 0)
  rm.ranges = append(rm.ranges, &Range{int(source_start), int(dest_start), int(range_size)})
}

func (rm *RangeMap) get_dest(source int) int {
  for _, r := range rm.ranges {
    if source >= r.source_start && source < r.source_start + r.range_size {
      return r.dest_start + (source - r.source_start)
    }
  }
  return source
}

func main() {
  input_file := flag.String("input_file", "", "Input filename.")
  flag.Parse()

  f, _ := os.Open(*input_file)
  r := bufio.NewScanner(f)

  var seeds *string
  range_maps := make(map[string]*RangeMap)
  for r.Scan() {
    var line string = r.Text()
    if strings.HasPrefix(line, "seeds: ") {
      parts := strings.SplitAfterN(line, ":", 2)
      seeds = &parts[1]
      r.Scan()
      continue
    } else if line == "seed-to-soil map:" || line == "soil-to-fertilizer map:" ||
    line == "fertilizer-to-water map:" || line == "water-to-light map:" ||
    line == "light-to-temperature map:" || line == "temperature-to-humidity map:" ||
    line == "humidity-to-location map:" {
      parts := strings.SplitAfterN(line, " ", 2)
      range_name := parts[0][0:len(parts[0])-1]
      //fmt.Printf("range_name = %s\n", range_name)
      range_map := newRangeMap()
      for r.Scan() {
        line = r.Text()
        if line == "" {
          break
        }
        //fmt.Println("appending line:", line)
        range_map.add_range(line)
      }
      //fmt.Printf("range_map = %q\n", range_map)
      range_maps[range_name] = range_map
      //fmt.Printf("range_maps = %q\n", range_maps)
    }
  }
  fmt.Println("seeds:", *seeds)
  //fmt.Printf("range_maps = %q\n", range_maps)
  //for k := range range_maps {
    //fmt.Printf("k = %s, map = %q\n", k, range_maps[k])
  //}

  seed_parts := strings.Split((*seeds)[1:], " ")
  var min_location int
  for i, seed := range seed_parts {
    fmt.Println("Traversing seed", seed)
    raw_int, _ := strconv.ParseInt(seed, 10, 0)
    seed_num := int(raw_int)
    soil_num := range_maps["seed-to-soil"].get_dest(seed_num)
    fert_num := range_maps["soil-to-fertilizer"].get_dest(soil_num)
    water_num := range_maps["fertilizer-to-water"].get_dest(fert_num)
    light_num := range_maps["water-to-light"].get_dest(water_num)
    temp_num := range_maps["light-to-temperature"].get_dest(light_num)
    humidity_num := range_maps["temperature-to-humidity"].get_dest(temp_num)
    loc_num := range_maps["humidity-to-location"].get_dest(humidity_num)
    fmt.Printf("seed = %d, soil = %d, fert = %d, water = %d, light = %d, temp = %d, humidity = %d, loc = %d\n", seed_num, soil_num, fert_num, water_num, light_num, temp_num, humidity_num, loc_num)
    if i == 0 {
      min_location = loc_num
    } else if loc_num < min_location {
      min_location = loc_num
    }
  }
  fmt.Printf("Closest location = %d\n", min_location)
}
