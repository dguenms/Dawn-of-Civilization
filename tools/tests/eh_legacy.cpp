// Compile with the original VC7.1 compiler, /MD and /EHsc. No exception
// representation is shared through these C entry points.
#include <eh.h>

typedef void (__cdecl *LegacyCallback)(void*);

extern "C" __declspec(dllexport) void __cdecl legacy_rethrow(
    LegacyCallback callback, void* context) {
  try {
    callback(context);
  } catch (...) {
    throw;
  }
}

extern "C" __declspec(dllexport) int __cdecl legacy_catch(
    LegacyCallback callback, void* context) {
  try {
    callback(context);
  } catch (...) {
    return 1;
  }
  return 0;
}

extern "C" __declspec(dllexport) int __cdecl legacy_uncaught() {
  return __uncaught_exception() ? 1 : 0;
}
