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

  bool check_word(int char_index, int row_num, int col_num, int row_dir,
                  int col_dir) {
    if (WORD[char_index] == word_search_.at(row_num).at(col_num)) {
      if (char_index + 1 == strlen(WORD)) {
        return true;
      }

      if ((row_num + row_dir >= 0 && row_num + row_dir < word_search_.size()) &&
          (col_num + col_dir >= 0 &&
           col_num + col_dir < word_search_.at(row_num).size())) {
        return check_word(char_index + 1, row_num + row_dir, col_num + col_dir,
                          row_dir, col_dir);
      }
    }
    return false;
  }

  int post_process() {
    int num_occurrences = 0;
    for (int row_num = 0; row_num < word_search_.size(); row_num++) {
      const auto& row = word_search_.at(row_num);
      for (int col_num = 0; col_num < row.size(); col_num++) {
        for (int row_dir = -1; row_dir <= 1; row_dir++) {
          for (int col_dir = -1; col_dir <= 1; col_dir++) {
            if (row_dir == 0 && col_dir == 0) {
              continue;
            }
            if (check_word(0, row_num, col_num, row_dir, col_dir)) {
              num_occurrences++;
            }
          }
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
