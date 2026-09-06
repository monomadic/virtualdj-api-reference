__ZN11ISkinObject4loadEP8CXMLNodeP6CImage:
00000001001c6e6e	pushq	%rbp
00000001001c6e6f	movq	%rsp, %rbp
00000001001c6e72	pushq	%r15
00000001001c6e74	pushq	%r14
00000001001c6e76	pushq	%r13
00000001001c6e78	pushq	%r12
00000001001c6e7a	pushq	%rbx
00000001001c6e7b	subq	$0x68, %rsp
00000001001c6e7f	movq	%rdx, -0x30(%rbp)
00000001001c6e83	movq	%rsi, %r15
00000001001c6e86	movq	%rdi, %r12
00000001001c6e89	leaq	0x1d392ee(%rip), %rsi           ## literal pool for: "deck"
00000001001c6e90	movl	$0x4, %edx
00000001001c6e95	movq	%r15, %rdi
00000001001c6e98	callq	__ZNK8CXMLNode8hasParamEPKci    ## CXMLNode::hasParam(char const*, int) const
00000001001c6e9d	testb	%al, %al
00000001001c6e9f	je	0x1001c6eaa
00000001001c6ea1	leaq	0x1d392d6(%rip), %rsi           ## literal pool for: "deck"
00000001001c6ea8	jmp	0x1001c6ec9
00000001001c6eaa	leaq	0x1d3a299(%rip), %rsi           ## literal pool for: "chan"
00000001001c6eb1	movl	$0x4, %edx
00000001001c6eb6	movq	%r15, %rdi
00000001001c6eb9	callq	__ZNK8CXMLNode8hasParamEPKci    ## CXMLNode::hasParam(char const*, int) const
00000001001c6ebe	testb	%al, %al
00000001001c6ec0	je	0x1001c6ee8
00000001001c6ec2	leaq	0x1d3a281(%rip), %rsi           ## literal pool for: "chan"
00000001001c6ec9	movl	$0x4, %edx
00000001001c6ece	movq	%r15, %rdi
00000001001c6ed1	callq	__ZN8CXMLNode8getParamEPKcm     ## CXMLNode::getParam(char const*, unsigned long)
00000001001c6ed6	leaq	0x44(%r12), %rbx
00000001001c6edb	movq	%rax, %rdi
00000001001c6ede	movq	%rbx, %rsi
00000001001c6ee1	callq	__ZN7IAction17getDeckFromStringERKNSt3__112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEERj ## IAction::getDeckFromString(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, unsigned int&)
00000001001c6ee6	jmp	0x1001c6eed
00000001001c6ee8	leaq	0x44(%r12), %rbx
00000001001c6eed	movq	%rbx, -0x40(%rbp)
00000001001c6ef1	movl	CONFIG_BETTER_HW_COMPATIBILITY(%rbx), %esi
00000001001c6ef3	movq	%r15, %rdi
00000001001c6ef6	callq	__ZN10CSkinClass5applyEP8CXMLNodej ## CSkinClass::apply(CXMLNode*, unsigned int)
00000001001c6efb	leaq	0x1d3a339(%rip), %rdx           ## literal pool for: "size"
00000001001c6f02	movq	%r15, %rsi
00000001001c6f05	callq	__ZN11ISkinObject12getConditionEP8CXMLNodePKc ## ISkinObject::getCondition(CXMLNode*, char const*)
00000001001c6f0a	movq	%rax, %rbx
00000001001c6f0d	leaq	0x1d38eb5(%rip), %rdx           ## literal pool for: "pos"
00000001001c6f14	movq	%r15, %rsi
00000001001c6f17	callq	__ZN11ISkinObject12getConditionEP8CXMLNodePKc ## ISkinObject::getCondition(CXMLNode*, char const*)
00000001001c6f1c	movq	%rax, %r14
00000001001c6f1f	leaq	0x1d3a34b(%rip), %rsi           ## literal pool for: "center"
00000001001c6f26	movl	$0x6, %edx
00000001001c6f2b	movq	%r15, %rdi
00000001001c6f2e	callq	__ZNK8CXMLNode8getChildEPKci    ## CXMLNode::getChild(char const*, int) const
00000001001c6f33	movq	%rax, %r13
00000001001c6f36	leaq	0x1d3a26d(%rip), %rsi           ## literal pool for: "width"
00000001001c6f3d	movl	$0x5, %edx
00000001001c6f42	xorl	%ecx, %ecx
00000001001c6f44	testq	%rbx, %rbx
00000001001c6f47	je	0x1001c6f6f
00000001001c6f49	movq	%rbx, %rdi
00000001001c6f4c	callq	__ZNK8CXMLNode13getIntParamNSEPKcii ## CXMLNode::getIntParamNS(char const*, int, int) const
00000001001c6f51	cvtsi2ss	%eax, %xmm0
00000001001c6f55	movss	%xmm0, 0x10(%r12)
00000001001c6f5c	leaq	0x1d3a23b(%rip), %rsi           ## literal pool for: "height"
00000001001c6f63	movl	$0x6, %edx
00000001001c6f68	xorl	%ecx, %ecx
00000001001c6f6a	movq	%rbx, %rdi
00000001001c6f6d	jmp	0x1001c6fbe
00000001001c6f6f	testq	%r14, %r14
00000001001c6f72	je	0x1001c6f9a
00000001001c6f74	movq	%r14, %rdi
00000001001c6f77	callq	__ZNK8CXMLNode13getIntParamNSEPKcii ## CXMLNode::getIntParamNS(char const*, int, int) const
00000001001c6f7c	cvtsi2ss	%eax, %xmm0
00000001001c6f80	movss	%xmm0, 0x10(%r12)
00000001001c6f87	leaq	0x1d3a210(%rip), %rsi           ## literal pool for: "height"
00000001001c6f8e	movl	$0x6, %edx
00000001001c6f93	xorl	%ecx, %ecx
00000001001c6f95	movq	%r14, %rdi
00000001001c6f98	jmp	0x1001c6fbe
00000001001c6f9a	movq	%r15, %rdi
00000001001c6f9d	callq	__ZNK8CXMLNode13getIntParamNSEPKcii ## CXMLNode::getIntParamNS(char const*, int, int) const
00000001001c6fa2	cvtsi2ss	%eax, %xmm0
00000001001c6fa6	movss	%xmm0, 0x10(%r12)
00000001001c6fad	leaq	0x1d3a1ea(%rip), %rsi           ## literal pool for: "height"
00000001001c6fb4	movl	$0x6, %edx
00000001001c6fb9	xorl	%ecx, %ecx
00000001001c6fbb	movq	%r15, %rdi
00000001001c6fbe	callq	__ZNK8CXMLNode13getIntParamNSEPKcii ## CXMLNode::getIntParamNS(char const*, int, int) const
00000001001c6fc3	xorps	%xmm0, %xmm0
00000001001c6fc6	cvtsi2ss	%eax, %xmm0
00000001001c6fca	movss	%xmm0, 0x14(%r12)
00000001001c6fd1	leaq	-0x48(%rbp), %rdi
00000001001c6fd5	leaq	-0x34(%rbp), %rsi
00000001001c6fd9	callq	__ZN10CSkinPanel20getParentCoordinatesERfS0_ ## CSkinPanel::getParentCoordinates(float&, float&)
00000001001c6fde	testq	%r14, %r14
00000001001c6fe1	je	0x1001c7026
00000001001c6fe3	cvttss2si	-0x48(%rbp), %edx
00000001001c6fe8	leaq	0x1d3b160(%rip), %rsi           ## literal pool for: "x"
00000001001c6fef	movq	%r14, %rdi
00000001001c6ff2	movl	%edx, %ecx
00000001001c6ff4	callq	__ZNK8CXMLNode19getSignedParamApplyEPKcii ## CXMLNode::getSignedParamApply(char const*, int, int) const
00000001001c6ff9	xorps	%xmm0, %xmm0
00000001001c6ffc	cvtsi2ss	%eax, %xmm0
00000001001c7000	movss	%xmm0, 0x8(%r12)
00000001001c7007	cvttss2si	-0x34(%rbp), %edx
00000001001c700c	leaq	0x1d3a189(%rip), %rsi           ## literal pool for: "y"
00000001001c7013	movq	%r14, %rdi
00000001001c7016	movl	%edx, %ecx
00000001001c7018	callq	__ZNK8CXMLNode19getSignedParamApplyEPKcii ## CXMLNode::getSignedParamApply(char const*, int, int) const
00000001001c701d	xorps	%xmm0, %xmm0
00000001001c7020	cvtsi2ss	%eax, %xmm0
00000001001c7024	jmp	0x1001c7096
00000001001c7026	cvttss2si	-0x48(%rbp), %edx
00000001001c702b	leaq	0x1d3b11d(%rip), %rsi           ## literal pool for: "x"
00000001001c7032	testq	%r13, %r13
00000001001c7035	je	0x1001c7694
00000001001c703b	movq	%r13, %rdi
00000001001c703e	movl	%edx, %ecx
00000001001c7040	callq	__ZNK8CXMLNode19getSignedParamApplyEPKcii ## CXMLNode::getSignedParamApply(char const*, int, int) const
00000001001c7045	xorps	%xmm0, %xmm0
00000001001c7048	cvtsi2ss	%eax, %xmm0
00000001001c704c	movss	0x10(%r12), %xmm1
00000001001c7053	mulss	0x19998f5(%rip), %xmm1
00000001001c705b	subss	%xmm1, %xmm0
00000001001c705f	movss	%xmm0, 0x8(%r12)
00000001001c7066	cvttss2si	-0x34(%rbp), %edx
00000001001c706b	leaq	0x1d3a12a(%rip), %rsi           ## literal pool for: "y"
00000001001c7072	movq	%r13, %rdi
00000001001c7075	movl	%edx, %ecx
00000001001c7077	callq	__ZNK8CXMLNode19getSignedParamApplyEPKcii ## CXMLNode::getSignedParamApply(char const*, int, int) const
00000001001c707c	xorps	%xmm0, %xmm0
00000001001c707f	cvtsi2ss	%eax, %xmm0
00000001001c7083	movss	0x19998c5(%rip), %xmm1
00000001001c708b	mulss	0x14(%r12), %xmm1
00000001001c7092	subss	%xmm1, %xmm0
00000001001c7096	movss	%xmm0, 0xc(%r12)
00000001001c709d	leaq	0x1d42557(%rip), %rsi           ## literal pool for: "minwidth"
00000001001c70a4	movl	$0x8, %edx
00000001001c70a9	xorl	%ecx, %ecx
00000001001c70ab	movq	%r15, %rdi
00000001001c70ae	callq	__ZNK8CXMLNode13getIntParamNSEPKcii ## CXMLNode::getIntParamNS(char const*, int, int) const
00000001001c70b3	xorps	%xmm0, %xmm0
00000001001c70b6	cvtsi2ss	%eax, %xmm0
00000001001c70ba	movss	%xmm0, 0xc8(%r12)
00000001001c70c4	leaq	0x1d42539(%rip), %rsi           ## literal pool for: "maxwidth"
00000001001c70cb	movl	$0x8, %edx
00000001001c70d0	xorl	%ecx, %ecx
00000001001c70d2	movq	%r15, %rdi
00000001001c70d5	callq	__ZNK8CXMLNode13getIntParamNSEPKcii ## CXMLNode::getIntParamNS(char const*, int, int) const
00000001001c70da	xorps	%xmm0, %xmm0
00000001001c70dd	cvtsi2ss	%eax, %xmm0
00000001001c70e1	movss	%xmm0, 0xcc(%r12)
00000001001c70eb	movzbl	0x28(%r12), %ecx
00000001001c70f1	leaq	0x1d42515(%rip), %rsi           ## literal pool for: "canstretch"
00000001001c70f8	movl	$0xa, %edx
00000001001c70fd	movq	%r15, %rdi
00000001001c7100	callq	__ZNK8CXMLNode14getBoolParamNSEPKcib ## CXMLNode::getBoolParamNS(char const*, int, bool) const
00000001001c7105	movb	%al, 0x28(%r12)
00000001001c710a	movq	0x8(%r12), %rax
00000001001c710f	movq	0x10(%r12), %rcx
00000001001c7114	movq	%rax, 0x18(%r12)
00000001001c7119	movq	%rcx, 0x20(%r12)
00000001001c711e	leaq	0x1d424f3(%rip), %rsi           ## literal pool for: "tooltip"
00000001001c7125	movl	$0x7, %edx
00000001001c712a	movq	%r15, %rdi
00000001001c712d	callq	__ZNK8CXMLNode8hasParamEPKci    ## CXMLNode::hasParam(char const*, int) const
00000001001c7132	leaq	0x1d424df(%rip), %rsi           ## literal pool for: "tooltip"
00000001001c7139	testb	%al, %al
00000001001c713b	je	0x1001c7169
00000001001c713d	movl	$0x7, %edx
00000001001c7142	movq	%r15, %rdi
00000001001c7145	callq	__ZN8CXMLNode8getParamEPKcm     ## CXMLNode::getParam(char const*, unsigned long)
00000001001c714a	leaq	0x60(%r12), %rbx
00000001001c714f	movq	%rbx, %rdi
00000001001c7152	movq	%rax, %rsi
00000001001c7155	callq	0x101b5d706                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
00000001001c715a	movzbl	0x60(%r12), %eax
00000001001c7160	testb	$0x1, %al
00000001001c7162	jne	0x1001c719d
00000001001c7164	shrq	%rax
00000001001c7167	jmp	0x1001c71a2
00000001001c7169	movl	$0x7, %edx
00000001001c716e	movq	%r15, %rdi
00000001001c7171	callq	__ZNK8CXMLNode8getChildEPKci    ## CXMLNode::getChild(char const*, int) const
00000001001c7176	testq	%rax, %rax
00000001001c7179	je	0x1001c71b0
00000001001c717b	leaq	0x1d42496(%rip), %rsi           ## literal pool for: "tooltip"
00000001001c7182	movl	$0x7, %edx
00000001001c7187	movq	%r15, %rdi
00000001001c718a	callq	__ZNK8CXMLNode8getChildEPKci    ## CXMLNode::getChild(char const*, int) const
00000001001c718f	testq	%rax, %rax
00000001001c7192	jne	0x1001c71ed
00000001001c7194	leaq	_emptyString(%rip), %rax
00000001001c719b	jmp	0x1001c71f1
00000001001c719d	movq	0x68(%r12), %rax
00000001001c71a2	testq	%rax, %rax
00000001001c71a5	jne	0x1001c7232
00000001001c71ab	jmp	0x1001c726d
00000001001c71b0	leaq	0x1d42469(%rip), %rsi           ## literal pool for: "tooltipaction"
00000001001c71b7	movl	$0xd, %edx
00000001001c71bc	movq	%r15, %rdi
00000001001c71bf	callq	__ZNK8CXMLNode8hasParamEPKci    ## CXMLNode::hasParam(char const*, int) const
00000001001c71c4	testb	%al, %al
00000001001c71c6	je	0x1001c7276
00000001001c71cc	leaq	0x1d4244d(%rip), %rsi           ## literal pool for: "tooltipaction"
00000001001c71d3	movq	%r15, %rdi
00000001001c71d6	callq	__ZNK8CXMLNode8getParamEPKc     ## CXMLNode::getParam(char const*) const
00000001001c71db	testb	$0x1, CONFIG_BETTER_HW_COMPATIBILITY(%rax)
00000001001c71de	je	0x1001c77ac
00000001001c71e4	movq	0x10(%rax), %rax
00000001001c71e8	jmp	0x1001c77af
00000001001c71ed	addq	$0x48, %rax
00000001001c71f1	leaq	0x60(%r12), %rbx
00000001001c71f6	movq	%rbx, %rdi
00000001001c71f9	movq	%rax, %rsi
00000001001c71fc	callq	0x101b5d706                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
00000001001c7201	movzbl	0x60(%r12), %eax
00000001001c7207	testb	$0x1, %al
00000001001c7209	jne	0x1001c7210
00000001001c720b	shrq	%rax
00000001001c720e	jmp	0x1001c7215
00000001001c7210	movq	0x68(%r12), %rax
00000001001c7215	testq	%rax, %rax
00000001001c7218	jne	0x1001c7232
00000001001c721a	leaq	0x1d42007(%rip), %rsi           ## literal pool for: "localized"
00000001001c7221	movl	$0x9, %edx
00000001001c7226	movq	%r15, %rdi
00000001001c7229	callq	__ZNK8CXMLNode8hasParamEPKci    ## CXMLNode::hasParam(char const*, int) const
00000001001c722e	testb	%al, %al
00000001001c7230	je	0x1001c726d
00000001001c7232	leaq	_messageEngine(%rip), %rsi
00000001001c7239	leaq	-0x68(%rbp), %r14
00000001001c723d	movl	$CONFIG_ENCODERS, %r8d
00000001001c7243	movq	%r14, %rdi
00000001001c7246	movq	%rbx, %rdx
00000001001c7249	movq	%r15, %rcx
00000001001c724c	callq	__ZN14CMessageEngine12localizeSkinERKNSt3__112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEEP8CXMLNodeb ## CMessageEngine::localizeSkin(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, CXMLNode*, bool)
00000001001c7251	movq	%rbx, %rdi
00000001001c7254	movq	%r14, %rsi
00000001001c7257	callq	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSEOS5_ ## std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>::operator=(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>&&)
00000001001c725c	testb	$0x1, CONFIG_BETTER_HW_COMPATIBILITY(%r14)
00000001001c7260	je	0x1001c7276
00000001001c7262	movq	-0x58(%rbp), %rdi
00000001001c7266	callq	0x101b5d868                     ## symbol stub for: __ZdlPv
00000001001c726b	jmp	0x1001c7276
00000001001c726d	movb	$0x1, 0xa8(%r12)
00000001001c7276	leaq	0x1d35eb6(%rip), %rsi           ## literal pool for: "\\n"
00000001001c727d	leaq	-0x68(%rbp), %rdi
00000001001c7281	callq	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEC1IDnEEPKc ## std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>::basic_string<std::nullptr_t>(char const*)
00000001001c7286	leaq	0x1d638d3(%rip), %rsi           ## literal pool for: "\n"
00000001001c728d	leaq	-0x88(%rbp), %rdi
00000001001c7294	callq	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEC1IDnEEPKc ## std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>::basic_string<std::nullptr_t>(char const*)
00000001001c7299	leaq	0x60(%r12), %rdi
00000001001c729e	leaq	-0x68(%rbp), %rsi
00000001001c72a2	leaq	-0x88(%rbp), %rdx
00000001001c72a9	callq	__Z18strReplace_inplacePNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEERKS5_S8_ ## strReplace_inplace(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>*, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&)
00000001001c72ae	testb	$0x1, -0x88(%rbp)
00000001001c72b5	je	0x1001c72c0
00000001001c72b7	movq	-0x78(%rbp), %rdi
00000001001c72bb	callq	0x101b5d868                     ## symbol stub for: __ZdlPv
00000001001c72c0	testb	$0x1, -0x68(%rbp)
00000001001c72c4	je	0x1001c72cf
00000001001c72c6	movq	-0x58(%rbp), %rdi
00000001001c72ca	callq	0x101b5d868                     ## symbol stub for: __ZdlPv
00000001001c72cf	leaq	0x1d3ba8b(%rip), %rsi           ## literal pool for: "visibility"
00000001001c72d6	movl	$0xa, %edx
00000001001c72db	movq	%r15, %rdi
00000001001c72de	callq	__ZN8CXMLNode8getParamEPKcm     ## CXMLNode::getParam(char const*, unsigned long)
00000001001c72e3	movzbl	CONFIG_BETTER_HW_COMPATIBILITY(%rax), %ecx
00000001001c72e6	movb	$0x1, %dl
00000001001c72e8	testb	%dl, %cl
00000001001c72ea	je	0x1001c72f2
00000001001c72ec	movq	0x8(%rax), %rdx
00000001001c72f0	jmp	0x1001c72f8
00000001001c72f2	movq	%rcx, %rdx
00000001001c72f5	shrq	%rdx
00000001001c72f8	testq	%rdx, %rdx
00000001001c72fb	je	0x1001c7308
00000001001c72fd	testb	$0x1, %cl
00000001001c7300	je	0x1001c7332
00000001001c7302	movq	0x10(%rax), %rsi
00000001001c7306	jmp	0x1001c7338
00000001001c7308	leaq	0x1d42329(%rip), %rsi           ## literal pool for: "novisibility"
00000001001c730f	movl	$0xc, %edx
00000001001c7314	movq	%r15, %rdi
00000001001c7317	callq	__ZN8CXMLNode8getParamEPKcm     ## CXMLNode::getParam(char const*, unsigned long)
00000001001c731c	movzbl	CONFIG_BETTER_HW_COMPATIBILITY(%rax), %ecx
00000001001c731f	movb	$0x1, %dl
00000001001c7321	testb	%dl, %cl
00000001001c7323	je	0x1001c73c1
00000001001c7329	movq	0x8(%rax), %rcx
00000001001c732d	jmp	0x1001c73c4
00000001001c7332	movq	%rax, %rsi
00000001001c7335	incq	%rsi
00000001001c7338	xorl	%edi, %edi
00000001001c733a	movabsq	$0x3ff402000000000, %r8         ## imm = 0x3FF402000000000
00000001001c7344	movb	CONFIG_BETTER_HW_COMPATIBILITY(%rsi,%rdi), %cl
00000001001c7347	movl	$CONFIG_ENCODERS, %ebx
00000001001c734c	shlq	%cl, %rbx
00000001001c734f	cmpb	$0x3f, %cl
00000001001c7352	ja	0x1001c7363
00000001001c7354	andq	%r8, %rbx
00000001001c7357	je	0x1001c7363
00000001001c7359	incq	%rdi
00000001001c735c	cmpq	%rdi, %rdx
00000001001c735f	jne	0x1001c7344
00000001001c7361	jmp	0x1001c7382
00000001001c7363	cmpq	$-0x1, %rdi
00000001001c7367	je	0x1001c7382
00000001001c7369	movl	0x44(%r12), %edx
00000001001c736e	movl	$CONFIG_ENCODERS, %edi
00000001001c7373	movq	%rax, %rsi
00000001001c7376	callq	__ZN11CSkinEngine12createActionEbRKNSt3__112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEEi ## CSkinEngine::createAction(bool, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, int)
00000001001c737b	movq	%rax, 0x30(%r12)
00000001001c7380	jmp	0x1001c73eb
00000001001c7382	leaq	0x1d422a5(%rip), %rsi           ## literal pool for: "constant "
00000001001c7389	leaq	-0x68(%rbp), %rbx
00000001001c738d	movq	%rbx, %rdi
00000001001c7390	movq	%rax, %rdx
00000001001c7393	callq	0x101b5d82c                     ## symbol stub for: __ZNSt3__1plIcNS_11char_traitsIcEENS_9allocatorIcEEEENS_12basic_stringIT_T0_T1_EEPKS6_RKS9_
00000001001c7398	movq	-0x40(%rbp), %rax
00000001001c739c	movl	CONFIG_BETTER_HW_COMPATIBILITY(%rax), %edx
00000001001c739e	movl	$CONFIG_ENCODERS, %edi
00000001001c73a3	movq	%rbx, %rsi
00000001001c73a6	callq	__ZN11CSkinEngine12createActionEbRKNSt3__112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEEi ## CSkinEngine::createAction(bool, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, int)
00000001001c73ab	movq	%rax, 0x30(%r12)
00000001001c73b0	testb	$0x1, -0x68(%rbp)
00000001001c73b4	je	0x1001c73eb
00000001001c73b6	movq	-0x58(%rbp), %rdi
00000001001c73ba	callq	0x101b5d868                     ## symbol stub for: __ZdlPv
00000001001c73bf	jmp	0x1001c73eb
00000001001c73c1	shrq	%rcx
00000001001c73c4	testq	%rcx, %rcx
00000001001c73c7	je	0x1001c73eb
00000001001c73c9	movl	0x44(%r12), %edx
00000001001c73ce	movl	$CONFIG_ENCODERS, %edi
00000001001c73d3	movq	%rax, %rsi
00000001001c73d6	callq	__ZN11CSkinEngine12createActionEbRKNSt3__112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEEi ## CSkinEngine::createAction(bool, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, int)
00000001001c73db	movq	%rax, 0x30(%r12)
00000001001c73e0	testq	%rax, %rax
00000001001c73e3	je	0x1001c73eb
00000001001c73e5	movb	$0x1, 0x38(%r12)
00000001001c73eb	leaq	0x1d42253(%rip), %rsi           ## literal pool for: "clickthrough"
00000001001c73f2	movl	$0xc, %edx
00000001001c73f7	movq	%r15, %rdi
00000001001c73fa	callq	__ZNK8CXMLNode8hasParamEPKci    ## CXMLNode::hasParam(char const*, int) const
00000001001c73ff	testb	%al, %al
00000001001c7401	je	0x1001c7440
00000001001c7403	leaq	0x1d4223b(%rip), %rsi           ## literal pool for: "clickthrough"
00000001001c740a	leaq	0x1d42241(%rip), %rdx           ## literal pool for: "pass"
00000001001c7411	movq	%r15, %rdi
00000001001c7414	callq	__ZNK8CXMLNode7isParamEPKcS1_   ## CXMLNode::isParam(char const*, char const*) const
00000001001c7419	movl	$0xfffffffe, %ecx               ## imm = 0xFFFFFFFE
00000001001c741e	testb	%al, %al
00000001001c7420	jne	0x1001c743b
00000001001c7422	leaq	0x1d4221c(%rip), %rsi           ## literal pool for: "clickthrough"
00000001001c7429	movl	$0xc, %edx
00000001001c742e	xorl	%ecx, %ecx
00000001001c7430	movq	%r15, %rdi
00000001001c7433	callq	__ZNK8CXMLNode14getBoolParamNSEPKcib ## CXMLNode::getBoolParamNS(char const*, int, bool) const
00000001001c7438	movzbl	%al, %ecx
00000001001c743b	movl	%ecx, 0x3c(%r12)
00000001001c7440	leaq	0x1d42210(%rip), %rsi           ## literal pool for: "panel"
00000001001c7447	movl	$0x5, %edx
00000001001c744c	movq	%r15, %rdi
00000001001c744f	callq	__ZNK8CXMLNode8hasParamEPKci    ## CXMLNode::hasParam(char const*, int) const
00000001001c7454	testb	%al, %al
00000001001c7456	je	0x1001c7466
00000001001c7458	leaq	0x1d421f8(%rip), %rsi           ## literal pool for: "panel"
00000001001c745f	movl	$0x5, %edx
00000001001c7464	jmp	0x1001c7472
00000001001c7466	leaq	0x1d421f0(%rip), %rsi           ## literal pool for: "pannel"
00000001001c746d	movl	$0x6, %edx
00000001001c7472	movq	%r15, %rdi
00000001001c7475	callq	__ZN8CXMLNode8getParamEPKcm     ## CXMLNode::getParam(char const*, unsigned long)
00000001001c747a	movzbl	CONFIG_BETTER_HW_COMPATIBILITY(%rax), %ecx
00000001001c747d	testb	$0x1, %cl
00000001001c7480	jne	0x1001c7487
00000001001c7482	shrq	%rcx
00000001001c7485	jmp	0x1001c748b
00000001001c7487	movq	0x8(%rax), %rcx
00000001001c748b	testq	%rcx, %rcx
00000001001c748e	je	0x1001c74a9
00000001001c7490	leaq	_skinEngine(%rip), %rdi
00000001001c7497	movl	$CONFIG_ENCODERS, %edx
00000001001c749c	movq	%rax, %rsi
00000001001c749f	callq	__ZN11CSkinEngine13getPanelIndexERKNSt3__112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEEb ## CSkinEngine::getPanelIndex(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, bool)
00000001001c74a4	movl	%eax, 0x40(%r12)
00000001001c74a9	leaq	0x1d421b4(%rip), %rsi           ## literal pool for: "mouserect"
00000001001c74b0	movl	$0x9, %edx
00000001001c74b5	movq	%r15, %rdi
00000001001c74b8	callq	__ZNK8CXMLNode8getChildEPKci    ## CXMLNode::getChild(char const*, int) const
00000001001c74bd	testq	%rax, %rax
00000001001c74c0	je	0x1001c7593
00000001001c74c6	movq	%rax, %rbx
00000001001c74c9	cvttss2si	0x8(%r12), %edx
00000001001c74d0	leaq	0x1d3ac78(%rip), %rsi           ## literal pool for: "x"
00000001001c74d7	movq	%rax, %rdi
00000001001c74da	movl	%edx, %ecx
00000001001c74dc	callq	__ZNK8CXMLNode19getSignedParamApplyEPKcii ## CXMLNode::getSignedParamApply(char const*, int, int) const
00000001001c74e1	cvtsi2ss	%eax, %xmm0
00000001001c74e5	subss	0x8(%r12), %xmm0
00000001001c74ec	cvttss2si	%xmm0, %eax
00000001001c74f0	movl	%eax, 0xb8(%r12)
00000001001c74f8	cvttss2si	0xc(%r12), %edx
00000001001c74ff	leaq	0x1d39c96(%rip), %rsi           ## literal pool for: "y"
00000001001c7506	movq	%rbx, %rdi
00000001001c7509	movl	%edx, %ecx
00000001001c750b	callq	__ZNK8CXMLNode19getSignedParamApplyEPKcii ## CXMLNode::getSignedParamApply(char const*, int, int) const
00000001001c7510	xorps	%xmm0, %xmm0
00000001001c7513	cvtsi2ss	%eax, %xmm0
00000001001c7517	subss	0xc(%r12), %xmm0
00000001001c751e	cvttss2si	%xmm0, %eax
00000001001c7522	movl	%eax, 0xbc(%r12)
00000001001c752a	cvttss2si	0x10(%r12), %ecx
00000001001c7531	leaq	0x1d39c72(%rip), %rsi           ## literal pool for: "width"
00000001001c7538	movl	$0x5, %edx
00000001001c753d	movq	%rbx, %rdi
00000001001c7540	callq	__ZNK8CXMLNode13getIntParamNSEPKcii ## CXMLNode::getIntParamNS(char const*, int, int) const
00000001001c7545	movl	%eax, 0xc0(%r12)
00000001001c754d	cvttss2si	0x14(%r12), %ecx
00000001001c7554	leaq	0x1d39c43(%rip), %rsi           ## literal pool for: "height"
00000001001c755b	movl	$0x6, %edx
00000001001c7560	movq	%rbx, %rdi
00000001001c7563	callq	__ZNK8CXMLNode13getIntParamNSEPKcii ## CXMLNode::getIntParamNS(char const*, int, int) const
00000001001c7568	movl	%eax, 0xc4(%r12)
00000001001c7570	movb	$0x1, %r13b
00000001001c7573	cmpl	$0x0, 0xc0(%r12)
00000001001c757c	jne	0x1001c7682
00000001001c7582	movl	$0xffffffff, 0xc0(%r12)         ## imm = 0xFFFFFFFF
00000001001c758e	jmp	0x1001c7682
00000001001c7593	leaq	0x1d420d4(%rip), %rsi           ## literal pool for: "mousecircle"
00000001001c759a	movl	$0xb, %edx
00000001001c759f	movq	%r15, %rdi
00000001001c75a2	callq	__ZNK8CXMLNode8getChildEPKci    ## CXMLNode::getChild(char const*, int) const
00000001001c75a7	testq	%rax, %rax
00000001001c75aa	je	0x1001c76c0
00000001001c75b0	movq	%rax, %r14
00000001001c75b3	movss	0x10(%r12), %xmm0
00000001001c75ba	mulss	0x199938e(%rip), %xmm0
00000001001c75c2	addss	0x8(%r12), %xmm0
00000001001c75c9	cvttss2si	%xmm0, %edx
00000001001c75cd	leaq	0x1d3ab7b(%rip), %rsi           ## literal pool for: "x"
00000001001c75d4	movq	%rax, %rdi
00000001001c75d7	movl	%edx, %ecx
00000001001c75d9	callq	__ZNK8CXMLNode19getSignedParamApplyEPKcii ## CXMLNode::getSignedParamApply(char const*, int, int) const
00000001001c75de	xorps	%xmm0, %xmm0
00000001001c75e1	cvtsi2ss	%eax, %xmm0
00000001001c75e5	subss	0x8(%r12), %xmm0
00000001001c75ec	cvttss2si	%xmm0, %eax
00000001001c75f0	movl	%eax, 0xb8(%r12)
00000001001c75f8	movss	0x14(%r12), %xmm0
00000001001c75ff	mulss	0x1999349(%rip), %xmm0
00000001001c7607	addss	0xc(%r12), %xmm0
00000001001c760e	cvttss2si	%xmm0, %edx
00000001001c7612	leaq	0x1d39b83(%rip), %rsi           ## literal pool for: "y"
00000001001c7619	movq	%r14, %rdi
00000001001c761c	movl	%edx, %ecx
00000001001c761e	callq	__ZNK8CXMLNode19getSignedParamApplyEPKcii ## CXMLNode::getSignedParamApply(char const*, int, int) const
00000001001c7623	xorps	%xmm0, %xmm0
00000001001c7626	cvtsi2ss	%eax, %xmm0
00000001001c762a	subss	0xc(%r12), %xmm0
00000001001c7631	cvttss2si	%xmm0, %eax
00000001001c7635	movl	%eax, 0xbc(%r12)
00000001001c763d	movss	0x14(%r12), %xmm0
00000001001c7644	minss	0x10(%r12), %xmm0
00000001001c764b	mulss	0x19992fd(%rip), %xmm0
00000001001c7653	cvttss2si	%xmm0, %ecx
00000001001c7657	leaq	0x1d35c6c(%rip), %rsi           ## literal pool for: "r"
00000001001c765e	movl	$CONFIG_ENCODERS, %edx
00000001001c7663	movq	%r14, %rdi
00000001001c7666	callq	__ZNK8CXMLNode13getIntParamNSEPKcii ## CXMLNode::getIntParamNS(char const*, int, int) const
00000001001c766b	movl	%eax, 0xc0(%r12)
00000001001c7673	movl	$0xfffffb2e, 0xc4(%r12)         ## imm = 0xFFFFFB2E
00000001001c767f	movb	$0x1, %r13b
00000001001c7682	movl	%r13d, %eax
00000001001c7685	addq	$0x68, %rsp
00000001001c7689	popq	%rbx
00000001001c768a	popq	%r12
00000001001c768c	popq	%r13
00000001001c768e	popq	%r14
00000001001c7690	popq	%r15
00000001001c7692	popq	%rbp
00000001001c7693	retq
00000001001c7694	movq	%r15, %rdi
00000001001c7697	movl	%edx, %ecx
00000001001c7699	callq	__ZNK8CXMLNode19getSignedParamApplyEPKcii ## CXMLNode::getSignedParamApply(char const*, int, int) const
00000001001c769e	xorps	%xmm0, %xmm0
00000001001c76a1	cvtsi2ss	%eax, %xmm0
00000001001c76a5	movss	%xmm0, 0x8(%r12)
00000001001c76ac	cvttss2si	-0x34(%rbp), %edx
00000001001c76b1	leaq	0x1d39ae4(%rip), %rsi           ## literal pool for: "y"
00000001001c76b8	movq	%r15, %rdi
00000001001c76bb	jmp	0x1001c7016
00000001001c76c0	leaq	0x1d41fb3(%rip), %rsi           ## literal pool for: "mousemask"
00000001001c76c7	movl	$0x9, %edx
00000001001c76cc	movq	%r15, %rdi
00000001001c76cf	callq	__ZNK8CXMLNode8getChildEPKci    ## CXMLNode::getChild(char const*, int) const
00000001001c76d4	testq	%rax, %rax
00000001001c76d7	je	0x1001c7767
00000001001c76dd	movq	%rax, %rbx
00000001001c76e0	movq	-0x30(%rbp), %rax
00000001001c76e4	testq	%rax, %rax
00000001001c76e7	je	0x1001c767f
00000001001c76e9	movb	$0x1, %r13b
00000001001c76ec	cmpq	$0x0, 0x30(%rax)
00000001001c76f1	je	0x1001c7682
00000001001c76f3	cvttss2si	0x20(%r12), %r14d
00000001001c76fa	cvttss2si	0x24(%r12), %eax
00000001001c7701	movq	%rax, -0x50(%rbp)
00000001001c7705	cvttss2si	0x8(%r12), %edx
00000001001c770c	leaq	0x1d3aa3c(%rip), %rsi           ## literal pool for: "x"
00000001001c7713	movq	%rbx, %rdi
00000001001c7716	movl	%edx, %ecx
00000001001c7718	callq	__ZNK8CXMLNode19getSignedParamApplyEPKcii ## CXMLNode::getSignedParamApply(char const*, int, int) const
00000001001c771d	movl	%eax, %r15d
00000001001c7720	cvttss2si	0xc(%r12), %edx
00000001001c7727	leaq	0x1d39a6e(%rip), %rsi           ## literal pool for: "y"
00000001001c772e	movq	%rbx, %rdi
00000001001c7731	movl	%edx, %ecx
00000001001c7733	callq	__ZNK8CXMLNode19getSignedParamApplyEPKcii ## CXMLNode::getSignedParamApply(char const*, int, int) const
00000001001c7738	movq	%r15, %rdx
00000001001c773b	movl	%eax, %r15d
00000001001c773e	orl	%edx, %eax
00000001001c7740	js	0x1001c775f
00000001001c7742	leal	CONFIG_BETTER_HW_COMPATIBILITY(%rdx,%r14), %eax
00000001001c7746	movq	-0x30(%rbp), %rcx
00000001001c774a	cmpl	CONFIG_BETTER_HW_COMPATIBILITY(%rcx), %eax
00000001001c774c	jg	0x1001c775f
00000001001c774e	movq	-0x50(%rbp), %rbx
00000001001c7752	leal	CONFIG_BETTER_HW_COMPATIBILITY(%r15,%rbx), %eax
00000001001c7756	cmpl	0x4(%rcx), %eax
00000001001c7759	jle	0x1001c77e0
00000001001c775f	xorl	%r13d, %r13d
00000001001c7762	jmp	0x1001c7682
00000001001c7767	movb	$0x1, %r13b
00000001001c776a	cmpl	$0x320, _skinVersion(%rip)      ## imm = 0x320
00000001001c7774	jl	0x1001c7682
00000001001c777a	leaq	0x1d38c0c(%rip), %rsi           ## literal pool for: "clipmask"
00000001001c7781	movl	$0x8, %edx
00000001001c7786	movq	%r15, %rdi
00000001001c7789	callq	__ZNK8CXMLNode8getChildEPKci    ## CXMLNode::getChild(char const*, int) const
00000001001c778e	movq	%rax, %rbx
00000001001c7791	movq	-0x30(%rbp), %rax
00000001001c7795	testq	%rax, %rax
00000001001c7798	je	0x1001c7682
00000001001c779e	testq	%rbx, %rbx
00000001001c77a1	jne	0x1001c76e9
00000001001c77a7	jmp	0x1001c7682
00000001001c77ac	incq	%rax
00000001001c77af	leaq	_messageEngine(%rip), %rdi
00000001001c77b6	leaq	0x1d38599(%rip), %rsi           ## literal pool for: "tooltips"
00000001001c77bd	movq	%rax, %rdx
00000001001c77c0	callq	__ZN14CMessageEngine18getMessageExistingEPKcS1_ ## CMessageEngine::getMessageExisting(char const*, char const*)
00000001001c77c5	testq	%rax, %rax
00000001001c77c8	je	0x1001c7276
00000001001c77ce	leaq	0x60(%r12), %rdi
00000001001c77d3	movq	%rax, %rsi
00000001001c77d6	callq	0x101b5d6b2                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6assignEPKc
00000001001c77db	jmp	0x1001c7276
00000001001c77e0	leal	0x7(%r14), %eax
00000001001c77e4	sarl	$0x1f, %eax
00000001001c77e7	shrl	$0x1d, %eax
00000001001c77ea	leal	0x7(%r14,%rax), %eax
00000001001c77ef	sarl	$0x3, %eax
00000001001c77f2	movl	%eax, -0x44(%rbp)
00000001001c77f5	imull	%ebx, %eax
00000001001c77f8	movslq	%eax, %rdi
00000001001c77fb	movl	$CONFIG_ENCODERS, %esi
00000001001c7800	movq	%rdx, -0x40(%rbp)
00000001001c7804	movq	%rdi, -0x70(%rbp)
00000001001c7808	callq	0x101b5d9b8                     ## symbol stub for: _calloc
00000001001c780d	movq	%rax, 0xb0(%r12)
00000001001c7815	movq	-0x30(%rbp), %rdi
00000001001c7819	movq	-0x40(%rbp), %rsi
00000001001c781d	movl	%r15d, %edx
00000001001c7820	callq	__ZN6CImage8getPixelEii         ## CImage::getPixel(int, int)
00000001001c7825	movq	-0x30(%rbp), %rdi
00000001001c7829	testl	%ebx, %ebx
00000001001c782b	jle	0x1001c7682
00000001001c7831	shrl	$0x18, %eax
00000001001c7834	xorl	%esi, %esi
00000001001c7836	xorl	%r8d, %r8d
00000001001c7839	movq	-0x50(%rbp), %r13
00000001001c783d	testl	%r14d, %r14d
00000001001c7840	jle	0x1001c78b5
00000001001c7842	movq	0x30(%rdi), %rcx
00000001001c7846	leal	CONFIG_BETTER_HW_COMPATIBILITY(%rsi,%r15), %edx
00000001001c784a	imull	CONFIG_BETTER_HW_COMPATIBILITY(%rdi), %edx
00000001001c784d	addl	-0x40(%rbp), %edx
00000001001c7850	movslq	%edx, %rdx
00000001001c7853	movl	%esi, %r9d
00000001001c7856	imull	-0x44(%rbp), %r9d
00000001001c785b	leaq	0x3(%rcx,%rdx,4), %rdx
00000001001c7860	xorl	%ebx, %ebx
00000001001c7862	movzbl	CONFIG_BETTER_HW_COMPATIBILITY(%rdx,%rbx,4), %ecx
00000001001c7866	cmpl	%ecx, %eax
00000001001c7868	jne	0x1001c78af
00000001001c786a	cmpb	$0x6, -0x1(%rdx,%rbx,4)
00000001001c786f	jb	0x1001c78a5
00000001001c7871	cmpb	$0x6, -0x3(%rdx,%rbx,4)
00000001001c7876	jb	0x1001c78a5
00000001001c7878	cmpb	$0x6, -0x2(%rdx,%rbx,4)
00000001001c787d	jb	0x1001c78a5
00000001001c787f	movl	%ebx, %ecx
00000001001c7881	andb	$0x7, %cl
00000001001c7884	movq	0xb0(%r12), %r10
00000001001c788c	movl	%ebx, %edi
00000001001c788e	shrl	$0x3, %edi
00000001001c7891	addl	%r9d, %edi
00000001001c7894	movb	$0x1, %r11b
00000001001c7897	shlb	%cl, %r11b
00000001001c789a	movslq	%edi, %rcx
00000001001c789d	orb	%r11b, CONFIG_BETTER_HW_COMPATIBILITY(%r10,%rcx)
00000001001c78a1	movq	-0x30(%rbp), %rdi
00000001001c78a5	incq	%rbx
00000001001c78a8	cmpl	%r14d, %ebx
00000001001c78ab	jl	0x1001c7862
00000001001c78ad	jmp	0x1001c78b5
00000001001c78af	movb	$0x1, %r8b
00000001001c78b2	movl	%r13d, %esi
00000001001c78b5	incl	%esi
00000001001c78b7	cmpl	%r13d, %esi
00000001001c78ba	jl	0x1001c783d
00000001001c78bc	movb	$0x1, %r13b
00000001001c78bf	testb	$0x1, %r8b
00000001001c78c3	je	0x1001c7682
00000001001c78c9	movq	0xb0(%r12), %rdi
00000001001c78d1	movq	-0x70(%rbp), %rsi
00000001001c78d5	callq	0x101b5d886                     ## symbol stub for: ___bzero
00000001001c78da	movq	-0x30(%rbp), %r11
00000001001c78de	cmpl	$0x0, -0x50(%rbp)
00000001001c78e2	jle	0x1001c7682
00000001001c78e8	movl	%r14d, %r9d
00000001001c78eb	xorl	%r8d, %r8d
00000001001c78ee	testl	%r14d, %r14d
00000001001c78f1	jle	0x1001c793f
00000001001c78f3	movq	0x30(%r11), %rcx
00000001001c78f7	movl	%r8d, %r10d
00000001001c78fa	imull	-0x44(%rbp), %r10d
00000001001c78ff	movl	CONFIG_BETTER_HW_COMPATIBILITY(%r11), %edi
00000001001c7902	imull	%r15d, %edi
00000001001c7906	addl	-0x40(%rbp), %edi
00000001001c7909	movslq	%edi, %rdi
00000001001c790c	leaq	0x3(%rcx,%rdi,4), %rdi
00000001001c7911	xorl	%ebx, %ebx
00000001001c7913	cmpb	$0x0, CONFIG_BETTER_HW_COMPATIBILITY(%rdi,%rbx,4)
00000001001c7917	js	0x1001c7937
00000001001c7919	movl	%ebx, %ecx
00000001001c791b	andb	$0x7, %cl
00000001001c791e	movq	0xb0(%r12), %rsi
00000001001c7926	movl	%ebx, %eax
00000001001c7928	shrl	$0x3, %eax
00000001001c792b	addl	%r10d, %eax
00000001001c792e	movb	$0x1, %dl
00000001001c7930	shlb	%cl, %dl
00000001001c7932	cltq
00000001001c7934	orb	%dl, CONFIG_BETTER_HW_COMPATIBILITY(%rsi,%rax)
00000001001c7937	incq	%rbx
00000001001c793a	cmpl	%ebx, %r9d
00000001001c793d	jne	0x1001c7913
00000001001c793f	incl	%r8d
00000001001c7942	incl	%r15d
00000001001c7945	movb	$0x1, %r13b
00000001001c7948	cmpl	-0x50(%rbp), %r8d
00000001001c794c	jne	0x1001c78ee
00000001001c794e	jmp	0x1001c7682
00000001001c7953	jmp	0x1001c796c
00000001001c7955	movq	%rax, %rbx
00000001001c7958	testb	$0x1, -0x88(%rbp)
00000001001c795f	je	0x1001c796f
00000001001c7961	movq	-0x78(%rbp), %rdi
00000001001c7965	callq	0x101b5d868                     ## symbol stub for: __ZdlPv
00000001001c796a	jmp	0x1001c796f
00000001001c796c	movq	%rax, %rbx
00000001001c796f	testb	$0x1, -0x68(%rbp)
00000001001c7973	je	0x1001c797e
00000001001c7975	movq	-0x58(%rbp), %rdi
00000001001c7979	callq	0x101b5d868                     ## symbol stub for: __ZdlPv
00000001001c797e	movq	%rbx, %rdi
00000001001c7981	callq	0x101b5d604                     ## symbol stub for: __Unwind_Resume
00000001001c7986	ud2
00000001001c7988	pushq	%rbp
00000001001c7989	movq	%rsp, %rbp
00000001001c798c	pushq	%r14
00000001001c798e	pushq	%rbx
00000001001c798f	movq	%rsi, %r14
00000001001c7992	movq	%rdi, %rbx
00000001001c7995	testb	$0x1, CONFIG_BETTER_HW_COMPATIBILITY(%rdi)
00000001001c7998	jne	0x1001c79a1
00000001001c799a	movw	$CONFIG_BETTER_HW_COMPATIBILITY, CONFIG_BETTER_HW_COMPATIBILITY(%rbx)
00000001001c799f	jmp	0x1001c79c5
00000001001c79a1	movq	0x10(%rbx), %rax
00000001001c79a5	movb	$0x0, CONFIG_BETTER_HW_COMPATIBILITY(%rax)
00000001001c79a8	movq	$CONFIG_BETTER_HW_COMPATIBILITY, 0x8(%rbx)
00000001001c79b0	testb	$0x1, CONFIG_BETTER_HW_COMPATIBILITY(%rbx)
00000001001c79b3	je	0x1001c79c5
00000001001c79b5	movq	0x10(%rbx), %rdi
00000001001c79b9	callq	0x101b5d868                     ## symbol stub for: __ZdlPv
00000001001c79be	movq	$CONFIG_BETTER_HW_COMPATIBILITY, CONFIG_BETTER_HW_COMPATIBILITY(%rbx)
00000001001c79c5	movq	0x10(%r14), %rax
00000001001c79c9	movq	%rax, 0x10(%rbx)
00000001001c79cd	movq	CONFIG_BETTER_HW_COMPATIBILITY(%r14), %rax
00000001001c79d0	movq	0x8(%r14), %rcx
00000001001c79d4	movq	%rcx, 0x8(%rbx)
00000001001c79d8	movq	%rax, CONFIG_BETTER_HW_COMPATIBILITY(%rbx)
00000001001c79db	xorl	%eax, %eax
00000001001c79dd	movq	%rax, 0x10(%r14)
00000001001c79e1	movq	%rax, 0x8(%r14)
00000001001c79e5	movq	%rax, CONFIG_BETTER_HW_COMPATIBILITY(%r14)
00000001001c79e8	popq	%rbx
00000001001c79e9	popq	%r14
00000001001c79eb	popq	%rbp
00000001001c79ec	retq
00000001001c79ed	nop
00000001001c79ee	pushq	%rbp
00000001001c79ef	movq	%rsp, %rbp
00000001001c79f2	pushq	%r15
00000001001c79f4	pushq	%r14
00000001001c79f6	pushq	%r12
00000001001c79f8	pushq	%rbx
00000001001c79f9	movq	%rsi, %r14
00000001001c79fc	movq	%rdi, %r12
00000001001c79ff	xorl	%eax, %eax
00000001001c7a01	movq	%rax, 0x10(%rdi)
00000001001c7a05	movq	%rax, 0x8(%rdi)
00000001001c7a09	movq	%rax, CONFIG_BETTER_HW_COMPATIBILITY(%rdi)
00000001001c7a0c	movq	%rsi, %rdi
00000001001c7a0f	callq	0x101b5e2b2                     ## symbol stub for: _strlen
00000001001c7a14	cmpq	$-0x10, %rax
00000001001c7a18	jae	0x1001c7a7b
00000001001c7a1a	movq	%rax, %r15
00000001001c7a1d	cmpq	$0x17, %rax
00000001001c7a21	jae	0x1001c7a37
00000001001c7a23	movl	%r15d, %eax
00000001001c7a26	addb	%r15b, %al
00000001001c7a29	movb	%al, CONFIG_BETTER_HW_COMPATIBILITY(%r12)
00000001001c7a2d	incq	%r12
00000001001c7a30	testq	%r15, %r15
00000001001c7a33	jne	0x1001c7a5f
00000001001c7a35	jmp	0x1001c7a6d
00000001001c7a37	movq	%r15, %rbx
00000001001c7a3a	addq	$0x10, %rbx
00000001001c7a3e	andq	$-0x10, %rbx
00000001001c7a42	movq	%rbx, %rdi
00000001001c7a45	callq	0x101b5d87a                     ## symbol stub for: __Znwm
00000001001c7a4a	movq	%rax, 0x10(%r12)
00000001001c7a4f	orq	$0x1, %rbx
00000001001c7a53	movq	%rbx, CONFIG_BETTER_HW_COMPATIBILITY(%r12)
00000001001c7a57	movq	%r15, 0x8(%r12)
00000001001c7a5c	movq	%rax, %r12
00000001001c7a5f	movq	%r12, %rdi
00000001001c7a62	movq	%r14, %rsi
00000001001c7a65	movq	%r15, %rdx
00000001001c7a68	callq	0x101b5df28                     ## symbol stub for: _memcpy
00000001001c7a6d	movb	$0x0, CONFIG_BETTER_HW_COMPATIBILITY(%r12,%r15)
00000001001c7a72	popq	%rbx
00000001001c7a73	popq	%r12
00000001001c7a75	popq	%r14
00000001001c7a77	popq	%r15
00000001001c7a79	popq	%rbp
00000001001c7a7a	retq
00000001001c7a7b	movq	%r12, %rdi
00000001001c7a7e	callq	0x101b5d62e                     ## symbol stub for: __ZNKSt3__121__basic_string_commonILb1EE20__throw_length_errorEv
00000001001c7a83	nop
