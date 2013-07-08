#include <stdio.h>
#include <stdlib.h>
#include <signal.h>

//Accumulate integer and floating point values
double f;
long long i;

void sig_int_handler(int signum)
{
	printf("Integer: %lld\n", i);
	printf("Float: %f\n", f);
	exit(0);
}

int main(int argc, char** argv)
{
	//Register signit handler
	signal(SIGINT, sig_int_handler);

	f = 0.0;
	i = 0;
	
	while(1)
	{
		f += 1.0;
		i +=1;
	}
}
