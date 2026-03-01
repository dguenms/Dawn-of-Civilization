#pragma once
#ifndef LINKEDLIST_H
#define LINKEDLIST_H

// LinkedList.h: A doubly-linked list
/*	advc.003k (note): This class appears to have been compiled into the EXE
	(it occurs in the parameter lists of exported CvPlayer member functions),
	so changing the memory layout may not be safe. */

#include "LinkedListTraversal.h" // advc.003s

template <class tVARTYPE> class CLinkList;

template <class tVARTYPE> class CLLNode
{
public:
	explicit CLLNode(const tVARTYPE& val)
	:	m_data(val), m_pNext(NULL), m_pPrev(NULL) {}
	virtual ~CLLNode() {}
	tVARTYPE m_data;

	friend class CLinkList<tVARTYPE>;
protected:
	CLLNode<tVARTYPE>*	m_pNext;
	CLLNode<tVARTYPE>*	m_pPrev;

};

/*	advc: Minor refactoring.
	Removed unnecessary assertions. assert calls replaced with FAssert. */
template <class tVARTYPE> class CLinkList /* advc.003e: */ : private boost::noncopyable
{
public:
	CLinkList() : m_iLength(0), m_pHead(NULL), m_pTail(NULL) {}
	virtual ~CLinkList();

	void clear();
	void swap(CLinkList<tVARTYPE>& list); // K-Mod: swap the contents of two lists
	// K-Mod: move the contents from the argument list onto the end of this list
	void concatenate(CLinkList<tVARTYPE>& list);

	void insertAtBeginning(const tVARTYPE& val);
	void insertAtEnd(const tVARTYPE& val);
	void insertBefore(const tVARTYPE& val, CLLNode<tVARTYPE>* pThisNode);
	void insertAfter(const tVARTYPE& val, CLLNode<tVARTYPE>* pThisNode);
	CLLNode<tVARTYPE>* deleteNode(CLLNode<tVARTYPE>*& pNode);
	void moveToEnd(CLLNode<tVARTYPE>* pThisNode);

	CLLNode<tVARTYPE>* next(CLLNode<tVARTYPE>* pNode) const { return pNode->m_pNext; }
	CLLNode<tVARTYPE>* prev(CLLNode<tVARTYPE>* pNode) const { return pNode->m_pPrev; }
	// <advc.003s>
	CLLNode<tVARTYPE> const* next(CLLNode<tVARTYPE> const* pNode) const { return pNode->m_pNext; }
	CLLNode<tVARTYPE> const* prev(CLLNode<tVARTYPE> const* pNode) const { return pNode->m_pPrev; }
	static CLLNode<tVARTYPE> const* static_next(CLLNode<tVARTYPE> const* pNode) { return pNode->m_pNext; }
	static CLLNode<tVARTYPE>* static_next(CLLNode<tVARTYPE>* pNode) { return pNode->m_pNext; }
	// </advc.003s>

	CLLNode<tVARTYPE>* nodeNum(int iNum) const;

	// use when linked list contains non-streamable types ...
	void Read(FDataStreamBase* pStream);
	void Write(FDataStreamBase* pStream) const;

	int getLength() const
	{
		return m_iLength;
	}

	CLLNode<tVARTYPE>* head() const
	{
		return m_pHead;
	}

	CLLNode<tVARTYPE>* tail() const
	{
		return m_pTail;
	}

protected:
	int m_iLength;
	CLLNode<tVARTYPE>* m_pHead;
	CLLNode<tVARTYPE>* m_pTail;
};


template <class tVARTYPE>
CLinkList<tVARTYPE>::~CLinkList()
{
	clear();
}


template <class tVARTYPE>
void CLinkList<tVARTYPE>::clear()
{
	CLLNode<tVARTYPE>* pCurrNode = m_pHead;
	while (pCurrNode != NULL)
	{
		CLLNode<tVARTYPE>* pNextNode = pCurrNode->m_pNext;
		SAFE_DELETE(pCurrNode);
		pCurrNode = pNextNode;
	}
	m_iLength = 0;
	m_pHead = m_pTail = NULL;
}

