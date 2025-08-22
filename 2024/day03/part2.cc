#include <algorithm>
#include <fstream>
#include <iostream>
#include <iterator>
#include <regex>
#include <sstream>
#include <unordered_map>
#include <vector>

using namespace std;

int main(int argc, char* argv[]) {
  if (argc < 2) {
    cerr << "Need to specify input filename.";
    return 1;
  }

  ifstream file(argv[1]);
  string line;
  bool enabled = true;
  int total = 0;
  while (getline(file, line)) {
    regex mul_pattern("mul\\((\\d+),(\\d+)\\)");
    regex do_pattern("do(n't)?\\(\\)");
    auto mul_itr = sregex_iterator(line.begin(), line.end(), mul_pattern);
    auto do_itr = sregex_iterator(line.begin(), line.end(), do_pattern);
    auto end = sregex_iterator();

    while (mul_itr != end) {
      if (do_itr == end || mul_itr->position(0) < do_itr->position(0)) {
        if (enabled) {
          total += stoi((*mul_itr)[1]) * stoi((*mul_itr)[2]);
        }
        mul_itr++;
      } else {
        enabled = (*do_itr)[1].str().empty();
        do_itr++;
      }
    }
  }

  cout << "result = " << total << endl;

  return 0;
}
