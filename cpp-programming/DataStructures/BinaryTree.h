#ifndef DATASTRUCTURES_BINARY_TREE_H
#define DATASTRUCTURES_BINARY_TREE_H

#include <iostream>
#include <string>
#include <list>
#include <queue>

#include "miterator.h"

using namespace std;

enum NodeType
{
	ROOT,
	LEFT,
	RIGHT
};

template<typename T>
class BinaryTree
{
private:
	struct Node
	{
		T value;
		int shift;
		Node* left;
		Node* right;
		Node* parent;

		Node(int value, Node* parent) : value(value), left(nullptr), right(nullptr), parent(parent), shift(0)
		{
		}
	};

	static const char FILLER = ' ';
	static const char UNDERLINE = '_';
	static const char LEFT_BRANCH = '/';
	static const char RIGHT_BRANCH = '\\';

	Node* root;

	void add(Node* node, T value)
	{
		if (value > node->value)
		{
			if (node->right == nullptr)
			{
				node->right = new Node(value, node);
			}
			else
			{
				add(node->right, value);
			}
		}
		else
		{
			if (node->left == nullptr)
			{
				node->left = new Node(value, node);
			}
			else
			{
				add(node->left, value);
			}
		}
	}

	Node* findMin(Node* node)
	{
		while (node->left != nullptr)
		{
			node = node->left;
		}
		return node;
	}

	Node* remove(Node* node, int value)
	{
		if (node == nullptr)
		{
			return node;
		}
		else if (value < node->value)
		{
			node->left = remove(node->left, value);
		}
		else if (value > node->value)
		{
			node->right = remove(node->right, value);
		}
		else
		{
			if (node->left == nullptr && node->right == nullptr)
			{
				delete node;
				node = nullptr;
			}
			else if (node->left == nullptr)
			{
				Node* temp = node;
				node->right->parent = node->parent;
				node = node->right;
				delete temp;
			}
			else if (node->right == nullptr)
			{
				Node* temp = node;
				node->left->parent = node->parent;
				node = node->left;
				delete temp;
			}
			else
			{
				Node* temp = findMin(node->right);
				node->value = temp->value;
				Node* rightNode = remove(node->right, temp->value);
				rightNode->parent = node;
				node->right = rightNode;
			}
		}
		return node;
	}


	void removeSubtree(Node* node)
	{
		if (node != nullptr)
		{
			removeSubtree(node->left);
			removeSubtree(node->right);
			delete node;
		}
	}

#pragma region _PRETTY_PRINT_

	Node* rightNode(Node* node)
	{
		// FIXME: this method is not returning the most 'right' node
		while (node->right != nullptr)
		{
			node = node->right;
		}
		return node;
	}

	Node* leftNode(Node* node)
	{
		// FIXME: this method is not returning the most 'left' node
		while (node->left != nullptr)
		{
			node = node->left;
		}
		return node;
	}

	void calculateNodeShift(Node* node, int direction, int parrentShift)
	{
		if (node == nullptr)
		{
			return;
		}
		node->shift = direction + parrentShift;
		calculateNodeShift(node->left, -1, node->shift);
		calculateNodeShift(node->right, 1, node->shift);
	}

	void addShiftToEachNode(Node* node, int shift)
	{
		if (node == nullptr)
		{
			return;
		}
		node->shift += shift;
		addShiftToEachNode(node->left, shift);
		addShiftToEachNode(node->right, shift);
	}

	void positionLeftNodeToAbsoluteZero()
	{
		addShiftToEachNode(root, -leftNode(root)->shift);
	}

	void fixNodeCollisions(Node* parentNode, Node* node, NodeType nodeType)
	{
		if (node->left == nullptr && node->right == nullptr)
		{
			if (nodeType == NodeType::LEFT)
			{
				node->shift--;
			}
			else if (nodeType == NodeType::RIGHT)
			{
				node->shift++;
			}
			return;
		}
		if (node->left != nullptr)
		{
			fixNodeCollisions(node, node->left, NodeType::LEFT);
		}
		if (node->right != nullptr)
		{
			fixNodeCollisions(node, node->right, NodeType::RIGHT);
		}


		if (nodeType == NodeType::ROOT)
		{
			return;
		}
		else if (nodeType == NodeType::LEFT)
		{
			Node* rightNode = this->rightNode(node);
			if (parentNode->shift <= rightNode->shift)
			{
				addShiftToEachNode(node, -(rightNode->shift - parentNode->shift + 1));
			}
		}
		else
		{
			Node* leftNode = this->leftNode(node);
			if (parentNode->shift >= leftNode->shift)
			{
				addShiftToEachNode(node, parentNode->shift - leftNode->shift + 1);
			}
		}
	}

