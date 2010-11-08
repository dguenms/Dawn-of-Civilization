#pragma once

//	$Revision: #2 $		$Author: mbreitkreutz $ 	$DateTime: 2005/06/13 13:35:55 $
//------------------------------------------------------------------------------------------------
//
//  *****************   FIRAXIS GAME ENGINE   ********************
//
//  FILE:    FFreeListTrashArray.h
//
//  AUTHOR:  Soren Johnson
//
//  PURPOSE: A dynamic array with a free list that keeps track of its own memory...
//
//------------------------------------------------------------------------------------------------
//  Copyright (c) 2004 Firaxis Games, Inc. All rights reserved.
//------------------------------------------------------------------------------------------------

#ifndef		FFREELISTTRASHARRAY_H
#define		FFREELISTTRASHARRAY_H
#pragma		once

#include	"FFreeListArrayBase.h"
#include	"FDataStreamBase.h"

#define FLTA_ID_SHIFT				(13)
#define FLTA_MAX_BUCKETS		(1 << FLTA_ID_SHIFT)
#define FLTA_INDEX_MASK			(FLTA_MAX_BUCKETS - 1)
#define FLTA_ID_MASK				(~(FLTA_INDEX_MASK))
#define FLTA_GROWTH_FACTOR	(2)

template <class T>
class FFreeListTrashArray : public FFreeListArrayBase<T>
{
public:

	FFreeListTrashArray();
	virtual ~FFreeListTrashArray();

	virtual void init(int iNumSlots = 8);
	virtual void uninit();
	virtual T* getAt(int iID) const;

	T* add();
	bool remove(T* pData);
	bool removeAt(int iID);
	virtual void removeAll();

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
		assert((iNewValue & FLTA_INDEX_MASK) == 0);
		assert((iNewValue & FLTA_ID_MASK) != 0);
		m_iCurrentID = iNewValue;
	}

	int getNextFreeIndex(int iIndex)
	{
		if ((iIndex >= getNumSlots()) || (m_pArray == NULL))
		{
			assert(false);
			return FFreeList::INVALID_INDEX;
		}
		return m_pArray[iIndex].iNextFreeIndex;
	}
	void setNextFreeIndex(int iIndex, int iNewValue)
	{
		if ((iIndex >= getNumSlots()) || (m_pArray == NULL))
		{
			assert(false);
			return;
		}
		m_pArray[iIndex].iNextFreeIndex = iNewValue;
	}

	void Read( FDataStreamBase* pStream );
	void Write( FDataStreamBase* pStream );

protected:

	struct FFreeListTrashArrayNode
	{
		int iNextFreeIndex;
		T* pData;
	};

	int m_iCurrentID;
	FFreeListTrashArrayNode* m_pArray;

	virtual void growArray();
};



// Public functions...

template <class T>
FFreeListTrashArray<T>::FFreeListTrashArray()
{
	m_iCurrentID = FLTA_MAX_BUCKETS;
	m_pArray = NULL;
}


template <class T>
FFreeListTrashArray<T>::~FFreeListTrashArray()
{
	uninit();
}


template <class T>
void FFreeListTrashArray<T>::init(int iNumSlots)
{
	int iCount;
	int iI;

	assert(iNumSlots >= 0);

	// make sure it's binary...
	if ((iNumSlots > 0) && ((iNumSlots - 1) & iNumSlots) != 0)
	{
		// find high bit
		iCount = 0;
		while (iNumSlots != 1)
		{
			iNumSlots >>= 1;
			iCount++;
		}
		iNumSlots = (1 << (iCount + 1));
	}

	assert(((iNumSlots - 1) & iNumSlots) == 0);
	assert((m_iNumSlots <= FLTA_MAX_BUCKETS) && "FFreeListTrashArray<T>::init() size too large");

	uninit();

	m_iNumSlots = iNumSlots;
	m_iLastIndex = FFreeList::INVALID_INDEX;
	m_iFreeListHead = FFreeList::INVALID_INDEX;
	m_iFreeListCount = 0;
	m_iCurrentID = FLTA_MAX_BUCKETS;

	if (m_iNumSlots > 0)
	{
		m_pArray = new FFreeListTrashArrayNode[m_iNumSlots];

		for (iI = 0; iI < m_iNumSlots; iI++)
		{
			m_pArray[iI].iNextFreeIndex = FFreeList::INVALID_INDEX;
			m_pArray[iI].pData = NULL;
		}
	}
}


