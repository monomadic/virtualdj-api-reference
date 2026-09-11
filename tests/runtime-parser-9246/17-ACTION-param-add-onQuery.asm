__ZN16ACTION_param_add7onQueryER12SActionParam [0x1009929f4, 0x100992dc8):
00000001009929f4	pushq	%rbp
00000001009929f5	movq	%rsp, %rbp
00000001009929f8	pushq	%r15
00000001009929fa	pushq	%r14
00000001009929fc	pushq	%r13
00000001009929fe	pushq	%r12
0000000100992a00	pushq	%rbx
0000000100992a01	subq	$rf.rp_ref, %rsp
0000000100992a08	movq	%rsi, %rbx
0000000100992a0b	movq	0x4e2d616(%rip), %rax           ## literal pool symbol address: ___stack_chk_guard
0000000100992a12	movq	CONFIG_EMULATE_HARDWARE(%rax), %rax
0000000100992a15	movq	%rax, -0x30(%rbp)
0000000100992a19	movq	0x20(%rdi), %rsi
0000000100992a1d	movq	0x28(%rdi), %rcx
0000000100992a21	movl	$0x80070057, %eax               ## imm = 0x80070057
0000000100992a26	cmpq	%rcx, %rsi
0000000100992a29	je	0x100992d3d
0000000100992a2f	movq	%rdi, %r14
0000000100992a32	subq	%rsi, %rcx
0000000100992a35	cmpq	$0x50, %rcx
0000000100992a39	je	0x100992a49
0000000100992a3b	movl	CONFIG_EMULATE_HARDWARE(%rsi), %ecx
0000000100992a3d	cmpl	$0x747874, %ecx                 ## imm = 0x747874
0000000100992a43	jne	0x100992bd0
0000000100992a49	xorps	%xmm0, %xmm0
0000000100992a4c	leaq	-0xd0(%rbp), %rsi
0000000100992a53	movaps	%xmm0, 0x10(%rsi)
0000000100992a57	movaps	%xmm0, CONFIG_EMULATE_HARDWARE(%rsi)
0000000100992a5a	xorl	%eax, %eax
0000000100992a5c	movb	%al, 0x20(%rsi)
0000000100992a5f	leaq	-0xa0(%rbp), %rdx
0000000100992a66	movb	%al, 0x20(%rdx)
0000000100992a69	movaps	%xmm0, 0x10(%rdx)
0000000100992a6d	movaps	%xmm0, CONFIG_EMULATE_HARDWARE(%rdx)
0000000100992a70	movq	%r14, %rdi
0000000100992a73	callq	__ZN18IParamValuesAction9getValuesEP12SActionParamS1_ ## IParamValuesAction::getValues(SActionParam*, SActionParam*)
0000000100992a78	movl	%eax, %r15d
0000000100992a7b	testl	%eax, %eax
0000000100992a7d	jne	0x100992b97
0000000100992a83	cmpl	$0x747874, -0xd0(%rbp)          ## imm = 0x747874
0000000100992a8d	je	0x100992ad1
0000000100992a8f	cmpl	$0x747874, -0xa0(%rbp)          ## imm = 0x747874
0000000100992a99	je	0x100992ad1
0000000100992a9b	leaq	-0xd0(%rbp), %rdi
0000000100992aa2	callq	__ZN12SActionParam7toFloatEv    ## SActionParam::toFloat()
0000000100992aa7	movss	%xmm0, -0x48(%rbp)
0000000100992aac	leaq	-0xa0(%rbp), %rdi
0000000100992ab3	callq	__ZN12SActionParam7toFloatEv    ## SActionParam::toFloat()
0000000100992ab8	addss	-0x48(%rbp), %xmm0
0000000100992abd	movl	$0x76616c, CONFIG_EMULATE_HARDWARE(%rbx) ## imm = 0x76616C
0000000100992ac3	movss	%xmm0, 0x4(%rbx)
0000000100992ac8	movb	$0x0, 0x20(%rbx)
0000000100992acc	jmp	0x100992b97
0000000100992ad1	leaq	-0x78(%rbp), %rdi
0000000100992ad5	leaq	-0xd0(%rbp), %rsi
0000000100992adc	callq	__ZN7IAction13paramToStringEP12SActionParam ## IAction::paramToString(SActionParam*)
0000000100992ae1	leaq	-0x60(%rbp), %rdi
0000000100992ae5	leaq	-0xa0(%rbp), %rsi
0000000100992aec	callq	__ZN7IAction13paramToStringEP12SActionParam ## IAction::paramToString(SActionParam*)
0000000100992af1	movzbl	-0x60(%rbp), %edx
0000000100992af5	testb	$0x1, %dl
0000000100992af8	je	0x100992b04
0000000100992afa	movq	-0x50(%rbp), %rsi
0000000100992afe	movq	-0x58(%rbp), %rdx
0000000100992b02	jmp	0x100992b0a
0000000100992b04	shrl	%edx
0000000100992b06	leaq	-0x5f(%rbp), %rsi
0000000100992b0a	leaq	-0x78(%rbp), %rdi
0000000100992b0e	callq	0x104fe8516                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm
0000000100992b13	movb	CONFIG_EMULATE_HARDWARE(%rax), %r12b
0000000100992b16	movb	0x1(%rax), %r13b
0000000100992b1a	movq	0x8(%rax), %rcx
0000000100992b1e	movq	%rcx, -0x3a(%rbp)
0000000100992b22	movq	0x2(%rax), %rcx
0000000100992b26	movq	%rcx, -0x40(%rbp)
0000000100992b2a	movq	0x10(%rax), %rdx
0000000100992b2e	xorps	%xmm0, %xmm0
0000000100992b31	movups	%xmm0, CONFIG_EMULATE_HARDWARE(%rax)
0000000100992b34	movq	$CONFIG_EMULATE_HARDWARE, 0x10(%rax)
0000000100992b3c	movl	$0x747874, CONFIG_EMULATE_HARDWARE(%rbx) ## imm = 0x747874
0000000100992b42	testb	$0x1, 0x8(%rbx)
0000000100992b46	je	0x100992b59
0000000100992b48	movq	0x18(%rbx), %rdi
0000000100992b4c	movq	%rdx, -0x48(%rbp)
0000000100992b50	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
0000000100992b55	movq	-0x48(%rbp), %rdx
0000000100992b59	movb	%r12b, 0x8(%rbx)
0000000100992b5d	movb	%r13b, 0x9(%rbx)
0000000100992b61	movq	-0x40(%rbp), %rax
0000000100992b65	movq	-0x3a(%rbp), %rcx
0000000100992b69	movq	%rax, 0xa(%rbx)
0000000100992b6d	movq	%rcx, 0x10(%rbx)
0000000100992b71	movq	%rdx, 0x18(%rbx)
0000000100992b75	movb	$0x0, 0x20(%rbx)
0000000100992b79	testb	$0x1, -0x60(%rbp)
0000000100992b7d	je	0x100992b88
0000000100992b7f	movq	-0x50(%rbp), %rdi
0000000100992b83	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
0000000100992b88	testb	$0x1, -0x78(%rbp)
0000000100992b8c	je	0x100992b97
0000000100992b8e	movq	-0x68(%rbp), %rdi
0000000100992b92	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
0000000100992b97	testb	$0x1, -0x98(%rbp)
0000000100992b9e	je	0x100992bac
0000000100992ba0	movq	-0x88(%rbp), %rdi
0000000100992ba7	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
0000000100992bac	testb	$0x1, -0xc8(%rbp)
0000000100992bb3	je	0x100992bc1
0000000100992bb5	movq	-0xb8(%rbp), %rdi
0000000100992bbc	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
0000000100992bc1	testl	%r15d, %r15d
0000000100992bc4	je	0x100992d3b
0000000100992bca	movq	0x20(%r14), %rsi
0000000100992bce	movl	CONFIG_EMULATE_HARDWARE(%rsi), %ecx
0000000100992bd0	xorps	%xmm1, %xmm1
0000000100992bd3	xorl	%edx, %edx
0000000100992bd5	cmpl	$0x696e73, %ecx                 ## imm = 0x696E73
0000000100992bdb	jg	0x100992bf4
0000000100992bdd	cmpl	$0x25, %ecx
0000000100992be0	je	0x100992c18
0000000100992be2	cmpl	$0x6274, %ecx                   ## imm = 0x6274
0000000100992be8	je	0x100992c18
0000000100992bea	cmpl	$0x6d73, %ecx                   ## imm = 0x6D73
0000000100992bf0	je	0x100992c18
0000000100992bf2	jmp	0x100992c1f
0000000100992bf4	cmpl	$0x626f6f6c, %ecx               ## imm = 0x626F6F6C
0000000100992bfa	je	0x100992c0c
0000000100992bfc	cmpl	$0x76616c, %ecx                 ## imm = 0x76616C
0000000100992c02	je	0x100992c18
0000000100992c04	cmpl	$0x696e74, %ecx                 ## imm = 0x696E74
0000000100992c0a	jne	0x100992c1f
0000000100992c0c	xorps	%xmm1, %xmm1
0000000100992c0f	cvtsi2ssl	0x4(%rsi), %xmm1
0000000100992c14	xorl	%edx, %edx
0000000100992c16	jmp	0x100992c1f
0000000100992c18	movss	0x4(%rsi), %xmm1
0000000100992c1d	movb	$0x1, %dl
0000000100992c1f	movq	0x68(%r14), %rdi
0000000100992c23	testq	%rdi, %rdi
0000000100992c26	je	0x100992c99
0000000100992c28	movl	CONFIG_EMULATE_HARDWARE(%rdi), %r8d
0000000100992c2b	testl	%r8d, %r8d
0000000100992c2e	je	0x100992c99
0000000100992c30	movq	0x38(%r14), %rax
0000000100992c34	testq	%rax, %rax
0000000100992c37	je	0x100992c3d
0000000100992c39	andb	$-0x5, 0x17(%rax)
0000000100992c3d	movl	$CONFIG_VP9, %eax
0000000100992c42	cmpl	$0x696e73, %r8d                 ## imm = 0x696E73
0000000100992c49	jle	0x100992cd5
0000000100992c4f	cmpl	$0x76616b, %r8d                 ## imm = 0x76616B
0000000100992c56	jg	0x100992cef
0000000100992c5c	cmpl	$0x696e74, %r8d                 ## imm = 0x696E74
0000000100992c63	je	0x100992d01
0000000100992c69	cmpl	$0x747874, %r8d                 ## imm = 0x747874
0000000100992c70	jne	0x100992d3d
0000000100992c76	movl	$0x80070057, %eax               ## imm = 0x80070057
0000000100992c7b	cmpl	$0x747874, %ecx                 ## imm = 0x747874
0000000100992c81	jne	0x100992d3d
0000000100992c87	addq	$0x8, %rdi
0000000100992c8b	addq	$0x8, %rsi
0000000100992c8f	callq	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendB8ne200100ERKS5_ ## std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>::append[abi:ne200100](std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&)
0000000100992c94	jmp	0x100992d3b
0000000100992c99	movq	0x38(%r14), %rdi
0000000100992c9d	testq	%rdi, %rdi
0000000100992ca0	je	0x100992cce
0000000100992ca2	movss	%xmm1, -0x48(%rbp)
0000000100992ca7	orb	$0x4, 0x17(%rdi)
0000000100992cab	movl	0x5c(%r14), %esi
0000000100992caf	movq	0x50(%r14), %rdx
0000000100992cb3	callq	__ZN7IAction10queryValueEjP11IController ## IAction::queryValue(unsigned int, IController*)
0000000100992cb8	subss	-0x48(%rbp), %xmm0
0000000100992cbd	movl	$0x76616c, CONFIG_EMULATE_HARDWARE(%rbx) ## imm = 0x76616C
0000000100992cc3	movss	%xmm0, 0x4(%rbx)
0000000100992cc8	movb	$0x0, 0x20(%rbx)
0000000100992ccc	jmp	0x100992d3b
0000000100992cce	movl	$CONFIG_VP9, %eax
0000000100992cd3	jmp	0x100992d3d
0000000100992cd5	cmpl	$0x25, %r8d
0000000100992cd9	je	0x100992d1e
0000000100992cdb	cmpl	$0x6274, %r8d                   ## imm = 0x6274
0000000100992ce2	je	0x100992d1e
0000000100992ce4	cmpl	$0x6d73, %r8d                   ## imm = 0x6D73
0000000100992ceb	je	0x100992d1e
0000000100992ced	jmp	0x100992d3d
0000000100992cef	cmpl	$0x76616c, %r8d                 ## imm = 0x76616C
0000000100992cf6	je	0x100992d1e
0000000100992cf8	cmpl	$0x626f6f6c, %r8d               ## imm = 0x626F6F6C
0000000100992cff	jne	0x100992d3d
0000000100992d01	xorps	%xmm0, %xmm0
0000000100992d04	cvtsi2ssl	0x4(%rdi), %xmm0
0000000100992d09	addss	%xmm0, %xmm1
0000000100992d0d	testb	%dl, %dl
0000000100992d0f	je	0x100992d2a
0000000100992d11	movl	$0x76616c, CONFIG_EMULATE_HARDWARE(%rdi) ## imm = 0x76616C
0000000100992d17	movss	%xmm1, 0x4(%rdi)
0000000100992d1c	jmp	0x100992d37
0000000100992d1e	addss	0x4(%rdi), %xmm1
0000000100992d23	movss	%xmm1, 0x4(%rdi)
0000000100992d28	jmp	0x100992d3b
0000000100992d2a	cvttss2si	%xmm1, %eax
0000000100992d2e	movl	$0x696e74, CONFIG_EMULATE_HARDWARE(%rdi) ## imm = 0x696E74
0000000100992d34	movl	%eax, 0x4(%rdi)
0000000100992d37	movb	$0x0, 0x20(%rdi)
0000000100992d3b	xorl	%eax, %eax
0000000100992d3d	movq	0x4e2d2e4(%rip), %rcx           ## literal pool symbol address: ___stack_chk_guard
0000000100992d44	movq	CONFIG_EMULATE_HARDWARE(%rcx), %rcx
0000000100992d47	cmpq	-0x30(%rbp), %rcx
0000000100992d4b	jne	0x100992d5f
0000000100992d4d	addq	$rf.rp_ref, %rsp
0000000100992d54	popq	%rbx
0000000100992d55	popq	%r12
0000000100992d57	popq	%r13
0000000100992d59	popq	%r14
0000000100992d5b	popq	%r15
0000000100992d5d	popq	%rbp
0000000100992d5e	retq
0000000100992d5f	callq	0x104fe882e                     ## symbol stub for: ___stack_chk_fail
0000000100992d64	movq	%rax, %rbx
0000000100992d67	testb	$0x1, -0x60(%rbp)
0000000100992d6b	je	0x100992d7b
0000000100992d6d	movq	-0x50(%rbp), %rdi
0000000100992d71	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
0000000100992d76	jmp	0x100992d7b
0000000100992d78	movq	%rax, %rbx
0000000100992d7b	testb	$0x1, -0x78(%rbp)
0000000100992d7f	je	0x100992d96
0000000100992d81	movq	-0x68(%rbp), %rdi
0000000100992d85	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
0000000100992d8a	jmp	0x100992d96
0000000100992d8c	jmp	0x100992d93
0000000100992d8e	movq	%rax, %rbx
0000000100992d91	jmp	0x100992dc0
0000000100992d93	movq	%rax, %rbx
0000000100992d96	testb	$0x1, -0x98(%rbp)
0000000100992d9d	je	0x100992dab
0000000100992d9f	movq	-0x88(%rbp), %rdi
0000000100992da6	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
0000000100992dab	testb	$0x1, -0xc8(%rbp)
0000000100992db2	je	0x100992dc0
0000000100992db4	movq	-0xb8(%rbp), %rdi
0000000100992dbb	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
0000000100992dc0	movq	%rbx, %rdi
0000000100992dc3	callq	0x104fe8456                     ## symbol stub for: __Unwind_Resume
