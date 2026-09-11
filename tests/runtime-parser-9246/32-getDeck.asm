__Z7getDecki [0x10047d9ff, 0x10047dd08):
000000010047d9ff	pushq	%rbp
000000010047da00	movq	%rsp, %rbp
000000010047da03	pushq	%rbx
000000010047da04	pushq	%rax
000000010047da05	testl	%edi, %edi
000000010047da07	je	0x10047dab0
000000010047da0d	movq	_nbDecks(%rip), %rbx
000000010047da14	testl	%edi, %edi
000000010047da16	setle	%al
000000010047da19	cmpl	%ebx, %edi
000000010047da1b	setg	%cl
000000010047da1e	orb	%al, %cl
000000010047da20	je	0x10047dabe
000000010047da26	cmpl	$0x6c656673, %edi               ## imm = 0x6C656673
000000010047da2c	jg	0x10047da4b
000000010047da2e	cmpl	$0x6175746e, %edi               ## imm = 0x6175746E
000000010047da34	jg	0x10047da6c
000000010047da36	cmpl	$0x646566, %edi                 ## imm = 0x646566
000000010047da3c	je	0x10047dab0
000000010047da3e	cmpl	$0x61637469, %edi               ## imm = 0x61637469
000000010047da44	jne	0x10047da92
000000010047da46	jmp	0x10047db02
000000010047da4b	cmpl	$0x72696767, %edi               ## imm = 0x72696767
000000010047da51	jg	0x10047da7e
000000010047da53	cmpl	$0x6c656674, %edi               ## imm = 0x6C656674
000000010047da59	je	0x10047db0d
000000010047da5f	cmpl	$0x6d617374, %edi               ## imm = 0x6D617374
000000010047da65	jne	0x10047da92
000000010047da67	jmp	0x10047daf6
000000010047da6c	cmpl	$0x6175746f, %edi               ## imm = 0x6175746F
000000010047da72	je	0x10047dadf
000000010047da74	cmpl	$0x6b617261, %edi               ## imm = 0x6B617261
000000010047da7a	jne	0x10047da92
000000010047da7c	jmp	0x10047dad6
000000010047da7e	cmpl	$0x72696768, %edi               ## imm = 0x72696768
000000010047da84	je	0x10047dacd
000000010047da86	cmpl	$0x73616e64, %edi               ## imm = 0x73616E64
000000010047da8c	je	0x10047db16
000000010047da92	leal	-0x6d697831(%rdi), %eax
000000010047da98	cmpl	$0x3, %eax
000000010047da9b	ja	0x10047db2c
000000010047daa1	callq	__Z17getMixerOrderDeckj         ## getMixerOrderDeck(unsigned int)
000000010047daa6	movl	%eax, %edi
000000010047daa8	testl	%eax, %eax
000000010047daaa	jne	0x10047da14
000000010047dab0	movq	_defaultDeck(%rip), %rax
000000010047dab7	addq	$0x8, %rsp
000000010047dabb	popq	%rbx
000000010047dabc	popq	%rbp
000000010047dabd	retq
000000010047dabe	decl	%edi
000000010047dac0	leaq	__ZN5CDeck5decksE(%rip), %rax   ## CDeck::decks
000000010047dac7	movq	CONFIG_EMULATE_HARDWARE(%rax,%rdi,8), %rax
000000010047dacb	jmp	0x10047dab7
000000010047dacd	movq	_rightDeck(%rip), %rax
000000010047dad4	jmp	0x10047dab7
000000010047dad6	leaq	_karaokeEngine(%rip), %rax
000000010047dadd	jmp	0x10047db1d
000000010047dadf	leaq	_autoMix(%rip), %rax
000000010047dae6	cmpb	$0x0, 0x8(%rax)
000000010047daea	je	0x10047dcf0
000000010047daf0	movq	0x20(%rax), %rax
000000010047daf4	jmp	0x10047dab7
000000010047daf6	movq	_masterDeck(%rip), %rax
000000010047dafd	testq	%rax, %rax
000000010047db00	jne	0x10047dab7
000000010047db02	addq	$0x8, %rsp
000000010047db06	popq	%rbx
000000010047db07	popq	%rbp
000000010047db08	jmp	__ZN5CDeck13getActiveDeckEv     ## CDeck::getActiveDeck()
000000010047db0d	movq	_leftDeck(%rip), %rax
000000010047db14	jmp	0x10047dab7
000000010047db16	leaq	_sandbox(%rip), %rax
000000010047db1d	cmpb	$0x0, CONFIG_EMULATE_HARDWARE(%rax)
000000010047db20	je	0x10047dcf0
000000010047db26	movq	0x8(%rax), %rax
000000010047db2a	jmp	0x10047dab7
000000010047db2c	xorl	%eax, %eax
000000010047db2e	cmpl	$0x766c6565, %edi               ## imm = 0x766C6565
000000010047db34	jg	0x10047db55
000000010047db36	cmpl	$0x6c6f6164, %edi               ## imm = 0x6C6F6164
000000010047db3c	je	0x10047db7b
000000010047db3e	cmpl	$0x706c6179, %edi               ## imm = 0x706C6179
000000010047db44	jne	0x10047dab7
000000010047db4a	addq	$0x8, %rsp
000000010047db4e	popq	%rbx
000000010047db4f	popq	%rbp
000000010047db50	jmp	__ZN5CDeck14getPlayingDeckEv    ## CDeck::getPlayingDeck()
000000010047db55	cmpl	$0x766c6566, %edi               ## imm = 0x766C6566
000000010047db5b	je	0x10047db99
000000010047db5d	cmpl	$0x76726967, %edi               ## imm = 0x76726967
000000010047db63	jne	0x10047dab7
000000010047db69	leaq	_videoEngine(%rip), %rdi
000000010047db70	addq	$0x8, %rsp
000000010047db74	popq	%rbx
000000010047db75	popq	%rbp
000000010047db76	jmp	__ZN12CVideoEngine12getRightDeckEv ## CVideoEngine::getRightDeck()
000000010047db7b	leaq	_skinEngine(%rip), %rax
000000010047db82	movl	0x2c8(%rax), %edx
000000010047db88	cmpl	$0x1, %edx
000000010047db8b	jne	0x10047dbab
000000010047db8d	movq	__ZN5CDeck5decksE(%rip), %rax   ## CDeck::decks
000000010047db94	jmp	0x10047dab7
000000010047db99	leaq	_videoEngine(%rip), %rdi
000000010047dba0	addq	$0x8, %rsp
000000010047dba4	popq	%rbx
000000010047dba5	popq	%rbp
000000010047dba6	jmp	__ZN12CVideoEngine11getLeftDeckEv ## CVideoEngine::getLeftDeck()
000000010047dbab	movq	_defaultDeck(%rip), %rax
000000010047dbb2	movq	0x6c8(%rax), %rcx
000000010047dbb9	movl	0x244(%rcx), %ecx
000000010047dbbf	testl	%ecx, %ecx
000000010047dbc1	setns	%sil
000000010047dbc5	cmpl	$-0x3, %ecx
000000010047dbc8	sete	%cl
000000010047dbcb	orb	%sil, %cl
000000010047dbce	jne	0x10047dbdc
000000010047dbd0	cmpl	%edx, 0x240(%rax)
000000010047dbd6	jl	0x10047dab7
000000010047dbdc	movq	_leftDeck(%rip), %rcx
000000010047dbe3	movq	0x6c8(%rcx), %rsi
000000010047dbea	movl	0x244(%rsi), %esi
000000010047dbf0	testl	%esi, %esi
000000010047dbf2	sets	%dil
000000010047dbf6	cmpl	$-0x3, %esi
000000010047dbf9	setne	%sil
000000010047dbfd	testb	%sil, %dil
000000010047dc00	jne	0x10047dcf7
000000010047dc06	movq	_rightDeck(%rip), %rsi
000000010047dc0d	movq	0x6c8(%rsi), %rdi
000000010047dc14	movl	0x244(%rdi), %edi
000000010047dc1a	testl	%edi, %edi
000000010047dc1c	sets	%r8b
000000010047dc20	cmpl	$-0x3, %edi
000000010047dc23	setne	%dil
000000010047dc27	testb	%dil, %r8b
000000010047dc2a	jne	0x10047dcff
000000010047dc30	cmpb	$0x1, 0x280(%rax)
000000010047dc37	jne	0x10047dab7
000000010047dc3d	cmpb	$0x1, 0x280(%rcx)
000000010047dc44	movq	%rcx, %rax
000000010047dc47	jne	0x10047dab7
000000010047dc4d	cmpb	$0x1, 0x280(%rsi)
000000010047dc54	movq	%rsi, %rax
000000010047dc57	jne	0x10047dab7
000000010047dc5d	cmpl	$0x3, %edx
000000010047dc60	movl	$0x2, %ecx
000000010047dc65	cmovgel	%edx, %ecx
000000010047dc68	cmpq	%rcx, %rbx
000000010047dc6b	cmovbq	%rbx, %rcx
000000010047dc6f	testq	%rbx, %rbx
000000010047dc72	je	0x10047dcf0
000000010047dc74	shlq	$0x3, %rcx
000000010047dc78	xorl	%esi, %esi
000000010047dc7a	leaq	__ZN5CDeck5decksE(%rip), %rdx   ## CDeck::decks
000000010047dc81	movq	CONFIG_EMULATE_HARDWARE(%rsi,%rdx), %rax
000000010047dc85	movq	0x6c8(%rax), %rdi
000000010047dc8c	movl	0x244(%rdi), %edi
000000010047dc92	testl	%edi, %edi
000000010047dc94	sets	%r8b
000000010047dc98	cmpl	$-0x3, %edi
000000010047dc9b	setne	%dil
000000010047dc9f	testb	%dil, %r8b
000000010047dca2	jne	0x10047dab7
000000010047dca8	cmpb	$0x0, 0x280(%rax)
000000010047dcaf	je	0x10047dab7
000000010047dcb5	addq	$0x8, %rsi
000000010047dcb9	cmpq	%rsi, %rcx
000000010047dcbc	jne	0x10047dc81
000000010047dcbe	testq	%rbx, %rbx
000000010047dcc1	je	0x10047dcf0
000000010047dcc3	xorl	%esi, %esi
000000010047dcc5	movq	CONFIG_EMULATE_HARDWARE(%rsi,%rdx), %rax
000000010047dcc9	movq	0x6c8(%rax), %rdi
000000010047dcd0	cmpl	$-0x3, 0x244(%rdi)
000000010047dcd7	je	0x10047dab7
000000010047dcdd	addq	$0x8, %rsi
000000010047dce1	movl	$CONFIG_EMULATE_HARDWARE, %eax
000000010047dce6	cmpq	%rsi, %rcx
000000010047dce9	jne	0x10047dcc5
000000010047dceb	jmp	0x10047dab7
000000010047dcf0	xorl	%eax, %eax
000000010047dcf2	jmp	0x10047dab7
000000010047dcf7	movq	%rcx, %rax
000000010047dcfa	jmp	0x10047dab7
000000010047dcff	movq	%rsi, %rax
000000010047dd02	jmp	0x10047dab7
000000010047dd07	nop
