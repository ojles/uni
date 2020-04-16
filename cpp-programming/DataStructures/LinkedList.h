#ifndef DATASTRUCTURES_LINKEDLIST_H
#define DATASTRUCTURES_LINKEDLIST_H

#include <iostream>

#include "miterator.h"

using namespace std;

template<typename T> class LinkedList
{
private:
	struct Node
	{
		T value;
		Node* next;

		Node()
		{
			next = nullptr;
		}
	};

	Node* root;
	Node* current;

public:
	class LinkedListIterator : public miterator<LinkedList, T>
	{
		Node* node;

	public:
		explicit LinkedListIterator(Node* node) : node(node)
		{
		}

		miterator<LinkedList, T>& operator= (const miterator<LinkedList, T>& iterator) override
		{
			this->node = ((LinkedListIterator&)iterator).node;
			return *this;
		}

		bool operator== (const miterator<LinkedList, T>& iterator) override
		{
			return this->node == ((LinkedListIterator&)iterator).node;
		}

		bool operator!= (const miterator<LinkedList, T>& iterator) override
		{
			return !operator==(iterator);
		}

		T operator* () const override
		{
			return node->value;
		}

		miterator<LinkedList, T>& operator++() override
		{
			if (node->next != nullptr)
			{
				node = node->next;
			}
			return *this;
		}
	};

	LinkedList()
	{
		root = new Node();
		current = root;
	}

	~LinkedList()
	{
		Node* walk = root;
		while (walk->next != nullptr)
		{
			Node* toRemove = walk;
			walk = walk->next;
			delete toRemove;
		}
		delete current;
	}

	void add(T value)
	{
		current->value = value;
		current->next = new Node();
		current = current->next;
	}

	void remove(T searchedValue)
	{
		if (root->value == searchedValue)
		{
			Node* toRemove = root;
			root = root->next;
			delete toRemove;
			return;
		}

		Node* previous = root;
		Node* walk = root->next;

		while (walk->next != nullptr)
		{
			if (walk->value == searchedValue)
			{
				previous->next = walk->next;
				delete walk;
				return;
			}
			walk = walk->next;
			previous = previous->next;
		}
	}


	bool contains(T value)
	{
		Node* walk = root;

		while (walk->next != nullptr)
		{
			if (walk->value == value)
			{
				return true;
			}
			walk = walk->next;
		}
		return false;
	}

	bool equals(LinkedList& anotherList)
	{
		Node* first = this->root;
		Node* second = anotherList.root;

		while (first->next != nullptr && second->next != nullptr)
		{
			if (first->value != second->value)
			{
				return false;
			}
			first = first->next;
			second = second->next;
		}

		return first->next == second->next;
	}

	void prettyPrint(ostream& out)
	{
		if (root->next == nullptr)
		{
			out << "NULL" << endl;
			return;
		}

		out << root->value;

		Node* walk = root->next;
		while (walk->next != nullptr)
		{
			out << " -> " << walk->value;
			walk = walk->next;
		}
		out << endl;
	}

	void forEach(void (*alter)(T&))
	{
		Node* walk = root;
		while (walk->next != nullptr)
		{
			(*alter)(walk->value);
			walk = walk->next;
		}
	}

	miterator<LinkedList, T>& begin()
	{
		return (miterator<LinkedList, T>&)*new LinkedListIterator(root);
	}

	miterator<LinkedList, T>& end()
	{
		return (miterator<LinkedList, T>&)*new LinkedListIterator(current);
	}
};


#endif
