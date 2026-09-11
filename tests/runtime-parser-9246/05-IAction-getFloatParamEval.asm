__ZN7IAction17getFloatParamEvalEmRfP16SActionCacheItemPj [0x100596cb2, 0x100596f1c):
0000000100596cb2	pushq	%rbp
0000000100596cb3	movq	%rsp, %rbp
0000000100596cb6	pushq	%r15
0000000100596cb8	pushq	%r14
0000000100596cba	pushq	%r13
0000000100596cbc	pushq	%r12
0000000100596cbe	pushq	%rbx
0000000100596cbf	subq	$0x38, %rsp
0000000100596cc3	movq	%rcx, %r13
0000000100596cc6	movq	%rdx, %r14
0000000100596cc9	movq	0x20(%rdi), %rax
0000000100596ccd	movq	0x28(%rdi), %rcx
0000000100596cd1	subq	%rax, %rcx
0000000100596cd4	sarq	$0x3, %rcx
0000000100596cd8	movabsq	$-0x3333333333333333, %rdx      ## imm = 0xCCCCCCCCCCCCCCCD
0000000100596ce2	imulq	%rcx, %rdx
0000000100596ce6	cmpq	%rsi, %rdx
0000000100596ce9	jb	0x100596eb3
0000000100596cef	movq	%r8, %rbx
0000000100596cf2	movq	%rdi, %r15
0000000100596cf5	jne	0x100596d0b
0000000100596cf7	movq	0x68(%r15), %rax
0000000100596cfb	testq	%rax, %rax
0000000100596cfe	leaq	_staticNullParam(%rip), %r12
0000000100596d05	cmovneq	%rax, %r12
0000000100596d09	jmp	0x100596d13
0000000100596d0b	leaq	CONFIG_EMULATE_HARDWARE(%rsi,%rsi,4), %rcx
0000000100596d0f	leaq	CONFIG_EMULATE_HARDWARE(%rax,%rcx,8), %r12
0000000100596d13	movl	CONFIG_EMULATE_HARDWARE(%r12), %eax
0000000100596d17	cmpl	$0x747874, %eax                 ## imm = 0x747874
0000000100596d1c	jne	0x100596d51
0000000100596d1e	movq	%rbx, -0x30(%rbp)
0000000100596d22	leaq	0x8(%r12), %rbx
0000000100596d27	leaq	0x5050bd8(%rip), %rsi           ## literal pool for: "`"
0000000100596d2e	movq	%rbx, %rdi
0000000100596d31	callq	__Z8isLeftCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## isLeftCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
0000000100596d36	testb	%al, %al
0000000100596d38	je	0x100596d49
0000000100596d3a	movzbl	(%r13), %eax
0000000100596d3f	testb	$0x1, %al
0000000100596d41	je	0x100596d89
0000000100596d43	movq	0x8(%r13), %rdx
0000000100596d47	jmp	0x100596d8d
0000000100596d49	movl	CONFIG_EMULATE_HARDWARE(%r12), %eax
0000000100596d4d	movq	-0x30(%rbp), %rbx
0000000100596d51	testl	%eax, %eax
0000000100596d53	je	0x100596eb3
0000000100596d59	movq	%r12, %rdi
0000000100596d5c	callq	__ZN12SActionParam7toFloatEv    ## SActionParam::toFloat()
0000000100596d61	cmpb	$0x0, 0x20(%r12)
0000000100596d67	je	0x100596d6e
0000000100596d69	addss	CONFIG_EMULATE_HARDWARE(%r14), %xmm0
0000000100596d6e	movss	%xmm0, CONFIG_EMULATE_HARDWARE(%r14)
0000000100596d73	movb	$0x1, %al
0000000100596d75	testq	%rbx, %rbx
0000000100596d78	je	0x100596eb5
0000000100596d7e	movl	CONFIG_EMULATE_HARDWARE(%r12), %ecx
0000000100596d82	movl	%ecx, CONFIG_EMULATE_HARDWARE(%rbx)
0000000100596d84	jmp	0x100596eb5
0000000100596d89	movl	%eax, %edx
0000000100596d8b	shrl	%edx
0000000100596d8d	movzbl	0x8(%r12), %ecx
0000000100596d93	testb	$0x1, %cl
0000000100596d96	je	0x100596d9f
0000000100596d98	movq	0x10(%r12), %rsi
0000000100596d9d	jmp	0x100596da3
0000000100596d9f	movl	%ecx, %esi
0000000100596da1	shrl	%esi
0000000100596da3	cmpq	%rsi, %rdx
0000000100596da6	jne	0x100596dd4
0000000100596da8	testb	$0x1, %al
0000000100596daa	je	0x100596db2
0000000100596dac	movq	0x10(%r13), %rdi
0000000100596db0	jmp	0x100596db6
0000000100596db2	leaq	0x1(%r13), %rdi
0000000100596db6	testb	$0x1, %cl
0000000100596db9	je	0x100596dc2
0000000100596dbb	movq	0x18(%r12), %rsi
0000000100596dc0	jmp	0x100596dc7
0000000100596dc2	leaq	0x9(%r12), %rsi
0000000100596dc7	callq	0x104fe8eca                     ## symbol stub for: _memcmp
0000000100596dcc	testl	%eax, %eax
0000000100596dce	je	0x100596e75
0000000100596dd4	movq	%r13, %rdi
0000000100596dd7	movq	%rbx, %rsi
0000000100596dda	callq	0x104fe856a                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
0000000100596ddf	movb	CONFIG_EMULATE_HARDWARE(%rbx), %al
0000000100596de1	testb	$0x1, %al
0000000100596de3	jne	0x100596df9
0000000100596de5	movzbl	%al, %ecx
0000000100596de8	shrl	%ecx
0000000100596dea	cmpb	$0x60, 0x8(%r12,%rcx)
0000000100596df0	jne	0x100596e11
0000000100596df2	leaq	0x9(%r12), %rdx
0000000100596df7	jmp	0x100596e0a
0000000100596df9	movq	0x10(%r12), %rcx
0000000100596dfe	movq	0x18(%r12), %rdx
0000000100596e03	cmpb	$0x60, -0x1(%rdx,%rcx)
0000000100596e08	jne	0x100596e11
0000000100596e0a	movb	$0x0, -0x1(%rdx,%rcx)
0000000100596e0f	movb	CONFIG_EMULATE_HARDWARE(%rbx), %al
0000000100596e11	testb	$0x1, %al
0000000100596e13	jne	0x100596e1c
0000000100596e15	leaq	0x9(%r12), %rdi
0000000100596e1a	jmp	0x100596e21
0000000100596e1c	movq	0x18(%r12), %rdi
0000000100596e21	incq	%rdi
0000000100596e24	xorl	%esi, %esi
0000000100596e26	xorl	%edx, %edx
0000000100596e28	callq	__ZN7IAction6createEPKcPS1_i    ## IAction::create(char const*, char const**, int)
0000000100596e2d	movq	0x18(%r13), %rdi
0000000100596e31	movq	%rax, 0x18(%r13)
0000000100596e35	testq	%rdi, %rdi
0000000100596e38	je	0x100596e46
0000000100596e3a	lock
0000000100596e3b	decl	0x8(%rdi)
0000000100596e3e	jg	0x100596e46
0000000100596e40	movq	CONFIG_EMULATE_HARDWARE(%rdi), %rax
0000000100596e43	callq	*0x8(%rax)
0000000100596e46	movzbl	CONFIG_EMULATE_HARDWARE(%rbx), %eax
0000000100596e49	testb	$0x1, %al
0000000100596e4b	jne	0x100596e5d
0000000100596e4d	shrl	%eax
0000000100596e4f	cmpb	$0x0, 0x8(%r12,%rax)
0000000100596e55	jne	0x100596e75
0000000100596e57	addq	$0x9, %r12
0000000100596e5b	jmp	0x100596e6f
0000000100596e5d	movq	0x10(%r12), %rax
0000000100596e62	movq	0x18(%r12), %r12
0000000100596e67	cmpb	$0x0, -0x1(%r12,%rax)
0000000100596e6d	jne	0x100596e75
0000000100596e6f	movb	$0x60, -0x1(%r12,%rax)
0000000100596e75	movq	0x18(%r13), %rdi
0000000100596e79	testq	%rdi, %rdi
0000000100596e7c	je	0x100596eb3
0000000100596e7e	xorps	%xmm0, %xmm0
0000000100596e81	leaq	-0x60(%rbp), %rsi
0000000100596e85	movaps	%xmm0, 0x10(%rsi)
0000000100596e89	movaps	%xmm0, CONFIG_EMULATE_HARDWARE(%rsi)
0000000100596e8c	movb	$0x0, 0x20(%rsi)
0000000100596e90	movl	0x5c(%r15), %edx
0000000100596e94	movq	0x50(%r15), %rcx
0000000100596e98	xorl	%r8d, %r8d
0000000100596e9b	callq	__ZN7IAction5queryER12SActionParamjP11IControllerj ## IAction::query(SActionParam&, unsigned int, IController*, unsigned int)
0000000100596ea0	testl	%eax, %eax
0000000100596ea2	je	0x100596ec4
0000000100596ea4	testb	$0x1, -0x58(%rbp)
0000000100596ea8	je	0x100596eb3
0000000100596eaa	movq	-0x48(%rbp), %rdi
0000000100596eae	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
0000000100596eb3	xorl	%eax, %eax
0000000100596eb5	addq	$0x38, %rsp
0000000100596eb9	popq	%rbx
0000000100596eba	popq	%r12
0000000100596ebc	popq	%r13
0000000100596ebe	popq	%r14
0000000100596ec0	popq	%r15
0000000100596ec2	popq	%rbp
0000000100596ec3	retq
0000000100596ec4	leaq	-0x60(%rbp), %rbx
0000000100596ec8	movq	%rbx, %rdi
0000000100596ecb	callq	__ZN12SActionParam7toFloatEv    ## SActionParam::toFloat()
0000000100596ed0	cmpb	$0x0, 0x20(%rbx)
0000000100596ed4	je	0x100596edb
0000000100596ed6	addss	CONFIG_EMULATE_HARDWARE(%r14), %xmm0
0000000100596edb	movq	-0x30(%rbp), %rcx
0000000100596edf	movss	%xmm0, CONFIG_EMULATE_HARDWARE(%r14)
0000000100596ee4	testq	%rcx, %rcx
0000000100596ee7	je	0x100596eee
0000000100596ee9	movl	-0x60(%rbp), %eax
0000000100596eec	movl	%eax, CONFIG_EMULATE_HARDWARE(%rcx)
0000000100596eee	testb	$0x1, -0x58(%rbp)
0000000100596ef2	je	0x100596efd
0000000100596ef4	movq	-0x48(%rbp), %rdi
0000000100596ef8	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
0000000100596efd	movb	$0x1, %al
0000000100596eff	jmp	0x100596eb5
0000000100596f01	movq	%rax, %rbx
0000000100596f04	testb	$0x1, -0x58(%rbp)
0000000100596f08	je	0x100596f13
0000000100596f0a	movq	-0x48(%rbp), %rdi
0000000100596f0e	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
0000000100596f13	movq	%rbx, %rdi
0000000100596f16	callq	0x104fe8456                     ## symbol stub for: __Unwind_Resume
0000000100596f1b	nop
