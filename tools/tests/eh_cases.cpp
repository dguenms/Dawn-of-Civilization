// Original-authored diagnostic for Clang C++23 frames crossing VC7.1 catches.
// Compile for i686-pc-windows-msvc with exceptions and RTTI enabled.
#include <eh.h>

using Record = void (__cdecl *)(const char*, int);
using Callback = void (__cdecl *)(void*);
using LegacyRethrow = void (__cdecl *)(Callback, void*);
using LegacyCatch = int (__cdecl *)(Callback, void*);
using LegacyUncaught = int (__cdecl *)();

extern "C" __declspec(dllimport) __declspec(noreturn) void __stdcall
ExitProcess(unsigned int);

namespace {
struct State {
  int created = 0;
  int copied = 0;
  int destroyed = 0;
  int scopes = 0;
  int uncaught_during_unwind = 0;
  LegacyUncaught uncaught = nullptr;
};

struct Token {
  State* state;
  explicit Token(State& owner) : state(&owner) { ++state->created; }
  Token(const Token& other) : state(other.state) { ++state->copied; }
  ~Token() { ++state->destroyed; }
};

struct Scope {
  State* state;
  explicit Scope(State& owner) : state(&owner) {}
  ~Scope() {
    ++state->scopes;
    if (state->uncaught != nullptr && state->uncaught() != 0) {
      ++state->uncaught_during_unwind;
    }
  }
};

struct Construction {
  Scope member;
  explicit Construction(State& state) : member(state) { throw Token(state); }
};

struct Left { int left = 1; };
struct Base {
  int base = 2;
  virtual ~Base() = default;
};
struct VirtualBase {
  int virtual_base = 3;
  virtual ~VirtualBase() = default;
};
struct Derived : Left, Base, virtual VirtualBase {
  State* state;
  explicit Derived(State& owner) : state(&owner) { ++state->created; }
  Derived(const Derived& other) : VirtualBase(other), Left(other), Base(other),
                                  state(other.state) {
    ++state->copied;
  }
  ~Derived() override { ++state->destroyed; }
};

__declspec(noinline) void throw_token(State& state) { throw Token(state); }

void __cdecl throw_token_callback(void* context) {
  throw_token(*static_cast<State*>(context));
}

struct Roundtrip {
  State* state;
  LegacyRethrow legacy_rethrow;
};

void __cdecl modern_rethrow_callback(void* context) {
  Roundtrip& roundtrip = *static_cast<Roundtrip*>(context);
  try {
    roundtrip.legacy_rethrow(throw_token_callback, roundtrip.state);
  } catch (Token&) {
    throw;
  }
}

__declspec(noinline) void nested_catch(State& state) {
  try {
    throw_token(state);
  } catch (Token&) {
    try {
      throw_token(state);
    } catch (Token&) {
      // The outer catch remains live while this catch finishes.
    }
  }
}

__declspec(noinline) void different_escape(State& state) {
  try {
    try {
      throw_token(state);
    } catch (Token&) {
      throw 37;
    }
  } catch (int value) {
    if (value != 37) {
      throw;
    }
  }
}

__declspec(noinline) void recursive_catches(State& state, int depth) {
  try {
    throw_token(state);
  } catch (Token&) {
    if (depth > 1) {
      recursive_catches(state, depth - 1);
    }
  }
}

bool balanced(const State& state) {
  return state.created + state.copied == state.destroyed;
}

void check(Record record, int& failures, const char* name, bool pass) {
  record(name, pass ? 1 : 0);
  if (!pass) {
    ++failures;
  }
}

Record termination_record = nullptr;

void __cdecl termination_handler() {
  if (termination_record != nullptr) {
    termination_record("terminate_handler", 1);
  }
  ExitProcess(77);
}

struct ThrowOnUnwind {
  State* state;
  explicit ThrowOnUnwind(State& owner) : state(&owner) {}
  ~ThrowOnUnwind() noexcept(false) { throw Token(*state); }
};

__declspec(noinline) void noexcept_plain(State& state) noexcept {
  throw_token(state);
}

__declspec(noinline) void noexcept_new_throw(State& state) noexcept {
  try {
    throw_token(state);
  } catch (Token&) {
    throw Token(state);
  }
}

__declspec(noinline) void noexcept_rethrow(State& state) noexcept {
  try {
    throw_token(state);
  } catch (Token&) {
    throw;
  }
}

__declspec(noinline) void noexcept_destructor(State& state) noexcept {
  ThrowOnUnwind guard(state);
  throw_token(state);
}
}  // namespace

