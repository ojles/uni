#include <iostream>
#include <algorithm>
#include <list>

#include "BinaryTree.h"
#include "LinkedList.h"


using namespace std;

template<class IT1, class IT2>
bool compare(IT1& fbegin, IT1& fend, IT2& sbegin, IT2& send)
{
	while (fbegin != fend && sbegin != send)
	{
		if (*fbegin != *sbegin)
		{
			return false;
		}
		++fbegin;
		++sbegin;
	}
	return fbegin == fend && sbegin == send;
}

int main()
{
	BinaryTree<int>* tree = new BinaryTree<int>();
	tree->add(8);
	tree->add(4);
	tree->add(10);
	tree->add(2);
	tree->add(6);
	tree->add(9);
	tree->add(11);
	tree->add(5);
	tree->add(7);

	LinkedList<int> list;
	list.add(2);
	list.add(3);
	list.add(5);
	list.add(1);

    cout << " [--- Binary Tree ---]" << endl;
    cout << endl;
	tree->prettyPrint(cout);
	cout << endl;


    cout << " [--- Linked List ---]" << endl;
    cout << endl;
    list.prettyPrint(cout);
    cout << endl;

	cout << "Compare tree with list: " << boolalpha << compare(tree->begin(), tree->end(), list.begin(), list.end()) << endl;

    delete tree;
	return 0;
}
