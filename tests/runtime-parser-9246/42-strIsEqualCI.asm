__Z12strIsEqualCIPKcS0_ [0x1005b4299, 0x1005b42c0):
00000001005b4299	testq	%rdi, %rdi
00000001005b429c	setne	%al
00000001005b429f	testq	%rsi, %rsi
00000001005b42a2	setne	%cl
00000001005b42a5	testb	%cl, %al
00000001005b42a7	je	0x1005b42b9
00000001005b42a9	pushq	%rbp
00000001005b42aa	movq	%rsp, %rbp
00000001005b42ad	callq	0x104fe9272                     ## symbol stub for: _strcasecmp
00000001005b42b2	testl	%eax, %eax
00000001005b42b4	sete	%al
00000001005b42b7	popq	%rbp
00000001005b42b8	retq
00000001005b42b9	cmpq	%rsi, %rdi
00000001005b42bc	sete	%al
00000001005b42bf	retq
