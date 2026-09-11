__ZN18IParamValuesAction9getValuesEP12SActionParamS1_ [0x100992dc8, 0x1009932da):
0000000100992dc8	pushq	%rbp
0000000100992dc9	movq	%rsp, %rbp
0000000100992dcc	pushq	%r15
0000000100992dce	pushq	%r14
0000000100992dd0	pushq	%r13
0000000100992dd2	pushq	%r12
0000000100992dd4	pushq	%rbx
0000000100992dd5	subq	$0x28, %rsp
0000000100992dd9	movq	0x20(%rdi), %r13
0000000100992ddd	movq	0x28(%rdi), %rcx
0000000100992de1	movl	$0x80070057, %r15d              ## imm = 0x80070057
0000000100992de7	subq	%r13, %rcx
0000000100992dea	je	0x100993109
0000000100992df0	movq	%rdx, %rbx
0000000100992df3	movq	%rsi, %r12
0000000100992df6	movq	%rdi, %r14
0000000100992df9	sarq	$0x3, %rcx
0000000100992dfd	movabsq	$-0x3333333333333333, %rax      ## imm = 0xCCCCCCCCCCCCCCCD
0000000100992e07	imulq	%rcx, %rax
0000000100992e0b	cmpq	$0x2, %rax
0000000100992e0f	jb	0x100992e17
0000000100992e11	addq	$0x28, %r13
0000000100992e15	jmp	0x100992e24
0000000100992e17	movq	0x68(%r14), %r13
0000000100992e1b	testq	%r13, %r13
0000000100992e1e	je	0x100992eda
0000000100992e24	movl	(%r13), %ecx
0000000100992e28	cmpl	$0x696e73, %ecx                 ## imm = 0x696E73
0000000100992e2e	jg	0x100992e52
0000000100992e30	cmpl	$0x6d72, %ecx                   ## imm = 0x6D72
0000000100992e36	jg	0x100992ef9
0000000100992e3c	testl	%ecx, %ecx
0000000100992e3e	je	0x100992eda
0000000100992e44	cmpl	$0x25, %ecx
0000000100992e47	je	0x10099303f
0000000100992e4d	jmp	0x100993109
0000000100992e52	cmpl	$0x76616b, %ecx                 ## imm = 0x76616B
0000000100992e58	jg	0x100992f16
0000000100992e5e	cmpl	$0x696e74, %ecx                 ## imm = 0x696E74
0000000100992e64	je	0x10099303f
0000000100992e6a	cmpl	$0x747874, %ecx                 ## imm = 0x747874
0000000100992e70	jne	0x100993109
0000000100992e76	movq	FGData.grain_scale_shift(%r14), %rdi
0000000100992e7d	testq	%rdi, %rdi
0000000100992e80	je	0x100992ea4
0000000100992e82	cmpq	$0x1, %rax
0000000100992e86	ja	0x10099302a
0000000100992e8c	leaq	rf.n_tile_threads(%r14), %rdi
0000000100992e93	leaq	0x8(%r13), %rsi
0000000100992e97	callq	__Z12strIsEqualCIRK11smallstringRKNSt3__112basic_stringIcNS2_11char_traitsIcEENS2_9allocatorIcEEEE ## strIsEqualCI(smallstring const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&)
0000000100992e9c	testb	%al, %al
0000000100992e9e	jne	0x10099301e
0000000100992ea4	leaq	0x8(%r13), %rsi
0000000100992ea8	movzbl	0x8(%r13), %eax
0000000100992ead	testb	$0x1, %al
0000000100992eaf	movq	%rsi, -0x50(%rbp)
0000000100992eb3	jne	0x100992f33
0000000100992eb5	testq	%rax, %rax
0000000100992eb8	je	0x100992f75
0000000100992ebe	cmpb	$0x60, 0x9(%r13)
0000000100992ec3	jne	0x100992f75
0000000100992ec9	movl	%eax, %ecx
0000000100992ecb	shrl	%ecx
0000000100992ecd	cmpb	$0x60, 0x8(%r13,%rcx)
0000000100992ed3	je	0x100992f50
0000000100992ed5	jmp	0x100992f75
0000000100992eda	movl	0x58(%r14), %eax
0000000100992ede	andl	$0x1, %eax
0000000100992ee1	movl	$0x76616c, CONFIG_EMULATE_HARDWARE(%r12) ## imm = 0x76616C
0000000100992ee9	movl	%eax, 0x4(%r12)
0000000100992eee	movb	$0x0, 0x20(%r12)
0000000100992ef4	jmp	0x10099305e
0000000100992ef9	cmpl	$0x6d73, %ecx                   ## imm = 0x6D73
0000000100992eff	je	0x10099303f
0000000100992f05	cmpl	$0x636f6c, %ecx                 ## imm = 0x636F6C
0000000100992f0b	je	0x10099303f
0000000100992f11	jmp	0x100993109
0000000100992f16	cmpl	$0x76616c, %ecx                 ## imm = 0x76616C
0000000100992f1c	je	0x10099303f
0000000100992f22	cmpl	$0x626f6f6c, %ecx               ## imm = 0x626F6F6C
0000000100992f28	je	0x10099303f
0000000100992f2e	jmp	0x100993109
0000000100992f33	movq	0x10(%r13), %rcx
0000000100992f37	testq	%rcx, %rcx
0000000100992f3a	je	0x100992f75
0000000100992f3c	movq	0x18(%r13), %rdx
0000000100992f40	cmpb	$0x60, CONFIG_EMULATE_HARDWARE(%rdx)
0000000100992f43	jne	0x100992f75
0000000100992f45	cmpb	$0x60, -0x1(%rdx,%rcx)
0000000100992f4a	jne	0x100992f75
0000000100992f4c	movq	0x10(%r13), %rcx
0000000100992f50	addq	$-0x2, %rcx
0000000100992f54	leaq	-0x48(%rbp), %rdi
0000000100992f58	leaq	-0x29(%rbp), %r8
0000000100992f5c	movl	$CONFIG_VP9, %edx
0000000100992f61	callq	0x104fe855e                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEC2ERKS5_mmRKS4_
0000000100992f66	leaq	-0x48(%rbp), %rax
0000000100992f6a	testb	$0x1, CONFIG_EMULATE_HARDWARE(%rax)
0000000100992f6d	je	0x100992fad
0000000100992f6f	movq	-0x38(%rbp), %rdi
0000000100992f73	jmp	0x100992fb1
0000000100992f75	testb	$0x1, %al
0000000100992f77	je	0x100992f7f
0000000100992f79	movq	0x18(%r13), %rdi
0000000100992f7d	jmp	0x100992f83
0000000100992f7f	leaq	0x9(%r13), %rdi
0000000100992f83	xorl	%esi, %esi
0000000100992f85	xorl	%edx, %edx
0000000100992f87	callq	__ZN7IAction6createEPKcPS1_i    ## IAction::create(char const*, char const**, int)
0000000100992f8c	movq	FGData.grain_scale_shift(%r14), %rdi
0000000100992f93	movq	%rax, FGData.grain_scale_shift(%r14)
0000000100992f9a	testq	%rdi, %rdi
0000000100992f9d	je	0x100992fef
0000000100992f9f	lock
0000000100992fa0	decl	0x8(%rdi)
0000000100992fa3	jg	0x100992fe8
0000000100992fa5	movq	CONFIG_EMULATE_HARDWARE(%rdi), %rax
0000000100992fa8	callq	*0x8(%rax)
0000000100992fab	jmp	0x100992fe8
0000000100992fad	leaq	-0x47(%rbp), %rdi
0000000100992fb1	xorl	%esi, %esi
0000000100992fb3	xorl	%edx, %edx
0000000100992fb5	callq	__ZN7IAction6createEPKcPS1_i    ## IAction::create(char const*, char const**, int)
0000000100992fba	movq	FGData.grain_scale_shift(%r14), %rdi
0000000100992fc1	movq	%rax, FGData.grain_scale_shift(%r14)
0000000100992fc8	testq	%rdi, %rdi
0000000100992fcb	je	0x100992fd9
0000000100992fcd	lock
0000000100992fce	decl	0x8(%rdi)
0000000100992fd1	jg	0x100992fd9
0000000100992fd3	movq	CONFIG_EMULATE_HARDWARE(%rdi), %rax
0000000100992fd6	callq	*0x8(%rax)
0000000100992fd9	testb	$0x1, -0x48(%rbp)
0000000100992fdd	je	0x100992fe8
0000000100992fdf	movq	-0x38(%rbp), %rdi
0000000100992fe3	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
0000000100992fe8	movq	FGData.grain_scale_shift(%r14), %rax
0000000100992fef	testq	%rax, %rax
0000000100992ff2	je	0x1009931ae
0000000100992ff8	leaq	0x70(%r14), %rsi
0000000100992ffc	leaq	-0x48(%rbp), %rdi
0000000100993000	callq	__ZN15CAutoThreadSyncC1EP11CThreadSync ## CAutoThreadSync::CAutoThreadSync(CThreadSync*)
0000000100993005	leaq	rf.n_tile_threads(%r14), %rdi
000000010099300c	movq	-0x50(%rbp), %rsi
0000000100993010	callq	__ZN11smallstringaSERKNSt3__112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEE ## smallstring::operator=(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&)
0000000100993015	leaq	-0x48(%rbp), %rdi
0000000100993019	callq	__ZN15CAutoThreadSyncD1Ev       ## CAutoThreadSync::~CAutoThreadSync()
000000010099301e	movq	FGData.grain_scale_shift(%r14), %rdi
0000000100993025	testq	%rdi, %rdi
0000000100993028	je	0x10099303f
000000010099302a	movl	0x5c(%r14), %edx
000000010099302e	movq	0x50(%r14), %rcx
0000000100993032	movq	%r12, %rsi
0000000100993035	xorl	%r8d, %r8d
0000000100993038	callq	__ZN7IAction5queryER12SActionParamjP11IControllerj ## IAction::query(SActionParam&, unsigned int, IController*, unsigned int)
000000010099303d	jmp	0x10099305e
000000010099303f	movq	(%r13), %rax
0000000100993043	movq	%rax, CONFIG_EMULATE_HARDWARE(%r12)
0000000100993047	leaq	0x8(%r12), %rdi
000000010099304c	leaq	0x8(%r13), %rsi
0000000100993050	callq	0x104fe856a                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
0000000100993055	movb	0x20(%r13), %al
0000000100993059	movb	%al, 0x20(%r12)
000000010099305e	movq	0x20(%r14), %r12
0000000100993062	movl	CONFIG_EMULATE_HARDWARE(%r12), %eax
0000000100993066	cmpl	$0x696e73, %eax                 ## imm = 0x696E73
000000010099306b	jle	0x1009930c6
000000010099306d	cmpl	$0x76616b, %eax                 ## imm = 0x76616B
0000000100993072	jg	0x1009930db
0000000100993074	cmpl	$0x696e74, %eax                 ## imm = 0x696E74
0000000100993079	je	0x1009930e9
000000010099307b	cmpl	$0x747874, %eax                 ## imm = 0x747874
0000000100993080	jne	0x100993109
0000000100993086	movq	rf.r(%r14), %rdi
000000010099308d	testq	%rdi, %rdi
0000000100993090	jne	0x10099323d
0000000100993096	movzbl	0x8(%r12), %eax
000000010099309c	testb	$0x1, %al
000000010099309e	jne	0x10099311b
00000001009930a0	testq	%rax, %rax
00000001009930a3	je	0x10099316e
00000001009930a9	cmpb	$0x60, 0x9(%r12)
00000001009930af	jne	0x10099316e
00000001009930b5	movl	%eax, %ecx
00000001009930b7	shrl	%ecx
00000001009930b9	cmpb	$0x60, 0x8(%r12,%rcx)
00000001009930bf	je	0x10099313b
00000001009930c1	jmp	0x10099316e
00000001009930c6	cmpl	$0x25, %eax
00000001009930c9	je	0x1009930e9
00000001009930cb	cmpl	$0x6d73, %eax                   ## imm = 0x6D73
00000001009930d0	je	0x1009930e9
00000001009930d2	cmpl	$0x636f6c, %eax                 ## imm = 0x636F6C
00000001009930d7	je	0x1009930e9
00000001009930d9	jmp	0x100993109
00000001009930db	cmpl	$0x626f6f6c, %eax               ## imm = 0x626F6F6C
00000001009930e0	je	0x1009930e9
00000001009930e2	cmpl	$0x76616c, %eax                 ## imm = 0x76616C
00000001009930e7	jne	0x100993109
00000001009930e9	movq	CONFIG_EMULATE_HARDWARE(%r12), %rax
00000001009930ed	movq	%rax, CONFIG_EMULATE_HARDWARE(%rbx)
00000001009930f0	leaq	0x8(%rbx), %rdi
00000001009930f4	leaq	0x8(%r12), %rsi
00000001009930f9	callq	0x104fe856a                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
00000001009930fe	movb	0x20(%r12), %al
0000000100993103	movb	%al, 0x20(%rbx)
0000000100993106	xorl	%r15d, %r15d
0000000100993109	movl	%r15d, %eax
000000010099310c	addq	$0x28, %rsp
0000000100993110	popq	%rbx
0000000100993111	popq	%r12
0000000100993113	popq	%r13
0000000100993115	popq	%r14
0000000100993117	popq	%r15
0000000100993119	popq	%rbp
000000010099311a	retq
000000010099311b	movq	0x10(%r12), %rcx
0000000100993120	testq	%rcx, %rcx
0000000100993123	je	0x10099316e
0000000100993125	movq	0x18(%r12), %rdx
000000010099312a	cmpb	$0x60, CONFIG_EMULATE_HARDWARE(%rdx)
000000010099312d	jne	0x10099316e
000000010099312f	cmpb	$0x60, -0x1(%rdx,%rcx)
0000000100993134	jne	0x10099316e
0000000100993136	movq	0x10(%r12), %rcx
000000010099313b	addq	$0x8, %r12
000000010099313f	addq	$-0x2, %rcx
0000000100993143	leaq	-0x48(%rbp), %r15
0000000100993147	leaq	-0x29(%rbp), %r8
000000010099314b	movl	$CONFIG_VP9, %edx
0000000100993150	movq	%r15, %rdi
0000000100993153	movq	%r12, %rsi
0000000100993156	callq	0x104fe855e                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEC2ERKS5_mmRKS4_
000000010099315b	testb	$0x1, CONFIG_EMULATE_HARDWARE(%r15)
000000010099315f	je	0x1009931ea
0000000100993165	movq	-0x38(%rbp), %rdi
0000000100993169	jmp	0x1009931ee
000000010099316e	testb	$0x1, %al
0000000100993170	je	0x100993179
0000000100993172	movq	0x18(%r12), %r12
0000000100993177	jmp	0x10099317d
0000000100993179	addq	$0x9, %r12
000000010099317d	movq	%r12, %rdi
0000000100993180	xorl	%esi, %esi
0000000100993182	xorl	%edx, %edx
0000000100993184	callq	__ZN7IAction6createEPKcPS1_i    ## IAction::create(char const*, char const**, int)
0000000100993189	movq	rf.r(%r14), %rdi
0000000100993190	movq	%rax, rf.r(%r14)
0000000100993197	testq	%rdi, %rdi
000000010099319a	je	0x10099322c
00000001009931a0	lock
00000001009931a1	decl	0x8(%rdi)
00000001009931a4	jg	0x100993225
00000001009931a6	movq	CONFIG_EMULATE_HARDWARE(%rdi), %rax
00000001009931a9	callq	*0x8(%rax)
00000001009931ac	jmp	0x100993225
00000001009931ae	leaq	0x4c5703e(%rip), %rdi           ## literal pool for: "nothing"
00000001009931b5	xorl	%esi, %esi
00000001009931b7	xorl	%edx, %edx
00000001009931b9	callq	__ZN7IAction6createEPKcPS1_i    ## IAction::create(char const*, char const**, int)
00000001009931be	movq	FGData.grain_scale_shift(%r14), %rdi
00000001009931c5	movq	%rax, FGData.grain_scale_shift(%r14)
00000001009931cc	testq	%rdi, %rdi
00000001009931cf	je	0x100992ff8
00000001009931d5	lock
00000001009931d6	decl	0x8(%rdi)
00000001009931d9	jg	0x100992ff8
00000001009931df	movq	CONFIG_EMULATE_HARDWARE(%rdi), %rax
00000001009931e2	callq	*0x8(%rax)
00000001009931e5	jmp	0x100992ff8
00000001009931ea	leaq	-0x47(%rbp), %rdi
00000001009931ee	xorl	%esi, %esi
00000001009931f0	xorl	%edx, %edx
00000001009931f2	callq	__ZN7IAction6createEPKcPS1_i    ## IAction::create(char const*, char const**, int)
00000001009931f7	movq	rf.r(%r14), %rdi
00000001009931fe	movq	%rax, rf.r(%r14)
0000000100993205	testq	%rdi, %rdi
0000000100993208	je	0x100993216
000000010099320a	lock
000000010099320b	decl	0x8(%rdi)
000000010099320e	jg	0x100993216
0000000100993210	movq	CONFIG_EMULATE_HARDWARE(%rdi), %rax
0000000100993213	callq	*0x8(%rax)
0000000100993216	testb	$0x1, -0x48(%rbp)
000000010099321a	je	0x100993225
000000010099321c	movq	-0x38(%rbp), %rdi
0000000100993220	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
0000000100993225	movq	rf.r(%r14), %rax
000000010099322c	testq	%rax, %rax
000000010099322f	je	0x100993258
0000000100993231	movq	rf.r(%r14), %rdi
0000000100993238	testq	%rdi, %rdi
000000010099323b	je	0x10099328f
000000010099323d	movl	0x5c(%r14), %edx
0000000100993241	movq	0x50(%r14), %rcx
0000000100993245	xorl	%r15d, %r15d
0000000100993248	movq	%rbx, %rsi
000000010099324b	xorl	%r8d, %r8d
000000010099324e	callq	__ZN7IAction5queryER12SActionParamjP11IControllerj ## IAction::query(SActionParam&, unsigned int, IController*, unsigned int)
0000000100993253	jmp	0x100993109
0000000100993258	leaq	0x4c56f94(%rip), %rdi           ## literal pool for: "nothing"
000000010099325f	xorl	%esi, %esi
0000000100993261	xorl	%edx, %edx
0000000100993263	callq	__ZN7IAction6createEPKcPS1_i    ## IAction::create(char const*, char const**, int)
0000000100993268	movq	%rax, %rdi
000000010099326b	movq	rf.r(%r14), %rax
0000000100993272	movq	%rdi, rf.r(%r14)
0000000100993279	testq	%rax, %rax
000000010099327c	je	0x100993238
000000010099327e	lock
000000010099327f	decl	0x8(%rax)
0000000100993282	jg	0x100993231
0000000100993284	movq	CONFIG_EMULATE_HARDWARE(%rax), %rcx
0000000100993287	movq	%rax, %rdi
000000010099328a	callq	*0x8(%rcx)
000000010099328d	jmp	0x100993231
000000010099328f	movq	0x20(%r14), %r14
0000000100993293	movq	CONFIG_EMULATE_HARDWARE(%r14), %rax
0000000100993296	movq	%rax, CONFIG_EMULATE_HARDWARE(%rbx)
0000000100993299	leaq	0x8(%rbx), %rdi
000000010099329d	leaq	0x8(%r14), %rsi
00000001009932a1	callq	0x104fe856a                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
00000001009932a6	movb	0x20(%r14), %al
00000001009932aa	jmp	0x100993103
00000001009932af	jmp	0x1009932b1
00000001009932b1	movq	%rax, %rbx
00000001009932b4	testb	$0x1, -0x48(%rbp)
00000001009932b8	je	0x1009932d1
00000001009932ba	movq	-0x38(%rbp), %rdi
00000001009932be	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
00000001009932c3	jmp	0x1009932d1
00000001009932c5	movq	%rax, %rbx
00000001009932c8	leaq	-0x48(%rbp), %rdi
00000001009932cc	callq	__ZN15CAutoThreadSyncD1Ev       ## CAutoThreadSync::~CAutoThreadSync()
00000001009932d1	movq	%rbx, %rdi
00000001009932d4	callq	0x104fe8456                     ## symbol stub for: __Unwind_Resume
00000001009932d9	nop
