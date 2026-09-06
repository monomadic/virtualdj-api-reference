__ZN11ISkinObject4loadEP8CXMLNodeP6CImage:
00000001003814f0	pushq	%rbp
00000001003814f1	movq	%rsp, %rbp
00000001003814f4	pushq	%r15
00000001003814f6	pushq	%r14
00000001003814f8	pushq	%r13
00000001003814fa	pushq	%r12
00000001003814fc	pushq	%rbx
00000001003814fd	subq	$0x48, %rsp
0000000100381501	movq	%rdx, %r14
0000000100381504	movq	%rsi, %r15
0000000100381507	movq	%rdi, %rbx
000000010038150a	leaq	-0x48(%rbp), %rdi
000000010038150e	leaq	-0x2c(%rbp), %rsi
0000000100381512	callq	__ZN10CSkinPanel20getParentCoordinatesERfS0_ ## CSkinPanel::getParentCoordinates(float&, float&)
0000000100381517	testq	%r15, %r15
000000010038151a	je	0x10038160c
0000000100381520	movq	%r14, -0x50(%rbp)
0000000100381524	leaq	0x525a584(%rip), %r14           ## literal pool for: "deck"
000000010038152b	movl	$FGData.num_y_points, %edx
0000000100381530	movq	%r15, %rdi
0000000100381533	movq	%r14, %rsi
0000000100381536	callq	__ZNK8CXMLNode8hasParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEE ## CXMLNode::hasParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>) const
000000010038153b	testb	%al, %al
000000010038153d	jne	0x10038155a
000000010038153f	leaq	0x52689ad(%rip), %r14           ## literal pool for: "chan"
0000000100381546	movl	$FGData.num_y_points, %edx
000000010038154b	movq	%r15, %rdi
000000010038154e	movq	%r14, %rsi
0000000100381551	callq	__ZNK8CXMLNode8hasParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEE ## CXMLNode::hasParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>) const
0000000100381556	testb	%al, %al
0000000100381558	je	0x100381576
000000010038155a	movl	$FGData.num_y_points, %edx
000000010038155f	movq	%r15, %rdi
0000000100381562	movq	%r14, %rsi
0000000100381565	callq	__ZN8CXMLNode16getParamNonConstENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEE ## CXMLNode::getParamNonConst(std::__1::basic_string_view<char, std::__1::char_traits<char>>)
000000010038156a	leaq	0x40(%rbx), %rsi
000000010038156e	movq	%rax, %rdi
0000000100381571	callq	__ZN7IAction17getDeckFromStringERKNSt3__112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEERj ## IAction::getDeckFromString(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, unsigned int&)
0000000100381576	movl	0x40(%rbx), %esi
0000000100381579	movq	%r15, %rdi
000000010038157c	callq	__ZN10CSkinClass5applyEP8CXMLNodej ## CSkinClass::apply(CXMLNode*, unsigned int)
0000000100381581	leaq	0x52761ae(%rip), %rdx           ## literal pool for: "size"
0000000100381588	movq	%r15, %rsi
000000010038158b	callq	__ZN11ISkinObject12getConditionEP8CXMLNodePKc ## ISkinObject::getCondition(CXMLNode*, char const*)
0000000100381590	movq	%rax, %r14
0000000100381593	leaq	0x5266393(%rip), %rdx           ## literal pool for: "pos"
000000010038159a	movq	%r15, %rsi
000000010038159d	callq	__ZN11ISkinObject12getConditionEP8CXMLNodePKc ## ISkinObject::getCondition(CXMLNode*, char const*)
00000001003815a2	movq	%rax, %r13
00000001003815a5	leaq	0x5268a61(%rip), %rsi           ## literal pool for: "center"
00000001003815ac	movl	$0x6, %edx
00000001003815b1	movq	%r15, %rdi
00000001003815b4	callq	__ZNK8CXMLNode8getChildENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEE ## CXMLNode::getChild(std::__1::basic_string_view<char, std::__1::char_traits<char>>) const
00000001003815b9	movq	%rax, %r12
00000001003815bc	leaq	0x525c91b(%rip), %rsi           ## literal pool for: "width"
00000001003815c3	movl	$0x5, %edx
00000001003815c8	testq	%r14, %r14
00000001003815cb	je	0x10038162d
00000001003815cd	movq	%r14, %rdi
00000001003815d0	xorl	%ecx, %ecx
00000001003815d2	callq	__ZNK8CXMLNode11getIntParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEEi ## CXMLNode::getIntParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>, int) const
00000001003815d7	cvtsi2ss	%eax, %xmm0
00000001003815db	movss	%xmm0, 0x10(%rbx)
00000001003815e0	leaq	0x525c8fd(%rip), %rsi           ## literal pool for: "height"
00000001003815e7	movl	$0x6, %edx
00000001003815ec	movq	%r14, %rdi
00000001003815ef	xorl	%ecx, %ecx
00000001003815f1	callq	__ZNK8CXMLNode11getIntParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEEi ## CXMLNode::getIntParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>, int) const
00000001003815f6	xorps	%xmm0, %xmm0
00000001003815f9	cvtsi2ss	%eax, %xmm0
00000001003815fd	movss	%xmm0, 0x14(%rbx)
0000000100381602	testq	%r13, %r13
0000000100381605	jne	0x10038166b
0000000100381607	jmp	0x1003816f0
000000010038160c	movss	-0x48(%rbp), %xmm0
0000000100381611	movss	%xmm0, 0x8(%rbx)
0000000100381616	movss	-0x2c(%rbp), %xmm0
000000010038161b	movss	%xmm0, 0xc(%rbx)
0000000100381620	movups	0x8(%rbx), %xmm0
0000000100381624	movups	%xmm0, 0x18(%rbx)
0000000100381628	jmp	0x100381cc4
000000010038162d	testq	%r13, %r13
0000000100381630	je	0x1003816bb
0000000100381636	movq	%r13, %rdi
0000000100381639	xorl	%ecx, %ecx
000000010038163b	callq	__ZNK8CXMLNode11getIntParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEEi ## CXMLNode::getIntParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>, int) const
0000000100381640	cvtsi2ss	%eax, %xmm0
0000000100381644	movss	%xmm0, 0x10(%rbx)
0000000100381649	leaq	0x525c894(%rip), %rsi           ## literal pool for: "height"
0000000100381650	movl	$0x6, %edx
0000000100381655	movq	%r13, %rdi
0000000100381658	xorl	%ecx, %ecx
000000010038165a	callq	__ZNK8CXMLNode11getIntParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEEi ## CXMLNode::getIntParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>, int) const
000000010038165f	xorps	%xmm0, %xmm0
0000000100381662	cvtsi2ss	%eax, %xmm0
0000000100381666	movss	%xmm0, 0x14(%rbx)
000000010038166b	cvttss2si	-0x48(%rbp), %ecx
0000000100381670	leaq	0x525c865(%rip), %rsi           ## literal pool for: "x"
0000000100381677	movl	$CONFIG_VP9, %edx
000000010038167c	movq	%r13, %rdi
000000010038167f	movl	%ecx, %r8d
0000000100381682	callq	__ZNK8CXMLNode19getSignedParamApplyENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEEii ## CXMLNode::getSignedParamApply(std::__1::basic_string_view<char, std::__1::char_traits<char>>, int, int) const
0000000100381687	xorps	%xmm0, %xmm0
000000010038168a	cvtsi2ss	%eax, %xmm0
000000010038168e	movss	%xmm0, 0x8(%rbx)
0000000100381693	cvttss2si	-0x2c(%rbp), %ecx
0000000100381698	leaq	0x525bffb(%rip), %rsi           ## literal pool for: "y"
000000010038169f	movl	$CONFIG_VP9, %edx
00000001003816a4	movq	%r13, %rdi
00000001003816a7	movl	%ecx, %r8d
00000001003816aa	callq	__ZNK8CXMLNode19getSignedParamApplyENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEEii ## CXMLNode::getSignedParamApply(std::__1::basic_string_view<char, std::__1::char_traits<char>>, int, int) const
00000001003816af	xorps	%xmm0, %xmm0
00000001003816b2	cvtsi2ss	%eax, %xmm0
00000001003816b6	jmp	0x100381769
00000001003816bb	movq	%r15, %rdi
00000001003816be	xorl	%ecx, %ecx
00000001003816c0	callq	__ZNK8CXMLNode11getIntParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEEi ## CXMLNode::getIntParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>, int) const
00000001003816c5	cvtsi2ss	%eax, %xmm0
00000001003816c9	movss	%xmm0, 0x10(%rbx)
00000001003816ce	leaq	0x525c80f(%rip), %rsi           ## literal pool for: "height"
00000001003816d5	movl	$0x6, %edx
00000001003816da	movq	%r15, %rdi
00000001003816dd	xorl	%ecx, %ecx
00000001003816df	callq	__ZNK8CXMLNode11getIntParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEEi ## CXMLNode::getIntParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>, int) const
00000001003816e4	xorps	%xmm0, %xmm0
00000001003816e7	cvtsi2ss	%eax, %xmm0
00000001003816eb	movss	%xmm0, 0x14(%rbx)
00000001003816f0	cvttss2si	-0x48(%rbp), %ecx
00000001003816f5	leaq	0x525c7e0(%rip), %rsi           ## literal pool for: "x"
00000001003816fc	movl	$CONFIG_VP9, %edx
0000000100381701	testq	%r12, %r12
0000000100381704	je	0x100381cd9
000000010038170a	movq	%r12, %rdi
000000010038170d	movl	%ecx, %r8d
0000000100381710	callq	__ZNK8CXMLNode19getSignedParamApplyENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEEii ## CXMLNode::getSignedParamApply(std::__1::basic_string_view<char, std::__1::char_traits<char>>, int, int) const
0000000100381715	xorps	%xmm0, %xmm0
0000000100381718	cvtsi2ss	%eax, %xmm0
000000010038171c	movss	0x10(%rbx), %xmm1
0000000100381721	mulss	0x4e0c85f(%rip), %xmm1
0000000100381729	addss	%xmm0, %xmm1
000000010038172d	movss	%xmm1, 0x8(%rbx)
0000000100381732	cvttss2si	-0x2c(%rbp), %ecx
0000000100381737	leaq	0x525bf5c(%rip), %rsi           ## literal pool for: "y"
000000010038173e	movl	$CONFIG_VP9, %edx
0000000100381743	movq	%r12, %rdi
0000000100381746	movl	%ecx, %r8d
0000000100381749	callq	__ZNK8CXMLNode19getSignedParamApplyENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEEii ## CXMLNode::getSignedParamApply(std::__1::basic_string_view<char, std::__1::char_traits<char>>, int, int) const
000000010038174e	xorps	%xmm0, %xmm0
0000000100381751	cvtsi2ss	%eax, %xmm0
0000000100381755	movss	0x4e0c82b(%rip), %xmm1
000000010038175d	mulss	0x14(%rbx), %xmm1
0000000100381762	addss	%xmm0, %xmm1
0000000100381766	movaps	%xmm1, %xmm0
0000000100381769	movss	%xmm0, 0xc(%rbx)
000000010038176e	leaq	0x527dbf8(%rip), %rsi           ## literal pool for: "minwidth"
0000000100381775	movl	$msac.end, %edx
000000010038177a	movq	%r15, %rdi
000000010038177d	xorl	%ecx, %ecx
000000010038177f	callq	__ZNK8CXMLNode11getIntParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEEi ## CXMLNode::getIntParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>, int) const
0000000100381784	xorps	%xmm0, %xmm0
0000000100381787	cvtsi2ss	%eax, %xmm0
000000010038178b	movss	%xmm0, FGData.grain_scale_shift(%rbx)
0000000100381793	leaq	0x527dbdc(%rip), %rsi           ## literal pool for: "maxwidth"
000000010038179a	movl	$msac.end, %edx
000000010038179f	movq	%r15, %rdi
00000001003817a2	xorl	%ecx, %ecx
00000001003817a4	callq	__ZNK8CXMLNode11getIntParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEEi ## CXMLNode::getIntParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>, int) const
00000001003817a9	xorps	%xmm0, %xmm0
00000001003817ac	cvtsi2ss	%eax, %xmm0
00000001003817b0	movss	%xmm0, FGData.uv_mult(%rbx)
00000001003817b8	movzbl	0x28(%rbx), %ecx
00000001003817bc	leaq	0x527dbbc(%rip), %rsi           ## literal pool for: "canstretch"
00000001003817c3	movl	$0xa, %edx
00000001003817c8	movq	%r15, %rdi
00000001003817cb	callq	__ZNK8CXMLNode12getBoolParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEEb ## CXMLNode::getBoolParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>, bool) const
00000001003817d0	movb	%al, 0x28(%rbx)
00000001003817d3	movups	0x8(%rbx), %xmm0
00000001003817d7	movups	%xmm0, 0x18(%rbx)
00000001003817db	leaq	0x527dba8(%rip), %rsi           ## literal pool for: "tooltip"
00000001003817e2	movl	$0x7, %edx
00000001003817e7	movq	%r15, %rdi
00000001003817ea	callq	__ZNK8CXMLNode8hasParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEE ## CXMLNode::hasParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>) const
00000001003817ef	leaq	0x527db94(%rip), %rsi           ## literal pool for: "tooltip"
00000001003817f6	movl	$0x7, %edx
00000001003817fb	movq	%r15, %rdi
00000001003817fe	testb	%al, %al
0000000100381800	je	0x100381822
0000000100381802	callq	__ZN8CXMLNode16getParamNonConstENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEE ## CXMLNode::getParamNonConst(std::__1::basic_string_view<char, std::__1::char_traits<char>>)
0000000100381807	leaq	0x58(%rbx), %r12
000000010038180b	movq	%r12, %rdi
000000010038180e	movq	%rax, %rsi
0000000100381811	callq	0x104fe856a                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
0000000100381816	movzbl	0x58(%rbx), %eax
000000010038181a	testb	$0x1, %al
000000010038181c	jne	0x10038185c
000000010038181e	shrl	%eax
0000000100381820	jmp	0x100381860
0000000100381822	callq	__ZNK8CXMLNode8getChildENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEE ## CXMLNode::getChild(std::__1::basic_string_view<char, std::__1::char_traits<char>>) const
0000000100381827	testq	%rax, %rax
000000010038182a	je	0x10038186a
000000010038182c	leaq	0x527db57(%rip), %rsi           ## literal pool for: "tooltip"
0000000100381833	movl	$0x7, %edx
0000000100381838	movq	%r15, %rdi
000000010038183b	callq	__ZNK8CXMLNode8getChildENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEE ## CXMLNode::getChild(std::__1::basic_string_view<char, std::__1::char_traits<char>>) const
0000000100381840	leaq	0x48(%rax), %rsi
0000000100381844	leaq	0x58(%rbx), %r12
0000000100381848	movq	%r12, %rdi
000000010038184b	callq	0x104fe856a                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
0000000100381850	movzbl	0x58(%rbx), %eax
0000000100381854	testb	$0x1, %al
0000000100381856	jne	0x1003818ac
0000000100381858	shrl	%eax
000000010038185a	jmp	0x1003818b0
000000010038185c	movq	0x60(%rbx), %rax
0000000100381860	testq	%rax, %rax
0000000100381863	jne	0x1003818cd
0000000100381865	jmp	0x10038190d
000000010038186a	leaq	0x527db21(%rip), %rsi           ## literal pool for: "tooltipaction"
0000000100381871	movl	$0xd, %edx
0000000100381876	movq	%r15, %rdi
0000000100381879	callq	__ZNK8CXMLNode8hasParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEE ## CXMLNode::hasParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>) const
000000010038187e	testb	%al, %al
0000000100381880	je	0x100381911
0000000100381886	leaq	0x527db05(%rip), %rsi           ## literal pool for: "tooltipaction"
000000010038188d	movl	$0xd, %edx
0000000100381892	movq	%r15, %rdi
0000000100381895	callq	__ZN8CXMLNode16getParamNonConstENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEE ## CXMLNode::getParamNonConst(std::__1::basic_string_view<char, std::__1::char_traits<char>>)
000000010038189a	testb	$0x1, CONFIG_EMULATE_HARDWARE(%rax)
000000010038189d	je	0x100381e03
00000001003818a3	movq	0x10(%rax), %rax
00000001003818a7	jmp	0x100381e06
00000001003818ac	movq	0x60(%rbx), %rax
00000001003818b0	testq	%rax, %rax
00000001003818b3	jne	0x1003818cd
00000001003818b5	leaq	0x5272c2d(%rip), %rsi           ## literal pool for: "localized"
00000001003818bc	movl	$0x9, %edx
00000001003818c1	movq	%r15, %rdi
00000001003818c4	callq	__ZNK8CXMLNode8hasParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEE ## CXMLNode::hasParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>) const
00000001003818c9	testb	%al, %al
00000001003818cb	je	0x10038190d
00000001003818cd	leaq	_messageEngine(%rip), %rsi
00000001003818d4	leaq	-0x68(%rbp), %rdi
00000001003818d8	movq	%r12, %rdx
00000001003818db	movq	%r15, %rcx
00000001003818de	movl	$CONFIG_VP9, %r8d
00000001003818e4	callq	__ZN14CMessageEngine12localizeSkinERKNSt3__112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEEP8CXMLNodeb ## CMessageEngine::localizeSkin(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, CXMLNode*, bool)
00000001003818e9	testb	$0x1, CONFIG_EMULATE_HARDWARE(%r12)
00000001003818ee	je	0x1003818f9
00000001003818f0	movq	0x68(%rbx), %rdi
00000001003818f4	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
00000001003818f9	movq	-0x58(%rbp), %rax
00000001003818fd	movq	%rax, 0x10(%r12)
0000000100381902	movups	-0x68(%rbp), %xmm0
0000000100381906	movups	%xmm0, CONFIG_EMULATE_HARDWARE(%r12)
000000010038190b	jmp	0x100381911
000000010038190d	movb	$0x1, 0x44(%rbx)
0000000100381911	leaq	0x58(%rbx), %rdi
0000000100381915	leaq	0x525b6ad(%rip), %rsi           ## literal pool for: "\\n"
000000010038191c	leaq	0x5275e5d(%rip), %rcx           ## literal pool for: "\n"
0000000100381923	movl	$0x2, %edx
0000000100381928	movl	$CONFIG_VP9, %r8d
000000010038192e	callq	__Z18strReplace_inplacePNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEENS_17basic_string_viewIcS2_EES8_ ## strReplace_inplace(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>*, std::__1::basic_string_view<char, std::__1::char_traits<char>>, std::__1::basic_string_view<char, std::__1::char_traits<char>>)
0000000100381933	leaq	0x526a660(%rip), %rsi           ## literal pool for: "visibility"
000000010038193a	movl	$0xa, %edx
000000010038193f	movq	%r15, -0x38(%rbp)
0000000100381943	movq	%r15, %rdi
0000000100381946	callq	__ZN8CXMLNode16getParamNonConstENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEE ## CXMLNode::getParamNonConst(std::__1::basic_string_view<char, std::__1::char_traits<char>>)
000000010038194b	movq	%rax, %r15
000000010038194e	movzbl	CONFIG_EMULATE_HARDWARE(%rax), %r13d
0000000100381952	testb	$0x1, %r13b
0000000100381956	jne	0x10038196c
0000000100381958	testq	%r13, %r13
000000010038195b	je	0x1003819a7
000000010038195d	movq	%rbx, -0x40(%rbp)
0000000100381961	movq	%r15, %r12
0000000100381964	incq	%r12
0000000100381967	shrl	%r13d
000000010038196a	jmp	0x10038197d
000000010038196c	movq	0x8(%r15), %r13
0000000100381970	testq	%r13, %r13
0000000100381973	je	0x1003819a7
0000000100381975	movq	%rbx, -0x40(%rbp)
0000000100381979	movq	0x10(%r15), %r12
000000010038197d	xorl	%ebx, %ebx
000000010038197f	leaq	0x527da1a(%rip), %r14           ## literal pool for: "0123456789.%"
0000000100381986	movsbl	CONFIG_EMULATE_HARDWARE(%r12,%rbx), %esi
000000010038198b	movl	$rf.ih4, %edx
0000000100381990	movq	%r14, %rdi
0000000100381993	callq	0x104fe8ec4                     ## symbol stub for: _memchr
0000000100381998	testq	%rax, %rax
000000010038199b	je	0x1003819cd
000000010038199d	incq	%rbx
00000001003819a0	cmpq	%rbx, %r13
00000001003819a3	jne	0x100381986
00000001003819a5	jmp	0x1003819f1
00000001003819a7	leaq	0x527da09(%rip), %rsi           ## literal pool for: "novisibility"
00000001003819ae	movl	$rf.ih4, %edx
00000001003819b3	movq	-0x38(%rbp), %r14
00000001003819b7	movq	%r14, %rdi
00000001003819ba	callq	__ZN8CXMLNode16getParamNonConstENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEE ## CXMLNode::getParamNonConst(std::__1::basic_string_view<char, std::__1::char_traits<char>>)
00000001003819bf	movzbl	CONFIG_EMULATE_HARDWARE(%rax), %ecx
00000001003819c2	testb	$0x1, %cl
00000001003819c5	je	0x100381a34
00000001003819c7	movq	0x8(%rax), %rcx
00000001003819cb	jmp	0x100381a36
00000001003819cd	cmpq	$-0x1, %rbx
00000001003819d1	je	0x1003819f1
00000001003819d3	movq	-0x40(%rbp), %rbx
00000001003819d7	movl	0x40(%rbx), %edx
00000001003819da	movl	$CONFIG_VP9, %edi
00000001003819df	movq	%r15, %rsi
00000001003819e2	callq	__ZN11CSkinEngine12createActionEbRKNSt3__112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEEi ## CSkinEngine::createAction(bool, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, int)
00000001003819e7	movq	%rax, 0x30(%rbx)
00000001003819eb	movq	-0x38(%rbp), %r14
00000001003819ef	jmp	0x100381a58
00000001003819f1	leaq	0x527d9b5(%rip), %rsi           ## literal pool for: "constant "
00000001003819f8	leaq	-0x68(%rbp), %r14
00000001003819fc	movq	%r14, %rdi
00000001003819ff	movq	%r15, %rdx
0000000100381a02	callq	0x104fe86fc                     ## symbol stub for: __ZNSt3__1plIcNS_11char_traitsIcEENS_9allocatorIcEEEENS_12basic_stringIT_T0_T1_EEPKS6_RKS9_
0000000100381a07	movq	-0x40(%rbp), %rbx
0000000100381a0b	movl	0x40(%rbx), %edx
0000000100381a0e	movl	$CONFIG_VP9, %edi
0000000100381a13	movq	%r14, %rsi
0000000100381a16	callq	__ZN11CSkinEngine12createActionEbRKNSt3__112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEEi ## CSkinEngine::createAction(bool, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, int)
0000000100381a1b	movq	%rax, 0x30(%rbx)
0000000100381a1f	testb	$0x1, -0x68(%rbp)
0000000100381a23	movq	-0x38(%rbp), %r14
0000000100381a27	je	0x100381a58
0000000100381a29	movq	-0x58(%rbp), %rdi
0000000100381a2d	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
0000000100381a32	jmp	0x100381a58
0000000100381a34	shrl	%ecx
0000000100381a36	testq	%rcx, %rcx
0000000100381a39	je	0x100381a58
0000000100381a3b	movl	0x40(%rbx), %edx
0000000100381a3e	movl	$CONFIG_VP9, %edi
0000000100381a43	movq	%rax, %rsi
0000000100381a46	callq	__ZN11CSkinEngine12createActionEbRKNSt3__112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEEi ## CSkinEngine::createAction(bool, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, int)
0000000100381a4b	movq	%rax, 0x30(%rbx)
0000000100381a4f	testq	%rax, %rax
0000000100381a52	je	0x100381a58
0000000100381a54	movb	$0x1, 0x2b(%rbx)
0000000100381a58	leaq	0x527d965(%rip), %rsi           ## literal pool for: "clickthrough"
0000000100381a5f	movl	$rf.ih4, %edx
0000000100381a64	movq	%r14, %rdi
0000000100381a67	callq	__ZNK8CXMLNode8hasParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEE ## CXMLNode::hasParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>) const
0000000100381a6c	testb	%al, %al
0000000100381a6e	je	0x100381ab6
0000000100381a70	leaq	0x527d94d(%rip), %rsi           ## literal pool for: "clickthrough"
0000000100381a77	leaq	0x527d953(%rip), %rcx           ## literal pool for: "pass"
0000000100381a7e	movl	$rf.ih4, %edx
0000000100381a83	movl	$FGData.num_y_points, %r8d
0000000100381a89	movq	%r14, %rdi
0000000100381a8c	callq	__ZNK8CXMLNode7isParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEES4_ ## CXMLNode::isParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>, std::__1::basic_string_view<char, std::__1::char_traits<char>>) const
0000000100381a91	movl	$0xfffffffe, %ecx               ## imm = 0xFFFFFFFE
0000000100381a96	testb	%al, %al
0000000100381a98	jne	0x100381ab3
0000000100381a9a	leaq	0x527d923(%rip), %rsi           ## literal pool for: "clickthrough"
0000000100381aa1	movl	$rf.ih4, %edx
0000000100381aa6	movq	%r14, %rdi
0000000100381aa9	xorl	%ecx, %ecx
0000000100381aab	callq	__ZNK8CXMLNode12getBoolParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEEb ## CXMLNode::getBoolParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>, bool) const
0000000100381ab0	movzbl	%al, %ecx
0000000100381ab3	movl	%ecx, 0x38(%rbx)
0000000100381ab6	leaq	0x527d919(%rip), %rsi           ## literal pool for: "panel"
0000000100381abd	leaq	0x527d918(%rip), %rcx           ## literal pool for: "pannel"
0000000100381ac4	movl	$0x5, %edx
0000000100381ac9	movl	$0x6, %r8d
0000000100381acf	movq	%r14, %rdi
0000000100381ad2	callq	__ZNK8CXMLNode9getParam2ENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEES4_ ## CXMLNode::getParam2(std::__1::basic_string_view<char, std::__1::char_traits<char>>, std::__1::basic_string_view<char, std::__1::char_traits<char>>) const
0000000100381ad7	movzbl	CONFIG_EMULATE_HARDWARE(%rax), %ecx
0000000100381ada	testb	$0x1, %cl
0000000100381add	je	0x100381ae5
0000000100381adf	movq	0x8(%rax), %rcx
0000000100381ae3	jmp	0x100381ae7
0000000100381ae5	shrl	%ecx
0000000100381ae7	testq	%rcx, %rcx
0000000100381aea	je	0x100381b03
0000000100381aec	leaq	_skinEngine(%rip), %rdi
0000000100381af3	movq	%rax, %rsi
0000000100381af6	movl	$CONFIG_VP9, %edx
0000000100381afb	callq	__ZN11CSkinEngine13getPanelIndexERKNSt3__112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEEb ## CSkinEngine::getPanelIndex(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, bool)
0000000100381b00	movl	%eax, 0x3c(%rbx)
0000000100381b03	leaq	0x527d8d9(%rip), %rsi           ## literal pool for: "mouserect"
0000000100381b0a	movl	$0x9, %edx
0000000100381b0f	movq	%r14, %rdi
0000000100381b12	callq	__ZNK8CXMLNode8getChildENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEE ## CXMLNode::getChild(std::__1::basic_string_view<char, std::__1::char_traits<char>>) const
0000000100381b17	testq	%rax, %rax
0000000100381b1a	je	0x100381be4
0000000100381b20	movq	%rax, %r12
0000000100381b23	cvttss2si	0x8(%rbx), %ecx
0000000100381b28	leaq	0x525c3ad(%rip), %rsi           ## literal pool for: "x"
0000000100381b2f	movl	$CONFIG_VP9, %edx
0000000100381b34	movq	%rax, %rdi
0000000100381b37	movl	%ecx, %r8d
0000000100381b3a	callq	__ZNK8CXMLNode19getSignedParamApplyENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEEii ## CXMLNode::getSignedParamApply(std::__1::basic_string_view<char, std::__1::char_traits<char>>, int, int) const
0000000100381b3f	xorps	%xmm0, %xmm0
0000000100381b42	cvtsi2ss	%eax, %xmm0
0000000100381b46	subss	0x8(%rbx), %xmm0
0000000100381b4b	cvttss2si	%xmm0, %eax
0000000100381b4f	movl	%eax, rf.rp_ref(%rbx)
0000000100381b55	cvttss2si	0xc(%rbx), %ecx
0000000100381b5a	leaq	0x525bb39(%rip), %rsi           ## literal pool for: "y"
0000000100381b61	movl	$CONFIG_VP9, %edx
0000000100381b66	movq	%r12, %rdi
0000000100381b69	movl	%ecx, %r8d
0000000100381b6c	callq	__ZNK8CXMLNode19getSignedParamApplyENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEEii ## CXMLNode::getSignedParamApply(std::__1::basic_string_view<char, std::__1::char_traits<char>>, int, int) const
0000000100381b71	xorps	%xmm0, %xmm0
0000000100381b74	cvtsi2ss	%eax, %xmm0
0000000100381b78	subss	0xc(%rbx), %xmm0
0000000100381b7d	cvttss2si	%xmm0, %eax
0000000100381b81	movl	%eax, 0xac(%rbx)
0000000100381b87	cvttss2si	0x10(%rbx), %ecx
0000000100381b8c	leaq	0x525c34b(%rip), %rsi           ## literal pool for: "width"
0000000100381b93	movl	$0x5, %edx
0000000100381b98	movq	%r12, %rdi
0000000100381b9b	callq	__ZNK8CXMLNode11getIntParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEEi ## CXMLNode::getIntParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>, int) const
0000000100381ba0	movl	%eax, rf.rp_proj(%rbx)
0000000100381ba6	cvttss2si	0x14(%rbx), %ecx
0000000100381bab	leaq	0x525c332(%rip), %rsi           ## literal pool for: "height"
0000000100381bb2	movl	$0x6, %edx
0000000100381bb7	movq	%r12, %rdi
0000000100381bba	callq	__ZNK8CXMLNode11getIntParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEEi ## CXMLNode::getIntParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>, int) const
0000000100381bbf	movl	%eax, 0xb4(%rbx)
0000000100381bc5	movb	$0x1, %r12b
0000000100381bc8	cmpl	$0x0, rf.rp_proj(%rbx)
0000000100381bcf	jne	0x100381cc7
0000000100381bd5	movl	$0xffffffff, rf.rp_proj(%rbx)   ## imm = 0xFFFFFFFF
0000000100381bdf	jmp	0x100381cc7
0000000100381be4	leaq	0x527d802(%rip), %rsi           ## literal pool for: "mousecircle"
0000000100381beb	movl	$0xb, %edx
0000000100381bf0	movq	%r14, %rdi
0000000100381bf3	callq	__ZNK8CXMLNode8getChildENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEE ## CXMLNode::getChild(std::__1::basic_string_view<char, std::__1::char_traits<char>>) const
0000000100381bf8	testq	%rax, %rax
0000000100381bfb	je	0x100381d09
0000000100381c01	movq	%rax, %r12
0000000100381c04	movss	0x10(%rbx), %xmm0
0000000100381c09	mulss	0x4e0b8a3(%rip), %xmm0
0000000100381c11	addss	0x8(%rbx), %xmm0
0000000100381c16	cvttss2si	%xmm0, %ecx
0000000100381c1a	leaq	0x525c2bb(%rip), %rsi           ## literal pool for: "x"
0000000100381c21	movl	$CONFIG_VP9, %edx
0000000100381c26	movq	%rax, %rdi
0000000100381c29	movl	%ecx, %r8d
0000000100381c2c	callq	__ZNK8CXMLNode19getSignedParamApplyENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEEii ## CXMLNode::getSignedParamApply(std::__1::basic_string_view<char, std::__1::char_traits<char>>, int, int) const
0000000100381c31	xorps	%xmm0, %xmm0
0000000100381c34	cvtsi2ss	%eax, %xmm0
0000000100381c38	subss	0x8(%rbx), %xmm0
0000000100381c3d	cvttss2si	%xmm0, %eax
0000000100381c41	movl	%eax, rf.rp_ref(%rbx)
0000000100381c47	movss	0x14(%rbx), %xmm0
0000000100381c4c	mulss	0x4e0b860(%rip), %xmm0
0000000100381c54	addss	0xc(%rbx), %xmm0
0000000100381c59	cvttss2si	%xmm0, %ecx
0000000100381c5d	leaq	0x525ba36(%rip), %rsi           ## literal pool for: "y"
0000000100381c64	movl	$CONFIG_VP9, %edx
0000000100381c69	movq	%r12, %rdi
0000000100381c6c	movl	%ecx, %r8d
0000000100381c6f	callq	__ZNK8CXMLNode19getSignedParamApplyENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEEii ## CXMLNode::getSignedParamApply(std::__1::basic_string_view<char, std::__1::char_traits<char>>, int, int) const
0000000100381c74	xorps	%xmm0, %xmm0
0000000100381c77	cvtsi2ss	%eax, %xmm0
0000000100381c7b	subss	0xc(%rbx), %xmm0
0000000100381c80	cvttss2si	%xmm0, %eax
0000000100381c84	movl	%eax, 0xac(%rbx)
0000000100381c8a	movss	0x14(%rbx), %xmm0
0000000100381c8f	minss	0x10(%rbx), %xmm0
0000000100381c94	mulss	0x4e0b818(%rip), %xmm0
0000000100381c9c	cvttss2si	%xmm0, %ecx
0000000100381ca0	leaq	0x5271d8b(%rip), %rsi           ## literal pool for: "r"
0000000100381ca7	movl	$CONFIG_VP9, %edx
0000000100381cac	movq	%r12, %rdi
0000000100381caf	callq	__ZNK8CXMLNode11getIntParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEEi ## CXMLNode::getIntParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>, int) const
0000000100381cb4	movl	%eax, rf.rp_proj(%rbx)
0000000100381cba	movl	$0xfffffb2e, 0xb4(%rbx)         ## imm = 0xFFFFFB2E
0000000100381cc4	movb	$0x1, %r12b
0000000100381cc7	movl	%r12d, %eax
0000000100381cca	addq	$0x48, %rsp
0000000100381cce	popq	%rbx
0000000100381ccf	popq	%r12
0000000100381cd1	popq	%r13
0000000100381cd3	popq	%r14
0000000100381cd5	popq	%r15
0000000100381cd7	popq	%rbp
0000000100381cd8	retq
0000000100381cd9	movq	%r15, %rdi
0000000100381cdc	movl	%ecx, %r8d
0000000100381cdf	callq	__ZNK8CXMLNode19getSignedParamApplyENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEEii ## CXMLNode::getSignedParamApply(std::__1::basic_string_view<char, std::__1::char_traits<char>>, int, int) const
0000000100381ce4	xorps	%xmm0, %xmm0
0000000100381ce7	cvtsi2ss	%eax, %xmm0
0000000100381ceb	movss	%xmm0, 0x8(%rbx)
0000000100381cf0	cvttss2si	-0x2c(%rbp), %ecx
0000000100381cf5	leaq	0x525b99e(%rip), %rsi           ## literal pool for: "y"
0000000100381cfc	movl	$CONFIG_VP9, %edx
0000000100381d01	movq	%r15, %rdi
0000000100381d04	jmp	0x1003816a7
0000000100381d09	leaq	0x527d6e9(%rip), %rsi           ## literal pool for: "mousemask"
0000000100381d10	movl	$0x9, %edx
0000000100381d15	movq	%r14, %rdi
0000000100381d18	callq	__ZNK8CXMLNode8getChildENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEE ## CXMLNode::getChild(std::__1::basic_string_view<char, std::__1::char_traits<char>>) const
0000000100381d1d	testq	%rax, %rax
0000000100381d20	je	0x100381dbe
0000000100381d26	cmpq	$0x0, -0x50(%rbp)
0000000100381d2b	je	0x100381cc4
0000000100381d2d	movq	%rax, %r13
0000000100381d30	movb	$0x1, %r12b
0000000100381d33	movq	-0x50(%rbp), %rax
0000000100381d37	cmpq	$0x0, 0x28(%rax)
0000000100381d3c	je	0x100381cc7
0000000100381d3e	cvttss2si	0x20(%rbx), %r14d
0000000100381d44	cvttss2si	0x24(%rbx), %eax
0000000100381d49	movq	%rax, -0x38(%rbp)
0000000100381d4d	cvttss2si	0x8(%rbx), %ecx
0000000100381d52	leaq	0x525c183(%rip), %rsi           ## literal pool for: "x"
0000000100381d59	movl	$CONFIG_VP9, %edx
0000000100381d5e	movq	%r13, %rdi
0000000100381d61	movl	%ecx, %r8d
0000000100381d64	callq	__ZNK8CXMLNode19getSignedParamApplyENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEEii ## CXMLNode::getSignedParamApply(std::__1::basic_string_view<char, std::__1::char_traits<char>>, int, int) const
0000000100381d69	movl	%eax, %r15d
0000000100381d6c	cvttss2si	0xc(%rbx), %ecx
0000000100381d71	leaq	0x525b922(%rip), %rsi           ## literal pool for: "y"
0000000100381d78	movl	$CONFIG_VP9, %edx
0000000100381d7d	movq	%r13, %rdi
0000000100381d80	movl	%ecx, %r8d
0000000100381d83	callq	__ZNK8CXMLNode19getSignedParamApplyENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEEii ## CXMLNode::getSignedParamApply(std::__1::basic_string_view<char, std::__1::char_traits<char>>, int, int) const
0000000100381d88	movl	%eax, %r13d
0000000100381d8b	movl	%r15d, %eax
0000000100381d8e	orl	%r13d, %eax
0000000100381d91	js	0x100381db6
0000000100381d93	movq	%r14, -0x40(%rbp)
0000000100381d97	leal	CONFIG_EMULATE_HARDWARE(%r15,%r14), %eax
0000000100381d9b	movq	-0x50(%rbp), %r14
0000000100381d9f	cmpl	CONFIG_EMULATE_HARDWARE(%r14), %eax
0000000100381da2	jg	0x100381db6
0000000100381da4	movq	-0x38(%rbp), %rcx
0000000100381da8	leal	CONFIG_EMULATE_HARDWARE(%rcx,%r13), %eax
0000000100381dac	cmpl	0x4(%r14), %eax
0000000100381db0	jle	0x100381e36
0000000100381db6	xorl	%r12d, %r12d
0000000100381db9	jmp	0x100381cc7
0000000100381dbe	movb	$0x1, %r12b
0000000100381dc1	cmpl	$0x320, _skinVersion(%rip)      ## imm = 0x320
0000000100381dcb	jl	0x100381cc7
0000000100381dd1	leaq	0x526661b(%rip), %rsi           ## literal pool for: "clipmask"
0000000100381dd8	movl	$msac.end, %edx
0000000100381ddd	movq	%r14, %rdi
0000000100381de0	callq	__ZNK8CXMLNode8getChildENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEE ## CXMLNode::getChild(std::__1::basic_string_view<char, std::__1::char_traits<char>>) const
0000000100381de5	movq	%rax, %r13
0000000100381de8	testq	%rax, %rax
0000000100381deb	setne	%al
0000000100381dee	cmpq	$0x0, -0x50(%rbp)
0000000100381df3	setne	%cl
0000000100381df6	testb	%al, %cl
0000000100381df8	je	0x100381cc7
0000000100381dfe	jmp	0x100381d30
0000000100381e03	incq	%rax
0000000100381e06	leaq	_messageEngine(%rip), %rdi
0000000100381e0d	leaq	0x5265aa2(%rip), %rsi           ## literal pool for: "tooltips"
0000000100381e14	movq	%rax, %rdx
0000000100381e17	callq	__ZN14CMessageEngine18getMessageExistingEPKcS1_ ## CMessageEngine::getMessageExisting(char const*, char const*)
0000000100381e1c	testq	%rax, %rax
0000000100381e1f	je	0x100381911
0000000100381e25	leaq	0x58(%rbx), %rdi
0000000100381e29	movq	%rax, %rsi
0000000100381e2c	callq	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE17__assign_externalEPKc ## std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>::__assign_external(char const*)
0000000100381e31	jmp	0x100381911
0000000100381e36	movq	-0x40(%rbp), %rsi
0000000100381e3a	leal	0x7(%rsi), %eax
0000000100381e3d	leal	0xe(%rsi), %edx
0000000100381e40	testl	%eax, %eax
0000000100381e42	cmovnsl	%eax, %edx
0000000100381e45	sarl	$0x3, %edx
0000000100381e48	movl	%edx, -0x44(%rbp)
0000000100381e4b	movl	%edx, %eax
0000000100381e4d	imull	%ecx, %eax
0000000100381e50	movslq	%eax, %rdi
0000000100381e53	movl	$CONFIG_VP9, %esi
0000000100381e58	movq	%rdi, -0x70(%rbp)
0000000100381e5c	callq	0x104fe88e8                     ## symbol stub for: _calloc
0000000100381e61	movq	%rax, rf.rp(%rbx)
0000000100381e68	movq	%r14, %rdi
0000000100381e6b	movl	%r15d, %esi
0000000100381e6e	movl	%r13d, %edx
0000000100381e71	callq	__ZN6CImage8getPixelEii         ## CImage::getPixel(int, int)
0000000100381e76	movq	-0x38(%rbp), %r10
0000000100381e7a	testl	%r10d, %r10d
0000000100381e7d	jle	0x100381cc7
0000000100381e83	shrl	$0x18, %eax
0000000100381e86	movl	-0x40(%rbp), %r14d
0000000100381e8a	xorl	%edx, %edx
0000000100381e8c	movl	%r13d, %esi
0000000100381e8f	movl	-0x44(%rbp), %r11d
0000000100381e93	cmpl	$0x0, -0x40(%rbp)
0000000100381e97	jle	0x100381f16
0000000100381e99	movq	-0x50(%rbp), %rdi
0000000100381e9d	movq	0x28(%rdi), %rcx
0000000100381ea1	movl	%edx, %r8d
0000000100381ea4	imull	%r11d, %r8d
0000000100381ea8	movl	CONFIG_EMULATE_HARDWARE(%rdi), %edi
0000000100381eaa	imull	%esi, %edi
0000000100381ead	addl	%r15d, %edi
0000000100381eb0	movslq	%edi, %rdi
0000000100381eb3	leaq	CONFIG_EMULATE_HARDWARE(%rcx,%rdi,4), %rdi
0000000100381eb7	addq	$0x3, %rdi
0000000100381ebb	movl	%r8d, %r8d
0000000100381ebe	xorl	%r9d, %r9d
0000000100381ec1	movzbl	CONFIG_EMULATE_HARDWARE(%rdi,%r9,4), %ecx
0000000100381ec6	cmpl	%ecx, %eax
0000000100381ec8	jne	0x100381f28
0000000100381eca	cmpb	$0x6, -0x1(%rdi,%r9,4)
0000000100381ed0	jb	0x100381f0e
0000000100381ed2	cmpb	$0x6, -0x3(%rdi,%r9,4)
0000000100381ed8	jb	0x100381f0e
0000000100381eda	cmpb	$0x6, -0x2(%rdi,%r9,4)
0000000100381ee0	jb	0x100381f0e
0000000100381ee2	movl	%r9d, %ecx
0000000100381ee5	andb	$0x7, %cl
0000000100381ee8	movl	$CONFIG_VP9, %r10d
0000000100381eee	shll	%cl, %r10d
0000000100381ef1	movq	rf.rp(%rbx), %rcx
0000000100381ef8	movl	%r9d, %r11d
0000000100381efb	shrl	$0x3, %r11d
0000000100381eff	addq	%r8, %r11
0000000100381f02	orb	%r10b, CONFIG_EMULATE_HARDWARE(%rcx,%r11)
0000000100381f06	movl	-0x44(%rbp), %r11d
0000000100381f0a	movq	-0x38(%rbp), %r10
0000000100381f0e	incq	%r9
0000000100381f11	cmpl	%r9d, %r14d
0000000100381f14	jne	0x100381ec1
0000000100381f16	incl	%edx
0000000100381f18	incl	%esi
0000000100381f1a	cmpl	%r10d, %edx
0000000100381f1d	jl	0x100381e93
0000000100381f23	jmp	0x100381cc7
0000000100381f28	movq	rf.rp(%rbx), %rdi
0000000100381f2f	movq	-0x70(%rbp), %rsi
0000000100381f33	callq	0x104fe8768                     ## symbol stub for: ___bzero
0000000100381f38	movl	-0x44(%rbp), %r11d
0000000100381f3c	movq	-0x38(%rbp), %r10
0000000100381f40	xorl	%eax, %eax
0000000100381f42	movq	-0x50(%rbp), %rdx
0000000100381f46	movq	0x28(%rdx), %rcx
0000000100381f4a	movl	%eax, %esi
0000000100381f4c	imull	%r11d, %esi
0000000100381f50	movl	CONFIG_EMULATE_HARDWARE(%rdx), %edx
0000000100381f52	imull	%r13d, %edx
0000000100381f56	addl	%r15d, %edx
0000000100381f59	movslq	%edx, %rdx
0000000100381f5c	leaq	CONFIG_EMULATE_HARDWARE(%rcx,%rdx,4), %rdx
0000000100381f60	addq	$0x3, %rdx
0000000100381f64	movl	%esi, %esi
0000000100381f66	xorl	%edi, %edi
0000000100381f68	cmpb	$0x0, CONFIG_EMULATE_HARDWARE(%rdx,%rdi,4)
0000000100381f6c	js	0x100381f91
0000000100381f6e	movl	%edi, %ecx
0000000100381f70	andb	$0x7, %cl
0000000100381f73	movl	$CONFIG_VP9, %r8d
0000000100381f79	shll	%cl, %r8d
0000000100381f7c	movq	rf.rp(%rbx), %rcx
0000000100381f83	movl	%edi, %r9d
0000000100381f86	shrl	$0x3, %r9d
0000000100381f8a	addq	%rsi, %r9
0000000100381f8d	orb	%r8b, CONFIG_EMULATE_HARDWARE(%rcx,%r9)
0000000100381f91	incq	%rdi
0000000100381f94	cmpl	%edi, %r14d
0000000100381f97	jne	0x100381f68
0000000100381f99	incl	%eax
0000000100381f9b	incl	%r13d
0000000100381f9e	cmpl	%r10d, %eax
0000000100381fa1	jne	0x100381f42
0000000100381fa3	jmp	0x100381cc7
0000000100381fa8	movq	%rax, %rbx
0000000100381fab	testb	$0x1, -0x68(%rbp)
0000000100381faf	je	0x100381fba
0000000100381fb1	movq	-0x58(%rbp), %rdi
0000000100381fb5	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
0000000100381fba	movq	%rbx, %rdi
0000000100381fbd	callq	0x104fe8456                     ## symbol stub for: __Unwind_Resume
