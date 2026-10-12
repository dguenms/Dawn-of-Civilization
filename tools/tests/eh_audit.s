// Observe the actual cdecl suite call's stack, retaining a recovery pointer.
.text
.def @feat.00; .scl 3; .type 0; .endef
.set @feat.00, 1
.globl _eh_audit_suite
_eh_audit_suite:
  pushl %ebp
  movl %esp, %ebp
  pushl %ebx
  pushl %esi
  pushl %edi
  movl %esp, %ebx
  movl 28(%ebp), %edi
  movl %ebx, 0(%edi)
  pushl 24(%ebp)
  pushl 20(%ebp)
  pushl 16(%ebp)
  pushl 12(%ebp)
  calll *8(%ebp)
  addl $16, %esp
  movl %esp, 4(%edi)
  movl %eax, 8(%edi)
  movl %ebx, %esp
  popl %edi
  popl %esi
  popl %ebx
  popl %ebp
  retl
