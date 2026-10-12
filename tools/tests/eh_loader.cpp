#include "eh_win32.h"
#include "eh_inputs.h"

using Suite = int (*)(Record, LegacyRethrow, LegacyCatch, LegacyUncaught);
struct Audit { Word before; Word after; int result; };
extern "C" void eh_audit_suite(Suite, Record, LegacyRethrow, LegacyCatch, LegacyUncaught, Audit*);

namespace {
char buffer[8192];
Word used;
Handle trace;
void text(const char* value) { while (*value) buffer[used++] = *value++; }
void number(Word value) {
  char digits[10];
  Word count = 0;
  do { digits[count++] = static_cast<char>('0' + value % 10); value /= 10; } while (value);
  while (count) buffer[used++] = digits[--count];
}
void bytes(const void* storage, Word count) {
  const auto* input = static_cast<const unsigned char*>(storage);
  text("\"");
  for (Word i = 0; i < count; ++i) {
    buffer[used++] = "0123456789abcdef"[input[i] >> 4];
    buffer[used++] = "0123456789abcdef"[input[i] & 15];
  }
  text("\"");
}
void flush() {
  text("}\n");
  Word written = 0;
  if (!WriteFile(trace, buffer, used, &written, nullptr) || written != used) ExitProcess(90);
  used = 0;
}
void record(const char* name, int value) {
  text("{\"name\":\""); text(name); text("\",\"value\":");
  number(static_cast<Word>(value)); flush();
}
template <typename Function>
Function symbol(Handle module, const char* name) {
  auto* result = GetProcAddress(module, name);
  if (!result) { record("missing_symbol", 1); ExitProcess(91); }
  return reinterpret_cast<Function>(result);
}
Handle load(const char* path) {
  Handle module = LoadLibraryExA(path, nullptr, 8);
  if (!module) { record("missing_module", 1); ExitProcess(92); }
  return module;
}
void provider(Handle module, const char* name, const char* entry) {
  char path[2048];
  Word length = GetModuleFileNameA(module, path, sizeof(path));
  if (!length || length >= sizeof(path)) ExitProcess(93);
  auto* address = symbol<const unsigned char*>(module, entry);
  text("{\"provider\":\""); text(name); text("\",\"base\":"); number(reinterpret_cast<Word>(module));
  text(",\"rva\":"); number(reinterpret_cast<Word>(address) - reinterpret_cast<Word>(module));
  text(",\"path_hex\":"); bytes(path, length);
  text(",\"code_hex\":"); bytes(address, 32); flush();
}
}  // namespace

extern "C" void __stdcall entry() {
  char path[2048];
  Word length = GetEnvironmentVariableA("BRIDGED_EH_TRACE", path, sizeof(path));
  if (!length || length >= sizeof(path)) ExitProcess(89);
  trace = CreateFileA(path, 0x40000000u, 0, nullptr, 2, 0x80, nullptr);
  if (trace == reinterpret_cast<Handle>(0xffffffffu)) ExitProcess(88);
  Handle crt = load(crt_path);
  symbol<int (*)(int)>(crt, "_set_error_mode")(1);
  provider(crt, "msvcr71.dll", "__CxxFrameHandler");
  Handle native = nullptr;
  if (native_path[0]) {
    native = load(native_path);
    provider(native, "vcruntime140.dll", "__CxxFrameHandler3");
  }
  Handle legacy = load(legacy_path);
  provider(legacy, "LegacyEH.dll", "legacy_rethrow");
  Handle modern = load(modern_path);
  provider(modern, "ModernEH.dll", "eh_suite");
  if (!native) provider(modern, "static_handler", "__CxxFrameHandler3");
  char mode[32]{};
  GetEnvironmentVariableA("BRIDGED_EH_CASE", mode, sizeof(mode));
  if (mode[0] >= '0' && mode[0] <= '3') {
    symbol<void (*)(Word, Record)>(modern, "eh_noexcept")(mode[0] - '0', record);
    ExitProcess(94);
  }
  Audit audit{};
  eh_audit_suite(symbol<Suite>(modern, "eh_suite"), record,
      symbol<LegacyRethrow>(legacy, "legacy_rethrow"),
      symbol<LegacyCatch>(legacy, "legacy_catch"),
      symbol<LegacyUncaught>(legacy, "legacy_uncaught"), &audit);
  record("stack_balanced", audit.before == audit.after);
  if (audit.before != audit.after) ExitProcess(99);
  if (symbol<int (*)(Record)>(modern, "eh_async")(record)) ExitProcess(96);
  if (symbol<int (*)(Record)>(modern, "eh_async_resume")(record)) ExitProcess(97);
  if (!FreeLibrary(modern) || !FreeLibrary(legacy) || (native && !FreeLibrary(native)) || !FreeLibrary(crt)) ExitProcess(98);
  record("complete", 1);
  ExitProcess(audit.result ? 95 : 0);
}
