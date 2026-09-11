__ZN15ACTION_constant7onQueryER12SActionParam [0x100990c2a, 0x100990c60):
0000000100990c2a	pushq	%rbp
0000000100990c2b	movq	%rsp, %rbp
0000000100990c2e	pushq	%r14
0000000100990c30	pushq	%rbx
0000000100990c31	movq	%rsi, %rbx
0000000100990c34	xorl	%esi, %esi
0000000100990c36	callq	__ZN7IAction8getParamEi         ## IAction::getParam(int)
0000000100990c3b	movq	%rax, %r14
0000000100990c3e	movq	CONFIG_EMULATE_HARDWARE(%rax), %rax
0000000100990c41	movq	%rax, CONFIG_EMULATE_HARDWARE(%rbx)
0000000100990c44	leaq	0x8(%rbx), %rdi
0000000100990c48	leaq	0x8(%r14), %rsi
0000000100990c4c	callq	0x104fe856a                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
0000000100990c51	movb	0x20(%r14), %al
0000000100990c55	movb	%al, 0x20(%rbx)
0000000100990c58	xorl	%eax, %eax
0000000100990c5a	popq	%rbx
0000000100990c5b	popq	%r14
0000000100990c5d	popq	%rbp
0000000100990c5e	retq
0000000100990c5f	nop
