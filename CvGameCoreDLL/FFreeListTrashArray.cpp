#include "CvGameCoreDLL.h"
#include "FFreeListTrashArray.h"
#include "CvUnitAI.h"
#include "CvCityAI.h"
#include "CvSelectionGroupAI.h"
#include "CvPlotGroup.h"
#include "CvArea.h"
#include "CvDeal.h"

/*	advc.003u: Implementation file for FLTA functions that are clearly too large
	to be inlined or that need to access member functions of T or AIType. */


/*	(advc: Could replace the 'new' calls with this in order to instantiate
	T and AIType with pointers instead of classes and structs.) */
/*namespace
{
	template<class ConcreteType>
	// Note: The parameter is only for type inference
	ConcreteType* createElement(ConcreteType*)
	{
		return new ConcreteType();
	}
}*/


template<class T,class AIType>
FFreeListTrashArray<T,AIType>::FFreeListTrashArray()
{
	// <advc> From FFreeListArrayBase constructor
	m_iFreeListHead = FFreeList::FREE_LIST_INDEX;
	m_iFreeListCount = 0;
	m_iLastIndex = FFreeList::INVALID_INDEX;
	m_iNumSlots = 0; // </advc>
	m_iCurrentID = FLTA_MAX_BUCKETS;
	m_pArray = NULL;
}


template<class T,class AIType>
void FFreeListTrashArray<T,AIType>::init(int iNumSlots)
{
	FAssert(iNumSlots >= 0);

	// make sure it's binary...
	if (iNumSlots > 0 && ((iNumSlots - 1) & iNumSlots) != 0)
	{
		// find high bit
		int iCount = 0;
		while (iNumSlots != 1)
		{
			iNumSlots >>= 1;
			iCount++;
		}
		iNumSlots = (1 << (iCount + 1));
	}

	FAssert(((iNumSlots - 1) & iNumSlots) == 0);
	FAssertMsg(m_iNumSlots <= FLTA_MAX_BUCKETS, "FFreeListTrashArray::init() size too large");

	uninit();

	m_iNumSlots = iNumSlots;
	m_iLastIndex = FFreeList::INVALID_INDEX;
	m_iFreeListHead = FFreeList::INVALID_INDEX;
	m_iFreeListCount = 0;
	m_iCurrentID = FLTA_MAX_BUCKETS;

	if (m_iNumSlots > 0)
	{
		m_pArray = new FFreeListTrashArrayNode[m_iNumSlots];
		for (int iI = 0; iI < m_iNumSlots; iI++)
		{
			m_pArray[iI].iNextFreeIndex = FFreeList::INVALID_INDEX;
			m_pArray[iI].pData = NULL;
		}
	}
}


template<class T,class AIType>
void FFreeListTrashArray<T,AIType>::uninit()
{
	if (m_pArray != NULL)
	{
		removeAll();
		SAFE_DELETE_ARRAY(m_pArray);
	}
	// advc: Seems necessary. Don't know why it worked w/o this before the merge w/ FFreeListArrayBase.
	m_iNumSlots = 0;
}


template<class T,class AIType>
T* FFreeListTrashArray<T,AIType>::add()
{
	if (m_pArray == NULL)
		init();

	if (m_iLastIndex == m_iNumSlots - 1 && m_iFreeListCount == 0)
	{
		if (m_iNumSlots * FLTA_GROWTH_FACTOR > FLTA_MAX_BUCKETS)
			return NULL;
		growArray();
	}

	int iIndex = m_iFreeListHead;
	if (m_iFreeListCount > 0)
	{
		m_iFreeListHead = m_pArray[m_iFreeListHead].iNextFreeIndex;
		m_iFreeListCount--;
	}
	else
	{
		m_iLastIndex++;
		iIndex = m_iLastIndex;
	}
	m_pArray[iIndex].pData = new AIType;
	m_pArray[iIndex].iNextFreeIndex = FFreeList::INVALID_INDEX;

	m_pArray[iIndex].pData->setID(m_iCurrentID + iIndex);
	m_iCurrentID += FLTA_MAX_BUCKETS;

	return m_pArray[iIndex].pData;
}


