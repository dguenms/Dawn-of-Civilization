#pragma once

#ifdef USE_MEMMANAGER
#if 0
void* operator new(size_t size);
void* operator new[](size_t size);
void operator delete(void* pvMem);
void operator delete[](void* pvMem);
#endif
void* operator new(size_t size, char* pcFile, int iLine);
void* operator new[](size_t size, char* pcFile, int iLine);
void operator delete(void* pvMem, char* pcFile, int iLine);
void operator delete[](void* pvMem, char* pcFile, int iLine);
unsigned int memSize(void* a);
void* reallocMem(void* a, unsigned int uiBytes, const char* pcFile, int iLine);

#define malloc(a) new(a, __FILE__, __LINE__)
#define new new(__FILE__, __LINE__)
#define free(a) delete(a)
#define realloc(a, b) reallocMem(a, b, __FILE__, __LINE__)
#define _msize(a) memSize(a)
#endif