extern "C" __declspec(dllexport) int __cdecl eh_suite(
    Record record, LegacyRethrow legacy_rethrow, LegacyCatch legacy_catch,
    LegacyUncaught legacy_uncaught) {
  if (record == nullptr || legacy_rethrow == nullptr || legacy_catch == nullptr) {
    return 1;
  }
  int failures = 0;

  {
    State state;
    for (int i = 0; i < 512; ++i) {
      nested_catch(state);
    }
    check(record, failures, "nested_catch_512", state.created == 1024 &&
          balanced(state));
  }
  {
    State state;
    for (int i = 0; i < 512; ++i) {
      different_escape(state);
    }
    check(record, failures, "different_escape_512", state.created == 512 &&
          balanced(state));
  }
  {
    State state;
    for (int i = 0; i < 512; ++i) {
      recursive_catches(state, 4);
    }
    check(record, failures, "recursive_depth4_512", state.created == 2048 &&
          balanced(state));
  }
  {
    State state;
    try {
      throw_token(state);
    } catch (Token copy) {
      (void)copy;
    }
    check(record, failures, "catch_by_value_lifetime", state.created == 1 &&
          state.copied >= 1 && balanced(state));
  }
  {
    State state;
    state.uncaught = legacy_uncaught;
    bool caught = false;
    bool clear_in_catch = false;
    try {
      Construction object(state);
      (void)object;
    } catch (Token&) {
      caught = true;
      clear_in_catch = legacy_uncaught == nullptr || legacy_uncaught() == 0;
    }
    check(record, failures, "constructor_unwind", caught && state.scopes == 1 &&
          balanced(state));
    if (legacy_uncaught != nullptr) {
      check(record, failures, "legacy_uncaught_state",
            state.uncaught_during_unwind == 1 && clear_in_catch);
    }
  }
  {
    State state;
    bool caught_base = false;
    bool caught_virtual = false;
    try {
      throw Derived(state);
    } catch (Base& base) {
      caught_base = base.base == 2;
    }
    try {
      throw Derived(state);
    } catch (VirtualBase& base) {
      caught_virtual = base.virtual_base == 3;
    }
    check(record, failures, "multiple_virtual_base_catches",
          caught_base && caught_virtual && state.created == 2 && balanced(state));
  }
  {
    State state;
    int caught = 0;
    for (int i = 0; i < 512; ++i) {
      try {
        legacy_rethrow(throw_token_callback, &state);
      } catch (Token&) {
        ++caught;
      }
    }
    check(record, failures, "legacy_catch_modern_rethrow_512",
          caught == 512 && state.created == 512 && balanced(state));
  }
  {
    State state;
    bool right_clause = false;
    try {
      throw Derived(state);
    } catch (const Token&) {
      right_clause = false;
    } catch (const Left& base) {
      right_clause = base.left == 1;
    } catch (const Base&) {
      right_clause = false;
    } catch (...) {
      right_clause = false;
    }
    check(record, failures, "distinct_typed_catch_clauses", right_clause && balanced(state));
  }
  {
    State state;
    Roundtrip roundtrip{&state, legacy_rethrow};
    int caught = 0;
    for (int i = 0; i < 512; ++i) {
      caught += legacy_catch(modern_rethrow_callback, &roundtrip);
    }
    check(record, failures, "modern_catch_legacy_rethrow_512",
          caught == 512 && state.created == 512 && balanced(state));
  }
  {
    State state;
    const int caught = legacy_catch(throw_token_callback, &state);
    check(record, failures, "legacy_catch_token_once",
          caught == 1 && state.created == 1 && state.copied == 0 &&
          state.destroyed == 1);
  }
  return failures;
}

extern "C" __declspec(dllexport) void __cdecl eh_noexcept(
    unsigned int mode, Record record) {
  termination_record = record;
  set_terminate(termination_handler);
  State state;
  switch (mode) {
    case 0: noexcept_plain(state); break;
    case 1: noexcept_new_throw(state); break;
    case 2: noexcept_rethrow(state); break;
    case 3: noexcept_destructor(state); break;
  }
  if (record != nullptr) {
    record("unexpected_survival", 1);
  }
  ExitProcess(78);
}
