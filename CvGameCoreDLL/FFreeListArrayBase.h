#pragma once

//	$Revision: #2 $		$Author: mbreitkreutz $ 	$DateTime: 2005/06/13 13:35:55 $
//------------------------------------------------------------------------------------------------
//
//  *****************   FIRAXIS GAME ENGINE   ********************
//
//  FILE:    FFreeListArrayBase.h
//
//  AUTHOR:  Mustafa Thamer
//
//  PURPOSE: abstract base class for FFreeListArray and FFreeListTrashArray
//
//------------------------------------------------------------------------------------------------
//  Copyright (c) 2004 Firaxis Games, Inc. All rights reserved.
//------------------------------------------------------------------------------------------------

#ifndef		FFREELISTARRAYBASE_H
#define		FFREELISTARRAYBASE_H
#pragma		once

namespace FFreeList
{
	enum
	{
		INVALID_INDEX	= -1,
		FREE_LIST_INDEX	= -2
	};
};

template <class T>
class FFreeListArrayBase
{
public:

	FFreeListArrayBase();
	virtual ~FFreeListArrayBase() {}
	virtual void init(int iNumSlots = 8) = 0;
	virtual void uninit() = 0;
	virtual T* getAt(int iIndex) const = 0;
	T* operator[]( int iIndex ) const;

	// start at the beginning of the list and return the first item or NULL when done
	T* beginIter(int* pIterIdx) const;

	// iterate from the current position and return the next item found or NULL when done
	T* nextIter(int* pIterIdx) const;

	// start at the end of the list and return the last item or NULL when done
	T* endIter(int* pIterIdx) const;

	// iterate from the current position and return the prev item found or NULL when done
	T* prevIter(int* pIterIdx) const;

	// Returns the iIndex after the last iIndex in the array containing an element
	int getIndexAfterLast() const	{	return m_iLastIndex + 1;	}

	// Returns the number of elements in the array (NOTE: this is a non-packed array, so this value is NOT the last iIndex in the array...)
	int getCount()	const {	return m_iLastIndex - m_iFreeListCount + 1;	}

	virtual void removeAll() = 0;
protected:
	int m_iFreeListHead;
	int m_iFreeListCount;
	int m_iLastIndex;
	int m_iNumSlots;

	virtual void growArray() = 0;
};

template <class T>
FFreeListArrayBase<T>::FFreeListArrayBase()
{
	m_iFreeListHead = FFreeList::FREE_LIST_INDEX;
	m_iFreeListCount = 0;
	m_iLastIndex = FFreeList::INVALID_INDEX;
	m_iNumSlots = 0;
}


//
// operators
//

template < class T >
inline T* FFreeListArrayBase< T >::operator[]( int iIndex ) const
{
	return ( getAt( iIndex ) );
}

//
// iteration functions
//

// start at the beginning of the list and return the first item or NULL when done
template <class T>
T* FFreeListArrayBase<T>::beginIter(int* pIterIdx) const
{
	*pIterIdx = 0;
	return nextIter(pIterIdx);
}

// iterate from the current position and return the next item found or NULL when done
template <class T>
T* FFreeListArrayBase<T>::nextIter(int* pIterIdx) const
{
	for( ; (*pIterIdx)<getIndexAfterLast(); (*pIterIdx)++)
	{
		T* pObj = getAt((*pIterIdx));
		if (pObj)
		{
			(*pIterIdx)++;	// prime for next call
			return pObj;
		}
	}
	return NULL;
}

// start at the end of the list and return the last item or NULL when done
template <class T>
T* FFreeListArrayBase<T>::endIter(int* pIterIdx) const
{
	*pIterIdx = getIndexAfterLast()-1;
	return prevIter(pIterIdx);
}

// iterate from the current position and return the prev item found or NULL when done
template <class T>
T* FFreeListArrayBase<T>::prevIter(int* pIterIdx) const
{
	for( ; (*pIterIdx)>=0; (*pIterIdx)--)
	{
		T* pObj = getAt((*pIterIdx));
		if (pObj)
		{
			(*pIterIdx)--;	// prime for next call
			return pObj;
		}
	}
	return NULL;
}

#endif	//FFREELISTARRAYBASE_H
