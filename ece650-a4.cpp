#include<iostream>
#include<stdio.h>
//#include<bits/stdc++.h>
#include<regex>
#include<sstream>
#include "minisat/core/Solver.h"
#include "minisat/core/SolverTypes.h"

using namespace std;

int main()
{
    int Total_Vertices=0;
    vector<int>List1;

    while(!cin.eof())
    {
        string line;
        getline(cin,line);
        istringstream input(line);

        while (!input.eof())
        {
            char commandline_arg;
            input>>commandline_arg;

            if (commandline_arg=='V')
            {
                regex For_V("\\d+");
                smatch c;
                regex_search(line, c,For_V);
                for (auto temp : c)
                {
                    Total_Vertices=stoi(temp);
                    if (Total_Vertices<=0)
                    {
                        Total_Vertices=0;
                        cerr<<"Error: Number of Vertices should be more than 1"<<endl;
                    }
                    break;
                }
            }
            if (commandline_arg=='E')
            {
                int x;
                int y;
                int flag1=0;

                List1.clear();

                regex For_Coord(R"(\d+)");
                smatch match;
                if(regex_search(line,match,For_Coord)==false)
                {
                    cout << endl;
                    break;
                }
                sregex_iterator iter(line.begin(), line.end(), For_Coord);
                sregex_iterator end;
                while(iter !=end)
                {
                    stringstream a((*iter)[0]);
                    a >> x;
                    ++iter;
                    stringstream b((*iter)[0]);
                    b>>y;

                    if ((x<=0 || y<=0 || x>Total_Vertices || y>Total_Vertices)&&flag1==0)
                    {
                        flag1=1;
                        Total_Vertices=0;
                    }

                    else
                    {
                        List1.push_back(x);
                        List1.push_back(y);
                    }
                    ++iter;

                }

                if (flag1==1)
                {
                    cerr<<"Error: Vertex does not exist in E";
                }

                unique_ptr<Minisat::Solver> solver(new Minisat::Solver());
                vector<int> VertexCoverResult;                     
                int VertexCoverSize = 1;                             
                Minisat::vec<Minisat::Lit> list;             
                Minisat::vec<Minisat::Lit> temp;                      
                bool SAT_UNSAT;                      

                while(VertexCoverSize<=Total_Vertices)
                {
                    Minisat::Lit Matrix[Total_Vertices][VertexCoverSize];        
                    for(int i=1; i<=Total_Vertices; i++)
                    {
                        for(int j=1; j<=VertexCoverSize; j++)
                        {
                            Matrix[i][j] = Minisat::mkLit(solver->newVar());  
                        }
                    }

                    // CLAUSE 1: At least one vertex is the ith vertex in the vertex cover

                    for(int i=1; i<=VertexCoverSize; i++)
                    {
                        list.clear();
                        for(int j=1; j<=Total_Vertices; j++)
                        {
                            list.push(Matrix[j][i]);
                        }
                        solver->addClause(list);

                        // CLAUSE 2: No one vertex can appear twice in a vertex cover

                        for(int p=0; p<Total_Vertices; p++)
                        {
                            for(int q=p+1; q<Total_Vertices; q++)
                            {
                                solver->addClause(~list[p], ~list[q]);
                            }
                        }
                    }

                    //CLAUSE 3: No more than one vertex appears in the mth position of the vertex cover.

                    for(int i=1; i<=Total_Vertices; i++)
                    {
                        for(int j=1; j<=VertexCoverSize; j++)
                        {
                            for(int m=j+1; m<=VertexCoverSize; m++)
                            {
                                solver->addClause(~Matrix[i][j], ~Matrix[i][m]);
                            }
                        }
                    }

                    // CLAUSE 4: Every edge is incident to at least one vertex in the vertex cover.

                    for(unsigned int i=0; i<List1.size()-1; i=i+2)
                    {
                        temp.clear();
                        for(int j=1; j<=VertexCoverSize; j++)
                        {
                            temp.push(Matrix[List1[i]][j]);
                            temp.push(Matrix[List1[i+1]][j]);
                        }
                        solver->addClause(temp);
                    }

                    SAT_UNSAT = solver->solve();  

                    if(SAT_UNSAT==1)         
                    {
                        for(int i=1; i<=Total_Vertices; i++)
                        {
                            for(int j=1; j<=VertexCoverSize; j++)
                            {
                                if(Minisat::toInt(solver->modelValue(Matrix[i][j])) == 0) 
                                {
                                    VertexCoverResult.push_back(i);
                                }
                            }
                        }
                        break;
                    }

                    else if (SAT_UNSAT==0)
                    {
                        VertexCoverSize++;                     
                        solver.reset (new Minisat::Solver());
                    }
                }

                for (unsigned int i = 0; i< VertexCoverResult.size(); i++)
                {
                    cout<<VertexCoverResult[i]<<" ";
                }
                cout<<endl;
            }
        }
    }
}


