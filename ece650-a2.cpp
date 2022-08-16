// Compile with c++ ece650-a2.cpp -std=c++11 -o ece650-a2

#include<iostream>
#include<stdio.h>
#include<bits/stdc++.h>
#include<regex>
#include<sstream>

using namespace std;

class Graph
{
    vector<int> G[1000];
public:
    void addEdge(int u, int v);
    void BFS(int vertices, int src, int dst);
    void clearVector();
};

void Graph::clearVector()
{
    for(int i=0; i<1000; i++)
    {
        G[i].clear();
    }
}

void Graph::addEdge(int u, int v)
{
    G[u].push_back(v);
    G[v].push_back(u);
}

void Graph::BFS(int vertices, int src, int dst)
{   
    int visited[1000] = {0};
    int d[1000], p[1000];
    visited[src]=1;
    d[src]=0;
    p[src]=-1;
    queue<int> q;
    q.push(src);
    while(!q.empty())
    {
        int v = q.front();
        q.pop();
        for(int u: G[v])
        {
            if(!visited[u])
            {
                visited[u]=1;
                q.push(u);
                d[u]=d[v]+1;
                p[u]=v;
            }
        }
    }

    vector<int> path;

    if (visited[dst]==0)
    {
        cout<<"Error: No path exists between the two vertices";
    }
    else
    {
        int x = dst;
        while(x!=-1)
        {
            path.push_back(x);
            x=p[x];
        }

        reverse(path.begin(),path.end());

    }
    for(unsigned int i=0;i<path.size();i++)
    {
        if(i==path.size()-1)
            cout<<path[i];
        else
            cout<<path[i]<<"-";
    }
    cout<<endl;
}

int regex_int_cnv(string input,int iterator)
{
    regex e(R"(\d+)");
    sregex_iterator iter(input.begin(), input.end(), e);
    sregex_iterator end;

    stringstream geek((*iter)[iterator]);
    int match_vertex;
    geek >> match_vertex;
    return match_vertex;
}

int main()
{
    string input;

    int vertex = 0;
    Graph obj;

    while(!cin.eof())
    {
        getline (cin,input);
        switch (input[0]) {
            case 'V':
            {
                vertex = regex_int_cnv(input,0);
                if (vertex<=1)
                    {
                        cout<<"Error: Number Of vertices should be greater than 1"<<endl;
                        vertex = 0;
                    }
                else
                    break;
            }
                break;
            case 'E':
            {
                obj.clearVector();
                int vertex1, vertex2;
                regex e(R"(\d+)");
                sregex_iterator iter(input.begin(), input.end(), e);
                sregex_iterator end;
                while(iter != end)
                {                    
                    stringstream geek1((*iter)[0]);                    
                    geek1 >> vertex1;

                    ++iter;

                    stringstream geek2((*iter)[0]);
                    geek2 >> vertex2;

                    if (vertex1 <= vertex && vertex2 <= vertex && vertex1 !=0 && vertex2 !=0)
                        obj.addEdge(vertex1,vertex2);
                    else
                    {
                        cout << "Error: The entered vertex does not exist"<<endl;
                        vertex = 0;
                        break;
                    }   
                    ++iter;
                }
            }

                break;
            case 's':
            {
                regex e(R"(\d+)");
                sregex_iterator iter(input.begin(), input.end(), e);
                sregex_iterator end;

                int vertex1, vertex2;

                stringstream geek1((*iter)[0]);

                ++iter;

                stringstream geek2((*iter)[0]);
                
                geek1 >> vertex1;
                geek2 >> vertex2;

                if (vertex1 <= vertex && vertex2 <= vertex)
                    obj.BFS(vertex,vertex1,vertex2);
                else
                {
                    cout << "Error: The entered vertex does not exist."<<endl;
                    break;
                }
            }
                break;
        }
    }
}