	list<Node*>* getNodesOnLevel(Node* node, int level, bool isFirstInvocation)
	{
		static list<Node*>* nodes = new list<Node*>();
		static int currentLevel = 0;

		if (isFirstInvocation)
		{
			nodes->clear();
		}

		if (currentLevel == level)
		{
			nodes->push_back(node);
			return nodes;
		}
		else
		{
			if (node->left != nullptr)
			{
				currentLevel++;
				getNodesOnLevel(node->left, level, false);
				currentLevel--;
			}
			if (node->right != nullptr)
			{
				currentLevel++;
				getNodesOnLevel(node->right, level, false);
				currentLevel--;
			}
		}
		return nodes;
	}

#pragma endregion

	class BinaryTreeIterator : public miterator<BinaryTree, T>
	{
		Node* node;

	public:
		explicit BinaryTreeIterator(Node* node) : node(node)
		{
		}

		miterator<BinaryTree, T>& operator=(const miterator<BinaryTree, T>& iterator) override
		{
			node = ((BinaryTreeIterator&)iterator).node;
            return *this;
		}

		bool operator==(const miterator<BinaryTree, T>& iterator) override
		{
			return node == ((BinaryTreeIterator&)iterator).node;
		}

		bool operator!=(const miterator<BinaryTree, T>& iterator) override
		{
			return !operator==(iterator);
		}

		T operator*() const override
		{
			return node->value;
		}

		miterator<BinaryTree, T>& operator++() override
		{
			if (this->node == nullptr)
			{
				return *this;
			}

			Node* parent = this->node->parent;

			if (parent == nullptr)
			{
				this->node = nullptr;
				return *this;
			}

			if ((this->node == parent->left) && (parent->right != nullptr))
			{
				this->node = parent->right;
			}
			else
			{
				this->node = this->node->parent;
				return *this;
			}
			while (true)
			{
				if (this->node->left != nullptr)
				{
					this->node = this->node->left;
				}
				else if (this->node->right != nullptr)
				{
					this->node = this->node->right;
				}
				else
				{
					return *this;
				}
			}
		}
	};

public:
	BinaryTree()
	{
	}

	~BinaryTree()
	{
		removeSubtree(root);
	}

	void add(T value)
	{
		if (root == nullptr)
		{
			root = new Node(value, nullptr);
		}
		else
		{
			add(root, value);
		}
	}

	void remove(int value)
	{
		remove(root, value);
	}

	void prettyPrint(ostream& out)
	{
		calculateNodeShift(root, 0, 0);
		fixNodeCollisions(nullptr, root, NodeType::ROOT);
		positionLeftNodeToAbsoluteZero();

		for (int i = 0; true; i++)
		{
			list<struct Node*>* nodesOnLevel = getNodesOnLevel(root, i, true);

			if (nodesOnLevel->size() == 0)
			{
				return;
			}

			int horizontalIndex = 0;
			for (Node* node : *nodesOnLevel)
			{
				if (node->left != nullptr)
				{
					while (horizontalIndex <= node->left->shift)
					{
						out << FILLER;
						horizontalIndex++;
					}

					while (horizontalIndex < node->shift)
					{
						out << UNDERLINE;
						horizontalIndex++;
					}
				}
				else
				{
					while (horizontalIndex < node->shift)
					{
						out << FILLER;
						horizontalIndex++;
					}
				}

				out << node->value;
				horizontalIndex += std::to_string(node->value).length();

				if (node->right != nullptr)
				{
					while (horizontalIndex < node->right->shift)
					{
						out << UNDERLINE;
						horizontalIndex++;
					}
				}
			}
			out << endl;

			int _horizontalIndex = 0;
			for (Node* node : *nodesOnLevel)
			{
				if (node->left != nullptr)
				{
					while (_horizontalIndex < node->left->shift)
					{
						out << FILLER;
						_horizontalIndex++;
					}
					out << LEFT_BRANCH;
					_horizontalIndex++;
				}
				else
				{
					while (_horizontalIndex < node->shift)
					{
						out << FILLER;
						_horizontalIndex++;
					}
				}
				if (node->right != nullptr)
				{
					while (_horizontalIndex < node->right->shift)
					{
						out << FILLER;
						_horizontalIndex++;
					}
					out << RIGHT_BRANCH;
					_horizontalIndex++;
				}
			}
			out << endl;
		}
	}

	miterator<BinaryTree, T>& begin()
	{
		return (miterator<BinaryTree, T> &)*new BinaryTreeIterator(findMin(root));
	}

	miterator<BinaryTree, T>& end()
	{
		return (miterator<BinaryTree, T> &)*new BinaryTreeIterator(nullptr);
	}
};


#endif
