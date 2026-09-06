__ZN10CSkinPanel12loadChildrenEP8CXMLNodeP6CImageP11CSkinWindow:
000000010044ff9c	pushq	%rbp
000000010044ff9d	movq	%rsp, %rbp
000000010044ffa0	pushq	%r15
000000010044ffa2	pushq	%r14
000000010044ffa4	pushq	%r13
000000010044ffa6	pushq	%r12
000000010044ffa8	pushq	%rbx
000000010044ffa9	subq	$0x48, %rsp
000000010044ffad	movq	%rcx, -0x50(%rbp)
000000010044ffb1	movq	%rdx, %r12
000000010044ffb4	movq	%rsi, %rbx
000000010044ffb7	movq	%rdi, %r13
000000010044ffba	movq	%rdi, -0x40(%rbp)
000000010044ffbe	movq	0x1f4836b(%rip), %rax
000000010044ffc5	cmpq	0x1f4836c(%rip), %rax
000000010044ffcc	jae	0x10044ffdf
000000010044ffce	movq	%r13, CONFIG_BETTER_HW_COMPATIBILITY(%rax)
000000010044ffd1	movl	$0x8, %eax
000000010044ffd6	addq	%rax, 0x1f48353(%rip)
000000010044ffdd	jmp	0x10044ffef
000000010044ffdf	leaq	__ZN10CSkinPanel11parentPanelE(%rip), %rdi ## CSkinPanel::parentPanel
000000010044ffe6	leaq	-0x40(%rbp), %rsi
000000010044ffea	callq	__ZNSt3__16vectorIP10CSkinPanelNS_9allocatorIS2_EEE21__push_back_slow_pathIS2_EEvOT_ ## void std::__1::vector<CSkinPanel*, std::__1::allocator<CSkinPanel*>>::__push_back_slow_path<CSkinPanel*>(CSkinPanel*&&)
000000010044ffef	leaq	0xd0(%r13), %rdi
000000010044fff6	movq	0xd8(%r13), %rax
000000010044fffd	subq	0xd0(%r13), %rax
0000000100450004	sarq	$0x3, %rax
0000000100450008	movq	0x38(%rbx), %rsi
000000010045000c	subq	0x30(%rbx), %rsi
0000000100450010	sarq	$0x3, %rsi
0000000100450014	addq	%rax, %rsi
0000000100450017	movq	%rdi, -0x48(%rbp)
000000010045001b	callq	__ZNSt3__16vectorIP11ISkinObjectNS_9allocatorIS2_EEE7reserveEm ## std::__1::vector<ISkinObject*, std::__1::allocator<ISkinObject*>>::reserve(unsigned long)
0000000100450020	movq	0x30(%rbx), %r15
0000000100450024	movq	0x38(%rbx), %r14
0000000100450028	cmpq	%r14, %r15
000000010045002b	je	0x10045053c
0000000100450031	leaq	0x1a0(%r13), %rax
0000000100450038	movq	%rax, -0x58(%rbp)
000000010045003c	xorl	%eax, %eax
000000010045003e	movq	%rax, -0x60(%rbp)
0000000100450042	movl	$0x180, %eax                    ## imm = 0x180
0000000100450047	addq	0x1dddcba(%rip), %rax
000000010045004e	movq	%rax, -0x68(%rbp)
0000000100450052	movq	CONFIG_BETTER_HW_COMPATIBILITY(%r15), %rdi
0000000100450055	movzbl	CONFIG_BETTER_HW_COMPATIBILITY(%rdi), %ecx
0000000100450058	movq	%rcx, %rax
000000010045005b	shrq	%rax
000000010045005e	movb	$0x1, %dl
0000000100450060	andb	%dl, %cl
0000000100450062	movq	0x8(%rdi), %rdx
0000000100450066	movq	%rdx, %rsi
0000000100450069	cmoveq	%rax, %rsi
000000010045006d	cmpq	$0x4, %rsi
0000000100450071	jne	0x100450095
0000000100450073	leaq	0x1ab0104(%rip), %rsi           ## literal pool for: "deck"
000000010045007a	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
000000010045007f	testb	%al, %al
0000000100450081	jne	0x1004500b4
0000000100450083	movq	CONFIG_BETTER_HW_COMPATIBILITY(%r15), %rdi
0000000100450086	movzbl	CONFIG_BETTER_HW_COMPATIBILITY(%rdi), %eax
0000000100450089	movq	0x8(%rdi), %rdx
000000010045008d	movl	%eax, %ecx
000000010045008f	andb	$0x1, %cl
0000000100450092	shrq	%rax
0000000100450095	testb	%cl, %cl
0000000100450097	movq	%rdx, %rsi
000000010045009a	cmoveq	%rax, %rsi
000000010045009e	cmpq	$0x7, %rsi
00000001004500a2	jne	0x100450115
00000001004500a4	leaq	0x1ad34ca(%rip), %rsi           ## literal pool for: "setdeck"
00000001004500ab	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
00000001004500b0	testb	%al, %al
00000001004500b2	je	0x100450103
00000001004500b4	movq	CONFIG_BETTER_HW_COMPATIBILITY(%r15), %rdi
00000001004500b7	movq	0x30(%rdi), %rax
00000001004500bb	cmpq	0x38(%rdi), %rax
00000001004500bf	je	0x1004503a9
00000001004500c5	movl	__ZN11ISkinObject10parentDeckE(%rip), %ebx ## ISkinObject::parentDeck
00000001004500cb	leaq	0x1ab00ac(%rip), %rsi           ## literal pool for: "deck"
00000001004500d2	callq	__ZNK8CXMLNode8getParamEPKc     ## CXMLNode::getParam(char const*) const
00000001004500d7	movq	%rax, %rdi
00000001004500da	leaq	__ZN11ISkinObject10parentDeckE(%rip), %rsi ## ISkinObject::parentDeck
00000001004500e1	callq	__ZN7IAction17getDeckFromStringERKNSt3__112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEERj ## IAction::getDeckFromString(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, unsigned int&)
00000001004500e6	movq	CONFIG_BETTER_HW_COMPATIBILITY(%r15), %rsi
00000001004500e9	movq	%r13, %rdi
00000001004500ec	movq	%r12, %rdx
00000001004500ef	movq	-0x50(%rbp), %rcx
00000001004500f3	callq	__ZN10CSkinPanel12loadChildrenEP8CXMLNodeP6CImageP11CSkinWindow ## CSkinPanel::loadChildren(CXMLNode*, CImage*, CSkinWindow*)
00000001004500f8	movl	%ebx, __ZN11ISkinObject10parentDeckE(%rip) ## ISkinObject::parentDeck
00000001004500fe	jmp	0x1004503a9
0000000100450103	movq	CONFIG_BETTER_HW_COMPATIBILITY(%r15), %rdi
0000000100450106	movzbl	CONFIG_BETTER_HW_COMPATIBILITY(%rdi), %eax
0000000100450109	movq	0x8(%rdi), %rdx
000000010045010d	movl	%eax, %ecx
000000010045010f	andb	$0x1, %cl
0000000100450112	shrq	%rax
0000000100450115	testb	%cl, %cl
0000000100450117	movq	%rdx, %rsi
000000010045011a	cmoveq	%rax, %rsi
000000010045011e	cmpq	$0x6, %rsi
0000000100450122	jne	0x10045019e
0000000100450124	leaq	0x1ab77eb(%rip), %rsi           ## literal pool for: "window"
000000010045012b	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
0000000100450130	testb	%al, %al
0000000100450132	je	0x10045018c
0000000100450134	movl	$0x348, %edi                    ## imm = 0x348
0000000100450139	callq	0x101b5d87a                     ## symbol stub for: __Znwm
000000010045013e	movq	%rax, %rbx
0000000100450141	movq	%rax, %rdi
0000000100450144	callq	__ZN11CSkinWindowC1Ev           ## CSkinWindow::CSkinWindow()
0000000100450149	movq	%rbx, -0x40(%rbp)
000000010045014d	movq	CONFIG_BETTER_HW_COMPATIBILITY(%r15), %rsi
0000000100450150	xorl	%ecx, %ecx
0000000100450152	movq	%rbx, %rdi
0000000100450155	movq	%r12, %rdx
0000000100450158	callq	__ZN11CSkinWindow4loadEP8CXMLNodeP6CImagePKc ## CSkinWindow::load(CXMLNode*, CImage*, char const*)
000000010045015d	leaq	_skinEngine(%rip), %rdx
0000000100450164	movq	0x188(%rdx), %rax
000000010045016b	cmpq	0x190(%rdx), %rax
0000000100450172	je	0x1004502c4
0000000100450178	movq	-0x40(%rbp), %rcx
000000010045017c	movq	%rcx, CONFIG_BETTER_HW_COMPATIBILITY(%rax)
000000010045017f	addq	$0x8, 0x188(%rdx)
0000000100450187	jmp	0x1004503a9
000000010045018c	movq	CONFIG_BETTER_HW_COMPATIBILITY(%r15), %rdi
000000010045018f	movzbl	CONFIG_BETTER_HW_COMPATIBILITY(%rdi), %eax
0000000100450192	movq	0x8(%rdi), %rdx
0000000100450196	movl	%eax, %ecx
0000000100450198	andb	$0x1, %cl
000000010045019b	shrq	%rax
000000010045019e	testb	%cl, %cl
00000001004501a0	cmovneq	%rdx, %rax
00000001004501a4	cmpq	$0x5, %rax
00000001004501a8	jne	0x1004501ee
00000001004501aa	leaq	0x1ab9556(%rip), %rsi           ## literal pool for: "group"
00000001004501b1	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
00000001004501b6	testb	%al, %al
00000001004501b8	je	0x1004501ee
00000001004501ba	movq	CONFIG_BETTER_HW_COMPATIBILITY(%r15), %rdi
00000001004501bd	movl	$0xa, %edx
00000001004501c2	leaq	0x1ab2b98(%rip), %rsi           ## literal pool for: "visibility"
00000001004501c9	callq	__ZNK8CXMLNode8hasParamEPKci    ## CXMLNode::hasParam(char const*, int) const
00000001004501ce	testb	%al, %al
00000001004501d0	jne	0x1004501ee
00000001004501d2	movq	CONFIG_BETTER_HW_COMPATIBILITY(%r15), %rdi
00000001004501d5	movl	$0xc, %edx
00000001004501da	leaq	0x1ab9457(%rip), %rsi           ## literal pool for: "novisibility"
00000001004501e1	callq	__ZNK8CXMLNode8hasParamEPKci    ## CXMLNode::hasParam(char const*, int) const
00000001004501e6	testb	%al, %al
00000001004501e8	je	0x1004502d6
00000001004501ee	movq	CONFIG_BETTER_HW_COMPATIBILITY(%r15), %rdi
00000001004501f1	movq	%r12, %rsi
00000001004501f4	movq	-0x50(%rbp), %rdx
00000001004501f8	callq	__ZN11ISkinObject16createSkinObjectEP8CXMLNodeP6CImageP11CSkinWindow ## ISkinObject::createSkinObject(CXMLNode*, CImage*, CSkinWindow*)
00000001004501fd	movq	%rax, -0x40(%rbp)
0000000100450201	testq	%rax, %rax
0000000100450204	je	0x1004503a9
000000010045020a	movl	0x40(%rax), %ecx
000000010045020d	cmpl	0x190(%r13), %ecx
0000000100450214	jne	0x10045021f
0000000100450216	movl	$0xffffffff, 0x40(%rax)         ## imm = 0xFFFFFFFF
000000010045021d	jmp	0x10045022d
000000010045021f	movb	$0x1, %al
0000000100450221	testl	%ecx, %ecx
0000000100450223	jns	0x100450229
0000000100450225	movq	-0x60(%rbp), %rax
0000000100450229	movq	%rax, -0x60(%rbp)
000000010045022d	movq	CONFIG_BETTER_HW_COMPATIBILITY(%r15), %rdi
0000000100450230	movzbl	CONFIG_BETTER_HW_COMPATIBILITY(%rdi), %eax
0000000100450233	movb	$0x1, %cl
0000000100450235	testb	%cl, %al
0000000100450237	je	0x10045023f
0000000100450239	movq	0x8(%rdi), %rax
000000010045023d	jmp	0x100450242
000000010045023f	shrq	%rax
0000000100450242	movl	$0x8, %ecx
0000000100450247	cmpq	%rcx, %rax
000000010045024a	jne	0x10045026e
000000010045024c	leaq	0x1ab94ba(%rip), %rsi           ## literal pool for: "grabzone"
0000000100450253	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
0000000100450258	testb	%al, %al
000000010045025a	je	0x10045026e
000000010045025c	movq	-0x48(%rbp), %rdi
0000000100450260	movq	CONFIG_BETTER_HW_COMPATIBILITY(%rdi), %rsi
0000000100450263	leaq	-0x40(%rbp), %rdx
0000000100450267	callq	__ZNSt3__16vectorIP11ISkinObjectNS_9allocatorIS2_EEE6insertENS_11__wrap_iterIPKS2_EERS7_ ## std::__1::vector<ISkinObject*, std::__1::allocator<ISkinObject*>>::insert(std::__1::__wrap_iter<ISkinObject* const*>, ISkinObject* const&)
000000010045026c	jmp	0x10045029c
000000010045026e	movq	0xd8(%r13), %rax
0000000100450275	cmpq	0xe0(%r13), %rax
000000010045027c	je	0x10045028f
000000010045027e	movq	-0x40(%rbp), %rcx
0000000100450282	movq	%rcx, CONFIG_BETTER_HW_COMPATIBILITY(%rax)
0000000100450285	addq	$0x8, 0xd8(%r13)
000000010045028d	jmp	0x10045029c
000000010045028f	movq	-0x48(%rbp), %rdi
0000000100450293	leaq	-0x40(%rbp), %rsi
0000000100450297	callq	__ZNSt3__16vectorIP11ISkinObjectNS_9allocatorIS2_EEE21__push_back_slow_pathIRKS2_EEvOT_ ## void std::__1::vector<ISkinObject*, std::__1::allocator<ISkinObject*>>::__push_back_slow_path<ISkinObject* const&>(ISkinObject* const&)
000000010045029c	movq	CONFIG_BETTER_HW_COMPATIBILITY(%r15), %rbx
000000010045029f	testq	%rbx, %rbx
00000001004502a2	je	0x1004503a9
00000001004502a8	movq	%rbx, %rdi
00000001004502ab	callq	__ZN8CXMLNodeD1Ev               ## CXMLNode::~CXMLNode()
00000001004502b0	movq	%rbx, %rdi
00000001004502b3	callq	0x101b5d868                     ## symbol stub for: __ZdlPv
00000001004502b8	movq	$CONFIG_BETTER_HW_COMPATIBILITY, CONFIG_BETTER_HW_COMPATIBILITY(%r15)
00000001004502bf	jmp	0x1004503a9
00000001004502c4	movq	-0x68(%rbp), %rdi
00000001004502c8	leaq	-0x40(%rbp), %rsi
00000001004502cc	callq	__ZNSt3__16vectorIP11CSkinWindowNS_9allocatorIS2_EEE21__push_back_slow_pathIRKS2_EEvOT_ ## void std::__1::vector<CSkinWindow*, std::__1::allocator<CSkinWindow*>>::__push_back_slow_path<CSkinWindow* const&>(CSkinWindow* const&)
00000001004502d1	jmp	0x1004503a9
00000001004502d6	movq	CONFIG_BETTER_HW_COMPATIBILITY(%r15), %rdi
00000001004502d9	callq	__ZN11ISkinObject14checkConditionEP8CXMLNode ## ISkinObject::checkCondition(CXMLNode*)
00000001004502de	testb	%al, %al
00000001004502e0	je	0x1004503a9
00000001004502e6	movq	-0x58(%rbp), %rcx
00000001004502ea	movq	CONFIG_BETTER_HW_COMPATIBILITY(%rcx), %rax
00000001004502ed	movq	0x8(%rcx), %rcx
00000001004502f1	movq	%rcx, -0x38(%rbp)
00000001004502f5	movq	%rax, -0x40(%rbp)
00000001004502f9	movq	CONFIG_BETTER_HW_COMPATIBILITY(%r15), %rdi
00000001004502fc	leaq	0x1ab1e4c(%rip), %rsi           ## literal pool for: "x"
0000000100450303	leaq	-0x30(%rbp), %rdx
0000000100450307	leaq	-0x29(%rbp), %rcx
000000010045030b	callq	__ZNK8CXMLNode14getSignedParamEPKcPiPb ## CXMLNode::getSignedParam(char const*, int*, bool*) const
0000000100450310	testb	%al, %al
0000000100450312	je	0x10045033a
0000000100450314	cvtsi2ssl	-0x30(%rbp), %xmm0
0000000100450319	movq	-0x58(%rbp), %rax
000000010045031d	addss	CONFIG_BETTER_HW_COMPATIBILITY(%rax), %xmm0
0000000100450321	movss	%xmm0, CONFIG_BETTER_HW_COMPATIBILITY(%rax)
0000000100450325	cmpb	$0x0, -0x29(%rbp)
0000000100450329	jne	0x10045033a
000000010045032b	subss	0x8(%r13), %xmm0
0000000100450331	movss	%xmm0, 0x1a0(%r13)
000000010045033a	movq	CONFIG_BETTER_HW_COMPATIBILITY(%r15), %rdi
000000010045033d	leaq	0x1ab0e58(%rip), %rsi           ## literal pool for: "y"
0000000100450344	leaq	-0x30(%rbp), %rdx
0000000100450348	leaq	-0x29(%rbp), %rcx
000000010045034c	callq	__ZNK8CXMLNode14getSignedParamEPKcPiPb ## CXMLNode::getSignedParam(char const*, int*, bool*) const
0000000100450351	testb	%al, %al
0000000100450353	je	0x100450384
0000000100450355	xorps	%xmm0, %xmm0
0000000100450358	cvtsi2ssl	-0x30(%rbp), %xmm0
000000010045035d	addss	0x1a4(%r13), %xmm0
0000000100450366	movss	%xmm0, 0x1a4(%r13)
000000010045036f	cmpb	$0x0, -0x29(%rbp)
0000000100450373	jne	0x100450384
0000000100450375	subss	0xc(%r13), %xmm0
000000010045037b	movss	%xmm0, 0x1a4(%r13)
0000000100450384	movq	CONFIG_BETTER_HW_COMPATIBILITY(%r15), %rsi
0000000100450387	movq	%r13, %rdi
000000010045038a	movq	%r12, %rdx
000000010045038d	movq	-0x50(%rbp), %rcx
0000000100450391	callq	__ZN10CSkinPanel12loadChildrenEP8CXMLNodeP6CImageP11CSkinWindow ## CSkinPanel::loadChildren(CXMLNode*, CImage*, CSkinWindow*)
0000000100450396	movq	-0x40(%rbp), %rax
000000010045039a	movq	-0x38(%rbp), %rcx
000000010045039e	movq	-0x58(%rbp), %rdx
00000001004503a2	movq	%rcx, 0x8(%rdx)
00000001004503a6	movq	%rax, CONFIG_BETTER_HW_COMPATIBILITY(%rdx)
00000001004503a9	addq	$0x8, %r15
00000001004503ad	cmpq	%r15, %r14
00000001004503b0	jne	0x100450052
00000001004503b6	addq	$-0x8, 0x1f47f72(%rip)
00000001004503be	testb	$0x1, -0x60(%rbp)
00000001004503c2	je	0x100450544
00000001004503c8	movq	0xd0(%r13), %r14
00000001004503cf	movq	0xd8(%r13), %rax
00000001004503d6	cmpq	%r14, %rax
00000001004503d9	je	0x100450544
00000001004503df	xorl	%r15d, %r15d
00000001004503e2	movq	CONFIG_BETTER_HW_COMPATIBILITY(%r14,%r15,8), %rcx
00000001004503e6	movl	0x40(%rcx), %r12d
00000001004503ea	testl	%r12d, %r12d
00000001004503ed	js	0x100450524
00000001004503f3	movq	-0x48(%rbp), %rdi
00000001004503f7	movl	%r12d, %esi
00000001004503fa	callq	__Z9findPanelRKNSt3__16vectorIP11ISkinObjectNS_9allocatorIS2_EEEEi ## findPanel(std::__1::vector<ISkinObject*, std::__1::allocator<ISkinObject*>> const&, int)
00000001004503ff	testq	%rax, %rax
0000000100450402	je	0x10045040c
0000000100450404	movq	%rax, %rbx
0000000100450407	jmp	0x1004504a6
000000010045040c	movl	$0x1b8, %edi                    ## imm = 0x1B8
0000000100450411	callq	0x101b5d87a                     ## symbol stub for: __Znwm
0000000100450416	movq	%rax, %rbx
0000000100450419	movq	%rax, %rdi
000000010045041c	callq	__ZN14ISkinContainerC2Ev        ## ISkinContainer::ISkinContainer()
0000000100450421	leaq	0x1e24938(%rip), %rax
0000000100450428	movq	%rax, CONFIG_BETTER_HW_COMPATIBILITY(%rbx)
000000010045042b	xorl	%eax, %eax
000000010045042d	movq	%rax, 0x1a8(%rbx)
0000000100450434	movq	%rax, 0x1a0(%rbx)
000000010045043b	movb	$0x0, 0x1b2(%rbx)
0000000100450442	movw	$CONFIG_BETTER_HW_COMPATIBILITY, 0x1b0(%rbx)
000000010045044b	movl	%r12d, 0x190(%rbx)
0000000100450452	movq	-0x50(%rbp), %rax
0000000100450456	movq	%rax, 0x198(%rbx)
000000010045045d	movabsq	$0x3f8000003f800000, %rax       ## imm = 0x3F8000003F800000
0000000100450467	movq	%rax, 0x10(%rbx)
000000010045046b	movl	$0xffffffff, 0x3c(%rbx)         ## imm = 0xFFFFFFFF
0000000100450472	movq	%rbx, -0x40(%rbp)
0000000100450476	movq	0xd8(%r13), %rax
000000010045047d	cmpq	0xe0(%r13), %rax
0000000100450484	movq	-0x48(%rbp), %r14
0000000100450488	jae	0x100450497
000000010045048a	movq	%rbx, CONFIG_BETTER_HW_COMPATIBILITY(%rax)
000000010045048d	addq	$0x8, 0xd8(%r13)
0000000100450495	jmp	0x1004504a3
0000000100450497	movq	%r14, %rdi
000000010045049a	leaq	-0x40(%rbp), %rsi
000000010045049e	callq	__ZNSt3__16vectorIP11ISkinObjectNS_9allocatorIS2_EEE21__push_back_slow_pathIS2_EEvOT_ ## void std::__1::vector<ISkinObject*, std::__1::allocator<ISkinObject*>>::__push_back_slow_path<ISkinObject*>(ISkinObject*&&)
00000001004504a3	movq	CONFIG_BETTER_HW_COMPATIBILITY(%r14), %r14
00000001004504a6	movq	CONFIG_BETTER_HW_COMPATIBILITY(%r14,%r15,8), %rax
00000001004504aa	movl	$0xffffffff, 0x40(%rax)         ## imm = 0xFFFFFFFF
00000001004504b1	movq	0xd8(%rbx), %rcx
00000001004504b8	cmpq	0xe0(%rbx), %rcx
00000001004504bf	je	0x1004504ce
00000001004504c1	movq	%rax, CONFIG_BETTER_HW_COMPATIBILITY(%rcx)
00000001004504c4	addq	$0x8, 0xd8(%rbx)
00000001004504cc	jmp	0x1004504e1
00000001004504ce	leaq	CONFIG_BETTER_HW_COMPATIBILITY(%r14,%r15,8), %rsi
00000001004504d2	addq	$0xd0, %rbx
00000001004504d9	movq	%rbx, %rdi
00000001004504dc	callq	__ZNSt3__16vectorIP11ISkinObjectNS_9allocatorIS2_EEE21__push_back_slow_pathIRKS2_EEvOT_ ## void std::__1::vector<ISkinObject*, std::__1::allocator<ISkinObject*>>::__push_back_slow_path<ISkinObject* const&>(ISkinObject* const&)
00000001004504e1	movq	0xd0(%r13), %r14
00000001004504e8	movq	0xd8(%r13), %rdx
00000001004504ef	leaq	CONFIG_BETTER_HW_COMPATIBILITY(%r14,%r15,8), %r12
00000001004504f3	leaq	0x8(%r14,%r15,8), %rsi
00000001004504f8	subq	%rsi, %rdx
00000001004504fb	movq	%rdx, %rbx
00000001004504fe	sarq	$0x3, %rbx
0000000100450502	testq	%rdx, %rdx
0000000100450505	je	0x100450516
0000000100450507	movq	%r12, %rdi
000000010045050a	callq	0x101b5df2e                     ## symbol stub for: _memmove
000000010045050f	movq	-0x48(%rbp), %rax
0000000100450513	movq	CONFIG_BETTER_HW_COMPATIBILITY(%rax), %r14
0000000100450516	leaq	CONFIG_BETTER_HW_COMPATIBILITY(%r12,%rbx,8), %rax
000000010045051a	movq	%rax, 0xd8(%r13)
0000000100450521	decq	%r15
0000000100450524	incq	%r15
0000000100450527	movq	%rax, %rcx
000000010045052a	subq	%r14, %rcx
000000010045052d	sarq	$0x3, %rcx
0000000100450531	cmpq	%rcx, %r15
0000000100450534	jb	0x1004503e2
000000010045053a	jmp	0x100450544
000000010045053c	addq	$-0x8, 0x1f47dec(%rip)
0000000100450544	addq	$0x48, %rsp
0000000100450548	popq	%rbx
0000000100450549	popq	%r12
000000010045054b	popq	%r13
000000010045054d	popq	%r14
000000010045054f	popq	%r15
0000000100450551	popq	%rbp
0000000100450552	retq
0000000100450553	jmp	0x100450555
0000000100450555	movq	%rax, %r14
0000000100450558	movq	%rbx, %rdi
000000010045055b	callq	0x101b5d868                     ## symbol stub for: __ZdlPv
0000000100450560	movq	%r14, %rdi
0000000100450563	callq	0x101b5d604                     ## symbol stub for: __Unwind_Resume
0000000100450568	ud2
