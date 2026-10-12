// Narrow PE32/i386 exception ABI declarations for the pinned Clang toolchain.
// This adapter uses the installed MSVCR71 implementation, not a second CRT.
#pragma once

#if !defined(_WIN32) || !defined(_M_IX86)
#error "The stock exception adapter requires the Windows i386 MSVC ABI"
#endif

namespace bridged::eh {
using Word = unsigned int;

struct ExceptionRecord {
  Word code;
  Word flags;
  ExceptionRecord* nested;
  void* address;
  Word parameter_count;
  Word parameters[15];
};

using SehHandler = int (*)(ExceptionRecord*, void*, void*, void*);
using CatchHandler = void* (*)();

struct CatchBlock {
  Word flags;
  const void* type;
  int object_offset;
  CatchHandler handler;
};

struct TryBlock {
  int start;
  int end;
  int catch_end;
  Word catch_count;
  const CatchBlock* catches;
};

struct CppFrame {
  void* previous;
  SehHandler handler;
  int state;
  Word saved_ebp;
};

// LLVM's i386 FH3 FuncInfo: the first seven words have the VC6 layout.
// See llvm/lib/CodeGen/AsmPrinter/WinException.cpp, emitCXXFrameHandler3Table.
struct LegacyFunctionInfo {
  Word magic;
  int unwind_count;
  const void* unwind_map;
  Word try_count;
  const TryBlock* try_map;
  Word ip_count;
  const void* ip_map;
};

struct FunctionInfo {
  LegacyFunctionInfo legacy;
  const void* expected_exceptions;
  Word flags;
};

// Installed MSVCR71's nested catch registration (RVA 0x19e87): leave its
// security cookie, chain, descriptor, frame and level unchanged. The native
// nested handler validates the cookie and performs all C++ bookkeeping.
struct NativeCatchFrame {
  void* previous;
  SehHandler handler;
  Word cookie;
  const LegacyFunctionInfo* function;
  CppFrame* parent;
  int level;
};

static_assert(sizeof(Word) == 4 && sizeof(void*) == 4);
static_assert(sizeof(ExceptionRecord) == 80);
static_assert(sizeof(LegacyFunctionInfo) == 28);
static_assert(sizeof(FunctionInfo) == 36);
static_assert(sizeof(CatchBlock) == 16 && sizeof(TryBlock) == 20);
static_assert(sizeof(CppFrame) == 16 && sizeof(NativeCatchFrame) == 24);
}  // namespace bridged::eh

// Assembly places the fifth argument in EAX and delegates the unchanged four
// cdecl SEH arguments to MSVCR71's __CxxFrameHandler import.
extern "C" int bridged_eh_legacy(bridged::eh::ExceptionRecord*, void*, void*,
                                  void*, const bridged::eh::LegacyFunctionInfo*);
extern "C" bridged::eh::NativeCatchFrame* bridged_eh_catch_frame();
extern "C" void* bridged_eh_call_catch(bridged::eh::CatchHandler, void*);
extern "C" int bridged_eh_nested(bridged::eh::ExceptionRecord*, void*, void*, void*);

// Preserve the process's stock set_terminate handler on forbidden escape.
[[noreturn]] __declspec(dllimport) void __cdecl terminate();
