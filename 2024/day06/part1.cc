#include <algorithm>
#include <fstream>
#include <iostream>
#include <iterator>
#include <map>
#include <regex>
#include <set>
#include <sstream>
#include <vector>

#include "string.h"

using namespace std;

class Processor {
 public:
  Processor() {}

  void process_line(const std::string& line) {
    map_.push_back(line);
    size_t pos = string::npos;
    if ((pos = line.find("^")) != string::npos) {
      guard_x_ = pos;
      guard_y_ = map_.size() - 1;
      x_dir_ = 0;
      y_dir_ = -1;
    } else if ((pos = line.find(">")) != string::npos) {
      guard_x_ = pos;
      guard_y_ = map_.size() - 1;
      x_dir_ = 1;
      y_dir_ = 0;
    } else if ((pos = line.find("v")) != string::npos) {
      guard_x_ = pos;
      guard_y_ = map_.size() - 1;
      x_dir_ = 0;
      y_dir_ = 1;
    } else if ((pos = line.find("<")) != string::npos) {
      guard_x_ = pos;
      guard_y_ = map_.size() - 1;
      x_dir_ = -1;
      y_dir_ = 0;
    }
  }

  void post_process() {
    while ((guard_x_ >= 0 && guard_x_ < map_.at(0).size()) &&
           (guard_y_ >= 0 && guard_y_ < map_.size())) {
      map_[guard_y_][guard_x_] = 'X';
      int next_x = guard_x_ + x_dir_;
      int next_y = guard_y_ + y_dir_;

      if ((next_x >= 0 && next_x < map_.at(0).size()) &&
          (next_y >= 0 && next_y < map_.size()) &&
          map_.at(next_y).at(next_x) == '#') {
        if (x_dir_ == 0 && y_dir_ == -1) {
          x_dir_ = 1;
          y_dir_ = 0;
        } else if (x_dir_ == 1 && y_dir_ == 0) {
          x_dir_ = 0;
          y_dir_ = 1;
        } else if (x_dir_ == 0 && y_dir_ == 1) {
          x_dir_ = -1;
          y_dir_ = 0;
        } else {
          x_dir_ = 0;
          y_dir_ = -1;
        }
      } else {
        guard_x_ = next_x;
        guard_y_ = next_y;
      }
    }

    int num_visited = 0;
    for (const auto& row : map_) {
      for (const auto& pos : row) {
        if (pos == 'X') {
          num_visited++;
        }
      }
    }
    cout << "num visisted = " << num_visited << endl;
  }

 private:
  int guard_x_;
  int guard_y_;
  int x_dir_;
  int y_dir_;
  vector<string> map_;
};

int main(int argc, char* argv[]) {
  if (argc < 2) {
    cerr << "Need to specify input filename.";
    return 1;
  }

  ifstream file(argv[1]);
  string line;
  Processor p;

  while (getline(file, line)) {
    p.process_line(line);
  }
  p.post_process();

  return 0;
}
