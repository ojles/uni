#include "Compiler.h"

string Compiler::compile(string code)
{
	lineIndex = 0;

	removeWhitespaces(code);

	tokenize(code);

	handleBlock(0, tokens.size());

	return parseCommands();
}

void Compiler::removeWhitespaces(string& code)
{
	auto end = remove_if(code.begin(), code.end(), ::isspace);
	code.erase(end, code.end());
}

void Compiler::tokenize(string& code)
{
	auto leftIt = code.begin();
	for (auto rightIt = code.begin(); rightIt != code.end(); ++rightIt)
	{
		if (isLexeme(*rightIt))
		{
			if (leftIt != rightIt)
			{
				tokens.push_back(string(leftIt, rightIt));
			}
			tokens.push_back(string(1, *rightIt));
			leftIt = rightIt;
			++leftIt;
		}
	}
}

void Compiler::handleBlock(int leftIndex, int rightIndex)
{
	for (int i = leftIndex; i < rightIndex; i++)
	{
		string token = tokens[i];
		if (token == "read" || token == "write")
		{
			transform(token.begin(), token.end(), token.begin(), ::toupper);
			addCommand(Command(token, tokens[i + 2]));
			i += 3;
		}
		else if (tokens[i + 1] == "=")
		{
			int endExpression = indexOfFrom(i, ";");
			handleExpression(i + 2, endExpression, tokens[i]);
			i = endExpression;
		}
		else if (token == "if" || token == "while")
		{
			int beginStatementIndex = lineIndex;

			addCommand(Command("GOTOIFNOT", handleStatementExpression(i + 2), "-"));

			i = indexOfFrom(i, "{");
			int endStatementIndex = getClosedBracket(i);
			handleBlock(i, endStatementIndex);
			i = endStatementIndex;

			if (token == "while")
			{
				addCommand(Command("GOTO", to_string(beginStatementIndex)));
			}

			(result.begin() + beginStatementIndex)->second = to_string(lineIndex);
		}
	}
}

string Compiler::parseCommands()
{
	int index = 0;
	for (Command& command : result)
	{
		cout << index << ":\t" << command.op << ' ' << command.first;
		if (!command.second.empty())
		{
			cout << ' ' << command.second;
			if (!command.third.empty())
			{
				cout << ' ' << command.third;
			}
		}
		cout << endl;
		index++;
	}

	stringstream resStream;
	for (Command& command : result)
	{
		resStream << command.op << ' ' << command.first;
		if (!command.second.empty())
		{
			resStream << ' ' << command.second;
			if (!command.third.empty())
			{
				resStream << ' ' << command.third;
			}
		}
		resStream << endl;
	}

	return resStream.str();
}

string Compiler::handleExpression(int leftIndex, int rightIndex, const string& lastVar)
{
	if (rightIndex - leftIndex == 1)
	{
		string resultVariable = lastVar.empty() ? "t" + to_string(tempCount++) : lastVar;
		addCommand(Command("COPY", tokens[leftIndex], resultVariable));
		return lastVar;
	}

	for (int i = leftIndex; i < rightIndex; i++)
	{
		string token = tokens[i];

		if (isNumberOrVariable(token))
		{
			args.push(token);
		}
		else if (isOperator(token))
		{
			while (!operators.empty() && isOperator(operators.top()) && priority[operators.top()] >= priority[token])
			{
				generateCommand();
			}
			operators.push(token);
		}
		else if (token == "(")
		{
			operators.push(token);
		}
		else if (token == ")")
		{
			while (operators.top() != "(")
			{
				generateCommand();
			}
			operators.pop();
		}
	}

	while (!operators.empty())
	{
		if (operators.top() == "(" || operators.top() == ")")
		{
			throw invalid_argument("Invalid argument");
		}
		generateCommand();
	}

	Command& lastCommand = result.back();
	if (!lastVar.empty())
	{
		lastCommand.third = lastVar;
	}

	return lastCommand.third;
}

string Compiler::handleStatementExpression(int i)
{
	int endExp = indexOfFrom(i, "]");
	if (endExp - i != 1)
	{
		return handleExpression(i, endExp);
	}
	else
	{
		return tokens[i];
	}
}

void Compiler::generateCommand()
{
	string op = operators.top(); operators.pop();
	string rhs = args.top();     args.pop();
	string lhs = args.top();     args.pop();

	string resultVariable = "t" + to_string(tempCount++);
	addCommand(Command(numberCommand[op], lhs, rhs, resultVariable));
	args.push(resultVariable);
}

void Compiler::addCommand(Command command)
{
	result.push_back(command);
	lineIndex++;
}

int Compiler::indexOfFrom(int i, string token)
{
	int shift = 0;
	while (tokens[i + shift] != token)
	{
		shift++;
	}
	return i + shift;
}

int Compiler::getClosedBracket(int i)
{
	int shift = 1;
	int bracketsToClose = 1;
	while (true)
	{
		string token = tokens[i + shift];
		if (token == "}")
		{
			bracketsToClose--;
			if (bracketsToClose == 0)
			{
				return i + shift;
			}
		}
		else if (token == "{")
		{
			bracketsToClose++;
		}
		shift++;
	}
}

bool Compiler::isOperator(string& token)
{
	return numberCommand.count(token) == 1;
}

bool Compiler::isNumberOrVariable(const string& value)
{
	return
			regex_match(value, regex(R"(\d+(.\d+)?)"))
			? true
			: regex_match(value, regex(R"((\w|\d)+(#((\w+\d*)|(\d+)))?)"));
}

bool Compiler::isLexeme(char symbol)
{
	return string(">;=+-*/(){}[]").find(symbol) != string::npos;
}
