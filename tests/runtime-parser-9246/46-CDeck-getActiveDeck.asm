__ZN5CDeck13getActiveDeckEv [0x10047dd08, 0x10047df68):
000000010047dd08	movq	_masterDeck(%rip), %rax
000000010047dd0f	testq	%rax, %rax
000000010047dd12	je	0x10047dd1c
000000010047dd14	movq	%rax, _activeDeck(%rip)
000000010047dd1b	retq
000000010047dd1c	pushq	%rbp
000000010047dd1d	movq	%rsp, %rbp
000000010047dd20	pushq	%r15
000000010047dd22	pushq	%r14
000000010047dd24	pushq	%r12
000000010047dd26	pushq	%rbx
000000010047dd27	subq	$0x10, %rsp
000000010047dd2b	movq	_nbDecks(%rip), %rcx
000000010047dd32	testq	%rcx, %rcx
000000010047dd35	je	0x10047de57
000000010047dd3b	movl	$0xffffffff, %eax               ## imm = 0xFFFFFFFF
000000010047dd40	leaq	__ZN5CDeck5decksE(%rip), %rdx   ## CDeck::decks
000000010047dd47	xorl	%esi, %esi
000000010047dd49	movq	CONFIG_EMULATE_HARDWARE(%rdx), %rdi
000000010047dd4c	cmpb	$0x1, 0x280(%rdi)
000000010047dd53	jne	0x10047dd5b
000000010047dd55	testl	%eax, %eax
000000010047dd57	jns	0x10047dd69
000000010047dd59	movl	%esi, %eax
000000010047dd5b	incq	%rsi
000000010047dd5e	addq	$0x8, %rdx
000000010047dd62	cmpq	%rsi, %rcx
000000010047dd65	jne	0x10047dd49
000000010047dd67	jmp	0x10047dd6b
000000010047dd69	movl	%ecx, %eax
000000010047dd6b	testl	%eax, %eax
000000010047dd6d	js	0x10047de57
000000010047dd73	cmpl	%ecx, %eax
000000010047dd75	jge	0x10047dda5
000000010047dd77	movl	%eax, %eax
000000010047dd79	leaq	__ZN5CDeck5decksE(%rip), %rdx   ## CDeck::decks
000000010047dd80	movq	CONFIG_EMULATE_HARDWARE(%rdx,%rax,8), %rax
000000010047dd84	movq	0x6c8(%rax), %rdx
000000010047dd8b	cmpl	$-0x3, 0x244(%rdx)
000000010047dd92	jne	0x10047de6a
000000010047dd98	cmpb	$0x1, 0x290(%rax)
000000010047dd9f	je	0x10047de6a
000000010047dda5	testq	%rcx, %rcx
000000010047dda8	je	0x10047de7e
000000010047ddae	movl	$0xffffffff, %ebx               ## imm = 0xFFFFFFFF
000000010047ddb3	xorps	%xmm0, %xmm0
000000010047ddb6	leaq	__ZN5CDeck5decksE(%rip), %r14   ## CDeck::decks
000000010047ddbd	xorl	%r15d, %r15d
000000010047ddc0	movl	$0xffffffff, %r12d              ## imm = 0xFFFFFFFF
000000010047ddc6	movq	CONFIG_EMULATE_HARDWARE(%r14), %rdi
000000010047ddc9	cmpb	$0x1, 0x280(%rdi)
000000010047ddd0	jne	0x10047de32
000000010047ddd2	movq	0x6c8(%rdi), %rax
000000010047ddd9	cmpl	$-0x3, 0x244(%rax)
000000010047dde0	jne	0x10047ddeb
000000010047dde2	cmpb	$0x1, 0x290(%rdi)
000000010047dde9	jne	0x10047de32
000000010047ddeb	movss	%xmm0, -0x24(%rbp)
000000010047ddf0	callq	__ZN5CDeck16getAudibleVolumeEv  ## CDeck::getAudibleVolume()
000000010047ddf5	ucomiss	-0x24(%rbp), %xmm0
000000010047ddf9	jbe	0x10047de08
000000010047ddfb	movq	CONFIG_EMULATE_HARDWARE(%r14), %rdi
000000010047ddfe	callq	__ZN5CDeck16getAudibleVolumeEv  ## CDeck::getAudibleVolume()
000000010047de03	movl	%r15d, %r12d
000000010047de06	jmp	0x10047de32
000000010047de08	movq	CONFIG_EMULATE_HARDWARE(%r14), %rdi
000000010047de0b	callq	__ZN5CDeck16getAudibleVolumeEv  ## CDeck::getAudibleVolume()
000000010047de10	ucomiss	-0x24(%rbp), %xmm0
000000010047de14	movss	-0x24(%rbp), %xmm0
000000010047de19	jne	0x10047de32
000000010047de1b	jp	0x10047de32
000000010047de1d	movq	CONFIG_EMULATE_HARDWARE(%r14), %rax
000000010047de20	movq	0x6c8(%rax), %rax
000000010047de27	cmpl	$-0x3, 0x244(%rax)
000000010047de2e	cmovnel	%ebx, %r12d
000000010047de32	incq	%r15
000000010047de35	addq	$0x8, %r14
000000010047de39	cmpq	_nbDecks(%rip), %r15
000000010047de40	jb	0x10047ddc6
000000010047de42	testl	%r12d, %r12d
000000010047de45	js	0x10047de81
000000010047de47	movl	%r12d, %eax
000000010047de4a	leaq	__ZN5CDeck5decksE(%rip), %rcx   ## CDeck::decks
000000010047de51	movq	CONFIG_EMULATE_HARDWARE(%rcx,%rax,8), %rax
000000010047de55	jmp	0x10047de6a
000000010047de57	movq	_activeDeck(%rip), %rax
000000010047de5e	testq	%rax, %rax
000000010047de61	jne	0x10047de71
000000010047de63	movq	_defaultDeck(%rip), %rax
000000010047de6a	movq	%rax, _activeDeck(%rip)
000000010047de71	addq	$0x10, %rsp
000000010047de75	popq	%rbx
000000010047de76	popq	%r12
000000010047de78	popq	%r14
000000010047de7a	popq	%r15
000000010047de7c	popq	%rbp
000000010047de7d	retq
000000010047de7e	xorps	%xmm0, %xmm0
000000010047de81	movss	%xmm0, -0x24(%rbp)
000000010047de86	movq	_activeDeck(%rip), %rdi
000000010047de8d	testq	%rdi, %rdi
000000010047de90	je	0x10047deb1
000000010047de92	cmpb	$0x1, 0x280(%rdi)
000000010047de99	jne	0x10047deb1
000000010047de9b	callq	__ZN5CDeck16getAudibleVolumeEv  ## CDeck::getAudibleVolume()
000000010047dea0	ucomiss	-0x24(%rbp), %xmm0
000000010047dea4	jne	0x10047deb1
000000010047dea6	jp	0x10047deb1
000000010047dea8	movq	_activeDeck(%rip), %rax
000000010047deaf	jmp	0x10047de71
000000010047deb1	movq	_leftDeck(%rip), %rdi
000000010047deb8	cmpb	$0x1, 0x280(%rdi)
000000010047debf	jne	0x10047dede
000000010047dec1	callq	__ZN5CDeck16getAudibleVolumeEv  ## CDeck::getAudibleVolume()
000000010047dec6	ucomiss	-0x24(%rbp), %xmm0
000000010047deca	jne	0x10047dede
000000010047decc	jp	0x10047dede
000000010047dece	movq	_leftDeck(%rip), %rax
000000010047ded5	cmpq	_defaultDeck(%rip), %rax
000000010047dedc	jne	0x10047de6a
000000010047dede	movq	_rightDeck(%rip), %rdi
000000010047dee5	cmpb	$0x1, 0x280(%rdi)
000000010047deec	jne	0x10047df0f
000000010047deee	callq	__ZN5CDeck16getAudibleVolumeEv  ## CDeck::getAudibleVolume()
000000010047def3	ucomiss	-0x24(%rbp), %xmm0
000000010047def7	jne	0x10047df0f
000000010047def9	jp	0x10047df0f
000000010047defb	movq	_rightDeck(%rip), %rax
000000010047df02	cmpq	_defaultDeck(%rip), %rax
000000010047df09	jne	0x10047de6a
000000010047df0f	cmpq	$0x0, _nbDecks(%rip)
000000010047df17	je	0x10047df5c
000000010047df19	leaq	__ZN5CDeck5decksE(%rip), %rbx   ## CDeck::decks
000000010047df20	xorl	%r14d, %r14d
000000010047df23	movq	CONFIG_EMULATE_HARDWARE(%rbx), %rdi
000000010047df26	cmpb	$0x1, 0x280(%rdi)
000000010047df2d	jne	0x10047df4c
000000010047df2f	callq	__ZN5CDeck16getAudibleVolumeEv  ## CDeck::getAudibleVolume()
000000010047df34	ucomiss	-0x24(%rbp), %xmm0
000000010047df38	jne	0x10047df4c
000000010047df3a	jp	0x10047df4c
000000010047df3c	movq	CONFIG_EMULATE_HARDWARE(%rbx), %rax
000000010047df3f	cmpq	_defaultDeck(%rip), %rax
000000010047df46	jne	0x10047de6a
000000010047df4c	incq	%r14
000000010047df4f	addq	$0x8, %rbx
000000010047df53	cmpq	_nbDecks(%rip), %r14
000000010047df5a	jb	0x10047df23
000000010047df5c	movq	_defaultDeck(%rip), %rax
000000010047df63	jmp	0x10047de71
