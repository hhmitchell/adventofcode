#include <algorithm>
#include <fstream>
#include <iostream>
#include <iterator>
#include <regex>
#include <sstream>
#include <unordered_map>
#include <vector>

#include "string.h"

using namespace std;

class Processor {
 public:
  static constexpr char WORD[] = "XMAS";
  Processor() {}

  void process_line(const std::string& line) {
    auto& new_row = word_search_.emplace_back();
    for (const char c : line) {
      new_row.push_back(c);
    }
  }

  bool check_x(int row_num, int col_num) {
    if (word_search_.at(row_num).at(col_num) != 'A') {
      return false;
    }
    if (((word_search_.at(row_num - 1).at(col_num - 1) == 'M' &&
          word_search_.at(row_num + 1).at(col_num + 1) == 'S') ||
         (word_search_.at(row_num - 1).at(col_num - 1) == 'S' &&
          word_search_.at(row_num + 1).at(col_num + 1) == 'M')) &&
        ((word_search_.at(row_num - 1).at(col_num + 1) == 'M' &&
          word_search_.at(row_num + 1).at(col_num - 1) == 'S') ||
         (word_search_.at(row_num - 1).at(col_num + 1) == 'S' &&
          word_search_.at(row_num + 1).at(col_num - 1) == 'M'))) {
      return true;
    }

    return false;
  }

  int post_process() {
    int num_occurrences = 0;
    for (int row_num = 1; row_num < word_search_.size() - 1; row_num++) {
      const auto& row = word_search_.at(row_num);
      for (int col_num = 1; col_num < row.size() - 1; col_num++) {
        if (check_x(row_num, col_num)) {
          num_occurrences++;
        }
      }
    }
    cout << "number = " << num_occurrences << endl;
    return 0;
  }

 private:
  vector<vector<char>> word_search_;
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

  return p.post_process();
}
