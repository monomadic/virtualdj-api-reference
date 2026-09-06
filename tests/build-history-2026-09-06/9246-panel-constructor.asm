__ZN10CSkinPanelC2EP8CXMLNodeP6CImageP11CSkinWindow:
00000001008106f4	pushq	%rbp
00000001008106f5	movq	%rsp, %rbp
00000001008106f8	pushq	%r15
00000001008106fa	pushq	%r14
00000001008106fc	pushq	%r13
00000001008106fe	pushq	%r12
0000000100810700	pushq	%rbx
0000000100810701	pushq	%rax
0000000100810702	movq	%rcx, %r14
0000000100810705	movq	%rdx, %r15
0000000100810708	movq	%rsi, %r12
000000010081070b	movq	%rdi, %rbx
000000010081070e	callq	__ZN14ISkinContainerC1Ev        ## ISkinContainer::ISkinContainer()
0000000100810713	leaq	0x502a1b6(%rip), %rax
000000010081071a	movq	%rax, CONFIG_EMULATE_HARDWARE(%rbx)
000000010081071d	movabsq	$-0x100000000, %rax             ## imm = 0xFFFFFFFF00000000
0000000100810727	movq	%rax, 0x180(%rbx)
000000010081072e	movl	$0xffffffff, %eax               ## imm = 0xFFFFFFFF
0000000100810733	movl	%eax, 0x188(%rbx)
0000000100810739	movw	$CONFIG_EMULATE_HARDWARE, 0x18c(%rbx)
0000000100810742	movb	$0x0, 0x18e(%rbx)
0000000100810749	xorps	%xmm0, %xmm0
000000010081074c	movups	%xmm0, 0x198(%rbx)
0000000100810753	movq	%r14, -0x30(%rbp)
0000000100810757	movq	%r14, 0x190(%rbx)
000000010081075e	movl	%eax, 0x38(%rbx)
0000000100810761	movq	%rbx, %rdi
0000000100810764	movq	%r12, %rsi
0000000100810767	movq	%r15, %rdx
000000010081076a	callq	__ZN11ISkinObject4loadEP8CXMLNodeP6CImage ## ISkinObject::load(CXMLNode*, CImage*)
000000010081076f	leaq	0x4dd974c(%rip), %rsi           ## literal pool for: "background"
0000000100810776	movl	$0xa, %edx
000000010081077b	movq	%r12, %rdi
000000010081077e	callq	__ZNK8CXMLNode8getChildENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEE ## CXMLNode::getChild(std::__1::basic_string_view<char, std::__1::char_traits<char>>) const
0000000100810783	movq	%rax, %r14
0000000100810786	testq	%rax, %rax
0000000100810789	jne	0x1008107a2
000000010081078b	leaq	0x4dd9852(%rip), %rsi           ## literal pool for: "down"
0000000100810792	movl	$FGData.num_y_points, %edx
0000000100810797	movq	%r12, %rdi
000000010081079a	callq	__ZNK8CXMLNode8getChildENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEE ## CXMLNode::getChild(std::__1::basic_string_view<char, std::__1::char_traits<char>>) const
000000010081079f	movq	%rax, %r14
00000001008107a2	leaq	0x4dd7c4a(%rip), %rsi           ## literal pool for: "clipmask"
00000001008107a9	movl	$msac.end, %edx
00000001008107ae	movq	%r12, %rdi
00000001008107b1	callq	__ZNK8CXMLNode8getChildENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEE ## CXMLNode::getChild(std::__1::basic_string_view<char, std::__1::char_traits<char>>) const
00000001008107b6	movq	%rbx, %rdi
00000001008107b9	movq	%r15, %rsi
00000001008107bc	movq	%r12, %rdx
00000001008107bf	movq	%r14, %rcx
00000001008107c2	movq	%rax, %r8
00000001008107c5	callq	__ZN11ISkinObject8getImageEP6CImageP8CXMLNodeS3_S3_ ## ISkinObject::getImage(CImage*, CXMLNode*, CXMLNode*, CXMLNode*)
00000001008107ca	movq	%rax, FGData.clip_to_restricted_range(%rbx)
00000001008107d1	cmpb	$0x0, __ZN11ISkinObject11isVideoSkinE(%rip) ## ISkinObject::isVideoSkin
00000001008107d8	je	0x1008107e3
00000001008107da	leaq	_emptyString(%rip), %rsi
00000001008107e1	jmp	0x10081081d
00000001008107e3	leaq	0x4e19588(%rip), %r14           ## literal pool for: "name"
00000001008107ea	movl	$FGData.num_y_points, %edx
00000001008107ef	movq	%r12, %rdi
00000001008107f2	movq	%r14, %rsi
00000001008107f5	callq	__ZNK8CXMLNode8hasParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEE ## CXMLNode::hasParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>) const
00000001008107fa	leaq	0x4de746b(%rip), %rsi           ## literal pool for: "id"
0000000100810801	testb	%al, %al
0000000100810803	cmovneq	%r14, %rsi
0000000100810807	movzbl	%al, %eax
000000010081080a	leaq	0x2(,%rax,2), %rdx
0000000100810812	movq	%r12, %rdi
0000000100810815	callq	__ZN8CXMLNode16getParamNonConstENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEE ## CXMLNode::getParamNonConst(std::__1::basic_string_view<char, std::__1::char_traits<char>>)
000000010081081a	movq	%rax, %rsi
000000010081081d	movzbl	CONFIG_EMULATE_HARDWARE(%rsi), %eax
0000000100810820	testb	$0x1, %al
0000000100810822	jne	0x100810828
0000000100810824	shrl	%eax
0000000100810826	jmp	0x10081082c
0000000100810828	movq	0x8(%rsi), %rax
000000010081082c	testq	%rax, %rax
000000010081082f	je	0x100810957
0000000100810835	leaq	_skinEngine(%rip), %r13
000000010081083c	movq	%r13, %rdi
000000010081083f	movl	$CONFIG_VP9, %edx
0000000100810844	callq	__ZN11CSkinEngine13getPanelIndexERKNSt3__112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEEb ## CSkinEngine::getPanelIndex(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, bool)
0000000100810849	movl	%eax, 0x180(%rbx)
000000010081084f	leaq	0x4ddc5fd(%rip), %rsi           ## literal pool for: "group"
0000000100810856	movl	$0x5, %edx
000000010081085b	movq	%r12, %rdi
000000010081085e	callq	__ZN8CXMLNode16getParamNonConstENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEE ## CXMLNode::getParamNonConst(std::__1::basic_string_view<char, std::__1::char_traits<char>>)
0000000100810863	movslq	0x180(%rbx), %rcx
000000010081086a	movq	0x290(%r13), %rdx
0000000100810871	imulq	$0x58, %rcx, %rcx
0000000100810875	leaq	CONFIG_EMULATE_HARDWARE(%rdx,%rcx), %rdi
0000000100810879	addq	$0x18, %rdi
000000010081087d	movq	%rax, %rsi
0000000100810880	callq	0x104fe856a                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
0000000100810885	leaq	0x4e17cc6(%rip), %rsi           ## literal pool for: "available"
000000010081088c	movl	$0x9, %edx
0000000100810891	movq	%r12, %rdi
0000000100810894	movl	$CONFIG_VP9, %ecx
0000000100810899	callq	__ZNK8CXMLNode12getBoolParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEEb ## CXMLNode::getBoolParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>, bool) const
000000010081089e	movslq	0x180(%rbx), %rcx
00000001008108a5	movq	0x290(%r13), %rdx
00000001008108ac	imulq	$0x58, %rcx, %rcx
00000001008108b0	movb	%al, 0x49(%rdx,%rcx)
00000001008108b4	leaq	0x4e17ca1(%rip), %rsi           ## literal pool for: "displayname"
00000001008108bb	movl	$0xb, %edx
00000001008108c0	movq	%r12, %rdi
00000001008108c3	callq	__ZN8CXMLNode16getParamNonConstENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEE ## CXMLNode::getParamNonConst(std::__1::basic_string_view<char, std::__1::char_traits<char>>)
00000001008108c8	movslq	0x180(%rbx), %rcx
00000001008108cf	movq	0x290(%r13), %rdx
00000001008108d6	imulq	$0x58, %rcx, %rcx
00000001008108da	leaq	CONFIG_EMULATE_HARDWARE(%rdx,%rcx), %rdi
00000001008108de	addq	$0x30, %rdi
00000001008108e2	movq	%rax, %rsi
00000001008108e5	callq	0x104fe856a                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
00000001008108ea	leaq	0x4e17c77(%rip), %rsi           ## literal pool for: "forceshow"
00000001008108f1	movl	$0x9, %edx
00000001008108f6	movq	%r12, %rdi
00000001008108f9	callq	__ZN8CXMLNode16getParamNonConstENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEE ## CXMLNode::getParamNonConst(std::__1::basic_string_view<char, std::__1::char_traits<char>>)
00000001008108fe	movq	%rax, %r14
0000000100810901	movzbl	CONFIG_EMULATE_HARDWARE(%rax), %ecx
0000000100810904	movl	%ecx, %eax
0000000100810906	shrl	%eax
0000000100810908	andb	$0x1, %cl
000000010081090b	movq	0x8(%r14), %rdx
000000010081090f	movq	%rdx, %rsi
0000000100810912	cmoveq	%rax, %rsi
0000000100810916	testq	%rsi, %rsi
0000000100810919	je	0x100810ab7
000000010081091f	cmpq	$0x3, %rsi
0000000100810923	jne	0x100810975
0000000100810925	leaq	0x4e17c46(%rip), %rsi           ## literal pool for: "1fx"
000000010081092c	movq	%r14, %rdi
000000010081092f	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
0000000100810934	testb	%al, %al
0000000100810936	je	0x100810966
0000000100810938	movslq	0x180(%rbx), %rcx
000000010081093f	movq	0x290(%r13), %rdx
0000000100810946	imulq	$0x58, %rcx, %rax
000000010081094a	movl	$0x2, 0x4c(%rdx,%rax)
0000000100810952	jmp	0x100810aac
0000000100810957	movl	$0xffffffff, 0x180(%rbx)        ## imm = 0xFFFFFFFF
0000000100810961	jmp	0x100810ab7
0000000100810966	movzbl	CONFIG_EMULATE_HARDWARE(%r14), %eax
000000010081096a	movq	0x8(%r14), %rdx
000000010081096e	movl	%eax, %ecx
0000000100810970	andb	$0x1, %cl
0000000100810973	shrl	%eax
0000000100810975	testb	%cl, %cl
0000000100810977	movq	%rdx, %rsi
000000010081097a	cmoveq	%rax, %rsi
000000010081097e	cmpq	$0x3, %rsi
0000000100810982	jne	0x1008109c5
0000000100810984	leaq	0x4e17beb(%rip), %rsi           ## literal pool for: "3fx"
000000010081098b	movq	%r14, %rdi
000000010081098e	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
0000000100810993	testb	%al, %al
0000000100810995	je	0x1008109b6
0000000100810997	movslq	0x180(%rbx), %rcx
000000010081099e	movq	0x290(%r13), %rdx
00000001008109a5	imulq	$0x58, %rcx, %rax
00000001008109a9	movl	$0x3, 0x4c(%rdx,%rax)
00000001008109b1	jmp	0x100810aac
00000001008109b6	movzbl	CONFIG_EMULATE_HARDWARE(%r14), %eax
00000001008109ba	movq	0x8(%r14), %rdx
00000001008109be	movl	%eax, %ecx
00000001008109c0	andb	$0x1, %cl
00000001008109c3	shrl	%eax
00000001008109c5	testb	%cl, %cl
00000001008109c7	movq	%rdx, %rsi
00000001008109ca	cmoveq	%rax, %rsi
00000001008109ce	cmpq	$0x3, %rsi
00000001008109d2	jne	0x100810a15
00000001008109d4	leaq	0x4e17b9f(%rip), %rsi           ## literal pool for: "6fx"
00000001008109db	movq	%r14, %rdi
00000001008109de	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
00000001008109e3	testb	%al, %al
00000001008109e5	je	0x100810a06
00000001008109e7	movslq	0x180(%rbx), %rcx
00000001008109ee	movq	0x290(%r13), %rdx
00000001008109f5	imulq	$0x58, %rcx, %rax
00000001008109f9	movl	$FGData.num_y_points, 0x4c(%rdx,%rax)
0000000100810a01	jmp	0x100810aac
0000000100810a06	movzbl	CONFIG_EMULATE_HARDWARE(%r14), %eax
0000000100810a0a	movq	0x8(%r14), %rdx
0000000100810a0e	movl	%eax, %ecx
0000000100810a10	andb	$0x1, %cl
0000000100810a13	shrl	%eax
0000000100810a15	testb	%cl, %cl
0000000100810a17	cmovneq	%rdx, %rax
0000000100810a1b	cmpq	$0x5, %rax
0000000100810a1f	jne	0x100810a50
0000000100810a21	leaq	0x4e17b56(%rip), %rsi           ## literal pool for: "8pads"
0000000100810a28	movq	%r14, %rdi
0000000100810a2b	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
0000000100810a30	testb	%al, %al
0000000100810a32	je	0x100810a50
0000000100810a34	movslq	0x180(%rbx), %rcx
0000000100810a3b	movq	0x290(%r13), %rdx
0000000100810a42	imulq	$0x58, %rcx, %rax
0000000100810a46	movl	$0x5, 0x4c(%rdx,%rax)
0000000100810a4e	jmp	0x100810aac
0000000100810a50	leaq	0x4e17b2d(%rip), %rsi           ## literal pool for: "16pads"
0000000100810a57	movq	%r14, %rdi
0000000100810a5a	callq	__Z13strIsEqualCILILm7EEbRKNSt3__112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEERAT__Kc ## bool strIsEqualCIL<7ul>(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const (&) [7ul])
0000000100810a5f	testb	%al, %al
0000000100810a61	je	0x100810a7f
0000000100810a63	movslq	0x180(%rbx), %rcx
0000000100810a6a	movq	0x290(%r13), %rdx
0000000100810a71	imulq	$0x58, %rcx, %rax
0000000100810a75	movl	$0x6, 0x4c(%rdx,%rax)
0000000100810a7d	jmp	0x100810aac
0000000100810a7f	leaq	0x4dd755e(%rip), %rsi           ## literal pool for: "timecode"
0000000100810a86	movq	%r14, %rdi
0000000100810a89	callq	__Z13strIsEqualCILILm9EEbRKNSt3__112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEERAT__Kc ## bool strIsEqualCIL<9ul>(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const (&) [9ul])
0000000100810a8e	movslq	0x180(%rbx), %rcx
0000000100810a95	movq	0x290(%r13), %rdx
0000000100810a9c	testb	%al, %al
0000000100810a9e	je	0x100810aac
0000000100810aa0	imulq	$0x58, %rcx, %rax
0000000100810aa4	movl	$CONFIG_VP9, 0x4c(%rdx,%rax)
0000000100810aac	movl	0x40(%rbx), %eax
0000000100810aaf	imulq	$0x58, %rcx, %rcx
0000000100810ab3	movl	%eax, 0x50(%rdx,%rcx)
0000000100810ab7	leaq	0x4de395a(%rip), %rsi           ## literal pool for: "visible"
0000000100810abe	movl	$0x7, %edx
0000000100810ac3	movq	%r12, %rdi
0000000100810ac6	callq	__ZN8CXMLNode16getParamNonConstENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEE ## CXMLNode::getParamNonConst(std::__1::basic_string_view<char, std::__1::char_traits<char>>)
0000000100810acb	movq	%rax, %r13
0000000100810ace	movzbl	CONFIG_EMULATE_HARDWARE(%rax), %ecx
0000000100810ad1	movl	%ecx, %eax
0000000100810ad3	shrl	%eax
0000000100810ad5	andb	$0x1, %cl
0000000100810ad8	movq	0x8(%r13), %rdx
0000000100810adc	movq	%rdx, %rsi
0000000100810adf	cmoveq	%rax, %rsi
0000000100810ae3	cmpq	$0x3, %rsi
0000000100810ae7	jne	0x100810b0c
0000000100810ae9	leaq	0x4dcbcff(%rip), %rsi           ## literal pool for: "yes"
0000000100810af0	movq	%r13, %rdi
0000000100810af3	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
0000000100810af8	testb	%al, %al
0000000100810afa	jne	0x100810b2b
0000000100810afc	movzbl	(%r13), %eax
0000000100810b01	movq	0x8(%r13), %rdx
0000000100810b05	movl	%eax, %ecx
0000000100810b07	andb	$0x1, %cl
0000000100810b0a	shrl	%eax
0000000100810b0c	testb	%cl, %cl
0000000100810b0e	cmovneq	%rdx, %rax
0000000100810b12	cmpq	$0x4, %rax
0000000100810b16	jne	0x100810b53
0000000100810b18	leaq	0x4dea06f(%rip), %rsi           ## literal pool for: "true"
0000000100810b1f	movq	%r13, %rdi
0000000100810b22	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
0000000100810b27	testb	%al, %al
0000000100810b29	je	0x100810b53
0000000100810b2b	movslq	0x180(%rbx), %rax
0000000100810b32	testq	%rax, %rax
0000000100810b35	js	0x100810b53
0000000100810b37	leaq	_skinEngine(%rip), %rcx
0000000100810b3e	movq	0x290(%rcx), %rcx
0000000100810b45	imulq	$0x58, %rax, %rax
0000000100810b49	movb	$0x1, 0x48(%rcx,%rax)
0000000100810b4e	jmp	0x100810c08
0000000100810b53	movzbl	(%r13), %ecx
0000000100810b58	movl	%ecx, %eax
0000000100810b5a	shrl	%eax
0000000100810b5c	andb	$0x1, %cl
0000000100810b5f	movq	0x8(%r13), %rdx
0000000100810b63	movq	%rdx, %rsi
0000000100810b66	cmoveq	%rax, %rsi
0000000100810b6a	cmpq	$0x2, %rsi
0000000100810b6e	jne	0x100810b93
0000000100810b70	leaq	0x4dcbc92(%rip), %rsi           ## literal pool for: "no"
0000000100810b77	movq	%r13, %rdi
0000000100810b7a	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
0000000100810b7f	testb	%al, %al
0000000100810b81	jne	0x100810bb2
0000000100810b83	movzbl	(%r13), %eax
0000000100810b88	movq	0x8(%r13), %rdx
0000000100810b8c	movl	%eax, %ecx
0000000100810b8e	andb	$0x1, %cl
0000000100810b91	shrl	%eax
0000000100810b93	testb	%cl, %cl
0000000100810b95	cmovneq	%rdx, %rax
0000000100810b99	cmpq	$0x5, %rax
0000000100810b9d	jne	0x100810bd7
0000000100810b9f	leaq	0x4dd5bef(%rip), %rsi           ## literal pool for: "false"
0000000100810ba6	movq	%r13, %rdi
0000000100810ba9	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
0000000100810bae	testb	%al, %al
0000000100810bb0	je	0x100810bd7
0000000100810bb2	movslq	0x180(%rbx), %rax
0000000100810bb9	testq	%rax, %rax
0000000100810bbc	js	0x100810bd7
0000000100810bbe	leaq	_skinEngine(%rip), %rcx
0000000100810bc5	movq	0x290(%rcx), %rcx
0000000100810bcc	imulq	$0x58, %rax, %rax
0000000100810bd0	movb	$0x0, 0x48(%rcx,%rax)
0000000100810bd5	jmp	0x100810c08
0000000100810bd7	movzbl	(%r13), %eax
0000000100810bdc	testb	$0x1, %al
0000000100810bde	je	0x100810be6
0000000100810be0	movq	0x8(%r13), %rax
0000000100810be4	jmp	0x100810be8
0000000100810be6	shrl	%eax
0000000100810be8	testq	%rax, %rax
0000000100810beb	je	0x100810c08
0000000100810bed	cmpq	$0x0, 0x30(%rbx)
0000000100810bf2	jne	0x100810c08
0000000100810bf4	movl	0x40(%rbx), %edx
0000000100810bf7	movl	$CONFIG_VP9, %edi
0000000100810bfc	movq	%r13, %rsi
0000000100810bff	callq	__ZN11CSkinEngine12createActionEbRKNSt3__112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEEi ## CSkinEngine::createAction(bool, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, int)
0000000100810c04	movq	%rax, 0x30(%rbx)
0000000100810c08	leaq	0x4e1797c(%rip), %rsi           ## literal pool for: "applyfx"
0000000100810c0f	movl	$0x7, %edx
0000000100810c14	movq	%r12, %rdi
0000000100810c17	xorl	%ecx, %ecx
0000000100810c19	callq	__ZNK8CXMLNode12getBoolParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEEb ## CXMLNode::getBoolParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>, bool) const
0000000100810c1e	movb	%al, 0x18c(%rbx)
0000000100810c24	movzbl	CONFIG_EMULATE_HARDWARE(%r12), %eax
0000000100810c29	testb	$0x1, %al
0000000100810c2b	je	0x100810c34
0000000100810c2d	movq	0x8(%r12), %rax
0000000100810c32	jmp	0x100810c36
0000000100810c34	shrl	%eax
0000000100810c36	cmpq	$0x4, %rax
0000000100810c3a	jne	0x100810c4d
0000000100810c3c	leaq	0x4dd687b(%rip), %rsi           ## literal pool for: "item"
0000000100810c43	movq	%r12, %rdi
0000000100810c46	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
0000000100810c4b	jmp	0x100810c4f
0000000100810c4d	xorl	%eax, %eax
0000000100810c4f	movb	%al, 0x18d(%rbx)
0000000100810c55	movq	0x52144ec(%rip), %rax
0000000100810c5c	cmpq	%rax, __ZN10CSkinPanel11parentPanelE(%rip) ## CSkinPanel::parentPanel
0000000100810c63	je	0x100810c79
0000000100810c65	movq	-0x8(%rax), %rax
0000000100810c69	cmpb	$0x1, 0x18d(%rax)
0000000100810c70	jne	0x100810c79
0000000100810c72	movb	$0x1, 0x18d(%rbx)
0000000100810c79	leaq	0x4e17913(%rip), %rsi           ## literal pool for: "childtooltip"
0000000100810c80	movl	$rf.ih4, %edx
0000000100810c85	movq	%r12, %rdi
0000000100810c88	xorl	%ecx, %ecx
0000000100810c8a	callq	__ZNK8CXMLNode12getBoolParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEEb ## CXMLNode::getBoolParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>, bool) const
0000000100810c8f	movb	%al, 0x18e(%rbx)
0000000100810c95	leaq	0x4de130f(%rip), %rsi           ## literal pool for: "skin"
0000000100810c9c	movq	%r12, %rdi
0000000100810c9f	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
0000000100810ca4	testb	%al, %al
0000000100810ca6	jne	0x100810ce6
0000000100810ca8	leaq	0x4dfa1ca(%rip), %rsi           ## literal pool for: "breakline1"
0000000100810caf	movl	$0xa, %edx
0000000100810cb4	movq	%r12, %rdi
0000000100810cb7	movl	$0xffffffff, %ecx               ## imm = 0xFFFFFFFF
0000000100810cbc	callq	__ZNK8CXMLNode11getIntParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEEi ## CXMLNode::getIntParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>, int) const
0000000100810cc1	movl	%eax, 0x184(%rbx)
0000000100810cc7	leaq	0x4dfa1b6(%rip), %rsi           ## literal pool for: "breakline2"
0000000100810cce	movl	$0xa, %edx
0000000100810cd3	movq	%r12, %rdi
0000000100810cd6	movl	$0xffffffff, %ecx               ## imm = 0xFFFFFFFF
0000000100810cdb	callq	__ZNK8CXMLNode11getIntParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEEi ## CXMLNode::getIntParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>, int) const
0000000100810ce0	movl	%eax, 0x188(%rbx)
0000000100810ce6	cmpl	$0x0, 0x184(%rbx)
0000000100810ced	jns	0x100810d1a
0000000100810cef	cmpl	$0x0, 0x188(%rbx)
0000000100810cf6	jns	0x100810d1a
0000000100810cf8	movq	0x5214449(%rip), %rax
0000000100810cff	cmpq	%rax, __ZN10CSkinPanel11parentPanelE(%rip) ## CSkinPanel::parentPanel
0000000100810d06	je	0x100810d1a
0000000100810d08	movq	-0x8(%rax), %rax
0000000100810d0c	movq	0x184(%rax), %rax
0000000100810d13	movq	%rax, 0x184(%rbx)
0000000100810d1a	movq	%rbx, %rdi
0000000100810d1d	movq	%r12, %rsi
0000000100810d20	movq	%r15, %rdx
0000000100810d23	movq	-0x30(%rbp), %rcx
0000000100810d27	callq	__ZN10CSkinPanel12loadChildrenEP8CXMLNodeP6CImageP11CSkinWindow ## CSkinPanel::loadChildren(CXMLNode*, CImage*, CSkinWindow*)
0000000100810d2c	movq	rf.n_tile_threads(%rbx), %rax
0000000100810d33	subq	rf.r(%rbx), %rax
0000000100810d3a	cmpq	$0x79, %rax
0000000100810d3e	jb	0x100810d47
0000000100810d40	movb	$0x1, 0xe0(%rbx)
0000000100810d47	addq	$0x8, %rsp
0000000100810d4b	popq	%rbx
0000000100810d4c	popq	%r12
0000000100810d4e	popq	%r13
0000000100810d50	popq	%r14
0000000100810d52	popq	%r15
0000000100810d54	popq	%rbp
0000000100810d55	retq
0000000100810d56	jmp	0x100810d5c
0000000100810d58	jmp	0x100810d5c
0000000100810d5a	jmp	0x100810d5c
0000000100810d5c	movq	%rax, %r14
0000000100810d5f	movq	%rbx, %rdi
0000000100810d62	callq	__ZN14ISkinContainerD2Ev        ## ISkinContainer::~ISkinContainer()
0000000100810d67	movq	%r14, %rdi
0000000100810d6a	callq	0x104fe8456                     ## symbol stub for: __Unwind_Resume
0000000100810d6f	addb	%dl, 0x48(%rbp)
