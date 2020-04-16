#include <iostream>
#include <fstream>

#include "Compiler.h"
#include "VirtualMachine.h"

using namespace std;

string readFile(const string& fileName)
{
	string data;
	ifstream in(fileName.c_str());
	getline(in, data, string::traits_type::to_char_type(string::traits_type::eof()));
	return data;
}

int main()
{
	string code = readFile("code.myl");

	Compiler compiler;
	string compiledCode = compiler.compile(code);

	VirtualMachine vm;
	vm.run(compiledCode);

	return 0;
}
