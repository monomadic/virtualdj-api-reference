__ZN11ISkinObject4loadEP8CXMLNodeP6CImage:
00000001002e8cce	pushq	%rbp
00000001002e8ccf	movq	%rsp, %rbp
00000001002e8cd2	pushq	%r15
00000001002e8cd4	pushq	%r14
00000001002e8cd6	pushq	%r13
00000001002e8cd8	pushq	%r12
00000001002e8cda	pushq	%rbx
00000001002e8cdb	subq	$0x58, %rsp
00000001002e8cdf	movq	%rdx, %rbx
00000001002e8ce2	movq	%rsi, %r15
00000001002e8ce5	movq	%rdi, %r13
00000001002e8ce8	leaq	-0x30(%rbp), %rdi
00000001002e8cec	leaq	-0x2c(%rbp), %rsi
00000001002e8cf0	callq	__ZN10CSkinPanel20getParentCoordinatesERfS0_ ## CSkinPanel::getParentCoordinates(float&, float&)
00000001002e8cf5	testq	%r15, %r15
00000001002e8cf8	je	0x1002e8ded
00000001002e8cfe	movq	%rbx, -0x38(%rbp)
00000001002e8d02	leaq	0x550da32(%rip), %rbx           ## literal pool for: "deck"
00000001002e8d09	movl	$FGData.num_y_points, %edx
00000001002e8d0e	movq	%r15, %rdi
00000001002e8d11	movq	%rbx, %rsi
00000001002e8d14	callq	__ZNK8CXMLNode8hasParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEE ## CXMLNode::hasParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>) const
00000001002e8d19	testb	%al, %al
00000001002e8d1b	jne	0x1002e8d38
00000001002e8d1d	leaq	0x551a256(%rip), %rbx           ## literal pool for: "chan"
00000001002e8d24	movl	$FGData.num_y_points, %edx
00000001002e8d29	movq	%r15, %rdi
00000001002e8d2c	movq	%rbx, %rsi
00000001002e8d2f	callq	__ZNK8CXMLNode8hasParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEE ## CXMLNode::hasParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>) const
00000001002e8d34	testb	%al, %al
00000001002e8d36	je	0x1002e8d54
00000001002e8d38	movl	$FGData.num_y_points, %edx
00000001002e8d3d	movq	%r15, %rdi
00000001002e8d40	movq	%rbx, %rsi
00000001002e8d43	callq	__ZNK8CXMLNode8getParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEE ## CXMLNode::getParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>) const
00000001002e8d48	leaq	0x40(%r13), %rsi
00000001002e8d4c	movq	%rax, %rdi
00000001002e8d4f	callq	__ZN7IAction17getDeckFromStringERKNSt3__112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEERj ## IAction::getDeckFromString(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, unsigned int&)
00000001002e8d54	movl	0x40(%r13), %esi
00000001002e8d58	movq	%r15, %rdi
00000001002e8d5b	callq	__ZN10CSkinClass5applyEP8CXMLNodej ## CSkinClass::apply(CXMLNode*, unsigned int)
00000001002e8d60	leaq	0x55258b9(%rip), %rdx           ## literal pool for: "size"
00000001002e8d67	movq	%r15, %rsi
00000001002e8d6a	callq	__ZN11ISkinObject12getConditionEP8CXMLNodePKc ## ISkinObject::getCondition(CXMLNode*, char const*)
00000001002e8d6f	movq	%rax, %r14
00000001002e8d72	leaq	0x5518919(%rip), %rdx           ## literal pool for: "pos"
00000001002e8d79	movq	%r15, %rsi
00000001002e8d7c	callq	__ZN11ISkinObject12getConditionEP8CXMLNodePKc ## ISkinObject::getCondition(CXMLNode*, char const*)
00000001002e8d81	movq	%rax, %rbx
00000001002e8d84	leaq	0x551a2fd(%rip), %rsi           ## literal pool for: "center"
00000001002e8d8b	movl	$0x6, %edx
00000001002e8d90	movq	%r15, %rdi
00000001002e8d93	callq	__ZNK8CXMLNode8getChildENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEE ## CXMLNode::getChild(std::__1::basic_string_view<char, std::__1::char_traits<char>>) const
00000001002e8d98	movq	%rax, %r12
00000001002e8d9b	leaq	0x550fad2(%rip), %rsi           ## literal pool for: "width"
00000001002e8da2	movl	$0x5, %edx
00000001002e8da7	testq	%r14, %r14
00000001002e8daa	je	0x1002e8e12
00000001002e8dac	movq	%r14, %rdi
00000001002e8daf	xorl	%ecx, %ecx
00000001002e8db1	callq	__ZNK8CXMLNode11getIntParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEEi ## CXMLNode::getIntParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>, int) const
00000001002e8db6	cvtsi2ss	%eax, %xmm0
00000001002e8dba	movss	%xmm0, 0x10(%r13)
00000001002e8dc0	leaq	0x550fab3(%rip), %rsi           ## literal pool for: "height"
00000001002e8dc7	movl	$0x6, %edx
00000001002e8dcc	movq	%r14, %rdi
00000001002e8dcf	xorl	%ecx, %ecx
00000001002e8dd1	callq	__ZNK8CXMLNode11getIntParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEEi ## CXMLNode::getIntParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>, int) const
00000001002e8dd6	xorps	%xmm0, %xmm0
00000001002e8dd9	cvtsi2ss	%eax, %xmm0
00000001002e8ddd	movss	%xmm0, 0x14(%r13)
00000001002e8de3	testq	%rbx, %rbx
00000001002e8de6	jne	0x1002e8e4e
00000001002e8de8	jmp	0x1002e8eca
00000001002e8ded	movss	-0x30(%rbp), %xmm0
00000001002e8df2	movss	%xmm0, 0x8(%r13)
00000001002e8df8	movss	-0x2c(%rbp), %xmm0
00000001002e8dfd	movss	%xmm0, 0xc(%r13)
00000001002e8e03	movups	0x8(%r13), %xmm0
00000001002e8e08	movups	%xmm0, 0x18(%r13)
00000001002e8e0d	jmp	0x1002e947f
00000001002e8e12	testq	%rbx, %rbx
00000001002e8e15	je	0x1002e8e93
00000001002e8e17	movq	%rbx, %rdi
00000001002e8e1a	xorl	%ecx, %ecx
00000001002e8e1c	callq	__ZNK8CXMLNode11getIntParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEEi ## CXMLNode::getIntParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>, int) const
00000001002e8e21	cvtsi2ss	%eax, %xmm0
00000001002e8e25	movss	%xmm0, 0x10(%r13)
00000001002e8e2b	leaq	0x550fa48(%rip), %rsi           ## literal pool for: "height"
00000001002e8e32	movl	$0x6, %edx
00000001002e8e37	movq	%rbx, %rdi
00000001002e8e3a	xorl	%ecx, %ecx
00000001002e8e3c	callq	__ZNK8CXMLNode11getIntParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEEi ## CXMLNode::getIntParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>, int) const
00000001002e8e41	xorps	%xmm0, %xmm0
00000001002e8e44	cvtsi2ss	%eax, %xmm0
00000001002e8e48	movss	%xmm0, 0x14(%r13)
00000001002e8e4e	cvttss2si	-0x30(%rbp), %ecx
00000001002e8e53	leaq	0x550fa16(%rip), %rsi           ## literal pool for: "x"
00000001002e8e5a	movq	%rbx, %rdi
00000001002e8e5d	movl	%ecx, %edx
00000001002e8e5f	callq	__ZNK8CXMLNode19getSignedParamApplyEPKcii ## CXMLNode::getSignedParamApply(char const*, int, int) const
00000001002e8e64	xorps	%xmm0, %xmm0
00000001002e8e67	cvtsi2ss	%eax, %xmm0
00000001002e8e6b	movss	%xmm0, 0x8(%r13)
00000001002e8e71	cvttss2si	-0x2c(%rbp), %ecx
00000001002e8e76	leaq	0x550f9f5(%rip), %rsi           ## literal pool for: "y"
00000001002e8e7d	movq	%rbx, %rdi
00000001002e8e80	movl	%ecx, %edx
00000001002e8e82	callq	__ZNK8CXMLNode19getSignedParamApplyEPKcii ## CXMLNode::getSignedParamApply(char const*, int, int) const
00000001002e8e87	xorps	%xmm0, %xmm0
00000001002e8e8a	cvtsi2ss	%eax, %xmm0
00000001002e8e8e	jmp	0x1002e8f3a
00000001002e8e93	movq	%r15, %rdi
00000001002e8e96	xorl	%ecx, %ecx
00000001002e8e98	callq	__ZNK8CXMLNode11getIntParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEEi ## CXMLNode::getIntParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>, int) const
00000001002e8e9d	cvtsi2ss	%eax, %xmm0
00000001002e8ea1	movss	%xmm0, 0x10(%r13)
00000001002e8ea7	leaq	0x550f9cc(%rip), %rsi           ## literal pool for: "height"
00000001002e8eae	movl	$0x6, %edx
00000001002e8eb3	movq	%r15, %rdi
00000001002e8eb6	xorl	%ecx, %ecx
00000001002e8eb8	callq	__ZNK8CXMLNode11getIntParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEEi ## CXMLNode::getIntParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>, int) const
00000001002e8ebd	xorps	%xmm0, %xmm0
00000001002e8ec0	cvtsi2ss	%eax, %xmm0
00000001002e8ec4	movss	%xmm0, 0x14(%r13)
00000001002e8eca	cvttss2si	-0x30(%rbp), %ecx
00000001002e8ecf	leaq	0x550f99a(%rip), %rsi           ## literal pool for: "x"
00000001002e8ed6	testq	%r12, %r12
00000001002e8ed9	je	0x1002e9492
00000001002e8edf	movq	%r12, %rdi
00000001002e8ee2	movl	%ecx, %edx
00000001002e8ee4	callq	__ZNK8CXMLNode19getSignedParamApplyEPKcii ## CXMLNode::getSignedParamApply(char const*, int, int) const
00000001002e8ee9	xorps	%xmm0, %xmm0
00000001002e8eec	cvtsi2ss	%eax, %xmm0
00000001002e8ef0	movss	0x10(%r13), %xmm1
00000001002e8ef6	mulss	0x50fe632(%rip), %xmm1
00000001002e8efe	addss	%xmm0, %xmm1
00000001002e8f02	movss	%xmm1, 0x8(%r13)
00000001002e8f08	cvttss2si	-0x2c(%rbp), %ecx
00000001002e8f0d	leaq	0x550f95e(%rip), %rsi           ## literal pool for: "y"
00000001002e8f14	movq	%r12, %rdi
00000001002e8f17	movl	%ecx, %edx
00000001002e8f19	callq	__ZNK8CXMLNode19getSignedParamApplyEPKcii ## CXMLNode::getSignedParamApply(char const*, int, int) const
00000001002e8f1e	xorps	%xmm0, %xmm0
00000001002e8f21	cvtsi2ss	%eax, %xmm0
00000001002e8f25	movss	0x50fe603(%rip), %xmm1
00000001002e8f2d	mulss	0x14(%r13), %xmm1
00000001002e8f33	addss	%xmm0, %xmm1
00000001002e8f37	movaps	%xmm1, %xmm0
00000001002e8f3a	movss	%xmm0, 0xc(%r13)
00000001002e8f40	leaq	0x5529803(%rip), %rsi           ## literal pool for: "minwidth"
00000001002e8f47	movl	$working_state.free_in_buffer, %edx
00000001002e8f4c	movq	%r15, %rdi
00000001002e8f4f	xorl	%ecx, %ecx
00000001002e8f51	callq	__ZNK8CXMLNode11getIntParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEEi ## CXMLNode::getIntParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>, int) const
00000001002e8f56	xorps	%xmm0, %xmm0
00000001002e8f59	cvtsi2ss	%eax, %xmm0
00000001002e8f5d	movss	%xmm0, FGData.grain_scale_shift(%r13)
00000001002e8f66	leaq	0x55297e6(%rip), %rsi           ## literal pool for: "maxwidth"
00000001002e8f6d	movl	$working_state.free_in_buffer, %edx
00000001002e8f72	movq	%r15, %rdi
00000001002e8f75	xorl	%ecx, %ecx
00000001002e8f77	callq	__ZNK8CXMLNode11getIntParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEEi ## CXMLNode::getIntParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>, int) const
00000001002e8f7c	xorps	%xmm0, %xmm0
00000001002e8f7f	cvtsi2ss	%eax, %xmm0
00000001002e8f83	movss	%xmm0, FGData.uv_mult(%r13)
00000001002e8f8c	movzbl	0x28(%r13), %ecx
00000001002e8f91	leaq	0x55297c4(%rip), %rsi           ## literal pool for: "canstretch"
00000001002e8f98	movl	$0xa, %edx
00000001002e8f9d	movq	%r15, %rdi
00000001002e8fa0	callq	__ZNK8CXMLNode12getBoolParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEEb ## CXMLNode::getBoolParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>, bool) const
00000001002e8fa5	movb	%al, 0x28(%r13)
00000001002e8fa9	movups	0x8(%r13), %xmm0
00000001002e8fae	movups	%xmm0, 0x18(%r13)
00000001002e8fb3	leaq	0x55297ad(%rip), %rsi           ## literal pool for: "tooltip"
00000001002e8fba	movl	$0x7, %edx
00000001002e8fbf	movq	%r15, %rdi
00000001002e8fc2	callq	__ZNK8CXMLNode8hasParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEE ## CXMLNode::hasParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>) const
00000001002e8fc7	leaq	0x5529799(%rip), %rsi           ## literal pool for: "tooltip"
00000001002e8fce	movl	$0x7, %edx
00000001002e8fd3	movq	%r15, %rdi
00000001002e8fd6	testb	%al, %al
00000001002e8fd8	je	0x1002e8ffc
00000001002e8fda	callq	__ZNK8CXMLNode8getParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEE ## CXMLNode::getParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>) const
00000001002e8fdf	leaq	0x58(%r13), %rbx
00000001002e8fe3	movq	%rbx, %rdi
00000001002e8fe6	movq	%rax, %rsi
00000001002e8fe9	callq	0x1052c2e50                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
00000001002e8fee	movzbl	0x58(%r13), %eax
00000001002e8ff3	testb	$0x1, %al
00000001002e8ff5	jne	0x1002e9038
00000001002e8ff7	shrq	%rax
00000001002e8ffa	jmp	0x1002e903c
00000001002e8ffc	callq	__ZNK8CXMLNode8getChildENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEE ## CXMLNode::getChild(std::__1::basic_string_view<char, std::__1::char_traits<char>>) const
00000001002e9001	testq	%rax, %rax
00000001002e9004	je	0x1002e9046
00000001002e9006	leaq	0x552975a(%rip), %rsi           ## literal pool for: "tooltip"
00000001002e900d	movl	$0x7, %edx
00000001002e9012	movq	%r15, %rdi
00000001002e9015	callq	__ZNK8CXMLNode8getChildENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEE ## CXMLNode::getChild(std::__1::basic_string_view<char, std::__1::char_traits<char>>) const
00000001002e901a	leaq	0x48(%rax), %rsi
00000001002e901e	leaq	0x58(%r13), %rbx
00000001002e9022	movq	%rbx, %rdi
00000001002e9025	callq	0x1052c2e50                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
00000001002e902a	movzbl	0x58(%r13), %eax
00000001002e902f	testb	$0x1, %al
00000001002e9031	jne	0x1002e9088
00000001002e9033	shrq	%rax
00000001002e9036	jmp	0x1002e908c
00000001002e9038	movq	0x60(%r13), %rax
00000001002e903c	testq	%rax, %rax
00000001002e903f	jne	0x1002e90a9
00000001002e9041	jmp	0x1002e90e4
00000001002e9046	leaq	0x5529722(%rip), %rsi           ## literal pool for: "tooltipaction"
00000001002e904d	movl	$0xd, %edx
00000001002e9052	movq	%r15, %rdi
00000001002e9055	callq	__ZNK8CXMLNode8hasParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEE ## CXMLNode::hasParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>) const
00000001002e905a	testb	%al, %al
00000001002e905c	je	0x1002e90e9
00000001002e9062	leaq	0x5529706(%rip), %rsi           ## literal pool for: "tooltipaction"
00000001002e9069	movl	$0xd, %edx
00000001002e906e	movq	%r15, %rdi
00000001002e9071	callq	__ZNK8CXMLNode8getParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEE ## CXMLNode::getParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>) const
00000001002e9076	testb	$0x1, VPX_ARCH_MIPS(%rax)
00000001002e9079	je	0x1002e95bf
00000001002e907f	movq	0x10(%rax), %rax
00000001002e9083	jmp	0x1002e95c2
00000001002e9088	movq	0x60(%r13), %rax
00000001002e908c	testq	%rax, %rax
00000001002e908f	jne	0x1002e90a9
00000001002e9091	leaq	0x55230db(%rip), %rsi           ## literal pool for: "localized"
00000001002e9098	movl	$0x9, %edx
00000001002e909d	movq	%r15, %rdi
00000001002e90a0	callq	__ZNK8CXMLNode8hasParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEE ## CXMLNode::hasParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>) const
00000001002e90a5	testb	%al, %al
00000001002e90a7	je	0x1002e90e4
00000001002e90a9	leaq	_messageEngine(%rip), %rsi
00000001002e90b0	leaq	-0x68(%rbp), %rdi
00000001002e90b4	movq	%rbx, %rdx
00000001002e90b7	movq	%r15, %rcx
00000001002e90ba	movl	$HAVE_SSE3, %r8d
00000001002e90c0	callq	__ZN14CMessageEngine12localizeSkinERKNSt3__112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEEP8CXMLNodeb ## CMessageEngine::localizeSkin(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, CXMLNode*, bool)
00000001002e90c5	testb	$0x1, VPX_ARCH_MIPS(%rbx)
00000001002e90c8	je	0x1002e90d3
00000001002e90ca	movq	0x68(%r13), %rdi
00000001002e90ce	callq	0x1052c300c                     ## symbol stub for: __ZdlPv
00000001002e90d3	movq	-0x58(%rbp), %rax
00000001002e90d7	movq	%rax, 0x10(%rbx)
00000001002e90db	movups	-0x68(%rbp), %xmm0
00000001002e90df	movups	%xmm0, VPX_ARCH_MIPS(%rbx)
00000001002e90e2	jmp	0x1002e90e9
00000001002e90e4	movb	$0x1, 0x44(%r13)
00000001002e90e9	leaq	0x58(%r13), %rdi
00000001002e90ed	leaq	0x550ea11(%rip), %rsi           ## literal pool for: "\\n"
00000001002e90f4	leaq	0x552556f(%rip), %rcx           ## literal pool for: "\n"
00000001002e90fb	movl	$0x2, %edx
00000001002e9100	movl	$HAVE_SSE3, %r8d
00000001002e9106	callq	__Z18strReplace_inplacePNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEENS_17basic_string_viewIcS2_EES8_ ## strReplace_inplace(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>*, std::__1::basic_string_view<char, std::__1::char_traits<char>>, std::__1::basic_string_view<char, std::__1::char_traits<char>>)
00000001002e910b	leaq	0x551bcf8(%rip), %rsi           ## literal pool for: "visibility"
00000001002e9112	movl	$0xa, %edx
00000001002e9117	movq	%r15, %rdi
00000001002e911a	callq	__ZNK8CXMLNode8getParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEE ## CXMLNode::getParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>) const
00000001002e911f	movzbl	VPX_ARCH_MIPS(%rax), %edx
00000001002e9122	testb	$0x1, %dl
00000001002e9125	jne	0x1002e9137
00000001002e9127	cmpb	$0x2, %dl
00000001002e912a	jb	0x1002e916f
00000001002e912c	movq	%rax, %rsi
00000001002e912f	incq	%rsi
00000001002e9132	shrq	%rdx
00000001002e9135	jmp	0x1002e9144
00000001002e9137	movq	0x8(%rax), %rdx
00000001002e913b	testq	%rdx, %rdx
00000001002e913e	je	0x1002e916f
00000001002e9140	movq	0x10(%rax), %rsi
00000001002e9144	xorl	%edi, %edi
00000001002e9146	movabsq	$0x3ff402000000000, %r8         ## imm = 0x3FF402000000000
00000001002e9150	movb	VPX_ARCH_MIPS(%rsi,%rdi), %cl
00000001002e9153	movl	$HAVE_SSE3, %ebx
00000001002e9158	shlq	%cl, %rbx
00000001002e915b	cmpb	$0x3f, %cl
00000001002e915e	ja	0x1002e9191
00000001002e9160	andq	%r8, %rbx
00000001002e9163	je	0x1002e9191
00000001002e9165	incq	%rdi
00000001002e9168	cmpq	%rdi, %rdx
00000001002e916b	jne	0x1002e9150
00000001002e916d	jmp	0x1002e91ae
00000001002e916f	leaq	0x5529611(%rip), %rsi           ## literal pool for: "novisibility"
00000001002e9176	movl	$0xc, %edx
00000001002e917b	movq	%r15, %rdi
00000001002e917e	callq	__ZNK8CXMLNode8getParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEE ## CXMLNode::getParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>) const
00000001002e9183	movzbl	VPX_ARCH_MIPS(%rax), %ecx
00000001002e9186	testb	$0x1, %cl
00000001002e9189	je	0x1002e91ea
00000001002e918b	movq	0x8(%rax), %rcx
00000001002e918f	jmp	0x1002e91ed
00000001002e9191	cmpq	$-0x1, %rdi
00000001002e9195	je	0x1002e91ae
00000001002e9197	movl	0x40(%r13), %edx
00000001002e919b	movl	$HAVE_SSE3, %edi
00000001002e91a0	movq	%rax, %rsi
00000001002e91a3	callq	__ZN11CSkinEngine12createActionEbRKNSt3__112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEEi ## CSkinEngine::createAction(bool, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, int)
00000001002e91a8	movq	%rax, 0x30(%r13)
00000001002e91ac	jmp	0x1002e9211
00000001002e91ae	leaq	0x55295c8(%rip), %rsi           ## literal pool for: "constant "
00000001002e91b5	leaq	-0x68(%rbp), %rbx
00000001002e91b9	movq	%rbx, %rdi
00000001002e91bc	movq	%rax, %rdx
00000001002e91bf	callq	0x1052c2fca                     ## symbol stub for: __ZNSt3__1plIcNS_11char_traitsIcEENS_9allocatorIcEEEENS_12basic_stringIT_T0_T1_EEPKS6_RKS9_
00000001002e91c4	movl	0x40(%r13), %edx
00000001002e91c8	movl	$HAVE_SSE3, %edi
00000001002e91cd	movq	%rbx, %rsi
00000001002e91d0	callq	__ZN11CSkinEngine12createActionEbRKNSt3__112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEEi ## CSkinEngine::createAction(bool, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, int)
00000001002e91d5	movq	%rax, 0x30(%r13)
00000001002e91d9	testb	$0x1, -0x68(%rbp)
00000001002e91dd	je	0x1002e9211
00000001002e91df	movq	-0x58(%rbp), %rdi
00000001002e91e3	callq	0x1052c300c                     ## symbol stub for: __ZdlPv
00000001002e91e8	jmp	0x1002e9211
00000001002e91ea	shrq	%rcx
00000001002e91ed	testq	%rcx, %rcx
00000001002e91f0	je	0x1002e9211
00000001002e91f2	movl	0x40(%r13), %edx
00000001002e91f6	movl	$HAVE_SSE3, %edi
00000001002e91fb	movq	%rax, %rsi
00000001002e91fe	callq	__ZN11CSkinEngine12createActionEbRKNSt3__112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEEi ## CSkinEngine::createAction(bool, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, int)
00000001002e9203	movq	%rax, 0x30(%r13)
00000001002e9207	testq	%rax, %rax
00000001002e920a	je	0x1002e9211
00000001002e920c	movb	$0x1, 0x2b(%r13)
00000001002e9211	leaq	0x552957c(%rip), %rsi           ## literal pool for: "clickthrough"
00000001002e9218	movl	$0xc, %edx
00000001002e921d	movq	%r15, %rdi
00000001002e9220	callq	__ZNK8CXMLNode8hasParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEE ## CXMLNode::hasParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>) const
00000001002e9225	testb	%al, %al
00000001002e9227	je	0x1002e9270
00000001002e9229	leaq	0x5529564(%rip), %rsi           ## literal pool for: "clickthrough"
00000001002e9230	leaq	0x552956a(%rip), %rcx           ## literal pool for: "pass"
00000001002e9237	movl	$0xc, %edx
00000001002e923c	movl	$FGData.num_y_points, %r8d
00000001002e9242	movq	%r15, %rdi
00000001002e9245	callq	__ZNK8CXMLNode7isParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEES4_ ## CXMLNode::isParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>, std::__1::basic_string_view<char, std::__1::char_traits<char>>) const
00000001002e924a	movl	$0xfffffffe, %ecx               ## imm = 0xFFFFFFFE
00000001002e924f	testb	%al, %al
00000001002e9251	jne	0x1002e926c
00000001002e9253	leaq	0x552953a(%rip), %rsi           ## literal pool for: "clickthrough"
00000001002e925a	movl	$0xc, %edx
00000001002e925f	movq	%r15, %rdi
00000001002e9262	xorl	%ecx, %ecx
00000001002e9264	callq	__ZNK8CXMLNode12getBoolParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEEb ## CXMLNode::getBoolParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>, bool) const
00000001002e9269	movzbl	%al, %ecx
00000001002e926c	movl	%ecx, 0x38(%r13)
00000001002e9270	leaq	0x552952f(%rip), %rsi           ## literal pool for: "panel"
00000001002e9277	leaq	0x552952e(%rip), %rcx           ## literal pool for: "pannel"
00000001002e927e	movl	$0x5, %edx
00000001002e9283	movl	$0x6, %r8d
00000001002e9289	movq	%r15, %rdi
00000001002e928c	callq	__ZNK8CXMLNode9getParam2ENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEES4_ ## CXMLNode::getParam2(std::__1::basic_string_view<char, std::__1::char_traits<char>>, std::__1::basic_string_view<char, std::__1::char_traits<char>>) const
00000001002e9291	movzbl	VPX_ARCH_MIPS(%rax), %ecx
00000001002e9294	testb	$0x1, %cl
00000001002e9297	je	0x1002e929f
00000001002e9299	movq	0x8(%rax), %rcx
00000001002e929d	jmp	0x1002e92a2
00000001002e929f	shrq	%rcx
00000001002e92a2	testq	%rcx, %rcx
00000001002e92a5	je	0x1002e92bf
00000001002e92a7	leaq	_skinEngine(%rip), %rdi
00000001002e92ae	movq	%rax, %rsi
00000001002e92b1	movl	$HAVE_SSE3, %edx
00000001002e92b6	callq	__ZN11CSkinEngine13getPanelIndexERKNSt3__112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEEb ## CSkinEngine::getPanelIndex(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, bool)
00000001002e92bb	movl	%eax, 0x3c(%r13)
00000001002e92bf	leaq	0x55294ed(%rip), %rsi           ## literal pool for: "mouserect"
00000001002e92c6	movl	$0x9, %edx
00000001002e92cb	movq	%r15, %rdi
00000001002e92ce	callq	__ZNK8CXMLNode8getChildENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEE ## CXMLNode::getChild(std::__1::basic_string_view<char, std::__1::char_traits<char>>) const
00000001002e92d3	testq	%rax, %rax
00000001002e92d6	je	0x1002e939f
00000001002e92dc	movq	%rax, %rbx
00000001002e92df	cvttss2si	0x8(%r13), %ecx
00000001002e92e5	leaq	0x550f584(%rip), %rsi           ## literal pool for: "x"
00000001002e92ec	movq	%rax, %rdi
00000001002e92ef	movl	%ecx, %edx
00000001002e92f1	callq	__ZNK8CXMLNode19getSignedParamApplyEPKcii ## CXMLNode::getSignedParamApply(char const*, int, int) const
00000001002e92f6	xorps	%xmm0, %xmm0
00000001002e92f9	cvtsi2ss	%eax, %xmm0
00000001002e92fd	subss	0x8(%r13), %xmm0
00000001002e9303	cvttss2si	%xmm0, %eax
00000001002e9307	movl	%eax, 0xa8(%r13)
00000001002e930e	cvttss2si	0xc(%r13), %ecx
00000001002e9314	leaq	0x550f557(%rip), %rsi           ## literal pool for: "y"
00000001002e931b	movq	%rbx, %rdi
00000001002e931e	movl	%ecx, %edx
00000001002e9320	callq	__ZNK8CXMLNode19getSignedParamApplyEPKcii ## CXMLNode::getSignedParamApply(char const*, int, int) const
00000001002e9325	xorps	%xmm0, %xmm0
00000001002e9328	cvtsi2ss	%eax, %xmm0
00000001002e932c	subss	0xc(%r13), %xmm0
00000001002e9332	cvttss2si	%xmm0, %eax
00000001002e9336	movl	%eax, 0xac(%r13)
00000001002e933d	cvttss2si	0x10(%r13), %ecx
00000001002e9343	leaq	0x550f52a(%rip), %rsi           ## literal pool for: "width"
00000001002e934a	movl	$0x5, %edx
00000001002e934f	movq	%rbx, %rdi
00000001002e9352	callq	__ZNK8CXMLNode11getIntParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEEi ## CXMLNode::getIntParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>, int) const
00000001002e9357	movl	%eax, FGData.ar_coeff_shift(%r13)
00000001002e935e	cvttss2si	0x14(%r13), %ecx
00000001002e9364	leaq	0x550f50f(%rip), %rsi           ## literal pool for: "height"
00000001002e936b	movl	$0x6, %edx
00000001002e9370	movq	%rbx, %rdi
00000001002e9373	callq	__ZNK8CXMLNode11getIntParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEEi ## CXMLNode::getIntParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>, int) const
00000001002e9378	movl	%eax, 0xb4(%r13)
00000001002e937f	movb	$0x1, %bl
00000001002e9381	cmpl	$0x0, FGData.ar_coeff_shift(%r13)
00000001002e9389	jne	0x1002e9481
00000001002e938f	movl	$0xffffffff, FGData.ar_coeff_shift(%r13) ## imm = 0xFFFFFFFF
00000001002e939a	jmp	0x1002e9481
00000001002e939f	leaq	0x5529417(%rip), %rsi           ## literal pool for: "mousecircle"
00000001002e93a6	movl	$0xb, %edx
00000001002e93ab	movq	%r15, %rdi
00000001002e93ae	callq	__ZNK8CXMLNode8getChildENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEE ## CXMLNode::getChild(std::__1::basic_string_view<char, std::__1::char_traits<char>>) const
00000001002e93b3	testq	%rax, %rax
00000001002e93b6	je	0x1002e94bd
00000001002e93bc	movq	%rax, %rbx
00000001002e93bf	movss	0x10(%r13), %xmm0
00000001002e93c5	mulss	0x50fd6a7(%rip), %xmm0
00000001002e93cd	addss	0x8(%r13), %xmm0
00000001002e93d3	cvttss2si	%xmm0, %ecx
00000001002e93d7	leaq	0x550f492(%rip), %rsi           ## literal pool for: "x"
00000001002e93de	movq	%rax, %rdi
00000001002e93e1	movl	%ecx, %edx
00000001002e93e3	callq	__ZNK8CXMLNode19getSignedParamApplyEPKcii ## CXMLNode::getSignedParamApply(char const*, int, int) const
00000001002e93e8	xorps	%xmm0, %xmm0
00000001002e93eb	cvtsi2ss	%eax, %xmm0
00000001002e93ef	subss	0x8(%r13), %xmm0
00000001002e93f5	cvttss2si	%xmm0, %eax
00000001002e93f9	movl	%eax, 0xa8(%r13)
00000001002e9400	movss	0x14(%r13), %xmm0
00000001002e9406	mulss	0x50fd666(%rip), %xmm0
00000001002e940e	addss	0xc(%r13), %xmm0
00000001002e9414	cvttss2si	%xmm0, %ecx
00000001002e9418	leaq	0x550f453(%rip), %rsi           ## literal pool for: "y"
00000001002e941f	movq	%rbx, %rdi
00000001002e9422	movl	%ecx, %edx
00000001002e9424	callq	__ZNK8CXMLNode19getSignedParamApplyEPKcii ## CXMLNode::getSignedParamApply(char const*, int, int) const
00000001002e9429	xorps	%xmm0, %xmm0
00000001002e942c	cvtsi2ss	%eax, %xmm0
00000001002e9430	subss	0xc(%r13), %xmm0
00000001002e9436	cvttss2si	%xmm0, %eax
00000001002e943a	movl	%eax, 0xac(%r13)
00000001002e9441	movss	0x14(%r13), %xmm0
00000001002e9447	minss	0x10(%r13), %xmm0
00000001002e944d	mulss	0x50fd61f(%rip), %xmm0
00000001002e9455	cvttss2si	%xmm0, %ecx
00000001002e9459	leaq	0x550e7ef(%rip), %rsi           ## literal pool for: "r"
00000001002e9460	movl	$HAVE_SSE3, %edx
00000001002e9465	movq	%rbx, %rdi
00000001002e9468	callq	__ZNK8CXMLNode11getIntParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEEi ## CXMLNode::getIntParam(std::__1::basic_string_view<char, std::__1::char_traits<char>>, int) const
00000001002e946d	movl	%eax, FGData.ar_coeff_shift(%r13)
00000001002e9474	movl	$0xfffffb2e, 0xb4(%r13)         ## imm = 0xFFFFFB2E
00000001002e947f	movb	$0x1, %bl
00000001002e9481	movl	%ebx, %eax
00000001002e9483	addq	$0x58, %rsp
00000001002e9487	popq	%rbx
00000001002e9488	popq	%r12
00000001002e948a	popq	%r13
00000001002e948c	popq	%r14
00000001002e948e	popq	%r15
00000001002e9490	popq	%rbp
00000001002e9491	retq
00000001002e9492	movq	%r15, %rdi
00000001002e9495	movl	%ecx, %edx
00000001002e9497	callq	__ZNK8CXMLNode19getSignedParamApplyEPKcii ## CXMLNode::getSignedParamApply(char const*, int, int) const
00000001002e949c	xorps	%xmm0, %xmm0
00000001002e949f	cvtsi2ss	%eax, %xmm0
00000001002e94a3	movss	%xmm0, 0x8(%r13)
00000001002e94a9	cvttss2si	-0x2c(%rbp), %ecx
00000001002e94ae	leaq	0x550f3bd(%rip), %rsi           ## literal pool for: "y"
00000001002e94b5	movq	%r15, %rdi
00000001002e94b8	jmp	0x1002e8e80
00000001002e94bd	leaq	0x5529305(%rip), %rsi           ## literal pool for: "mousemask"
00000001002e94c4	movl	$0x9, %edx
00000001002e94c9	movq	%r15, %rdi
00000001002e94cc	callq	__ZNK8CXMLNode8getChildENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEE ## CXMLNode::getChild(std::__1::basic_string_view<char, std::__1::char_traits<char>>) const
00000001002e94d1	testq	%rax, %rax
00000001002e94d4	je	0x1002e9579
00000001002e94da	movq	%rax, %r14
00000001002e94dd	movq	-0x38(%rbp), %rax
00000001002e94e1	testq	%rax, %rax
00000001002e94e4	je	0x1002e947f
00000001002e94e6	cmpq	$0x0, 0x28(%rax)
00000001002e94eb	je	0x1002e947f
00000001002e94ed	cvttss2si	0x20(%r13), %eax
00000001002e94f3	movq	%rax, -0x50(%rbp)
00000001002e94f7	cvttss2si	0x24(%r13), %eax
00000001002e94fd	movq	%rax, -0x78(%rbp)
00000001002e9501	cvttss2si	0x8(%r13), %ecx
00000001002e9507	leaq	0x550f362(%rip), %rsi           ## literal pool for: "x"
00000001002e950e	movq	%r14, %rdi
00000001002e9511	movl	%ecx, %edx
00000001002e9513	callq	__ZNK8CXMLNode19getSignedParamApplyEPKcii ## CXMLNode::getSignedParamApply(char const*, int, int) const
00000001002e9518	movl	%eax, %r15d
00000001002e951b	cvttss2si	0xc(%r13), %ecx
00000001002e9521	leaq	0x550f34a(%rip), %rsi           ## literal pool for: "y"
00000001002e9528	movq	%r14, %rdi
00000001002e952b	movl	%ecx, %edx
00000001002e952d	callq	__ZNK8CXMLNode19getSignedParamApplyEPKcii ## CXMLNode::getSignedParamApply(char const*, int, int) const
00000001002e9532	xorl	%ebx, %ebx
00000001002e9534	movq	%r15, -0x48(%rbp)
00000001002e9538	testl	%r15d, %r15d
00000001002e953b	js	0x1002e9481
00000001002e9541	movl	%eax, %r12d
00000001002e9544	testl	%eax, %eax
00000001002e9546	movq	-0x38(%rbp), %rcx
00000001002e954a	js	0x1002e9481
00000001002e9550	movq	-0x50(%rbp), %rdx
00000001002e9554	movq	-0x48(%rbp), %rax
00000001002e9558	addl	%edx, %eax
00000001002e955a	cmpl	VPX_ARCH_MIPS(%rcx), %eax
00000001002e955c	jg	0x1002e9572
00000001002e955e	movq	%rcx, %rbx
00000001002e9561	movq	-0x78(%rbp), %r15
00000001002e9565	leal	VPX_ARCH_MIPS(%r12,%r15), %eax
00000001002e9569	cmpl	0x4(%rcx), %eax
00000001002e956c	jle	0x1002e9600
00000001002e9572	xorl	%ebx, %ebx
00000001002e9574	jmp	0x1002e9481
00000001002e9579	movb	$0x1, %bl
00000001002e957b	cmpl	$0x320, _skinVersion(%rip)      ## imm = 0x320
00000001002e9585	jl	0x1002e9481
00000001002e958b	leaq	0x551893a(%rip), %rsi           ## literal pool for: "clipmask"
00000001002e9592	movl	$working_state.free_in_buffer, %edx
00000001002e9597	movq	%r15, %rdi
00000001002e959a	callq	__ZNK8CXMLNode8getChildENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEE ## CXMLNode::getChild(std::__1::basic_string_view<char, std::__1::char_traits<char>>) const
00000001002e959f	cmpq	$0x0, -0x38(%rbp)
00000001002e95a4	je	0x1002e9481
00000001002e95aa	movq	%rax, %r14
00000001002e95ad	testq	%rax, %rax
00000001002e95b0	movq	-0x38(%rbp), %rax
00000001002e95b4	jne	0x1002e94e6
00000001002e95ba	jmp	0x1002e9481
00000001002e95bf	incq	%rax
00000001002e95c2	leaq	_messageEngine(%rip), %rdi
00000001002e95c9	leaq	0x5518047(%rip), %rsi           ## literal pool for: "tooltips"
00000001002e95d0	movq	%rax, %rdx
00000001002e95d3	callq	__ZN14CMessageEngine18getMessageExistingEPKcS1_ ## CMessageEngine::getMessageExisting(char const*, char const*)
00000001002e95d8	testq	%rax, %rax
00000001002e95db	je	0x1002e90e9
00000001002e95e1	movq	%rax, %rbx
00000001002e95e4	movq	%rax, %rdi
00000001002e95e7	callq	0x1052c3b0a                     ## symbol stub for: _strlen
00000001002e95ec	leaq	0x58(%r13), %rdi
00000001002e95f0	movq	%rbx, %rsi
00000001002e95f3	movq	%rax, %rdx
00000001002e95f6	callq	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE17__assign_externalEPKcm ## std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>::__assign_external(char const*, unsigned long)
00000001002e95fb	jmp	0x1002e90e9
00000001002e9600	leal	0x7(%rdx), %eax
00000001002e9603	leal	0xe(%rdx), %ecx
00000001002e9606	testl	%eax, %eax
00000001002e9608	cmovnsl	%eax, %ecx
00000001002e960b	sarl	$0x3, %ecx
00000001002e960e	movl	%ecx, -0x3c(%rbp)
00000001002e9611	movl	%ecx, %eax
00000001002e9613	imull	%r15d, %eax
00000001002e9617	movslq	%eax, %r14
00000001002e961a	movl	$HAVE_SSE3, %esi
00000001002e961f	movq	%r14, %rdi
00000001002e9622	callq	0x1052c3192                     ## symbol stub for: _calloc
00000001002e9627	movq	%rax, 0xa0(%r13)
00000001002e962e	movq	%rbx, %rdi
00000001002e9631	movq	-0x48(%rbp), %rsi
00000001002e9635	movl	%r12d, %edx
00000001002e9638	callq	__ZN6CImage8getPixelEii         ## CImage::getPixel(int, int)
00000001002e963d	testl	%r15d, %r15d
00000001002e9640	jle	0x1002e947f
00000001002e9646	movq	%r14, -0x70(%rbp)
00000001002e964a	shrl	$0x18, %eax
00000001002e964d	movq	-0x50(%rbp), %r11
00000001002e9651	movl	%r11d, %r14d
00000001002e9654	xorl	%edx, %edx
00000001002e9656	xorl	%r8d, %r8d
00000001002e9659	testl	%r11d, %r11d
00000001002e965c	jle	0x1002e96d4
00000001002e965e	movq	-0x38(%rbp), %rdi
00000001002e9662	movq	0x28(%rdi), %rcx
00000001002e9666	leal	VPX_ARCH_MIPS(%rdx,%r12), %esi
00000001002e966a	imull	VPX_ARCH_MIPS(%rdi), %esi
00000001002e966d	addl	-0x48(%rbp), %esi
00000001002e9670	movslq	%esi, %rsi
00000001002e9673	movl	%edx, %r9d
00000001002e9676	imull	-0x3c(%rbp), %r9d
00000001002e967b	leaq	VPX_ARCH_MIPS(%rcx,%rsi,4), %rsi
00000001002e967f	addq	$0x3, %rsi
00000001002e9683	xorl	%ebx, %ebx
00000001002e9685	movzbl	VPX_ARCH_MIPS(%rsi,%rbx,4), %ecx
00000001002e9689	cmpl	%ecx, %eax
00000001002e968b	jne	0x1002e96ce
00000001002e968d	cmpb	$0x6, -0x1(%rsi,%rbx,4)
00000001002e9692	jb	0x1002e96c4
00000001002e9694	cmpb	$0x6, -0x3(%rsi,%rbx,4)
00000001002e9699	jb	0x1002e96c4
00000001002e969b	cmpb	$0x6, -0x2(%rsi,%rbx,4)
00000001002e96a0	jb	0x1002e96c4
00000001002e96a2	movl	%ebx, %ecx
00000001002e96a4	andb	$0x7, %cl
00000001002e96a7	movl	$HAVE_SSE3, %edi
00000001002e96ac	shll	%cl, %edi
00000001002e96ae	movq	0xa0(%r13), %r10
00000001002e96b5	movl	%ebx, %ecx
00000001002e96b7	shrl	$0x3, %ecx
00000001002e96ba	addl	%r9d, %ecx
00000001002e96bd	movslq	%ecx, %rcx
00000001002e96c0	orb	%dil, VPX_ARCH_MIPS(%r10,%rcx)
00000001002e96c4	incq	%rbx
00000001002e96c7	cmpl	%ebx, %r14d
00000001002e96ca	jne	0x1002e9685
00000001002e96cc	jmp	0x1002e96d4
00000001002e96ce	movb	$0x1, %r8b
00000001002e96d1	movl	%r15d, %edx
00000001002e96d4	incl	%edx
00000001002e96d6	cmpl	%r15d, %edx
00000001002e96d9	jl	0x1002e9659
00000001002e96df	testb	$0x1, %r8b
00000001002e96e3	je	0x1002e947f
00000001002e96e9	movq	0xa0(%r13), %rdi
00000001002e96f0	movq	-0x70(%rbp), %rsi
00000001002e96f4	callq	0x1052c3030                     ## symbol stub for: ___bzero
00000001002e96f9	movq	-0x50(%rbp), %r9
00000001002e96fd	xorl	%r8d, %r8d
00000001002e9700	testl	%r9d, %r9d
00000001002e9703	jle	0x1002e9757
00000001002e9705	movq	-0x38(%rbp), %rax
00000001002e9709	movq	0x28(%rax), %rcx
00000001002e970d	movl	%r8d, %edx
00000001002e9710	imull	-0x3c(%rbp), %edx
00000001002e9714	movl	VPX_ARCH_MIPS(%rax), %esi
00000001002e9716	imull	%r12d, %esi
00000001002e971a	addl	-0x48(%rbp), %esi
00000001002e971d	movslq	%esi, %rsi
00000001002e9720	leaq	VPX_ARCH_MIPS(%rcx,%rsi,4), %rsi
00000001002e9724	addq	$0x3, %rsi
00000001002e9728	xorl	%edi, %edi
00000001002e972a	cmpb	$0x0, VPX_ARCH_MIPS(%rsi,%rdi,4)
00000001002e972e	js	0x1002e974f
00000001002e9730	movl	%edi, %ecx
00000001002e9732	andb	$0x7, %cl
00000001002e9735	movl	$HAVE_SSE3, %ebx
00000001002e973a	shll	%cl, %ebx
00000001002e973c	movq	0xa0(%r13), %rcx
00000001002e9743	movl	%edi, %eax
00000001002e9745	shrl	$0x3, %eax
00000001002e9748	addl	%edx, %eax
00000001002e974a	cltq
00000001002e974c	orb	%bl, VPX_ARCH_MIPS(%rcx,%rax)
00000001002e974f	incq	%rdi
00000001002e9752	cmpl	%edi, %r14d
00000001002e9755	jne	0x1002e972a
00000001002e9757	incl	%r8d
00000001002e975a	incl	%r12d
00000001002e975d	cmpl	%r15d, %r8d
00000001002e9760	jne	0x1002e9700
00000001002e9762	jmp	0x1002e947f
00000001002e9767	movq	%rax, %rbx
00000001002e976a	testb	$0x1, -0x68(%rbp)
00000001002e976e	je	0x1002e9779
00000001002e9770	movq	-0x58(%rbp), %rdi
00000001002e9774	callq	0x1052c300c                     ## symbol stub for: __ZdlPv
00000001002e9779	movq	%rbx, %rdi
00000001002e977c	callq	0x1052c2d5a                     ## symbol stub for: __Unwind_Resume
00000001002e9781	nop
