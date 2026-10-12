#pragma once
using Word = unsigned int;
using Handle = void*;
using Record = void (*)(const char*, int);
using Callback = void (*)(void*);
using LegacyRethrow = void (*)(Callback, void*);
using LegacyCatch = int (*)(Callback, void*);
using LegacyUncaught = int (*)();

extern "C" {
__declspec(dllimport) Handle __stdcall LoadLibraryExA(const char*, Handle, Word);
__declspec(dllimport) int __stdcall FreeLibrary(Handle);
__declspec(dllimport) void* __stdcall GetProcAddress(Handle, const char*);
__declspec(dllimport) Word __stdcall GetEnvironmentVariableA(const char*, char*, Word);
__declspec(dllimport) Word __stdcall GetModuleFileNameA(Handle, char*, Word);
__declspec(dllimport) Handle __stdcall GetStdHandle(Word);
__declspec(dllimport) Handle __stdcall CreateFileA(const char*, Word, Word, void*, Word, Word, Handle);
__declspec(dllimport) int __stdcall WriteFile(Handle, const void*, Word, Word*, void*);
[[noreturn]] __declspec(dllimport) void __stdcall ExitProcess(Word);
}
