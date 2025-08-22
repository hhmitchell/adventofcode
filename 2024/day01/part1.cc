#include <algorithm>
#include <fstream>
#include <iostream>
#include <iterator>
#include <sstream>
#include <vector>

using namespace std;

int main(int argc, char* argv[]) {
  if (argc < 2) {
    cerr << "Need to specify input filename.";
    return 1;
  }

  ifstream file(argv[1]);
  string str;
  vector<int> left, right;
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
    right.push_back(stoi(vstrings.at(1)));
  }

  sort(left.begin(), left.end());
  sort(right.begin(), right.end());
  int distance = 0;
  for (int i = 0; i < left.size(); i++) {
    distance += abs(left.at(i) - right.at(i));
  }
  cout << "distance = " << distance << endl;

  return 0;
}
