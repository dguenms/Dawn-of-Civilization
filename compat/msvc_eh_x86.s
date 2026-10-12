// Original-authored glue for LLVM's i386 MSVC SEH convention. No native
// runtime instruction bytes or Wine implementation are reproduced here.
.text
.def @feat.00; .scl 3; .type 0; .endef
.set @feat.00, 1

// Register the authored nested SEH entry for Windows SafeSEH validation.
.globl _bridged_eh_nested
.def _bridged_eh_nested; .scl 2; .type 32; .endef
_bridged_eh_nested:
  jmp _bridged_eh_nested_dispatch
.safeseh _bridged_eh_nested

// The compiler's per-function thunk supplies FuncInfo in EAX. Marshal it as
// argument five while preserving the four cdecl SEH arguments and caller EBP.
.globl ___CxxFrameHandler3
___CxxFrameHandler3:
  pushl %eax
  pushl 20(%esp)
  pushl 20(%esp)
  pushl 20(%esp)
  pushl 20(%esp)
  calll _bridged_eh_dispatch
  addl $20, %esp
  retl

// Keep the dispatcher's stack-local facade live until the original handler
// finishes its catch or search. The C++ caller calls this bridge normally;
// only this ABI glue tail-jumps, with the fifth argument also placed in EAX.
.globl _bridged_eh_legacy
_bridged_eh_legacy:
  movl 20(%esp), %eax
  jmpl *__imp____CxxFrameHandler

// Each copied catch clause has a distinct ordinary C++ callback. The native
// handler has already installed this catch's registration at FS:0.
.globl _bridged_eh_catch_frame
_bridged_eh_catch_frame:
  movl %fs:0, %eax
  retl

// Invoke the original compiler funclet with its parent frame in EBP. Match
// the native call helper's preservation of all x86 nonvolatile registers.
.globl _bridged_eh_call_catch
_bridged_eh_call_catch:
  pushl %ebp
  pushl %ebx
  pushl %esi
  pushl %edi
  movl 24(%esp), %ebp
  calll *20(%esp)
  popl %edi
  popl %esi
  popl %ebx
  popl %ebp
  retl
