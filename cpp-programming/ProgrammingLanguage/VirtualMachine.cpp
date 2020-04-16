#include "VirtualMachine.h"

bool isNumber(string&);

void VirtualMachine::run(string code)
{
	parseCommands(code);
	executeSteps();
}

void VirtualMachine::parseCommands(string& code)
{
	stringstream codeStream(code);

	string command;
	vector<string> parameters;

	while (codeStream >> command)
	{
		string param, paramLine;
		getline(codeStream, paramLine, '\n');

		stringstream paramStream(paramLine);
		while (paramStream >> param)
		{
			parameters.push_back(param);
		}

		pair<string, vector<string>> step(command, parameters);
		steps.push_back(step);

		parameters.clear();
	}
}

void VirtualMachine::executeSteps()
{
	while (stepIndex != steps.size())
	{
		functions[steps[stepIndex].first](steps[stepIndex].second);
		stepIndex++;
	}
}

double VirtualMachine::getVariable(string variable)
{
	if (isNumber(variable))
	{
		return stod(variable);
	}
	else
	{
		variable = setIndexIfArray(variable);
		auto variableIterator = variables.find(variable);
		if (variableIterator == variables.end())
		{
			throw invalid_argument("Invalid variable!");
		}
		else
		{
			return variableIterator->second;
		}
	}
}

void VirtualMachine::setVariable(string variable, double value)
{
	variable = setIndexIfArray(variable);
	variables[variable] = value;
}

string VirtualMachine::setIndexIfArray(string variable)
{
	auto arrayIndex = variable.find('#');
	if (arrayIndex != string::npos)
	{
		int index = static_cast<int>(getVariable(variable.substr(arrayIndex + 1)));
		return variable.substr(0, arrayIndex) + '#' + to_string(index);
	}
	return variable;
}

bool isNumber(string& value)
{
	for (char symbol : value)
	{
		if ((symbol < '0' || symbol > '9') && symbol != '.')
		{
			return false;
		}
	}
	return true;
}