// K-Mod. (I wish they had just used the STL...)
template <class tVARTYPE>
void CLinkList<tVARTYPE>::swap(CLinkList<tVARTYPE>& list)
{
	std::swap(m_pHead, list.m_pHead);
	std::swap(m_pTail, list.m_pTail);
	std::swap(m_iLength, list.m_iLength);
}


template <class tVARTYPE>
void CLinkList<tVARTYPE>::concatenate(CLinkList<tVARTYPE>& list)
{
	if (list.m_pHead == NULL)
		return;

	if (m_pTail)
	{
		m_pTail->m_pNext = list.m_pHead;
		list.m_pHead->m_pPrev = m_pTail;
	}
	else
	{
		assert(m_pHead == NULL && m_iLength == 0);
		m_pHead = list.m_pHead;
	}
	assert(list.m_pTail != NULL);
	m_pTail = list.m_pTail;
	m_iLength += list.m_iLength;

	list.m_iLength = 0;
	list.m_pHead = 0;
	list.m_pTail = 0;
} // K-Mod end


template <class tVARTYPE>
void CLinkList<tVARTYPE>::insertAtBeginning(const tVARTYPE& val)
{
	FAssert(m_pHead == NULL || m_iLength > 0);
	CLLNode<tVARTYPE>* pNode = new CLLNode<tVARTYPE>(val);
	if (m_pHead != NULL)
	{
		m_pHead->m_pPrev = pNode;
		pNode->m_pNext = m_pHead;
		m_pHead = pNode;
	}
	else
	{
		m_pHead = pNode;
		m_pTail = pNode;
	}
	m_iLength++;
}


template <class tVARTYPE>
void CLinkList<tVARTYPE>::insertAtEnd(const tVARTYPE& val)
{
	FAssert(m_pHead == NULL || m_iLength > 0);
	CLLNode<tVARTYPE>* pNode = new CLLNode<tVARTYPE>(val);
	if (m_pTail != NULL)
	{
		m_pTail->m_pNext = pNode;
		pNode->m_pPrev = m_pTail;
		m_pTail = pNode;
	}
	else
	{
		m_pHead = pNode;
		m_pTail = pNode;
	}
	m_iLength++;
}


template <class tVARTYPE>
void CLinkList<tVARTYPE>::insertBefore(const tVARTYPE& val, CLLNode<tVARTYPE>* pThisNode)
{
	FAssert(m_pHead == NULL || m_iLength > 0);
	if (pThisNode == NULL || pThisNode->m_pPrev == NULL)
	{
		insertAtBeginning(val);
		return;
	}
	CLLNode<tVARTYPE>* pNode = new CLLNode<tVARTYPE>(val);

	pThisNode->m_pPrev->m_pNext = pNode;
	pNode->m_pPrev = pThisNode->m_pPrev;
	pThisNode->m_pPrev = pNode;
	pNode->m_pNext = pThisNode;

	m_iLength++;
}


template <class tVARTYPE>
void CLinkList<tVARTYPE>::insertAfter(const tVARTYPE& val, CLLNode<tVARTYPE>* pThisNode)
{
	FAssert(m_pHead == NULL || m_iLength > 0);
	if (pThisNode == NULL || pThisNode->m_pNext == NULL)
	{
		insertAtEnd(val);
		return;
	}
	CLLNode<tVARTYPE>*pNode = new CLLNode<tVARTYPE>(val);

	pThisNode->m_pNext->m_pPrev = pNode;
	pNode->m_pNext = pThisNode->m_pNext;
	pThisNode->m_pNext = pNode;
	pNode->m_pPrev = pThisNode;

	m_iLength++;
}


