__ZNK8CXMLNode12getBoolParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEEb:
000000010037625a	pushq	%rbp
000000010037625b	movq	%rsp, %rbp
000000010037625e	pushq	%r15
0000000100376260	pushq	%r14
0000000100376262	pushq	%r13
0000000100376264	pushq	%r12
0000000100376266	pushq	%rbx
0000000100376267	pushq	%rax
0000000100376268	movl	%ecx, %r14d
000000010037626b	testq	%rdi, %rdi
000000010037626e	je	0x1003762c8
0000000100376270	movq	%rdi, %r15
0000000100376273	movq	0x18(%rdi), %rax
0000000100376277	cmpq	%rax, 0x20(%rdi)
000000010037627b	je	0x1003762c8
000000010037627d	movq	%rdx, %r12
0000000100376280	movq	%rsi, %r13
0000000100376283	xorl	%ebx, %ebx
0000000100376285	movq	VPX_ARCH_MIPS(%rax,%rbx,8), %rdi
0000000100376289	movzbl	VPX_ARCH_MIPS(%rdi), %esi
000000010037628c	testb	$0x1, %sil
0000000100376290	jne	0x10037629a
0000000100376292	incq	%rdi
0000000100376295	shrq	%rsi
0000000100376298	jmp	0x1003762a2
000000010037629a	movq	0x8(%rdi), %rsi
000000010037629e	movq	0x10(%rdi), %rdi
00000001003762a2	movq	%r13, %rdx
00000001003762a5	movq	%r12, %rcx
00000001003762a8	callq	__Z12strIsEqualCINSt3__117basic_string_viewIcNS_11char_traitsIcEEEES3_ ## strIsEqualCI(std::__1::basic_string_view<char, std::__1::char_traits<char>>, std::__1::basic_string_view<char, std::__1::char_traits<char>>)
00000001003762ad	testb	%al, %al
00000001003762af	jne	0x1003762da
00000001003762b1	incq	%rbx
00000001003762b4	movq	0x18(%r15), %rax
00000001003762b8	movq	0x20(%r15), %rcx
00000001003762bc	subq	%rax, %rcx
00000001003762bf	sarq	$0x3, %rcx
00000001003762c3	cmpq	%rcx, %rbx
00000001003762c6	jb	0x100376285
00000001003762c8	movl	%r14d, %eax
00000001003762cb	addq	$0x8, %rsp
00000001003762cf	popq	%rbx
00000001003762d0	popq	%r12
00000001003762d2	popq	%r13
00000001003762d4	popq	%r14
00000001003762d6	popq	%r15
00000001003762d8	popq	%rbp
00000001003762d9	retq
00000001003762da	movq	0x18(%r15), %rax
00000001003762de	movq	VPX_ARCH_MIPS(%rax,%rbx,8), %rdi
00000001003762e2	movzbl	0x18(%rdi), %ecx
00000001003762e6	movq	%rcx, %rax
00000001003762e9	shrq	%rax
00000001003762ec	andb	$0x1, %cl
00000001003762ef	movq	0x20(%rdi), %rdx
00000001003762f3	movq	%rdx, %rsi
00000001003762f6	cmoveq	%rax, %rsi
00000001003762fa	cmpq	$0x3, %rsi
00000001003762fe	jne	0x100376330
0000000100376300	addq	$0x18, %rdi
0000000100376304	leaq	0x54810b0(%rip), %rsi           ## literal pool for: "yes"
000000010037630b	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
0000000100376310	movl	%eax, %ecx
0000000100376312	movb	$0x1, %al
0000000100376314	testb	%cl, %cl
0000000100376316	jne	0x1003762cb
0000000100376318	movq	0x18(%r15), %rax
000000010037631c	movq	VPX_ARCH_MIPS(%rax,%rbx,8), %rdi
0000000100376320	movzbl	0x18(%rdi), %eax
0000000100376324	movq	0x20(%rdi), %rdx
0000000100376328	movl	%eax, %ecx
000000010037632a	andb	$0x1, %cl
000000010037632d	shrq	%rax
0000000100376330	testb	%cl, %cl
0000000100376332	movq	%rdx, %rsi
0000000100376335	cmoveq	%rax, %rsi
0000000100376339	cmpq	$0x4, %rsi
000000010037633d	jne	0x100376373
000000010037633f	addq	$0x18, %rdi
0000000100376343	leaq	0x548a8bf(%rip), %rsi           ## literal pool for: "true"
000000010037634a	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
000000010037634f	movl	%eax, %ecx
0000000100376351	movb	$0x1, %al
0000000100376353	testb	%cl, %cl
0000000100376355	jne	0x1003762cb
000000010037635b	movq	0x18(%r15), %rax
000000010037635f	movq	VPX_ARCH_MIPS(%rax,%rbx,8), %rdi
0000000100376363	movzbl	0x18(%rdi), %eax
0000000100376367	movq	0x20(%rdi), %rdx
000000010037636b	movl	%eax, %ecx
000000010037636d	andb	$0x1, %cl
0000000100376370	shrq	%rax
0000000100376373	testb	%cl, %cl
0000000100376375	movq	%rdx, %rsi
0000000100376378	cmoveq	%rax, %rsi
000000010037637c	cmpq	$0x2, %rsi
0000000100376380	jne	0x1003763b5
0000000100376382	addq	$0x18, %rdi
0000000100376386	leaq	0x548103a(%rip), %rsi           ## literal pool for: "no"
000000010037638d	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
0000000100376392	testb	%al, %al
0000000100376394	je	0x10037639d
0000000100376396	xorl	%eax, %eax
0000000100376398	jmp	0x1003762cb
000000010037639d	movq	0x18(%r15), %rax
00000001003763a1	movq	VPX_ARCH_MIPS(%rax,%rbx,8), %rdi
00000001003763a5	movzbl	0x18(%rdi), %eax
00000001003763a9	movq	0x20(%rdi), %rdx
00000001003763ad	movl	%eax, %ecx
00000001003763af	andb	$0x1, %cl
00000001003763b2	shrq	%rax
00000001003763b5	testb	%cl, %cl
00000001003763b7	cmovneq	%rdx, %rax
00000001003763bb	cmpq	$0x5, %rax
00000001003763bf	jne	0x1003762c8
00000001003763c5	addq	$0x18, %rdi
00000001003763c9	leaq	0x54999b0(%rip), %rsi           ## literal pool for: "false"
00000001003763d0	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
00000001003763d5	notb	%al
00000001003763d7	andb	%r14b, %al
00000001003763da	jmp	0x1003762cb
00000001003763df	nop
00000001003763e0	nop
00000001003763e1	nop
00000001003763e2	nop
00000001003763e3	nop
00000001003763e4	nop
00000001003763e5	nop
00000001003763e6	nop
00000001003763e7	nop
00000001003763e8	nop
00000001003763e9	nop
00000001003763ea	nop
00000001003763eb	nop
