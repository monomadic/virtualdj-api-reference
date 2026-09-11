__ZN7IAction8getParamEi [0x100596c26, 0x100596cb2):
0000000100596c26	pushq	%rbp
0000000100596c27	movq	%rsp, %rbp
0000000100596c2a	movq	0x20(%rdi), %rax
0000000100596c2e	movq	0x28(%rdi), %rcx
0000000100596c32	subq	%rax, %rcx
0000000100596c35	shrq	$0x3, %rcx
0000000100596c39	imull	$0xcccccccd, %ecx, %edx         ## imm = 0xCCCCCCCD
0000000100596c3f	movl	0x58(%rdi), %ecx
0000000100596c42	testl	$0x30000, %ecx                  ## imm = 0x30000
0000000100596c48	setne	%r8b
0000000100596c4c	testl	%edx, %edx
0000000100596c4e	setne	%r9b
0000000100596c52	andb	%r8b, %r9b
0000000100596c55	movzbl	%r9b, %r8d
0000000100596c59	subl	%r8d, %edx
0000000100596c5c	cmpl	%esi, %edx
0000000100596c5e	jle	0x100596c6d
0000000100596c60	movslq	%esi, %rcx
0000000100596c63	leaq	CONFIG_EMULATE_HARDWARE(%rcx,%rcx,4), %rcx
0000000100596c67	leaq	CONFIG_EMULATE_HARDWARE(%rax,%rcx,8), %rax
0000000100596c6b	jmp	0x100596cb0
0000000100596c6d	movq	0x68(%rdi), %rax
0000000100596c71	testq	%rax, %rax
0000000100596c74	sete	%dil
0000000100596c78	movl	%ecx, %r8d
0000000100596c7b	shrl	$0xc, %r8d
0000000100596c7f	andl	$0x1, %r8d
0000000100596c83	orb	%dil, %r8b
0000000100596c86	jne	0x100596ca9
0000000100596c88	cmpl	%esi, %edx
0000000100596c8a	je	0x100596cb0
0000000100596c8c	incl	%edx
0000000100596c8e	addq	$0x28, %rax
0000000100596c92	cmpl	%esi, %edx
0000000100596c94	leaq	_staticNullParam(%rip), %rdx
0000000100596c9b	cmovneq	%rdx, %rax
0000000100596c9f	btl	$0xd, %ecx
0000000100596ca3	cmovaeq	%rdx, %rax
0000000100596ca7	jmp	0x100596cb0
0000000100596ca9	leaq	_staticNullParam(%rip), %rax
0000000100596cb0	popq	%rbp
0000000100596cb1	retq
