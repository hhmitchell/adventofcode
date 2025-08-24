#include <algorithm>
#include <fstream>
#include <iostream>
#include <iterator>
#include <map>
#include <memory>
#include <optional>
#include <regex>
#include <set>
#include <sstream>
#include <tuple>
#include <unordered_set>
#include <vector>

#include "string.h"

using namespace std;

class Guard {
 public:
  Guard(int x, int y) : x_(x), y_(y) {}
  ~Guard() = default;

  class Direction {
   public:
    Direction(int dir_x, int dir_y) : dir_x_(dir_x), dir_y_(dir_y) {}
    ~Direction() = default;

    int dir_x() const { return dir_x_; }
    int dir_y() const { return dir_y_; }
    struct Comparator {
      bool operator()(const Direction& a, const Direction& b) const {
        if (a.dir_x() == b.dir_x()) {
          return a.dir_y() < b.dir_y();
        }
        return a.dir_x() < b.dir_x();
      }
    };

   private:
    int dir_x_, dir_y_;
  };

  int x() const { return x_; }
  int y() const { return y_; }

  struct Comparator {
    bool operator()(const Guard& a, const Guard& b) const {
      if (a.x() == b.x()) {
        return a.y() < b.y();
      }
      return a.x() < b.x();
    }
  };

 private:
  int x_, y_;
};

class Processor {
 public:
  Processor() {}
  ~Processor() = default;

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

  bool walk(map<Guard, set<Guard::Direction, Guard::Direction::Comparator>,
                Guard::Comparator>& visited,
            const Guard& obstacle) {
    int current_guard_x = guard_x_;
    int current_guard_y = guard_y_;
    int current_x_dir = x_dir_;
    int current_y_dir = y_dir_;
    while ((current_guard_x >= 0 && current_guard_x < map_.at(0).size()) &&
           (current_guard_y >= 0 && current_guard_y < map_.size())) {
      Guard guard = Guard(current_guard_x, current_guard_y);
      Guard::Direction dir = Guard::Direction(current_x_dir, current_y_dir);
      if (visited.contains(guard) && visited.at(guard).contains(dir)) {
        return false;
      }
      visited[guard].insert(dir);
      int next_x = current_guard_x + current_x_dir;
      int next_y = current_guard_y + current_y_dir;

      if ((next_x >= 0 && next_x < map_.at(0).size()) &&
          (next_y >= 0 && next_y < map_.size())) {
        if (map_.at(next_y).at(next_x) == '#' ||
            (next_x == obstacle.x() && next_y == obstacle.y())) {
          if (current_x_dir == 0 && current_y_dir == -1) {
            current_x_dir = 1;
            current_y_dir = 0;
          } else if (current_x_dir == 1 && current_y_dir == 0) {
            current_x_dir = 0;
            current_y_dir = 1;
          } else if (current_x_dir == 0 && current_y_dir == 1) {
            current_x_dir = -1;
            current_y_dir = 0;
          } else {
            current_x_dir = 0;
            current_y_dir = -1;
          }
        } else {
          current_guard_x = next_x;
          current_guard_y = next_y;
        }
      } else {
        current_guard_x = next_x;
        current_guard_y = next_y;
      }
    }

    return true;
  }

  bool check_loop(const Guard& candidate) {
    if (map_.at(candidate.y()).at(candidate.x()) != '.') {
      return false;
    }
    map<Guard, set<Guard::Direction, Guard::Direction::Comparator>,
        Guard::Comparator>
        visited;
    return !walk(visited, candidate);
  }

  void dump() {
    for (int i = 0; i < map_.size(); i++) {
      for (int j = 0; j < map_.at(i).size(); j++) {
        cout << map_.at(i).at(j);
      }
      cout << endl;
    }
  }

  void post_process() {
    if (!walk(visited_, Guard(-3, -3))) {
      cout << "BAD" << endl;
    }

    int num_possible = 0;
    for (const auto& [candidate, unused] : visited_) {
      if (check_loop(candidate)) {
        num_possible++;
      }
    }
    cout << "possible obstructions = " << num_possible << endl;
  }

 private:
  int guard_x_;
  int guard_y_;
  int x_dir_;
  int y_dir_;
  vector<string> map_;
  map<Guard, set<Guard::Direction, Guard::Direction::Comparator>,
      Guard::Comparator>
      visited_;
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
