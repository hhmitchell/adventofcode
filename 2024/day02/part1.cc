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
  string report;
  int num_safe = 0;
  while (getline(file, report)) {
    stringstream ss(report);
    string level;
    if (!(ss >> level)) {
      cerr << "Report contains no value!";
      return 1;
    }
    int prev_value = stoi(level);
    int direction = 0;
    bool safe = true;
    cout << "Report: " << report;
    while (ss >> level) {
      int value = stoi(level);
      if (direction == 0) {
        if (value > prev_value) {
          direction = 1;
        } else if (value < prev_value) {
          direction = -1;
        } else {
          safe = false;
          cout << " level (" << level << ")";
          break;
        }
      }

      int diff = (value - prev_value) * direction;
      if (!(diff >= 1 && diff <= 3)) {
        cout << " level (" << level << ")";
        safe = false;
        break;
      }
      prev_value = value;
    }
    if (safe) {
      num_safe++;
      cout << endl;
    } else {
      cout << " NOT SAFE" << endl;
    }
  }

  cout << "num_safe = " << num_safe << endl;

  return 0;
}
