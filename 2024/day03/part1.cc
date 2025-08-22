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
  int total = 0;
  while (getline(file, line)) {
    regex mul_pattern("mul\\((\\d+),(\\d+)\\)");
    auto itr = sregex_iterator(line.begin(), line.end(), mul_pattern);
    auto end = sregex_iterator();
    while (itr != end) {
      total += stoi((*itr)[1]) * stoi((*itr)[2]);
      itr++;
    }
  }

  cout << "result = " << total << endl;

  return 0;
}
