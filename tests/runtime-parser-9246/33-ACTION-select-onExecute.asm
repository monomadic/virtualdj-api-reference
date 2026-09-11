__ZN13ACTION_select9onExecuteEv [0x10038ad7c, 0x10038ae4c):
000000010038ad7c	pushq	%rbp
000000010038ad7d	movq	%rsp, %rbp
000000010038ad80	pushq	%rbx
000000010038ad81	pushq	%rax
000000010038ad82	movq	%rdi, %rbx
000000010038ad85	movl	0x5c(%rdi), %eax
000000010038ad88	testl	%eax, %eax
000000010038ad8a	je	0x10038ad97
000000010038ad8c	cmpl	$0x61637469, %eax               ## imm = 0x61637469
000000010038ad91	jne	0x10038ae29
000000010038ad97	leaq	_nbDecks(%rip), %rax
000000010038ad9e	movl	CONFIG_EMULATE_HARDWARE(%rax), %eax
000000010038ada0	leaq	_skinEngine(%rip), %rcx
000000010038ada7	movl	0x2c8(%rcx), %edx
000000010038adad	cmpl	%eax, %edx
000000010038adaf	cmovgel	%eax, %edx
000000010038adb2	cmpl	$0x3, %edx
000000010038adb5	movl	$0x2, %ecx
000000010038adba	cmovgel	%edx, %ecx
000000010038adbd	cmpq	$0x0, 0x50(%rbx)
000000010038adc2	cmovnel	%eax, %ecx
000000010038adc5	leaq	_defaultDeck(%rip), %rax
000000010038adcc	movq	CONFIG_EMULATE_HARDWARE(%rax), %rax
000000010038adcf	cmpl	$0x2, %ecx
000000010038add2	jne	0x10038ae0d
000000010038add4	leaq	_leftDeck(%rip), %rdx
000000010038addb	movq	CONFIG_EMULATE_HARDWARE(%rdx), %rdi
000000010038adde	cmpq	%rdi, %rax
000000010038ade1	setne	%sil
000000010038ade5	leaq	_rightDeck(%rip), %rdx
000000010038adec	movq	CONFIG_EMULATE_HARDWARE(%rdx), %rdx
000000010038adef	cmpq	%rdx, %rax
000000010038adf2	sete	%r8b
000000010038adf6	orb	%sil, %r8b
000000010038adf9	je	0x10038ae2f
000000010038adfb	cmpq	%rdx, %rax
000000010038adfe	setne	%sil
000000010038ae02	cmpq	%rdx, %rdi
000000010038ae05	sete	%dl
000000010038ae08	orb	%sil, %dl
000000010038ae0b	je	0x10038ae38
000000010038ae0d	movl	0x240(%rax), %eax
000000010038ae13	incl	%eax
000000010038ae15	cltd
000000010038ae16	idivl	%ecx
000000010038ae18	leal	0x1(%rdx), %edi
000000010038ae1b	callq	__Z11getDeckSafei               ## getDeckSafe(int)
000000010038ae20	movq	%rax, %rdi
000000010038ae23	movq	%rax, 0x60(%rbx)
000000010038ae27	jmp	0x10038ae3c
000000010038ae29	movq	0x60(%rbx), %rdi
000000010038ae2d	jmp	0x10038ae3c
000000010038ae2f	movq	%rdx, 0x60(%rbx)
000000010038ae33	movq	%rdx, %rdi
000000010038ae36	jmp	0x10038ae3c
000000010038ae38	movq	%rdi, 0x60(%rbx)
000000010038ae3c	xorl	%esi, %esi
000000010038ae3e	callq	__ZN5CDeck6selectEb             ## CDeck::select(bool)
000000010038ae43	xorl	%eax, %eax
000000010038ae45	addq	$0x8, %rsp
000000010038ae49	popq	%rbx
000000010038ae4a	popq	%rbp
000000010038ae4b	retq
