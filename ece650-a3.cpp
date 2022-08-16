#include <iostream>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <vector>
#include <sys/wait.h>

using namespace std;

int run_rgen(int argc, char** argv) 
{
	argv[0] = (char *)"rgen";
	execv("rgen", argv); 

	return 0;
}


int run_A1(int argc, char** argv) 
{
	argv[0] = (char *)"/usr/bin/python3";
	argv[1] = (char *)"./ece650-a1.py";
	argv[2] = nullptr;

	execv("/usr/bin/python3", argv);

	return 0;
}

int run_A2(int argc, char** argv) 
{
	argv[0] = (char*)"ece650-a2";
	argv[1] = nullptr;

	execv("ece650-a2", argv);

	return 0;
}


int Process_IP(void) 
{
    while (!std::cin.eof()) 
    {
		std::string line;
		std::getline(std::cin, line);

		if (line.size() > 0) 
        {
			std::cout << line << std::endl;
		}
	}
	return 0;
}


int main (int argc, char** argv) 
{
    std::vector<pid_t> kids;

    std::string val_s;
    int s_default = 10;
    std::string val_n; 
    int n_default = 5; 
    std::string val_l;
    int l_default = 5; 
    std::string val_c;
    int c_default = 20; 
    int c;

    opterr = 0;

    while ((c = getopt (argc, argv, "s:n:l:c:?")) != -1)
        switch (c)
        {
        case 's':
            val_s = optarg;
            s_default = atoi(val_s.c_str());
            if(s_default < 2) {
                std::cerr << "Error: Option -s must have value >= 2" << std::endl;
                return 1;
            }
            break;

        case 'n':
            val_n = optarg;
            n_default = atoi(val_n.c_str());
            if(n_default < 1) {
                std::cerr << "Error: Option -n must have value >= 1" << std::endl;
                return 1;
            }
            break;

        case 'l':
            val_l = optarg;
            l_default = atoi(val_l.c_str());
            if(l_default < 5) {
                std::cerr << "Error: Option -l must have value >= 5" << std::endl;
                return 1;
            }
            break;

        case 'c':
            val_c = optarg;
            c_default = atoi(val_c.c_str());
            if(c_default < 1) {
                std::cerr << "Error: Option -c must have value >= 1" << std::endl;
                return 1;
            }
            break;
        
        case '?':
            std::cerr << "Error: unknown option: " << optopt << std::endl;
            return 1;
        default:
            return 0;
        }

	int pipeRtoA1[2];  
	pipe(pipeRtoA1);

	int pipeA1toA2[2]; 
	pipe(pipeA1toA2);

	pid_t child_pid;

	child_pid = fork();
	if (child_pid == 0)
    {
		dup2(pipeRtoA1[1], STDOUT_FILENO);
		close(pipeRtoA1[0]);
		close(pipeRtoA1[1]); 
		return run_rgen(argc,argv);
    }
    kids.push_back(child_pid);
	
	child_pid = fork();
    if (child_pid == 0) 
    {
		dup2(pipeRtoA1[0], STDIN_FILENO);
		close(pipeRtoA1[0]);
		close(pipeRtoA1[1]);

		dup2(pipeA1toA2[1], STDOUT_FILENO);
		close(pipeA1toA2[0]);
		close(pipeA1toA2[1]);
		return run_A1(argc,argv);
    }
    kids.push_back(child_pid);
	
    child_pid = fork();
    if (child_pid == 0)
    {
		dup2(pipeA1toA2[0], STDIN_FILENO);
		close(pipeA1toA2[1]);
		close(pipeA1toA2[0]);
		return run_A2(argc, argv);
	}
    kids.push_back(child_pid);

	
    child_pid = 0;

	// s i/p to a2

	dup2(pipeA1toA2[1], STDOUT_FILENO);
	close(pipeA1toA2[0]);
	close(pipeA1toA2[1]);
	int op = Process_IP();

    //killing all children

	for (pid_t kill_child : kids) 
    {
        int status;
        kill (kill_child, SIGTERM);
        waitpid(kill_child, &status, 0);
    }
	return op;
}
