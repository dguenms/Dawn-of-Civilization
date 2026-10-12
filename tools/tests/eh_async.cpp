// PE32 probe: an asynchronous SEH event inside an active C++ catch must reach
// the outer SEH consumer under /EHs, rather than a nested C++ catch(...).
using Record = void (*)(const char*, int);
extern "C" __declspec(dllimport) void __stdcall RaiseException(
    unsigned long, unsigned long, unsigned long, const unsigned long*);

namespace {
struct Token {
  Record record;
  ~Token() { record("asynchronous_token_destroy", 1); }
};

__declspec(noinline) void raise_inside_catch(Record record) {
  try {
    throw Token{record};
  } catch (Token&) {
    try {
      RaiseException(0xe0424242ul, 0, 0, nullptr);
    } catch (...) {
      record("asynchronous_cpp_caught", 1);
    }
  }
}

__declspec(noinline) void resume_inside_catch(Record record) {
  try {
    throw Token{record};
  } catch (const Token& token) {
    try {
      RaiseException(0xe0424242ul, 0, 0, nullptr);
      record("asynchronous_resumed", 1);
      throw 17;
    } catch (int value) {
      record("asynchronous_later_cpp", value == 17);
    } catch (...) {
      record("asynchronous_cpp_caught", 1);
    }
    record("asynchronous_outer_preserved", token.record == record);
  }
}
}  // namespace

extern "C" __declspec(dllexport) int eh_async(Record record) {
  __try {
    raise_inside_catch(record);
  } __except (1) {
    record("asynchronous_outer_seh", 1);
    return 0;
  }
  record("asynchronous_wrong_survival", 1);
  return 1;
}

extern "C" __declspec(dllexport) int eh_async_resume(Record record) {
  __try {
    resume_inside_catch(record);
  } __except ((record("asynchronous_continue_filter", 1), -1)) {
    record("asynchronous_wrong_except_body", 1);
    return 1;
  }
  return 0;
}
