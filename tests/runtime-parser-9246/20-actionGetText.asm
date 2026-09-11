__Z13actionGetTextP7SDBInfoPKcPNSt3__112basic_stringIcNS3_11char_traitsIcEENS3_9allocatorIcEEEEiP5CDeckP5CSongbP7IActionPNS3_6vectorIP16SActionCacheItemNS7_ISJ_EEEE [0x100422f51, 0x100425874):
0000000100422f51	pushq	%rbp
0000000100422f52	movq	%rsp, %rbp
0000000100422f55	pushq	%r15
0000000100422f57	pushq	%r14
0000000100422f59	pushq	%r13
0000000100422f5b	pushq	%r12
0000000100422f5d	pushq	%rbx
0000000100422f5e	subq	$rf.n_tile_threads, %rsp
0000000100422f65	movq	%r9, %rbx
0000000100422f68	movl	%ecx, -0xbc(%rbp)
0000000100422f6e	movq	%rdx, %r15
0000000100422f71	movq	%rdi, %r14
0000000100422f74	movq	%rsi, -0x40(%rbp)
0000000100422f78	testb	$0x1, CONFIG_EMULATE_HARDWARE(%rdx)
0000000100422f7b	jne	0x100422f85
0000000100422f7d	movw	$CONFIG_EMULATE_HARDWARE, CONFIG_EMULATE_HARDWARE(%r15)
0000000100422f83	jmp	0x100422f94
0000000100422f85	movq	0x10(%r15), %rax
0000000100422f89	movb	$0x0, CONFIG_EMULATE_HARDWARE(%rax)
0000000100422f8c	movq	$CONFIG_EMULATE_HARDWARE, 0x8(%r15)
0000000100422f94	testq	%r8, %r8
0000000100422f97	jne	0x100422fa6
0000000100422f99	movl	$0x61637469, %edi               ## imm = 0x61637469
0000000100422f9e	callq	__Z7getDecki                    ## getDeck(int)
0000000100422fa3	movq	%rax, %r8
0000000100422fa6	testq	%rbx, %rbx
0000000100422fa9	jne	0x100422fb2
0000000100422fab	movq	0x6c8(%r8), %rbx
0000000100422fb2	movq	%r8, -0x48(%rbp)
0000000100422fb6	movq	%rbx, -0xc8(%rbp)
0000000100422fbd	movb	0x10(%rbp), %al
0000000100422fc0	testq	%r14, %r14
0000000100422fc3	jne	0x100422fcc
0000000100422fc5	leaq	_emptyDBInfo(%rip), %r14
0000000100422fcc	movq	%r14, -0x50(%rbp)
0000000100422fd0	leaq	_Config(%rip), %rcx
0000000100422fd7	andb	0x9f80(%rcx), %al
0000000100422fdd	movb	%al, -0x51(%rbp)
0000000100422fe0	leaq	0x1(%r15), %rax
0000000100422fe4	movq	%rax, -0xb8(%rbp)
0000000100422feb	movl	$0x268, %eax                    ## imm = 0x268
0000000100422ff0	addq	0x539c6a1(%rip), %rax
0000000100422ff7	movq	%rax, -0xe8(%rbp)
0000000100422ffe	movq	%r15, -0x30(%rbp)
0000000100423002	movq	-0x40(%rbp), %r12
0000000100423006	movzbl	CONFIG_EMULATE_HARDWARE(%r12), %eax
000000010042300b	cmpl	$0x5b, %eax
000000010042300e	jle	0x100423059
0000000100423010	cmpl	$0x60, %eax
0000000100423013	je	0x1004230a8
0000000100423019	cmpl	$0x5c, %eax
000000010042301c	jne	0x100423103
0000000100423022	leaq	0x1(%r12), %rdi
0000000100423027	movq	%rdi, -0x40(%rbp)
000000010042302b	movzbl	0x1(%r12), %eax
0000000100423031	leal	-0x30(%rax), %ecx
0000000100423034	cmpb	$0x9, %cl
0000000100423037	ja	0x100423138
000000010042303d	callq	0x104fe88d6                     ## symbol stub for: _atoi
0000000100423042	movl	%eax, %r14d
0000000100423045	movzbl	CONFIG_EMULATE_HARDWARE(%r15), %ebx
0000000100423049	testb	$0x1, %bl
000000010042304c	jne	0x100423372
0000000100423052	shrl	%ebx
0000000100423054	jmp	0x100423376
0000000100423059	cmpl	$0x25, %eax
000000010042305c	jne	0x1004230fb
0000000100423062	leaq	0x1(%r12), %r14
0000000100423067	movq	%r14, -0x40(%rbp)
000000010042306b	movl	$CONFIG_EMULATE_HARDWARE, -0x34(%rbp)
0000000100423072	movzbl	0x1(%r12), %r13d
0000000100423078	cmpl	$0x7b, %r13d
000000010042307c	je	0x100423183
0000000100423082	cmpl	$0x25, %r13d
0000000100423086	jne	0x1004232fb
000000010042308c	addq	$0x2, %r12
0000000100423090	movq	%r12, -0x40(%rbp)
0000000100423094	movzbl	CONFIG_EMULATE_HARDWARE(%r15), %ebx
0000000100423098	testb	$0x1, %bl
000000010042309b	jne	0x10042342b
00000001004230a1	shrl	%ebx
00000001004230a3	jmp	0x10042342f
00000001004230a8	leaq	0x1(%r12), %r13
00000001004230ad	movq	%r13, -0x40(%rbp)
00000001004230b1	movq	%r13, %rdi
00000001004230b4	movl	$FGData.ar_coeffs_y, %esi
00000001004230b9	callq	0x104fe927e                     ## symbol stub for: _strchr
00000001004230be	testq	%rax, %rax
00000001004230c1	je	0x10042316f
00000001004230c7	movq	%rax, %r14
00000001004230ca	cmpq	%r13, %rax
00000001004230cd	je	0x1004233f2
00000001004230d3	movb	CONFIG_EMULATE_HARDWARE(%r14), %bl
00000001004230d6	movb	$0x0, CONFIG_EMULATE_HARDWARE(%r14)
00000001004230da	movq	-0x40(%rbp), %rsi
00000001004230de	movq	0x20(%rbp), %rdi
00000001004230e2	testq	%rdi, %rdi
00000001004230e5	je	0x100423457
00000001004230eb	movl	-0xbc(%rbp), %edx
00000001004230f1	callq	__ZN11CSkinEngine12createActionEPNSt3__16vectorIP16SActionCacheItemNS0_9allocatorIS3_EEEEPKci ## CSkinEngine::createAction(std::__1::vector<SActionCacheItem*, std::__1::allocator<SActionCacheItem*>>*, char const*, int)
00000001004230f6	jmp	0x100423467
00000001004230fb	testl	%eax, %eax
00000001004230fd	je	0x100425707
0000000100423103	movq	%r12, %rdi
0000000100423106	leaq	0x51e339d(%rip), %rsi           ## literal pool for: "%\\`"
000000010042310d	callq	0x104fe92cc                     ## symbol stub for: _strpbrk
0000000100423112	testq	%rax, %rax
0000000100423115	je	0x1004256f1
000000010042311b	movq	%rax, %r14
000000010042311e	movq	%rax, %rdx
0000000100423121	subq	%r12, %rdx
0000000100423124	movq	%r15, %rdi
0000000100423127	movq	%r12, %rsi
000000010042312a	callq	0x104fe8516                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm
000000010042312f	movq	%r14, -0x40(%rbp)
0000000100423133	jmp	0x100423002
0000000100423138	cmpl	$0x71, %eax
000000010042313b	jg	0x1004233c4
0000000100423141	cmpl	$0x5c, %eax
0000000100423144	je	0x10042357b
000000010042314a	cmpl	$0x6e, %eax
000000010042314d	jne	0x100423583
0000000100423153	addq	$0x2, %r12
0000000100423157	movq	%r12, -0x40(%rbp)
000000010042315b	movzbl	CONFIG_EMULATE_HARDWARE(%r15), %ebx
000000010042315f	testb	$0x1, %bl
0000000100423162	jne	0x1004236fa
0000000100423168	shrl	%ebx
000000010042316a	jmp	0x1004236fe
000000010042316f	movzbl	CONFIG_EMULATE_HARDWARE(%r15), %ebx
0000000100423173	testb	$0x1, %bl
0000000100423176	jne	0x1004233ff
000000010042317c	shrl	%ebx
000000010042317e	jmp	0x100423403
0000000100423183	addq	$0x2, %r12
0000000100423187	movq	%r12, -0x40(%rbp)
000000010042318b	movq	%r12, %rdi
000000010042318e	movl	$0x7d, %esi
0000000100423193	callq	0x104fe927e                     ## symbol stub for: _strchr
0000000100423198	testq	%rax, %rax
000000010042319b	je	0x100423546
00000001004231a1	movq	%rax, %r14
00000001004231a4	leaq	-0x80(%rbp), %rdi
00000001004231a8	leaq	0x51ba06b(%rip), %rsi           ## literal pool for: "msg"
00000001004231af	callq	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEC2B8ne200100ILi0EEEPKc ## std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>::basic_string[abi:ne200100]<0>(char const*)
00000001004231b4	movq	-0x40(%rbp), %rsi
00000001004231b8	movq	%r14, %rdx
00000001004231bb	subq	%rsi, %rdx
00000001004231be	leaq	-0xa0(%rbp), %rbx
00000001004231c5	movq	%rbx, %rdi
00000001004231c8	callq	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEC2B8ne200100EPKcm ## std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>::basic_string[abi:ne200100](char const*, unsigned long)
00000001004231cd	incq	%r14
00000001004231d0	movq	%r14, -0x40(%rbp)
00000001004231d4	movq	%rbx, %rdi
00000001004231d7	movl	$0x2f, %esi
00000001004231dc	xorl	%edx, %edx
00000001004231de	callq	0x104fe8474                     ## symbol stub for: __ZNKSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE4findEcm
00000001004231e3	cmpq	$-0x1, %rax
00000001004231e7	je	0x100423284
00000001004231ed	movq	%rax, %r14
00000001004231f0	leaq	-0xe0(%rbp), %rdi
00000001004231f7	movq	%rbx, %rsi
00000001004231fa	xorl	%edx, %edx
00000001004231fc	movq	%rax, %rcx
00000001004231ff	leaq	-0xa9(%rbp), %r8
0000000100423206	callq	0x104fe855e                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEC2ERKS5_mmRKS4_
000000010042320b	testb	$0x1, -0x80(%rbp)
000000010042320f	je	0x10042321a
0000000100423211	movq	-0x70(%rbp), %rdi
0000000100423215	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
000000010042321a	movq	-0xd0(%rbp), %rax
0000000100423221	movq	%rax, -0x70(%rbp)
0000000100423225	movups	-0xe0(%rbp), %xmm0
000000010042322c	movaps	%xmm0, -0x80(%rbp)
0000000100423230	incq	%r14
0000000100423233	leaq	-0xe0(%rbp), %rdi
000000010042323a	movq	%rbx, %rsi
000000010042323d	movq	%r14, %rdx
0000000100423240	movq	$-0x1, %rcx
0000000100423247	leaq	-0xa9(%rbp), %r8
000000010042324e	callq	0x104fe855e                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEC2ERKS5_mmRKS4_
0000000100423253	testb	$0x1, -0xa0(%rbp)
000000010042325a	je	0x100423268
000000010042325c	movq	-0x90(%rbp), %rdi
0000000100423263	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
0000000100423268	movq	-0xd0(%rbp), %rax
000000010042326f	movq	%rax, -0x90(%rbp)
0000000100423276	movups	-0xe0(%rbp), %xmm0
000000010042327d	movaps	%xmm0, -0xa0(%rbp)
0000000100423284	testb	$0x1, -0x80(%rbp)
0000000100423288	leaq	-0x7f(%rbp), %rsi
000000010042328c	je	0x100423292
000000010042328e	movq	-0x70(%rbp), %rsi
0000000100423292	testb	$0x1, -0xa0(%rbp)
0000000100423299	leaq	-0x9f(%rbp), %rdx
00000001004232a0	je	0x1004232a9
00000001004232a2	movq	-0x90(%rbp), %rdx
00000001004232a9	leaq	_messageEngine(%rip), %rdi
00000001004232b0	callq	__ZN14CMessageEngine10getMessageEPKcS1_ ## CMessageEngine::getMessage(char const*, char const*)
00000001004232b5	movq	%rax, %r14
00000001004232b8	movq	%rax, %rdi
00000001004232bb	callq	0x104fe92ae                     ## symbol stub for: _strlen
00000001004232c0	movq	%r15, %rdi
00000001004232c3	movq	%r14, %rsi
00000001004232c6	movq	%rax, %rdx
00000001004232c9	callq	0x104fe8516                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm
00000001004232ce	testb	$0x1, -0xa0(%rbp)
00000001004232d5	je	0x1004232e3
00000001004232d7	movq	-0x90(%rbp), %rdi
00000001004232de	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
00000001004232e3	testb	$0x1, -0x80(%rbp)
00000001004232e7	je	0x100423002
00000001004232ed	movq	-0x70(%rbp), %rdi
00000001004232f1	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
00000001004232f6	jmp	0x100423002
00000001004232fb	movl	$msac.end, %edx
0000000100423300	movq	%r14, %rdi
0000000100423303	leaq	0x51cd462(%rip), %rsi           ## literal pool for: "leftdeck"
000000010042330a	callq	0x104fe92b4                     ## symbol stub for: _strncasecmp
000000010042330f	testl	%eax, %eax
0000000100423311	je	0x10042355f
0000000100423317	movl	$0x9, %edx
000000010042331c	movq	%r14, %rdi
000000010042331f	leaq	0x51ce060(%rip), %rsi           ## literal pool for: "rightdeck"
0000000100423326	callq	0x104fe92b4                     ## symbol stub for: _strncasecmp
000000010042332b	testl	%eax, %eax
000000010042332d	je	0x100423672
0000000100423333	leaq	0x5(%r12), %r15
0000000100423338	xorl	%r14d, %r14d
000000010042333b	movq	%r15, %rbx
000000010042333e	movl	%r13d, %eax
0000000100423341	cmpb	$0x42, %al
0000000100423343	je	0x100423362
0000000100423345	movzbl	%al, %ecx
0000000100423348	movl	$CONFIG_VP9, %eax
000000010042334d	cmpl	$0x50, %ecx
0000000100423350	je	0x100423367
0000000100423352	cmpl	$0x4c, %ecx
0000000100423355	jne	0x1004234ed
000000010042335b	movl	$0x2, %eax
0000000100423360	jmp	0x100423367
0000000100423362	movl	$FGData.num_y_points, %eax
0000000100423367	orl	%eax, %r14d
000000010042336a	movb	-0x3(%rbx), %al
000000010042336d	incq	%rbx
0000000100423370	jmp	0x100423341
0000000100423372	movq	0x8(%r15), %rbx
0000000100423376	leaq	0x1(%rbx), %rsi
000000010042337a	movq	%r15, %rdi
000000010042337d	xorl	%edx, %edx
000000010042337f	callq	0x104fe853a                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6resizeEmc
0000000100423384	testb	$0x1, CONFIG_EMULATE_HARDWARE(%r15)
0000000100423388	movq	-0xb8(%rbp), %rax
000000010042338f	je	0x100423395
0000000100423391	movq	0x10(%r15), %rax
0000000100423395	movb	%r14b, CONFIG_EMULATE_HARDWARE(%rax,%rbx)
0000000100423399	movq	-0x40(%rbp), %rax
000000010042339d	movb	CONFIG_EMULATE_HARDWARE(%rax), %cl
000000010042339f	addb	$-0x30, %cl
00000001004233a2	cmpb	$0x9, %cl
00000001004233a5	ja	0x100423002
00000001004233ab	incq	%rax
00000001004233ae	movq	%rax, -0x40(%rbp)
00000001004233b2	movb	CONFIG_EMULATE_HARDWARE(%rax), %cl
00000001004233b4	addb	$-0x30, %cl
00000001004233b7	incq	%rax
00000001004233ba	cmpb	$0xa, %cl
00000001004233bd	jb	0x1004233ae
00000001004233bf	jmp	0x100423002
00000001004233c4	cmpl	$0x72, %eax
00000001004233c7	je	0x1004235bc
00000001004233cd	cmpl	$0x74, %eax
00000001004233d0	jne	0x100423583
00000001004233d6	addq	$0x2, %r12
00000001004233da	movq	%r12, -0x40(%rbp)
00000001004233de	movzbl	CONFIG_EMULATE_HARDWARE(%r15), %ebx
00000001004233e2	testb	$0x1, %bl
00000001004233e5	jne	0x10042372e
00000001004233eb	shrl	%ebx
00000001004233ed	jmp	0x100423732
00000001004233f2	addq	$0x2, %r12
00000001004233f6	movq	%r12, -0x40(%rbp)
00000001004233fa	jmp	0x100423002
00000001004233ff	movq	0x8(%r15), %rbx
0000000100423403	leaq	0x1(%rbx), %rsi
0000000100423407	movq	%r15, %rdi
000000010042340a	xorl	%edx, %edx
000000010042340c	callq	0x104fe853a                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6resizeEmc
0000000100423411	testb	$0x1, CONFIG_EMULATE_HARDWARE(%r15)
0000000100423415	movq	-0xb8(%rbp), %rax
000000010042341c	je	0x100423422
000000010042341e	movq	0x10(%r15), %rax
0000000100423422	movb	$0x60, CONFIG_EMULATE_HARDWARE(%rax,%rbx)
0000000100423426	jmp	0x100423002
000000010042342b	movq	0x8(%r15), %rbx
000000010042342f	leaq	0x1(%rbx), %rsi
0000000100423433	movq	%r15, %rdi
0000000100423436	xorl	%edx, %edx
0000000100423438	callq	0x104fe853a                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6resizeEmc
000000010042343d	testb	$0x1, CONFIG_EMULATE_HARDWARE(%r15)
0000000100423441	movq	-0xb8(%rbp), %rax
0000000100423448	je	0x10042344e
000000010042344a	movq	0x10(%r15), %rax
000000010042344e	movb	$0x25, CONFIG_EMULATE_HARDWARE(%rax,%rbx)
0000000100423452	jmp	0x100423002
0000000100423457	movq	%rsi, %rdi
000000010042345a	xorl	%esi, %esi
000000010042345c	movl	-0xbc(%rbp), %edx
0000000100423462	callq	__ZN7IAction6createEPKcPS1_i    ## IAction::create(char const*, char const**, int)
0000000100423467	movq	%rax, %r12
000000010042346a	movb	%bl, CONFIG_EMULATE_HARDWARE(%r14)
000000010042346d	incq	%r14
0000000100423470	movq	%r14, -0x40(%rbp)
0000000100423474	testq	%rax, %rax
0000000100423477	je	0x100423002
000000010042347d	cmpq	$0x0, 0x18(%rbp)
0000000100423482	je	0x100423497
0000000100423484	movq	0x18(%rbp), %rax
0000000100423488	movl	0x18(%rax), %esi
000000010042348b	testl	%esi, %esi
000000010042348d	je	0x100423497
000000010042348f	movq	%r12, %rdi
0000000100423492	callq	__ZN7IAction9setSourceEi        ## IAction::setSource(int)
0000000100423497	xorpd	%xmm0, %xmm0
000000010042349b	movapd	%xmm0, -0x70(%rbp)
00000001004234a0	movapd	%xmm0, -0x80(%rbp)
00000001004234a5	movb	$0x0, -0x60(%rbp)
00000001004234a9	movq	%r12, %rdi
00000001004234ac	leaq	-0x80(%rbp), %rsi
00000001004234b0	movl	-0xbc(%rbp), %edx
00000001004234b6	callq	__ZN7IAction9queryTextER12SActionParamj ## IAction::queryText(SActionParam&, unsigned int)
00000001004234bb	testl	%eax, %eax
00000001004234bd	je	0x1004235d8
00000001004234c3	testb	$0x1, -0x78(%rbp)
00000001004234c7	je	0x1004234d2
00000001004234c9	movq	-0x68(%rbp), %rdi
00000001004234cd	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
00000001004234d2	lock
00000001004234d3	decl	0x8(%r12)
00000001004234d8	jg	0x100423002
00000001004234de	movq	CONFIG_EMULATE_HARDWARE(%r12), %rax
00000001004234e2	movq	%r12, %rdi
00000001004234e5	callq	*0x8(%rax)
00000001004234e8	jmp	0x100423002
00000001004234ed	leaq	-0x4(%rbx), %rdi
00000001004234f1	movl	$FGData.num_y_points, %edx
00000001004234f6	leaq	0x51db18e(%rip), %rsi           ## literal pool for: "time"
00000001004234fd	callq	0x104fe92b4                     ## symbol stub for: _strncasecmp
0000000100423502	testl	%eax, %eax
0000000100423504	je	0x1004237b2
000000010042350a	leaq	0x6(%r12), %rbx
000000010042350f	xorl	%r14d, %r14d
0000000100423512	movl	%r13d, %eax
0000000100423515	cmpb	$0x42, %al
0000000100423517	je	0x100423536
0000000100423519	movzbl	%al, %ecx
000000010042351c	movl	$CONFIG_VP9, %eax
0000000100423521	cmpl	$0x50, %ecx
0000000100423524	je	0x10042353b
0000000100423526	cmpl	$0x4c, %ecx
0000000100423529	jne	0x100423621
000000010042352f	movl	$0x2, %eax
0000000100423534	jmp	0x10042353b
0000000100423536	movl	$FGData.num_y_points, %eax
000000010042353b	orl	%eax, %r14d
000000010042353e	movb	-0x4(%rbx), %al
0000000100423541	incq	%rbx
0000000100423544	jmp	0x100423515
0000000100423546	movl	$0x2, %edx
000000010042354b	movq	%r15, %rdi
000000010042354e	leaq	0x51e2f59(%rip), %rsi           ## literal pool for: "%{"
0000000100423555	callq	0x104fe8516                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm
000000010042355a	jmp	0x100423002
000000010042355f	addq	$0x9, %r12
0000000100423563	movq	%r12, -0x40(%rbp)
0000000100423567	movzbl	CONFIG_EMULATE_HARDWARE(%r15), %ebx
000000010042356b	testb	$0x1, %bl
000000010042356e	jne	0x10042368e
0000000100423574	shrl	%ebx
0000000100423576	jmp	0x100423692
000000010042357b	addq	$0x2, %r12
000000010042357f	movq	%r12, -0x40(%rbp)
0000000100423583	movzbl	CONFIG_EMULATE_HARDWARE(%r15), %ebx
0000000100423587	testb	$0x1, %bl
000000010042358a	jne	0x100423590
000000010042358c	shrl	%ebx
000000010042358e	jmp	0x100423594
0000000100423590	movq	0x8(%r15), %rbx
0000000100423594	leaq	0x1(%rbx), %rsi
0000000100423598	movq	%r15, %rdi
000000010042359b	xorl	%edx, %edx
000000010042359d	callq	0x104fe853a                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6resizeEmc
00000001004235a2	testb	$0x1, CONFIG_EMULATE_HARDWARE(%r15)
00000001004235a6	movq	-0xb8(%rbp), %rax
00000001004235ad	je	0x1004235b3
00000001004235af	movq	0x10(%r15), %rax
00000001004235b3	movb	$0x5c, CONFIG_EMULATE_HARDWARE(%rax,%rbx)
00000001004235b7	jmp	0x100423002
00000001004235bc	addq	$0x2, %r12
00000001004235c0	movq	%r12, -0x40(%rbp)
00000001004235c4	movzbl	CONFIG_EMULATE_HARDWARE(%r15), %ebx
00000001004235c8	testb	$0x1, %bl
00000001004235cb	jne	0x100423786
00000001004235d1	shrl	%ebx
00000001004235d3	jmp	0x10042378a
00000001004235d8	movl	-0x80(%rbp), %eax
00000001004235db	cmpl	$0x696e73, %eax                 ## imm = 0x696E73
00000001004235e0	jle	0x1004237fe
00000001004235e6	cmpl	$0x76616b, %eax                 ## imm = 0x76616B
00000001004235eb	jg	0x100423977
00000001004235f1	cmpl	$0x696e74, %eax                 ## imm = 0x696E74
00000001004235f6	je	0x100423b0c
00000001004235fc	cmpl	$0x747874, %eax                 ## imm = 0x747874
0000000100423601	jne	0x1004234c3
0000000100423607	movzbl	-0x78(%rbp), %edx
000000010042360b	testb	$0x1, %dl
000000010042360e	je	0x100423c52
0000000100423614	movq	-0x68(%rbp), %rsi
0000000100423618	movq	-0x70(%rbp), %rdx
000000010042361c	jmp	0x100423c58
0000000100423621	leaq	-0x5(%rbx), %rdi
0000000100423625	movl	$0x5, %edx
000000010042362a	leaq	0x51e2e80(%rip), %rsi           ## literal pool for: "spent"
0000000100423631	callq	0x104fe92b4                     ## symbol stub for: _strncasecmp
0000000100423636	testl	%eax, %eax
0000000100423638	je	0x10042393e
000000010042363e	xorl	%r14d, %r14d
0000000100423641	movl	%r13d, %eax
0000000100423644	cmpb	$0x42, %al
0000000100423646	je	0x100423661
0000000100423648	movzbl	%al, %ecx
000000010042364b	movl	$CONFIG_VP9, %eax
0000000100423650	cmpl	$0x50, %ecx
0000000100423653	je	0x100423666
0000000100423655	cmpl	$0x4c, %ecx
0000000100423658	jne	0x10042369e
000000010042365a	movl	$0x2, %eax
000000010042365f	jmp	0x100423666
0000000100423661	movl	$FGData.num_y_points, %eax
0000000100423666	orl	%eax, %r14d
0000000100423669	movb	-0x3(%r15), %al
000000010042366d	incq	%r15
0000000100423670	jmp	0x100423644
0000000100423672	addq	$0xa, %r12
0000000100423676	movq	%r12, -0x40(%rbp)
000000010042367a	movzbl	CONFIG_EMULATE_HARDWARE(%r15), %ebx
000000010042367e	testb	$0x1, %bl
0000000100423681	jne	0x10042384f
0000000100423687	shrl	%ebx
0000000100423689	jmp	0x100423853
000000010042368e	movq	0x8(%r15), %rbx
0000000100423692	leaq	_leftDeck(%rip), %rax
0000000100423699	jmp	0x10042385a
000000010042369e	leaq	-0x4(%r15), %rdi
00000001004236a2	movl	$FGData.num_y_points, %edx
00000001004236a7	leaq	0x51c6192(%rip), %rsi           ## literal pool for: "left"
00000001004236ae	callq	0x104fe92b4                     ## symbol stub for: _strncasecmp
00000001004236b3	testl	%eax, %eax
00000001004236b5	je	0x1004239ec
00000001004236bb	addq	$0x8, %r12
00000001004236bf	xorl	%ebx, %ebx
00000001004236c1	movq	-0x30(%rbp), %r15
00000001004236c5	cmpb	$0x42, %r13b
00000001004236c9	je	0x1004236e9
00000001004236cb	movzbl	%r13b, %ecx
00000001004236cf	movl	$CONFIG_VP9, %eax
00000001004236d4	cmpl	$0x50, %ecx
00000001004236d7	je	0x1004236ee
00000001004236d9	cmpl	$0x4c, %ecx
00000001004236dc	jne	0x100423890
00000001004236e2	movl	$0x2, %eax
00000001004236e7	jmp	0x1004236ee
00000001004236e9	movl	$FGData.num_y_points, %eax
00000001004236ee	orl	%eax, %ebx
00000001004236f0	movb	-0x6(%r12), %r13b
00000001004236f5	incq	%r12
00000001004236f8	jmp	0x1004236c5
00000001004236fa	movq	0x8(%r15), %rbx
00000001004236fe	leaq	0x1(%rbx), %rsi
0000000100423702	movq	%r15, %rdi
0000000100423705	xorl	%edx, %edx
0000000100423707	callq	0x104fe853a                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6resizeEmc
000000010042370c	testb	$0x1, CONFIG_EMULATE_HARDWARE(%r15)
0000000100423710	movq	-0xb8(%rbp), %rax
0000000100423717	je	0x10042371d
0000000100423719	movq	0x10(%r15), %rax
000000010042371d	movb	$0xd, CONFIG_EMULATE_HARDWARE(%rax,%rbx)
0000000100423721	movzbl	CONFIG_EMULATE_HARDWARE(%r15), %ebx
0000000100423725	testb	$0x1, %bl
0000000100423728	jne	0x10042375a
000000010042372a	shrl	%ebx
000000010042372c	jmp	0x10042375e
000000010042372e	movq	0x8(%r15), %rbx
0000000100423732	leaq	0x1(%rbx), %rsi
0000000100423736	movq	%r15, %rdi
0000000100423739	xorl	%edx, %edx
000000010042373b	callq	0x104fe853a                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6resizeEmc
0000000100423740	testb	$0x1, CONFIG_EMULATE_HARDWARE(%r15)
0000000100423744	movq	-0xb8(%rbp), %rax
000000010042374b	je	0x100423751
000000010042374d	movq	0x10(%r15), %rax
0000000100423751	movb	$0x9, CONFIG_EMULATE_HARDWARE(%rax,%rbx)
0000000100423755	jmp	0x100423002
000000010042375a	movq	0x8(%r15), %rbx
000000010042375e	leaq	0x1(%rbx), %rsi
0000000100423762	movq	%r15, %rdi
0000000100423765	xorl	%edx, %edx
0000000100423767	callq	0x104fe853a                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6resizeEmc
000000010042376c	testb	$0x1, CONFIG_EMULATE_HARDWARE(%r15)
0000000100423770	movq	-0xb8(%rbp), %rax
0000000100423777	je	0x10042377d
0000000100423779	movq	0x10(%r15), %rax
000000010042377d	movb	$0xa, CONFIG_EMULATE_HARDWARE(%rax,%rbx)
0000000100423781	jmp	0x100423002
0000000100423786	movq	0x8(%r15), %rbx
000000010042378a	leaq	0x1(%rbx), %rsi
000000010042378e	movq	%r15, %rdi
0000000100423791	xorl	%edx, %edx
0000000100423793	callq	0x104fe853a                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6resizeEmc
0000000100423798	testb	$0x1, CONFIG_EMULATE_HARDWARE(%r15)
000000010042379c	movq	-0xb8(%rbp), %rax
00000001004237a3	je	0x1004237a9
00000001004237a5	movq	0x10(%r15), %rax
00000001004237a9	movb	$0xd, CONFIG_EMULATE_HARDWARE(%rax,%rbx)
00000001004237ad	jmp	0x100423002
00000001004237b2	movq	%rbx, -0x40(%rbp)
00000001004237b6	movl	%r14d, -0x34(%rbp)
00000001004237ba	movq	-0xc8(%rbp), %rdx
00000001004237c1	movl	0x244(%rdx), %eax
00000001004237c7	testl	%eax, %eax
00000001004237c9	setle	%cl
00000001004237cc	cmpl	$-0x3, %eax
00000001004237cf	setne	%al
00000001004237d2	testb	%al, %cl
00000001004237d4	jne	0x1004247fe
00000001004237da	xorps	%xmm0, %xmm0
00000001004237dd	cvtsi2sdq	0x250(%rdx), %xmm0
00000001004237e6	movq	-0x30(%rbp), %r15
00000001004237ea	movq	%r15, %rdi
00000001004237ed	movl	%r14d, %esi
00000001004237f0	movq	-0x48(%rbp), %rdx
00000001004237f4	callq	__Z9writeTimePNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEdjP5CDeck ## writeTime(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>*, double, unsigned int, CDeck*)
00000001004237f9	jmp	0x100423002
00000001004237fe	cmpl	$0x25, %eax
0000000100423801	je	0x1004239ad
0000000100423807	cmpl	$0x6d73, %eax                   ## imm = 0x6D73
000000010042380c	je	0x100423b3e
0000000100423812	cmpl	$0x636f6c, %eax                 ## imm = 0x636F6C
0000000100423817	jne	0x1004234c3
000000010042381d	movl	-0x7c(%rbp), %esi
0000000100423820	leaq	-0xa0(%rbp), %rdi
0000000100423827	callq	__Z10colorToStrj                ## colorToStr(unsigned int)
000000010042382c	movzbl	-0xa0(%rbp), %edx
0000000100423833	testb	$0x1, %dl
0000000100423836	je	0x100423c78
000000010042383c	movq	-0x90(%rbp), %rsi
0000000100423843	movq	-0x98(%rbp), %rdx
000000010042384a	jmp	0x100423c81
000000010042384f	movq	0x8(%r15), %rbx
0000000100423853	leaq	_rightDeck(%rip), %rax
000000010042385a	movq	CONFIG_EMULATE_HARDWARE(%rax), %rax
000000010042385d	movb	0x240(%rax), %r14b
0000000100423864	leaq	0x1(%rbx), %rsi
0000000100423868	movq	%r15, %rdi
000000010042386b	xorl	%edx, %edx
000000010042386d	callq	0x104fe853a                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6resizeEmc
0000000100423872	testb	$0x1, CONFIG_EMULATE_HARDWARE(%r15)
0000000100423876	movq	-0xb8(%rbp), %rax
000000010042387d	je	0x100423883
000000010042387f	movq	0x10(%r15), %rax
0000000100423883	addb	$0x41, %r14b
0000000100423887	movb	%r14b, CONFIG_EMULATE_HARDWARE(%rax,%rbx)
000000010042388b	jmp	0x100423002
0000000100423890	leaq	-0x7(%r12), %rdi
0000000100423895	movl	$0x7, %edx
000000010042389a	leaq	0x51e2c16(%rip), %rsi           ## literal pool for: "looppos"
00000001004238a1	callq	0x104fe92b4                     ## symbol stub for: _strncasecmp
00000001004238a6	testl	%eax, %eax
00000001004238a8	je	0x100423a31
00000001004238ae	leaq	-0x40(%rbp), %rbx
00000001004238b2	movq	%rbx, %rdi
00000001004238b5	leaq	0x51c3fa4(%rip), %rsi           ## literal pool for: "loop"
00000001004238bc	movl	$FGData.num_y_points, %edx
00000001004238c1	leaq	-0x34(%rbp), %r13
00000001004238c5	movq	%r13, %rcx
00000001004238c8	callq	__Z19matchStringWithFlagRPKcS0_iRj ## matchStringWithFlag(char const*&, char const*, int, unsigned int&)
00000001004238cd	testb	%al, %al
00000001004238cf	movq	-0x50(%rbp), %r14
00000001004238d3	je	0x100423bd1
00000001004238d9	movq	-0x48(%rbp), %rax
00000001004238dd	movss	0x2f0(%rax), %xmm0
00000001004238e5	xorps	%xmm1, %xmm1
00000001004238e8	ucomiss	%xmm1, %xmm0
00000001004238eb	jne	0x1004238f7
00000001004238ed	jp	0x1004238f7
00000001004238ef	movss	0x2f4(%rax), %xmm0
00000001004238f7	ucomiss	%xmm1, %xmm0
00000001004238fa	jne	0x100423902
00000001004238fc	jnp	0x100423d5e
0000000100423902	movaps	%xmm0, %xmm1
0000000100423905	addss	0x4d715af(%rip), %xmm1
000000010042390d	andps	0x4d69d7c(%rip), %xmm1
0000000100423914	movss	0x4d69df8(%rip), %xmm2
000000010042391c	ucomiss	%xmm1, %xmm2
000000010042391f	jbe	0x100423d77
0000000100423925	movl	$0x3, %edx
000000010042392a	movq	%r15, %rdi
000000010042392d	leaq	0x51e2b8b(%rip), %rsi           ## literal pool for: "3/4"
0000000100423934	callq	0x104fe8516                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm
0000000100423939	jmp	0x100423002
000000010042393e	movq	%rbx, -0x40(%rbp)
0000000100423942	movl	%r14d, -0x34(%rbp)
0000000100423946	movq	-0xc8(%rbp), %rax
000000010042394d	movl	0x244(%rax), %eax
0000000100423953	testl	%eax, %eax
0000000100423955	setle	%cl
0000000100423958	cmpl	$-0x3, %eax
000000010042395b	setne	%al
000000010042395e	testb	%al, %cl
0000000100423960	jne	0x1004247fe
0000000100423966	movq	-0x48(%rbp), %rdx
000000010042396a	movsd	0x2a8(%rdx), %xmm0
0000000100423972	jmp	0x100423a1d
0000000100423977	cmpl	$0x76616c, %eax                 ## imm = 0x76616C
000000010042397c	je	0x1004239ad
000000010042397e	cmpl	$0x626f6f6c, %eax               ## imm = 0x626F6F6C
0000000100423983	jne	0x1004234c3
0000000100423989	xorl	%edx, %edx
000000010042398b	cmpl	$0x0, -0x7c(%rbp)
000000010042398f	setg	%dl
0000000100423992	leaq	0x51d3fbd(%rip), %rsi           ## literal pool for: "off"
0000000100423999	leaq	0x51b9068(%rip), %rax           ## literal pool for: "on"
00000001004239a0	cmovgq	%rax, %rsi
00000001004239a4	xorq	$0x3, %rdx
00000001004239a8	jmp	0x100423cd9
00000001004239ad	xorps	%xmm0, %xmm0
00000001004239b0	cvtss2sd	-0x7c(%rbp), %xmm0
00000001004239b5	mulsd	0x4d69b1b(%rip), %xmm0
00000001004239bd	leaq	-0xa0(%rbp), %rdi
00000001004239c4	callq	__Z12dblToStrDot2d              ## dblToStrDot2(double)
00000001004239c9	movzbl	-0xa0(%rbp), %edx
00000001004239d0	testb	$0x1, %dl
00000001004239d3	je	0x100423b72
00000001004239d9	movq	-0x90(%rbp), %rsi
00000001004239e0	movq	-0x98(%rbp), %rdx
00000001004239e7	jmp	0x100423b7b
00000001004239ec	movq	%r15, -0x40(%rbp)
00000001004239f0	movl	%r14d, -0x34(%rbp)
00000001004239f4	movq	-0xc8(%rbp), %rax
00000001004239fb	cmpl	$0x0, 0x244(%rax)
0000000100423a02	jle	0x1004247fe
0000000100423a08	cvtsi2sdq	0x250(%rax), %xmm0
0000000100423a11	movq	-0x48(%rbp), %rdx
0000000100423a15	subsd	0x2a8(%rdx), %xmm0
0000000100423a1d	movq	-0x30(%rbp), %r15
0000000100423a21	movq	%r15, %rdi
0000000100423a24	movl	%r14d, %esi
0000000100423a27	callq	__Z9writeTimePNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEdjP5CDeck ## writeTime(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>*, double, unsigned int, CDeck*)
0000000100423a2c	jmp	0x100423002
0000000100423a31	movq	%r12, -0x40(%rbp)
0000000100423a35	movl	%ebx, -0x34(%rbp)
0000000100423a38	movq	-0x48(%rbp), %rbx
0000000100423a3c	movss	0x2f0(%rbx), %xmm0
0000000100423a44	movss	%xmm0, -0xa8(%rbp)
0000000100423a4c	movq	%rbx, %rdi
0000000100423a4f	callq	__ZN5CDeck13getLoopLengthEv     ## CDeck::getLoopLength()
0000000100423a54	movss	-0xa8(%rbp), %xmm3
0000000100423a5c	ucomiss	0x4d934f1(%rip), %xmm3
0000000100423a63	jbe	0x100423002
0000000100423a69	leaq	_Config(%rip), %rax
0000000100423a70	cvtsi2ssl	0x3c8(%rax), %xmm1
0000000100423a78	mulss	0x4d69c94(%rip), %xmm1
0000000100423a80	ucomiss	%xmm3, %xmm1
0000000100423a83	jbe	0x100423002
0000000100423a89	ucomiss	0x4d69a44(%rip), %xmm0
0000000100423a90	jne	0x100423a98
0000000100423a92	jnp	0x100423002
0000000100423a98	movsd	0x2a8(%rbx), %xmm1
0000000100423aa0	cvtsi2ssq	0x2e0(%rbx), %xmm2
0000000100423aa9	subss	%xmm0, %xmm2
0000000100423aad	cvtss2sd	%xmm2, %xmm2
0000000100423ab1	subsd	%xmm2, %xmm1
0000000100423ab5	cvtsd2ss	%xmm1, %xmm1
0000000100423ab9	divss	%xmm0, %xmm1
0000000100423abd	movss	0x4d69243(%rip), %xmm0
0000000100423ac5	minss	%xmm1, %xmm0
0000000100423ac9	movss	0x4d6f10f(%rip), %xmm2
0000000100423ad1	cmpnless	%xmm2, %xmm1
0000000100423ad6	andps	%xmm1, %xmm0
0000000100423ad9	andnps	%xmm2, %xmm1
0000000100423adc	orps	%xmm0, %xmm1
0000000100423adf	mulss	%xmm1, %xmm3
0000000100423ae3	xorps	%xmm0, %xmm0
0000000100423ae6	roundss	$0xa, %xmm3, %xmm0
0000000100423aec	cvttss2si	%xmm0, %esi
0000000100423af0	leaq	-0x80(%rbp), %rbx
0000000100423af4	movq	%rbx, %rdi
0000000100423af7	callq	__Z8intToStri                   ## intToStr(int)
0000000100423afc	movq	%r15, %rdi
0000000100423aff	movq	%rbx, %rsi
0000000100423b02	callq	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendB8ne200100ERKS5_ ## std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>::append[abi:ne200100](std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&)
0000000100423b07	jmp	0x1004232e3
0000000100423b0c	movl	-0x7c(%rbp), %esi
0000000100423b0f	leaq	-0xa0(%rbp), %rdi
0000000100423b16	callq	__Z8intToStri                   ## intToStr(int)
0000000100423b1b	movzbl	-0xa0(%rbp), %edx
0000000100423b22	testb	$0x1, %dl
0000000100423b25	je	0x100423c65
0000000100423b2b	movq	-0x90(%rbp), %rsi
0000000100423b32	movq	-0x98(%rbp), %rdx
0000000100423b39	jmp	0x100423c6e
0000000100423b3e	movss	-0x7c(%rbp), %xmm0
0000000100423b43	leaq	-0xa0(%rbp), %rdi
0000000100423b4a	callq	__Z12dblToStrDot2f              ## dblToStrDot2(float)
0000000100423b4f	movzbl	-0xa0(%rbp), %edx
0000000100423b56	testb	$0x1, %dl
0000000100423b59	je	0x100423ca7
0000000100423b5f	movq	-0x90(%rbp), %rsi
0000000100423b66	movq	-0x98(%rbp), %rdx
0000000100423b6d	jmp	0x100423cb0
0000000100423b72	shrl	%edx
0000000100423b74	leaq	-0x9f(%rbp), %rsi
0000000100423b7b	movq	%r15, %rdi
0000000100423b7e	callq	0x104fe8516                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm
0000000100423b83	testb	$0x1, -0xa0(%rbp)
0000000100423b8a	je	0x100423b98
0000000100423b8c	movq	-0x90(%rbp), %rdi
0000000100423b93	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
0000000100423b98	movzbl	CONFIG_EMULATE_HARDWARE(%r15), %ebx
0000000100423b9c	testb	$0x1, %bl
0000000100423b9f	jne	0x100423ba5
0000000100423ba1	shrl	%ebx
0000000100423ba3	jmp	0x100423ba9
0000000100423ba5	movq	0x8(%r15), %rbx
0000000100423ba9	leaq	0x1(%rbx), %rsi
0000000100423bad	movq	%r15, %rdi
0000000100423bb0	xorl	%edx, %edx
0000000100423bb2	callq	0x104fe853a                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6resizeEmc
0000000100423bb7	testb	$0x1, CONFIG_EMULATE_HARDWARE(%r15)
0000000100423bbb	movq	-0xb8(%rbp), %rax
0000000100423bc2	je	0x100423bc8
0000000100423bc4	movq	0x10(%r15), %rax
0000000100423bc8	movb	$0x25, CONFIG_EMULATE_HARDWARE(%rax,%rbx)
0000000100423bcc	jmp	0x1004234c3
0000000100423bd1	movq	%rbx, %rdi
0000000100423bd4	leaq	0x51e28f0(%rip), %rsi           ## literal pool for: "namecue"
0000000100423bdb	movl	$0x7, %edx
0000000100423be0	movq	%r13, %rcx
0000000100423be3	callq	__Z19matchStringWithFlagRPKcS0_iRj ## matchStringWithFlag(char const*&, char const*, int, unsigned int&)
0000000100423be8	testb	%al, %al
0000000100423bea	je	0x100423ce6
0000000100423bf0	movq	-0x40(%rbp), %rax
0000000100423bf4	movb	CONFIG_EMULATE_HARDWARE(%rax), %cl
0000000100423bf6	leal	-0x30(%rcx), %edx
0000000100423bf9	xorl	%esi, %esi
0000000100423bfb	cmpb	$0x9, %dl
0000000100423bfe	ja	0x100423c22
0000000100423c00	incq	%rax
0000000100423c03	xorl	%esi, %esi
0000000100423c05	leal	CONFIG_EMULATE_HARDWARE(%rsi,%rsi,4), %edx
0000000100423c08	addb	$-0x30, %cl
0000000100423c0b	movzbl	%cl, %ecx
0000000100423c0e	leal	CONFIG_EMULATE_HARDWARE(%rcx,%rdx,2), %esi
0000000100423c11	movq	%rax, -0x40(%rbp)
0000000100423c15	movb	CONFIG_EMULATE_HARDWARE(%rax), %cl
0000000100423c17	leal	-0x30(%rcx), %edx
0000000100423c1a	incq	%rax
0000000100423c1d	cmpb	$0xa, %dl
0000000100423c20	jb	0x100423c05
0000000100423c22	movq	%r14, %rdi
0000000100423c25	callq	__ZN7SDBInfo6getCueEi           ## SDBInfo::getCue(int)
0000000100423c2a	testq	%rax, %rax
0000000100423c2d	je	0x100423002
0000000100423c33	leaq	-0x80(%rbp), %rbx
0000000100423c37	movq	%rbx, %rdi
0000000100423c3a	movq	%rax, %rsi
0000000100423c3d	callq	__ZNK4SPoi7getNameEv            ## SPoi::getName() const
0000000100423c42	movq	%r15, %rdi
0000000100423c45	movq	%rbx, %rsi
0000000100423c48	callq	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendB8ne200100ERKS5_ ## std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>::append[abi:ne200100](std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&)
0000000100423c4d	jmp	0x1004232e3
0000000100423c52	shrl	%edx
0000000100423c54	leaq	-0x77(%rbp), %rsi
0000000100423c58	movq	%r15, %rdi
0000000100423c5b	callq	0x104fe8516                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm
0000000100423c60	jmp	0x1004234c3
0000000100423c65	shrl	%edx
0000000100423c67	leaq	-0x9f(%rbp), %rsi
0000000100423c6e	movq	%r15, %rdi
0000000100423c71	callq	0x104fe8516                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm
0000000100423c76	jmp	0x100423c89
0000000100423c78	shrl	%edx
0000000100423c7a	leaq	-0x9f(%rbp), %rsi
0000000100423c81	movq	%r15, %rdi
0000000100423c84	callq	0x104fe8516                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm
0000000100423c89	testb	$0x1, -0xa0(%rbp)
0000000100423c90	je	0x1004234c3
0000000100423c96	movq	-0x90(%rbp), %rdi
0000000100423c9d	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
0000000100423ca2	jmp	0x1004234c3
0000000100423ca7	shrl	%edx
0000000100423ca9	leaq	-0x9f(%rbp), %rsi
0000000100423cb0	movq	%r15, %rdi
0000000100423cb3	callq	0x104fe8516                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm
0000000100423cb8	testb	$0x1, -0xa0(%rbp)
0000000100423cbf	je	0x100423ccd
0000000100423cc1	movq	-0x90(%rbp), %rdi
0000000100423cc8	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
0000000100423ccd	movl	$0x2, %edx
0000000100423cd2	leaq	0x51b8d35(%rip), %rsi           ## literal pool for: "ms"
0000000100423cd9	movq	%r15, %rdi
0000000100423cdc	callq	0x104fe8516                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm
0000000100423ce1	jmp	0x1004234c3
0000000100423ce6	movq	%rbx, %rdi
0000000100423ce9	leaq	0x51c626f(%rip), %rsi           ## literal pool for: "cue"
0000000100423cf0	movl	$0x3, %edx
0000000100423cf5	movq	%r13, %rcx
0000000100423cf8	callq	__Z19matchStringWithFlagRPKcS0_iRj ## matchStringWithFlag(char const*&, char const*, int, unsigned int&)
0000000100423cfd	testb	%al, %al
0000000100423cff	je	0x100423dd9
0000000100423d05	movq	-0x40(%rbp), %rax
0000000100423d09	movb	CONFIG_EMULATE_HARDWARE(%rax), %cl
0000000100423d0b	leal	-0x30(%rcx), %edx
0000000100423d0e	xorl	%esi, %esi
0000000100423d10	cmpb	$0x9, %dl
0000000100423d13	movq	-0x48(%rbp), %rbx
0000000100423d17	ja	0x100423d3b
0000000100423d19	incq	%rax
0000000100423d1c	xorl	%esi, %esi
0000000100423d1e	leal	CONFIG_EMULATE_HARDWARE(%rsi,%rsi,4), %edx
0000000100423d21	addb	$-0x30, %cl
0000000100423d24	movzbl	%cl, %ecx
0000000100423d27	leal	CONFIG_EMULATE_HARDWARE(%rcx,%rdx,2), %esi
0000000100423d2a	movq	%rax, -0x40(%rbp)
0000000100423d2e	movb	CONFIG_EMULATE_HARDWARE(%rax), %cl
0000000100423d30	leal	-0x30(%rcx), %edx
0000000100423d33	incq	%rax
0000000100423d36	cmpb	$0xa, %dl
0000000100423d39	jb	0x100423d1e
0000000100423d3b	movq	%r14, %rdi
0000000100423d3e	callq	__ZN7SDBInfo6getCueEi           ## SDBInfo::getCue(int)
0000000100423d43	testq	%rax, %rax
0000000100423d46	je	0x100423002
0000000100423d4c	cvtsi2sdl	0xfa0(%rbx), %xmm0
0000000100423d54	mulsd	0x8(%rax), %xmm0
0000000100423d59	jmp	0x100423e54
0000000100423d5e	movl	$CONFIG_VP9, %edx
0000000100423d63	movq	%r15, %rdi
0000000100423d66	leaq	0x51d2d35(%rip), %rsi           ## literal pool for: "?"
0000000100423d6d	callq	0x104fe8516                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm
0000000100423d72	jmp	0x100423002
0000000100423d77	movss	0x4d6fd75(%rip), %xmm1
0000000100423d7f	ucomiss	%xmm0, %xmm1
0000000100423d82	leaq	-0xa0(%rbp), %r14
0000000100423d89	jbe	0x100423e67
0000000100423d8f	movss	0x4d68f71(%rip), %xmm1
0000000100423d97	divss	%xmm0, %xmm1
0000000100423d9b	movaps	%xmm1, %xmm0
0000000100423d9e	callq	0x104fe8e6a                     ## symbol stub for: _lroundf
0000000100423da3	movl	%eax, -0xa0(%rbp)
0000000100423da9	movl	$FGData.num_y_points, %edx
0000000100423dae	movl	$CONFIG_VP9, %ecx
0000000100423db3	leaq	-0x80(%rbp), %rbx
0000000100423db7	movq	%rbx, %rdi
0000000100423dba	leaq	0x51c7fda(%rip), %rsi           ## literal pool for: "1/{}"
0000000100423dc1	movq	%r14, %r8
0000000100423dc4	callq	__ZN3fmt3v127vformatENS0_17basic_string_viewIcEENS0_17basic_format_argsINS0_7contextEEE ## fmt::v12::vformat(fmt::v12::basic_string_view<char>, fmt::v12::basic_format_args<fmt::v12::context>)
0000000100423dc9	movq	%r15, %rdi
0000000100423dcc	movq	%rbx, %rsi
0000000100423dcf	callq	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendB8ne200100ERKS5_ ## std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>::append[abi:ne200100](std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&)
0000000100423dd4	jmp	0x1004232e3
0000000100423dd9	movq	%rbx, %rdi
0000000100423ddc	leaq	0x51e26f0(%rip), %rsi           ## literal pool for: "tocue"
0000000100423de3	movl	$0x5, %edx
0000000100423de8	movq	%r13, %rcx
0000000100423deb	callq	__Z19matchStringWithFlagRPKcS0_iRj ## matchStringWithFlag(char const*&, char const*, int, unsigned int&)
0000000100423df0	testb	%al, %al
0000000100423df2	je	0x100423ea3
0000000100423df8	movq	-0x40(%rbp), %rax
0000000100423dfc	movb	CONFIG_EMULATE_HARDWARE(%rax), %cl
0000000100423dfe	leal	-0x30(%rcx), %edx
0000000100423e01	xorl	%esi, %esi
0000000100423e03	cmpb	$0x9, %dl
0000000100423e06	movq	-0x48(%rbp), %rbx
0000000100423e0a	ja	0x100423e2e
0000000100423e0c	incq	%rax
0000000100423e0f	xorl	%esi, %esi
0000000100423e11	leal	CONFIG_EMULATE_HARDWARE(%rsi,%rsi,4), %edx
0000000100423e14	addb	$-0x30, %cl
0000000100423e17	movzbl	%cl, %ecx
0000000100423e1a	leal	CONFIG_EMULATE_HARDWARE(%rcx,%rdx,2), %esi
0000000100423e1d	movq	%rax, -0x40(%rbp)
0000000100423e21	movb	CONFIG_EMULATE_HARDWARE(%rax), %cl
0000000100423e23	leal	-0x30(%rcx), %edx
0000000100423e26	incq	%rax
0000000100423e29	cmpb	$0xa, %dl
0000000100423e2c	jb	0x100423e11
0000000100423e2e	movq	%r14, %rdi
0000000100423e31	callq	__ZN7SDBInfo6getCueEi           ## SDBInfo::getCue(int)
0000000100423e36	testq	%rax, %rax
0000000100423e39	je	0x100423002
0000000100423e3f	cvtsi2sdl	0xfa0(%rbx), %xmm0
0000000100423e47	mulsd	0x8(%rax), %xmm0
0000000100423e4c	subsd	0x2a8(%rbx), %xmm0
0000000100423e54	movl	-0x34(%rbp), %esi
0000000100423e57	movq	%r15, %rdi
0000000100423e5a	movq	%rbx, %rdx
0000000100423e5d	callq	__Z9writeTimePNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEdjP5CDeck ## writeTime(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>*, double, unsigned int, CDeck*)
0000000100423e62	jmp	0x100423002
0000000100423e67	movaps	%xmm0, %xmm1
0000000100423e6a	addss	0x4d6a10a(%rip), %xmm1
0000000100423e72	andps	0x4d69817(%rip), %xmm1
0000000100423e79	movss	0x4d69893(%rip), %xmm2
0000000100423e81	ucomiss	%xmm1, %xmm2
0000000100423e84	jbe	0x100423f39
0000000100423e8a	movl	$0x3, %edx
0000000100423e8f	movq	%r15, %rdi
0000000100423e92	leaq	0x51e262a(%rip), %rsi           ## literal pool for: "3/2"
0000000100423e99	callq	0x104fe8516                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm
0000000100423e9e	jmp	0x100423002
0000000100423ea3	movq	%rbx, %rdi
0000000100423ea6	leaq	0x51e262c(%rip), %rsi           ## literal pool for: "fromcue"
0000000100423ead	movl	$0x7, %edx
0000000100423eb2	movq	%r13, %rcx
0000000100423eb5	callq	__Z19matchStringWithFlagRPKcS0_iRj ## matchStringWithFlag(char const*&, char const*, int, unsigned int&)
0000000100423eba	testb	%al, %al
0000000100423ebc	movq	-0x48(%rbp), %r12
0000000100423ec0	je	0x100423f7b
0000000100423ec6	movq	-0x40(%rbp), %rax
0000000100423eca	movb	CONFIG_EMULATE_HARDWARE(%rax), %cl
0000000100423ecc	leal	-0x30(%rcx), %edx
0000000100423ecf	xorl	%esi, %esi
0000000100423ed1	cmpb	$0x9, %dl
0000000100423ed4	ja	0x100423ef8
0000000100423ed6	incq	%rax
0000000100423ed9	xorl	%esi, %esi
0000000100423edb	leal	CONFIG_EMULATE_HARDWARE(%rsi,%rsi,4), %edx
0000000100423ede	addb	$-0x30, %cl
0000000100423ee1	movzbl	%cl, %ecx
0000000100423ee4	leal	CONFIG_EMULATE_HARDWARE(%rcx,%rdx,2), %esi
0000000100423ee7	movq	%rax, -0x40(%rbp)
0000000100423eeb	movb	CONFIG_EMULATE_HARDWARE(%rax), %cl
0000000100423eed	leal	-0x30(%rcx), %edx
0000000100423ef0	incq	%rax
0000000100423ef3	cmpb	$0xa, %dl
0000000100423ef6	jb	0x100423edb
0000000100423ef8	movq	%r14, %rdi
0000000100423efb	callq	__ZN7SDBInfo6getCueEi           ## SDBInfo::getCue(int)
0000000100423f00	testq	%rax, %rax
0000000100423f03	je	0x100423002
0000000100423f09	movsd	0x2a8(%r12), %xmm0
0000000100423f13	cvtsi2sdl	0xfa0(%r12), %xmm1
0000000100423f1d	mulsd	0x8(%rax), %xmm1
0000000100423f22	subsd	%xmm1, %xmm0
0000000100423f26	movl	-0x34(%rbp), %esi
0000000100423f29	movq	%r15, %rdi
0000000100423f2c	movq	%r12, %rdx
0000000100423f2f	callq	__Z9writeTimePNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEdjP5CDeck ## writeTime(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>*, double, unsigned int, CDeck*)
0000000100423f34	jmp	0x100423002
0000000100423f39	leaq	_Config(%rip), %rax
0000000100423f40	xorps	%xmm1, %xmm1
0000000100423f43	cvtsi2ssl	0x3c8(%rax), %xmm1
0000000100423f4b	mulss	%xmm2, %xmm1
0000000100423f4f	ucomiss	%xmm0, %xmm1
0000000100423f52	jbe	0x10042403e
0000000100423f58	callq	0x104fe8e6a                     ## symbol stub for: _lroundf
0000000100423f5d	leaq	-0x80(%rbp), %rbx
0000000100423f61	movq	%rbx, %rdi
0000000100423f64	movl	%eax, %esi
0000000100423f66	callq	__Z8intToStri                   ## intToStr(int)
0000000100423f6b	movq	%r15, %rdi
0000000100423f6e	movq	%rbx, %rsi
0000000100423f71	callq	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendB8ne200100ERKS5_ ## std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>::append[abi:ne200100](std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&)
0000000100423f76	jmp	0x1004232e3
0000000100423f7b	movq	%rbx, %rdi
0000000100423f7e	leaq	0x51e255c(%rip), %rsi           ## literal pool for: "nextcuename"
0000000100423f85	movl	$0xb, %edx
0000000100423f8a	movq	%r13, %rcx
0000000100423f8d	callq	__Z19matchStringWithFlagRPKcS0_iRj ## matchStringWithFlag(char const*&, char const*, int, unsigned int&)
0000000100423f92	testb	%al, %al
0000000100423f94	je	0x100424057
0000000100423f9a	movsd	0x2a8(%r12), %xmm0
0000000100423fa4	movsd	%xmm0, -0xa8(%rbp)
0000000100423fac	movl	0xfa0(%r12), %ebx
0000000100423fb4	movq	%r14, %rdi
0000000100423fb7	callq	__ZN7SDBInfo12getPoiVectorEv    ## SDBInfo::getPoiVector()
0000000100423fbc	movq	CONFIG_EMULATE_HARDWARE(%rax), %rcx
0000000100423fbf	movq	0x8(%rax), %rax
0000000100423fc3	cmpq	%rax, %rcx
0000000100423fc6	je	0x100423002
0000000100423fcc	xorps	%xmm0, %xmm0
0000000100423fcf	cvtsi2sd	%ebx, %xmm0
0000000100423fd3	movsd	-0xa8(%rbp), %xmm1
0000000100423fdb	divsd	%xmm0, %xmm1
0000000100423fdf	xorps	%xmm0, %xmm0
0000000100423fe2	cvtsd2ss	%xmm1, %xmm0
0000000100423fe6	cvtss2sd	%xmm0, %xmm0
0000000100423fea	xorl	%esi, %esi
0000000100423fec	cmpl	$0x0, 0x10(%rcx)
0000000100423ff0	je	0x100424010
0000000100423ff2	movsd	0x8(%rcx), %xmm1
0000000100423ff7	ucomisd	%xmm0, %xmm1
0000000100423ffb	jbe	0x100424010
0000000100423ffd	testq	%rsi, %rsi
0000000100424000	je	0x10042400d
0000000100424002	movsd	0x8(%rsi), %xmm2
0000000100424007	ucomisd	%xmm1, %xmm2
000000010042400b	jbe	0x100424010
000000010042400d	movq	%rcx, %rsi
0000000100424010	addq	$0x38, %rcx
0000000100424014	cmpq	%rax, %rcx
0000000100424017	jne	0x100423fec
0000000100424019	testq	%rsi, %rsi
000000010042401c	je	0x100423002
0000000100424022	leaq	-0x80(%rbp), %rbx
0000000100424026	movq	%rbx, %rdi
0000000100424029	callq	__ZNK4SPoi7getNameEv            ## SPoi::getName() const
000000010042402e	movq	%r15, %rdi
0000000100424031	movq	%rbx, %rsi
0000000100424034	callq	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendB8ne200100ERKS5_ ## std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>::append[abi:ne200100](std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&)
0000000100424039	jmp	0x1004232e3
000000010042403e	movl	$0x3, %edx
0000000100424043	movq	%r15, %rdi
0000000100424046	leaq	0x51e247a(%rip), %rsi           ## literal pool for: "<->"
000000010042404d	callq	0x104fe8516                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm
0000000100424052	jmp	0x100423002
0000000100424057	movq	%rbx, %rdi
000000010042405a	leaq	0x51e248c(%rip), %rsi           ## literal pool for: "prevcuename"
0000000100424061	movl	$0xb, %edx
0000000100424066	movq	%r13, %rcx
0000000100424069	callq	__Z19matchStringWithFlagRPKcS0_iRj ## matchStringWithFlag(char const*&, char const*, int, unsigned int&)
000000010042406e	testb	%al, %al
0000000100424070	je	0x100424116
0000000100424076	movsd	0x2a8(%r12), %xmm0
0000000100424080	movsd	%xmm0, -0xa8(%rbp)
0000000100424088	movl	0xfa0(%r12), %ebx
0000000100424090	movq	%r14, %rdi
0000000100424093	callq	__ZN7SDBInfo12getPoiVectorEv    ## SDBInfo::getPoiVector()
0000000100424098	movq	CONFIG_EMULATE_HARDWARE(%rax), %rcx
000000010042409b	movq	0x8(%rax), %rax
000000010042409f	cmpq	%rax, %rcx
00000001004240a2	je	0x100423002
00000001004240a8	xorps	%xmm0, %xmm0
00000001004240ab	cvtsi2sd	%ebx, %xmm0
00000001004240af	movsd	-0xa8(%rbp), %xmm1
00000001004240b7	divsd	%xmm0, %xmm1
00000001004240bb	xorps	%xmm0, %xmm0
00000001004240be	cvtsd2ss	%xmm1, %xmm0
00000001004240c2	cvtss2sd	%xmm0, %xmm0
00000001004240c6	xorl	%esi, %esi
00000001004240c8	cmpl	$0x0, 0x10(%rcx)
00000001004240cc	je	0x1004240e8
00000001004240ce	movsd	0x8(%rcx), %xmm1
00000001004240d3	ucomisd	%xmm1, %xmm0
00000001004240d7	jb	0x1004240e8
00000001004240d9	testq	%rsi, %rsi
00000001004240dc	je	0x1004240e5
00000001004240de	ucomisd	0x8(%rsi), %xmm1
00000001004240e3	jbe	0x1004240e8
00000001004240e5	movq	%rcx, %rsi
00000001004240e8	addq	$0x38, %rcx
00000001004240ec	cmpq	%rax, %rcx
00000001004240ef	jne	0x1004240c8
00000001004240f1	testq	%rsi, %rsi
00000001004240f4	je	0x100423002
00000001004240fa	leaq	-0x80(%rbp), %rbx
00000001004240fe	movq	%rbx, %rdi
0000000100424101	callq	__ZNK4SPoi7getNameEv            ## SPoi::getName() const
0000000100424106	movq	%r15, %rdi
0000000100424109	movq	%rbx, %rsi
000000010042410c	callq	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendB8ne200100ERKS5_ ## std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>::append[abi:ne200100](std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&)
0000000100424111	jmp	0x1004232e3
0000000100424116	movq	%rbx, %rdi
0000000100424119	leaq	0x51e23d9(%rip), %rsi           ## literal pool for: "nextcue"
0000000100424120	movl	$0x7, %edx
0000000100424125	movq	%r13, %rcx
0000000100424128	callq	__Z19matchStringWithFlagRPKcS0_iRj ## matchStringWithFlag(char const*&, char const*, int, unsigned int&)
000000010042412d	testb	%al, %al
000000010042412f	je	0x1004241cb
0000000100424135	movsd	0x2a8(%r12), %xmm0
000000010042413f	movsd	%xmm0, -0xa8(%rbp)
0000000100424147	movl	0xfa0(%r12), %ebx
000000010042414f	movq	%r14, %rdi
0000000100424152	callq	__ZN7SDBInfo12getPoiVectorEv    ## SDBInfo::getPoiVector()
0000000100424157	movq	CONFIG_EMULATE_HARDWARE(%rax), %rcx
000000010042415a	movq	0x8(%rax), %rax
000000010042415e	cmpq	%rax, %rcx
0000000100424161	je	0x100423002
0000000100424167	xorps	%xmm0, %xmm0
000000010042416a	cvtsi2sd	%ebx, %xmm0
000000010042416e	movsd	-0xa8(%rbp), %xmm1
0000000100424176	divsd	%xmm0, %xmm1
000000010042417a	xorps	%xmm0, %xmm0
000000010042417d	cvtsd2ss	%xmm1, %xmm0
0000000100424181	cvtss2sd	%xmm0, %xmm0
0000000100424185	xorl	%edx, %edx
0000000100424187	cmpl	$0x0, 0x10(%rcx)
000000010042418b	je	0x1004241ab
000000010042418d	movsd	0x8(%rcx), %xmm1
0000000100424192	ucomisd	%xmm0, %xmm1
0000000100424196	jbe	0x1004241ab
0000000100424198	testq	%rdx, %rdx
000000010042419b	je	0x1004241a8
000000010042419d	movsd	0x8(%rdx), %xmm2
00000001004241a2	ucomisd	%xmm1, %xmm2
00000001004241a6	jbe	0x1004241ab
00000001004241a8	movq	%rcx, %rdx
00000001004241ab	addq	$0x38, %rcx
00000001004241af	cmpq	%rax, %rcx
00000001004241b2	jne	0x100424187
00000001004241b4	testq	%rdx, %rdx
00000001004241b7	je	0x100423002
00000001004241bd	movsd	0x8(%rdx), %xmm1
00000001004241c2	subsd	%xmm0, %xmm1
00000001004241c6	jmp	0x100424276
00000001004241cb	movq	%rbx, %rdi
00000001004241ce	leaq	0x51e232c(%rip), %rsi           ## literal pool for: "prevcue"
00000001004241d5	movl	$0x7, %edx
00000001004241da	movq	%r13, %rcx
00000001004241dd	callq	__Z19matchStringWithFlagRPKcS0_iRj ## matchStringWithFlag(char const*&, char const*, int, unsigned int&)
00000001004241e2	testb	%al, %al
00000001004241e4	je	0x10042428c
00000001004241ea	movsd	0x2a8(%r12), %xmm0
00000001004241f4	movsd	%xmm0, -0xa8(%rbp)
00000001004241fc	movl	0xfa0(%r12), %ebx
0000000100424204	movq	%r14, %rdi
0000000100424207	callq	__ZN7SDBInfo12getPoiVectorEv    ## SDBInfo::getPoiVector()
000000010042420c	movq	CONFIG_EMULATE_HARDWARE(%rax), %rcx
000000010042420f	movq	0x8(%rax), %rax
0000000100424213	cmpq	%rax, %rcx
0000000100424216	je	0x100423002
000000010042421c	xorps	%xmm0, %xmm0
000000010042421f	cvtsi2sd	%ebx, %xmm0
0000000100424223	movsd	-0xa8(%rbp), %xmm1
000000010042422b	divsd	%xmm0, %xmm1
000000010042422f	xorps	%xmm0, %xmm0
0000000100424232	cvtsd2ss	%xmm1, %xmm0
0000000100424236	xorps	%xmm1, %xmm1
0000000100424239	cvtss2sd	%xmm0, %xmm1
000000010042423d	xorl	%edx, %edx
000000010042423f	cmpl	$0x0, 0x10(%rcx)
0000000100424243	je	0x10042425f
0000000100424245	movsd	0x8(%rcx), %xmm0
000000010042424a	ucomisd	%xmm0, %xmm1
000000010042424e	jb	0x10042425f
0000000100424250	testq	%rdx, %rdx
0000000100424253	je	0x10042425c
0000000100424255	ucomisd	0x8(%rdx), %xmm0
000000010042425a	jbe	0x10042425f
000000010042425c	movq	%rcx, %rdx
000000010042425f	addq	$0x38, %rcx
0000000100424263	cmpq	%rax, %rcx
0000000100424266	jne	0x10042423f
0000000100424268	testq	%rdx, %rdx
000000010042426b	je	0x100423002
0000000100424271	subsd	0x8(%rdx), %xmm1
0000000100424276	xorps	%xmm0, %xmm0
0000000100424279	cvtsi2sdl	0xfa0(%r12), %xmm0
0000000100424283	mulsd	%xmm1, %xmm0
0000000100424287	jmp	0x100423f26
000000010042428c	movq	%rbx, %rdi
000000010042428f	leaq	0x51e2273(%rip), %rsi           ## literal pool for: "start"
0000000100424296	movl	$0x5, %edx
000000010042429b	movq	%r13, %rcx
000000010042429e	callq	__Z19matchStringWithFlagRPKcS0_iRj ## matchStringWithFlag(char const*&, char const*, int, unsigned int&)
00000001004242a3	testb	%al, %al
00000001004242a5	je	0x1004242ed
00000001004242a7	movq	%r14, %rdi
00000001004242aa	movl	$0x6, %esi
00000001004242af	callq	__ZN7SDBInfo11getMixPointE17EAutomixPointType ## SDBInfo::getMixPoint(EAutomixPointType)
00000001004242b4	testq	%rax, %rax
00000001004242b7	jne	0x10042435e
00000001004242bd	movq	%r14, %rdi
00000001004242c0	movl	$FGData.num_y_points, %esi
00000001004242c5	callq	__ZN7SDBInfo11getMixPointE17EAutomixPointType ## SDBInfo::getMixPoint(EAutomixPointType)
00000001004242ca	testq	%rax, %rax
00000001004242cd	jne	0x10042435e
00000001004242d3	movq	%r14, %rdi
00000001004242d6	movl	$0x2, %esi
00000001004242db	callq	__ZN7SDBInfo11getMixPointE17EAutomixPointType ## SDBInfo::getMixPoint(EAutomixPointType)
00000001004242e0	testq	%rax, %rax
00000001004242e3	jne	0x100424356
00000001004242e5	movq	-0x50(%rbp), %rdi
00000001004242e9	xorl	%esi, %esi
00000001004242eb	jmp	0x100424348
00000001004242ed	movq	%rbx, %rdi
00000001004242f0	leaq	0x51d21fb(%rip), %rsi           ## literal pool for: "end"
00000001004242f7	movl	$0x3, %edx
00000001004242fc	movq	%r13, %rcx
00000001004242ff	callq	__Z19matchStringWithFlagRPKcS0_iRj ## matchStringWithFlag(char const*&, char const*, int, unsigned int&)
0000000100424304	testb	%al, %al
0000000100424306	je	0x100424372
0000000100424308	movq	%r14, %rdi
000000010042430b	movl	$0x7, %esi
0000000100424310	callq	__ZN7SDBInfo11getMixPointE17EAutomixPointType ## SDBInfo::getMixPoint(EAutomixPointType)
0000000100424315	testq	%rax, %rax
0000000100424318	jne	0x10042435e
000000010042431a	movq	%r14, %rdi
000000010042431d	movl	$0x5, %esi
0000000100424322	callq	__ZN7SDBInfo11getMixPointE17EAutomixPointType ## SDBInfo::getMixPoint(EAutomixPointType)
0000000100424327	testq	%rax, %rax
000000010042432a	jne	0x100424356
000000010042432c	movq	-0x50(%rbp), %rdi
0000000100424330	movl	$0x3, %esi
0000000100424335	callq	__ZN7SDBInfo11getMixPointE17EAutomixPointType ## SDBInfo::getMixPoint(EAutomixPointType)
000000010042433a	testq	%rax, %rax
000000010042433d	jne	0x100424356
000000010042433f	movq	-0x50(%rbp), %rdi
0000000100424343	movl	$CONFIG_VP9, %esi
0000000100424348	callq	__ZN7SDBInfo11getMixPointE17EAutomixPointType ## SDBInfo::getMixPoint(EAutomixPointType)
000000010042434d	testq	%rax, %rax
0000000100424350	je	0x1004247fe
0000000100424356	movq	-0x30(%rbp), %r15
000000010042435a	movq	-0x48(%rbp), %r12
000000010042435e	cvtsi2sdl	0xfa0(%r12), %xmm0
0000000100424368	mulsd	0x8(%rax), %xmm0
000000010042436d	jmp	0x100423f26
0000000100424372	movq	%rbx, %rdi
0000000100424375	leaq	0x51e2193(%rip), %rsi           ## literal pool for: "tostart"
000000010042437c	movl	$0x7, %edx
0000000100424381	movq	%r13, %rcx
0000000100424384	callq	__Z19matchStringWithFlagRPKcS0_iRj ## matchStringWithFlag(char const*&, char const*, int, unsigned int&)
0000000100424389	testb	%al, %al
000000010042438b	je	0x1004243d5
000000010042438d	movq	%r14, %rdi
0000000100424390	movl	$0x6, %esi
0000000100424395	callq	__ZN7SDBInfo11getMixPointE17EAutomixPointType ## SDBInfo::getMixPoint(EAutomixPointType)
000000010042439a	testq	%rax, %rax
000000010042439d	jne	0x100424440
00000001004243a3	movq	-0x50(%rbp), %rdi
00000001004243a7	movl	$FGData.num_y_points, %esi
00000001004243ac	callq	__ZN7SDBInfo11getMixPointE17EAutomixPointType ## SDBInfo::getMixPoint(EAutomixPointType)
00000001004243b1	testq	%rax, %rax
00000001004243b4	jne	0x100424440
00000001004243ba	movq	-0x50(%rbp), %rdi
00000001004243be	movl	$0x2, %esi
00000001004243c3	callq	__ZN7SDBInfo11getMixPointE17EAutomixPointType ## SDBInfo::getMixPoint(EAutomixPointType)
00000001004243c8	testq	%rax, %rax
00000001004243cb	jne	0x100424440
00000001004243cd	movq	-0x50(%rbp), %rdi
00000001004243d1	xorl	%esi, %esi
00000001004243d3	jmp	0x100424432
00000001004243d5	movq	%rbx, %rdi
00000001004243d8	leaq	0x51e2138(%rip), %rsi           ## literal pool for: "toend"
00000001004243df	movl	$0x5, %edx
00000001004243e4	movq	%r13, %rcx
00000001004243e7	callq	__Z19matchStringWithFlagRPKcS0_iRj ## matchStringWithFlag(char const*&, char const*, int, unsigned int&)
00000001004243ec	testb	%al, %al
00000001004243ee	je	0x10042446d
00000001004243f0	movq	-0x50(%rbp), %rdi
00000001004243f4	movl	$0x7, %esi
00000001004243f9	callq	__ZN7SDBInfo11getMixPointE17EAutomixPointType ## SDBInfo::getMixPoint(EAutomixPointType)
00000001004243fe	testq	%rax, %rax
0000000100424401	jne	0x100424440
0000000100424403	movq	-0x50(%rbp), %rdi
0000000100424407	movl	$0x5, %esi
000000010042440c	callq	__ZN7SDBInfo11getMixPointE17EAutomixPointType ## SDBInfo::getMixPoint(EAutomixPointType)
0000000100424411	testq	%rax, %rax
0000000100424414	jne	0x100424440
0000000100424416	movq	-0x50(%rbp), %rdi
000000010042441a	movl	$0x3, %esi
000000010042441f	callq	__ZN7SDBInfo11getMixPointE17EAutomixPointType ## SDBInfo::getMixPoint(EAutomixPointType)
0000000100424424	testq	%rax, %rax
0000000100424427	jne	0x100424440
0000000100424429	movq	-0x50(%rbp), %rdi
000000010042442d	movl	$CONFIG_VP9, %esi
0000000100424432	callq	__ZN7SDBInfo11getMixPointE17EAutomixPointType ## SDBInfo::getMixPoint(EAutomixPointType)
0000000100424437	testq	%rax, %rax
000000010042443a	je	0x1004247fe
0000000100424440	movq	-0x48(%rbp), %rdx
0000000100424444	cvtsi2sdl	0xfa0(%rdx), %xmm0
000000010042444c	mulsd	0x8(%rax), %xmm0
0000000100424451	subsd	0x2a8(%rdx), %xmm0
0000000100424459	movl	-0x34(%rbp), %esi
000000010042445c	movq	-0x30(%rbp), %r15
0000000100424460	movq	%r15, %rdi
0000000100424463	callq	__Z9writeTimePNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEdjP5CDeck ## writeTime(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>*, double, unsigned int, CDeck*)
0000000100424468	jmp	0x100423002
000000010042446d	leaq	-0x40(%rbp), %rdi
0000000100424471	leaq	0x51e20a5(%rip), %rsi           ## literal pool for: "fromstart"
0000000100424478	movl	$0x9, %edx
000000010042447d	leaq	-0x34(%rbp), %rcx
0000000100424481	callq	__Z19matchStringWithFlagRPKcS0_iRj ## matchStringWithFlag(char const*&, char const*, int, unsigned int&)
0000000100424486	testb	%al, %al
0000000100424488	je	0x1004244d3
000000010042448a	movq	-0x50(%rbp), %rdi
000000010042448e	movl	$0x6, %esi
0000000100424493	callq	__ZN7SDBInfo11getMixPointE17EAutomixPointType ## SDBInfo::getMixPoint(EAutomixPointType)
0000000100424498	testq	%rax, %rax
000000010042449b	jne	0x100424540
00000001004244a1	movq	-0x50(%rbp), %rdi
00000001004244a5	movl	$FGData.num_y_points, %esi
00000001004244aa	callq	__ZN7SDBInfo11getMixPointE17EAutomixPointType ## SDBInfo::getMixPoint(EAutomixPointType)
00000001004244af	testq	%rax, %rax
00000001004244b2	jne	0x100424540
00000001004244b8	movq	-0x50(%rbp), %rdi
00000001004244bc	movl	$0x2, %esi
00000001004244c1	callq	__ZN7SDBInfo11getMixPointE17EAutomixPointType ## SDBInfo::getMixPoint(EAutomixPointType)
00000001004244c6	testq	%rax, %rax
00000001004244c9	jne	0x100424540
00000001004244cb	movq	-0x50(%rbp), %rdi
00000001004244cf	xorl	%esi, %esi
00000001004244d1	jmp	0x100424532
00000001004244d3	leaq	-0x40(%rbp), %rdi
00000001004244d7	leaq	0x51e2049(%rip), %rsi           ## literal pool for: "fromend"
00000001004244de	movl	$0x7, %edx
00000001004244e3	leaq	-0x34(%rbp), %rcx
00000001004244e7	callq	__Z19matchStringWithFlagRPKcS0_iRj ## matchStringWithFlag(char const*&, char const*, int, unsigned int&)
00000001004244ec	testb	%al, %al
00000001004244ee	je	0x100424562
00000001004244f0	movq	-0x50(%rbp), %rdi
00000001004244f4	movl	$0x7, %esi
00000001004244f9	callq	__ZN7SDBInfo11getMixPointE17EAutomixPointType ## SDBInfo::getMixPoint(EAutomixPointType)
00000001004244fe	testq	%rax, %rax
0000000100424501	jne	0x100424540
0000000100424503	movq	-0x50(%rbp), %rdi
0000000100424507	movl	$0x5, %esi
000000010042450c	callq	__ZN7SDBInfo11getMixPointE17EAutomixPointType ## SDBInfo::getMixPoint(EAutomixPointType)
0000000100424511	testq	%rax, %rax
0000000100424514	jne	0x100424540
0000000100424516	movq	-0x50(%rbp), %rdi
000000010042451a	movl	$0x3, %esi
000000010042451f	callq	__ZN7SDBInfo11getMixPointE17EAutomixPointType ## SDBInfo::getMixPoint(EAutomixPointType)
0000000100424524	testq	%rax, %rax
0000000100424527	jne	0x100424540
0000000100424529	movq	-0x50(%rbp), %rdi
000000010042452d	movl	$CONFIG_VP9, %esi
0000000100424532	callq	__ZN7SDBInfo11getMixPointE17EAutomixPointType ## SDBInfo::getMixPoint(EAutomixPointType)
0000000100424537	testq	%rax, %rax
000000010042453a	je	0x1004247fe
0000000100424540	movq	-0x48(%rbp), %rdx
0000000100424544	movsd	0x2a8(%rdx), %xmm0
000000010042454c	cvtsi2sdl	0xfa0(%rdx), %xmm1
0000000100424554	mulsd	0x8(%rax), %xmm1
0000000100424559	subsd	%xmm1, %xmm0
000000010042455d	jmp	0x100424459
0000000100424562	leaq	-0x40(%rbp), %rdi
0000000100424566	leaq	0x51e1fc2(%rip), %rsi           ## literal pool for: "bpmexx"
000000010042456d	movl	$0x6, %edx
0000000100424572	leaq	-0x34(%rbp), %rcx
0000000100424576	callq	__Z19matchStringWithFlagRPKcS0_iRj ## matchStringWithFlag(char const*&, char const*, int, unsigned int&)
000000010042457b	testb	%al, %al
000000010042457d	je	0x100424622
0000000100424583	movq	-0x48(%rbp), %rax
0000000100424587	movss	0x44c(%rax), %xmm1
000000010042458f	ucomiss	0x4d68f3e(%rip), %xmm1
0000000100424596	jne	0x10042459a
0000000100424598	jnp	0x1004245a0
000000010042459a	testb	$0x1, -0x34(%rbp)
000000010042459e	jne	0x1004245c7
00000001004245a0	movq	-0x48(%rbp), %rax
00000001004245a4	movsd	0x2a8(%rax), %xmm0
00000001004245ac	movl	0xfa0(%rax), %esi
00000001004245b2	xorps	%xmm1, %xmm1
00000001004245b5	movq	-0x50(%rbp), %rdi
00000001004245b9	xorl	%edx, %edx
00000001004245bb	callq	__ZN7SDBInfo8localBpmEdifb      ## SDBInfo::localBpm(double, int, float, bool)
00000001004245c0	xorps	%xmm1, %xmm1
00000001004245c3	cvtsd2ss	%xmm0, %xmm1
00000001004245c7	movq	-0x50(%rbp), %rax
00000001004245cb	movss	0xb4(%rax), %xmm0
00000001004245d3	ucomiss	0x4d68efa(%rip), %xmm0
00000001004245da	jne	0x1004245e2
00000001004245dc	jnp	0x1004247fe
00000001004245e2	movss	0x4d690da(%rip), %xmm0
00000001004245ea	divss	%xmm1, %xmm0
00000001004245ee	testb	$0x1, -0x34(%rbp)
00000001004245f2	je	0x100424600
00000001004245f4	movq	-0x48(%rbp), %rax
00000001004245f8	mulss	0x284(%rax), %xmm0
0000000100424600	leaq	-0x80(%rbp), %rbx
0000000100424604	movq	%rbx, %rdi
0000000100424607	movl	$0x3, %esi
000000010042460c	callq	__Z8dblToStrfi                  ## dblToStr(float, int)
0000000100424611	movq	-0x30(%rbp), %rdi
0000000100424615	movq	%rbx, %rsi
0000000100424618	callq	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendB8ne200100ERKS5_ ## std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>::append[abi:ne200100](std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&)
000000010042461d	jmp	0x1004247ef
0000000100424622	leaq	-0x40(%rbp), %rdi
0000000100424626	leaq	0x51e1f09(%rip), %rsi           ## literal pool for: "bpmex"
000000010042462d	movl	$0x5, %edx
0000000100424632	leaq	-0x34(%rbp), %rcx
0000000100424636	callq	__Z19matchStringWithFlagRPKcS0_iRj ## matchStringWithFlag(char const*&, char const*, int, unsigned int&)
000000010042463b	testb	%al, %al
000000010042463d	je	0x1004246e2
0000000100424643	movq	-0x48(%rbp), %rax
0000000100424647	movss	0x44c(%rax), %xmm1
000000010042464f	ucomiss	0x4d68e7e(%rip), %xmm1
0000000100424656	jne	0x10042465a
0000000100424658	jnp	0x100424660
000000010042465a	testb	$0x1, -0x34(%rbp)
000000010042465e	jne	0x100424687
0000000100424660	movq	-0x48(%rbp), %rax
0000000100424664	movsd	0x2a8(%rax), %xmm0
000000010042466c	movl	0xfa0(%rax), %esi
0000000100424672	xorps	%xmm1, %xmm1
0000000100424675	movq	-0x50(%rbp), %rdi
0000000100424679	xorl	%edx, %edx
000000010042467b	callq	__ZN7SDBInfo8localBpmEdifb      ## SDBInfo::localBpm(double, int, float, bool)
0000000100424680	xorps	%xmm1, %xmm1
0000000100424683	cvtsd2ss	%xmm0, %xmm1
0000000100424687	movq	-0x50(%rbp), %rax
000000010042468b	movss	0xb4(%rax), %xmm0
0000000100424693	ucomiss	0x4d68e3a(%rip), %xmm0
000000010042469a	jne	0x1004246a2
000000010042469c	jnp	0x1004247fe
00000001004246a2	movss	0x4d6901a(%rip), %xmm0
00000001004246aa	divss	%xmm1, %xmm0
00000001004246ae	testb	$0x1, -0x34(%rbp)
00000001004246b2	je	0x1004246c0
00000001004246b4	movq	-0x48(%rbp), %rax
00000001004246b8	mulss	0x284(%rax), %xmm0
00000001004246c0	leaq	-0x80(%rbp), %rbx
00000001004246c4	movq	%rbx, %rdi
00000001004246c7	movl	$0x2, %esi
00000001004246cc	callq	__Z8dblToStrfi                  ## dblToStr(float, int)
00000001004246d1	movq	-0x30(%rbp), %rdi
00000001004246d5	movq	%rbx, %rsi
00000001004246d8	callq	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendB8ne200100ERKS5_ ## std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>::append[abi:ne200100](std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&)
00000001004246dd	jmp	0x1004247ef
00000001004246e2	leaq	-0x40(%rbp), %rdi
00000001004246e6	leaq	0x51b8d05(%rip), %rsi           ## literal pool for: "bpm"
00000001004246ed	movl	$0x3, %edx
00000001004246f2	leaq	-0x34(%rbp), %rcx
00000001004246f6	callq	__Z19matchStringWithFlagRPKcS0_iRj ## matchStringWithFlag(char const*&, char const*, int, unsigned int&)
00000001004246fb	testb	%al, %al
00000001004246fd	je	0x10042479f
0000000100424703	movq	-0x48(%rbp), %rax
0000000100424707	movss	0x44c(%rax), %xmm1
000000010042470f	ucomiss	0x4d68dbe(%rip), %xmm1
0000000100424716	jne	0x10042471a
0000000100424718	jnp	0x100424720
000000010042471a	testb	$0x1, -0x34(%rbp)
000000010042471e	jne	0x100424747
0000000100424720	movq	-0x48(%rbp), %rax
0000000100424724	movsd	0x2a8(%rax), %xmm0
000000010042472c	movl	0xfa0(%rax), %esi
0000000100424732	xorps	%xmm1, %xmm1
0000000100424735	movq	-0x50(%rbp), %rdi
0000000100424739	xorl	%edx, %edx
000000010042473b	callq	__ZN7SDBInfo8localBpmEdifb      ## SDBInfo::localBpm(double, int, float, bool)
0000000100424740	xorps	%xmm1, %xmm1
0000000100424743	cvtsd2ss	%xmm0, %xmm1
0000000100424747	movq	-0x50(%rbp), %rax
000000010042474b	movss	0xb4(%rax), %xmm0
0000000100424753	ucomiss	0x4d68d7a(%rip), %xmm0
000000010042475a	jne	0x100424762
000000010042475c	jnp	0x1004247fe
0000000100424762	movss	0x4d68f5a(%rip), %xmm0
000000010042476a	divss	%xmm1, %xmm0
000000010042476e	testb	$0x1, -0x34(%rbp)
0000000100424772	je	0x100424780
0000000100424774	movq	-0x48(%rbp), %rax
0000000100424778	mulss	0x284(%rax), %xmm0
0000000100424780	leaq	-0x80(%rbp), %rbx
0000000100424784	movq	%rbx, %rdi
0000000100424787	movl	$CONFIG_VP9, %esi
000000010042478c	callq	__Z8dblToStrfi                  ## dblToStr(float, int)
0000000100424791	movq	-0x30(%rbp), %rdi
0000000100424795	movq	%rbx, %rsi
0000000100424798	callq	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendB8ne200100ERKS5_ ## std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>::append[abi:ne200100](std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&)
000000010042479d	jmp	0x1004247ef
000000010042479f	leaq	-0x40(%rbp), %rdi
00000001004247a3	leaq	0x51e1d92(%rip), %rsi           ## literal pool for: "pitchrange"
00000001004247aa	movl	$0xa, %edx
00000001004247af	leaq	-0x34(%rbp), %rcx
00000001004247b3	callq	__Z19matchStringWithFlagRPKcS0_iRj ## matchStringWithFlag(char const*&, char const*, int, unsigned int&)
00000001004247b8	testb	%al, %al
00000001004247ba	je	0x100424807
00000001004247bc	movq	-0x48(%rbp), %rax
00000001004247c0	movslq	0x240(%rax), %rax
00000001004247c7	leaq	_Config(%rip), %rcx
00000001004247ce	movss	0x1a24(%rcx,%rax,4), %xmm0
00000001004247d7	leaq	-0x80(%rbp), %rbx
00000001004247db	movq	%rbx, %rdi
00000001004247de	callq	__Z12dblToStrDot2f              ## dblToStrDot2(float)
00000001004247e3	movq	-0x30(%rbp), %rdi
00000001004247e7	movq	%rbx, %rsi
00000001004247ea	callq	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendB8ne200100ERKS5_ ## std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>::append[abi:ne200100](std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&)
00000001004247ef	testb	$0x1, -0x80(%rbp)
00000001004247f3	je	0x1004247fe
00000001004247f5	movq	-0x70(%rbp), %rdi
00000001004247f9	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
00000001004247fe	movq	-0x30(%rbp), %r15
0000000100424802	jmp	0x100423002
0000000100424807	leaq	-0x40(%rbp), %rdi
000000010042480b	leaq	0x51b8cfc(%rip), %rsi           ## literal pool for: "pitch"
0000000100424812	movl	$0x5, %edx
0000000100424817	leaq	-0x34(%rbp), %rcx
000000010042481b	callq	__Z19matchStringWithFlagRPKcS0_iRj ## matchStringWithFlag(char const*&, char const*, int, unsigned int&)
0000000100424820	testb	%al, %al
0000000100424822	je	0x10042487f
0000000100424824	testb	$0x1, -0x34(%rbp)
0000000100424828	jne	0x10042491f
000000010042482e	movq	-0x48(%rbp), %rax
0000000100424832	movss	0x284(%rax), %xmm0
000000010042483a	mulss	0x4d68e7e(%rip), %xmm0
0000000100424842	movss	%xmm0, -0xa0(%rbp)
000000010042484a	movl	$0x7, %edx
000000010042484f	movl	$0x9, %ecx
0000000100424854	leaq	-0x80(%rbp), %rbx
0000000100424858	movq	%rbx, %rdi
000000010042485b	leaq	0x51e1ced(%rip), %rsi           ## literal pool for: "{:5.1f}"
0000000100424862	leaq	-0xa0(%rbp), %r8
0000000100424869	callq	__ZN3fmt3v127vformatENS0_17basic_string_viewIcEENS0_17basic_format_argsINS0_7contextEEE ## fmt::v12::vformat(fmt::v12::basic_string_view<char>, fmt::v12::basic_format_args<fmt::v12::context>)
000000010042486e	movq	-0x30(%rbp), %rdi
0000000100424872	movq	%rbx, %rsi
0000000100424875	callq	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendB8ne200100ERKS5_ ## std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>::append[abi:ne200100](std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&)
000000010042487a	jmp	0x1004247ef
000000010042487f	leaq	-0x40(%rbp), %rdi
0000000100424883	leaq	0x51e1ccd(%rip), %rsi           ## literal pool for: "keyoffset"
000000010042488a	movl	$0x9, %edx
000000010042488f	leaq	-0x34(%rbp), %rcx
0000000100424893	callq	__Z19matchStringWithFlagRPKcS0_iRj ## matchStringWithFlag(char const*&, char const*, int, unsigned int&)
0000000100424898	testb	%al, %al
000000010042489a	je	0x100424978
00000001004248a0	movq	-0x48(%rbp), %rdi
00000001004248a4	callq	__ZN5CDeck6getKeyEv             ## CDeck::getKey()
00000001004248a9	movss	%xmm0, -0xa8(%rbp)
00000001004248b1	callq	0x104fe8e6a                     ## symbol stub for: _lroundf
00000001004248b6	xorps	%xmm0, %xmm0
00000001004248b9	cvtsi2ss	%eax, %xmm0
00000001004248bd	movss	-0xa8(%rbp), %xmm1
00000001004248c5	movaps	%xmm1, %xmm2
00000001004248c8	subss	%xmm0, %xmm1
00000001004248cc	andps	0x4d68dbd(%rip), %xmm1
00000001004248d3	movss	0x4d68e39(%rip), %xmm0
00000001004248db	ucomiss	%xmm1, %xmm0
00000001004248de	jbe	0x1004249cc
00000001004248e4	movl	%eax, -0xa0(%rbp)
00000001004248ea	movl	$FGData.num_y_points, %edx
00000001004248ef	movl	$CONFIG_VP9, %ecx
00000001004248f4	leaq	-0x80(%rbp), %rbx
00000001004248f8	movq	%rbx, %rdi
00000001004248fb	leaq	0x51c9ac9(%rip), %rsi           ## literal pool for: "{:+}"
0000000100424902	leaq	-0xa0(%rbp), %r8
0000000100424909	callq	__ZN3fmt3v127vformatENS0_17basic_string_viewIcEENS0_17basic_format_argsINS0_7contextEEE ## fmt::v12::vformat(fmt::v12::basic_string_view<char>, fmt::v12::basic_format_args<fmt::v12::context>)
000000010042490e	movq	-0x30(%rbp), %rdi
0000000100424912	movq	%rbx, %rsi
0000000100424915	callq	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendB8ne200100ERKS5_ ## std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>::append[abi:ne200100](std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&)
000000010042491a	jmp	0x1004247ef
000000010042491f	movq	-0x48(%rbp), %rax
0000000100424923	movss	0x284(%rax), %xmm0
000000010042492b	addss	0x4d68b0d(%rip), %xmm0
0000000100424933	mulss	0x4d68d85(%rip), %xmm0
000000010042493b	movss	%xmm0, -0xa0(%rbp)
0000000100424943	movl	$0x7, %edx
0000000100424948	movl	$0x9, %ecx
000000010042494d	leaq	-0x80(%rbp), %rbx
0000000100424951	movq	%rbx, %rdi
0000000100424954	leaq	0x51e1bec(%rip), %rsi           ## literal pool for: "{:+.1f}"
000000010042495b	leaq	-0xa0(%rbp), %r8
0000000100424962	callq	__ZN3fmt3v127vformatENS0_17basic_string_viewIcEENS0_17basic_format_argsINS0_7contextEEE ## fmt::v12::vformat(fmt::v12::basic_string_view<char>, fmt::v12::basic_format_args<fmt::v12::context>)
0000000100424967	movq	-0x30(%rbp), %rdi
000000010042496b	movq	%rbx, %rsi
000000010042496e	callq	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendB8ne200100ERKS5_ ## std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>::append[abi:ne200100](std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&)
0000000100424973	jmp	0x1004247ef
0000000100424978	leaq	-0x40(%rbp), %rdi
000000010042497c	leaq	0x51d0dc3(%rip), %rsi           ## literal pool for: "key"
0000000100424983	movl	$0x3, %edx
0000000100424988	leaq	-0x34(%rbp), %rcx
000000010042498c	callq	__Z19matchStringWithFlagRPKcS0_iRj ## matchStringWithFlag(char const*&, char const*, int, unsigned int&)
0000000100424991	testb	%al, %al
0000000100424993	je	0x100424a09
0000000100424995	movq	-0x50(%rbp), %rdi
0000000100424999	callq	__ZN7SDBInfo6getKeyEv           ## SDBInfo::getKey()
000000010042499e	testl	%eax, %eax
00000001004249a0	setne	%cl
00000001004249a3	andb	-0x34(%rbp), %cl
00000001004249a6	cmpb	$0x1, %cl
00000001004249a9	jne	0x1004249b4
00000001004249ab	movq	-0x48(%rbp), %rdi
00000001004249af	callq	__ZN5CDeck13getCurrentKeyEv     ## CDeck::getCurrentKey()
00000001004249b4	leal	-0x1(%rax), %ecx
00000001004249b7	cmpl	$0x17, %ecx
00000001004249ba	ja	0x1004247fe
00000001004249c0	movl	%eax, %edi
00000001004249c2	callq	__ZN12CHarmonicKey9keyToNameEi  ## CHarmonicKey::keyToName(int)
00000001004249c7	jmp	0x10042512f
00000001004249cc	movss	%xmm2, -0xa0(%rbp)
00000001004249d4	movl	$0x7, %edx
00000001004249d9	movl	$0x9, %ecx
00000001004249de	leaq	-0x80(%rbp), %rbx
00000001004249e2	movq	%rbx, %rdi
00000001004249e5	leaq	0x51e1b75(%rip), %rsi           ## literal pool for: "{:+.2f}"
00000001004249ec	leaq	-0xa0(%rbp), %r8
00000001004249f3	callq	__ZN3fmt3v127vformatENS0_17basic_string_viewIcEENS0_17basic_format_argsINS0_7contextEEE ## fmt::v12::vformat(fmt::v12::basic_string_view<char>, fmt::v12::basic_format_args<fmt::v12::context>)
00000001004249f8	movq	-0x30(%rbp), %rdi
00000001004249fc	movq	%rbx, %rsi
00000001004249ff	callq	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendB8ne200100ERKS5_ ## std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>::append[abi:ne200100](std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&)
0000000100424a04	jmp	0x1004247ef
0000000100424a09	leaq	-0x40(%rbp), %rdi
0000000100424a0d	leaq	0x51e1b55(%rip), %rsi           ## literal pool for: "camelot"
0000000100424a14	movl	$0x7, %edx
0000000100424a19	leaq	-0x34(%rbp), %rcx
0000000100424a1d	callq	__Z19matchStringWithFlagRPKcS0_iRj ## matchStringWithFlag(char const*&, char const*, int, unsigned int&)
0000000100424a22	testb	%al, %al
0000000100424a24	je	0x100424a5d
0000000100424a26	movq	-0x50(%rbp), %rdi
0000000100424a2a	callq	__ZN7SDBInfo6getKeyEv           ## SDBInfo::getKey()
0000000100424a2f	testl	%eax, %eax
0000000100424a31	setne	%cl
0000000100424a34	andb	-0x34(%rbp), %cl
0000000100424a37	cmpb	$0x1, %cl
0000000100424a3a	jne	0x100424a45
0000000100424a3c	movq	-0x48(%rbp), %rdi
0000000100424a40	callq	__ZN5CDeck13getCurrentKeyEv     ## CDeck::getCurrentKey()
0000000100424a45	leal	-0x1(%rax), %ecx
0000000100424a48	cmpl	$0x17, %ecx
0000000100424a4b	ja	0x1004247fe
0000000100424a51	movl	%eax, %edi
0000000100424a53	callq	__ZN12CHarmonicKey12keyToCamelotEi ## CHarmonicKey::keyToCamelot(int)
0000000100424a58	jmp	0x10042512f
0000000100424a5d	leaq	-0x40(%rbp), %rdi
0000000100424a61	leaq	0x51cbd28(%rip), %rsi           ## literal pool for: "level"
0000000100424a68	movl	$0x5, %edx
0000000100424a6d	leaq	-0x34(%rbp), %rcx
0000000100424a71	callq	__Z19matchStringWithFlagRPKcS0_iRj ## matchStringWithFlag(char const*&, char const*, int, unsigned int&)
0000000100424a76	testb	%al, %al
0000000100424a78	je	0x100424a95
0000000100424a7a	testb	$0x2, -0x34(%rbp)
0000000100424a7e	jne	0x100424dbf
0000000100424a84	movq	-0x50(%rbp), %rax
0000000100424a88	movss	rf.rp_proj(%rax), %xmm0
0000000100424a90	jmp	0x100424e71
0000000100424a95	movq	-0x40(%rbp), %r12
0000000100424a99	movl	$working_state.cur.put_buffer.simd, %edx
0000000100424a9e	movq	%r12, %rdi
0000000100424aa1	leaq	0x51e1ac9(%rip), %rsi           ## literal pool for: "artisttitleremix"
0000000100424aa8	callq	0x104fe92b4                     ## symbol stub for: _strncasecmp
0000000100424aad	testl	%eax, %eax
0000000100424aaf	je	0x100424ef1
0000000100424ab5	movl	$0xa, %edx
0000000100424aba	movq	%r12, %rdi
0000000100424abd	leaq	0x51b7843(%rip), %rsi           ## literal pool for: "titleremix"
0000000100424ac4	callq	0x104fe92b4                     ## symbol stub for: _strncasecmp
0000000100424ac9	testl	%eax, %eax
0000000100424acb	je	0x100424f24
0000000100424ad1	movl	$0x5, %edx
0000000100424ad6	movq	%r12, %rdi
0000000100424ad9	leaq	0x51b8906(%rip), %rsi           ## literal pool for: "title"
0000000100424ae0	callq	0x104fe92b4                     ## symbol stub for: _strncasecmp
0000000100424ae5	testl	%eax, %eax
0000000100424ae7	je	0x100425026
0000000100424aed	movl	$0x6, %edx
0000000100424af2	movq	%r12, %rdi
0000000100424af5	leaq	0x51b783c(%rip), %rsi           ## literal pool for: "author"
0000000100424afc	callq	0x104fe92b4                     ## symbol stub for: _strncasecmp
0000000100424b01	testl	%eax, %eax
0000000100424b03	je	0x100424f57
0000000100424b09	movl	$0x6, %edx
0000000100424b0e	movq	%r12, %rdi
0000000100424b11	leaq	0x51b88c7(%rip), %rsi           ## literal pool for: "artist"
0000000100424b18	callq	0x104fe92b4                     ## symbol stub for: _strncasecmp
0000000100424b1d	testl	%eax, %eax
0000000100424b1f	je	0x100424f57
0000000100424b25	movl	$0x7, %edx
0000000100424b2a	movq	%r12, %rdi
0000000100424b2d	leaq	0x51e1a61(%rip), %rsi           ## literal pool for: "remixer"
0000000100424b34	callq	0x104fe92b4                     ## symbol stub for: _strncasecmp
0000000100424b39	testl	%eax, %eax
0000000100424b3b	je	0x100425151
0000000100424b41	movl	$0x5, %edx
0000000100424b46	movq	%r12, %rdi
0000000100424b49	leaq	0x51b889c(%rip), %rsi           ## literal pool for: "remix"
0000000100424b50	callq	0x104fe92b4                     ## symbol stub for: _strncasecmp
0000000100424b55	testl	%eax, %eax
0000000100424b57	je	0x10042516d
0000000100424b5d	movl	$msac.end, %edx
0000000100424b62	movq	%r12, %rdi
0000000100424b65	leaq	0x51e1a31(%rip), %rsi           ## literal pool for: "composer"
0000000100424b6c	callq	0x104fe92b4                     ## symbol stub for: _strncasecmp
0000000100424b71	testl	%eax, %eax
0000000100424b73	je	0x10042517f
0000000100424b79	movl	$0x5, %edx
0000000100424b7e	movq	%r12, %rdi
0000000100424b81	leaq	0x51c1fa5(%rip), %rsi           ## literal pool for: "album"
0000000100424b88	callq	0x104fe92b4                     ## symbol stub for: _strncasecmp
0000000100424b8d	testl	%eax, %eax
0000000100424b8f	je	0x100425191
0000000100424b95	movl	$0x5, %edx
0000000100424b9a	movq	%r12, %rdi
0000000100424b9d	leaq	0x51c067e(%rip), %rsi           ## literal pool for: "genre"
0000000100424ba4	callq	0x104fe92b4                     ## symbol stub for: _strncasecmp
0000000100424ba9	testl	%eax, %eax
0000000100424bab	je	0x1004251a3
0000000100424bb1	movl	$0x7, %edx
0000000100424bb6	movq	%r12, %rdi
0000000100424bb9	leaq	0x51d30a4(%rip), %rsi           ## literal pool for: "comment"
0000000100424bc0	callq	0x104fe92b4                     ## symbol stub for: _strncasecmp
0000000100424bc5	testl	%eax, %eax
0000000100424bc7	je	0x1004251b5
0000000100424bcd	movl	$0x6, %edx
0000000100424bd2	movq	%r12, %rdi
0000000100424bd5	leaq	0x51e19ca(%rip), %rsi           ## literal pool for: "hour12"
0000000100424bdc	callq	0x104fe92b4                     ## symbol stub for: _strncasecmp
0000000100424be1	testl	%eax, %eax
0000000100424be3	je	0x1004251d6
0000000100424be9	movl	$msac.end, %edx
0000000100424bee	movq	%r12, %rdi
0000000100424bf1	leaq	0x51e19bd(%rip), %rsi           ## literal pool for: "fullhour"
0000000100424bf8	callq	0x104fe92b4                     ## symbol stub for: _strncasecmp
0000000100424bfd	testl	%eax, %eax
0000000100424bff	je	0x10042520c
0000000100424c05	movl	$FGData.num_y_points, %edx
0000000100424c0a	movq	%r12, %rdi
0000000100424c0d	leaq	0x51e19aa(%rip), %rsi           ## literal pool for: "hour"
0000000100424c14	callq	0x104fe92b4                     ## symbol stub for: _strncasecmp
0000000100424c19	testl	%eax, %eax
0000000100424c1b	je	0x100425242
0000000100424c21	movl	$0x7, %edx
0000000100424c26	movq	%r12, %rdi
0000000100424c29	leaq	0x51e1993(%rip), %rsi           ## literal pool for: "counter"
0000000100424c30	callq	0x104fe92b4                     ## symbol stub for: _strncasecmp
0000000100424c35	testl	%eax, %eax
0000000100424c37	je	0x100425278
0000000100424c3d	movl	$0xa, %edx
0000000100424c42	movq	%r12, %rdi
0000000100424c45	leaq	0x51e197f(%rip), %rsi           ## literal pool for: "maineffect"
0000000100424c4c	callq	0x104fe92b4                     ## symbol stub for: _strncasecmp
0000000100424c51	testl	%eax, %eax
0000000100424c53	je	0x1004252d6
0000000100424c59	movl	$0xa, %edx
0000000100424c5e	movq	%r12, %rdi
0000000100424c61	leaq	0x51e196e(%rip), %rsi           ## literal pool for: "effectslot"
0000000100424c68	callq	0x104fe92b4                     ## symbol stub for: _strncasecmp
0000000100424c6d	testl	%eax, %eax
0000000100424c6f	je	0x1004252f7
0000000100424c75	movl	$0xa, %edx
0000000100424c7a	movq	%r12, %rdi
0000000100424c7d	leaq	0x51ca23e(%rip), %rsi           ## literal pool for: "djc_button"
0000000100424c84	callq	0x104fe92b4                     ## symbol stub for: _strncasecmp
0000000100424c89	testl	%eax, %eax
0000000100424c8b	je	0x100425383
0000000100424c91	movl	$0xa, %edx
0000000100424c96	movq	%r12, %rdi
0000000100424c99	leaq	0x51e1941(%rip), %rsi           ## literal pool for: "mainsample"
0000000100424ca0	callq	0x104fe92b4                     ## symbol stub for: _strncasecmp
0000000100424ca5	testl	%eax, %eax
0000000100424ca7	je	0x1004253eb
0000000100424cad	movl	$0x7, %edx
0000000100424cb2	movq	%r12, %rdi
0000000100424cb5	leaq	0x51e1930(%rip), %rsi           ## literal pool for: "videofx"
0000000100424cbc	callq	0x104fe92b4                     ## symbol stub for: _strncasecmp
0000000100424cc1	testl	%eax, %eax
0000000100424cc3	je	0x10042545f
0000000100424cc9	movl	$0xf, %edx
0000000100424cce	movq	%r12, %rdi
0000000100424cd1	leaq	0x51e191c(%rip), %rsi           ## literal pool for: "videotransition"
0000000100424cd8	callq	0x104fe92b4                     ## symbol stub for: _strncasecmp
0000000100424cdd	testl	%eax, %eax
0000000100424cdf	je	0x100425497
0000000100424ce5	movl	$0xb, %edx
0000000100424cea	movq	%r12, %rdi
0000000100424ced	leaq	0x51e1910(%rip), %rsi           ## literal pool for: "videosource"
0000000100424cf4	callq	0x104fe92b4                     ## symbol stub for: _strncasecmp
0000000100424cf9	testl	%eax, %eax
0000000100424cfb	je	0x1004254da
0000000100424d01	movl	$0x3, %edx
0000000100424d06	movq	%r12, %rdi
0000000100424d09	leaq	0x51c611e(%rip), %rsi           ## literal pool for: "cpu"
0000000100424d10	callq	0x104fe92b4                     ## symbol stub for: _strncasecmp
0000000100424d15	testl	%eax, %eax
0000000100424d17	je	0x10042551a
0000000100424d1d	movl	$0x6, %edx
0000000100424d22	movq	%r12, %rdi
0000000100424d25	leaq	0x51d5dac(%rip), %rsi           ## literal pool for: "status"
0000000100424d2c	callq	0x104fe92b4                     ## symbol stub for: _strncasecmp
0000000100424d31	testl	%eax, %eax
0000000100424d33	je	0x100425583
0000000100424d39	movl	$FGData.num_y_points, %edx
0000000100424d3e	movq	%r12, %rdi
0000000100424d41	leaq	0x520502a(%rip), %rsi           ## literal pool for: "name"
0000000100424d48	callq	0x104fe92b4                     ## symbol stub for: _strncasecmp
0000000100424d4d	testl	%eax, %eax
0000000100424d4f	je	0x1004255cc
0000000100424d55	movl	$0xb, %edx
0000000100424d5a	movq	%r12, %rdi
0000000100424d5d	leaq	0x51e18ac(%rip), %rsi           ## literal pool for: "defaultdeck"
0000000100424d64	callq	0x104fe92b4                     ## symbol stub for: _strncasecmp
0000000100424d69	testl	%eax, %eax
0000000100424d6b	je	0x10042562d
0000000100424d71	movl	$0xa, %edx
0000000100424d76	movq	%r12, %rdi
0000000100424d79	leaq	0x51e189c(%rip), %rsi           ## literal pool for: "activedeck"
0000000100424d80	callq	0x104fe92b4                     ## symbol stub for: _strncasecmp
0000000100424d85	testl	%eax, %eax
0000000100424d87	je	0x100425664
0000000100424d8d	movl	$0xe, %edx
0000000100424d92	movq	%r12, %rdi
0000000100424d95	leaq	0x51c09b6(%rip), %rsi           ## literal pool for: "soundswitch_id"
0000000100424d9c	callq	0x104fe92b4                     ## symbol stub for: _strncasecmp
0000000100424da1	testl	%eax, %eax
0000000100424da3	je	0x100425696
0000000100424da9	movq	-0x30(%rbp), %r15
0000000100424dad	movq	%r15, %rdi
0000000100424db0	movl	$0x25, %esi
0000000100424db5	callq	__Z10appendCharPNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEc ## appendChar(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>*, char)
0000000100424dba	jmp	0x100423002
0000000100424dbf	movq	-0xc8(%rbp), %rbx
0000000100424dc6	movq	0x930(%rbx), %r14
0000000100424dcd	movl	$0x360, %eax                    ## imm = 0x360
0000000100424dd2	addq	%rax, %r14
0000000100424dd5	movq	%r14, %rdi
0000000100424dd8	callq	__ZN15CThreadSyncRWNR9EnterReadEv ## CThreadSyncRWNR::EnterRead()
0000000100424ddd	movq	0x930(%rbx), %rbx
0000000100424de4	movq	-0x48(%rbp), %rax
0000000100424de8	movsd	0x2a8(%rax), %xmm1
0000000100424df0	movsd	0x4d68878(%rip), %xmm0
0000000100424df8	minsd	%xmm1, %xmm0
0000000100424dfc	cmpnlesd	0x4d6a2b3(%rip), %xmm1
0000000100424e05	andpd	%xmm0, %xmm1
0000000100424e09	movq	0x2a0(%rbx), %r15
0000000100424e10	movq	0x2a8(%rbx), %rax
0000000100424e17	subq	%r15, %rax
0000000100424e1a	sarq	$0x2, %rax
0000000100424e1e	movq	%rax, %xmm0
0000000100424e23	punpckldq	0x4d68c35(%rip), %xmm0  ## xmm0 = xmm0[0],mem[0],xmm0[1],mem[1]
0000000100424e2b	subpd	0x4d68c3d(%rip), %xmm0
0000000100424e33	haddpd	%xmm0, %xmm0
0000000100424e37	mulsd	%xmm1, %xmm0
0000000100424e3b	callq	_lround
0000000100424e40	movzbl	0x3(%r15,%rax,4), %r15d
0000000100424e46	xorps	%xmm0, %xmm0
0000000100424e49	cvtsi2ssl	0x2bc(%rbx), %xmm0
0000000100424e51	movss	%xmm0, -0xa8(%rbp)
0000000100424e59	movq	%r14, %rdi
0000000100424e5c	callq	__ZN15CThreadSyncRWNR9LeaveReadEv ## CThreadSyncRWNR::LeaveRead()
0000000100424e61	xorps	%xmm0, %xmm0
0000000100424e64	cvtsi2ss	%r15d, %xmm0
0000000100424e69	divss	-0xa8(%rbp), %xmm0
0000000100424e71	ucomiss	0x4d6865c(%rip), %xmm0
0000000100424e78	jne	0x100424e80
0000000100424e7a	jnp	0x1004247fe
0000000100424e80	leaq	_Config(%rip), %rax
0000000100424e87	divss	0x2138(%rax), %xmm0
0000000100424e8f	callq	0x104fe8e46                     ## symbol stub for: _log10f
0000000100424e94	mulss	0x4d68620(%rip), %xmm0
0000000100424e9c	movss	%xmm0, -0xa8(%rbp)
0000000100424ea4	testb	$0x1, -0x34(%rbp)
0000000100424ea8	je	0x100424ec7
0000000100424eaa	movq	-0x48(%rbp), %rdi
0000000100424eae	callq	__ZN5CDeck9getGainDbEv          ## CDeck::getGainDb()
0000000100424eb3	movss	-0xa8(%rbp), %xmm1
0000000100424ebb	addss	%xmm0, %xmm1
0000000100424ebf	movss	%xmm1, -0xa8(%rbp)
0000000100424ec7	leaq	-0x80(%rbp), %rbx
0000000100424ecb	movq	%rbx, %rdi
0000000100424ece	movss	-0xa8(%rbp), %xmm0
0000000100424ed6	movl	$CONFIG_VP9, %esi
0000000100424edb	callq	__Z8dblToStrfi                  ## dblToStr(float, int)
0000000100424ee0	movq	-0x30(%rbp), %rdi
0000000100424ee4	movq	%rbx, %rsi
0000000100424ee7	callq	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendB8ne200100ERKS5_ ## std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>::append[abi:ne200100](std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&)
0000000100424eec	jmp	0x1004247ef
0000000100424ef1	addq	$0x10, %r12
0000000100424ef5	movq	%r12, -0x40(%rbp)
0000000100424ef9	cmpb	$0x0, -0x51(%rbp)
0000000100424efd	jne	0x100425115
0000000100424f03	leaq	-0x80(%rbp), %rbx
0000000100424f07	movq	%rbx, %rdi
0000000100424f0a	movq	-0x50(%rbp), %rsi
0000000100424f0e	callq	__ZN7SDBInfo16artistTitleRemixEv ## SDBInfo::artistTitleRemix()
0000000100424f13	movq	-0x30(%rbp), %rdi
0000000100424f17	movq	%rbx, %rsi
0000000100424f1a	callq	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendB8ne200100ERKS5_ ## std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>::append[abi:ne200100](std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&)
0000000100424f1f	jmp	0x1004247ef
0000000100424f24	addq	$0xa, %r12
0000000100424f28	movq	%r12, -0x40(%rbp)
0000000100424f2c	cmpb	$0x0, -0x51(%rbp)
0000000100424f30	jne	0x100425115
0000000100424f36	leaq	-0x80(%rbp), %rbx
0000000100424f3a	movq	%rbx, %rdi
0000000100424f3d	movq	-0x50(%rbp), %rsi
0000000100424f41	callq	__ZN7SDBInfo10titleRemixEv      ## SDBInfo::titleRemix()
0000000100424f46	movq	-0x30(%rbp), %rdi
0000000100424f4a	movq	%rbx, %rsi
0000000100424f4d	callq	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendB8ne200100ERKS5_ ## std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>::append[abi:ne200100](std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&)
0000000100424f52	jmp	0x1004247ef
0000000100424f57	addq	$0x6, %r12
0000000100424f5b	movq	%r12, -0x40(%rbp)
0000000100424f5f	cmpq	$0x0, -0x48(%rbp)
0000000100424f64	je	0x100424ffb
0000000100424f6a	movq	-0x48(%rbp), %rax
0000000100424f6e	cmpb	$0x1, 0x291(%rax)
0000000100424f75	jne	0x100424ffb
0000000100424f7b	leaq	-0xa0(%rbp), %rdi
0000000100424f82	movq	-0x48(%rbp), %rsi
0000000100424f86	callq	__ZN5CDeck13getMuteStringEv     ## CDeck::getMuteString()
0000000100424f8b	leaq	-0xe0(%rbp), %rdi
0000000100424f92	leaq	0x51b7895(%rip), %rsi           ## literal pool for: " - "
0000000100424f99	callq	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEC2B8ne200100ILi0EEEPKc ## std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>::basic_string[abi:ne200100]<0>(char const*)
0000000100424f9e	leaq	-0x80(%rbp), %rdi
0000000100424fa2	leaq	-0xa0(%rbp), %rsi
0000000100424fa9	leaq	-0xe0(%rbp), %rdx
0000000100424fb0	callq	__ZNSt3__1plB8ne200100IcNS_11char_traitsIcEENS_9allocatorIcEEEENS_12basic_stringIT_T0_T1_EEOS9_RKS9_ ## std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> std::__1::operator+[abi:ne200100]<char, std::__1::char_traits<char>, std::__1::allocator<char>>(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>&&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&)
0000000100424fb5	movq	-0x30(%rbp), %rdi
0000000100424fb9	leaq	-0x80(%rbp), %rsi
0000000100424fbd	callq	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendB8ne200100ERKS5_ ## std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>::append[abi:ne200100](std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&)
0000000100424fc2	testb	$0x1, -0x80(%rbp)
0000000100424fc6	je	0x100424fd1
0000000100424fc8	movq	-0x70(%rbp), %rdi
0000000100424fcc	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
0000000100424fd1	testb	$0x1, -0xe0(%rbp)
0000000100424fd8	je	0x100424fe6
0000000100424fda	movq	-0xd0(%rbp), %rdi
0000000100424fe1	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
0000000100424fe6	testb	$0x1, -0xa0(%rbp)
0000000100424fed	je	0x100424ffb
0000000100424fef	movq	-0x90(%rbp), %rdi
0000000100424ff6	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
0000000100424ffb	movq	-0xc8(%rbp), %rax
0000000100425002	cmpl	$-0x1, 0x244(%rax)
0000000100425009	je	0x1004247fe
000000010042500f	cmpb	$0x0, -0x51(%rbp)
0000000100425013	jne	0x100425115
0000000100425019	movq	-0x50(%rbp), %rax
000000010042501d	movq	0x18(%rax), %r14
0000000100425021	jmp	0x1004251c5
0000000100425026	addq	$0x5, %r12
000000010042502a	movq	%r12, -0x40(%rbp)
000000010042502e	cmpq	$0x0, -0x48(%rbp)
0000000100425033	je	0x1004250ca
0000000100425039	movq	-0x48(%rbp), %rax
000000010042503d	cmpb	$0x1, 0x291(%rax)
0000000100425044	jne	0x1004250ca
000000010042504a	leaq	-0xa0(%rbp), %rdi
0000000100425051	movq	-0x48(%rbp), %rsi
0000000100425055	callq	__ZN5CDeck13getMuteStringEv     ## CDeck::getMuteString()
000000010042505a	leaq	-0xe0(%rbp), %rdi
0000000100425061	leaq	0x51b77c6(%rip), %rsi           ## literal pool for: " - "
0000000100425068	callq	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEC2B8ne200100ILi0EEEPKc ## std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>::basic_string[abi:ne200100]<0>(char const*)
000000010042506d	leaq	-0x80(%rbp), %rdi
0000000100425071	leaq	-0xa0(%rbp), %rsi
0000000100425078	leaq	-0xe0(%rbp), %rdx
000000010042507f	callq	__ZNSt3__1plB8ne200100IcNS_11char_traitsIcEENS_9allocatorIcEEEENS_12basic_stringIT_T0_T1_EEOS9_RKS9_ ## std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> std::__1::operator+[abi:ne200100]<char, std::__1::char_traits<char>, std::__1::allocator<char>>(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>&&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&)
0000000100425084	movq	-0x30(%rbp), %rdi
0000000100425088	leaq	-0x80(%rbp), %rsi
000000010042508c	callq	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendB8ne200100ERKS5_ ## std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>::append[abi:ne200100](std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&)
0000000100425091	testb	$0x1, -0x80(%rbp)
0000000100425095	je	0x1004250a0
0000000100425097	movq	-0x70(%rbp), %rdi
000000010042509b	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
00000001004250a0	testb	$0x1, -0xe0(%rbp)
00000001004250a7	je	0x1004250b5
00000001004250a9	movq	-0xd0(%rbp), %rdi
00000001004250b0	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
00000001004250b5	testb	$0x1, -0xa0(%rbp)
00000001004250bc	je	0x1004250ca
00000001004250be	movq	-0x90(%rbp), %rdi
00000001004250c5	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
00000001004250ca	movq	-0xc8(%rbp), %rax
00000001004250d1	movl	0x244(%rax), %eax
00000001004250d7	cmpl	$-0x2, %eax
00000001004250da	je	0x1004250f8
00000001004250dc	cmpl	$-0x1, %eax
00000001004250df	jne	0x10042510f
00000001004250e1	leaq	_messageEngine(%rip), %rdi
00000001004250e8	leaq	0x5204da5(%rip), %rsi           ## literal pool for: "error"
00000001004250ef	leaq	0x51b8c08(%rip), %rdx           ## literal pool for: "Error"
00000001004250f6	jmp	0x10042512a
00000001004250f8	leaq	_messageEngine(%rip), %rdi
00000001004250ff	leaq	0x51b8114(%rip), %rsi           ## literal pool for: "msg"
0000000100425106	leaq	0x51e147c(%rip), %rdx           ## literal pool for: "DragToStart"
000000010042510d	jmp	0x10042512a
000000010042510f	cmpb	$0x0, -0x51(%rbp)
0000000100425113	je	0x100425163
0000000100425115	leaq	_messageEngine(%rip), %rdi
000000010042511c	leaq	0x51b80f7(%rip), %rsi           ## literal pool for: "msg"
0000000100425123	leaq	0x51e1458(%rip), %rdx           ## literal pool for: "Hidden"
000000010042512a	callq	__ZN14CMessageEngine10getMessageEPKcS1_ ## CMessageEngine::getMessage(char const*, char const*)
000000010042512f	movq	%rax, %r14
0000000100425132	movq	%rax, %rdi
0000000100425135	callq	0x104fe92ae                     ## symbol stub for: _strlen
000000010042513a	movq	-0x30(%rbp), %r15
000000010042513e	movq	%r15, %rdi
0000000100425141	movq	%r14, %rsi
0000000100425144	movq	%rax, %rdx
0000000100425147	callq	0x104fe8516                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm
000000010042514c	jmp	0x100423002
0000000100425151	addq	$0x7, %r12
0000000100425155	movq	%r12, -0x40(%rbp)
0000000100425159	movq	-0x50(%rbp), %rax
000000010042515d	movq	0x58(%rax), %r14
0000000100425161	jmp	0x1004251c5
0000000100425163	movq	-0x50(%rbp), %rax
0000000100425167	movq	0x20(%rax), %r14
000000010042516b	jmp	0x1004251c5
000000010042516d	addq	$0x5, %r12
0000000100425171	movq	%r12, -0x40(%rbp)
0000000100425175	movq	-0x50(%rbp), %rax
0000000100425179	movq	0x50(%rax), %r14
000000010042517d	jmp	0x1004251c5
000000010042517f	addq	$0x8, %r12
0000000100425183	movq	%r12, -0x40(%rbp)
0000000100425187	movq	-0x50(%rbp), %rax
000000010042518b	movq	0x40(%rax), %r14
000000010042518f	jmp	0x1004251c5
0000000100425191	addq	$0x5, %r12
0000000100425195	movq	%r12, -0x40(%rbp)
0000000100425199	movq	-0x50(%rbp), %rax
000000010042519d	movq	0x38(%rax), %r14
00000001004251a1	jmp	0x1004251c5
00000001004251a3	addq	$0x5, %r12
00000001004251a7	movq	%r12, -0x40(%rbp)
00000001004251ab	movq	-0x50(%rbp), %rax
00000001004251af	movq	0x30(%rax), %r14
00000001004251b3	jmp	0x1004251c5
00000001004251b5	addq	$0x7, %r12
00000001004251b9	movq	%r12, -0x40(%rbp)
00000001004251bd	movq	-0x50(%rbp), %rax
00000001004251c1	movq	0x28(%rax), %r14
00000001004251c5	testq	%r14, %r14
00000001004251c8	je	0x1004247fe
00000001004251ce	movq	%r14, %rdi
00000001004251d1	jmp	0x100425135
00000001004251d6	addq	$0x6, %r12
00000001004251da	movq	%r12, -0x40(%rbp)
00000001004251de	xorl	%edi, %edi
00000001004251e0	callq	0x104fe9344                     ## symbol stub for: _time
00000001004251e5	leaq	-0x80(%rbp), %rbx
00000001004251e9	movq	%rbx, %rdi
00000001004251ec	leaq	0x51e13ba(%rip), %rsi           ## literal pool for: "%I:%M%p"
00000001004251f3	movq	%rax, %rdx
00000001004251f6	callq	__Z14formatDateTimePKcl         ## formatDateTime(char const*, long)
00000001004251fb	movq	-0x30(%rbp), %rdi
00000001004251ff	movq	%rbx, %rsi
0000000100425202	callq	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendB8ne200100ERKS5_ ## std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>::append[abi:ne200100](std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&)
0000000100425207	jmp	0x1004247ef
000000010042520c	addq	$0x8, %r12
0000000100425210	movq	%r12, -0x40(%rbp)
0000000100425214	xorl	%edi, %edi
0000000100425216	callq	0x104fe9344                     ## symbol stub for: _time
000000010042521b	leaq	-0x80(%rbp), %rbx
000000010042521f	movq	%rbx, %rdi
0000000100425222	leaq	0x51cfb07(%rip), %rsi           ## literal pool for: "%H:%M:%S"
0000000100425229	movq	%rax, %rdx
000000010042522c	callq	__Z14formatDateTimePKcl         ## formatDateTime(char const*, long)
0000000100425231	movq	-0x30(%rbp), %rdi
0000000100425235	movq	%rbx, %rsi
0000000100425238	callq	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendB8ne200100ERKS5_ ## std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>::append[abi:ne200100](std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&)
000000010042523d	jmp	0x1004247ef
0000000100425242	addq	$0x4, %r12
0000000100425246	movq	%r12, -0x40(%rbp)
000000010042524a	xorl	%edi, %edi
000000010042524c	callq	0x104fe9344                     ## symbol stub for: _time
0000000100425251	leaq	-0x80(%rbp), %rbx
0000000100425255	movq	%rbx, %rdi
0000000100425258	leaq	0x51c37d8(%rip), %rsi           ## literal pool for: "%H:%M"
000000010042525f	movq	%rax, %rdx
0000000100425262	callq	__Z14formatDateTimePKcl         ## formatDateTime(char const*, long)
0000000100425267	movq	-0x30(%rbp), %rdi
000000010042526b	movq	%rbx, %rsi
000000010042526e	callq	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendB8ne200100ERKS5_ ## std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>::append[abi:ne200100](std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&)
0000000100425273	jmp	0x1004247ef
0000000100425278	addq	$0x7, %r12
000000010042527c	movq	%r12, -0x40(%rbp)
0000000100425280	xorpd	%xmm0, %xmm0
0000000100425284	ucomisd	_counterStartTime(%rip), %xmm0
000000010042528c	jbe	0x10042529b
000000010042528e	callq	__Z16timeGetExactTimev          ## timeGetExactTime()
0000000100425293	movsd	%xmm0, _counterStartTime(%rip)
000000010042529b	callq	__Z16timeGetExactTimev          ## timeGetExactTime()
00000001004252a0	subsd	_counterStartTime(%rip), %xmm0
00000001004252a8	divsd	0x4d68468(%rip), %xmm0
00000001004252b0	cvtsd2ss	%xmm0, %xmm0
00000001004252b4	leaq	-0x80(%rbp), %rbx
00000001004252b8	movq	%rbx, %rdi
00000001004252bb	movl	$CONFIG_VP9, %esi
00000001004252c0	callq	__Z10formatTimefi               ## formatTime(float, int)
00000001004252c5	movq	-0x30(%rbp), %rdi
00000001004252c9	movq	%rbx, %rsi
00000001004252cc	callq	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendB8ne200100ERKS5_ ## std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>::append[abi:ne200100](std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&)
00000001004252d1	jmp	0x1004247ef
00000001004252d6	addq	$0xa, %r12
00000001004252da	movq	%r12, -0x40(%rbp)
00000001004252de	movq	-0x48(%rbp), %rdi
00000001004252e2	callq	__ZN13CPluginEngine13getPluginDeckEP5CDeck ## CPluginEngine::getPluginDeck(CDeck*)
00000001004252e7	leaq	_pluginEngine(%rip), %rdi
00000001004252ee	movl	%eax, %esi
00000001004252f0	movl	$0x15, %edx
00000001004252f5	jmp	0x10042535d
00000001004252f7	leaq	0xa(%r12), %rax
00000001004252fc	movq	%rax, -0x40(%rbp)
0000000100425300	movb	0xa(%r12), %al
0000000100425305	leal	-0x30(%rax), %ecx
0000000100425308	xorl	%r14d, %r14d
000000010042530b	cmpb	$0x9, %cl
000000010042530e	ja	0x100425337
0000000100425310	addq	$0xb, %r12
0000000100425314	xorl	%r14d, %r14d
0000000100425317	leal	CONFIG_EMULATE_HARDWARE(%r14,%r14,4), %ecx
000000010042531b	addb	$-0x30, %al
000000010042531d	movzbl	%al, %eax
0000000100425320	leal	CONFIG_EMULATE_HARDWARE(%rax,%rcx,2), %r14d
0000000100425324	movq	%r12, -0x40(%rbp)
0000000100425328	movb	CONFIG_EMULATE_HARDWARE(%r12), %al
000000010042532c	leal	-0x30(%rax), %ecx
000000010042532f	incq	%r12
0000000100425332	cmpb	$0xa, %cl
0000000100425335	jb	0x100425317
0000000100425337	cmpl	$0x2, %r14d
000000010042533b	movl	$CONFIG_VP9, %eax
0000000100425340	cmovll	%eax, %r14d
0000000100425344	movq	-0x48(%rbp), %rdi
0000000100425348	callq	__ZN13CPluginEngine13getPluginDeckEP5CDeck ## CPluginEngine::getPluginDeck(CDeck*)
000000010042534d	addl	$0x14, %r14d
0000000100425351	leaq	_pluginEngine(%rip), %rdi
0000000100425358	movl	%eax, %esi
000000010042535a	movl	%r14d, %edx
000000010042535d	callq	__ZN13CPluginEngine13getPluginFileEii ## CPluginEngine::getPluginFile(int, int)
0000000100425362	testq	%rax, %rax
0000000100425365	je	0x1004247fe
000000010042536b	addq	$0x20, %rax
000000010042536f	movq	-0x30(%rbp), %r15
0000000100425373	movq	%r15, %rdi
0000000100425376	movq	%rax, %rsi
0000000100425379	callq	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendB8ne200100ERKS5_ ## std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>::append[abi:ne200100](std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&)
000000010042537e	jmp	0x100423002
0000000100425383	leaq	0xa(%r12), %rax
0000000100425388	movq	%rax, -0x40(%rbp)
000000010042538c	movb	0xa(%r12), %al
0000000100425391	leal	-0x30(%rax), %ecx
0000000100425394	movl	$0xffffffff, %esi               ## imm = 0xFFFFFFFF
0000000100425399	cmpb	$0x9, %cl
000000010042539c	ja	0x1004253c4
000000010042539e	addq	$0xb, %r12
00000001004253a2	xorl	%esi, %esi
00000001004253a4	leal	CONFIG_EMULATE_HARDWARE(%rsi,%rsi,4), %ecx
00000001004253a7	addb	$-0x30, %al
00000001004253a9	movzbl	%al, %eax
00000001004253ac	leal	CONFIG_EMULATE_HARDWARE(%rax,%rcx,2), %esi
00000001004253af	movq	%r12, -0x40(%rbp)
00000001004253b3	movb	CONFIG_EMULATE_HARDWARE(%r12), %al
00000001004253b7	leal	-0x30(%rax), %ecx
00000001004253ba	incq	%r12
00000001004253bd	cmpb	$0xa, %cl
00000001004253c0	jb	0x1004253a4
00000001004253c2	decl	%esi
00000001004253c4	movq	-0x48(%rbp), %rax
00000001004253c8	movl	0x240(%rax), %edx
00000001004253ce	leaq	-0x80(%rbp), %rbx
00000001004253d2	movq	%rbx, %rdi
00000001004253d5	callq	__Z23djcButtonsGetActionTextii  ## djcButtonsGetActionText(int, int)
00000001004253da	movq	-0x30(%rbp), %rdi
00000001004253de	movq	%rbx, %rsi
00000001004253e1	callq	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendB8ne200100ERKS5_ ## std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>::append[abi:ne200100](std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&)
00000001004253e6	jmp	0x1004247ef
00000001004253eb	addq	$0xa, %r12
00000001004253ef	movq	%r12, -0x40(%rbp)
00000001004253f3	leaq	_sampler(%rip), %rbx
00000001004253fa	leaq	0x268(%rbx), %rdi
0000000100425401	callq	__ZN15CThreadSyncRWNR9EnterReadEv ## CThreadSyncRWNR::EnterRead()
0000000100425406	movq	%rbx, %rdi
0000000100425409	movq	-0x48(%rbp), %rsi
000000010042540d	callq	__ZN14CSamplerEngine14getDeckSamplesEP5CDeck ## CSamplerEngine::getDeckSamples(CDeck*)
0000000100425412	movq	CONFIG_EMULATE_HARDWARE(%rax), %rcx
0000000100425415	movq	0x8(%rax), %rax
0000000100425419	subq	%rcx, %rax
000000010042541c	je	0x1004254c5
0000000100425422	movq	-0x48(%rbp), %rdx
0000000100425426	movslq	0x240(%rdx), %rdx
000000010042542d	leaq	_sampler(%rip), %rsi
0000000100425434	movl	0x3dc(%rsi,%rdx,4), %edx
000000010042543b	sarq	$0x3, %rax
000000010042543f	cmpq	$0x1, %rax
0000000100425443	adcq	$0x0, %rax
0000000100425447	xorl	%edi, %edi
0000000100425449	movq	CONFIG_EMULATE_HARDWARE(%rcx,%rdi,8), %rsi
000000010042544d	cmpl	%edx, 0x560(%rsi)
0000000100425453	je	0x1004254af
0000000100425455	incq	%rdi
0000000100425458	cmpq	%rdi, %rax
000000010042545b	jne	0x100425449
000000010042545d	jmp	0x1004254c5
000000010042545f	addq	$0x7, %r12
0000000100425463	cmpl	$0x0, -0xbc(%rbp)
000000010042546a	movq	%r12, -0x40(%rbp)
000000010042546e	movq	-0x48(%rbp), %rdi
0000000100425472	movl	$CONFIG_EMULATE_HARDWARE, %eax
0000000100425477	cmoveq	%rax, %rdi
000000010042547b	movq	%rdi, -0x48(%rbp)
000000010042547f	callq	__ZN13CPluginEngine13getPluginDeckEP5CDeck ## CPluginEngine::getPluginDeck(CDeck*)
0000000100425484	leaq	_pluginEngine(%rip), %rdi
000000010042548b	movl	%eax, %esi
000000010042548d	movl	$CONFIG_VP9, %edx
0000000100425492	jmp	0x10042535d
0000000100425497	addq	$0xf, %r12
000000010042549b	movq	%r12, -0x40(%rbp)
000000010042549f	leaq	_pluginEngine(%rip), %rdi
00000001004254a6	xorl	%esi, %esi
00000001004254a8	xorl	%edx, %edx
00000001004254aa	jmp	0x10042535d
00000001004254af	cmpq	$-0x1, %rdi
00000001004254b3	je	0x1004254c5
00000001004254b5	addq	$0x4d0, %rsi                    ## imm = 0x4D0
00000001004254bc	movq	-0x30(%rbp), %rdi
00000001004254c0	callq	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendB8ne200100ERKS5_ ## std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>::append[abi:ne200100](std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&)
00000001004254c5	movq	-0xe8(%rbp), %rdi
00000001004254cc	callq	__ZN15CThreadSyncRWNR9LeaveReadEv ## CThreadSyncRWNR::LeaveRead()
00000001004254d1	movq	-0x30(%rbp), %r15
00000001004254d5	jmp	0x100423002
00000001004254da	addq	$0xb, %r12
00000001004254de	movq	%r12, -0x40(%rbp)
00000001004254e2	leaq	_Config(%rip), %rax
00000001004254e9	movb	0x6620(%rax), %al
00000001004254ef	testb	$0x1, %al
00000001004254f1	jne	0x100425547
00000001004254f3	testb	%al, %al
00000001004254f5	je	0x1004255af
00000001004254fb	leaq	_Config(%rip), %rcx
0000000100425502	movq	0x6630(%rcx), %rax
0000000100425509	movq	%rax, -0x70(%rbp)
000000010042550d	movups	0x6620(%rcx), %xmm0
0000000100425514	movaps	%xmm0, -0x80(%rbp)
0000000100425518	jmp	0x100425571
000000010042551a	addq	$0x3, %r12
000000010042551e	movq	%r12, -0x40(%rbp)
0000000100425522	leaq	_Config(%rip), %rax
0000000100425529	cmpl	$0x0, 0x9d38(%rax)
0000000100425530	je	0x1004255d9
0000000100425536	leaq	_soundEngine(%rip), %rax
000000010042553d	movss	0x48(%rax), %xmm0
0000000100425542	jmp	0x1004255e5
0000000100425547	leaq	_Config(%rip), %rax
000000010042554e	movq	0x6628(%rax), %rdx
0000000100425555	testq	%rdx, %rdx
0000000100425558	je	0x1004255af
000000010042555a	leaq	_Config(%rip), %rax
0000000100425561	movq	0x6630(%rax), %rsi
0000000100425568	leaq	-0x80(%rbp), %rdi
000000010042556c	callq	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE25__init_copy_ctor_externalEPKcm ## std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>::__init_copy_ctor_external(char const*, unsigned long)
0000000100425571	movq	-0x30(%rbp), %rdi
0000000100425575	leaq	-0x80(%rbp), %rsi
0000000100425579	callq	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendB8ne200100ERKS5_ ## std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>::append[abi:ne200100](std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&)
000000010042557e	jmp	0x1004247ef
0000000100425583	addq	$0x6, %r12
0000000100425587	movq	%r12, -0x40(%rbp)
000000010042558b	leaq	-0x80(%rbp), %rbx
000000010042558f	movq	%rbx, %rdi
0000000100425592	leaq	_status(%rip), %rsi
0000000100425599	callq	__ZN7CStatus3getEv              ## CStatus::get()
000000010042559e	movq	-0x30(%rbp), %rdi
00000001004255a2	movq	%rbx, %rsi
00000001004255a5	callq	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendB8ne200100ERKS5_ ## std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>::append[abi:ne200100](std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&)
00000001004255aa	jmp	0x1004247ef
00000001004255af	movl	$FGData.num_y_points, %edx
00000001004255b4	movq	-0x30(%rbp), %r15
00000001004255b8	movq	%r15, %rdi
00000001004255bb	leaq	0x51b8994(%rip), %rsi           ## literal pool for: "None"
00000001004255c2	callq	0x104fe8516                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm
00000001004255c7	jmp	0x100423002
00000001004255cc	addq	$0x4, %r12
00000001004255d0	movq	%r12, -0x40(%rbp)
00000001004255d4	jmp	0x1004247fe
00000001004255d9	leaq	_cpuMeter(%rip), %rdi
00000001004255e0	callq	__ZN9CCpuMeter7getPeakEv        ## CCpuMeter::getPeak()
00000001004255e5	mulss	0x4d680d3(%rip), %xmm0
00000001004255ed	callq	0x104fe8e6a                     ## symbol stub for: _lroundf
00000001004255f2	movl	%eax, -0xa0(%rbp)
00000001004255f8	movl	$0x5, %edx
00000001004255fd	movl	$CONFIG_VP9, %ecx
0000000100425602	leaq	-0x80(%rbp), %rbx
0000000100425606	movq	%rbx, %rdi
0000000100425609	leaq	0x51b7170(%rip), %rsi           ## literal pool for: "{:02}"
0000000100425610	leaq	-0xa0(%rbp), %r8
0000000100425617	callq	__ZN3fmt3v127vformatENS0_17basic_string_viewIcEENS0_17basic_format_argsINS0_7contextEEE ## fmt::v12::vformat(fmt::v12::basic_string_view<char>, fmt::v12::basic_format_args<fmt::v12::context>)
000000010042561c	movq	-0x30(%rbp), %rdi
0000000100425620	movq	%rbx, %rsi
0000000100425623	callq	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendB8ne200100ERKS5_ ## std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>::append[abi:ne200100](std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&)
0000000100425628	jmp	0x1004247ef
000000010042562d	addq	$0xb, %r12
0000000100425631	movq	%r12, -0x40(%rbp)
0000000100425635	leaq	_defaultDeck(%rip), %rax
000000010042563c	movq	CONFIG_EMULATE_HARDWARE(%rax), %rax
000000010042563f	movl	0x240(%rax), %esi
0000000100425645	incl	%esi
0000000100425647	leaq	-0x80(%rbp), %rbx
000000010042564b	movq	%rbx, %rdi
000000010042564e	callq	__Z8intToStri                   ## intToStr(int)
0000000100425653	movq	-0x30(%rbp), %rdi
0000000100425657	movq	%rbx, %rsi
000000010042565a	callq	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendB8ne200100ERKS5_ ## std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>::append[abi:ne200100](std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&)
000000010042565f	jmp	0x1004247ef
0000000100425664	addq	$0xa, %r12
0000000100425668	movq	%r12, -0x40(%rbp)
000000010042566c	callq	__ZN5CDeck13getActiveDeckEv     ## CDeck::getActiveDeck()
0000000100425671	movl	0x240(%rax), %esi
0000000100425677	incl	%esi
0000000100425679	leaq	-0x80(%rbp), %rbx
000000010042567d	movq	%rbx, %rdi
0000000100425680	callq	__Z8intToStri                   ## intToStr(int)
0000000100425685	movq	-0x30(%rbp), %rdi
0000000100425689	movq	%rbx, %rsi
000000010042568c	callq	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendB8ne200100ERKS5_ ## std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>::append[abi:ne200100](std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&)
0000000100425691	jmp	0x1004247ef
0000000100425696	addq	$0xe, %r12
000000010042569a	movq	%r12, -0x40(%rbp)
000000010042569e	movq	-0x50(%rbp), %rax
00000001004256a2	movq	0x110(%rax), %r14
00000001004256a9	testq	%r14, %r14
00000001004256ac	jne	0x1004251c5
00000001004256b2	cmpq	$0x0, -0xc8(%rbp)
00000001004256ba	je	0x1004251c5
00000001004256c0	movq	-0xc8(%rbp), %rax
00000001004256c7	cmpl	$-0x2, 0x244(%rax)
00000001004256ce	je	0x1004247fe
00000001004256d4	movl	$0x26, %edx
00000001004256d9	movq	-0x30(%rbp), %r15
00000001004256dd	movq	%r15, %rdi
00000001004256e0	leaq	0x51e0f40(%rip), %rsi           ## literal pool for: "{00000000-0000-0000-0000-000000000000}"
00000001004256e7	callq	0x104fe8516                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm
00000001004256ec	jmp	0x100423002
00000001004256f1	movq	%r12, %rdi
00000001004256f4	callq	0x104fe92ae                     ## symbol stub for: _strlen
00000001004256f9	movq	%r15, %rdi
00000001004256fc	movq	%r12, %rsi
00000001004256ff	movq	%rax, %rdx
0000000100425702	callq	0x104fe8516                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm
0000000100425707	xorl	%eax, %eax
0000000100425709	addq	$rf.n_tile_threads, %rsp
0000000100425710	popq	%rbx
0000000100425711	popq	%r12
0000000100425713	popq	%r13
0000000100425715	popq	%r14
0000000100425717	popq	%r15
0000000100425719	popq	%rbp
000000010042571a	retq
000000010042571b	jmp	0x10042581a
0000000100425720	jmp	0x10042581a
0000000100425725	jmp	0x10042581a
000000010042572a	jmp	0x10042581a
000000010042572f	jmp	0x10042581a
0000000100425734	jmp	0x1004257c5
0000000100425739	jmp	0x10042573b
000000010042573b	movq	%rax, %rbx
000000010042573e	movl	$0x268, %edi                    ## imm = 0x268
0000000100425743	addq	0x5399f4e(%rip), %rdi
000000010042574a	callq	__ZN15CThreadSyncRWNR9LeaveReadEv ## CThreadSyncRWNR::LeaveRead()
000000010042574f	jmp	0x10042586c
0000000100425754	jmp	0x1004257c5
0000000100425756	jmp	0x10042581a
000000010042575b	jmp	0x10042581a
0000000100425760	jmp	0x10042581a
0000000100425765	jmp	0x10042581a
000000010042576a	jmp	0x10042581a
000000010042576f	jmp	0x100425775
0000000100425771	jmp	0x100425789
0000000100425773	jmp	0x1004257a3
0000000100425775	movq	%rax, %rbx
0000000100425778	testb	$0x1, -0x80(%rbp)
000000010042577c	je	0x10042578c
000000010042577e	movq	-0x70(%rbp), %rdi
0000000100425782	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
0000000100425787	jmp	0x10042578c
0000000100425789	movq	%rax, %rbx
000000010042578c	testb	$0x1, -0xe0(%rbp)
0000000100425793	je	0x1004257a6
0000000100425795	movq	-0xd0(%rbp), %rdi
000000010042579c	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
00000001004257a1	jmp	0x1004257a6
00000001004257a3	movq	%rax, %rbx
00000001004257a6	testb	$0x1, -0xa0(%rbp)
00000001004257ad	je	0x10042586c
00000001004257b3	movq	-0x90(%rbp), %rdi
00000001004257ba	jmp	0x100425867
00000001004257bf	jmp	0x10042581a
00000001004257c1	jmp	0x10042581a
00000001004257c3	jmp	0x10042581a
00000001004257c5	movq	%rax, %rdi
00000001004257c8	callq	___clang_call_terminate
00000001004257cd	jmp	0x10042581a
00000001004257cf	jmp	0x10042581a
00000001004257d1	jmp	0x10042581a
00000001004257d3	jmp	0x10042581a
00000001004257d5	jmp	0x10042581a
00000001004257d7	jmp	0x10042581a
00000001004257d9	jmp	0x10042581a
00000001004257db	jmp	0x10042581a
00000001004257dd	jmp	0x10042581a
00000001004257df	jmp	0x10042581a
00000001004257e1	jmp	0x10042581a
00000001004257e3	jmp	0x10042581a
00000001004257e5	jmp	0x10042581a
00000001004257e7	jmp	0x10042581a
00000001004257e9	jmp	0x1004257f5
00000001004257eb	jmp	0x10042581f
00000001004257ed	jmp	0x1004257f5
00000001004257ef	jmp	0x10042581f
00000001004257f1	jmp	0x1004257f5
00000001004257f3	jmp	0x10042581f
00000001004257f5	movq	%rax, %rbx
00000001004257f8	testb	$0x1, -0xa0(%rbp)
00000001004257ff	je	0x100425822
0000000100425801	movq	-0x90(%rbp), %rdi
0000000100425808	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
000000010042580d	jmp	0x100425822
000000010042580f	jmp	0x10042581f
0000000100425811	movq	%rax, %rbx
0000000100425814	jmp	0x100425831
0000000100425816	jmp	0x100425845
0000000100425818	jmp	0x100425845
000000010042581a	movq	%rax, %rbx
000000010042581d	jmp	0x10042585d
000000010042581f	movq	%rax, %rbx
0000000100425822	testb	$0x1, -0x78(%rbp)
0000000100425826	je	0x100425831
0000000100425828	movq	-0x68(%rbp), %rdi
000000010042582c	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
0000000100425831	lock
0000000100425832	decl	0x8(%r12)
0000000100425837	jg	0x10042586c
0000000100425839	movq	CONFIG_EMULATE_HARDWARE(%r12), %rax
000000010042583d	movq	%r12, %rdi
0000000100425840	callq	*0x8(%rax)
0000000100425843	jmp	0x10042586c
0000000100425845	movq	%rax, %rbx
0000000100425848	testb	$0x1, -0xa0(%rbp)
000000010042584f	je	0x10042585d
0000000100425851	movq	-0x90(%rbp), %rdi
0000000100425858	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
000000010042585d	testb	$0x1, -0x80(%rbp)
0000000100425861	je	0x10042586c
0000000100425863	movq	-0x70(%rbp), %rdi
0000000100425867	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
000000010042586c	movq	%rbx, %rdi
000000010042586f	callq	0x104fe8456                     ## symbol stub for: __Unwind_Resume
