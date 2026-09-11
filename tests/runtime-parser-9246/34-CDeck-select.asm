__ZN5CDeck6selectEb [0x100481bb8, 0x100481cb8):
0000000100481bb8	pushq	%rbp
0000000100481bb9	movq	%rsp, %rbp
0000000100481bbc	pushq	%rbx
0000000100481bbd	pushq	%rax
0000000100481bbe	testq	%rdi, %rdi
0000000100481bc1	je	0x100481c3c
0000000100481bc3	movq	%rdi, %rbx
0000000100481bc6	movq	_defaultDeck(%rip), %rax
0000000100481bcd	movl	0x240(%rax), %eax
0000000100481bd3	movq	%rdi, _defaultDeck(%rip)
0000000100481bda	leaq	_Config(%rip), %rcx
0000000100481be1	orb	0x1d30(%rcx), %sil
0000000100481be8	cmpb	$0x1, %sil
0000000100481bec	jne	0x100481c3c
0000000100481bee	movq	_nbDecks(%rip), %rdx
0000000100481bf5	movl	$0xffffffff, %ecx               ## imm = 0xFFFFFFFF
0000000100481bfa	testq	%rdx, %rdx
0000000100481bfd	je	0x100481c34
0000000100481bff	leaq	__ZN5CDeck5decksE(%rip), %rsi   ## CDeck::decks
0000000100481c06	xorl	%edi, %edi
0000000100481c08	xorps	%xmm0, %xmm0
0000000100481c0b	movq	CONFIG_EMULATE_HARDWARE(%rsi), %r8
0000000100481c0e	movss	0x2a0(%r8), %xmm1
0000000100481c17	ucomiss	%xmm0, %xmm1
0000000100481c1a	jne	0x100481c1e
0000000100481c1c	jnp	0x100481c24
0000000100481c1e	testl	%ecx, %ecx
0000000100481c20	jns	0x100481c32
0000000100481c22	movl	%edi, %ecx
0000000100481c24	incq	%rdi
0000000100481c27	addq	$0x8, %rsi
0000000100481c2b	cmpq	%rdi, %rdx
0000000100481c2e	jne	0x100481c0b
0000000100481c30	jmp	0x100481c34
0000000100481c32	movl	%edx, %ecx
0000000100481c34	movslq	%ecx, %rsi
0000000100481c37	cmpq	%rsi, %rdx
0000000100481c3a	jne	0x100481c43
0000000100481c3c	addq	$0x8, %rsp
0000000100481c40	popq	%rbx
0000000100481c41	popq	%rbp
0000000100481c42	retq
0000000100481c43	cmpq	$0x3, %rdx
0000000100481c47	jb	0x100481c60
0000000100481c49	cmpl	%ecx, %eax
0000000100481c4b	je	0x100481c60
0000000100481c4d	cmpl	$0x1, %eax
0000000100481c50	jg	0x100481c3c
0000000100481c52	cmpl	$0x1, %ecx
0000000100481c55	jg	0x100481c3c
0000000100481c57	cmpl	$0x1, 0x240(%rbx)
0000000100481c5e	jg	0x100481c3c
0000000100481c60	leaq	_mixerEngine(%rip), %rax
0000000100481c67	movl	$0xbf800000, 0x6c(%rax)         ## imm = 0xBF800000
0000000100481c6e	testl	%ecx, %ecx
0000000100481c70	js	0x100481c98
0000000100481c72	leaq	__ZN5CDeck5decksE(%rip), %rax   ## CDeck::decks
0000000100481c79	movq	CONFIG_EMULATE_HARDWARE(%rax,%rsi,8), %rsi
0000000100481c7d	cmpq	%rbx, %rsi
0000000100481c80	je	0x100481c98
0000000100481c82	movl	$CONFIG_EMULATE_HARDWARE, 0x2a0(%rsi)
0000000100481c8c	leaq	_mixerEngine(%rip), %rdi
0000000100481c93	callq	__ZN12CMixerEngine11setPflLevelEP5CDeck ## CMixerEngine::setPflLevel(CDeck*)
0000000100481c98	movl	$0x3f800000, 0x2a0(%rbx)        ## imm = 0x3F800000
0000000100481ca2	leaq	_mixerEngine(%rip), %rdi
0000000100481ca9	movq	%rbx, %rsi
0000000100481cac	addq	$0x8, %rsp
0000000100481cb0	popq	%rbx
0000000100481cb1	popq	%rbp
0000000100481cb2	jmp	__ZN12CMixerEngine11setPflLevelEP5CDeck ## CMixerEngine::setPflLevel(CDeck*)
0000000100481cb7	nop