template<class T,class AIType>
T* FFreeListTrashArray<T,AIType>::getAt(int iID) const
{
	if (iID == FFreeList::INVALID_INDEX) //|| m_pArray == NULL // advc.opt
		return NULL;

	int iIndex = (iID & FLTA_INDEX_MASK);
	FAssert(iIndex >= 0);
	if (iIndex <= m_iLastIndex && m_pArray[iIndex].pData != NULL)
	{
		if ((iID & FLTA_ID_MASK) == 0 || m_pArray[iIndex].pData->getID() == iID)
			return m_pArray[iIndex].pData;
	}
	return NULL;
}


template<class T,class AIType>
bool FFreeListTrashArray<T,AIType>::remove(T* pData)
{
	FAssert(m_pArray != NULL);
	if (pData != NULL)
	{
		for (int i = 0; i <= m_iLastIndex; i++)
		{
			if (m_pArray[i].pData == pData)
				return removeAt(i);
		}
	}
	return false;
}


template<class T,class AIType>
bool FFreeListTrashArray<T,AIType>::removeAt(int iID)
{
	if (iID == FFreeList::INVALID_INDEX || m_pArray == NULL)
		return false;

	int iIndex = (iID & FLTA_INDEX_MASK);
	FAssert(iIndex >= 0);
	if (iIndex <= m_iLastIndex && m_pArray[iIndex].pData != NULL)
	{
		if ((iID & FLTA_ID_MASK) == 0 || m_pArray[iIndex].pData->getID() == iID)
		{
			SAFE_DELETE(m_pArray[iIndex].pData);
			m_pArray[iIndex].iNextFreeIndex = m_iFreeListHead;
			m_iFreeListHead = iIndex;
			m_iFreeListCount++;
			return true;
		}
		FAssert(false);
	}
	return false;
}


template<class T,class AIType>
void FFreeListTrashArray<T,AIType>::removeAll()
{
	if (m_pArray == NULL)
		return;

	m_iLastIndex = FFreeList::INVALID_INDEX;
	m_iFreeListHead = FFreeList::INVALID_INDEX;
	m_iFreeListCount = 0;

	for (int i = 0; i < m_iNumSlots; i++)
	{
		m_pArray[i].iNextFreeIndex = FFreeList::INVALID_INDEX;
		SAFE_DELETE(m_pArray[i].pData);
	}
}


template<class T,class AIType>
void FFreeListTrashArray<T,AIType>::load(T* pData)
{
	FAssert(pData != NULL);
	FAssert((pData->getID() & FLTA_ID_MASK) < m_iCurrentID);
	FAssert(m_pArray != NULL);

	int iIndex = (pData->getID() & FLTA_INDEX_MASK);

	FAssert(iIndex < FLTA_MAX_BUCKETS);
	FAssert(iIndex <= m_iLastIndex);
	FAssert(m_pArray[iIndex].pData == NULL);
	FAssert(m_pArray[iIndex].iNextFreeIndex == FFreeList::INVALID_INDEX);

	m_pArray[iIndex].pData = pData;
}


template<class T,class AIType>
void FFreeListTrashArray<T,AIType>::growArray()
{
	FAssert(m_pArray != NULL);
	FFreeListTrashArrayNode* pOldArray = m_pArray;
	int const iOldNumSlots = m_iNumSlots;

	m_iNumSlots *= FLTA_GROWTH_FACTOR;
	FAssertMsg(m_iNumSlots <= FLTA_MAX_BUCKETS, "FFreeListTrashArray::growArray() size too large");
	m_pArray = new FFreeListTrashArrayNode[m_iNumSlots];

	for (int i = 0; i < m_iNumSlots; i++)
	{
		if (i < iOldNumSlots)
			m_pArray[i] = pOldArray[i];
		else
		{
			m_pArray[i].iNextFreeIndex = FFreeList::INVALID_INDEX;
			m_pArray[i].pData = NULL;
		}
	}

	delete[] pOldArray;
}

