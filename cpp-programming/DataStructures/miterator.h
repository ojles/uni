#ifndef DATASTRUCTURES_ITERATOR_H
#define DATASTRUCTURES_ITERATOR_H

template<class S, typename T>
class miterator
{
public:
	virtual miterator& operator=(const miterator&) = 0;
	virtual bool operator==(const miterator& iterator) = 0;
	virtual bool operator!=(const miterator& iterator) = 0;
	virtual miterator& operator++() = 0;
	virtual T operator*() const = 0;
};


#endif
