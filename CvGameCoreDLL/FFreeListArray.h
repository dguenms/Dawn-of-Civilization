#pragma once

//	$Revision: #2 $		$Author: mbreitkreutz $ 	$DateTime: 2005/06/13 13:35:55 $
//------------------------------------------------------------------------------------------------
//
//  *****************   FIRAXIS GAME ENGINE   ********************
//
//  FILE:    FFreeListArray.h
//
//  AUTHOR:  Soren Johnson
//
//  PURPOSE: A dynamic array with a free list...
//
//------------------------------------------------------------------------------------------------
//  Copyright (c) 2004 Firaxis Games, Inc. All rights reserved.
//------------------------------------------------------------------------------------------------

#ifndef		FFREELISTARRAY_H
#define		FFREELISTARRAY_H
#pragma		once

#include	"FFreeListArrayBase.h"
#include	"FDataStreamBase.h"

template <class T>
class FFreeListArray : public FFreeListArrayBase<T>
{
public:

	FFreeListArray();
	virtual ~FFreeListArray();

	virtual void init(int iNumSlots = 8);
	virtual void uninit();
	virtual T* getAt(int iIndex);

	void insert(T data);
	void insertAt(T data, int iIndex);
	void insertFirst(T data);

	int getIndex(T data);

	bool remove(T data);
	bool removeAt(int iIndex);
	virtual void removeAll();

	void Read( FDataStreamBase* pStream );
	void Write( FDataStreamBase* pStream );


protected:

	struct DArrayNode
	{
		int iNextFreeIndex;
		T		data;
	};

	DArrayNode* m_pArray;

	virtual void growArray();
};



// Public Functions...

template <class T>
FFreeListArray<T>::FFreeListArray()
{
	m_iFreeListHead = FFreeList::FLA_FREE_LIST_INDEX;
	m_iFreeListCount = 0;
	m_iLastIndex = FFreeList::INVALID_INDEX;
	m_iNumSlots = 0;

	m_pArray = NULL;
}


template <class T>
FFreeListArray<T>::~FFreeListArray()
{
	uninit();
}


template <class T>
void FFreeListArray<T>::init(int iNumSlots)
{
	int iI;

	uninit();

	m_iFreeListHead = FLA_FREE_LIST_INDEX;
	m_iFreeListCount = 0;
	m_iLastIndex = FFreeList::INVALID_INDEX;
	m_iNumSlots = iNumSlots;

	if (m_iNumSlots > 0)
	{
		m_pArray = new DArrayNode[m_iNumSlots];

		for (iI = 0; iI < m_iNumSlots; iI++)
		{
			m_pArray[iI].iNextFreeIndex = FFreeList::INVALID_INDEX;
		}
	}
}


template <class T>
void FFreeListArray<T>::uninit()
{
	if (m_pArray != NULL)
	{
		removeAll();

		SAFE_DELETE_ARRAY(m_pArray);
	}
}