template <class T>
void FFreeListTrashArray<T>::uninit()
{
	if (m_pArray != NULL)
	{
		removeAll();

		SAFE_DELETE_ARRAY(m_pArray);
	}
}


template <class T>
T* FFreeListTrashArray<T>::add()
{
	int iIndex;

	if (m_pArray == NULL) 
	{
		init();
	}

	if ((m_iLastIndex == m_iNumSlots - 1) &&
		(m_iFreeListCount == 0))
	{
		if ((m_iNumSlots * FLTA_GROWTH_FACTOR) > FLTA_MAX_BUCKETS)
		{
			return NULL;
		}

		growArray();
	}

	if (m_iFreeListCount > 0)
	{
		iIndex = m_iFreeListHead;
		m_iFreeListHead = m_pArray[m_iFreeListHead].iNextFreeIndex;
		m_iFreeListCount--;
	}
	else
	{
		m_iLastIndex++;
		iIndex = m_iLastIndex;
	}

	m_pArray[iIndex].pData = new T;
	m_pArray[iIndex].iNextFreeIndex = FFreeList::INVALID_INDEX;

	m_pArray[iIndex].pData->setID(m_iCurrentID + iIndex);
	m_iCurrentID += FLTA_MAX_BUCKETS;

	return m_pArray[iIndex].pData;
}


template <class T>
T* FFreeListTrashArray<T>::getAt(int iID) const
{
	int iIndex;

	if ((iID == FFreeList::INVALID_INDEX) || (m_pArray == NULL))
	{
		return NULL;
	}

	iIndex = (iID & FLTA_INDEX_MASK);

	assert(iIndex >= 0);

	if ((iIndex <= m_iLastIndex) && 
		(m_pArray[iIndex].pData != NULL))
	{
		if (((iID & FLTA_ID_MASK) == 0) || (m_pArray[iIndex].pData->getID() == iID))
		{
			return m_pArray[iIndex].pData;
		}
	}

	return NULL;
}


template <class T>
bool FFreeListTrashArray<T>::remove(T* pData)
{
	int iI;

	assert(m_pArray != NULL);

	if (pData != NULL)
	{
		for (iI = 0; iI <= m_iLastIndex; iI++)
		{
			if (m_pArray[iI].pData == pData)
			{
				return removeAt(iI);
			}
		}
	}

	return false;
}


template <class T>
bool FFreeListTrashArray<T>::removeAt(int iID)
{
	int iIndex;

	if ((iID == FFreeList::INVALID_INDEX) || (m_pArray == NULL))
	{
		return false;
	}

	iIndex = (iID & FLTA_INDEX_MASK);

	assert(iIndex >= 0);

	if ((iIndex <= m_iLastIndex) && 
		(m_pArray[iIndex].pData != NULL))
	{
		if (((iID & FLTA_ID_MASK) == 0) || (m_pArray[iIndex].pData->getID() == iID))
		{
			delete m_pArray[iIndex].pData;
			m_pArray[iIndex].pData = NULL;

			m_pArray[iIndex].iNextFreeIndex = m_iFreeListHead;
			m_iFreeListHead = iIndex;
			m_iFreeListCount++;

			return true;
		}
		else
		{
			assert(false);
		}
	}

	return false;
}


template <class T>
void FFreeListTrashArray<T>::removeAll()
{
	int iI;

	if (m_pArray == NULL)
	{
		return;
	}

	m_iLastIndex = FFreeList::INVALID_INDEX;
	m_iFreeListHead = FFreeList::INVALID_INDEX;
	m_iFreeListCount = 0;

	for (iI = 0; iI < m_iNumSlots; iI++)
	{
		m_pArray[iI].iNextFreeIndex = FFreeList::INVALID_INDEX;
		if (m_pArray[iI].pData != NULL)
		{
			delete m_pArray[iI].pData;
		}
		m_pArray[iI].pData = NULL;
	}
}


template <class T>
void FFreeListTrashArray<T>::load(T* pData)
{
	int iIndex;

	assert(pData != NULL);
	assert((pData->getID() & FLTA_ID_MASK) < m_iCurrentID);
	assert(m_pArray != NULL);

	iIndex = (pData->getID() & FLTA_INDEX_MASK);

	assert(iIndex < FLTA_MAX_BUCKETS);
	assert(iIndex <= m_iLastIndex);
	assert(m_pArray[iIndex].pData == NULL);
	assert(m_pArray[iIndex].iNextFreeIndex == FFreeList::INVALID_INDEX);

	m_pArray[iIndex].pData = pData;
}

// Protected functions...

