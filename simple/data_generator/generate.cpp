#include <iostream>
#include <fstream>
#include <time.h>
#include <vector>
#include <set>
using namespace std;

int r(int start, int end) {
    return start + (rand() % (end - start));
}

int main(int argc, char *argv[]) {
    srand(time(nullptr));
    int R = atoi(argv[1]);
    int B = atoi(argv[2]);

    set<pair<int, int> > locations;

    while (locations.size() < B)
        locations.insert(make_pair(r(0, R), r(0, R)));

    ofstream ofs("data.csv", ios::out);
    ofs << "id,name,x,y,weight,distance\n";
    int id = 0;
    for (auto &l : locations)
        ofs << ++id << "," << id << "," << l.first << "," << l.second << "," << "-1,-1\n";
    ofs.close();
}