template <class T>
void FFreeListArray<T>::insert(T data)
{
	int iIndex;

	if (m_pArray == NULL) 
	{
		init();
	}

	if ((m_iLastIndex == m_iNumSlots - 1) && 
		(m_iFreeListCount == 0)) 
	{
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

	m_pArray[iIndex].data = data;
	m_pArray[iIndex].iNextFreeIndex = FFreeList::INVALID_INDEX;
}


template <class T>
void FFreeListArray<T>::insertAt(T data, int iIndex)
{
	int iTempIndex;

	if (m_pArray == NULL) 
	{
		init();
	}

	if (iIndex <= m_iLastIndex)
	{
		if (m_pArray[iIndex].iNextFreeIndex == FFreeList::INVALID_INDEX)
		{
			m_pArray[iIndex].data = data;
			return;
		}
	}

	while (iIndex > m_iNumSlots - 1)
	{
		growArray();
	}

	if (iIndex > m_iLastIndex)
	{
		while (iIndex != m_iLastIndex + 1)
		{
			m_iLastIndex++;
			m_pArray[m_iLastIndex].iNextFreeIndex = m_iFreeListHead;
			m_iFreeListHead = m_iLastIndex;
			m_iFreeListCount++;
		}

		m_iLastIndex++;
	}

	m_pArray[iIndex].data = data;

	if (m_iFreeListHead != FLA_FREE_LIST_INDEX)
	{
		if (iIndex == m_iFreeListHead)
		{
			m_iFreeListHead = m_pArray[iIndex].iNextFreeIndex;
			m_iFreeListCount--;
		}
		else
		{
			iTempIndex = m_iFreeListHead;
			while (iTempIndex != FLA_FREE_LIST_INDEX)
			{
				assert(iTempIndex != FFreeList::INVALID_INDEX);
				if (m_pArray[iTempIndex].iNextFreeIndex == iIndex)
				{
					m_pArray[iTempIndex].iNextFreeIndex = m_pArray[iIndex].iNextFreeIndex;
					m_iFreeListCount--;
					break;
				}
				iTempIndex = m_pArray[iTempIndex].iNextFreeIndex;
			}
		}
	}

	m_pArray[iIndex].iNextFreeIndex = FFreeList::INVALID_INDEX;
}


template <class T>
void FFreeListArray<T>::insertFirst(T data)
{
	int iI;

	if (m_pArray == NULL) 
	{
		init();
	}

	if ((m_iLastIndex == m_iNumSlots - 1) && 
		(m_iFreeListCount == 0)) 
	{
		growArray();
	}

	for (iI = 0; iI <= m_iLastIndex; iI++)
	{
		if (m_pArray[iI].iNextFreeIndex != FFreeList::INVALID_INDEX)
		{
			insertAt(data, iI);
			return;
		}
	}

	insert(data);
}


template <class T>
T* FFreeListArray<T>::getAt(int iIndex)
{
	if ((m_pArray == NULL) || (iIndex == FFreeList::INVALID_INDEX))
	{
		return NULL;
	}

	if ((iIndex >= 0) && (iIndex <= m_iLastIndex)) 
	{
		if (m_pArray[iIndex].iNextFreeIndex == FFreeList::INVALID_INDEX)
		{
			return &(m_pArray[iIndex].data);
		}
	}

	return NULL;
}


template <class T>
int FFreeListArray<T>::getIndex(T data)
{
	int iI;

	if (m_pArray == NULL)
	{
		return FFreeList::INVALID_INDEX;
	}

	for (iI = 0; iI <= m_iLastIndex; iI++)
	{
		if (m_pArray[iI].iNextFreeIndex == FFreeList::INVALID_INDEX)
		{
			if (m_pArray[iI].data == data)
			{
				return iI;
			}
		}
	}

	return FFreeList::INVALID_INDEX;
}


template <class T>
bool FFreeListArray<T>::remove(T data)
{
	int iI;

	assert(m_pArray != NULL);

	for (iI = 0; iI <= m_iLastIndex; iI++)
	{
		if (m_pArray[iI].iNextFreeIndex == FFreeList::INVALID_INDEX)
		{
			if (m_pArray[iI].data == data)
			{
				return removeAt(iI);
			}
		}
	}

	return false;
}


template <class T>
bool FFreeListArray<T>::removeAt(int iIndex)
{
	assert(m_pArray != NULL);

	if ((iIndex >= 0) && (iIndex <= m_iLastIndex))
	{
		if (m_pArray[iIndex].iNextFreeIndex == FFreeList::INVALID_INDEX)
		{
			m_pArray[iIndex].iNextFreeIndex = m_iFreeListHead;
			m_iFreeListHead = iIndex;
			m_iFreeListCount++;

			return true;
		}
	}

	return false;
}


template <class T>
void FFreeListArray<T>::removeAll()
{
	int iI;

	if (m_pArray == NULL)
	{
		return;
	}

	m_iFreeListHead = FLA_FREE_LIST_INDEX;
	m_iFreeListCount = 0;
	m_iLastIndex = FFreeList::INVALID_INDEX;

	for (iI = 0; iI < m_iNumSlots; iI++)
	{
		m_pArray[iI].iNextFreeIndex = FFreeList::INVALID_INDEX;
	}
}

// Protected functions...

template <class T>
void FFreeListArray<T>::growArray()
{
	DArrayNode* pOldArray;
	int iOldNumSlots;
	int iI;

	pOldArray = m_pArray;
	iOldNumSlots = m_iNumSlots;

	m_iNumSlots *= 2;
	m_pArray = new DArrayNode[m_iNumSlots];

	for (iI = 0; iI < m_iNumSlots; iI++)
	{
		if (iI < iOldNumSlots)
		{
			m_pArray[iI] = pOldArray[iI];
		}
		else
		{
			m_pArray[iI].iNextFreeIndex = FFreeList::INVALID_INDEX;
		}
	}

	delete [] pOldArray;
}

//
// use when list contains non-streamable types
//
template < class T >
inline void FFreeListArray< T >::Read( FDataStreamBase* pStream )
{
	int iCount = 0;
	pStream->Read( &iCount );
	init( iCount );

	if ( iCount )
	{
		for ( int i = 0; i < iCount; i++ )
		{
			T* pData = new T;
			pStream->Read( sizeof ( T ), ( byte* )pData );
			insert( pData );
		}
	}
}

template < class T >
inline void FFreeListArray< T >::Write( FDataStreamBase* pStream )
{
	int iCount = getCount();
	pStream->Write( iCount );

	for ( int i = 0; i < getIndexAfterLast(); i++ )
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
inline void ReadStreamableFFreeListArray( FFreeListArray< T >& flist, FDataStreamBase* pStream )
{
	int iCount = 0;
	pStream->Read( &iCount );
	flist.init( iCount );

	if ( iCount )
	{
		for ( int i = 0; i < iCount; i++ )
		{
			T* pData = new T;
			pData->read( pStream );
			flist.insert( pData );
		}
	}
}

//
// use when list contains streamable types
//
template < class T >
inline void WriteStreamableFFreeListArray( FFreeListArray< T >& flist, FDataStreamBase* pStream )
{
	int iCount = flist.getCount();
	pStream->Write( iCount );

	for ( int i = 0; i < flist.getIndexAfterLast(); i++ )
	{
		if ( flist[ i ] )
		{
			flist[ i ]->write( pStream );
		}
	}
}

#endif	//FFREELISTARRAY_H