template <class T>
void FFreeListTrashArray<T>::growArray()
{
	FFreeListTrashArrayNode* pOldArray;
	int iOldNumSlots;
	int iI;

	assert(m_pArray != NULL);

	pOldArray = m_pArray;
	iOldNumSlots = m_iNumSlots;

	m_iNumSlots *= FLTA_GROWTH_FACTOR;
	assert((m_iNumSlots <= FLTA_MAX_BUCKETS) && "FFreeListTrashArray<T>::growArray() size too large");
	m_pArray = new FFreeListTrashArrayNode[m_iNumSlots];

	for (iI = 0; iI < m_iNumSlots; iI++)
	{
		if (iI < iOldNumSlots)
		{
			m_pArray[iI] = pOldArray[iI];
		}
		else
		{
			m_pArray[iI].iNextFreeIndex = FFreeList::INVALID_INDEX;
			m_pArray[iI].pData = NULL;
		}
	}

	delete [] pOldArray;
}

//
// use when list contains non-streamable types
//
template < class T >
inline void FFreeListTrashArray< T >::Read( FDataStreamBase* pStream )
{
	int iTemp;
	pStream->Read( &iTemp );
	init( iTemp );
	pStream->Read( &iTemp );
	setLastIndex( iTemp );
	pStream->Read( &iTemp );
	setFreeListHead( iTemp );
	pStream->Read( &iTemp );
	setFreeListCount( iTemp );
	pStream->Read( &iTemp );
	setCurrentID( iTemp );

	int i;

	for ( i = 0; i < getNumSlots(); i++ )
	{
		pStream->Read( &iTemp );
		setNextFreeIndex( i, iTemp );
	}

	int iCount;
	pStream->Read( &iCount );

	for ( i = 0; i < iCount; i++ )
	{
		T* pData = new T;
		pStream->Read( sizeof ( T ), ( byte* )pData );
		load( pData );
	}
}

template < class T >
inline void FFreeListTrashArray< T >::Write( FDataStreamBase* pStream )
{
	pStream->Write( getNumSlots() );
	pStream->Write( getLastIndex() );
	pStream->Write( getFreeListHead() );
	pStream->Write( getFreeListCount() );
	pStream->Write( getCurrentID() );

	int i;

	for ( i = 0; i < getNumSlots(); i++ )
	{
		pStream->Write( getNextFreeIndex( i ) );
	}

	pStream->Write( getCount() );

	for ( i = 0; i < getIndexAfterLast(); i++ )
	{
		if ( getAt( i ) )
		{
			pStream->Write( sizeof ( T ), ( byte* )getAt( i ) );
		}
	}
}

//-------------------------------
// Serialization helper templates:
//-------------------------------

//
// use when list contains streamable types
//
template < class T >
inline void ReadStreamableFFreeListTrashArray( FFreeListTrashArray< T >& flist, FDataStreamBase* pStream )
{
	int iTemp;
	pStream->Read( &iTemp );
	flist.init( iTemp );
	pStream->Read( &iTemp );
	flist.setLastIndex( iTemp );
	pStream->Read( &iTemp );
	flist.setFreeListHead( iTemp );
	pStream->Read( &iTemp );
	flist.setFreeListCount( iTemp );
	pStream->Read( &iTemp );
	flist.setCurrentID( iTemp );

	int i;

	for ( i = 0; i < flist.getNumSlots(); i++ )
	{
		pStream->Read( &iTemp );
		flist.setNextFreeIndex( i, iTemp );
	}

	int iCount;
	pStream->Read( &iCount );

	for ( i = 0; i < iCount; i++ )
	{
		T* pData = new T;
		pData->read( pStream );
		flist.load( pData );
	}
}

template < class T >
inline void WriteStreamableFFreeListTrashArray( FFreeListTrashArray< T >& flist, FDataStreamBase* pStream )
{
	pStream->Write( flist.getNumSlots() );
	pStream->Write( flist.getLastIndex() );
	pStream->Write( flist.getFreeListHead() );
	pStream->Write( flist.getFreeListCount() );
	pStream->Write( flist.getCurrentID() );

	int i;

	for ( i = 0; i < flist.getNumSlots(); i++ )
	{
		pStream->Write( flist.getNextFreeIndex( i ) );
	}

	pStream->Write( flist.getCount() );

	for ( i = 0; i < flist.getIndexAfterLast(); i++ )
	{
		if ( flist[ i ] )
		{
			flist[ i ]->write( pStream );
		}
	}
}

#endif	//FFREELISTTRASHARRAY_H
