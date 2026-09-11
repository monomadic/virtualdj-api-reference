__Z8isLeftCINSt3__117basic_string_viewIcNS_11char_traitsIcEEEEPKc [0x1005b3dbf, 0x1005b3e0d):
00000001005b3dbf	testq	%rdx, %rdx
00000001005b3dc2	je	0x1005b3dfd
00000001005b3dc4	pushq	%rbp
00000001005b3dc5	movq	%rsp, %rbp
00000001005b3dc8	pushq	%r15
00000001005b3dca	pushq	%r14
00000001005b3dcc	pushq	%rbx
00000001005b3dcd	pushq	%rax
00000001005b3dce	movq	%rdx, %rbx
00000001005b3dd1	movq	%rsi, %r15
00000001005b3dd4	movq	%rdi, %r14
00000001005b3dd7	movq	%rdx, %rdi
00000001005b3dda	callq	0x104fe92ae                     ## symbol stub for: _strlen
00000001005b3ddf	leaq	-0x1(%rax), %rcx
00000001005b3de3	cmpq	%r15, %rcx
00000001005b3de6	jae	0x1005b3e00
00000001005b3de8	movq	%r14, %rdi
00000001005b3deb	movq	%rbx, %rsi
00000001005b3dee	movq	%rax, %rdx
00000001005b3df1	callq	0x104fe92b4                     ## symbol stub for: _strncasecmp
00000001005b3df6	testl	%eax, %eax
00000001005b3df8	sete	%al
00000001005b3dfb	jmp	0x1005b3e02
00000001005b3dfd	xorl	%eax, %eax
00000001005b3dff	retq
00000001005b3e00	xorl	%eax, %eax
00000001005b3e02	addq	$0x8, %rsp
00000001005b3e06	popq	%rbx
00000001005b3e07	popq	%r14
00000001005b3e09	popq	%r15
00000001005b3e0b	popq	%rbp
00000001005b3e0c	retq
