__ZN11ACTION_zoom9onExecuteEv [0x1005c9310, 0x1005c9502):
00000001005c9310	pushq	%rbp
00000001005c9311	movq	%rsp, %rbp
00000001005c9314	pushq	%r15
00000001005c9316	pushq	%r14
00000001005c9318	pushq	%rbx
00000001005c9319	pushq	%rax
00000001005c931a	xorl	%esi, %esi
00000001005c931c	callq	__ZN7IAction8getParamEi         ## IAction::getParam(int)
00000001005c9321	movq	%rax, %r14
00000001005c9324	movq	%rax, %r15
00000001005c9327	movl	CONFIG_EMULATE_HARDWARE(%rax), %eax
00000001005c9329	movss	0x4bc6467(%rip), %xmm2
00000001005c9331	movl	$0x80070057, %ebx               ## imm = 0x80070057
00000001005c9336	cmpl	$0x747873, %eax                 ## imm = 0x747873
00000001005c933b	jg	0x1005c934f
00000001005c933d	testl	%eax, %eax
00000001005c933f	je	0x1005c93d6
00000001005c9345	cmpl	$0x25, %eax
00000001005c9348	je	0x1005c93a3
00000001005c934a	jmp	0x1005c93f0
00000001005c934f	cmpl	$0x76616c, %eax                 ## imm = 0x76616C
00000001005c9354	je	0x1005c93a3
00000001005c9356	cmpl	$0x747874, %eax                 ## imm = 0x747874
00000001005c935b	jne	0x1005c93f0
00000001005c9361	addq	$0x8, %r14
00000001005c9365	movzbl	0x8(%r15), %ecx
00000001005c936a	movl	%ecx, %eax
00000001005c936c	shrl	%eax
00000001005c936e	andb	$0x1, %cl
00000001005c9371	movq	0x10(%r15), %rdx
00000001005c9375	movq	%rdx, %rsi
00000001005c9378	cmoveq	%rax, %rsi
00000001005c937c	cmpq	$0x4, %rsi
00000001005c9380	jne	0x1005c940d
00000001005c9386	leaq	0x504f384(%rip), %rsi           ## literal pool for: "near"
00000001005c938d	movq	%r14, %rdi
00000001005c9390	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
00000001005c9395	testb	%al, %al
00000001005c9397	je	0x1005c93fd
00000001005c9399	movss	0x4bc410f(%rip), %xmm2
00000001005c93a1	jmp	0x1005c93d6
00000001005c93a3	movss	0x4(%r15), %xmm2
00000001005c93a9	cmpb	$0x0, 0x20(%r15)
00000001005c93ae	je	0x1005c93bf
00000001005c93b0	leaq	_Config(%rip), %rax
00000001005c93b7	addss	0x4350(%rax), %xmm2
00000001005c93bf	movss	0x4bc3941(%rip), %xmm0
00000001005c93c7	minss	%xmm2, %xmm0
00000001005c93cb	xorps	%xmm1, %xmm1
00000001005c93ce	cmpnless	%xmm1, %xmm2
00000001005c93d3	andps	%xmm0, %xmm2
00000001005c93d6	leaq	_Config(%rip), %rax
00000001005c93dd	movw	$CONFIG_VP9, 0x4310(%rax)
00000001005c93e6	movss	%xmm2, 0x4350(%rax)
00000001005c93ee	xorl	%ebx, %ebx
00000001005c93f0	movl	%ebx, %eax
00000001005c93f2	addq	$0x8, %rsp
00000001005c93f6	popq	%rbx
00000001005c93f7	popq	%r14
00000001005c93f9	popq	%r15
00000001005c93fb	popq	%rbp
00000001005c93fc	retq
00000001005c93fd	movzbl	0x8(%r15), %eax
00000001005c9402	movq	0x10(%r15), %rdx
00000001005c9406	movl	%eax, %ecx
00000001005c9408	andb	$0x1, %cl
00000001005c940b	shrl	%eax
00000001005c940d	testb	%cl, %cl
00000001005c940f	movq	%rdx, %rsi
00000001005c9412	cmoveq	%rax, %rsi
00000001005c9416	cmpq	$0x7, %rsi
00000001005c941a	jne	0x1005c9447
00000001005c941c	leaq	0x501efed(%rip), %rsi           ## literal pool for: "default"
00000001005c9423	movq	%r14, %rdi
00000001005c9426	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
00000001005c942b	movss	0x4bc6365(%rip), %xmm2
00000001005c9433	testb	%al, %al
00000001005c9435	jne	0x1005c93d6
00000001005c9437	movzbl	0x8(%r15), %eax
00000001005c943c	movq	0x10(%r15), %rdx
00000001005c9440	movl	%eax, %ecx
00000001005c9442	andb	$0x1, %cl
00000001005c9445	shrl	%eax
00000001005c9447	testb	%cl, %cl
00000001005c9449	movq	%rdx, %rsi
00000001005c944c	cmoveq	%rax, %rsi
00000001005c9450	cmpq	$0x3, %rsi
00000001005c9454	jne	0x1005c9486
00000001005c9456	leaq	0x504f2b9(%rip), %rsi           ## literal pool for: "far"
00000001005c945d	movq	%r14, %rdi
00000001005c9460	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
00000001005c9465	testb	%al, %al
00000001005c9467	je	0x1005c9476
00000001005c9469	movss	0x4bc4043(%rip), %xmm2
00000001005c9471	jmp	0x1005c93d6
00000001005c9476	movzbl	0x8(%r15), %eax
00000001005c947b	movq	0x10(%r15), %rdx
00000001005c947f	movl	%eax, %ecx
00000001005c9481	andb	$0x1, %cl
00000001005c9484	shrl	%eax
00000001005c9486	testb	%cl, %cl
00000001005c9488	cmovneq	%rdx, %rax
00000001005c948c	cmpq	$0x4, %rax
00000001005c9490	jne	0x1005c94a5
00000001005c9492	leaq	0x501e3cc(%rip), %rsi           ## literal pool for: "load"
00000001005c9499	movq	%r14, %rdi
00000001005c949c	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
00000001005c94a1	testb	%al, %al
00000001005c94a3	jne	0x1005c94b8
00000001005c94a5	leaq	0x504f26e(%rip), %rsi           ## literal pool for: "recall"
00000001005c94ac	movq	%r14, %rdi
00000001005c94af	callq	__Z13strIsEqualCILILm7EEbRKNSt3__112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEERAT__Kc ## bool strIsEqualCIL<7ul>(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const (&) [7ul])
00000001005c94b4	testb	%al, %al
00000001005c94b6	je	0x1005c94cc
00000001005c94b8	leaq	_Config(%rip), %rax
00000001005c94bf	movss	0x4450(%rax), %xmm2
00000001005c94c7	jmp	0x1005c93d6
00000001005c94cc	leaq	0x504f24e(%rip), %rsi           ## literal pool for: "save"
00000001005c94d3	movq	%r14, %rdi
00000001005c94d6	callq	__Z13strIsEqualCILILm5EEbRKNSt3__112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEERAT__Kc ## bool strIsEqualCIL<5ul>(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const (&) [5ul])
00000001005c94db	testb	%al, %al
00000001005c94dd	je	0x1005c93f0
00000001005c94e3	leaq	_Config(%rip), %rsi
00000001005c94ea	leaq	0x43d8(%rsi), %rdi
00000001005c94f1	addq	$0x42d8, %rsi                   ## imm = 0x42D8
00000001005c94f8	callq	__ZN13CSettingFloataSERKS_      ## CSettingFloat::operator=(CSettingFloat const&)
00000001005c94fd	jmp	0x1005c93ee
