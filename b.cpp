

#include<iostream>
#include <unordered_map>
#include <vector>
#include <string>

using namespace std;

unordered_map<string, vector<string> > graph;
unordered_map<string, bool> visited;
vector<string> path;

bool dfs(string node, string goal) {

    visited[node] = true;
    path.push_back(node);

    if(node == goal) {
        return true;
    }

    for(int i = 0; i < graph[node].size(); i++) {
        string next = graph[node][i];

        if(!visited[next]) {
            if(dfs(next, goal)) {
                return true;
            }
        }
    }

    path.pop_back();
    return false;
}

int main() {

    graph["start"].push_back("A");
    graph["start"].push_back("B");
    graph["A"].push_back("start");
    graph["A"].push_back("C");
    graph["B"].push_back("start");
    graph["B"].push_back("D");
    graph["C"].push_back("A");
    graph["C"].push_back("goal");
    graph["D"].push_back("B");
    graph["goal"].push_back("C");

    string start = "start";
    string goal = "goal";

    for(auto it : graph) {
        visited[it.first] = false;
    }

    if(dfs(start, goal)) {
        cout << "Path from start to goal:\n";
        for(int i = 0; i < path.size(); i++) {
            cout << path[i] << " ";
        }
    } else {
        cout << "No path found";
    }

    return 0;
}
