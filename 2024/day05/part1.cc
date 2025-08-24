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
  Processor() : read_ordering_(true), sum_(0) {}

  void process_line(const std::string& line) {
    if (read_ordering_) {
      if (line.empty()) {
        read_ordering_ = false;

        return;
      }
      regex ordering_pattern("^(\\d+)\\|(\\d+)$");
      smatch match;
      if (regex_match(line, match, ordering_pattern)) {
        ordering_rules_[stoi(match[1])].insert(stoi(match[2]));
      } else {
        cout << "OOPS: " << line << endl;
      }
      return;
    }

    set<int> seen;
    vector<int> update;
    size_t start_pos = 0;
    bool valid_rule = true;
    while (start_pos < line.size()) {
      size_t found_len = line.substr(start_pos).find(',');
      int page = stoi(line.substr(start_pos, found_len));
      const auto itr = ordering_rules_.find(page);
      vector<int> intersection;
      if (itr != ordering_rules_.end()) {
        set_intersection(seen.begin(), seen.end(), itr->second.begin(),
                         itr->second.end(), back_inserter(intersection));
        if (!intersection.empty()) {
          valid_rule = false;
          break;
        }
      }
      seen.insert(page);
      update.push_back(page);

      if (found_len == string::npos) {
        start_pos = line.size();
      } else {
        start_pos = start_pos + found_len + 1;
      }
    }
    if (valid_rule) {
      sum_ += update.at(update.size() / 2);
    }
  }

  void post_process() { cout << "sum = " << sum_ << endl; }

 private:
  bool read_ordering_;
  std::map<int, set<int>> ordering_rules_;
  int sum_;
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
