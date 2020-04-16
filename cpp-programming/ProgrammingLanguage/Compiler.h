#ifndef PROGRAMMINGLANGUAGE_COMPILER_H
#define PROGRAMMINGLANGUAGE_COMPILER_H

#include <string>
#include <iostream>
#include <algorithm>
#include <sstream>
#include <stack>
#include <regex>
#include <utility>
#include <vector>
#include <map>
#include <list>

using namespace std;

class Compiler
{
private:
	struct Command
	{
		string op;
		string first;
		string second;
		string third;

		Command(string op, string first, string second = "", string third = "")
				: op(move(op)), first(move(first)), second(move(second)), third(move(third))
		{
		}
	};

	int lineIndex = 0;
	int tempCount = 0;

	vector<Command> result;
	vector<string> tokens;

	stack<string> args;
	stack<string> operators;

	map<string, string> numberCommand
	{
			{"+", "ADD"},
			{"-", "SUB"},
			{"*", "MUL"},
			{"/", "DIV"},
	};

	map<string, int> priority
	{
			{"+", 1},
			{"-", 1},
			{"*", 2},
			{"/", 2},
	};


	void removeWhitespaces(string& code);

	void tokenize(string& code);

	void handleBlock(int leftIndex, int rightIndex);

	string parseCommands();

	string handleExpression(int leftIndex, int rightIndex, const string& lastVar = "");

	string handleStatementExpression(int i);

	void generateCommand();

	void addCommand(Command command);

	int indexOfFrom(int i, string token);

	int getClosedBracket(int i);

	bool isOperator(string& token);

	bool isNumberOrVariable(const string& variable);

	bool isLexeme(char symbol);

public:
	string compile(string code);
};


#endif
