#include<bits/stdc++.h>
using namespace std;

int main() {

    // graphj by adjency list
    unordered_map<string, vector<string> > graph;

    // given edges
    vector<pair<string, string> > edge;

    edge.push_back({"george", "jean"});
    edge.push_back({"frank", "fred"});
    edge.push_back({"george", "john"});
    edge.push_back({"jim", "fred"});
    edge.push_back({"jim", "frank"});
    edge.push_back({"gim", "susan"});
    edge.push_back({"susan", "frank"});

    // graph code
    for(int i = 0; i < edge.size(); i++) {
        string u = edge[i].first;
        string v = edge[i].second;

        graph[u].push_back(v);
        graph[v].push_back(u);
    }

    // friend ofjohn
    cout << "friends of john: ";
    for(int i = 0; i < graph["john"].size(); i++) {
        cout << graph["john"][i] << " ";
    }
    cout << endl;

    // friends of susan
    cout << "friends of susan: ";
    for(int i = 0; i < graph["susan"].size(); i++) {
        cout << graph["susan"][i] << " ";
    }
    cout << endl;

    // (c) friend of friend of jean
    set<string> s1;

    for(int i = 0; i < graph["jean"].size(); i++) {
        string f = graph["jean"][i];

        for(int j = 0; j < graph[f].size(); j++) {
            string ff = graph[f][j];

            if(ff != "jean") {
                s1.insert(ff);
            }
        }
    }

    cout << "friends of friends of Jean: ";
    for(auto x : s1) {
        cout << x << " ";
    }
    cout << endl;

    // friends of friends of Jim
    set<string> s2;

    for(int i = 0; i < graph["jim"].size(); i++) {
        string f = graph["jim"][i];

        for(int j = 0; j < graph[f].size(); j++) {
            string ff = graph[f][j];

            if(ff != "jim") {
                s2.insert(ff);
            }
        }
    }

    cout << "friends of friends of Jim: ";
    for(auto x : s2) {
        cout << x << " ";
    }
    cout << endl;

    return 0;
}