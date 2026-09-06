__ZN10CSkinPanelC2EP8CXMLNodeP6CImageP11CSkinWindow:
000000010044f980	pushq	%rbp
000000010044f981	movq	%rsp, %rbp
000000010044f984	pushq	%r15
000000010044f986	pushq	%r14
000000010044f988	pushq	%r13
000000010044f98a	pushq	%r12
000000010044f98c	pushq	%rbx
000000010044f98d	subq	$0x18, %rsp
000000010044f991	movq	%rcx, %rbx
000000010044f994	movq	%rdx, %r14
000000010044f997	movq	%rsi, %r12
000000010044f99a	movq	%rdi, %r15
000000010044f99d	callq	__ZN14ISkinContainerC2Ev        ## ISkinContainer::ISkinContainer()
000000010044f9a2	leaq	0x1e253b7(%rip), %rax
000000010044f9a9	movq	%rax, CONFIG_BETTER_HW_COMPATIBILITY(%r15)
000000010044f9ac	xorl	%eax, %eax
000000010044f9ae	movq	%rax, 0x1a8(%r15)
000000010044f9b5	movq	%rax, 0x1a0(%r15)
000000010044f9bc	movb	$0x0, 0x1b2(%r15)
000000010044f9c4	movw	$CONFIG_BETTER_HW_COMPATIBILITY, 0x1b0(%r15)
000000010044f9ce	movq	%rbx, -0x30(%rbp)
000000010044f9d2	movq	%rbx, 0x198(%r15)
000000010044f9d9	movl	$0xffffffff, 0x3c(%r15)         ## imm = 0xFFFFFFFF
000000010044f9e1	movq	%r15, %rdi
000000010044f9e4	movq	%r12, %rsi
000000010044f9e7	movq	%r14, %rdx
000000010044f9ea	callq	__ZN11ISkinObject4loadEP8CXMLNodeP6CImage ## ISkinObject::load(CXMLNode*, CImage*)
000000010044f9ef	leaq	0x1ab1723(%rip), %rsi           ## literal pool for: "background"
000000010044f9f6	leaq	0x1ab184b(%rip), %rdx           ## literal pool for: "down"
000000010044f9fd	movq	%r12, %rdi
000000010044fa00	callq	__ZNK8CXMLNode9getChild2EPKcS1_ ## CXMLNode::getChild2(char const*, char const*) const
000000010044fa05	movq	%rax, %rbx
000000010044fa08	leaq	0x1ab097e(%rip), %rsi           ## literal pool for: "clipmask"
000000010044fa0f	movl	$0x8, %edx
000000010044fa14	movq	%r12, %rdi
000000010044fa17	callq	__ZNK8CXMLNode8getChildEPKci    ## CXMLNode::getChild(char const*, int) const
000000010044fa1c	movq	%r15, %rdi
000000010044fa1f	movq	%r14, %rsi
000000010044fa22	movq	%r12, %rdx
000000010044fa25	movq	%rbx, %rcx
000000010044fa28	movq	%rax, %r8
000000010044fa2b	callq	__ZN11ISkinObject8getImageEP6CImageP8CXMLNodeS3_S3_ ## ISkinObject::getImage(CImage*, CXMLNode*, CXMLNode*, CXMLNode*)
000000010044fa30	movq	%rax, 0xe8(%r15)
000000010044fa37	cmpb	$0x0, __ZN11ISkinObject11isVideoSkinE(%rip) ## ISkinObject::isVideoSkin
000000010044fa3e	je	0x10044fa49
000000010044fa40	leaq	_emptyString(%rip), %rsi
000000010044fa47	jmp	0x10044fa8e
000000010044fa49	leaq	0x1ad4a9e(%rip), %rsi           ## literal pool for: "name"
000000010044fa50	movl	$0x4, %edx
000000010044fa55	movq	%r12, %rdi
000000010044fa58	callq	__ZNK8CXMLNode8hasParamEPKci    ## CXMLNode::hasParam(char const*, int) const
000000010044fa5d	testb	%al, %al
000000010044fa5f	je	0x10044fa77
000000010044fa61	leaq	0x1ad4a86(%rip), %rsi           ## literal pool for: "name"
000000010044fa68	movl	$0x4, %edx
000000010044fa6d	movq	%r12, %rdi
000000010044fa70	callq	__ZN8CXMLNode8getParamEPKcm     ## CXMLNode::getParam(char const*, unsigned long)
000000010044fa75	jmp	0x10044fa8b
000000010044fa77	leaq	0x1aaeb5e(%rip), %rsi           ## literal pool for: "id"
000000010044fa7e	movl	$0x2, %edx
000000010044fa83	movq	%r12, %rdi
000000010044fa86	callq	__ZN8CXMLNode8getParamEPKcm     ## CXMLNode::getParam(char const*, unsigned long)
000000010044fa8b	movq	%rax, %rsi
000000010044fa8e	movzbl	CONFIG_BETTER_HW_COMPATIBILITY(%rsi), %eax
000000010044fa91	testb	$0x1, %al
000000010044fa93	movq	%r14, -0x38(%rbp)
000000010044fa97	jne	0x10044fa9e
000000010044fa99	shrq	%rax
000000010044fa9c	jmp	0x10044faa2
000000010044fa9e	movq	0x8(%rsi), %rax
000000010044faa2	testq	%rax, %rax
000000010044faa5	je	0x10044fbdc
000000010044faab	leaq	_skinEngine(%rip), %r13
000000010044fab2	movl	$CONFIG_ENCODERS, %edx
000000010044fab7	movq	%r13, %rdi
000000010044faba	callq	__ZN11CSkinEngine13getPanelIndexERKNSt3__112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEEb ## CSkinEngine::getPanelIndex(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, bool)
000000010044fabf	movl	%eax, 0x190(%r15)
000000010044fac6	leaq	0x1ab9c3a(%rip), %rsi           ## literal pool for: "group"
000000010044facd	movl	$0x5, %edx
000000010044fad2	movq	%r12, %rdi
000000010044fad5	callq	__ZN8CXMLNode8getParamEPKcm     ## CXMLNode::getParam(char const*, unsigned long)
000000010044fada	movslq	0x190(%r15), %rcx
000000010044fae1	movq	0x1c0(%r13), %rdx
000000010044fae8	leaq	CONFIG_BETTER_HW_COMPATIBILITY(%rcx,%rcx,4), %rcx
000000010044faec	shlq	$0x4, %rcx
000000010044faf0	leaq	0x18(%rdx,%rcx), %rdi
000000010044faf5	movq	%rax, %rsi
000000010044faf8	callq	0x101b5d706                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
000000010044fafd	leaq	0x1ad3a27(%rip), %rsi           ## literal pool for: "available"
000000010044fb04	movl	$0x9, %edx
000000010044fb09	movl	$CONFIG_ENCODERS, %ecx
000000010044fb0e	movq	%r12, %rdi
000000010044fb11	callq	__ZNK8CXMLNode14getBoolParamNSEPKcib ## CXMLNode::getBoolParamNS(char const*, int, bool) const
000000010044fb16	movslq	0x190(%r15), %rcx
000000010044fb1d	movq	0x1c0(%r13), %rdx
000000010044fb24	leaq	CONFIG_BETTER_HW_COMPATIBILITY(%rcx,%rcx,4), %rcx
000000010044fb28	shlq	$0x4, %rcx
000000010044fb2c	movb	%al, 0x49(%rdx,%rcx)
000000010044fb30	leaq	0x1ad39fe(%rip), %rsi           ## literal pool for: "displayname"
000000010044fb37	movl	$0xb, %edx
000000010044fb3c	movq	%r12, %rdi
000000010044fb3f	callq	__ZN8CXMLNode8getParamEPKcm     ## CXMLNode::getParam(char const*, unsigned long)
000000010044fb44	movslq	0x190(%r15), %rcx
000000010044fb4b	movq	0x1c0(%r13), %rdx
000000010044fb52	leaq	CONFIG_BETTER_HW_COMPATIBILITY(%rcx,%rcx,4), %rcx
000000010044fb56	shlq	$0x4, %rcx
000000010044fb5a	leaq	0x30(%rdx,%rcx), %rdi
000000010044fb5f	movq	%rax, %rsi
000000010044fb62	callq	0x101b5d706                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
000000010044fb67	leaq	0x1ad39d3(%rip), %rsi           ## literal pool for: "forceshow"
000000010044fb6e	movl	$0x9, %edx
000000010044fb73	movq	%r12, %rdi
000000010044fb76	callq	__ZN8CXMLNode8getParamEPKcm     ## CXMLNode::getParam(char const*, unsigned long)
000000010044fb7b	movq	%rax, %r14
000000010044fb7e	movzbl	CONFIG_BETTER_HW_COMPATIBILITY(%rax), %ecx
000000010044fb81	movq	%rcx, %rax
000000010044fb84	shrq	%rax
000000010044fb87	movb	$0x1, %dl
000000010044fb89	andb	%cl, %dl
000000010044fb8b	movq	0x8(%r14), %rcx
000000010044fb8f	movq	%rcx, %rsi
000000010044fb92	cmoveq	%rax, %rsi
000000010044fb96	testq	%rsi, %rsi
000000010044fb99	je	0x10044fbe7
000000010044fb9b	cmpq	$0x3, %rsi
000000010044fb9f	jne	0x10044fe2d
000000010044fba5	leaq	0x1ad399f(%rip), %rsi           ## literal pool for: "1fx"
000000010044fbac	movq	%r14, %rdi
000000010044fbaf	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
000000010044fbb4	testb	%al, %al
000000010044fbb6	je	0x10044fe1d
000000010044fbbc	movslq	0x190(%r15), %rax
000000010044fbc3	movq	0x1c0(%r13), %rcx
000000010044fbca	leaq	CONFIG_BETTER_HW_COMPATIBILITY(%rax,%rax,4), %rax
000000010044fbce	shlq	$0x4, %rax
000000010044fbd2	movl	$0x2, 0x4c(%rcx,%rax)
000000010044fbda	jmp	0x10044fbe7
000000010044fbdc	movl	$0xffffffff, 0x190(%r15)        ## imm = 0xFFFFFFFF
000000010044fbe7	leaq	0x1abf61c(%rip), %rsi           ## literal pool for: "visible"
000000010044fbee	movl	$0x7, %edx
000000010044fbf3	movq	%r12, %rdi
000000010044fbf6	callq	__ZN8CXMLNode8getParamEPKcm     ## CXMLNode::getParam(char const*, unsigned long)
000000010044fbfb	movq	-0x38(%rbp), %r14
000000010044fbff	movq	%rax, %rbx
000000010044fc02	movzbl	CONFIG_BETTER_HW_COMPATIBILITY(%rax), %edx
000000010044fc05	movq	%rdx, %rax
000000010044fc08	shrq	%rax
000000010044fc0b	movb	$0x1, %cl
000000010044fc0d	andb	%dl, %cl
000000010044fc0f	movq	0x8(%rbx), %rdx
000000010044fc13	movq	%rdx, %rsi
000000010044fc16	cmoveq	%rax, %rsi
000000010044fc1a	cmpq	$0x3, %rsi
000000010044fc1e	jne	0x10044fc42
000000010044fc20	leaq	0x1aace63(%rip), %rsi           ## literal pool for: "yes"
000000010044fc27	movq	%rbx, %rdi
000000010044fc2a	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
000000010044fc2f	testb	%al, %al
000000010044fc31	jne	0x10044fc61
000000010044fc33	movzbl	CONFIG_BETTER_HW_COMPATIBILITY(%rbx), %eax
000000010044fc36	movq	0x8(%rbx), %rdx
000000010044fc3a	movl	%eax, %ecx
000000010044fc3c	andb	$0x1, %cl
000000010044fc3f	shrq	%rax
000000010044fc42	testb	%cl, %cl
000000010044fc44	cmovneq	%rdx, %rax
000000010044fc48	cmpq	$0x4, %rax
000000010044fc4c	jne	0x10044fc8d
000000010044fc4e	leaq	0x1ab00d8(%rip), %rsi           ## literal pool for: "true"
000000010044fc55	movq	%rbx, %rdi
000000010044fc58	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
000000010044fc5d	testb	%al, %al
000000010044fc5f	je	0x10044fc8d
000000010044fc61	movslq	0x190(%r15), %rax
000000010044fc68	testq	%rax, %rax
000000010044fc6b	js	0x10044fc8d
000000010044fc6d	leaq	_skinEngine(%rip), %rcx
000000010044fc74	movq	0x1c0(%rcx), %rcx
000000010044fc7b	leaq	CONFIG_BETTER_HW_COMPATIBILITY(%rax,%rax,4), %rax
000000010044fc7f	shlq	$0x4, %rax
000000010044fc83	movb	$0x1, 0x48(%rcx,%rax)
000000010044fc88	jmp	0x10044fd48
000000010044fc8d	movzbl	CONFIG_BETTER_HW_COMPATIBILITY(%rbx), %edx
000000010044fc90	movq	%rdx, %rax
000000010044fc93	shrq	%rax
000000010044fc96	movb	$0x1, %cl
000000010044fc98	andb	%dl, %cl
000000010044fc9a	movq	0x8(%rbx), %rdx
000000010044fc9e	movq	%rdx, %rsi
000000010044fca1	cmoveq	%rax, %rsi
000000010044fca5	cmpq	$0x2, %rsi
000000010044fca9	jne	0x10044fccd
000000010044fcab	leaq	0x1aacddc(%rip), %rsi           ## literal pool for: "no"
000000010044fcb2	movq	%rbx, %rdi
000000010044fcb5	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
000000010044fcba	testb	%al, %al
000000010044fcbc	jne	0x10044fcec
000000010044fcbe	movzbl	CONFIG_BETTER_HW_COMPATIBILITY(%rbx), %eax
000000010044fcc1	movq	0x8(%rbx), %rdx
000000010044fcc5	movl	%eax, %ecx
000000010044fcc7	andb	$0x1, %cl
000000010044fcca	shrq	%rax
000000010044fccd	testb	%cl, %cl
000000010044fccf	cmovneq	%rdx, %rax
000000010044fcd3	cmpq	$0x5, %rax
000000010044fcd7	jne	0x10044fd15
000000010044fcd9	leaq	0x1ab0052(%rip), %rsi           ## literal pool for: "false"
000000010044fce0	movq	%rbx, %rdi
000000010044fce3	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
000000010044fce8	testb	%al, %al
000000010044fcea	je	0x10044fd15
000000010044fcec	movslq	0x190(%r15), %rax
000000010044fcf3	testq	%rax, %rax
000000010044fcf6	js	0x10044fd15
000000010044fcf8	leaq	_skinEngine(%rip), %rcx
000000010044fcff	movq	0x1c0(%rcx), %rcx
000000010044fd06	leaq	CONFIG_BETTER_HW_COMPATIBILITY(%rax,%rax,4), %rax
000000010044fd0a	shlq	$0x4, %rax
000000010044fd0e	movb	$0x0, 0x48(%rcx,%rax)
000000010044fd13	jmp	0x10044fd48
000000010044fd15	movzbl	CONFIG_BETTER_HW_COMPATIBILITY(%rbx), %eax
000000010044fd18	movb	$0x1, %cl
000000010044fd1a	testb	%cl, %al
000000010044fd1c	je	0x10044fd24
000000010044fd1e	movq	0x8(%rbx), %rax
000000010044fd22	jmp	0x10044fd27
000000010044fd24	shrq	%rax
000000010044fd27	testq	%rax, %rax
000000010044fd2a	je	0x10044fd48
000000010044fd2c	cmpq	$0x0, 0x30(%r15)
000000010044fd31	jne	0x10044fd48
000000010044fd33	movl	0x44(%r15), %edx
000000010044fd37	movl	$CONFIG_ENCODERS, %edi
000000010044fd3c	movq	%rbx, %rsi
000000010044fd3f	callq	__ZN11CSkinEngine12createActionEbRKNSt3__112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEEi ## CSkinEngine::createAction(bool, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, int)
000000010044fd44	movq	%rax, 0x30(%r15)
000000010044fd48	leaq	0x1ad3811(%rip), %rsi           ## literal pool for: "applyfx"
000000010044fd4f	movl	$0x7, %edx
000000010044fd54	xorl	%ecx, %ecx
000000010044fd56	movq	%r12, %rdi
000000010044fd59	callq	__ZNK8CXMLNode14getBoolParamNSEPKcib ## CXMLNode::getBoolParamNS(char const*, int, bool) const
000000010044fd5e	movb	%al, 0x1b0(%r15)
000000010044fd65	movzbl	CONFIG_BETTER_HW_COMPATIBILITY(%r12), %eax
000000010044fd6a	movb	$0x1, %cl
000000010044fd6c	testb	%cl, %al
000000010044fd6e	je	0x10044fd77
000000010044fd70	movq	0x8(%r12), %rax
000000010044fd75	jmp	0x10044fd7a
000000010044fd77	shrq	%rax
000000010044fd7a	cmpq	$0x4, %rax
000000010044fd7e	jne	0x10044fd91
000000010044fd80	leaq	0x1ab2fcd(%rip), %rsi           ## literal pool for: "item"
000000010044fd87	movq	%r12, %rdi
000000010044fd8a	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
000000010044fd8f	jmp	0x10044fd93
000000010044fd91	xorl	%eax, %eax
000000010044fd93	movb	%al, 0x1b1(%r15)
000000010044fd9a	movq	0x1f4858f(%rip), %rax
000000010044fda1	cmpq	%rax, __ZN10CSkinPanel11parentPanelE(%rip) ## CSkinPanel::parentPanel
000000010044fda8	je	0x10044fdbf
000000010044fdaa	movq	-0x8(%rax), %rax
000000010044fdae	cmpb	$0x0, 0x1b1(%rax)
000000010044fdb5	je	0x10044fdbf
000000010044fdb7	movb	$0x1, 0x1b1(%r15)
000000010044fdbf	leaq	0x1ad37a2(%rip), %rsi           ## literal pool for: "childtooltip"
000000010044fdc6	movl	$0xc, %edx
000000010044fdcb	xorl	%ecx, %ecx
000000010044fdcd	movq	%r12, %rdi
000000010044fdd0	callq	__ZNK8CXMLNode14getBoolParamNSEPKcib ## CXMLNode::getBoolParamNS(char const*, int, bool) const
000000010044fdd5	movb	%al, 0x1b2(%r15)
000000010044fddc	movq	%r15, %rdi
000000010044fddf	movq	%r12, %rsi
000000010044fde2	movq	%r14, %rdx
000000010044fde5	movq	-0x30(%rbp), %rcx
000000010044fde9	callq	__ZN10CSkinPanel12loadChildrenEP8CXMLNodeP6CImageP11CSkinWindow ## CSkinPanel::loadChildren(CXMLNode*, CImage*, CSkinWindow*)
000000010044fdee	movq	0xd8(%r15), %rax
000000010044fdf5	subq	0xd0(%r15), %rax
000000010044fdfc	sarq	$0x3, %rax
000000010044fe00	cmpq	$0x10, %rax
000000010044fe04	jb	0x10044fe0e
000000010044fe06	movb	$0x1, 0xf0(%r15)
000000010044fe0e	addq	$0x18, %rsp
000000010044fe12	popq	%rbx
000000010044fe13	popq	%r12
000000010044fe15	popq	%r13
000000010044fe17	popq	%r14
000000010044fe19	popq	%r15
000000010044fe1b	popq	%rbp
000000010044fe1c	retq
000000010044fe1d	movzbl	CONFIG_BETTER_HW_COMPATIBILITY(%r14), %eax
000000010044fe21	movq	0x8(%r14), %rcx
000000010044fe25	movl	%eax, %edx
000000010044fe27	andb	$0x1, %dl
000000010044fe2a	shrq	%rax
000000010044fe2d	testb	%dl, %dl
000000010044fe2f	movq	%rcx, %rsi
000000010044fe32	cmoveq	%rax, %rsi
000000010044fe36	cmpq	$0x3, %rsi
000000010044fe3a	jne	0x10044fe82
000000010044fe3c	leaq	0x1ad370c(%rip), %rsi           ## literal pool for: "3fx"
000000010044fe43	movq	%r14, %rdi
000000010044fe46	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
000000010044fe4b	testb	%al, %al
000000010044fe4d	je	0x10044fe72
000000010044fe4f	movslq	0x190(%r15), %rax
000000010044fe56	movq	0x1c0(%r13), %rcx
000000010044fe5d	leaq	CONFIG_BETTER_HW_COMPATIBILITY(%rax,%rax,4), %rax
000000010044fe61	shlq	$0x4, %rax
000000010044fe65	movl	$0x3, 0x4c(%rcx,%rax)
000000010044fe6d	jmp	0x10044fbe7
000000010044fe72	movzbl	CONFIG_BETTER_HW_COMPATIBILITY(%r14), %eax
000000010044fe76	movq	0x8(%r14), %rcx
000000010044fe7a	movl	%eax, %edx
000000010044fe7c	andb	$0x1, %dl
000000010044fe7f	shrq	%rax
000000010044fe82	testb	%dl, %dl
000000010044fe84	movq	%rcx, %rsi
000000010044fe87	cmoveq	%rax, %rsi
000000010044fe8b	cmpq	$0x5, %rsi
000000010044fe8f	jne	0x10044fed7
000000010044fe91	leaq	0x1ad36bb(%rip), %rsi           ## literal pool for: "8pads"
000000010044fe98	movq	%r14, %rdi
000000010044fe9b	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
000000010044fea0	testb	%al, %al
000000010044fea2	je	0x10044fec7
000000010044fea4	movslq	0x190(%r15), %rax
000000010044feab	movq	0x1c0(%r13), %rcx
000000010044feb2	leaq	CONFIG_BETTER_HW_COMPATIBILITY(%rax,%rax,4), %rax
000000010044feb6	shlq	$0x4, %rax
000000010044feba	movl	$0x4, 0x4c(%rcx,%rax)
000000010044fec2	jmp	0x10044fbe7
000000010044fec7	movzbl	CONFIG_BETTER_HW_COMPATIBILITY(%r14), %eax
000000010044fecb	movq	0x8(%r14), %rcx
000000010044fecf	movl	%eax, %edx
000000010044fed1	andb	$0x1, %dl
000000010044fed4	shrq	%rax
000000010044fed7	testb	%dl, %dl
000000010044fed9	movq	%rcx, %rsi
000000010044fedc	cmoveq	%rax, %rsi
000000010044fee0	cmpq	$0x6, %rsi
000000010044fee4	jne	0x10044ff2c
000000010044fee6	leaq	0x1ad366c(%rip), %rsi           ## literal pool for: "16pads"
000000010044feed	movq	%r14, %rdi
000000010044fef0	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
000000010044fef5	testb	%al, %al
000000010044fef7	je	0x10044ff1c
000000010044fef9	movslq	0x190(%r15), %rax
000000010044ff00	movq	0x1c0(%r13), %rcx
000000010044ff07	leaq	CONFIG_BETTER_HW_COMPATIBILITY(%rax,%rax,4), %rax
000000010044ff0b	shlq	$0x4, %rax
000000010044ff0f	movl	$0x5, 0x4c(%rcx,%rax)
000000010044ff17	jmp	0x10044fbe7
000000010044ff1c	movzbl	CONFIG_BETTER_HW_COMPATIBILITY(%r14), %eax
000000010044ff20	movq	0x8(%r14), %rcx
000000010044ff24	movl	%eax, %edx
000000010044ff26	andb	$0x1, %dl
000000010044ff29	shrq	%rax
000000010044ff2c	testb	%dl, %dl
000000010044ff2e	cmovneq	%rcx, %rax
000000010044ff32	cmpq	$0x8, %rax
000000010044ff36	jne	0x10044fbe7
000000010044ff3c	leaq	0x1ab0205(%rip), %rsi           ## literal pool for: "timecode"
000000010044ff43	movq	%r14, %rdi
000000010044ff46	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
000000010044ff4b	testb	%al, %al
000000010044ff4d	je	0x10044fbe7
000000010044ff53	movslq	0x190(%r15), %rax
000000010044ff5a	movq	0x1c0(%r13), %rcx
000000010044ff61	leaq	CONFIG_BETTER_HW_COMPATIBILITY(%rax,%rax,4), %rax
000000010044ff65	shlq	$0x4, %rax
000000010044ff69	movl	$CONFIG_ENCODERS, 0x4c(%rcx,%rax)
000000010044ff71	jmp	0x10044fbe7
000000010044ff76	jmp	0x10044ff7c
000000010044ff78	jmp	0x10044ff7c
000000010044ff7a	jmp	0x10044ff7c
000000010044ff7c	movq	%rax, %rbx
000000010044ff7f	movq	%r15, %rdi
000000010044ff82	callq	__ZN14ISkinContainerD2Ev        ## ISkinContainer::~ISkinContainer()
000000010044ff87	movq	%rbx, %rdi
000000010044ff8a	callq	0x101b5d604                     ## symbol stub for: __Unwind_Resume
000000010044ff8f	ud2
000000010044ff91	nop
000000010044ff92	nop
000000010044ff93	nop
000000010044ff94	nop
000000010044ff95	nop
000000010044ff96	nop
000000010044ff97	nop
000000010044ff98	nop
000000010044ff99	nop
000000010044ff9a	nop
000000010044ff9b	nop
