__ZN15ACTION_get_text7onQueryER12SActionParam [0x100425bac, 0x100425d10):
0000000100425bac	pushq	%rbp
0000000100425bad	movq	%rsp, %rbp
0000000100425bb0	pushq	%r15
0000000100425bb2	pushq	%r14
0000000100425bb4	pushq	%r13
0000000100425bb6	pushq	%r12
0000000100425bb8	pushq	%rbx
0000000100425bb9	pushq	%rax
0000000100425bba	movq	%rsi, %rbx
0000000100425bbd	movq	%rdi, %r14
0000000100425bc0	xorl	%r15d, %r15d
0000000100425bc3	xorl	%esi, %esi
0000000100425bc5	callq	__ZN7IAction8getParamEi         ## IAction::getParam(int)
0000000100425bca	movl	CONFIG_EMULATE_HARDWARE(%rax), %ecx
0000000100425bcc	cmpl	$0x747874, %ecx                 ## imm = 0x747874
0000000100425bd2	je	0x100425c0a
0000000100425bd4	cmpl	$0x696e74, %ecx                 ## imm = 0x696E74
0000000100425bda	jne	0x100425be0
0000000100425bdc	movl	0x4(%rax), %r15d
0000000100425be0	movq	0x60(%r14), %rdi
0000000100425be4	leaq	0x8(%rbx), %rsi
0000000100425be8	movl	%r15d, %edx
0000000100425beb	callq	__ZN5CDeck17getControllerTextERNSt3__112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEEi ## CDeck::getControllerText(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>&, int)
0000000100425bf0	movl	%eax, %ecx
0000000100425bf2	movl	$0x80070057, %eax               ## imm = 0x80070057
0000000100425bf7	testb	%cl, %cl
0000000100425bf9	je	0x100425d00
0000000100425bff	movl	$0x747874, CONFIG_EMULATE_HARDWARE(%rbx) ## imm = 0x747874
0000000100425c05	jmp	0x100425cfe
0000000100425c0a	movq	%rax, %r12
0000000100425c0d	movl	$0x747874, CONFIG_EMULATE_HARDWARE(%rbx) ## imm = 0x747874
0000000100425c13	testb	$0x1, 0x8(%rax)
0000000100425c17	jne	0x100425c20
0000000100425c19	leaq	0x9(%r12), %r15
0000000100425c1e	jmp	0x100425c24
0000000100425c20	movq	0x18(%rax), %r15
0000000100425c24	addq	$0x8, %r12
0000000100425c28	testb	$0x1, 0x8(%rbx)
0000000100425c2c	jne	0x100425c36
0000000100425c2e	movw	$CONFIG_EMULATE_HARDWARE, 0x8(%rbx)
0000000100425c34	jmp	0x100425c45
0000000100425c36	movq	0x18(%rbx), %rcx
0000000100425c3a	movb	$0x0, CONFIG_EMULATE_HARDWARE(%rcx)
0000000100425c3d	movq	$CONFIG_EMULATE_HARDWARE, 0x10(%rbx)
0000000100425c45	addq	$0x8, %rbx
0000000100425c49	movzbl	CONFIG_EMULATE_HARDWARE(%r12), %esi
0000000100425c4e	testb	$0x1, %sil
0000000100425c52	jne	0x100425c58
0000000100425c54	shrl	%esi
0000000100425c56	jmp	0x100425c5c
0000000100425c58	movq	0x10(%rax), %rsi
0000000100425c5c	movq	%rbx, %rdi
0000000100425c5f	callq	0x104fe8546                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE7reserveEm
0000000100425c64	cmpl	$0x6175746f, 0x5c(%r14)         ## imm = 0x6175746F
0000000100425c6c	jne	0x100425c7b
0000000100425c6e	leaq	_autoMix(%rip), %rax
0000000100425c75	addq	$0x10, %rax
0000000100425c79	jmp	0x100425c84
0000000100425c7b	movl	$0x6c8, %eax                    ## imm = 0x6C8
0000000100425c80	addq	0x60(%r14), %rax
0000000100425c84	movq	CONFIG_EMULATE_HARDWARE(%rax), %r13
0000000100425c87	cmpl	$0x0, 0x78(%r14)
0000000100425c8c	jne	0x100425cd1
0000000100425c8e	movq	%r12, %rdi
0000000100425c91	movl	$FGData.ar_coeffs_y, %esi
0000000100425c96	xorl	%edx, %edx
0000000100425c98	callq	0x104fe8474                     ## symbol stub for: __ZNKSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE4findEcm
0000000100425c9d	cmpq	$-0x1, %rax
0000000100425ca1	je	0x100425cc9
0000000100425ca3	movl	$CONFIG_VP9, 0x78(%r14)
0000000100425cab	movl	$rf.sbsz, %edi
0000000100425cb0	callq	0x104fe8750                     ## symbol stub for: __Znwm
0000000100425cb5	xorps	%xmm0, %xmm0
0000000100425cb8	movups	%xmm0, CONFIG_EMULATE_HARDWARE(%rax)
0000000100425cbb	movq	$CONFIG_EMULATE_HARDWARE, 0x10(%rax)
0000000100425cc3	movq	%rax, 0x70(%r14)
0000000100425cc7	jmp	0x100425cd1
0000000100425cc9	movl	$0xffffffff, 0x78(%r14)         ## imm = 0xFFFFFFFF
0000000100425cd1	movq	0x60(%r14), %r8
0000000100425cd5	movq	0x6b8(%r8), %rdi
0000000100425cdc	movl	0x5c(%r14), %ecx
0000000100425ce0	subq	$0x8, %rsp
0000000100425ce4	movq	%r15, %rsi
0000000100425ce7	movq	%rbx, %rdx
0000000100425cea	movq	%r13, %r9
0000000100425ced	pushq	0x70(%r14)
0000000100425cf1	pushq	%r14
0000000100425cf3	pushq	$0x1
0000000100425cf5	callq	__Z13actionGetTextP7SDBInfoPKcPNSt3__112basic_stringIcNS3_11char_traitsIcEENS3_9allocatorIcEEEEiP5CDeckP5CSongbP7IActionPNS3_6vectorIP16SActionCacheItemNS7_ISJ_EEEE ## actionGetText(SDBInfo*, char const*, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>*, int, CDeck*, CSong*, bool, IAction*, std::__1::vector<SActionCacheItem*, std::__1::allocator<SActionCacheItem*>>*)
0000000100425cfa	addq	$0x20, %rsp
0000000100425cfe	xorl	%eax, %eax
0000000100425d00	addq	$0x8, %rsp
0000000100425d04	popq	%rbx
0000000100425d05	popq	%r12
0000000100425d07	popq	%r13
0000000100425d09	popq	%r14
0000000100425d0b	popq	%r15
0000000100425d0d	popq	%rbp
0000000100425d0e	retq
0000000100425d0f	nop
