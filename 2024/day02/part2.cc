#include <algorithm>
#include <fstream>
#include <iostream>
#include <iterator>
#include <sstream>
#include <unordered_map>
#include <vector>

using namespace std;

bool is_safe(const std::vector<int>& levels) {
  if (levels.size() < 2) {
    return true;
  }

  int prev_level = levels.at(0);
  int direction = 0;
  bool safe = true;

  for (int i = 1; i < levels.size(); i++) {
    int level = levels.at(i);
    if (direction == 0) {
      if (level > prev_level) {
        direction = 1;
      } else if (level < prev_level) {
        direction = -1;
      } else {
        safe = false;
        break;
      }
    }

    int diff = (level - prev_level) * direction;
    if (!(diff >= 1 && diff <= 3)) {
      safe = false;
      break;
    }
    prev_level = level;
  }

  return safe;
}

int main(int argc, char* argv[]) {
  if (argc < 2) {
    cerr << "Need to specify input filename.";
    return 1;
  }

  ifstream file(argv[1]);
  string report;
  int num_safe = 0;
  while (getline(file, report)) {
    stringstream ss(report);
    string level;
    std::vector<int> levels;
    while (ss >> level) {
      levels.push_back(stoi(level));
    }

    if (is_safe(levels)) {
      num_safe++;
    } else {
      for (int i = 0; i < levels.size(); i++) {
        std::vector<int> dampened_levels(levels.cbegin(), levels.cend());
        auto itr = dampened_levels.begin();
        advance(itr, i);
        dampened_levels.erase(itr);
        if (is_safe(dampened_levels)) {
          num_safe++;
          break;
        }
      }
    }
  }

  cout << "num_safe = " << num_safe << endl;

  return 0;
}
