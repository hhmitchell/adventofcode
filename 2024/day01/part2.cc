#include <algorithm>
#include <fstream>
#include <iostream>
#include <iterator>
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
  string str;
  vector<int> left;
  unordered_map<int, int> right;

  while (getline(file, str)) {
    stringstream ss(str);
    istream_iterator<string> begin(ss);
    istream_iterator<string> end;
    vector<string> vstrings(begin, end);
    if (vstrings.size() != 2) {
      cerr << "Line should have exactly 2 integers." << endl;
      return 1;
    }

    left.push_back(stoi(vstrings.at(0)));
    int rval = stoi(vstrings.at(1));
    if (right.contains(rval)) {
      right[rval] += 1;
    } else {
      right[rval] = 1;
    }
  }

  int similarity = 0;
  for (const auto& val : left) {
    similarity += right.contains(val) ? right.at(val) * val : 0;
  }
  cout << "similarity = " << similarity << endl;

  return 0;
}
