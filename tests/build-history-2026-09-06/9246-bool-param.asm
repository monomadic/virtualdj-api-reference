__ZNK8CXMLNode12getBoolParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEEb:
000000010044fbee	testq	%rdi, %rdi
000000010044fbf1	je	0x10044fc56
000000010044fbf3	pushq	%rbp
000000010044fbf4	movq	%rsp, %rbp
000000010044fbf7	pushq	%r15
000000010044fbf9	pushq	%r14
000000010044fbfb	pushq	%r13
000000010044fbfd	pushq	%r12
000000010044fbff	pushq	%rbx
000000010044fc00	pushq	%rax
000000010044fc01	movq	0x18(%rdi), %r13
000000010044fc05	movq	0x20(%rdi), %rbx
000000010044fc09	cmpq	%rbx, %r13
000000010044fc0c	je	0x10044fc59
000000010044fc0e	movq	%rdx, %r14
000000010044fc11	movq	%rsi, %r15
000000010044fc14	movl	%ecx, -0x2c(%rbp)
000000010044fc17	movq	(%r13), %r12
000000010044fc1b	movzbl	CONFIG_EMULATE_HARDWARE(%r12), %esi
000000010044fc20	testb	$0x1, %sil
000000010044fc24	jne	0x10044fc2f
000000010044fc26	leaq	0x1(%r12), %rdi
000000010044fc2b	shrl	%esi
000000010044fc2d	jmp	0x10044fc39
000000010044fc2f	movq	0x8(%r12), %rsi
000000010044fc34	movq	0x10(%r12), %rdi
000000010044fc39	movq	%r15, %rdx
000000010044fc3c	movq	%r14, %rcx
000000010044fc3f	callq	__Z12strIsEqualCINSt3__117basic_string_viewIcNS_11char_traitsIcEEEES3_ ## strIsEqualCI(std::__1::basic_string_view<char, std::__1::char_traits<char>>, std::__1::basic_string_view<char, std::__1::char_traits<char>>)
000000010044fc44	testb	%al, %al
000000010044fc46	jne	0x10044fc6a
000000010044fc48	addq	$0x8, %r13
000000010044fc4c	cmpq	%rbx, %r13
000000010044fc4f	jne	0x10044fc17
000000010044fc51	movl	-0x2c(%rbp), %eax
000000010044fc54	jmp	0x10044fc5b
000000010044fc56	movl	%ecx, %eax
000000010044fc58	retq
000000010044fc59	movl	%ecx, %eax
000000010044fc5b	addq	$0x8, %rsp
000000010044fc5f	popq	%rbx
000000010044fc60	popq	%r12
000000010044fc62	popq	%r13
000000010044fc64	popq	%r14
000000010044fc66	popq	%r15
000000010044fc68	popq	%rbp
000000010044fc69	retq
000000010044fc6a	leaq	0x18(%r12), %r14
000000010044fc6f	movzbl	0x18(%r12), %ecx
000000010044fc75	movl	%ecx, %eax
000000010044fc77	shrl	%eax
000000010044fc79	andb	$0x1, %cl
000000010044fc7c	movq	0x20(%r12), %rdx
000000010044fc81	movq	%rdx, %rsi
000000010044fc84	cmoveq	%rax, %rsi
000000010044fc88	cmpq	$0x3, %rsi
000000010044fc8c	jne	0x10044fcb7
000000010044fc8e	leaq	0x518cb5a(%rip), %rsi           ## literal pool for: "yes"
000000010044fc95	movq	%r14, %rdi
000000010044fc98	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
000000010044fc9d	movl	%eax, %ecx
000000010044fc9f	movb	$0x1, %al
000000010044fca1	testb	%cl, %cl
000000010044fca3	jne	0x10044fc5b
000000010044fca5	movzbl	0x18(%r12), %eax
000000010044fcab	movq	0x20(%r12), %rdx
000000010044fcb0	movl	%eax, %ecx
000000010044fcb2	andb	$0x1, %cl
000000010044fcb5	shrl	%eax
000000010044fcb7	testb	%cl, %cl
000000010044fcb9	movq	%rdx, %rsi
000000010044fcbc	cmoveq	%rax, %rsi
000000010044fcc0	cmpq	$0x4, %rsi
000000010044fcc4	jne	0x10044fcf3
000000010044fcc6	leaq	0x51aaec1(%rip), %rsi           ## literal pool for: "true"
000000010044fccd	movq	%r14, %rdi
000000010044fcd0	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
000000010044fcd5	movl	%eax, %ecx
000000010044fcd7	movb	$0x1, %al
000000010044fcd9	testb	%cl, %cl
000000010044fcdb	jne	0x10044fc5b
000000010044fce1	movzbl	0x18(%r12), %eax
000000010044fce7	movq	0x20(%r12), %rdx
000000010044fcec	movl	%eax, %ecx
000000010044fcee	andb	$0x1, %cl
000000010044fcf1	shrl	%eax
000000010044fcf3	testb	%cl, %cl
000000010044fcf5	movq	%rdx, %rsi
000000010044fcf8	cmoveq	%rax, %rsi
000000010044fcfc	cmpq	$0x2, %rsi
000000010044fd00	jne	0x10044fd2e
000000010044fd02	leaq	0x518cb00(%rip), %rsi           ## literal pool for: "no"
000000010044fd09	movq	%r14, %rdi
000000010044fd0c	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
000000010044fd11	testb	%al, %al
000000010044fd13	je	0x10044fd1c
000000010044fd15	xorl	%eax, %eax
000000010044fd17	jmp	0x10044fc5b
000000010044fd1c	movzbl	0x18(%r12), %eax
000000010044fd22	movq	0x20(%r12), %rdx
000000010044fd27	movl	%eax, %ecx
000000010044fd29	andb	$0x1, %cl
000000010044fd2c	shrl	%eax
000000010044fd2e	testb	%cl, %cl
000000010044fd30	cmovneq	%rdx, %rax
000000010044fd34	cmpq	$0x5, %rax
000000010044fd38	jne	0x10044fc51
000000010044fd3e	leaq	0x5196a50(%rip), %rsi           ## literal pool for: "false"
000000010044fd45	movq	%r14, %rdi
000000010044fd48	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
000000010044fd4d	notb	%al
000000010044fd4f	andb	-0x2c(%rbp), %al
000000010044fd52	jmp	0x10044fc5b
000000010044fd57	addb	%dl, 0x48(%rbp)
