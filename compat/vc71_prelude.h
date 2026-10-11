#pragma once

// The pinned ObjBase.h uses IUnknown in a template before its declaration.
struct IUnknown;

// VC7.1 xlocale needs this declaration before modern two-phase lookup.
namespace std { template<class Character> class collate; }
#include <stddef.h>
#undef offsetof
#define offsetof(Type, Member) __builtin_offsetof(Type, Member)

// Python 2.4 still spells register in declarations. Keep the diagnostic
// accommodation at the external-header boundary, rather than all SDK code.
#pragma clang diagnostic push
#pragma clang diagnostic ignored "-Wregister"
#include <Python.h>
#pragma clang diagnostic pop

// VC7.1's x86 stdarg macros derive the argument list from &last. Clang may
// inline such a function and relocate last into unrelated local storage.
// Use compiler varargs operations while retaining the pinned CRT's char*
// va_list. S4's direct-call O2 probe reproduces the legacy macro failure and
// checks mixed arguments against the original MSVCR71 _vsnprintf provider.
#include <stdarg.h>
static_assert(sizeof(va_list) == 4);
#undef va_start
#undef va_arg
#undef va_end
#define va_start(Arguments, Last) __builtin_va_start(Arguments, Last)
#define va_arg(Arguments, Type) __builtin_va_arg(Arguments, Type)
#define va_end(Arguments) __builtin_va_end(Arguments)
