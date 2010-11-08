#pragma once


#ifdef USE_MEMMANAGER
#undef new 
#undef malloc
#undef realloc
#undef _msize
#undef free
#endif
