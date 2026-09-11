__Z8isLeftCIPKcS0_ [0x1005b3e0d, 0x1005b3e4d):
00000001005b3e0d	testq	%rsi, %rsi
00000001005b3e10	sete	%al
00000001005b3e13	testq	%rdi, %rdi
00000001005b3e16	sete	%cl
00000001005b3e19	orb	%al, %cl
00000001005b3e1b	jne	0x1005b3e4a
00000001005b3e1d	pushq	%rbp
00000001005b3e1e	movq	%rsp, %rbp
00000001005b3e21	pushq	%r14
00000001005b3e23	pushq	%rbx
00000001005b3e24	movq	%rsi, %rbx
00000001005b3e27	movq	%rdi, %r14
00000001005b3e2a	movq	%rsi, %rdi
00000001005b3e2d	callq	0x104fe92ae                     ## symbol stub for: _strlen
00000001005b3e32	movq	%r14, %rdi
00000001005b3e35	movq	%rbx, %rsi
00000001005b3e38	movq	%rax, %rdx
00000001005b3e3b	callq	0x104fe92b4                     ## symbol stub for: _strncasecmp
00000001005b3e40	testl	%eax, %eax
00000001005b3e42	sete	%al
00000001005b3e45	popq	%rbx
00000001005b3e46	popq	%r14
00000001005b3e48	popq	%rbp
00000001005b3e49	retq
00000001005b3e4a	xorl	%eax, %eax
00000001005b3e4c	retq