//
// use when list contains non-streamable types
//
template<class T,class AIType>
void FFreeListTrashArray<T,AIType>::Read(FDataStreamBase* pStream)
{
	int iTemp;
	pStream->Read( &iTemp );
	init(iTemp);
	pStream->Read(&iTemp);
	setLastIndex(iTemp);
	pStream->Read(&iTemp);
	setFreeListHead(iTemp);
	pStream->Read(&iTemp);
	setFreeListCount(iTemp);
	pStream->Read(&iTemp);
	setCurrentID(iTemp);

	for (int i = 0; i < getNumSlots(); i++)
	{
		pStream->Read(&iTemp);
		setNextFreeIndex(i, iTemp);
	}

	int iCount;
	pStream->Read(&iCount);
	for (int i = 0; i < iCount; i++)
	{
		AIType* pData = new AIType;
		pStream->Read(sizeof(*pData), (byte*)pData);
		load(pData);
	}
}

template<class T,class AIType>
void FFreeListTrashArray<T,AIType>::Write(FDataStreamBase* pStream)
{
	pStream->Write(getNumSlots());
	pStream->Write(getLastIndex());
	pStream->Write(getFreeListHead());
	pStream->Write(getFreeListCount());
	pStream->Write(getCurrentID());

	for (int i = 0; i < getNumSlots(); i++)
	{
		pStream->Write(getNextFreeIndex(i));
	}

	pStream->Write(getCount());
	for (int i = 0; i < getIndexAfterLast(); i++)
	{
		AIType* pData = AI_getAt(i);
		if (pData != NULL)
			pStream->Write(sizeof(*pData), (byte*)pData);
	}
}


template<class T,class AIType>
void ReadStreamableFFreeListTrashArray(
	FFreeListTrashArray<T,AIType>& flist, FDataStreamBase* pStream)
{
	int iTemp;
	pStream->Read(&iTemp);
	flist.init(iTemp);
	pStream->Read(&iTemp);
	flist.setLastIndex(iTemp);
	pStream->Read(&iTemp);
	flist.setFreeListHead(iTemp);
	pStream->Read(&iTemp);
	flist.setFreeListCount(iTemp);
	pStream->Read(&iTemp);
	flist.setCurrentID(iTemp);

	for (int i = 0; i < flist.getNumSlots(); i++)
	{
		pStream->Read(&iTemp);
		flist.setNextFreeIndex(i, iTemp);
	}

	int iCount;
	pStream->Read(&iCount);
	for (int i = 0; i < iCount; i++)
	{
		AIType* pData = new AIType;
		pData->read(pStream);
		flist.load(pData);
	}
}

template<class T,class AIType>
void WriteStreamableFFreeListTrashArray(
	FFreeListTrashArray<T,AIType>& flist, FDataStreamBase* pStream)
{
	pStream->Write(flist.getNumSlots());
	pStream->Write(flist.getLastIndex());
	pStream->Write(flist.getFreeListHead());
	pStream->Write(flist.getFreeListCount());
	pStream->Write(flist.getCurrentID());

	for (int i = 0; i < flist.getNumSlots(); i++)
	{
		pStream->Write(flist.getNextFreeIndex(i));
	}

	pStream->Write(flist.getCount());
	for (i = 0; i < flist.getIndexAfterLast(); i++)
	{
		if (flist[i] != NULL)
			flist[i]->write(pStream);
	}
}

// advc.003u: Explicit instantiations (for linker)

#define DO_FOR_EACH_FLTA_TYPE(DO) \
	DO(CvUnit,CvUnitAI) \
	DO(CvCity,CvCityAI) \
	DO(CvSelectionGroup,CvSelectionGroupAI) \
	DO(CvPlotGroup,CvPlotGroup) \
	DO(CvArea,CvArea) \
	DO(CvDeal,CvDeal) \
	DO(VoteSelectionData,VoteSelectionData) \
	DO(VoteTriggeredData,VoteTriggeredData) \
	DO(EventTriggeredData,EventTriggeredData)

#define INSTANTIATE_FLTA(T, AIType) \
	template class FFreeListTrashArray<T,AIType>; \
	template void ReadStreamableFFreeListTrashArray(FFreeListTrashArray<T,AIType>&, FDataStreamBase*); \
	template void WriteStreamableFFreeListTrashArray(FFreeListTrashArray<T,AIType>&, FDataStreamBase*);

DO_FOR_EACH_FLTA_TYPE(INSTANTIATE_FLTA);
