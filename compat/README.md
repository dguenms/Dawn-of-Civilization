# Stock exception adapter

Ported from BridgedCvGameCore commit
`8c1830992e0d5b5da615e51d4583417541eafc57`. The three production adapter
files and diagnostic sources are unchanged. DoC retains its own export
baseline, fractional-trade definition, Psapi dependency and gameplay source.
The stock-SDK inventory and game fixtures below describe the upstream
adapter validation; they do not establish DoC gameplay acceptance.

`msvc_eh.cpp`, `msvc_eh_abi.h` and `msvc_eh_x86.s` supply Clang's i386
`__CxxFrameHandler3` inside GameCore. Throwing, matching, object copying,
destruction, rethrow state and termination use the game's installed MSVCR71.
The production DLL needs no `vcruntime140.dll` or additional CRT distribution.
These are original adapter sources; no Wine or sibling shim implementation is
incorporated.

## Contract and implementation

The target is pinned Clang/LLD 23.1.2, PE32/i386 and installed MSVCR71
7.10.3052.4 (SHA256
`8094af5ee310714caebccaeee7769ffb08048503ba478b879edfef5f1a24fefe`).
Changing the compiler or runtime requires renewed metadata and runtime checks.
The source uses strict C++23 apart from bounded MSVC ABI declarations; the
register and SEH-chain interface is confined to the assembly helpers.

Clang emits VC8 `FuncInfo` with magic `0x19930522`, a null expected-exception
list and flags 0 or 1. Its leading seven words and pointed-to i386 maps have
the VC6 layout; see LLVM's pinned
[table emitter](https://github.com/llvm/llvm-project/blob/llvmorg-23.1.2/llvm/lib/CodeGen/AsmPrinter/WinException.cpp).
Installed MSVCR71's exported `__CxxFrameHandler` at RVA
`0x19b77` forwards EAX to a dispatcher that accepts masked VC6 magic
`0x19930520`. Each adapter invocation supplies a stack-local VC6 descriptor,
with copied try/catch maps and distinct callbacks for the original catch
funclets. Original compiler metadata remains read-only.

MSVCR71 retains this descriptor in its 24-byte native catch registration:
previous node, handler, cookie, descriptor, parent C++ frame and catch level.
Its catch helper preserves EBX/ESI/EDI, passes the parent's saved EBP to the
funclet and snapshots/restores the saved ESP per invocation (RVAs `0x19140`
and `0x1927a`). The adapter preserves this contract rather than maintaining
its own exception ownership, TLS or saved stack pointer.

The native nested handler at RVA `0x19bc7` bypasses the exported frame handler
and knows no synchronous-exception flag. While a copied catch callback runs,
the adapter temporarily substitutes the native node's handler field with a
SafeSEH-registered entry. For synchronous C++ functions this entry declines
asynchronous SEH search; it forwards C++ events and every unwind pass to the
saved native handler. A stack-local linked context records the original
handler through nesting. Normal return restores it; native unwind retains
its cleanup and exception-object lifetime duties. The SEH chain's previous
pointer and native cookie are untouched.

Clang's `noexcept` behavior is encoded in terminate cleanup funclets, which
the native unwind map invokes. The adapter does not substitute `ExitProcess`
for the process's MSVCR71 `set_terminate` callback.

There are 64 callback slots per function, bounding both copied try blocks and
the sum of their catch clauses. Unsupported flags, expected-exception lists
or capacities fail closed. `tools/build_dll.py` audits each SDK COFF object's
maps using `tools/eh_metadata.py` before accepting the build. The upstream stock
99-unit SDK has 10,535 descriptors, all flags 1, null expected lists and at
most eight try blocks and eight catch clauses per function. A derived mod
must pass this audit with its own metadata. This is not an arbitrary MSVC
runtime replacement or a VC9/FH4/x64 adapter.

## Reproduction and evidence

Build with the repository's documented `tools/build_dll.py` command. It checks
the stock export set, forbids supplemental CRT imports and requires the
handler, throw and terminate imports from MSVCR71. Only the resulting
`CvGameCoreDLL.dll` is deployed to a test mod.

The independent exception diagnostic uses the VC7.1 compiler solely to build
the original-reference catch/rethrow DLL; production compilation remains
Clang/C++23:

```bash
python3 tools/tests/run_eh.py \
  --bts-dir "$BTS_DIR" \
  --llvm-bin /path/to/llvm-23.1.2/bin \
  --icu70-dir /path/to/icu70 \
  --proton /path/to/Proton/proton --steam-client /path/to/Steam
```

An optional `--native-runtime /path/to/vcruntime140.dll_x86` selects the pinned
former route as a diagnostic comparator. It is not a build input. At O0 and
O2, the static route passes repeated nested and recursive catches, bidirectional
legacy/modern rethrow, multiple typed clauses, catch-by-value and polymorphic
matching, construction failure, original uncaught-exception queries, balanced
stack and object lifetimes, asynchronous SEH escape/resume, and four terminate
callback cases. Loaded paths, export RVAs and relocated code are authenticated.
The native comparator has a recorded MSVCR71 uncaught-state mismatch because
its modern throws use a different CRT; the runner reports that difference
explicitly.

The Windows LLVM/CMake build also compiles all 99 SDK units and both adapter
units under Wine with the same export, provider and metadata checks. Its DLL
has a different hash from the Linux-hosted build and has not been exercised
in the game. Runtime acceptance below concerns the Linux-hosted DLL.

Upstream stock GameCore original and converted game runs load the same turn-ten seed,
advance two turns, save, reload and close normally. Six state/help snapshots,
three four-phase checksum comparisons and all 56 ordered gameplay events
agree. A fresh converted process reload also agrees with stock. All fourteen
heap checkpoints pass. Source-backed comparison accounts for every endpoint
save difference as turn/movement slices or existing object padding; all other
decoded bytes and both RNG seeds agree. Process maps confirm no vcruntime
provider, although Proton's usual system CRT dependencies remain present in
both original and converted processes.

The upstream reports live under its ignored `tmp/eh-validation/`,
`tmp/eh-dll-build/`, `tmp/eh-analysis/` and `tmp/eh-game/`. DoC build reports
remain in its selected build output directories. Selected probes and named stock-game
fixtures establish their exercised paths. Arbitrary SE translators, custom
exception handlers, concurrent exceptional execution, PE32 sanitizer coverage
and multiplayer remain unvalidated.