template <class tVARTYPE>
CLLNode<tVARTYPE>* CLinkList<tVARTYPE>::deleteNode(
	// advc: Take a reference so that we can set the caller's pointer to NULL
	CLLNode<tVARTYPE>*& pNode)
{
	CLLNode<tVARTYPE>* pPrevNode = pNode->m_pPrev;
	CLLNode<tVARTYPE>* pNextNode = pNode->m_pNext;
	if (pPrevNode != NULL && pNextNode != NULL)
	{
		pPrevNode->m_pNext = pNextNode;
		pNextNode->m_pPrev = pPrevNode;
	}
	else if (pPrevNode != NULL)
	{
		pPrevNode->m_pNext = NULL;
		m_pTail = pPrevNode;
	}
	else if (pNextNode != NULL)
	{
		pNextNode->m_pPrev = NULL;
		m_pHead = pNextNode;
	}
	else
	{
		m_pHead = NULL;
		m_pTail = NULL;
	}
	delete pNode;
	pNode = NULL;
	
	m_iLength--;
	return pNextNode;
}


template <class tVARTYPE>
void CLinkList<tVARTYPE>::moveToEnd(CLLNode<tVARTYPE>* pNode)
{
	if (getLength() == 1)
		return;

	if (pNode == m_pTail)
		return;

	CLLNode<tVARTYPE>* pPrevNode = pNode->m_pPrev;
	CLLNode<tVARTYPE>* pNextNode = pNode->m_pNext;

	if (pPrevNode != NULL && pNextNode != NULL)
	{
		pPrevNode->m_pNext = pNextNode;
		pNextNode->m_pPrev = pPrevNode;
	}
	else if (pPrevNode != NULL)
	{
		pPrevNode->m_pNext = NULL;
		m_pTail = pPrevNode;
	}
	else if (pNextNode != NULL)
	{
		pNextNode->m_pPrev = NULL;
		m_pHead = pNextNode;
	}
	else
	{
		m_pHead = NULL;
		m_pTail = NULL;
	}
	pNode->m_pNext = NULL;
	m_pTail->m_pNext = pNode;
	pNode->m_pPrev = m_pTail;
	m_pTail = pNode;
}


template <class tVARTYPE>
CLLNode<tVARTYPE>* CLinkList<tVARTYPE>::nodeNum(int iNum) const
{
	int iCount = 0;
	CLLNode<tVARTYPE>* pNode = m_pHead;
	while (pNode != NULL)
	{
		if (iCount == iNum)
			return pNode;
		iCount++;
		pNode = pNode->m_pNext;
	}
	return NULL;
}


template <class T>
void CLinkList<T>::Read(FDataStreamBase* pStream)
{
	clear();
	int iLength;
	pStream->Read(&iLength);
	if (iLength > 0)
	{
		T* pData = new T;
		for (int i = 0; i < iLength; i++)
		{
			pStream->Read(sizeof(T), (byte*)pData);
			insertAtEnd(*pData);
		}
		SAFE_DELETE(pData);
	}
}


template <class T>
void CLinkList<T>::Write(FDataStreamBase* pStream) const
{
	int iLength = getLength();
	pStream->Write(iLength);
	CLLNode<T>* pNode = head();
	while (pNode != NULL)
	{
		pStream->Write(sizeof(T),(byte*)&pNode->m_data);
		pNode = next(pNode);
	}
}


// Serialization helper templates: use when linked list contains streamable types ...

template<class T>
void ReadStreamableLinkList(CLinkList<T>& llist, FDataStreamBase* pStream)
{
	llist.init();
	int iLength;
	pStream->Read(&iLength);
	if (iLength > 0)
	{
		T* pData = new T;
		for (int i = 0; i < iLength; i++)
		{
			pData->read(pStream);
			llist.insertAtEnd(*pData);
		}
		SAFE_DELETE(pData);
	}
}


template <class T>
void WriteStreamableLinkList(CLinkList<T>& llist, FDataStreamBase* pStream)
{
	int iLength = llist.getLength();
	pStream->Write(iLength);
	CLLNode<T>* pNode = llist.head();
	while (pNode != NULL)
	{
		pNode->m_data.write(pStream);
		pNode = llist.next(pNode);
	}
}

#endif
