#include <iostream>
#include <string>

using namespace std;

struct aaa
{
	int a;
	int b;
};


int main()
{
	aaa as[10][10];
	as[9][9].a = 1;
	as[9][0].b = 2;
	return 0;
}
