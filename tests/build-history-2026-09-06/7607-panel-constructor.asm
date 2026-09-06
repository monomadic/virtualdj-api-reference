__ZN10CSkinPanelC2EP8CXMLNodeP6CImageP11CSkinWindow:
0000000100691cd8	pushq	%rbp
0000000100691cd9	movq	%rsp, %rbp
0000000100691cdc	pushq	%r15
0000000100691cde	pushq	%r14
0000000100691ce0	pushq	%r13
0000000100691ce2	pushq	%r12
0000000100691ce4	pushq	%rbx
0000000100691ce5	pushq	%rax
0000000100691ce6	movq	%rcx, %rbx
0000000100691ce9	movq	%rdx, %r15
0000000100691cec	movq	%rsi, %r12
0000000100691cef	movq	%rdi, %r14
0000000100691cf2	callq	__ZN14ISkinContainerC2Ev        ## ISkinContainer::ISkinContainer()
0000000100691cf7	leaq	0x538135a(%rip), %rax
0000000100691cfe	movq	%rax, VPX_ARCH_MIPS(%r14)
0000000100691d01	movabsq	$-0x100000000, %rax             ## imm = 0xFFFFFFFF00000000
0000000100691d0b	movq	%rax, 0x180(%r14)
0000000100691d12	movl	$0xffffffff, %eax               ## imm = 0xFFFFFFFF
0000000100691d17	movl	%eax, 0x188(%r14)
0000000100691d1e	movw	$VPX_ARCH_MIPS, 0x18c(%r14)
0000000100691d28	movb	$0x0, 0x18e(%r14)
0000000100691d30	xorps	%xmm0, %xmm0
0000000100691d33	movups	%xmm0, 0x198(%r14)
0000000100691d3b	movq	%rbx, -0x30(%rbp)
0000000100691d3f	movq	%rbx, 0x190(%r14)
0000000100691d46	movl	%eax, 0x38(%r14)
0000000100691d4a	movq	%r14, %rdi
0000000100691d4d	movq	%r12, %rsi
0000000100691d50	movq	%r15, %rdx
0000000100691d53	callq	__ZN11ISkinObject4loadEP8CXMLNodeP6CImage ## ISkinObject::load(CXMLNode*, CImage*)
0000000100691d58	leaq	0x51711ea(%rip), %rsi           ## literal pool for: "background"
0000000100691d5f	movl	$0xa, %edx
0000000100691d64	movq	%r12, %rdi
0000000100691d67	callq	__ZNK8CXMLNode8getChildENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEE ## CXMLNode::getChild(std::__1::basic_string_view<char, std::__1::char_traits<char>>) const
0000000100691d6c	movq	%rax, %rbx
0000000100691d6f	testq	%rax, %rax
0000000100691d72	jne	0x100691d8b
0000000100691d74	leaq	0x51712e4(%rip), %rsi           ## literal pool for: "down"
0000000100691d7b	movl	$FGData.num_y_points, %edx
0000000100691d80	movq	%r12, %rdi
0000000100691d83	callq	__ZNK8CXMLNode8getChildENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEE ## CXMLNode::getChild(std::__1::basic_string_view<char, std::__1::char_traits<char>>) const
0000000100691d88	movq	%rax, %rbx
0000000100691d8b	leaq	0x517013a(%rip), %rsi           ## literal pool for: "clipmask"
0000000100691d92	movl	$working_state.free_in_buffer, %edx
0000000100691d97	movq	%r12, %rdi
0000000100691d9a	callq	__ZNK8CXMLNode8getChildENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEE ## CXMLNode::getChild(std::__1::basic_string_view<char, std::__1::char_traits<char>>) const
0000000100691d9f	movq	%r14, %rdi
0000000100691da2	movq	%r15, %rsi
0000000100691da5	movq	%r12, %rdx
0000000100691da8	movq	%rbx, %rcx
0000000100691dab	movq	%rax, %r8
0000000100691dae	callq	__ZN11ISkinObject8getImageEP6CImageP8CXMLNodeS3_S3_ ## ISkinObject::getImage(CImage*, CXMLNode*, CXMLNode*, CXMLNode*)
0000000100691db3	movq	%rax, FGData.clip_to_restricted_range(%r14)
0000000100691dba	cmpb	$0x0, __ZN11ISkinObject11isVideoSkinE(%rip) ## ISkinObject::isVideoSkin
0000000100691dc1	je	0x100691dcc
0000000100691dc3	leaq	_emptyString(%rip), %rsi
0000000100691dca	jmp	0x100691e06
0000000100691dcc	leaq	0x517d2bd(%rip), %rbx           ## literal pool for: "name"
0000000100691dd3	movl	$FGData.num_y_points, %edx
0000000100691dd8	movq	%r12, %rdi
0000000100691ddb	movq	%rbx, %rsi
0000000100691dde	callq	__ZNK8CXMLNode8hasParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEE ## CXMLNode::hasParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>) const
0000000100691de3	leaq	0x516db77(%rip), %rsi           ## literal pool for: "id"
0000000100691dea	testb	%al, %al
0000000100691dec	cmovneq	%rbx, %rsi
0000000100691df0	movzbl	%al, %eax
0000000100691df3	leaq	VPX_ARCH_MIPS(%rax,%rax), %rdx
0000000100691df7	addq	$0x2, %rdx
0000000100691dfb	movq	%r12, %rdi
0000000100691dfe	callq	__ZNK8CXMLNode8getParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEE ## CXMLNode::getParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>) const
0000000100691e03	movq	%rax, %rsi
0000000100691e06	movzbl	VPX_ARCH_MIPS(%rsi), %eax
0000000100691e09	testb	$0x1, %al
0000000100691e0b	jne	0x100691e12
0000000100691e0d	shrq	%rax
0000000100691e10	jmp	0x100691e16
0000000100691e12	movq	0x8(%rsi), %rax
0000000100691e16	testq	%rax, %rax
0000000100691e19	je	0x100691f55
0000000100691e1f	leaq	_skinEngine(%rip), %r13
0000000100691e26	movq	%r13, %rdi
0000000100691e29	movl	$HAVE_SSE3, %edx
0000000100691e2e	callq	__ZN11CSkinEngine13getPanelIndexERKNSt3__112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEEb ## CSkinEngine::getPanelIndex(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, bool)
0000000100691e33	movl	%eax, 0x180(%r14)
0000000100691e3a	leaq	0x5173e40(%rip), %rsi           ## literal pool for: "group"
0000000100691e41	movl	$0x5, %edx
0000000100691e46	movq	%r12, %rdi
0000000100691e49	callq	__ZNK8CXMLNode8getParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEE ## CXMLNode::getParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>) const
0000000100691e4e	movslq	0x180(%r14), %rcx
0000000100691e55	movq	0x210(%r13), %rdx
0000000100691e5c	leaq	VPX_ARCH_MIPS(%rcx,%rcx,4), %rcx
0000000100691e60	shlq	$0x4, %rcx
0000000100691e64	leaq	VPX_ARCH_MIPS(%rdx,%rcx), %rdi
0000000100691e68	addq	$0x18, %rdi
0000000100691e6c	movq	%rax, %rsi
0000000100691e6f	callq	0x1052c2e50                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
0000000100691e74	leaq	0x519b0f8(%rip), %rsi           ## literal pool for: "available"
0000000100691e7b	movl	$0x9, %edx
0000000100691e80	movq	%r12, %rdi
0000000100691e83	movl	$HAVE_SSE3, %ecx
0000000100691e88	callq	__ZNK8CXMLNode12getBoolParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEEb ## CXMLNode::getBoolParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>, bool) const
0000000100691e8d	movslq	0x180(%r14), %rcx
0000000100691e94	movq	0x210(%r13), %rdx
0000000100691e9b	leaq	VPX_ARCH_MIPS(%rcx,%rcx,4), %rcx
0000000100691e9f	shlq	$0x4, %rcx
0000000100691ea3	movb	%al, 0x49(%rdx,%rcx)
0000000100691ea7	leaq	0x519b0cf(%rip), %rsi           ## literal pool for: "displayname"
0000000100691eae	movl	$0xb, %edx
0000000100691eb3	movq	%r12, %rdi
0000000100691eb6	callq	__ZNK8CXMLNode8getParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEE ## CXMLNode::getParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>) const
0000000100691ebb	movslq	0x180(%r14), %rcx
0000000100691ec2	movq	0x210(%r13), %rdx
0000000100691ec9	leaq	VPX_ARCH_MIPS(%rcx,%rcx,4), %rcx
0000000100691ecd	shlq	$0x4, %rcx
0000000100691ed1	leaq	VPX_ARCH_MIPS(%rdx,%rcx), %rdi
0000000100691ed5	addq	$0x30, %rdi
0000000100691ed9	movq	%rax, %rsi
0000000100691edc	callq	0x1052c2e50                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
0000000100691ee1	leaq	0x519b0a1(%rip), %rsi           ## literal pool for: "forceshow"
0000000100691ee8	movl	$0x9, %edx
0000000100691eed	movq	%r12, %rdi
0000000100691ef0	callq	__ZNK8CXMLNode8getParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEE ## CXMLNode::getParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>) const
0000000100691ef5	movq	%rax, %rbx
0000000100691ef8	movzbl	VPX_ARCH_MIPS(%rax), %ecx
0000000100691efb	movq	%rcx, %rax
0000000100691efe	shrq	%rax
0000000100691f01	andb	$0x1, %cl
0000000100691f04	movq	0x8(%rbx), %rdx
0000000100691f08	movq	%rdx, %rsi
0000000100691f0b	cmoveq	%rax, %rsi
0000000100691f0f	testq	%rsi, %rsi
0000000100691f12	je	0x100691f60
0000000100691f14	cmpq	$0x3, %rsi
0000000100691f18	jne	0x10069222a
0000000100691f1e	leaq	0x519b06e(%rip), %rsi           ## literal pool for: "1fx"
0000000100691f25	movq	%rbx, %rdi
0000000100691f28	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
0000000100691f2d	testb	%al, %al
0000000100691f2f	je	0x10069221b
0000000100691f35	movslq	0x180(%r14), %rax
0000000100691f3c	movq	0x210(%r13), %rcx
0000000100691f43	leaq	VPX_ARCH_MIPS(%rax,%rax,4), %rax
0000000100691f47	shlq	$0x4, %rax
0000000100691f4b	movl	$0x2, 0x4c(%rcx,%rax)
0000000100691f53	jmp	0x100691f60
0000000100691f55	movl	$0xffffffff, 0x180(%r14)        ## imm = 0xFFFFFFFF
0000000100691f60	leaq	0x517a13b(%rip), %rsi           ## literal pool for: "visible"
0000000100691f67	movl	$0x7, %edx
0000000100691f6c	movq	%r12, %rdi
0000000100691f6f	callq	__ZNK8CXMLNode8getParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEE ## CXMLNode::getParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>) const
0000000100691f74	movq	%rax, %rbx
0000000100691f77	movzbl	VPX_ARCH_MIPS(%rax), %ecx
0000000100691f7a	movq	%rcx, %rax
0000000100691f7d	shrq	%rax
0000000100691f80	andb	$0x1, %cl
0000000100691f83	movq	0x8(%rbx), %rdx
0000000100691f87	movq	%rdx, %rsi
0000000100691f8a	cmoveq	%rax, %rsi
0000000100691f8e	cmpq	$0x3, %rsi
0000000100691f92	jne	0x100691fb6
0000000100691f94	leaq	0x5165420(%rip), %rsi           ## literal pool for: "yes"
0000000100691f9b	movq	%rbx, %rdi
0000000100691f9e	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
0000000100691fa3	testb	%al, %al
0000000100691fa5	jne	0x100691fd5
0000000100691fa7	movzbl	VPX_ARCH_MIPS(%rbx), %eax
0000000100691faa	movq	0x8(%rbx), %rdx
0000000100691fae	movl	%eax, %ecx
0000000100691fb0	andb	$0x1, %cl
0000000100691fb3	shrq	%rax
0000000100691fb6	testb	%cl, %cl
0000000100691fb8	cmovneq	%rdx, %rax
0000000100691fbc	cmpq	$0x4, %rax
0000000100691fc0	jne	0x100692000
0000000100691fc2	leaq	0x516ec40(%rip), %rsi           ## literal pool for: "true"
0000000100691fc9	movq	%rbx, %rdi
0000000100691fcc	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
0000000100691fd1	testb	%al, %al
0000000100691fd3	je	0x100692000
0000000100691fd5	movl	0x180(%r14), %eax
0000000100691fdc	testl	%eax, %eax
0000000100691fde	js	0x100692000
0000000100691fe0	leaq	_skinEngine(%rip), %rcx
0000000100691fe7	movq	0x210(%rcx), %rcx
0000000100691fee	leaq	VPX_ARCH_MIPS(%rax,%rax,4), %rax
0000000100691ff2	shlq	$0x4, %rax
0000000100691ff6	movb	$0x1, 0x48(%rcx,%rax)
0000000100691ffb	jmp	0x1006920b7
0000000100692000	movzbl	VPX_ARCH_MIPS(%rbx), %ecx
0000000100692003	movq	%rcx, %rax
0000000100692006	shrq	%rax
0000000100692009	andb	$0x1, %cl
000000010069200c	movq	0x8(%rbx), %rdx
0000000100692010	movq	%rdx, %rsi
0000000100692013	cmoveq	%rax, %rsi
0000000100692017	cmpq	$0x2, %rsi
000000010069201b	jne	0x10069203f
000000010069201d	leaq	0x51653a3(%rip), %rsi           ## literal pool for: "no"
0000000100692024	movq	%rbx, %rdi
0000000100692027	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
000000010069202c	testb	%al, %al
000000010069202e	jne	0x10069205e
0000000100692030	movzbl	VPX_ARCH_MIPS(%rbx), %eax
0000000100692033	movq	0x8(%rbx), %rdx
0000000100692037	movl	%eax, %ecx
0000000100692039	andb	$0x1, %cl
000000010069203c	shrq	%rax
000000010069203f	testb	%cl, %cl
0000000100692041	cmovneq	%rdx, %rax
0000000100692045	cmpq	$0x5, %rax
0000000100692049	jne	0x100692086
000000010069204b	leaq	0x517dd2e(%rip), %rsi           ## literal pool for: "false"
0000000100692052	movq	%rbx, %rdi
0000000100692055	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
000000010069205a	testb	%al, %al
000000010069205c	je	0x100692086
000000010069205e	movl	0x180(%r14), %eax
0000000100692065	testl	%eax, %eax
0000000100692067	js	0x100692086
0000000100692069	leaq	_skinEngine(%rip), %rcx
0000000100692070	movq	0x210(%rcx), %rcx
0000000100692077	leaq	VPX_ARCH_MIPS(%rax,%rax,4), %rax
000000010069207b	shlq	$0x4, %rax
000000010069207f	movb	$0x0, 0x48(%rcx,%rax)
0000000100692084	jmp	0x1006920b7
0000000100692086	movzbl	VPX_ARCH_MIPS(%rbx), %eax
0000000100692089	testb	$0x1, %al
000000010069208b	je	0x100692093
000000010069208d	movq	0x8(%rbx), %rax
0000000100692091	jmp	0x100692096
0000000100692093	shrq	%rax
0000000100692096	testq	%rax, %rax
0000000100692099	je	0x1006920b7
000000010069209b	cmpq	$0x0, 0x30(%r14)
00000001006920a0	jne	0x1006920b7
00000001006920a2	movl	0x40(%r14), %edx
00000001006920a6	movl	$HAVE_SSE3, %edi
00000001006920ab	movq	%rbx, %rsi
00000001006920ae	callq	__ZN11CSkinEngine12createActionEbRKNSt3__112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEEi ## CSkinEngine::createAction(bool, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, int)
00000001006920b3	movq	%rax, 0x30(%r14)
00000001006920b7	leaq	0x519aeee(%rip), %rsi           ## literal pool for: "applyfx"
00000001006920be	movl	$0x7, %edx
00000001006920c3	movq	%r12, %rdi
00000001006920c6	xorl	%ecx, %ecx
00000001006920c8	callq	__ZNK8CXMLNode12getBoolParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEEb ## CXMLNode::getBoolParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>, bool) const
00000001006920cd	movb	%al, 0x18c(%r14)
00000001006920d4	movzbl	VPX_ARCH_MIPS(%r12), %eax
00000001006920d9	testb	$0x1, %al
00000001006920db	je	0x1006920e4
00000001006920dd	movq	0x8(%r12), %rax
00000001006920e2	jmp	0x1006920e7
00000001006920e4	shrq	%rax
00000001006920e7	cmpq	$0x4, %rax
00000001006920eb	jne	0x1006920fe
00000001006920ed	leaq	0x516f383(%rip), %rsi           ## literal pool for: "item"
00000001006920f4	movq	%r12, %rdi
00000001006920f7	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
00000001006920fc	jmp	0x100692100
00000001006920fe	xorl	%eax, %eax
0000000100692100	movb	%al, 0x18d(%r14)
0000000100692107	movq	0x54ff4ea(%rip), %rax
000000010069210e	cmpq	%rax, __ZN10CSkinPanel11parentPanelE(%rip) ## CSkinPanel::parentPanel
0000000100692115	je	0x10069212c
0000000100692117	movq	-0x8(%rax), %rax
000000010069211b	cmpb	$0x0, 0x18d(%rax)
0000000100692122	je	0x10069212c
0000000100692124	movb	$0x1, 0x18d(%r14)
000000010069212c	leaq	0x519ae81(%rip), %rsi           ## literal pool for: "childtooltip"
0000000100692133	movl	$0xc, %edx
0000000100692138	movq	%r12, %rdi
000000010069213b	xorl	%ecx, %ecx
000000010069213d	callq	__ZNK8CXMLNode12getBoolParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEEb ## CXMLNode::getBoolParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>, bool) const
0000000100692142	movb	%al, 0x18e(%r14)
0000000100692149	leaq	0x517821b(%rip), %rsi           ## literal pool for: "skin"
0000000100692150	movq	%r12, %rdi
0000000100692153	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
0000000100692158	testb	%al, %al
000000010069215a	jne	0x10069219c
000000010069215c	leaq	0x5187bf1(%rip), %rsi           ## literal pool for: "breakline1"
0000000100692163	movl	$0xa, %edx
0000000100692168	movq	%r12, %rdi
000000010069216b	movl	$0xffffffff, %ecx               ## imm = 0xFFFFFFFF
0000000100692170	callq	__ZNK8CXMLNode11getIntParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEEi ## CXMLNode::getIntParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>, int) const
0000000100692175	movl	%eax, 0x184(%r14)
000000010069217c	leaq	0x5187bdc(%rip), %rsi           ## literal pool for: "breakline2"
0000000100692183	movl	$0xa, %edx
0000000100692188	movq	%r12, %rdi
000000010069218b	movl	$0xffffffff, %ecx               ## imm = 0xFFFFFFFF
0000000100692190	callq	__ZNK8CXMLNode11getIntParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEEi ## CXMLNode::getIntParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>, int) const
0000000100692195	movl	%eax, 0x188(%r14)
000000010069219c	cmpl	$0x0, 0x184(%r14)
00000001006921a4	jns	0x1006921de
00000001006921a6	cmpl	$0x0, 0x188(%r14)
00000001006921ae	jns	0x1006921de
00000001006921b0	movq	0x54ff441(%rip), %rax
00000001006921b7	cmpq	%rax, __ZN10CSkinPanel11parentPanelE(%rip) ## CSkinPanel::parentPanel
00000001006921be	je	0x1006921de
00000001006921c0	movq	-0x8(%rax), %rax
00000001006921c4	movl	0x184(%rax), %ecx
00000001006921ca	movl	%ecx, 0x184(%r14)
00000001006921d1	movl	0x188(%rax), %eax
00000001006921d7	movl	%eax, 0x188(%r14)
00000001006921de	movq	%r14, %rdi
00000001006921e1	movq	%r12, %rsi
00000001006921e4	movq	%r15, %rdx
00000001006921e7	movq	-0x30(%rbp), %rcx
00000001006921eb	callq	__ZN10CSkinPanel12loadChildrenEP8CXMLNodeP6CImageP11CSkinWindow ## CSkinPanel::loadChildren(CXMLNode*, CImage*, CSkinWindow*)
00000001006921f0	movq	0xc8(%r14), %rax
00000001006921f7	subq	0xc0(%r14), %rax
00000001006921fe	cmpq	$0x79, %rax
0000000100692202	jb	0x10069220c
0000000100692204	movb	$0x1, 0xe0(%r14)
000000010069220c	addq	$0x8, %rsp
0000000100692210	popq	%rbx
0000000100692211	popq	%r12
0000000100692213	popq	%r13
0000000100692215	popq	%r14
0000000100692217	popq	%r15
0000000100692219	popq	%rbp
000000010069221a	retq
000000010069221b	movzbl	VPX_ARCH_MIPS(%rbx), %eax
000000010069221e	movq	0x8(%rbx), %rdx
0000000100692222	movl	%eax, %ecx
0000000100692224	andb	$0x1, %cl
0000000100692227	shrq	%rax
000000010069222a	testb	%cl, %cl
000000010069222c	movq	%rdx, %rsi
000000010069222f	cmoveq	%rax, %rsi
0000000100692233	cmpq	$0x3, %rsi
0000000100692237	jne	0x10069227e
0000000100692239	leaq	0x519ad57(%rip), %rsi           ## literal pool for: "3fx"
0000000100692240	movq	%rbx, %rdi
0000000100692243	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
0000000100692248	testb	%al, %al
000000010069224a	je	0x10069226f
000000010069224c	movslq	0x180(%r14), %rax
0000000100692253	movq	0x210(%r13), %rcx
000000010069225a	leaq	VPX_ARCH_MIPS(%rax,%rax,4), %rax
000000010069225e	shlq	$0x4, %rax
0000000100692262	movl	$0x3, 0x4c(%rcx,%rax)
000000010069226a	jmp	0x100691f60
000000010069226f	movzbl	VPX_ARCH_MIPS(%rbx), %eax
0000000100692272	movq	0x8(%rbx), %rdx
0000000100692276	movl	%eax, %ecx
0000000100692278	andb	$0x1, %cl
000000010069227b	shrq	%rax
000000010069227e	testb	%cl, %cl
0000000100692280	movq	%rdx, %rsi
0000000100692283	cmoveq	%rax, %rsi
0000000100692287	cmpq	$0x3, %rsi
000000010069228b	jne	0x1006922d2
000000010069228d	leaq	0x519ad07(%rip), %rsi           ## literal pool for: "6fx"
0000000100692294	movq	%rbx, %rdi
0000000100692297	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
000000010069229c	testb	%al, %al
000000010069229e	je	0x1006922c3
00000001006922a0	movslq	0x180(%r14), %rax
00000001006922a7	movq	0x210(%r13), %rcx
00000001006922ae	leaq	VPX_ARCH_MIPS(%rax,%rax,4), %rax
00000001006922b2	shlq	$0x4, %rax
00000001006922b6	movl	$FGData.num_y_points, 0x4c(%rcx,%rax)
00000001006922be	jmp	0x100691f60
00000001006922c3	movzbl	VPX_ARCH_MIPS(%rbx), %eax
00000001006922c6	movq	0x8(%rbx), %rdx
00000001006922ca	movl	%eax, %ecx
00000001006922cc	andb	$0x1, %cl
00000001006922cf	shrq	%rax
00000001006922d2	testb	%cl, %cl
00000001006922d4	cmovneq	%rdx, %rax
00000001006922d8	cmpq	$0x5, %rax
00000001006922dc	jne	0x100692314
00000001006922de	leaq	0x519acba(%rip), %rsi           ## literal pool for: "8pads"
00000001006922e5	movq	%rbx, %rdi
00000001006922e8	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
00000001006922ed	testb	%al, %al
00000001006922ef	je	0x100692314
00000001006922f1	movslq	0x180(%r14), %rax
00000001006922f8	movq	0x210(%r13), %rcx
00000001006922ff	leaq	VPX_ARCH_MIPS(%rax,%rax,4), %rax
0000000100692303	shlq	$0x4, %rax
0000000100692307	movl	$0x5, 0x4c(%rcx,%rax)
000000010069230f	jmp	0x100691f60
0000000100692314	leaq	0x519ac8a(%rip), %rsi           ## literal pool for: "16pads"
000000010069231b	movq	%rbx, %rdi
000000010069231e	callq	__Z13strIsEqualCILILm7EEbRKNSt3__112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEERAT__Kc ## bool strIsEqualCIL<7ul>(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const (&) [7ul])
0000000100692323	testb	%al, %al
0000000100692325	je	0x10069234a
0000000100692327	movslq	0x180(%r14), %rax
000000010069232e	movq	0x210(%r13), %rcx
0000000100692335	leaq	VPX_ARCH_MIPS(%rax,%rax,4), %rax
0000000100692339	shlq	$0x4, %rax
000000010069233d	movl	$0x6, 0x4c(%rcx,%rax)
0000000100692345	jmp	0x100691f60
000000010069234a	leaq	0x516f8b2(%rip), %rsi           ## literal pool for: "timecode"
0000000100692351	movq	%rbx, %rdi
0000000100692354	callq	__Z13strIsEqualCILILm9EEbRKNSt3__112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEERAT__Kc ## bool strIsEqualCIL<9ul>(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const (&) [9ul])
0000000100692359	testb	%al, %al
000000010069235b	je	0x100691f60
0000000100692361	movslq	0x180(%r14), %rax
0000000100692368	movq	0x210(%r13), %rcx
000000010069236f	leaq	VPX_ARCH_MIPS(%rax,%rax,4), %rax
0000000100692373	shlq	$0x4, %rax
0000000100692377	movl	$HAVE_SSE3, 0x4c(%rcx,%rax)
000000010069237f	jmp	0x100691f60
0000000100692384	jmp	0x10069238a
0000000100692386	jmp	0x10069238a
0000000100692388	jmp	0x10069238a
000000010069238a	movq	%rax, %rbx
000000010069238d	movq	%r14, %rdi
0000000100692390	callq	__ZN14ISkinContainerD2Ev        ## ISkinContainer::~ISkinContainer()
0000000100692395	movq	%rbx, %rdi
0000000100692398	callq	0x1052c2d5a                     ## symbol stub for: __Unwind_Resume
000000010069239d	nop
000000010069239e	nop
000000010069239f	nop
00000001006923a0	nop
00000001006923a1	nop
00000001006923a2	nop
00000001006923a3	nop
00000001006923a4	nop
00000001006923a5	nop
