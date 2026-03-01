//	$Revision: #2 $		$Author: mbreitkreutz $ 	$DateTime: 2005/06/13 13:35:55 $
//-------------------------------------------------------------------------------------
//  *****************   FIRAXIS GAME ENGINE   ********************
//  FILE:    FFreeListTrashArray.h
//  AUTHOR:  Soren Johnson
//  PURPOSE: A dynamic array with a free list that keeps track of its own memory...
//-------------------------------------------------------------------------------------
//  Copyright (c) 2004 Firaxis Games, Inc. All rights reserved.
/*	advc: Merged with the base class FreeListArrayBase and removed the unused sibling
	FreeListArray from the code base. And other changes; see comments below. */
/*	advc.003u: Part of the implementation moved to FFreeListTrashArray.cpp.
	Caveat: All instantiations have to be made explicit at the end of that cpp file. */

#ifndef FFREELISTTRASHARRAY_H
#define FFREELISTTRASHARRAY_H
#pragma once

#include "FreeListTraversal.h" // advc.003s

namespace FFreeList
{
	enum
	{
		INVALID_INDEX	= -1,
		FREE_LIST_INDEX	= -2
	};
};

class FDataStreamBase;

#define FLTA_ID_SHIFT				(13)
#define FLTA_MAX_BUCKETS			(1 << FLTA_ID_SHIFT)
#define FLTA_INDEX_MASK				(FLTA_MAX_BUCKETS - 1)
#define FLTA_ID_MASK				(~(FLTA_INDEX_MASK))
#define FLTA_GROWTH_FACTOR			(2)

/*	advc.003u: AIType has to be a concrete class or struct with a default constructor
	and functions getID, setID, read and write. If only T is given, then T has to satisfy
	these requirements (same as in BtS). If AIType!=T, then AIType needs to be derived from T,
	and all elements will have the type AIType. (The only point of this additional parameter
	is to avoid problems with type casts in client code.) */
template <class T, class AIType = T>
class FFreeListTrashArray
{
public:

	FFreeListTrashArray();
	~FFreeListTrashArray() { uninit(); }

	void init(int iNumSlots = 8);
	void uninit();
	T* getAt(int iID) const;
	AIType* AI_getAt(int iID) const
	{
		return AI(getAt(iID));
	}

	T* add();
	AIType* AI_add() { return AI(add()); }
	bool remove(T* pData);
	bool removeAt(int iID);
	void removeAll();

	void load(T* pData);

	int getNumSlots() const
	{
		return m_iNumSlots;
	}
	int getLastIndex() const
	{
		return m_iLastIndex;
	}
	void setLastIndex(int iNewValue)
	{
		m_iLastIndex = iNewValue;
	}
	int getFreeListHead() const
	{
		return m_iFreeListHead;
	}
	void setFreeListHead(int iNewValue)
	{
		m_iFreeListHead = iNewValue;
	}
	int getFreeListCount() const
	{
		return m_iFreeListCount;
	}
	void setFreeListCount(int iNewValue)
	{
		m_iFreeListCount = iNewValue;
	}
	int getCurrentID()
	{
		return m_iCurrentID;
	}
	void setCurrentID(int iNewValue)
	{
		FAssert((iNewValue & FLTA_INDEX_MASK) == 0);
		FAssert((iNewValue & FLTA_ID_MASK) != 0);
		m_iCurrentID = iNewValue;
	}
	int getNextFreeIndex(int iIndex)
	{
		if (iIndex >= getNumSlots() || m_pArray == NULL)
		{
			FAssert(false);
			return FFreeList::INVALID_INDEX;
		}
		return m_pArray[iIndex].iNextFreeIndex;
	}
	void setNextFreeIndex(int iIndex, int iNewValue)
	{
		if (iIndex >= getNumSlots() || m_pArray == NULL)
		{
			FAssert(false);
			return;
		}
		m_pArray[iIndex].iNextFreeIndex = iNewValue;
	}

	void Read(FDataStreamBase* pStream);
	void Write(FDataStreamBase* pStream);

	// advc: The rest of the public functions are from FFreeListArrayBase ...

	T* operator[](int iIndex) const
	{
		return getAt(iIndex);
	}

	// start at the beginning of the list and return the first item or NULL when done
	T* beginIter(int* pIterIdx) const
	{
		*pIterIdx = 0;
		return nextIter(pIterIdx);
	}
	AIType* AI_beginIter(int* pIterIdx) const
	{
		return AI(beginIter(pIterIdx));
	}

	// iterate from the current position and return the next item found or NULL when done
	T* nextIter(int* pIterIdx) const
	{
		for(; (*pIterIdx) < getIndexAfterLast(); (*pIterIdx)++)
		{
			T* pObj = getAt(*pIterIdx);
			if (pObj != NULL)
			{
				(*pIterIdx)++; // prime for next call
				return pObj;
			}
		}
		return NULL;
	}
	AIType* AI_nextIter(int* pIterIdx) const
	{
		return AI(nextIter(pIterIdx));
	}

	// start at the end of the list and return the last item or NULL when done
	T* endIter(int* pIterIdx) const
	{
		*pIterIdx = getIndexAfterLast()-1;
		return prevIter(pIterIdx);
	}
	AIType* AI_endIter(int* pIterIdx) const
	{
		return AI(endIter(pIterIdx));
	}

	// iterate from the current position and return the prev item found or NULL when done
	T* prevIter(int* pIterIdx) const
	{
		for(; (*pIterIdx) >= 0; (*pIterIdx)--)
		{
			T* pObj = getAt(*pIterIdx);
			if (pObj != NULL)
			{
				(*pIterIdx)--; // prime for next call
				return pObj;
			}
		}
		return NULL;
	}
	AIType* AI_prevIter(int* pIterIdx) const
	{
		return AI(prevIter(pIterIdx));
	}

	// Returns the iIndex after the last iIndex in the array containing an element
	int getIndexAfterLast() const { return m_iLastIndex + 1; }

	/*	Returns the number of elements in the array (NOTE: this is a non-packed array, so
		this value is NOT the last iIndex in the array...) */
	int getCount() const { return m_iLastIndex - m_iFreeListCount + 1; }

protected:
	// <advc> (from FFreeListArrayBase)
	int m_iFreeListHead;
	int m_iFreeListCount;
	int m_iLastIndex;
	int m_iNumSlots;
	// </advc>
	struct FFreeListTrashArrayNode
	{
		int iNextFreeIndex;
		T* pData;
	};
	int m_iCurrentID;
	FFreeListTrashArrayNode* m_pArray;

	void growArray();
	/*	advc.003u: This cast is safe b/c the add function only creates AIType objects.
		Cf. other cast wrapper functions, e.g. CvPlayer::AI. */
	AIType* AI(T* pData) const
	{
		return reinterpret_cast<AIType*>(pData);
	}
};

// Serialization helper templates - use when list contains streamable types
template<class T, class AIType>
void ReadStreamableFFreeListTrashArray(
	FFreeListTrashArray<T,AIType>& flist, FDataStreamBase* pStream);

template<class T, class AIType>
void WriteStreamableFFreeListTrashArray(
	FFreeListTrashArray<T,AIType>& flist, FDataStreamBase* pStream);

#endif
