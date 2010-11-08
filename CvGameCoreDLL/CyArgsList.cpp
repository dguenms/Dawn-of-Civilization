#include "CvGameCoreDLL.h"
#include "CyArgsList.h"
#include "CyGlobalContext.h"
#include "CvDLLPythonIFaceBase.h"

//////////////////////////////////////////////////////
// CyArgsList
//////////////////////////////////////////////////////

void CyArgsList::add(int i) 
{ 
	push_back(PyInt_FromLong(i)); 
}

void CyArgsList::add(float f) 
{ 
	push_back(PyFloat_FromDouble(f)); 
}

// add PyObject
void CyArgsList::add(void* p) 
{ 
	push_back((PyObject*)p);	
}

// add null-terminated string
void CyArgsList::add(const char* s)
{
	push_back(PyString_FromString(s));
}

// add null-terminated string
void CyArgsList::add(const wchar* s)
{
	if (s)
		push_back(PyUnicode_FromWideChar(s, wcslen(s)));
	else
		push_back(PyUnicode_FromWideChar(L"", 0));
}

// add data string
void CyArgsList::add(const char* buf, int iLength)
{
	push_back(PyString_FromStringAndSize(buf, iLength));
}

// add float list
void CyArgsList::add(const float* buf, int iLength)
{
	PyObject* pList = PyList_New(iLength);	// new ref
	FAssertMsg(pList, "failed creating PyList");
	int i;
	for(i=0;i<iLength;i++)
	{
		PyObject* pItem=PyFloat_FromDouble(buf[i]);		// new ref
		FAssertMsg(pItem, "failed creating PyFloat");
		PyList_SetItem(pList, i, pItem);				// steals the ref, no unref necesary
	}
	push_back(pList);
}

// add byte list
void CyArgsList::add(const byte* buf, int iLength)
{
	PyObject* pList = PyList_New(iLength);	// new ref
	FAssertMsg(pList, "failed creating PyList");
	int i;
	for(i=0;i<iLength;i++)
	{
		PyObject* pItem=PyInt_FromLong(buf[i]);		// new ref
		FAssertMsg(pItem, "failed creating PyInt");
		PyList_SetItem(pList, i, pItem);				// steals the ref, no unref necesary
	}
	push_back(pList);
}

// add int list
void CyArgsList::add(const int* buf, int iLength)
{
	PyObject* pList = PyList_New(iLength);	// new ref
	FAssertMsg(pList, "failed creating PyList");
	int i;
	for(i=0;i<iLength;i++)
	{
		PyObject* pItem=PyInt_FromLong(buf[i]);		// new ref
		FAssertMsg(pItem, "failed creating PyInt");
		PyList_SetItem(pList, i, pItem);				// steals the ref, no unref necesary
	}
	push_back(pList);
}

void* CyArgsList::makeFunctionArgs() 
{ 
	return gDLL->getPythonIFace()->MakeFunctionArgs(m_aList, m_iCnt);
}

