__ZN10CSkinPanel12loadChildrenEP8CXMLNodeP6CImageP11CSkinWindow:
0000000100810d70	pushq	%rbp
0000000100810d71	movq	%rsp, %rbp
0000000100810d74	pushq	%r15
0000000100810d76	pushq	%r14
0000000100810d78	pushq	%r13
0000000100810d7a	pushq	%r12
0000000100810d7c	pushq	%rbx
0000000100810d7d	subq	$0x58, %rsp
0000000100810d81	movq	%rcx, -0x58(%rbp)
0000000100810d85	movq	%rdx, %r12
0000000100810d88	movq	%rsi, %r13
0000000100810d8b	movq	%rdi, %r14
0000000100810d8e	leaq	-0x50(%rbp), %rsi
0000000100810d92	movq	%rdi, CONFIG_EMULATE_HARDWARE(%rsi)
0000000100810d95	leaq	__ZN10CSkinPanel11parentPanelE(%rip), %rdi ## CSkinPanel::parentPanel
0000000100810d9c	callq	__ZNSt3__16vectorIP10CSkinPanelNS_9allocatorIS2_EEE9push_backB8ne200100EOS2_ ## std::__1::vector<CSkinPanel*, std::__1::allocator<CSkinPanel*>>::push_back[abi:ne200100](CSkinPanel*&&)
0000000100810da1	leaq	rf.r(%r14), %rdi
0000000100810da8	movq	rf.n_tile_threads(%r14), %rax
0000000100810daf	subq	rf.r(%r14), %rax
0000000100810db6	sarq	$0x3, %rax
0000000100810dba	movq	0x38(%r13), %rsi
0000000100810dbe	subq	0x30(%r13), %rsi
0000000100810dc2	sarq	$0x3, %rsi
0000000100810dc6	addq	%rax, %rsi
0000000100810dc9	movq	%rdi, -0x38(%rbp)
0000000100810dcd	callq	__ZNSt3__16vectorIP11ISkinObjectNS_9allocatorIS2_EEE7reserveEm ## std::__1::vector<ISkinObject*, std::__1::allocator<ISkinObject*>>::reserve(unsigned long)
0000000100810dd2	movq	0x30(%r13), %rbx
0000000100810dd6	movq	0x38(%r13), %r15
0000000100810dda	cmpq	%r15, %rbx
0000000100810ddd	je	0x10081126b
0000000100810de3	leaq	0x198(%r14), %rax
0000000100810dea	movq	%rax, -0x60(%rbp)
0000000100810dee	movq	$CONFIG_EMULATE_HARDWARE, -0x68(%rbp)
0000000100810df6	movl	$0x238, %eax                    ## imm = 0x238
0000000100810dfb	addq	0x4fae8a6(%rip), %rax
0000000100810e02	movq	%rax, -0x78(%rbp)
0000000100810e06	movq	%r14, -0x70(%rbp)
0000000100810e0a	movq	CONFIG_EMULATE_HARDWARE(%rbx), %rdi
0000000100810e0d	movzbl	CONFIG_EMULATE_HARDWARE(%rdi), %ecx
0000000100810e10	movl	%ecx, %eax
0000000100810e12	shrl	%eax
0000000100810e14	andb	$0x1, %cl
0000000100810e17	movq	0x8(%rdi), %rdx
0000000100810e1b	movq	%rdx, %rsi
0000000100810e1e	cmoveq	%rax, %rsi
0000000100810e22	cmpq	$0x4, %rsi
0000000100810e26	jne	0x100810e49
0000000100810e28	leaq	0x4dcac80(%rip), %rsi           ## literal pool for: "deck"
0000000100810e2f	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
0000000100810e34	testb	%al, %al
0000000100810e36	jne	0x100810e68
0000000100810e38	movq	CONFIG_EMULATE_HARDWARE(%rbx), %rdi
0000000100810e3b	movzbl	CONFIG_EMULATE_HARDWARE(%rdi), %eax
0000000100810e3e	movq	0x8(%rdi), %rdx
0000000100810e42	movl	%eax, %ecx
0000000100810e44	andb	$0x1, %cl
0000000100810e47	shrl	%eax
0000000100810e49	testb	%cl, %cl
0000000100810e4b	movq	%rdx, %rsi
0000000100810e4e	cmoveq	%rax, %rsi
0000000100810e52	cmpq	$0x7, %rsi
0000000100810e56	jne	0x100810ed7
0000000100810e58	leaq	0x4e17741(%rip), %rsi           ## literal pool for: "setdeck"
0000000100810e5f	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
0000000100810e64	testb	%al, %al
0000000100810e66	je	0x100810ec6
0000000100810e68	movq	CONFIG_EMULATE_HARDWARE(%rbx), %r13
0000000100810e6b	movq	0x30(%r13), %rax
0000000100810e6f	cmpq	0x38(%r13), %rax
0000000100810e73	je	0x100811021
0000000100810e79	movl	__ZN11ISkinObject10parentDeckE(%rip), %r14d ## ISkinObject::parentDeck
0000000100810e80	movl	$FGData.num_y_points, %edx
0000000100810e85	movq	%r13, %rdi
0000000100810e88	leaq	0x4dcac20(%rip), %rsi           ## literal pool for: "deck"
0000000100810e8f	callq	__ZN8CXMLNode16getParamNonConstENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEE ## CXMLNode::getParamNonConst(std::__1::basic_string_view<char, std::__1::char_traits<char>>)
0000000100810e94	movq	%rax, %rdi
0000000100810e97	leaq	__ZN11ISkinObject10parentDeckE(%rip), %rsi ## ISkinObject::parentDeck
0000000100810e9e	callq	__ZN7IAction17getDeckFromStringERKNSt3__112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEERj ## IAction::getDeckFromString(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, unsigned int&)
0000000100810ea3	movq	CONFIG_EMULATE_HARDWARE(%rbx), %rsi
0000000100810ea6	movq	-0x70(%rbp), %rdi
0000000100810eaa	movq	%r12, %rdx
0000000100810ead	movq	-0x58(%rbp), %rcx
0000000100810eb1	callq	__ZN10CSkinPanel12loadChildrenEP8CXMLNodeP6CImageP11CSkinWindow ## CSkinPanel::loadChildren(CXMLNode*, CImage*, CSkinWindow*)
0000000100810eb6	movl	%r14d, __ZN11ISkinObject10parentDeckE(%rip) ## ISkinObject::parentDeck
0000000100810ebd	movq	-0x70(%rbp), %r14
0000000100810ec1	jmp	0x100811019
0000000100810ec6	movq	CONFIG_EMULATE_HARDWARE(%rbx), %rdi
0000000100810ec9	movzbl	CONFIG_EMULATE_HARDWARE(%rdi), %eax
0000000100810ecc	movq	0x8(%rdi), %rdx
0000000100810ed0	movl	%eax, %ecx
0000000100810ed2	andb	$0x1, %cl
0000000100810ed5	shrl	%eax
0000000100810ed7	testb	%cl, %cl
0000000100810ed9	movq	%rdx, %rsi
0000000100810edc	cmoveq	%rax, %rsi
0000000100810ee0	cmpq	$0x6, %rsi
0000000100810ee4	jne	0x100810f42
0000000100810ee6	leaq	0x4de10cd(%rip), %rsi           ## literal pool for: "window"
0000000100810eed	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
0000000100810ef2	testb	%al, %al
0000000100810ef4	je	0x100810f31
0000000100810ef6	movl	$0x690, %edi                    ## imm = 0x690
0000000100810efb	callq	0x104fe8750                     ## symbol stub for: __Znwm
0000000100810f00	movq	%rax, %r13
0000000100810f03	movq	%rax, %rdi
0000000100810f06	callq	__ZN11CSkinWindowC1Ev           ## CSkinWindow::CSkinWindow()
0000000100810f0b	movq	%r13, -0x50(%rbp)
0000000100810f0f	movq	CONFIG_EMULATE_HARDWARE(%rbx), %rsi
0000000100810f12	movq	%r13, %rdi
0000000100810f15	movq	%r12, %rdx
0000000100810f18	xorl	%ecx, %ecx
0000000100810f1a	callq	__ZN11CSkinWindow4loadEP8CXMLNodeP6CImagePKc ## CSkinWindow::load(CXMLNode*, CImage*, char const*)
0000000100810f1f	movq	-0x78(%rbp), %rdi
0000000100810f23	leaq	-0x50(%rbp), %rsi
0000000100810f27	callq	__ZNSt3__16vectorIP11CSkinWindowNS_9allocatorIS2_EEE9push_backB8ne200100EOS2_ ## std::__1::vector<CSkinWindow*, std::__1::allocator<CSkinWindow*>>::push_back[abi:ne200100](CSkinWindow*&&)
0000000100810f2c	jmp	0x100811019
0000000100810f31	movq	CONFIG_EMULATE_HARDWARE(%rbx), %rdi
0000000100810f34	movzbl	CONFIG_EMULATE_HARDWARE(%rdi), %eax
0000000100810f37	movq	0x8(%rdi), %rdx
0000000100810f3b	movl	%eax, %ecx
0000000100810f3d	andb	$0x1, %cl
0000000100810f40	shrl	%eax
0000000100810f42	testb	%cl, %cl
0000000100810f44	cmovneq	%rdx, %rax
0000000100810f48	cmpq	$0x5, %rax
0000000100810f4c	jne	0x100810f95
0000000100810f4e	leaq	0x4ddbefe(%rip), %rsi           ## literal pool for: "group"
0000000100810f55	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
0000000100810f5a	movq	CONFIG_EMULATE_HARDWARE(%rbx), %rdi
0000000100810f5d	testb	%al, %al
0000000100810f5f	je	0x100810f95
0000000100810f61	movl	$0xa, %edx
0000000100810f66	leaq	0x4ddb02d(%rip), %rsi           ## literal pool for: "visibility"
0000000100810f6d	callq	__ZNK8CXMLNode8hasParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEE ## CXMLNode::hasParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>) const
0000000100810f72	movq	CONFIG_EMULATE_HARDWARE(%rbx), %rdi
0000000100810f75	testb	%al, %al
0000000100810f77	jne	0x100810f95
0000000100810f79	movl	$rf.ih4, %edx
0000000100810f7e	leaq	0x4dee432(%rip), %rsi           ## literal pool for: "novisibility"
0000000100810f85	callq	__ZNK8CXMLNode8hasParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEE ## CXMLNode::hasParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>) const
0000000100810f8a	movq	CONFIG_EMULATE_HARDWARE(%rbx), %rdi
0000000100810f8d	testb	%al, %al
0000000100810f8f	je	0x10081104a
0000000100810f95	movq	%r12, %rsi
0000000100810f98	movq	-0x58(%rbp), %rdx
0000000100810f9c	callq	__ZN11ISkinObject16createSkinObjectEP8CXMLNodeP6CImageP11CSkinWindow ## ISkinObject::createSkinObject(CXMLNode*, CImage*, CSkinWindow*)
0000000100810fa1	movq	%rax, -0x50(%rbp)
0000000100810fa5	testq	%rax, %rax
0000000100810fa8	je	0x100811038
0000000100810fae	movl	0x3c(%rax), %ecx
0000000100810fb1	cmpl	0x180(%r14), %ecx
0000000100810fb8	jne	0x100810fc3
0000000100810fba	movl	$0xffffffff, 0x3c(%rax)         ## imm = 0xFFFFFFFF
0000000100810fc1	jmp	0x100810fd2
0000000100810fc3	testl	%ecx, %ecx
0000000100810fc5	setns	%al
0000000100810fc8	movq	-0x68(%rbp), %rcx
0000000100810fcc	orb	%al, %cl
0000000100810fce	movq	%rcx, -0x68(%rbp)
0000000100810fd2	movq	CONFIG_EMULATE_HARDWARE(%rbx), %rdi
0000000100810fd5	movzbl	CONFIG_EMULATE_HARDWARE(%rdi), %eax
0000000100810fd8	testb	$0x1, %al
0000000100810fda	je	0x100810fe2
0000000100810fdc	movq	0x8(%rdi), %rax
0000000100810fe0	jmp	0x100810fe4
0000000100810fe2	shrl	%eax
0000000100810fe4	cmpq	$0x8, %rax
0000000100810fe8	jne	0x10081100c
0000000100810fea	leaq	0x4dee487(%rip), %rsi           ## literal pool for: "grabzone"
0000000100810ff1	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
0000000100810ff6	testb	%al, %al
0000000100810ff8	je	0x10081100c
0000000100810ffa	movq	-0x38(%rbp), %rdi
0000000100810ffe	movq	CONFIG_EMULATE_HARDWARE(%rdi), %rsi
0000000100811001	leaq	-0x50(%rbp), %rdx
0000000100811005	callq	__ZNSt3__16vectorIP11ISkinObjectNS_9allocatorIS2_EEE6insertENS_11__wrap_iterIPKS2_EERS7_ ## std::__1::vector<ISkinObject*, std::__1::allocator<ISkinObject*>>::insert(std::__1::__wrap_iter<ISkinObject* const*>, ISkinObject* const&)
000000010081100a	jmp	0x100811019
000000010081100c	movq	-0x38(%rbp), %rdi
0000000100811010	leaq	-0x50(%rbp), %rsi
0000000100811014	callq	__ZNSt3__16vectorIP11ISkinObjectNS_9allocatorIS2_EEE9push_backB8ne200100ERKS2_ ## std::__1::vector<ISkinObject*, std::__1::allocator<ISkinObject*>>::push_back[abi:ne200100](ISkinObject* const&)
0000000100811019	movq	CONFIG_EMULATE_HARDWARE(%rbx), %r13
000000010081101c	testq	%r13, %r13
000000010081101f	je	0x100811038
0000000100811021	movq	%r13, %rdi
0000000100811024	callq	__ZN8CXMLNodeD1Ev               ## CXMLNode::~CXMLNode()
0000000100811029	movq	%r13, %rdi
000000010081102c	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
0000000100811031	movq	$CONFIG_EMULATE_HARDWARE, CONFIG_EMULATE_HARDWARE(%rbx)
0000000100811038	addq	$0x8, %rbx
000000010081103c	cmpq	%r15, %rbx
000000010081103f	jne	0x100810e0a
0000000100811045	jmp	0x100811118
000000010081104a	callq	__ZN11ISkinObject14checkConditionEP8CXMLNode ## ISkinObject::checkCondition(CXMLNode*)
000000010081104f	testb	%al, %al
0000000100811051	je	0x100811038
0000000100811053	movq	-0x60(%rbp), %rax
0000000100811057	movups	CONFIG_EMULATE_HARDWARE(%rax), %xmm0
000000010081105a	movaps	%xmm0, -0x50(%rbp)
000000010081105e	movq	CONFIG_EMULATE_HARDWARE(%rbx), %rdi
0000000100811061	movl	$CONFIG_VP9, %edx
0000000100811066	leaq	0x4dcce6f(%rip), %rsi           ## literal pool for: "x"
000000010081106d	leaq	-0x30(%rbp), %rcx
0000000100811071	leaq	-0x29(%rbp), %r8
0000000100811075	callq	__ZNK8CXMLNode14getSignedParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEEPiPb ## CXMLNode::getSignedParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>, int*, bool*) const
000000010081107a	testb	%al, %al
000000010081107c	je	0x1008110a7
000000010081107e	xorps	%xmm0, %xmm0
0000000100811081	cvtsi2ssl	-0x30(%rbp), %xmm0
0000000100811086	movq	-0x60(%rbp), %rax
000000010081108a	addss	CONFIG_EMULATE_HARDWARE(%rax), %xmm0
000000010081108e	movss	%xmm0, CONFIG_EMULATE_HARDWARE(%rax)
0000000100811092	cmpb	$0x0, -0x29(%rbp)
0000000100811096	jne	0x1008110a7
0000000100811098	subss	0x8(%r14), %xmm0
000000010081109e	movss	%xmm0, 0x198(%r14)
00000001008110a7	movq	CONFIG_EMULATE_HARDWARE(%rbx), %rdi
00000001008110aa	movl	$CONFIG_VP9, %edx
00000001008110af	leaq	0x4dcc5e4(%rip), %rsi           ## literal pool for: "y"
00000001008110b6	leaq	-0x30(%rbp), %rcx
00000001008110ba	leaq	-0x29(%rbp), %r8
00000001008110be	callq	__ZNK8CXMLNode14getSignedParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEEPiPb ## CXMLNode::getSignedParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>, int*, bool*) const
00000001008110c3	testb	%al, %al
00000001008110c5	je	0x1008110f6
00000001008110c7	xorps	%xmm0, %xmm0
00000001008110ca	cvtsi2ssl	-0x30(%rbp), %xmm0
00000001008110cf	addss	0x19c(%r14), %xmm0
00000001008110d8	movss	%xmm0, 0x19c(%r14)
00000001008110e1	cmpb	$0x0, -0x29(%rbp)
00000001008110e5	jne	0x1008110f6
00000001008110e7	subss	0xc(%r14), %xmm0
00000001008110ed	movss	%xmm0, 0x19c(%r14)
00000001008110f6	movq	CONFIG_EMULATE_HARDWARE(%rbx), %rsi
00000001008110f9	movq	%r14, %rdi
00000001008110fc	movq	%r12, %rdx
00000001008110ff	movq	-0x58(%rbp), %rcx
0000000100811103	callq	__ZN10CSkinPanel12loadChildrenEP8CXMLNodeP6CImageP11CSkinWindow ## CSkinPanel::loadChildren(CXMLNode*, CImage*, CSkinWindow*)
0000000100811108	movaps	-0x50(%rbp), %xmm0
000000010081110c	movq	-0x60(%rbp), %rax
0000000100811110	movups	%xmm0, CONFIG_EMULATE_HARDWARE(%rax)
0000000100811113	jmp	0x100811019
0000000100811118	addq	$-0x8, 0x5214028(%rip)
0000000100811120	testb	$0x1, -0x68(%rbp)
0000000100811124	je	0x100811273
000000010081112a	movq	rf.r(%r14), %r15
0000000100811131	movq	rf.n_tile_threads(%r14), %r13
0000000100811138	cmpq	%r15, %r13
000000010081113b	je	0x100811273
0000000100811141	xorl	%ebx, %ebx
0000000100811143	movq	CONFIG_EMULATE_HARDWARE(%r15,%rbx,8), %r14
0000000100811147	movl	0x3c(%r14), %r12d
000000010081114b	testl	%r12d, %r12d
000000010081114e	js	0x100811253
0000000100811154	movq	-0x38(%rbp), %rdi
0000000100811158	movl	%r12d, %esi
000000010081115b	callq	__Z9findPanelRKNSt3__16vectorIP11ISkinObjectNS_9allocatorIS2_EEEEi ## findPanel(std::__1::vector<ISkinObject*, std::__1::allocator<ISkinObject*>> const&, int)
0000000100811160	movq	%rax, %r13
0000000100811163	testq	%rax, %rax
0000000100811166	jne	0x1008111f7
000000010081116c	movl	$0x1a8, %edi                    ## imm = 0x1A8
0000000100811171	callq	0x104fe8750                     ## symbol stub for: __Znwm
0000000100811176	movq	%rax, %r13
0000000100811179	movq	%rax, %rdi
000000010081117c	callq	__ZN14ISkinContainerC1Ev        ## ISkinContainer::ISkinContainer()
0000000100811181	leaq	0x5029748(%rip), %rax
0000000100811188	movq	%rax, (%r13)
000000010081118c	movq	$-0x1, 0x184(%r13)
0000000100811197	movw	$CONFIG_EMULATE_HARDWARE, 0x18c(%r13)
00000001008111a1	movb	$0x0, 0x18e(%r13)
00000001008111a9	xorps	%xmm0, %xmm0
00000001008111ac	movups	%xmm0, 0x198(%r13)
00000001008111b4	movl	%r12d, 0x180(%r13)
00000001008111bb	movq	-0x58(%rbp), %rax
00000001008111bf	movq	%rax, 0x190(%r13)
00000001008111c6	movsd	0x497c292(%rip), %xmm0
00000001008111ce	movsd	%xmm0, 0x10(%r13)
00000001008111d4	movl	$0xffffffff, 0x38(%r13)         ## imm = 0xFFFFFFFF
00000001008111dc	movq	%r13, -0x50(%rbp)
00000001008111e0	movq	-0x38(%rbp), %r14
00000001008111e4	movq	%r14, %rdi
00000001008111e7	leaq	-0x50(%rbp), %rsi
00000001008111eb	callq	__ZNSt3__16vectorIP11ISkinObjectNS_9allocatorIS2_EEE9push_backB8ne200100ERKS2_ ## std::__1::vector<ISkinObject*, std::__1::allocator<ISkinObject*>>::push_back[abi:ne200100](ISkinObject* const&)
00000001008111f0	movq	CONFIG_EMULATE_HARDWARE(%r14), %r15
00000001008111f3	movq	CONFIG_EMULATE_HARDWARE(%r15,%rbx,8), %r14
00000001008111f7	leaq	CONFIG_EMULATE_HARDWARE(%r15,%rbx,8), %rsi
00000001008111fb	movl	$0xffffffff, 0x3c(%r14)         ## imm = 0xFFFFFFFF
0000000100811203	addq	$rf.r, %r13
000000010081120a	movq	%r13, %rdi
000000010081120d	callq	__ZNSt3__16vectorIP11ISkinObjectNS_9allocatorIS2_EEE9push_backB8ne200100ERKS2_ ## std::__1::vector<ISkinObject*, std::__1::allocator<ISkinObject*>>::push_back[abi:ne200100](ISkinObject* const&)
0000000100811212	movq	-0x70(%rbp), %r14
0000000100811216	movq	rf.r(%r14), %r15
000000010081121d	movq	rf.n_tile_threads(%r14), %r12
0000000100811224	leaq	CONFIG_EMULATE_HARDWARE(%r15,%rbx,8), %r13
0000000100811228	leaq	CONFIG_EMULATE_HARDWARE(%r15,%rbx,8), %rsi
000000010081122c	addq	$0x8, %rsi
0000000100811230	subq	%rsi, %r12
0000000100811233	je	0x100811247
0000000100811235	movq	%r13, %rdi
0000000100811238	movq	%r12, %rdx
000000010081123b	callq	0x104fe8ed6                     ## symbol stub for: _memmove
0000000100811240	movq	-0x38(%rbp), %rax
0000000100811244	movq	CONFIG_EMULATE_HARDWARE(%rax), %r15
0000000100811247	addq	%r12, %r13
000000010081124a	movq	%r13, rf.n_tile_threads(%r14)
0000000100811251	jmp	0x100811256
0000000100811253	incq	%rbx
0000000100811256	movq	%r13, %rax
0000000100811259	subq	%r15, %rax
000000010081125c	sarq	$0x3, %rax
0000000100811260	cmpq	%rax, %rbx
0000000100811263	jb	0x100811143
0000000100811269	jmp	0x100811273
000000010081126b	addq	$-0x8, 0x5213ed5(%rip)
0000000100811273	addq	$0x58, %rsp
0000000100811277	popq	%rbx
0000000100811278	popq	%r12
000000010081127a	popq	%r13
000000010081127c	popq	%r14
000000010081127e	popq	%r15
0000000100811280	popq	%rbp
0000000100811281	retq
0000000100811282	jmp	0x100811284
0000000100811284	movq	%rax, %rbx
0000000100811287	movq	%r13, %rdi
000000010081128a	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
000000010081128f	movq	%rbx, %rdi
0000000100811292	callq	0x104fe8456                     ## symbol stub for: __Unwind_Resume
0000000100811297	nop
