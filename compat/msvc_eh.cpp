#include "msvc_eh_abi.h"

namespace {
constexpr bridged::eh::Word magic_mask = 0x1fffffffu;
constexpr bridged::eh::Word vc6_magic = 0x19930520u;
constexpr bridged::eh::Word vc8_magic = 0x19930522u;
constexpr bridged::eh::Word cpp_exception = 0xe06d7363u;
constexpr bridged::eh::Word unwind_flags = 0x2u | 0x4u;
constexpr bridged::eh::Word synchronous = 0x1u;
constexpr int continue_search = 1;
// Stock Clang-generated functions use far fewer clauses. Bound stack usage
// and supply a distinct callback identity for every copied catch clause.
constexpr unsigned int catch_slots = 64;

struct CatchContext {
  CatchContext* previous;
  bridged::eh::NativeCatchFrame* frame;
  bridged::eh::SehHandler native_handler;
};

struct Facade {
  bridged::eh::LegacyFunctionInfo legacy;
  const bridged::eh::FunctionInfo* original;
  void* parent;
  CatchContext* active;
  bridged::eh::TryBlock tries[catch_slots];
  bridged::eh::CatchBlock catches[catch_slots];
  bridged::eh::CatchHandler handlers[catch_slots];
};

void unlink(Facade& facade, CatchContext& context) {
  auto** link = &facade.active;
  while (*link != &context) {
    if (*link == nullptr) terminate();
    link = &(*link)->previous;
  }
  *link = context.previous;
}

extern "C" int bridged_eh_nested_dispatch(bridged::eh::ExceptionRecord* exception,
                                          void* registration, void* context,
                                          void* dispatcher) {
  auto* frame = static_cast<bridged::eh::NativeCatchFrame*>(registration);
  auto& facade = *reinterpret_cast<Facade*>(
      const_cast<bridged::eh::LegacyFunctionInfo*>(frame->function));
  if (frame->parent != facade.parent || frame->function != &facade.legacy) terminate();
  auto* active = facade.active;
  while (active != nullptr && active->frame != frame) active = active->previous;
  if (active == nullptr) terminate();

  const bool unwinding = (exception->flags & unwind_flags) != 0;
  // The native nested node bypasses exported Handler3 and knows no EHs flag.
  // Filter search only. All unwind passes still reach its original handler
  // so native current-exception state and caught-object destruction balance.
  if (!unwinding && (facade.original->flags & synchronous) != 0 &&
      exception->code != cpp_exception) {
    return continue_search;
  }
  const int result = active->native_handler(exception, registration, context, dispatcher);
  if (unwinding) unlink(facade, *active);
  return result;
}

template <unsigned int Slot>
void* catch_body() {
  auto* frame = bridged_eh_catch_frame();
  auto& facade = *reinterpret_cast<Facade*>(
      const_cast<bridged::eh::LegacyFunctionInfo*>(frame->function));
  if (frame->parent != facade.parent || frame->function != &facade.legacy ||
      frame->handler == nullptr || facade.legacy.try_map != facade.tries) {
    terminate();
  }
  CatchContext context{facade.active, frame, frame->handler};
  facade.active = &context;
  frame->handler = &bridged_eh_nested;
  // Native invokes a catch with EBP=&parent->saved_ebp and preserves EBX/ESI/
  // EDI. A normal C++ callback cannot carry that implicit register contract.
  void* continuation = bridged_eh_call_catch(facade.handlers[Slot], &frame->parent->saved_ebp);
  frame->handler = context.native_handler;
  unlink(facade, context);
  return continuation;
}

template <unsigned int... Slots>
struct CatchBodies {
  static constexpr bridged::eh::CatchHandler entries[] = {&catch_body<Slots>...};
};
template <unsigned int Count, unsigned int... Slots>
struct MakeCatchBodies : MakeCatchBodies<Count - 1, Count - 1, Slots...> {};
template <unsigned int... Slots>
struct MakeCatchBodies<0, Slots...> : CatchBodies<Slots...> {};

void prepare(Facade& facade, const bridged::eh::FunctionInfo& original, void* parent) {
  facade.legacy = original.legacy;
  facade.legacy.magic = (facade.legacy.magic & ~magic_mask) | vc6_magic;
  facade.original = &original;
  facade.parent = parent;
  facade.active = nullptr;
  if (original.legacy.try_count > catch_slots) terminate();
  unsigned int slot = 0;
  for (unsigned int i = 0; i < original.legacy.try_count; ++i) {
    facade.tries[i] = original.legacy.try_map[i];
    auto& block = facade.tries[i];
    if (block.catch_count > catch_slots - slot) terminate();
    block.catches = &facade.catches[slot];
    for (unsigned int j = 0; j < block.catch_count; ++j, ++slot) {
      facade.catches[slot] = original.legacy.try_map[i].catches[j];
      facade.handlers[slot] = facade.catches[slot].handler;
      facade.catches[slot].handler = MakeCatchBodies<catch_slots>::entries[slot];
    }
  }
  facade.legacy.try_map = facade.tries;
}
}  // namespace

extern "C" int bridged_eh_dispatch(bridged::eh::ExceptionRecord* exception,
                                    void* frame, void* context, void* dispatcher,
                                    const bridged::eh::FunctionInfo* function) {
  // Installed MSVCR71 __CxxFrameHandler (RVA 0x19b77) passes EAX to its
  // internal dispatcher, which accepts masked VC6 magic only. Clang 23.1.2
  // emits VC8 magic even with -fms-compatibility-version=13.10. The seven
  // leading fields and pointed-to i386 maps match; do not modify read-only
  // compiler metadata or discard flags before handling their obligations.
  if ((function->legacy.magic & magic_mask) != vc8_magic ||
      function->expected_exceptions != nullptr ||
      (function->flags & ~synchronous) != 0) {
    terminate();
  }

  // FH3 /EHs frames exclude asynchronous SEH events, including their unwind
  // pass. The legacy handler has no descriptor flag for this distinction.
  if ((function->flags & synchronous) != 0 && exception->code != cpp_exception) {
    return continue_search;
  }

  // A separate facade for every invocation stays live throughout the native
  // catch call. MSVCR71 retains this pointer in its nested catch registration;
  // a global, TLS singleton or prematurely returned facade is invalid.
  // Native catch dispatch snapshots/restores frame[-1] per invocation (RVA
  // 0x19140/0x1927a), including Clang catches that overwrite the saved ESP.
  // Keep throw, current-exception and exception-object ownership in MSVCR71.
  Facade facade;
  prepare(facade, *function, frame);
  // Clang represents noexcept with terminate cleanup funclets in these maps,
  // rather than bit 4 of MSVC's EHFlags. Native unwind invokes those actions,
  // including escapes from catch bodies, using the stock terminate handler.
  return bridged_eh_legacy(exception, frame, context, dispatcher, &facade.legacy);
}
