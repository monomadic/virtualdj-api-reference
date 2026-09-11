__ZN15DLGActionWizard5STree8setColorEj [0x1006c6a46, 0x1006c6aba):
00000001006c6a46	pushq	%rbp
00000001006c6a47	movq	%rsp, %rbp
00000001006c6a4a	pushq	%r14
00000001006c6a4c	pushq	%rbx
00000001006c6a4d	movl	%esi, %ebx
00000001006c6a4f	movq	%rdi, %r14
00000001006c6a52	movq	CONFIG_EMULATE_HARDWARE(%r14), %rax
00000001006c6a55	movq	0x8(%r14), %rcx
00000001006c6a59	subq	%rax, %rcx
00000001006c6a5c	je	0x1006c6a7b
00000001006c6a5e	sarq	$0x3, %rcx
00000001006c6a62	cmpq	$0x1, %rcx
00000001006c6a66	adcq	$0x0, %rcx
00000001006c6a6a	xorl	%edx, %edx
00000001006c6a6c	movq	CONFIG_EMULATE_HARDWARE(%rax,%rdx,8), %rsi
00000001006c6a70	movl	%ebx, 0x10(%rsi)
00000001006c6a73	incq	%rdx
00000001006c6a76	cmpq	%rdx, %rcx
00000001006c6a79	jne	0x1006c6a6c
00000001006c6a7b	movq	0x18(%r14), %rdi
00000001006c6a7f	testq	%rdi, %rdi
00000001006c6a82	je	0x1006c6a8b
00000001006c6a84	movl	%ebx, %esi
00000001006c6a86	callq	__ZN15DLGActionWizard5STree8setColorEj ## DLGActionWizard::STree::setColor(unsigned int)
00000001006c6a8b	movq	0x20(%r14), %rdi
00000001006c6a8f	testq	%rdi, %rdi
00000001006c6a92	je	0x1006c6a9b
00000001006c6a94	movl	%ebx, %esi
00000001006c6a96	callq	__ZN15DLGActionWizard5STree8setColorEj ## DLGActionWizard::STree::setColor(unsigned int)
00000001006c6a9b	movq	0x28(%r14), %rdi
00000001006c6a9f	testq	%rdi, %rdi
00000001006c6aa2	je	0x1006c6aab
00000001006c6aa4	movl	%ebx, %esi
00000001006c6aa6	callq	__ZN15DLGActionWizard5STree8setColorEj ## DLGActionWizard::STree::setColor(unsigned int)
00000001006c6aab	movq	0x40(%r14), %r14
00000001006c6aaf	testq	%r14, %r14
00000001006c6ab2	jne	0x1006c6a52
00000001006c6ab4	popq	%rbx
00000001006c6ab5	popq	%r14
00000001006c6ab7	popq	%rbp
00000001006c6ab8	retq
00000001006c6ab9	nop
