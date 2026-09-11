__ZN15DLGActionWizard10updateListEv [0x1006c5830, 0x1006c6136):
00000001006c5830	pushq	%rbp
00000001006c5831	movq	%rsp, %rbp
00000001006c5834	pushq	%r15
00000001006c5836	pushq	%r14
00000001006c5838	pushq	%r13
00000001006c583a	pushq	%r12
00000001006c583c	pushq	%rbx
00000001006c583d	subq	$FGData.grain_scale_shift, %rsp
00000001006c5844	movq	%rdi, %rbx
00000001006c5847	leaq	0x5c8(%rdi), %r14
00000001006c584e	movq	%r14, %rdi
00000001006c5851	callq	__ZN15DLGActionWizard5STree5clearEv ## DLGActionWizard::STree::clear()
00000001006c5856	xorps	%xmm0, %xmm0
00000001006c5859	movaps	%xmm0, 0x610(%rbx)
00000001006c5860	movaps	%xmm0, -0x90(%rbp)
00000001006c5867	movq	$CONFIG_EMULATE_HARDWARE, -0x80(%rbp)
00000001006c586f	movl	$CONFIG_EMULATE_HARDWARE, 0x638(%rbx)
00000001006c5879	movq	%rbx, %rdi
00000001006c587c	callq	__ZN7DLGEdit13getLineHeightEv   ## DLGEdit::getLineHeight()
00000001006c5881	movq	%rax, -0xb8(%rbp)
00000001006c5888	testb	$0x1, 0x138(%rbx)
00000001006c588f	jne	0x1006c589a
00000001006c5891	leaq	0x139(%rbx), %rcx
00000001006c5898	jmp	0x1006c58a1
00000001006c589a	movq	0x148(%rbx), %rcx
00000001006c58a1	leaq	0x138(%rbx), %rax
00000001006c58a8	movq	%rax, -0xa8(%rbp)
00000001006c58af	leaq	0x160(%rbx), %rax
00000001006c58b6	movq	%rax, -0xd8(%rbp)
00000001006c58bd	movq	%rbx, -0x68(%rbp)
00000001006c58c1	leaq	0x139(%rbx), %rax
00000001006c58c8	movq	%rax, -0xa0(%rbp)
00000001006c58cf	movl	$CONFIG_EMULATE_HARDWARE, -0x5c(%rbp)
00000001006c58d6	movl	$CONFIG_EMULATE_HARDWARE, -0x3c(%rbp)
00000001006c58dd	xorl	%r12d, %r12d
00000001006c58e0	movq	%rcx, %r13
00000001006c58e3	movq	%rcx, -0xb0(%rbp)
00000001006c58ea	movq	%rcx, -0x50(%rbp)
00000001006c58ee	movq	$CONFIG_EMULATE_HARDWARE, -0x98(%rbp)
00000001006c58f9	xorl	%ebx, %ebx
00000001006c58fb	movq	$CONFIG_EMULATE_HARDWARE, -0x58(%rbp)
00000001006c5903	movq	%rbx, -0x70(%rbp)
00000001006c5907	movzbl	%r12b, %eax
00000001006c590b	movl	%eax, -0x40(%rbp)
00000001006c590e	testb	%r12b, %r12b
00000001006c5911	je	0x1006c5932
00000001006c5913	leaq	-0x1(%r13), %rbx
00000001006c5917	movzbl	(%r13), %ecx
00000001006c591c	testl	%ecx, %ecx
00000001006c591e	je	0x1006c5995
00000001006c5920	cmpl	$0xa, %ecx
00000001006c5923	je	0x1006c5995
00000001006c5925	cmpb	%r12b, %cl
00000001006c5928	je	0x1006c5992
00000001006c592a	incq	%r13
00000001006c592d	incq	%rbx
00000001006c5930	jmp	0x1006c5917
00000001006c5932	leaq	-0x1(%r13), %rax
00000001006c5936	incq	%r13
00000001006c5939	movq	%r13, %rbx
00000001006c593c	movb	0x1(%rax), %r15b
00000001006c5940	incq	%rax
00000001006c5943	incq	%r13
00000001006c5946	cmpb	$0x20, %r15b
00000001006c594a	je	0x1006c5939
00000001006c594c	movq	-0xb0(%rbp), %r13
00000001006c5953	movzbl	%r15b, %eax
00000001006c5957	cmpb	$0x3f, %al
00000001006c5959	ja	0x1006c5985
00000001006c595b	movabsq	$-0x7bfffcc000000000, %rcx      ## imm = 0x8400034000000000
00000001006c5965	btq	%rax, %rcx
00000001006c5969	jb	0x1006c5cc9
00000001006c596f	movabsq	$0x8400000401, %rcx             ## imm = 0x8400000401
00000001006c5979	btq	%rax, %rcx
00000001006c597d	jb	0x1006c59c3
00000001006c597f	cmpq	$0x20, %rax
00000001006c5983	je	0x1006c59c6
00000001006c5985	cmpl	$0x60, %eax
00000001006c5988	je	0x1006c59c3
00000001006c598a	movb	CONFIG_EMULATE_HARDWARE(%rbx), %r15b
00000001006c598d	incq	%rbx
00000001006c5990	jmp	0x1006c5953
00000001006c5992	movl	%r12d, %ecx
00000001006c5995	xorl	%eax, %eax
00000001006c5997	cmpb	%r12b, %cl
00000001006c599a	sete	%al
00000001006c599d	movl	$CONFIG_EMULATE_HARDWARE, %ecx
00000001006c59a2	cmovel	-0x40(%rbp), %ecx
00000001006c59a6	movq	-0xb0(%rbp), %r13
00000001006c59ad	cmpb	$0x20, 0x1(%rbx,%rax)
00000001006c59b2	leaq	0x1(%rbx), %rbx
00000001006c59b6	je	0x1006c59ad
00000001006c59b8	movsbl	%cl, %ecx
00000001006c59bb	movl	%ecx, -0x44(%rbp)
00000001006c59be	addq	%rax, %rbx
00000001006c59c1	jmp	0x1006c59cd
00000001006c59c3	decq	%rbx
00000001006c59c6	movl	$CONFIG_EMULATE_HARDWARE, -0x44(%rbp)
00000001006c59cd	xorl	%r15d, %r15d
00000001006c59d0	movl	$0x48, %edi
00000001006c59d5	callq	0x104fe8750                     ## symbol stub for: __Znwm
00000001006c59da	xorps	%xmm0, %xmm0
00000001006c59dd	movups	%xmm0, 0x30(%rax)
00000001006c59e1	movups	%xmm0, 0x20(%rax)
00000001006c59e5	movups	%xmm0, 0x10(%rax)
00000001006c59e9	movups	%xmm0, CONFIG_EMULATE_HARDWARE(%rax)
00000001006c59ec	movq	$CONFIG_EMULATE_HARDWARE, 0x40(%rax)
00000001006c59f4	movq	%rax, -0x38(%rbp)
00000001006c59f8	movq	-0x98(%rbp), %rcx
00000001006c59ff	movl	%ecx, 0x4(%rax)
00000001006c5a02	movq	%rbx, %rcx
00000001006c5a05	movq	-0x50(%rbp), %rdx
00000001006c5a09	subq	%rdx, %rcx
00000001006c5a0c	subq	%r13, %rdx
00000001006c5a0f	movl	%edx, 0x30(%rax)
00000001006c5a12	leaq	-0xd0(%rbp), %rdi
00000001006c5a19	movq	-0xa8(%rbp), %rsi
00000001006c5a20	leaq	-0x74(%rbp), %r8
00000001006c5a24	callq	0x104fe855e                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEC2ERKS5_mmRKS4_
00000001006c5a29	movq	-0x38(%rbp), %r13
00000001006c5a2d	testb	$0x1, 0x18(%r13)
00000001006c5a32	movq	%r13, %rsi
00000001006c5a35	je	0x1006c5a44
00000001006c5a37	movq	0x28(%r13), %rdi
00000001006c5a3b	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
00000001006c5a40	movq	-0x38(%rbp), %rsi
00000001006c5a44	addq	$0x18, %r13
00000001006c5a48	movq	-0xc0(%rbp), %rax
00000001006c5a4f	movq	%rax, 0x10(%r13)
00000001006c5a53	movups	-0xd0(%rbp), %xmm0
00000001006c5a5a	movups	%xmm0, (%r13)
00000001006c5a5f	movl	$0x7fffffff, %eax               ## imm = 0x7FFFFFFF
00000001006c5a64	movl	%eax, -0xd0(%rbp)
00000001006c5a6a	movl	%eax, -0x74(%rbp)
00000001006c5a6d	movq	-0x70(%rbp), %rax
00000001006c5a71	movl	%eax, CONFIG_EMULATE_HARDWARE(%rsi)
00000001006c5a73	movq	-0x68(%rbp), %rax
00000001006c5a77	movq	0x8(%rax), %rax
00000001006c5a7b	movq	0x148(%rax), %rdi
00000001006c5a82	addq	$0x18, %rsi
00000001006c5a86	movq	CONFIG_EMULATE_HARDWARE(%rdi), %rax
00000001006c5a89	leaq	-0xd0(%rbp), %rdx
00000001006c5a90	leaq	-0x74(%rbp), %rcx
00000001006c5a94	movq	-0xd8(%rbp), %r8
00000001006c5a9b	xorl	%r9d, %r9d
00000001006c5a9e	callq	*0x70(%rax)
00000001006c5aa1	movl	-0x3c(%rbp), %r13d
00000001006c5aa5	movl	-0xd0(%rbp), %eax
00000001006c5aab	movq	-0x38(%rbp), %rdi
00000001006c5aaf	movl	%eax, -0x2c(%rbp)
00000001006c5ab2	movl	%eax, 0x8(%rdi)
00000001006c5ab5	movq	-0xb8(%rbp), %rax
00000001006c5abc	movl	%eax, 0xc(%rdi)
00000001006c5abf	movl	$CONFIG_EMULATE_HARDWARE, 0x10(%rdi)
00000001006c5ac6	testb	%r12b, %r12b
00000001006c5ac9	jne	0x1006c5b3e
00000001006c5acb	testl	%r13d, %r13d
00000001006c5ace	jle	0x1006c5b3e
00000001006c5ad0	movb	0x18(%rdi), %al
00000001006c5ad3	testb	$0x1, %al
00000001006c5ad5	jne	0x1006c5af4
00000001006c5ad7	testb	%al, %al
00000001006c5ad9	je	0x1006c5b3e
00000001006c5adb	movzbl	0x19(%rdi), %eax
00000001006c5adf	cmpl	$0x2b, %eax
00000001006c5ae2	je	0x1006c5b3e
00000001006c5ae4	cmpl	$0x2d, %eax
00000001006c5ae7	je	0x1006c5b3e
00000001006c5ae9	addb	$-0x30, %al
00000001006c5aeb	cmpb	$0xa, %al
00000001006c5aed	jb	0x1006c5b3e
00000001006c5aef	movb	0x19(%rdi), %al
00000001006c5af2	jmp	0x1006c5b1a
00000001006c5af4	cmpq	$0x0, 0x20(%rdi)
00000001006c5af9	je	0x1006c5b3e
00000001006c5afb	movq	0x28(%rdi), %rax
00000001006c5aff	movzbl	CONFIG_EMULATE_HARDWARE(%rax), %eax
00000001006c5b02	cmpl	$0x2b, %eax
00000001006c5b05	je	0x1006c5b3e
00000001006c5b07	cmpl	$0x2d, %eax
00000001006c5b0a	je	0x1006c5b3e
00000001006c5b0c	cmpb	$0x30, %al
00000001006c5b0e	jl	0x1006c5b22
00000001006c5b10	cmpb	$0x3a, %al
00000001006c5b12	jb	0x1006c5b3e
00000001006c5b14	movq	0x28(%rdi), %rax
00000001006c5b18	movb	CONFIG_EMULATE_HARDWARE(%rax), %al
00000001006c5b1a	cmpb	$0x3f, %al
00000001006c5b1c	je	0x1006c5b3e
00000001006c5b1e	cmpb	$0x3a, %al
00000001006c5b20	je	0x1006c5b3e
00000001006c5b22	addq	$0x18, %rdi
00000001006c5b26	leaq	0x4f5213b(%rip), %rsi           ## literal pool for: "while_pressed"
00000001006c5b2d	callq	__Z8isLeftCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## isLeftCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
00000001006c5b32	movq	-0x38(%rbp), %rdi
00000001006c5b36	testb	%al, %al
00000001006c5b38	je	0x1006c5f73
00000001006c5b3e	testb	%r12b, %r12b
00000001006c5b41	leaq	_DLGCOLOR_ACTIONWIZARD_QUOTE(%rip), %rax
00000001006c5b48	leaq	_DLGCOLOR_EDIT_TEXT(%rip), %rcx
00000001006c5b4f	cmoveq	%rcx, %rax
00000001006c5b53	cmpb	$0x60, %r12b
00000001006c5b57	leaq	_DLGCOLOR_ACTIONWIZARD_BACKTICK(%rip), %rcx
00000001006c5b5e	cmoveq	%rcx, %rax
00000001006c5b62	movl	CONFIG_EMULATE_HARDWARE(%rax), %eax
00000001006c5b64	movl	%eax, 0x14(%rdi)
00000001006c5b67	movq	-0x58(%rbp), %rax
00000001006c5b6b	testq	%rax, %rax
00000001006c5b6e	cmoveq	%rdi, %rax
00000001006c5b72	movq	%rax, -0x58(%rbp)
00000001006c5b76	leaq	-0x90(%rbp), %rdi
00000001006c5b7d	leaq	-0x38(%rbp), %rsi
00000001006c5b81	callq	__ZNSt3__16vectorIPN15DLGActionWizard5SItemENS_9allocatorIS3_EEE9push_backB8ne200100ERKS3_ ## std::__1::vector<DLGActionWizard::SItem*, std::__1::allocator<DLGActionWizard::SItem*>>::push_back[abi:ne200100](DLGActionWizard::SItem* const&)
00000001006c5b86	movq	%r14, %rdi
00000001006c5b89	leaq	-0x38(%rbp), %rsi
00000001006c5b8d	callq	__ZNSt3__16vectorIPN15DLGActionWizard5SItemENS_9allocatorIS3_EEE9push_backB8ne200100ERKS3_ ## std::__1::vector<DLGActionWizard::SItem*, std::__1::allocator<DLGActionWizard::SItem*>>::push_back[abi:ne200100](DLGActionWizard::SItem* const&)
00000001006c5b92	movq	-0x68(%rbp), %r8
00000001006c5b96	movl	0x5a4(%r8), %eax
00000001006c5b9d	testl	%eax, %eax
00000001006c5b9f	js	0x1006c5bd5
00000001006c5ba1	movq	-0x38(%rbp), %rcx
00000001006c5ba5	movl	0x5a0(%r8), %edx
00000001006c5bac	movl	CONFIG_EMULATE_HARDWARE(%rcx), %edi
00000001006c5bae	cmpl	%edx, %edi
00000001006c5bb0	jg	0x1006c5bd5
00000001006c5bb2	movl	0x4(%rcx), %esi
00000001006c5bb5	cmpl	%eax, %esi
00000001006c5bb7	jg	0x1006c5bd5
00000001006c5bb9	addl	0x8(%rcx), %edi
00000001006c5bbc	cmpl	%edx, %edi
00000001006c5bbe	jle	0x1006c5bd5
00000001006c5bc0	addl	0xc(%rcx), %esi
00000001006c5bc3	cmpl	%eax, %esi
00000001006c5bc5	jle	0x1006c5bd5
00000001006c5bc7	movq	%r14, 0x618(%r8)
00000001006c5bce	movq	%rcx, 0x610(%r8)
00000001006c5bd5	movl	-0x2c(%rbp), %ecx
00000001006c5bd8	addl	-0x70(%rbp), %ecx
00000001006c5bdb	movl	-0xd0(%rbp), %eax
00000001006c5be1	movl	%ecx, -0x2c(%rbp)
00000001006c5be4	addl	%ecx, %eax
00000001006c5be6	movl	-0x5c(%rbp), %ecx
00000001006c5be9	cmpl	%eax, %ecx
00000001006c5beb	cmovlel	%eax, %ecx
00000001006c5bee	movl	%ecx, -0x5c(%rbp)
00000001006c5bf1	movq	-0xb8(%rbp), %rax
00000001006c5bf8	movq	-0x98(%rbp), %rcx
00000001006c5bff	addl	%eax, %ecx
00000001006c5c01	movl	0x638(%r8), %eax
00000001006c5c08	cmpl	%ecx, %eax
00000001006c5c0a	movl	%ecx, -0x70(%rbp)
00000001006c5c0d	cmovlel	%ecx, %eax
00000001006c5c10	movl	%eax, 0x638(%r8)
00000001006c5c17	movzbl	%r15b, %eax
00000001006c5c1b	cmpl	$0x28, %eax
00000001006c5c1e	jle	0x1006c5c86
00000001006c5c20	cmpl	$0x29, %eax
00000001006c5c23	je	0x1006c5cf4
00000001006c5c29	cmpl	$0x3f, %eax
00000001006c5c2c	je	0x1006c5d0c
00000001006c5c32	movq	%r14, %r15
00000001006c5c35	cmpl	$0x3a, %eax
00000001006c5c38	jne	0x1006c5d71
00000001006c5c3e	movq	0x38(%r15), %r15
00000001006c5c42	testq	%r15, %r15
00000001006c5c45	je	0x1006c5d71
00000001006c5c4b	cmpq	$0x0, 0x20(%r15)
00000001006c5c50	jne	0x1006c5c3e
00000001006c5c52	movl	$0x48, %edi
00000001006c5c57	callq	0x104fe8750                     ## symbol stub for: __Znwm
00000001006c5c5c	movq	%rax, %r14
00000001006c5c5f	xorps	%xmm0, %xmm0
00000001006c5c62	movups	%xmm0, 0x30(%rax)
00000001006c5c66	movups	%xmm0, 0x20(%rax)
00000001006c5c6a	movups	%xmm0, 0x10(%rax)
00000001006c5c6e	movups	%xmm0, CONFIG_EMULATE_HARDWARE(%rax)
00000001006c5c71	movq	$CONFIG_EMULATE_HARDWARE, 0x40(%rax)
00000001006c5c79	movq	%r15, 0x38(%rax)
00000001006c5c7d	movq	%rax, 0x20(%r15)
00000001006c5c81	jmp	0x1006c5d71
00000001006c5c86	cmpl	$0x26, %eax
00000001006c5c89	je	0x1006c5d3a
00000001006c5c8f	cmpl	$0x28, %eax
00000001006c5c92	jne	0x1006c5d71
00000001006c5c98	movl	$0x48, %edi
00000001006c5c9d	callq	0x104fe8750                     ## symbol stub for: __Znwm
00000001006c5ca2	xorps	%xmm0, %xmm0
00000001006c5ca5	movups	%xmm0, 0x30(%rax)
00000001006c5ca9	movups	%xmm0, 0x20(%rax)
00000001006c5cad	movups	%xmm0, 0x10(%rax)
00000001006c5cb1	movups	%xmm0, CONFIG_EMULATE_HARDWARE(%rax)
00000001006c5cb4	movq	$CONFIG_EMULATE_HARDWARE, 0x40(%rax)
00000001006c5cbc	movq	%r14, 0x38(%rax)
00000001006c5cc0	movq	%rax, 0x40(%r14)
00000001006c5cc4	jmp	0x1006c5d6e
00000001006c5cc9	movl	$0xffffffff, -0x3c(%rbp)        ## imm = 0xFFFFFFFF
00000001006c5cd0	movl	$CONFIG_EMULATE_HARDWARE, -0x44(%rbp)
00000001006c5cd7	cmpb	$0x26, %r15b
00000001006c5cdb	jne	0x1006c59d0
00000001006c5ce1	cmpb	$0x26, CONFIG_EMULATE_HARDWARE(%rbx)
00000001006c5ce4	leaq	0x1(%rbx), %rax
00000001006c5ce8	cmoveq	%rax, %rbx
00000001006c5cec	movb	$0x26, %r15b
00000001006c5cef	jmp	0x1006c59d0
00000001006c5cf4	movq	%r14, %rax
00000001006c5cf7	movq	%rax, %r14
00000001006c5cfa	movq	0x38(%rax), %rax
00000001006c5cfe	testq	%rax, %rax
00000001006c5d01	je	0x1006c5d71
00000001006c5d03	cmpq	$0x0, 0x40(%r14)
00000001006c5d08	je	0x1006c5cf7
00000001006c5d0a	jmp	0x1006c5d71
00000001006c5d0c	movl	$0x48, %edi
00000001006c5d11	callq	0x104fe8750                     ## symbol stub for: __Znwm
00000001006c5d16	xorps	%xmm0, %xmm0
00000001006c5d19	movups	%xmm0, 0x30(%rax)
00000001006c5d1d	movups	%xmm0, 0x20(%rax)
00000001006c5d21	movups	%xmm0, 0x10(%rax)
00000001006c5d25	movups	%xmm0, CONFIG_EMULATE_HARDWARE(%rax)
00000001006c5d28	movq	$CONFIG_EMULATE_HARDWARE, 0x40(%rax)
00000001006c5d30	movq	%r14, 0x38(%rax)
00000001006c5d34	movq	%rax, 0x18(%r14)
00000001006c5d38	jmp	0x1006c5d6e
00000001006c5d3a	movl	$0x48, %edi
00000001006c5d3f	callq	0x104fe8750                     ## symbol stub for: __Znwm
00000001006c5d44	xorps	%xmm0, %xmm0
00000001006c5d47	movups	%xmm0, 0x30(%rax)
00000001006c5d4b	movups	%xmm0, 0x20(%rax)
00000001006c5d4f	movups	%xmm0, 0x10(%rax)
00000001006c5d53	movups	%xmm0, CONFIG_EMULATE_HARDWARE(%rax)
00000001006c5d56	movq	$CONFIG_EMULATE_HARDWARE, 0x40(%rax)
00000001006c5d5e	movq	0x38(%r14), %rcx
00000001006c5d62	movq	%rcx, 0x38(%rax)
00000001006c5d66	movq	%rax, 0x28(%r14)
00000001006c5d6a	movq	%r14, 0x30(%rax)
00000001006c5d6e	movq	%rax, %r14
00000001006c5d71	movzbl	CONFIG_EMULATE_HARDWARE(%rbx), %eax
00000001006c5d74	cmpl	$0xa, %eax
00000001006c5d77	je	0x1006c5d94
00000001006c5d79	testl	%eax, %eax
00000001006c5d7b	je	0x1006c5f7e
00000001006c5d81	testb	%r12b, %r12b
00000001006c5d84	je	0x1006c5e01
00000001006c5d86	xorl	%r12d, %r12d
00000001006c5d89	movl	%r13d, %r15d
00000001006c5d8c	movq	%rbx, %r13
00000001006c5d8f	jmp	0x1006c5e2e
00000001006c5d94	movsbl	%r12b, %eax
00000001006c5d98	cmpl	%eax, -0x44(%rbp)
00000001006c5d9b	movl	$CONFIG_EMULATE_HARDWARE, %eax
00000001006c5da0	movl	-0x40(%rbp), %ecx
00000001006c5da3	cmovel	%eax, %ecx
00000001006c5da6	movl	%ecx, -0x40(%rbp)
00000001006c5da9	movq	-0x38(%rbp), %rdi
00000001006c5dad	movzbl	0x18(%rdi), %esi
00000001006c5db1	testb	$0x1, %sil
00000001006c5db5	jne	0x1006c5dbf
00000001006c5db7	addq	$0x19, %rdi
00000001006c5dbb	shrl	%esi
00000001006c5dbd	jmp	0x1006c5dc7
00000001006c5dbf	movq	0x20(%rdi), %rsi
00000001006c5dc3	movq	0x28(%rdi), %rdi
00000001006c5dc7	movq	-0x58(%rbp), %r12
00000001006c5dcb	callq	__Z7strTrimNSt3__117basic_string_viewIcNS_11char_traitsIcEEEE ## strTrim(std::__1::basic_string_view<char, std::__1::char_traits<char>>)
00000001006c5dd0	incq	%rbx
00000001006c5dd3	cmpq	$0x1, %rdx
00000001006c5dd7	movl	$CONFIG_EMULATE_HARDWARE, %r15d
00000001006c5ddd	sbbl	%r15d, %r15d
00000001006c5de0	orl	%r13d, %r15d
00000001006c5de3	testq	%r12, %r12
00000001006c5de6	je	0x1006c5e3c
00000001006c5de8	movq	-0xa8(%rbp), %rax
00000001006c5def	movzbl	CONFIG_EMULATE_HARDWARE(%rax), %eax
00000001006c5df2	testb	$0x1, %al
00000001006c5df4	jne	0x1006c5e5d
00000001006c5df6	shrl	%eax
00000001006c5df8	movq	-0xa0(%rbp), %rcx
00000001006c5dff	jmp	0x1006c5e6f
00000001006c5e01	xorl	%r12d, %r12d
00000001006c5e04	leal	-0x22(%rax), %ecx
00000001006c5e07	cmpl	$0x3e, %ecx
00000001006c5e0a	ja	0x1006c5d89
00000001006c5e10	movabsq	$0x4000000000000021, %rdx       ## imm = 0x4000000000000021
00000001006c5e1a	btq	%rcx, %rdx
00000001006c5e1e	jae	0x1006c5d89
00000001006c5e24	movl	%r13d, %r15d
00000001006c5e27	leaq	0x1(%rbx), %r13
00000001006c5e2b	movl	%eax, %r12d
00000001006c5e2e	movq	%rbx, -0x50(%rbp)
00000001006c5e32	movl	-0x2c(%rbp), %eax
00000001006c5e35	movl	%eax, %ebx
00000001006c5e37	jmp	0x1006c5ecf
00000001006c5e3c	movl	-0x40(%rbp), %r12d
00000001006c5e40	movq	%rbx, %r13
00000001006c5e43	movq	%rbx, -0x50(%rbp)
00000001006c5e47	movl	-0x70(%rbp), %eax
00000001006c5e4a	movq	%rax, -0x98(%rbp)
00000001006c5e51	movq	$CONFIG_EMULATE_HARDWARE, -0x58(%rbp)
00000001006c5e59	xorl	%ebx, %ebx
00000001006c5e5b	jmp	0x1006c5ecf
00000001006c5e5d	movq	-0x68(%rbp), %rcx
00000001006c5e61	movq	0x140(%rcx), %rax
00000001006c5e68	movq	0x148(%rcx), %rcx
00000001006c5e6f	movq	-0x38(%rbp), %rsi
00000001006c5e73	movzbl	0x18(%rsi), %edx
00000001006c5e77	testb	$0x1, %dl
00000001006c5e7a	jne	0x1006c5e80
00000001006c5e7c	shrl	%edx
00000001006c5e7e	jmp	0x1006c5e84
00000001006c5e80	movq	0x20(%rsi), %rdx
00000001006c5e84	movslq	0x30(%r12), %rdi
00000001006c5e89	subq	%rdi, %rax
00000001006c5e8c	jb	0x1006c60e1
00000001006c5e92	movslq	0x30(%rsi), %rsi
00000001006c5e96	subq	%rdi, %rsi
00000001006c5e99	addq	%rsi, %rdx
00000001006c5e9c	addq	%rdi, %rcx
00000001006c5e9f	cmpq	%rdx, %rax
00000001006c5ea2	cmovbq	%rax, %rdx
00000001006c5ea6	movq	%rcx, 0x38(%r12)
00000001006c5eab	movq	%rdx, 0x40(%r12)
00000001006c5eb0	movl	-0x40(%rbp), %r12d
00000001006c5eb4	movq	%rbx, %r13
00000001006c5eb7	movq	%rbx, -0x50(%rbp)
00000001006c5ebb	xorl	%ebx, %ebx
00000001006c5ebd	movl	-0x70(%rbp), %eax
00000001006c5ec0	movq	%rax, -0x98(%rbp)
00000001006c5ec7	movq	$CONFIG_EMULATE_HARDWARE, -0x58(%rbp)
00000001006c5ecf	movq	-0x38(%rbp), %rdi
00000001006c5ed3	testl	%r15d, %r15d
00000001006c5ed6	jne	0x1006c5f1c
00000001006c5ed8	movzbl	0x18(%rdi), %esi
00000001006c5edc	testb	$0x1, %sil
00000001006c5ee0	jne	0x1006c5eea
00000001006c5ee2	addq	$0x19, %rdi
00000001006c5ee6	shrl	%esi
00000001006c5ee8	jmp	0x1006c5ef2
00000001006c5eea	movq	0x20(%rdi), %rsi
00000001006c5eee	movq	0x28(%rdi), %rdi
00000001006c5ef2	callq	__Z7strTrimNSt3__117basic_string_viewIcNS_11char_traitsIcEEEE ## strTrim(std::__1::basic_string_view<char, std::__1::char_traits<char>>)
00000001006c5ef7	movq	%rax, %rdi
00000001006c5efa	movq	%rdx, %rsi
00000001006c5efd	leaq	0x4f15bab(%rip), %rdx           ## literal pool for: "deck"
00000001006c5f04	callq	__Z8isLeftCINSt3__117basic_string_viewIcNS_11char_traitsIcEEEEPKc ## isLeftCI(std::__1::basic_string_view<char, std::__1::char_traits<char>>, char const*)
00000001006c5f09	movl	$0xffffffff, -0x3c(%rbp)        ## imm = 0xFFFFFFFF
00000001006c5f10	testb	%al, %al
00000001006c5f12	jne	0x1006c5903
00000001006c5f18	movq	-0x38(%rbp), %rdi
00000001006c5f1c	movzbl	0x18(%rdi), %esi
00000001006c5f20	testb	$0x1, %sil
00000001006c5f24	jne	0x1006c5f2e
00000001006c5f26	addq	$0x19, %rdi
00000001006c5f2a	shrl	%esi
00000001006c5f2c	jmp	0x1006c5f36
00000001006c5f2e	movq	0x20(%rdi), %rsi
00000001006c5f32	movq	0x28(%rdi), %rdi
00000001006c5f36	callq	__Z7strTrimNSt3__117basic_string_viewIcNS_11char_traitsIcEEEE ## strTrim(std::__1::basic_string_view<char, std::__1::char_traits<char>>)
00000001006c5f3b	cmpq	$0x3, %rdx
00000001006c5f3f	jne	0x1006c5f67
00000001006c5f41	movl	$0x3, %edx
00000001006c5f46	movq	%rax, %rdi
00000001006c5f49	leaq	0x4f51cd6(%rip), %rsi           ## literal pool for: "not"
00000001006c5f50	callq	0x104fe92b4                     ## symbol stub for: _strncasecmp
00000001006c5f55	incl	%r15d
00000001006c5f58	testl	%eax, %eax
00000001006c5f5a	cmovel	%eax, %r15d
00000001006c5f5e	movl	%r15d, -0x3c(%rbp)
00000001006c5f62	jmp	0x1006c5903
00000001006c5f67	incl	%r15d
00000001006c5f6a	movl	%r15d, -0x3c(%rbp)
00000001006c5f6e	jmp	0x1006c5903
00000001006c5f73	movl	_DLGCOLOR_ACTIONWIZARD_QUOTE(%rip), %eax
00000001006c5f79	jmp	0x1006c5b64
00000001006c5f7e	movq	-0x58(%rbp), %r9
00000001006c5f82	testq	%r9, %r9
00000001006c5f85	je	0x1006c5f9d
00000001006c5f87	movq	-0xa8(%rbp), %rax
00000001006c5f8e	movzbl	CONFIG_EMULATE_HARDWARE(%rax), %eax
00000001006c5f91	testb	$0x1, %al
00000001006c5f93	movq	-0x68(%rbp), %r8
00000001006c5f97	jne	0x1006c5faa
00000001006c5f99	shrl	%eax
00000001006c5f9b	jmp	0x1006c5fbf
00000001006c5f9d	movq	-0x88(%rbp), %rcx
00000001006c5fa4	movq	-0x68(%rbp), %r8
00000001006c5fa8	jmp	0x1006c600b
00000001006c5faa	movq	0x140(%r8), %rax
00000001006c5fb1	movq	0x148(%r8), %rcx
00000001006c5fb8	movq	%rcx, -0xa0(%rbp)
00000001006c5fbf	movslq	0x30(%r9), %rsi
00000001006c5fc3	movq	-0x88(%rbp), %rcx
00000001006c5fca	movq	-0x8(%rcx), %rdi
00000001006c5fce	movzbl	0x18(%rdi), %edx
00000001006c5fd2	testb	$0x1, %dl
00000001006c5fd5	jne	0x1006c5fdb
00000001006c5fd7	shrl	%edx
00000001006c5fd9	jmp	0x1006c5fdf
00000001006c5fdb	movq	0x20(%rdi), %rdx
00000001006c5fdf	subq	%rsi, %rax
00000001006c5fe2	jb	0x1006c60ef
00000001006c5fe8	movslq	0x30(%rdi), %rdi
00000001006c5fec	subq	%rsi, %rdi
00000001006c5fef	addq	%rdi, %rdx
00000001006c5ff2	movq	-0xa0(%rbp), %rdi
00000001006c5ff9	addq	%rsi, %rdi
00000001006c5ffc	cmpq	%rdx, %rax
00000001006c5fff	cmovbq	%rax, %rdx
00000001006c6003	movq	%rdi, 0x38(%r9)
00000001006c6007	movq	%rdx, 0x40(%r9)
00000001006c600b	movl	-0x5c(%rbp), %eax
00000001006c600e	movl	%eax, 0x150(%r8)
00000001006c6015	movl	0x638(%r8), %eax
00000001006c601c	movl	%eax, 0x154(%r8)
00000001006c6023	movq	-0x90(%rbp), %rax
00000001006c602a	movq	0x5b0(%r8), %rdi
00000001006c6031	movq	%rdi, -0x90(%rbp)
00000001006c6038	movq	%rax, 0x5b0(%r8)
00000001006c603f	movq	-0x80(%rbp), %rdx
00000001006c6043	movq	0x5b8(%r8), %rax
00000001006c604a	movups	0x5b8(%r8), %xmm0
00000001006c6052	movq	%rcx, 0x5b8(%r8)
00000001006c6059	movups	%xmm0, -0x88(%rbp)
00000001006c6060	movq	%rdx, 0x5c0(%r8)
00000001006c6067	cmpq	%rdi, %rax
00000001006c606a	je	0x1006c60be
00000001006c606c	xorl	%r14d, %r14d
00000001006c606f	movq	CONFIG_EMULATE_HARDWARE(%rdi,%r14,8), %rbx
00000001006c6073	testq	%rbx, %rbx
00000001006c6076	je	0x1006c60ac
00000001006c6078	testb	$0x1, 0x18(%rbx)
00000001006c607c	je	0x1006c6087
00000001006c607e	movq	0x28(%rbx), %rdi
00000001006c6082	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
00000001006c6087	movq	%rbx, %rdi
00000001006c608a	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
00000001006c608f	movq	-0x90(%rbp), %rax
00000001006c6096	movq	$CONFIG_EMULATE_HARDWARE, CONFIG_EMULATE_HARDWARE(%rax,%r14,8)
00000001006c609e	movq	-0x90(%rbp), %rdi
00000001006c60a5	movq	-0x88(%rbp), %rax
00000001006c60ac	incq	%r14
00000001006c60af	movq	%rax, %rcx
00000001006c60b2	subq	%rdi, %rcx
00000001006c60b5	sarq	$0x3, %rcx
00000001006c60b9	cmpq	%rcx, %r14
00000001006c60bc	jb	0x1006c606f
00000001006c60be	testq	%rdi, %rdi
00000001006c60c1	je	0x1006c60cf
00000001006c60c3	movq	%rdi, -0x88(%rbp)
00000001006c60ca	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
00000001006c60cf	addq	$FGData.grain_scale_shift, %rsp
00000001006c60d6	popq	%rbx
00000001006c60d7	popq	%r12
00000001006c60d9	popq	%r13
00000001006c60db	popq	%r14
00000001006c60dd	popq	%r15
00000001006c60df	popq	%rbp
00000001006c60e0	retq
00000001006c60e1	leaq	0x4f178b3(%rip), %rdi           ## literal pool for: "string_view::substr"
00000001006c60e8	callq	__ZNSt3__120__throw_out_of_rangeB8ne200100EPKc ## std::__1::__throw_out_of_range[abi:ne200100](char const*)
00000001006c60ed	jmp	0x1006c60fb
00000001006c60ef	leaq	0x4f178a5(%rip), %rdi           ## literal pool for: "string_view::substr"
00000001006c60f6	callq	__ZNSt3__120__throw_out_of_rangeB8ne200100EPKc ## std::__1::__throw_out_of_range[abi:ne200100](char const*)
00000001006c60fb	ud2
00000001006c60fd	jmp	0x1006c6113
00000001006c60ff	jmp	0x1006c6113
00000001006c6101	jmp	0x1006c6113
00000001006c6103	jmp	0x1006c6113
00000001006c6105	jmp	0x1006c6113
00000001006c6107	jmp	0x1006c6113
00000001006c6109	jmp	0x1006c6113
00000001006c610b	jmp	0x1006c6113
00000001006c610d	jmp	0x1006c6113
00000001006c610f	jmp	0x1006c6113
00000001006c6111	jmp	0x1006c6113
00000001006c6113	movq	%rax, %rbx
00000001006c6116	movq	-0x90(%rbp), %rdi
00000001006c611d	testq	%rdi, %rdi
00000001006c6120	je	0x1006c612e
00000001006c6122	movq	%rdi, -0x88(%rbp)
00000001006c6129	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
00000001006c612e	movq	%rbx, %rdi
00000001006c6131	callq	0x104fe8456                     ## symbol stub for: __Unwind_Resume
