__ZNK8CXMLNode14getBoolParamNSEPKcib:
000000010022aaf6	pushq	%rbp
000000010022aaf7	movq	%rsp, %rbp
000000010022aafa	pushq	%r15
000000010022aafc	pushq	%r14
000000010022aafe	pushq	%r13
000000010022ab00	pushq	%r12
000000010022ab02	pushq	%rbx
000000010022ab03	pushq	%rax
000000010022ab04	testq	%rdi, %rdi
000000010022ab07	je	0x10022ab57
000000010022ab09	movq	0x18(%rdi), %rbx
000000010022ab0d	movq	0x20(%rdi), %r12
000000010022ab11	cmpq	%r12, %rbx
000000010022ab14	je	0x10022ab57
000000010022ab16	movq	%rsi, %r15
000000010022ab19	movl	%ecx, -0x2c(%rbp)
000000010022ab1c	movslq	%edx, %r14
000000010022ab1f	movq	CONFIG_BETTER_HW_COMPATIBILITY(%rbx), %r13
000000010022ab22	movzbl	(%r13), %eax
000000010022ab27	testb	$0x1, %al
000000010022ab29	jne	0x10022ab30
000000010022ab2b	shrq	%rax
000000010022ab2e	jmp	0x10022ab34
000000010022ab30	movq	0x8(%r13), %rax
000000010022ab34	cmpq	%r14, %rax
000000010022ab37	jne	0x10022ab48
000000010022ab39	movq	%r13, %rdi
000000010022ab3c	movq	%r15, %rsi
000000010022ab3f	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
000000010022ab44	testb	%al, %al
000000010022ab46	jne	0x10022ab6c
000000010022ab48	addq	$0x8, %rbx
000000010022ab4c	cmpq	%rbx, %r12
000000010022ab4f	jne	0x10022ab1f
000000010022ab51	movl	-0x2c(%rbp), %r12d
000000010022ab55	jmp	0x10022ab5a
000000010022ab57	movl	%ecx, %r12d
000000010022ab5a	movl	%r12d, %eax
000000010022ab5d	addq	$0x8, %rsp
000000010022ab61	popq	%rbx
000000010022ab62	popq	%r12
000000010022ab64	popq	%r13
000000010022ab66	popq	%r14
000000010022ab68	popq	%r15
000000010022ab6a	popq	%rbp
000000010022ab6b	retq
000000010022ab6c	leaq	0x18(%r13), %r15
000000010022ab70	movzbl	0x18(%r13), %ecx
000000010022ab75	movq	%rcx, %rax
000000010022ab78	shrq	%rax
000000010022ab7b	movb	$0x1, %r12b
000000010022ab7e	andb	%r12b, %cl
000000010022ab81	movq	0x20(%r13), %rdx
000000010022ab85	movq	%rdx, %rsi
000000010022ab88	cmoveq	%rax, %rsi
000000010022ab8c	cmpq	$0x3, %rsi
000000010022ab90	jne	0x10022abb6
000000010022ab92	leaq	0x1cd1ef1(%rip), %rsi           ## literal pool for: "yes"
000000010022ab99	movq	%r15, %rdi
000000010022ab9c	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
000000010022aba1	testb	%al, %al
000000010022aba3	jne	0x10022ab5a
000000010022aba5	movzbl	0x18(%r13), %eax
000000010022abaa	movq	0x20(%r13), %rdx
000000010022abae	movl	%eax, %ecx
000000010022abb0	andb	$0x1, %cl
000000010022abb3	shrq	%rax
000000010022abb6	testb	%cl, %cl
000000010022abb8	movq	%rdx, %rsi
000000010022abbb	cmoveq	%rax, %rsi
000000010022abbf	cmpq	$0x4, %rsi
000000010022abc3	jne	0x10022abf0
000000010022abc5	leaq	0x1cd5161(%rip), %rsi           ## literal pool for: "true"
000000010022abcc	movq	%r15, %rdi
000000010022abcf	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
000000010022abd4	movb	$0x1, %r12b
000000010022abd7	testb	%al, %al
000000010022abd9	jne	0x10022ab5a
000000010022abdf	movzbl	0x18(%r13), %eax
000000010022abe4	movq	0x20(%r13), %rdx
000000010022abe8	movl	%eax, %ecx
000000010022abea	andb	$0x1, %cl
000000010022abed	shrq	%rax
000000010022abf0	testb	%cl, %cl
000000010022abf2	movq	%rdx, %rsi
000000010022abf5	cmoveq	%rax, %rsi
000000010022abf9	cmpq	$0x2, %rsi
000000010022abfd	jne	0x10022ac2b
000000010022abff	leaq	0x1cd1e88(%rip), %rsi           ## literal pool for: "no"
000000010022ac06	movq	%r15, %rdi
000000010022ac09	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
000000010022ac0e	testb	%al, %al
000000010022ac10	je	0x10022ac1a
000000010022ac12	xorl	%r12d, %r12d
000000010022ac15	jmp	0x10022ab5a
000000010022ac1a	movzbl	0x18(%r13), %eax
000000010022ac1f	movq	0x20(%r13), %rdx
000000010022ac23	movl	%eax, %ecx
000000010022ac25	andb	$0x1, %cl
000000010022ac28	shrq	%rax
000000010022ac2b	testb	%cl, %cl
000000010022ac2d	cmovneq	%rdx, %rax
000000010022ac31	cmpq	$0x5, %rax
000000010022ac35	jne	0x10022ab51
000000010022ac3b	leaq	0x1cd50f0(%rip), %rsi           ## literal pool for: "false"
000000010022ac42	movq	%r15, %rdi
000000010022ac45	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
000000010022ac4a	notb	%al
000000010022ac4c	andb	-0x2c(%rbp), %al
000000010022ac4f	jmp	0x10022ab5d
