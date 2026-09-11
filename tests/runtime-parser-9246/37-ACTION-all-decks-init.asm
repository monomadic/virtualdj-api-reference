__ZN16ACTION_all_decks4initEv [0x1000fe6c2, 0x1000fe704):
00000001000fe6c2	pushq	%rbp
00000001000fe6c3	movq	%rsp, %rbp
00000001000fe6c6	pushq	%rbx
00000001000fe6c7	pushq	%rax
00000001000fe6c8	movq	%rdi, %rbx
00000001000fe6cb	movq	0x38(%rdi), %rax
00000001000fe6cf	testq	%rax, %rax
00000001000fe6d2	je	0x1000fe6f5
00000001000fe6d4	movq	0x70(%rbx), %rdi
00000001000fe6d8	movq	%rax, 0x70(%rbx)
00000001000fe6dc	testq	%rdi, %rdi
00000001000fe6df	je	0x1000fe6ed
00000001000fe6e1	lock
00000001000fe6e2	decl	0x8(%rdi)
00000001000fe6e5	jg	0x1000fe6ed
00000001000fe6e7	movq	CONFIG_EMULATE_HARDWARE(%rdi), %rax
00000001000fe6ea	callq	*0x8(%rax)
00000001000fe6ed	movq	$CONFIG_EMULATE_HARDWARE, 0x38(%rbx)
00000001000fe6f5	cmpq	$0x0, 0x70(%rbx)
00000001000fe6fa	setne	%al
00000001000fe6fd	addq	$0x8, %rsp
00000001000fe701	popq	%rbx
00000001000fe702	popq	%rbp
00000001000fe703	retq
