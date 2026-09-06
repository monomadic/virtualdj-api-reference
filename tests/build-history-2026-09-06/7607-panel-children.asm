__ZN10CSkinPanel12loadChildrenEP8CXMLNodeP6CImageP11CSkinWindow:
00000001006923a6	pushq	%rbp
00000001006923a7	movq	%rsp, %rbp
00000001006923aa	pushq	%r15
00000001006923ac	pushq	%r14
00000001006923ae	pushq	%r13
00000001006923b0	pushq	%r12
00000001006923b2	pushq	%rbx
00000001006923b3	subq	$0x78, %rsp
00000001006923b7	movq	%rcx, -0x58(%rbp)
00000001006923bb	movq	%rdx, -0x48(%rbp)
00000001006923bf	movq	%rsi, %r12
00000001006923c2	movabsq	$0x1fffffffffffffff, %r15       ## imm = 0x1FFFFFFFFFFFFFFF
00000001006923cc	movq	0x54ff225(%rip), %rbx
00000001006923d3	movq	0x54ff226(%rip), %rax
00000001006923da	cmpq	%rax, %rbx
00000001006923dd	movq	%rdi, -0x50(%rbp)
00000001006923e1	jae	0x1006923f9
00000001006923e3	movq	%rdi, %r13
00000001006923e6	movq	%rdi, VPX_ARCH_MIPS(%rbx)
00000001006923e9	addq	$0x8, %rbx
00000001006923ed	movq	%rbx, 0x54ff204(%rip)
00000001006923f4	jmp	0x1006924b0
00000001006923f9	movq	__ZN10CSkinPanel11parentPanelE(%rip), %rcx ## CSkinPanel::parentPanel
0000000100692400	subq	%rcx, %rbx
0000000100692403	sarq	$0x3, %rbx
0000000100692407	leaq	0x1(%rbx), %rdx
000000010069240b	cmpq	%r15, %rdx
000000010069240e	ja	0x100692d68
0000000100692414	subq	%rcx, %rax
0000000100692417	movq	%rax, %rsi
000000010069241a	sarq	$0x2, %rsi
000000010069241e	cmpq	%rdx, %rsi
0000000100692421	cmovbeq	%rdx, %rsi
0000000100692425	movabsq	$0x7ffffffffffffff8, %rcx       ## imm = 0x7FFFFFFFFFFFFFF8
000000010069242f	cmpq	%rcx, %rax
0000000100692432	cmovaeq	%r15, %rsi
0000000100692436	testq	%rsi, %rsi
0000000100692439	je	0x100692449
000000010069243b	leaq	0x54ff1be(%rip), %rdi
0000000100692442	callq	__ZNSt3__119__allocate_at_leastB6v15006INS_9allocatorIP10CSkinPanelEEEENS_19__allocation_resultINS_16allocator_traitsIT_E7pointerEEERS7_m ## std::__1::__allocation_result<std::__1::allocator_traits<std::__1::allocator<CSkinPanel*>>::pointer> std::__1::__allocate_at_least[abi:v15006]<std::__1::allocator<CSkinPanel*>>(std::__1::allocator<CSkinPanel*>&, unsigned long)
0000000100692447	jmp	0x10069244d
0000000100692449	xorl	%eax, %eax
000000010069244b	xorl	%edx, %edx
000000010069244d	leaq	VPX_ARCH_MIPS(%rax,%rbx,8), %r14
0000000100692451	leaq	VPX_ARCH_MIPS(%rax,%rdx,8), %r15
0000000100692455	movq	-0x50(%rbp), %r13
0000000100692459	movq	%r13, VPX_ARCH_MIPS(%r14)
000000010069245c	leaq	VPX_ARCH_MIPS(%rax,%rbx,8), %rbx
0000000100692460	addq	$0x8, %rbx
0000000100692464	movq	0x54ff18d(%rip), %rdx
000000010069246b	movq	__ZN10CSkinPanel11parentPanelE(%rip), %rsi ## CSkinPanel::parentPanel
0000000100692472	subq	%rsi, %rdx
0000000100692475	subq	%rdx, %r14
0000000100692478	movq	%r14, %rdi
000000010069247b	callq	0x1052c3756                     ## symbol stub for: _memmove
0000000100692480	movq	__ZN10CSkinPanel11parentPanelE(%rip), %rdi ## CSkinPanel::parentPanel
0000000100692487	movq	%r14, __ZN10CSkinPanel11parentPanelE(%rip) ## CSkinPanel::parentPanel
000000010069248e	movq	%rbx, 0x54ff163(%rip)
0000000100692495	movq	%r15, 0x54ff164(%rip)
000000010069249c	testq	%rdi, %rdi
000000010069249f	movabsq	$0x1fffffffffffffff, %r15       ## imm = 0x1FFFFFFFFFFFFFFF
00000001006924a9	je	0x1006924b0
00000001006924ab	callq	0x1052c300c                     ## symbol stub for: __ZdlPv
00000001006924b0	leaq	0xc0(%r13), %rdi
00000001006924b7	movq	0xc8(%r13), %rax
00000001006924be	subq	0xc0(%r13), %rax
00000001006924c5	sarq	$0x3, %rax
00000001006924c9	movq	0x38(%r12), %rsi
00000001006924ce	subq	0x30(%r12), %rsi
00000001006924d3	sarq	$0x3, %rsi
00000001006924d7	addq	%rax, %rsi
00000001006924da	movq	%rdi, -0x38(%rbp)
00000001006924de	callq	__ZNSt3__16vectorIP11ISkinObjectNS_9allocatorIS2_EEE7reserveEm ## std::__1::vector<ISkinObject*, std::__1::allocator<ISkinObject*>>::reserve(unsigned long)
00000001006924e3	movq	0x30(%r12), %r14
00000001006924e8	movq	0x38(%r12), %r12
00000001006924ed	cmpq	%r12, %r14
00000001006924f0	je	0x100692d28
00000001006924f6	leaq	0x198(%r13), %rax
00000001006924fd	movq	%rax, -0x60(%rbp)
0000000100692501	leaq	0xd0(%r13), %rax
0000000100692508	movq	%rax, -0x88(%rbp)
000000010069250f	xorl	%eax, %eax
0000000100692511	movq	%rax, -0x68(%rbp)
0000000100692515	leaq	_skinEngine(%rip), %rbx
000000010069251c	movl	$0x1e0, %eax                    ## imm = 0x1E0
0000000100692521	addq	0x531aac0(%rip), %rax
0000000100692528	movq	%rax, -0x90(%rbp)
000000010069252f	movq	%r12, -0x70(%rbp)
0000000100692533	movq	VPX_ARCH_MIPS(%r14), %rdi
0000000100692536	movzbl	VPX_ARCH_MIPS(%rdi), %ecx
0000000100692539	movq	%rcx, %rax
000000010069253c	shrq	%rax
000000010069253f	andb	$0x1, %cl
0000000100692542	movq	0x8(%rdi), %rdx
0000000100692546	movq	%rdx, %rsi
0000000100692549	cmoveq	%rax, %rsi
000000010069254d	cmpq	$0x4, %rsi
0000000100692551	jne	0x100692575
0000000100692553	leaq	0x51641e1(%rip), %rsi           ## literal pool for: "deck"
000000010069255a	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
000000010069255f	testb	%al, %al
0000000100692561	jne	0x100692598
0000000100692563	movq	VPX_ARCH_MIPS(%r14), %rdi
0000000100692566	movzbl	VPX_ARCH_MIPS(%rdi), %eax
0000000100692569	movq	0x8(%rdi), %rdx
000000010069256d	movl	%eax, %ecx
000000010069256f	andb	$0x1, %cl
0000000100692572	shrq	%rax
0000000100692575	testb	%cl, %cl
0000000100692577	movq	%rdx, %rsi
000000010069257a	cmoveq	%rax, %rsi
000000010069257e	cmpq	$0x7, %rsi
0000000100692582	jne	0x100692608
0000000100692588	leaq	0x519aa32(%rip), %rsi           ## literal pool for: "setdeck"
000000010069258f	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
0000000100692594	testb	%al, %al
0000000100692596	je	0x1006925f6
0000000100692598	movq	VPX_ARCH_MIPS(%r14), %rbx
000000010069259b	movq	0x30(%rbx), %rax
000000010069259f	cmpq	0x38(%rbx), %rax
00000001006925a3	je	0x10069296e
00000001006925a9	movl	__ZN11ISkinObject10parentDeckE(%rip), %r12d ## ISkinObject::parentDeck
00000001006925b0	movl	$FGData.num_y_points, %edx
00000001006925b5	movq	%rbx, %rdi
00000001006925b8	leaq	0x516417c(%rip), %rsi           ## literal pool for: "deck"
00000001006925bf	callq	__ZNK8CXMLNode8getParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEE ## CXMLNode::getParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>) const
00000001006925c4	movq	%rax, %rdi
00000001006925c7	leaq	__ZN11ISkinObject10parentDeckE(%rip), %rsi ## ISkinObject::parentDeck
00000001006925ce	callq	__ZN7IAction17getDeckFromStringERKNSt3__112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEERj ## IAction::getDeckFromString(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, unsigned int&)
00000001006925d3	movq	VPX_ARCH_MIPS(%r14), %rsi
00000001006925d6	movq	%r13, %rdi
00000001006925d9	movq	-0x48(%rbp), %rdx
00000001006925dd	movq	-0x58(%rbp), %rcx
00000001006925e1	callq	__ZN10CSkinPanel12loadChildrenEP8CXMLNodeP6CImageP11CSkinWindow ## CSkinPanel::loadChildren(CXMLNode*, CImage*, CSkinWindow*)
00000001006925e6	movl	%r12d, __ZN11ISkinObject10parentDeckE(%rip) ## ISkinObject::parentDeck
00000001006925ed	movq	-0x70(%rbp), %r12
00000001006925f1	jmp	0x100692966
00000001006925f6	movq	VPX_ARCH_MIPS(%r14), %rdi
00000001006925f9	movzbl	VPX_ARCH_MIPS(%rdi), %eax
00000001006925fc	movq	0x8(%rdi), %rdx
0000000100692600	movl	%eax, %ecx
0000000100692602	andb	$0x1, %cl
0000000100692605	shrq	%rax
0000000100692608	testb	%cl, %cl
000000010069260a	movq	%rdx, %rsi
000000010069260d	cmoveq	%rax, %rsi
0000000100692611	cmpq	$0x6, %rsi
0000000100692615	jne	0x100692686
0000000100692617	leaq	0x5177d5c(%rip), %rsi           ## literal pool for: "window"
000000010069261e	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
0000000100692623	testb	%al, %al
0000000100692625	je	0x100692674
0000000100692627	movl	$0x468, %edi                    ## imm = 0x468
000000010069262c	callq	0x1052c301e                     ## symbol stub for: __Znwm
0000000100692631	movq	%rax, %r12
0000000100692634	movq	%rax, %rdi
0000000100692637	callq	__ZN11CSkinWindowC1Ev           ## CSkinWindow::CSkinWindow()
000000010069263c	movq	VPX_ARCH_MIPS(%r14), %rsi
000000010069263f	movq	%r12, %rdi
0000000100692642	movq	-0x48(%rbp), %rdx
0000000100692646	xorl	%ecx, %ecx
0000000100692648	callq	__ZN11CSkinWindow4loadEP8CXMLNodeP6CImagePKc ## CSkinWindow::load(CXMLNode*, CImage*, char const*)
000000010069264d	movq	0x1d8(%rbx), %rax
0000000100692654	cmpq	0x1e0(%rbx), %rax
000000010069265b	je	0x1006927d6
0000000100692661	movq	%r12, VPX_ARCH_MIPS(%rax)
0000000100692664	addq	$0x8, %rax
0000000100692668	movq	%rax, 0x1d8(%rbx)
000000010069266f	jmp	0x100692a10
0000000100692674	movq	VPX_ARCH_MIPS(%r14), %rdi
0000000100692677	movzbl	VPX_ARCH_MIPS(%rdi), %eax
000000010069267a	movq	0x8(%rdi), %rdx
000000010069267e	movl	%eax, %ecx
0000000100692680	andb	$0x1, %cl
0000000100692683	shrq	%rax
0000000100692686	testb	%cl, %cl
0000000100692688	cmovneq	%rdx, %rax
000000010069268c	cmpq	$0x5, %rax
0000000100692690	jne	0x1006926d6
0000000100692692	leaq	0x51735e8(%rip), %rsi           ## literal pool for: "group"
0000000100692699	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
000000010069269e	testb	%al, %al
00000001006926a0	je	0x1006926d6
00000001006926a2	movq	VPX_ARCH_MIPS(%r14), %rdi
00000001006926a5	movl	$0xa, %edx
00000001006926aa	leaq	0x5172759(%rip), %rsi           ## literal pool for: "visibility"
00000001006926b1	callq	__ZNK8CXMLNode8hasParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEE ## CXMLNode::hasParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>) const
00000001006926b6	testb	%al, %al
00000001006926b8	jne	0x1006926d6
00000001006926ba	movq	VPX_ARCH_MIPS(%r14), %rdi
00000001006926bd	movl	$0xc, %edx
00000001006926c2	leaq	0x51800be(%rip), %rsi           ## literal pool for: "novisibility"
00000001006926c9	callq	__ZNK8CXMLNode8hasParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEE ## CXMLNode::hasParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>) const
00000001006926ce	testb	%al, %al
00000001006926d0	je	0x10069282a
00000001006926d6	movq	VPX_ARCH_MIPS(%r14), %rdi
00000001006926d9	movq	-0x48(%rbp), %rsi
00000001006926dd	movq	-0x58(%rbp), %rdx
00000001006926e1	callq	__ZN11ISkinObject16createSkinObjectEP8CXMLNodeP6CImageP11CSkinWindow ## ISkinObject::createSkinObject(CXMLNode*, CImage*, CSkinWindow*)
00000001006926e6	movq	%rax, -0x80(%rbp)
00000001006926ea	testq	%rax, %rax
00000001006926ed	je	0x10069298c
00000001006926f3	movl	0x3c(%rax), %ecx
00000001006926f6	cmpl	0x180(%r13), %ecx
00000001006926fd	jne	0x100692708
00000001006926ff	movl	$0xffffffff, 0x3c(%rax)         ## imm = 0xFFFFFFFF
0000000100692706	jmp	0x10069271d
0000000100692708	testl	%ecx, %ecx
000000010069270a	movq	-0x68(%rbp), %rax
000000010069270e	movzbl	%al, %eax
0000000100692711	movl	$HAVE_SSE3, %ecx
0000000100692716	cmovnsl	%ecx, %eax
0000000100692719	movq	%rax, -0x68(%rbp)
000000010069271d	movq	VPX_ARCH_MIPS(%r14), %rdi
0000000100692720	movzbl	VPX_ARCH_MIPS(%rdi), %eax
0000000100692723	testb	$0x1, %al
0000000100692725	je	0x10069272d
0000000100692727	movq	0x8(%rdi), %rax
000000010069272b	jmp	0x100692730
000000010069272d	shrq	%rax
0000000100692730	cmpq	$0x8, %rax
0000000100692734	jne	0x10069275b
0000000100692736	leaq	0x5180112(%rip), %rsi           ## literal pool for: "grabzone"
000000010069273d	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
0000000100692742	testb	%al, %al
0000000100692744	je	0x10069275b
0000000100692746	movq	-0x38(%rbp), %rdi
000000010069274a	movq	VPX_ARCH_MIPS(%rdi), %rsi
000000010069274d	leaq	-0x80(%rbp), %rdx
0000000100692751	callq	__ZNSt3__16vectorIP11ISkinObjectNS_9allocatorIS2_EEE6insertENS_11__wrap_iterIPKS2_EERS7_ ## std::__1::vector<ISkinObject*, std::__1::allocator<ISkinObject*>>::insert(std::__1::__wrap_iter<ISkinObject* const*>, ISkinObject* const&)
0000000100692756	jmp	0x100692966
000000010069275b	movq	0xc8(%r13), %rax
0000000100692762	cmpq	0xd0(%r13), %rax
0000000100692769	je	0x100692782
000000010069276b	movq	-0x80(%rbp), %rcx
000000010069276f	movq	%rcx, VPX_ARCH_MIPS(%rax)
0000000100692772	addq	$0x8, %rax
0000000100692776	movq	%rax, 0xc8(%r13)
000000010069277d	jmp	0x100692966
0000000100692782	movq	-0x38(%rbp), %rdi
0000000100692786	subq	VPX_ARCH_MIPS(%rdi), %rax
0000000100692789	movq	%rax, %rbx
000000010069278c	sarq	$0x3, %rbx
0000000100692790	leaq	0x1(%rbx), %rcx
0000000100692794	cmpq	%r15, %rcx
0000000100692797	ja	0x100692d49
000000010069279d	movq	%rax, %rsi
00000001006927a0	sarq	$0x2, %rsi
00000001006927a4	cmpq	%rcx, %rsi
00000001006927a7	cmovbeq	%rcx, %rsi
00000001006927ab	movabsq	$0x7ffffffffffffff8, %rcx       ## imm = 0x7FFFFFFFFFFFFFF8
00000001006927b5	cmpq	%rcx, %rax
00000001006927b8	cmovaeq	%r15, %rsi
00000001006927bc	testq	%rsi, %rsi
00000001006927bf	je	0x1006928f3
00000001006927c5	movq	-0x88(%rbp), %rdi
00000001006927cc	callq	__ZNSt3__119__allocate_at_leastB6v15006INS_9allocatorIP11ISkinObjectEEEENS_19__allocation_resultINS_16allocator_traitsIT_E7pointerEEERS7_m ## std::__1::__allocation_result<std::__1::allocator_traits<std::__1::allocator<ISkinObject*>>::pointer> std::__1::__allocate_at_least[abi:v15006]<std::__1::allocator<ISkinObject*>>(std::__1::allocator<ISkinObject*>&, unsigned long)
00000001006927d1	jmp	0x1006928f7
00000001006927d6	subq	0x1d0(%rbx), %rax
00000001006927dd	movq	%rax, %r13
00000001006927e0	sarq	$0x3, %r13
00000001006927e4	leaq	0x1(%r13), %rcx
00000001006927e8	cmpq	%r15, %rcx
00000001006927eb	ja	0x100692d4e
00000001006927f1	movq	%rax, %rsi
00000001006927f4	sarq	$0x2, %rsi
00000001006927f8	cmpq	%rcx, %rsi
00000001006927fb	cmovbeq	%rcx, %rsi
00000001006927ff	movabsq	$0x7ffffffffffffff8, %rcx       ## imm = 0x7FFFFFFFFFFFFFF8
0000000100692809	cmpq	%rcx, %rax
000000010069280c	cmovaeq	%r15, %rsi
0000000100692810	testq	%rsi, %rsi
0000000100692813	je	0x10069299e
0000000100692819	movq	-0x90(%rbp), %rdi
0000000100692820	callq	__ZNSt3__119__allocate_at_leastB6v15006INS_9allocatorIP11CSkinWindowEEEENS_19__allocation_resultINS_16allocator_traitsIT_E7pointerEEERS7_m ## std::__1::__allocation_result<std::__1::allocator_traits<std::__1::allocator<CSkinWindow*>>::pointer> std::__1::__allocate_at_least[abi:v15006]<std::__1::allocator<CSkinWindow*>>(std::__1::allocator<CSkinWindow*>&, unsigned long)
0000000100692825	jmp	0x1006929a2
000000010069282a	movq	VPX_ARCH_MIPS(%r14), %rdi
000000010069282d	callq	__ZN11ISkinObject14checkConditionEP8CXMLNode ## ISkinObject::checkCondition(CXMLNode*)
0000000100692832	testb	%al, %al
0000000100692834	je	0x10069298c
000000010069283a	movq	-0x60(%rbp), %rax
000000010069283e	movups	VPX_ARCH_MIPS(%rax), %xmm0
0000000100692841	movaps	%xmm0, -0x80(%rbp)
0000000100692845	movq	VPX_ARCH_MIPS(%r14), %rdi
0000000100692848	leaq	0x5166021(%rip), %rsi           ## literal pool for: "x"
000000010069284f	leaq	-0x3c(%rbp), %rdx
0000000100692853	leaq	-0x29(%rbp), %rcx
0000000100692857	callq	__ZNK8CXMLNode14getSignedParamEPKcPiPb ## CXMLNode::getSignedParam(char const*, int*, bool*) const
000000010069285c	testb	%al, %al
000000010069285e	je	0x100692889
0000000100692860	xorps	%xmm0, %xmm0
0000000100692863	cvtsi2ssl	-0x3c(%rbp), %xmm0
0000000100692868	movq	-0x60(%rbp), %rax
000000010069286c	addss	VPX_ARCH_MIPS(%rax), %xmm0
0000000100692870	movss	%xmm0, VPX_ARCH_MIPS(%rax)
0000000100692874	cmpb	$0x0, -0x29(%rbp)
0000000100692878	jne	0x100692889
000000010069287a	subss	0x8(%r13), %xmm0
0000000100692880	movss	%xmm0, 0x198(%r13)
0000000100692889	movq	VPX_ARCH_MIPS(%r14), %rdi
000000010069288c	leaq	0x5165fdf(%rip), %rsi           ## literal pool for: "y"
0000000100692893	leaq	-0x3c(%rbp), %rdx
0000000100692897	leaq	-0x29(%rbp), %rcx
000000010069289b	callq	__ZNK8CXMLNode14getSignedParamEPKcPiPb ## CXMLNode::getSignedParam(char const*, int*, bool*) const
00000001006928a0	testb	%al, %al
00000001006928a2	je	0x1006928d3
00000001006928a4	xorps	%xmm0, %xmm0
00000001006928a7	cvtsi2ssl	-0x3c(%rbp), %xmm0
00000001006928ac	addss	0x19c(%r13), %xmm0
00000001006928b5	movss	%xmm0, 0x19c(%r13)
00000001006928be	cmpb	$0x0, -0x29(%rbp)
00000001006928c2	jne	0x1006928d3
00000001006928c4	subss	0xc(%r13), %xmm0
00000001006928ca	movss	%xmm0, 0x19c(%r13)
00000001006928d3	movq	VPX_ARCH_MIPS(%r14), %rsi
00000001006928d6	movq	%r13, %rdi
00000001006928d9	movq	-0x48(%rbp), %rdx
00000001006928dd	movq	-0x58(%rbp), %rcx
00000001006928e1	callq	__ZN10CSkinPanel12loadChildrenEP8CXMLNodeP6CImageP11CSkinWindow ## CSkinPanel::loadChildren(CXMLNode*, CImage*, CSkinWindow*)
00000001006928e6	movaps	-0x80(%rbp), %xmm0
00000001006928ea	movq	-0x60(%rbp), %rax
00000001006928ee	movups	%xmm0, VPX_ARCH_MIPS(%rax)
00000001006928f1	jmp	0x100692966
00000001006928f3	xorl	%eax, %eax
00000001006928f5	xorl	%edx, %edx
00000001006928f7	leaq	VPX_ARCH_MIPS(%rax,%rbx,8), %r12
00000001006928fb	leaq	VPX_ARCH_MIPS(%rax,%rdx,8), %r13
00000001006928ff	movq	-0x80(%rbp), %rcx
0000000100692903	movq	%rcx, VPX_ARCH_MIPS(%r12)
0000000100692907	leaq	VPX_ARCH_MIPS(%rax,%rbx,8), %r15
000000010069290b	addq	$0x8, %r15
000000010069290f	movq	-0x50(%rbp), %rbx
0000000100692913	movq	0xc0(%rbx), %rsi
000000010069291a	movq	0xc8(%rbx), %rdx
0000000100692921	subq	%rsi, %rdx
0000000100692924	subq	%rdx, %r12
0000000100692927	movq	%r12, %rdi
000000010069292a	callq	0x1052c3756                     ## symbol stub for: _memmove
000000010069292f	movq	0xc0(%rbx), %rdi
0000000100692936	movq	%r12, 0xc0(%rbx)
000000010069293d	movq	%r15, 0xc8(%rbx)
0000000100692944	movq	%r13, 0xd0(%rbx)
000000010069294b	movq	%rbx, %r13
000000010069294e	testq	%rdi, %rdi
0000000100692951	movabsq	$0x1fffffffffffffff, %r15       ## imm = 0x1FFFFFFFFFFFFFFF
000000010069295b	movq	-0x70(%rbp), %r12
000000010069295f	je	0x100692966
0000000100692961	callq	0x1052c300c                     ## symbol stub for: __ZdlPv
0000000100692966	movq	VPX_ARCH_MIPS(%r14), %rbx
0000000100692969	testq	%rbx, %rbx
000000010069296c	je	0x100692985
000000010069296e	movq	%rbx, %rdi
0000000100692971	callq	__ZN8CXMLNodeD1Ev               ## CXMLNode::~CXMLNode()
0000000100692976	movq	%rbx, %rdi
0000000100692979	callq	0x1052c300c                     ## symbol stub for: __ZdlPv
000000010069297e	movq	$VPX_ARCH_MIPS, VPX_ARCH_MIPS(%r14)
0000000100692985	leaq	_skinEngine(%rip), %rbx
000000010069298c	addq	$0x8, %r14
0000000100692990	cmpq	%r12, %r14
0000000100692993	jne	0x100692533
0000000100692999	jmp	0x100692a25
000000010069299e	xorl	%eax, %eax
00000001006929a0	xorl	%edx, %edx
00000001006929a2	leaq	VPX_ARCH_MIPS(%rax,%r13,8), %rbx
00000001006929a6	leaq	VPX_ARCH_MIPS(%rax,%rdx,8), %rcx
00000001006929aa	movq	%rcx, -0x98(%rbp)
00000001006929b1	movq	%r12, VPX_ARCH_MIPS(%rbx)
00000001006929b4	leaq	VPX_ARCH_MIPS(%rax,%r13,8), %r12
00000001006929b8	addq	$0x8, %r12
00000001006929bc	leaq	_skinEngine(%rip), %r13
00000001006929c3	movq	0x1d0(%r13), %rsi
00000001006929ca	movq	0x1d8(%r13), %rdx
00000001006929d1	subq	%rsi, %rdx
00000001006929d4	subq	%rdx, %rbx
00000001006929d7	movq	%rbx, %rdi
00000001006929da	callq	0x1052c3756                     ## symbol stub for: _memmove
00000001006929df	movq	0x1d0(%r13), %rdi
00000001006929e6	movq	%rbx, 0x1d0(%r13)
00000001006929ed	movq	%r12, 0x1d8(%r13)
00000001006929f4	movq	-0x98(%rbp), %rax
00000001006929fb	movq	%rax, 0x1e0(%r13)
0000000100692a02	testq	%rdi, %rdi
0000000100692a05	movq	-0x50(%rbp), %r13
0000000100692a09	je	0x100692a10
0000000100692a0b	callq	0x1052c300c                     ## symbol stub for: __ZdlPv
0000000100692a10	movq	VPX_ARCH_MIPS(%r14), %rbx
0000000100692a13	testq	%rbx, %rbx
0000000100692a16	movq	-0x70(%rbp), %r12
0000000100692a1a	jne	0x10069296e
0000000100692a20	jmp	0x100692985
0000000100692a25	addq	$-0x8, 0x54febcb(%rip)
0000000100692a2d	testb	$0x1, -0x68(%rbp)
0000000100692a31	je	0x100692d30
0000000100692a37	movq	0xc0(%r13), %rax
0000000100692a3e	movq	0xc8(%r13), %r12
0000000100692a45	cmpq	%rax, %r12
0000000100692a48	je	0x100692d30
0000000100692a4e	xorl	%r14d, %r14d
0000000100692a51	movq	VPX_ARCH_MIPS(%rax,%r14,8), %rcx
0000000100692a55	movl	0x3c(%rcx), %ebx
0000000100692a58	testl	%ebx, %ebx
0000000100692a5a	js	0x100692d10
0000000100692a60	movq	-0x38(%rbp), %r15
0000000100692a64	movq	%r15, %rdi
0000000100692a67	movl	%ebx, %esi
0000000100692a69	callq	__Z9findPanelRKNSt3__16vectorIP11ISkinObjectNS_9allocatorIS2_EEEEi ## findPanel(std::__1::vector<ISkinObject*, std::__1::allocator<ISkinObject*>> const&, int)
0000000100692a6e	movq	%rax, %r12
0000000100692a71	testq	%rax, %rax
0000000100692a74	jne	0x100692bdf
0000000100692a7a	movl	$0x1a8, %edi                    ## imm = 0x1A8
0000000100692a7f	callq	0x1052c301e                     ## symbol stub for: __Znwm
0000000100692a84	movq	%rax, %r12
0000000100692a87	movq	%rax, %rdi
0000000100692a8a	callq	__ZN14ISkinContainerC2Ev        ## ISkinContainer::ISkinContainer()
0000000100692a8f	leaq	0x53805c2(%rip), %rax
0000000100692a96	movq	%rax, VPX_ARCH_MIPS(%r12)
0000000100692a9a	movq	$-0x1, 0x184(%r12)
0000000100692aa6	movw	$VPX_ARCH_MIPS, 0x18c(%r12)
0000000100692ab1	movb	$0x0, 0x18e(%r12)
0000000100692aba	xorps	%xmm0, %xmm0
0000000100692abd	movups	%xmm0, 0x198(%r12)
0000000100692ac6	movl	%ebx, 0x180(%r12)
0000000100692ace	movq	-0x58(%rbp), %rax
0000000100692ad2	movq	%rax, 0x190(%r12)
0000000100692ada	movabsq	$0x3f8000003f800000, %rax       ## imm = 0x3F8000003F800000
0000000100692ae4	movq	%rax, 0x10(%r12)
0000000100692ae9	movl	$0xffffffff, 0x38(%r12)         ## imm = 0xFFFFFFFF
0000000100692af2	movq	%r13, %rcx
0000000100692af5	movq	0xc8(%r13), %r13
0000000100692afc	movq	0xd0(%rcx), %rax
0000000100692b03	cmpq	%rax, %r13
0000000100692b06	jae	0x100692b1c
0000000100692b08	movq	%r12, (%r13)
0000000100692b0c	addq	$0x8, %r13
0000000100692b10	movq	%r13, 0xc8(%rcx)
0000000100692b17	jmp	0x100692bdb
0000000100692b1c	movq	-0x38(%rbp), %rcx
0000000100692b20	movq	VPX_ARCH_MIPS(%rcx), %rcx
0000000100692b23	subq	%rcx, %r13
0000000100692b26	sarq	$0x3, %r13
0000000100692b2a	leaq	0x1(%r13), %rdx
0000000100692b2e	movabsq	$0x1fffffffffffffff, %rdi       ## imm = 0x1FFFFFFFFFFFFFFF
0000000100692b38	cmpq	%rdi, %rdx
0000000100692b3b	ja	0x100692d5f
0000000100692b41	subq	%rcx, %rax
0000000100692b44	movq	%rax, %rsi
0000000100692b47	sarq	$0x2, %rsi
0000000100692b4b	cmpq	%rdx, %rsi
0000000100692b4e	cmovbeq	%rdx, %rsi
0000000100692b52	movabsq	$0x7ffffffffffffff8, %rcx       ## imm = 0x7FFFFFFFFFFFFFF8
0000000100692b5c	cmpq	%rcx, %rax
0000000100692b5f	cmovaeq	%rdi, %rsi
0000000100692b63	testq	%rsi, %rsi
0000000100692b66	je	0x100692b76
0000000100692b68	movq	-0x88(%rbp), %rdi
0000000100692b6f	callq	__ZNSt3__119__allocate_at_leastB6v15006INS_9allocatorIP11ISkinObjectEEEENS_19__allocation_resultINS_16allocator_traitsIT_E7pointerEEERS7_m ## std::__1::__allocation_result<std::__1::allocator_traits<std::__1::allocator<ISkinObject*>>::pointer> std::__1::__allocate_at_least[abi:v15006]<std::__1::allocator<ISkinObject*>>(std::__1::allocator<ISkinObject*>&, unsigned long)
0000000100692b74	jmp	0x100692b7a
0000000100692b76	xorl	%eax, %eax
0000000100692b78	xorl	%edx, %edx
0000000100692b7a	leaq	VPX_ARCH_MIPS(%rax,%r13,8), %r15
0000000100692b7e	leaq	VPX_ARCH_MIPS(%rax,%rdx,8), %rcx
0000000100692b82	movq	%rcx, -0x48(%rbp)
0000000100692b86	movq	%r12, VPX_ARCH_MIPS(%r15)
0000000100692b89	leaq	VPX_ARCH_MIPS(%rax,%r13,8), %r13
0000000100692b8d	addq	$0x8, %r13
0000000100692b91	movq	-0x50(%rbp), %rbx
0000000100692b95	movq	0xc0(%rbx), %rsi
0000000100692b9c	movq	0xc8(%rbx), %rdx
0000000100692ba3	subq	%rsi, %rdx
0000000100692ba6	subq	%rdx, %r15
0000000100692ba9	movq	%r15, %rdi
0000000100692bac	callq	0x1052c3756                     ## symbol stub for: _memmove
0000000100692bb1	movq	0xc0(%rbx), %rdi
0000000100692bb8	movq	%r15, 0xc0(%rbx)
0000000100692bbf	movq	%r13, 0xc8(%rbx)
0000000100692bc6	movq	-0x48(%rbp), %rax
0000000100692bca	movq	%rax, 0xd0(%rbx)
0000000100692bd1	testq	%rdi, %rdi
0000000100692bd4	je	0x100692bdb
0000000100692bd6	callq	0x1052c300c                     ## symbol stub for: __ZdlPv
0000000100692bdb	movq	-0x38(%rbp), %r15
0000000100692bdf	movq	VPX_ARCH_MIPS(%r15), %r13
0000000100692be2	movq	(%r13,%r14,8), %rcx
0000000100692be7	movl	$0xffffffff, 0x3c(%rcx)         ## imm = 0xFFFFFFFF
0000000100692bee	movq	0xc8(%r12), %rax
0000000100692bf6	cmpq	0xd0(%r12), %rax
0000000100692bfe	je	0x100692c14
0000000100692c00	movq	%rcx, VPX_ARCH_MIPS(%rax)
0000000100692c03	addq	$0x8, %rax
0000000100692c07	movq	%rax, 0xc8(%r12)
0000000100692c0f	jmp	0x100692cd2
0000000100692c14	subq	0xc0(%r12), %rax
0000000100692c1c	movq	%rax, %rbx
0000000100692c1f	sarq	$0x3, %rbx
0000000100692c23	leaq	0x1(%rbx), %rdx
0000000100692c27	movabsq	$0x1fffffffffffffff, %rdi       ## imm = 0x1FFFFFFFFFFFFFFF
0000000100692c31	cmpq	%rdi, %rdx
0000000100692c34	ja	0x100692d3f
0000000100692c3a	movq	%rax, %rsi
0000000100692c3d	sarq	$0x2, %rsi
0000000100692c41	cmpq	%rdx, %rsi
0000000100692c44	cmovbeq	%rdx, %rsi
0000000100692c48	movabsq	$0x7ffffffffffffff8, %rdx       ## imm = 0x7FFFFFFFFFFFFFF8
0000000100692c52	cmpq	%rdx, %rax
0000000100692c55	cmovaeq	%rdi, %rsi
0000000100692c59	testq	%rsi, %rsi
0000000100692c5c	je	0x100692c72
0000000100692c5e	leaq	0xd0(%r12), %rdi
0000000100692c66	callq	__ZNSt3__119__allocate_at_leastB6v15006INS_9allocatorIP11ISkinObjectEEEENS_19__allocation_resultINS_16allocator_traitsIT_E7pointerEEERS7_m ## std::__1::__allocation_result<std::__1::allocator_traits<std::__1::allocator<ISkinObject*>>::pointer> std::__1::__allocate_at_least[abi:v15006]<std::__1::allocator<ISkinObject*>>(std::__1::allocator<ISkinObject*>&, unsigned long)
0000000100692c6b	movq	(%r13,%r14,8), %rcx
0000000100692c70	jmp	0x100692c76
0000000100692c72	xorl	%eax, %eax
0000000100692c74	xorl	%edx, %edx
0000000100692c76	leaq	VPX_ARCH_MIPS(%rax,%rbx,8), %r13
0000000100692c7a	leaq	VPX_ARCH_MIPS(%rax,%rdx,8), %r15
0000000100692c7e	movq	%rcx, (%r13)
0000000100692c82	leaq	VPX_ARCH_MIPS(%rax,%rbx,8), %rbx
0000000100692c86	addq	$0x8, %rbx
0000000100692c8a	movq	0xc0(%r12), %rsi
0000000100692c92	movq	0xc8(%r12), %rdx
0000000100692c9a	subq	%rsi, %rdx
0000000100692c9d	subq	%rdx, %r13
0000000100692ca0	movq	%r13, %rdi
0000000100692ca3	callq	0x1052c3756                     ## symbol stub for: _memmove
0000000100692ca8	movq	0xc0(%r12), %rdi
0000000100692cb0	movq	%r13, 0xc0(%r12)
0000000100692cb8	movq	%rbx, 0xc8(%r12)
0000000100692cc0	movq	%r15, 0xd0(%r12)
0000000100692cc8	testq	%rdi, %rdi
0000000100692ccb	je	0x100692cd2
0000000100692ccd	callq	0x1052c300c                     ## symbol stub for: __ZdlPv
0000000100692cd2	movq	-0x50(%rbp), %r13
0000000100692cd6	movq	0xc0(%r13), %rax
0000000100692cdd	movq	0xc8(%r13), %r12
0000000100692ce4	leaq	VPX_ARCH_MIPS(%rax,%r14,8), %rdi
0000000100692ce8	leaq	VPX_ARCH_MIPS(%rax,%r14,8), %rsi
0000000100692cec	addq	$0x8, %rsi
0000000100692cf0	movq	%r12, %rdx
0000000100692cf3	subq	%rsi, %rdx
0000000100692cf6	callq	0x1052c3756                     ## symbol stub for: _memmove
0000000100692cfb	addq	$-0x8, %r12
0000000100692cff	movq	%r12, 0xc8(%r13)
0000000100692d06	decq	%r14
0000000100692d09	movq	0xc0(%r13), %rax
0000000100692d10	incq	%r14
0000000100692d13	movq	%r12, %rcx
0000000100692d16	subq	%rax, %rcx
0000000100692d19	sarq	$0x3, %rcx
0000000100692d1d	cmpq	%rcx, %r14
0000000100692d20	jb	0x100692a51
0000000100692d26	jmp	0x100692d30
0000000100692d28	addq	$-0x8, 0x54fe8c8(%rip)
0000000100692d30	addq	$0x78, %rsp
0000000100692d34	popq	%rbx
0000000100692d35	popq	%r12
0000000100692d37	popq	%r13
0000000100692d39	popq	%r14
0000000100692d3b	popq	%r15
0000000100692d3d	popq	%rbp
0000000100692d3e	retq
0000000100692d3f	addq	$0xc0, %r12
0000000100692d46	movq	%r12, %rdi
0000000100692d49	callq	__ZNKSt3__16vectorIP11ISkinObjectNS_9allocatorIS2_EEE20__throw_length_errorB6v15006Ev ## std::__1::vector<ISkinObject*, std::__1::allocator<ISkinObject*>>::__throw_length_error[abi:v15006]() const
0000000100692d4e	movl	$0x1d0, %edi                    ## imm = 0x1D0
0000000100692d53	addq	0x531a28e(%rip), %rdi
0000000100692d5a	callq	__ZNKSt3__16vectorIP11CSkinWindowNS_9allocatorIS2_EEE20__throw_length_errorB6v15006Ev ## std::__1::vector<CSkinWindow*, std::__1::allocator<CSkinWindow*>>::__throw_length_error[abi:v15006]() const
0000000100692d5f	movq	-0x38(%rbp), %rdi
0000000100692d63	callq	__ZNKSt3__16vectorIP11ISkinObjectNS_9allocatorIS2_EEE20__throw_length_errorB6v15006Ev ## std::__1::vector<ISkinObject*, std::__1::allocator<ISkinObject*>>::__throw_length_error[abi:v15006]() const
0000000100692d68	leaq	__ZN10CSkinPanel11parentPanelE(%rip), %rdi ## CSkinPanel::parentPanel
0000000100692d6f	callq	__ZNKSt3__16vectorIP10CSkinPanelNS_9allocatorIS2_EEE20__throw_length_errorB6v15006Ev ## std::__1::vector<CSkinPanel*, std::__1::allocator<CSkinPanel*>>::__throw_length_error[abi:v15006]() const
0000000100692d74	jmp	0x100692d76
0000000100692d76	movq	%rax, %rbx
0000000100692d79	movq	%r12, %rdi
0000000100692d7c	callq	0x1052c300c                     ## symbol stub for: __ZdlPv
0000000100692d81	movq	%rbx, %rdi
0000000100692d84	callq	0x1052c2d5a                     ## symbol stub for: __Unwind_Resume
0000000100692d89	nop
