__ZN15DLGActionWizard10updateHintEv [0x1006c6136, 0x1006c6704):
00000001006c6136	pushq	%rbp
00000001006c6137	movq	%rsp, %rbp
00000001006c613a	pushq	%r15
00000001006c613c	pushq	%r14
00000001006c613e	pushq	%r13
00000001006c6140	pushq	%r12
00000001006c6142	pushq	%rbx
00000001006c6143	subq	$0x78, %rsp
00000001006c6147	movq	%rdi, %r12
00000001006c614a	movq	0x50f9ed7(%rip), %rax           ## literal pool symbol address: ___stack_chk_guard
00000001006c6151	movq	CONFIG_EMULATE_HARDWARE(%rax), %rax
00000001006c6154	movq	%rax, -0x30(%rbp)
00000001006c6158	testb	$0x1, 0x620(%rdi)
00000001006c615f	jne	0x1006c616e
00000001006c6161	movw	$CONFIG_EMULATE_HARDWARE, 0x620(%r12)
00000001006c616c	jmp	0x1006c6185
00000001006c616e	movq	0x630(%r12), %rax
00000001006c6176	movb	$0x0, CONFIG_EMULATE_HARDWARE(%rax)
00000001006c6179	movq	$CONFIG_EMULATE_HARDWARE, 0x628(%r12)
00000001006c6185	leaq	0x620(%r12), %rax
00000001006c618d	movq	%rax, -0x48(%rbp)
00000001006c6191	movq	0x618(%r12), %r14
00000001006c6199	testq	%r14, %r14
00000001006c619c	je	0x1006c6605
00000001006c61a2	cmpq	$0x0, 0x5f0(%r12)
00000001006c61ab	jne	0x1006c61bc
00000001006c61ad	cmpq	$0x0, 0x5e0(%r12)
00000001006c61b6	je	0x1006c6605
00000001006c61bc	cmpq	$0x0, 0x38(%r14)
00000001006c61c1	je	0x1006c6510
00000001006c61c7	leaq	0x621(%r12), %rax
00000001006c61cf	movq	%rax, -0x88(%rbp)
00000001006c61d6	leaq	0x622(%r12), %rax
00000001006c61de	movq	%rax, -0x98(%rbp)
00000001006c61e5	leaq	-0x80(%rbp), %r15
00000001006c61e9	movq	%r14, %rbx
00000001006c61ec	movq	0x30(%r14), %r14
00000001006c61f0	testq	%r14, %r14
00000001006c61f3	je	0x1006c61fc
00000001006c61f5	cmpq	$0x0, 0x38(%r14)
00000001006c61fa	jne	0x1006c61e9
00000001006c61fc	movq	0x38(%rbx), %rcx
00000001006c6200	testq	%rcx, %rcx
00000001006c6203	je	0x1006c621c
00000001006c6205	cmpq	$0x0, 0x38(%rcx)
00000001006c620a	je	0x1006c621c
00000001006c620c	cmpq	$0x0, 0x40(%rcx)
00000001006c6211	je	0x1006c621c
00000001006c6213	testq	%r14, %r14
00000001006c6216	cmoveq	%rcx, %r14
00000001006c621a	jmp	0x1006c61e9
00000001006c621c	xorps	%xmm0, %xmm0
00000001006c621f	movaps	%xmm0, -0x80(%rbp)
00000001006c6223	movq	$CONFIG_EMULATE_HARDWARE, -0x70(%rbp)
00000001006c622b	movq	CONFIG_EMULATE_HARDWARE(%rcx), %rax
00000001006c622e	movq	0x8(%rcx), %rcx
00000001006c6232	subq	%rax, %rcx
00000001006c6235	je	0x1006c630a
00000001006c623b	sarq	$0x3, %rcx
00000001006c623f	xorl	%r14d, %r14d
00000001006c6242	movq	%r14, %r13
00000001006c6245	incq	%r14
00000001006c6248	cmpq	%rcx, %r14
00000001006c624b	jne	0x1006c62c1
00000001006c624d	movq	CONFIG_EMULATE_HARDWARE(%rax,%r13,8), %rdi
00000001006c6251	movzbl	0x18(%rdi), %esi
00000001006c6255	testb	$0x1, %sil
00000001006c6259	jne	0x1006c6263
00000001006c625b	addq	$0x19, %rdi
00000001006c625f	shrl	%esi
00000001006c6261	jmp	0x1006c626b
00000001006c6263	movq	0x20(%rdi), %rsi
00000001006c6267	movq	0x28(%rdi), %rdi
00000001006c626b	movl	$CONFIG_VP9, %ecx
00000001006c6270	leaq	0x4f3082b(%rip), %rdx           ## literal pool for: "?"
00000001006c6277	callq	__Z12strIsEqualCINSt3__117basic_string_viewIcNS_11char_traitsIcEEEES3_ ## strIsEqualCI(std::__1::basic_string_view<char, std::__1::char_traits<char>>, std::__1::basic_string_view<char, std::__1::char_traits<char>>)
00000001006c627c	testb	%al, %al
00000001006c627e	jne	0x1006c62ef
00000001006c6280	movq	0x38(%rbx), %rax
00000001006c6284	movq	CONFIG_EMULATE_HARDWARE(%rax), %rax
00000001006c6287	movq	CONFIG_EMULATE_HARDWARE(%rax,%r13,8), %rdi
00000001006c628b	movzbl	0x18(%rdi), %esi
00000001006c628f	testb	$0x1, %sil
00000001006c6293	jne	0x1006c629d
00000001006c6295	addq	$0x19, %rdi
00000001006c6299	shrl	%esi
00000001006c629b	jmp	0x1006c62a5
00000001006c629d	movq	0x20(%rdi), %rsi
00000001006c62a1	movq	0x28(%rdi), %rdi
00000001006c62a5	movl	$0x2, %ecx
00000001006c62aa	leaq	0x4f5923b(%rip), %rdx           ## literal pool for: " ?"
00000001006c62b1	callq	__Z12strIsEqualCINSt3__117basic_string_viewIcNS_11char_traitsIcEEEES3_ ## strIsEqualCI(std::__1::basic_string_view<char, std::__1::char_traits<char>>, std::__1::basic_string_view<char, std::__1::char_traits<char>>)
00000001006c62b6	testb	%al, %al
00000001006c62b8	jne	0x1006c62ef
00000001006c62ba	movq	0x38(%rbx), %rax
00000001006c62be	movq	CONFIG_EMULATE_HARDWARE(%rax), %rax
00000001006c62c1	movl	_DLGCOLOR_ACTIONWIZARD_BLOCKCONDITION(%rip), %ecx
00000001006c62c7	movq	CONFIG_EMULATE_HARDWARE(%rax,%r13,8), %rsi
00000001006c62cb	movl	%ecx, 0x10(%rsi)
00000001006c62ce	movzbl	0x18(%rsi), %edx
00000001006c62d2	testb	$0x1, %dl
00000001006c62d5	je	0x1006c62e1
00000001006c62d7	movq	0x20(%rsi), %rdx
00000001006c62db	movq	0x28(%rsi), %rsi
00000001006c62df	jmp	0x1006c62e7
00000001006c62e1	addq	$0x19, %rsi
00000001006c62e5	shrl	%edx
00000001006c62e7	movq	%r15, %rdi
00000001006c62ea	callq	0x104fe8516                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm
00000001006c62ef	movq	0x38(%rbx), %rcx
00000001006c62f3	movq	CONFIG_EMULATE_HARDWARE(%rcx), %rax
00000001006c62f6	movq	0x8(%rcx), %rcx
00000001006c62fa	subq	%rax, %rcx
00000001006c62fd	sarq	$0x3, %rcx
00000001006c6301	cmpq	%rcx, %r14
00000001006c6304	jb	0x1006c6242
00000001006c630a	movq	%r15, %rdi
00000001006c630d	callq	__Z15strTrim_inplaceRNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEE ## strTrim_inplace(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>&)
00000001006c6312	movq	0x38(%rbx), %rax
00000001006c6316	movq	0x40(%rax), %rdi
00000001006c631a	testq	%rdi, %rdi
00000001006c631d	je	0x1006c6377
00000001006c631f	movl	_DLGCOLOR_ACTIONWIZARD_BLOCKCONDITION(%rip), %esi
00000001006c6325	callq	__ZN15DLGActionWizard5STree8setColorEj ## DLGActionWizard::STree::setColor(unsigned int)
00000001006c632a	movq	0x38(%rbx), %rax
00000001006c632e	movq	0x40(%rax), %rsi
00000001006c6332	leaq	-0x68(%rbp), %rdi
00000001006c6336	callq	__ZN15DLGActionWizard5STree8toStringEv ## DLGActionWizard::STree::toString()
00000001006c633b	movzbl	-0x68(%rbp), %edx
00000001006c633f	testb	$0x1, %dl
00000001006c6342	je	0x1006c634e
00000001006c6344	movq	-0x58(%rbp), %rsi
00000001006c6348	movq	-0x60(%rbp), %rdx
00000001006c634c	jmp	0x1006c6354
00000001006c634e	shrl	%edx
00000001006c6350	leaq	-0x67(%rbp), %rsi
00000001006c6354	movq	%r15, %rdi
00000001006c6357	callq	0x104fe8516                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm
00000001006c635c	testb	$0x1, -0x68(%rbp)
00000001006c6360	je	0x1006c636b
00000001006c6362	movq	-0x58(%rbp), %rdi
00000001006c6366	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
00000001006c636b	movq	%r15, %rdi
00000001006c636e	callq	__Z15strTrim_inplaceRNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEE ## strTrim_inplace(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>&)
00000001006c6373	movq	0x38(%rbx), %rax
00000001006c6377	cmpq	%rbx, 0x20(%rax)
00000001006c637b	jne	0x1006c63af
00000001006c637d	leaq	-0x68(%rbp), %rdi
00000001006c6381	leaq	0x4f59167(%rip), %rsi           ## literal pool for: "not "
00000001006c6388	movq	%r15, %rdx
00000001006c638b	callq	0x104fe86fc                     ## symbol stub for: __ZNSt3__1plIcNS_11char_traitsIcEENS_9allocatorIcEEEENS_12basic_stringIT_T0_T1_EEPKS6_RKS9_
00000001006c6390	testb	$0x1, -0x80(%rbp)
00000001006c6394	je	0x1006c639f
00000001006c6396	movq	-0x70(%rbp), %rdi
00000001006c639a	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
00000001006c639f	movq	-0x58(%rbp), %rax
00000001006c63a3	movq	%rax, -0x70(%rbp)
00000001006c63a7	movups	-0x68(%rbp), %xmm0
00000001006c63ab	movaps	%xmm0, -0x80(%rbp)
00000001006c63af	movq	-0x48(%rbp), %rax
00000001006c63b3	movzbl	CONFIG_EMULATE_HARDWARE(%rax), %eax
00000001006c63b6	testb	$0x1, %al
00000001006c63b8	jne	0x1006c63be
00000001006c63ba	shrl	%eax
00000001006c63bc	jmp	0x1006c63c6
00000001006c63be	movq	0x628(%r12), %rax
00000001006c63c6	testq	%rax, %rax
00000001006c63c9	je	0x1006c63dc
00000001006c63cb	movzbl	-0x80(%rbp), %r14d
00000001006c63d0	testb	$0x1, %r14b
00000001006c63d4	je	0x1006c63ed
00000001006c63d6	movq	-0x78(%rbp), %r14
00000001006c63da	jmp	0x1006c63f0
00000001006c63dc	movq	-0x48(%rbp), %rdi
00000001006c63e0	movq	%r15, %rsi
00000001006c63e3	callq	0x104fe856a                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
00000001006c63e8	jmp	0x1006c64f2
00000001006c63ed	shrl	%r14d
00000001006c63f0	leaq	0x3(%r14), %rsi
00000001006c63f4	leaq	-0x68(%rbp), %rdi
00000001006c63f8	leaq	-0x49(%rbp), %rdx
00000001006c63fc	callq	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEC2B8ne200100ENS_24__uninitialized_size_tagEmRKS4_ ## std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>::basic_string[abi:ne200100](std::__1::__uninitialized_size_tag, unsigned long, std::__1::allocator<char> const&)
00000001006c6401	testb	$0x1, -0x68(%rbp)
00000001006c6405	leaq	-0x67(%rbp), %r13
00000001006c6409	je	0x1006c640f
00000001006c640b	movq	-0x58(%rbp), %r13
00000001006c640f	testq	%r14, %r14
00000001006c6412	je	0x1006c642d
00000001006c6414	testb	$0x1, -0x80(%rbp)
00000001006c6418	leaq	-0x7f(%rbp), %rsi
00000001006c641c	je	0x1006c6422
00000001006c641e	movq	-0x70(%rbp), %rsi
00000001006c6422	movq	%r13, %rdi
00000001006c6425	movq	%r14, %rdx
00000001006c6428	callq	0x104fe8ed6                     ## symbol stub for: _memmove
00000001006c642d	movl	$0x202620, (%r13,%r14)          ## imm = 0x202620
00000001006c6436	movzbl	0x620(%r12), %edx
00000001006c643f	testb	$0x1, %dl
00000001006c6442	je	0x1006c6456
00000001006c6444	movq	0x630(%r12), %rsi
00000001006c644c	movq	0x628(%r12), %rdx
00000001006c6454	jmp	0x1006c645f
00000001006c6456	shrl	%edx
00000001006c6458	movq	-0x88(%rbp), %rsi
00000001006c645f	leaq	-0x68(%rbp), %rdi
00000001006c6463	callq	0x104fe8516                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm
00000001006c6468	movb	CONFIG_EMULATE_HARDWARE(%rax), %r14b
00000001006c646b	movb	0x1(%rax), %r13b
00000001006c646f	movq	0x8(%rax), %rcx
00000001006c6473	movq	%rcx, -0x3a(%rbp)
00000001006c6477	movq	0x2(%rax), %rcx
00000001006c647b	movq	%rcx, -0x40(%rbp)
00000001006c647f	movq	0x10(%rax), %rsi
00000001006c6483	xorps	%xmm0, %xmm0
00000001006c6486	movups	%xmm0, CONFIG_EMULATE_HARDWARE(%rax)
00000001006c6489	movq	$CONFIG_EMULATE_HARDWARE, 0x10(%rax)
00000001006c6491	movq	-0x48(%rbp), %rax
00000001006c6495	testb	$0x1, CONFIG_EMULATE_HARDWARE(%rax)
00000001006c6498	je	0x1006c64b5
00000001006c649a	movq	0x630(%r12), %rdi
00000001006c64a2	movq	%rsi, -0x90(%rbp)
00000001006c64a9	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
00000001006c64ae	movq	-0x90(%rbp), %rsi
00000001006c64b5	movb	%r14b, 0x620(%r12)
00000001006c64bd	movb	%r13b, 0x621(%r12)
00000001006c64c5	movq	-0x40(%rbp), %rax
00000001006c64c9	movq	-0x3a(%rbp), %rcx
00000001006c64cd	movq	-0x98(%rbp), %rdx
00000001006c64d4	movq	%rcx, 0x6(%rdx)
00000001006c64d8	movq	%rax, CONFIG_EMULATE_HARDWARE(%rdx)
00000001006c64db	movq	%rsi, 0x630(%r12)
00000001006c64e3	testb	$0x1, -0x68(%rbp)
00000001006c64e7	je	0x1006c64f2
00000001006c64e9	movq	-0x58(%rbp), %rdi
00000001006c64ed	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
00000001006c64f2	movq	0x38(%rbx), %r14
00000001006c64f6	testb	$0x1, -0x80(%rbp)
00000001006c64fa	je	0x1006c6505
00000001006c64fc	movq	-0x70(%rbp), %rdi
00000001006c6500	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
00000001006c6505	cmpq	$0x0, 0x38(%r14)
00000001006c650a	jne	0x1006c61e9
00000001006c6510	movq	-0x48(%rbp), %rax
00000001006c6514	movzbl	CONFIG_EMULATE_HARDWARE(%rax), %eax
00000001006c6517	testb	$0x1, %al
00000001006c6519	jne	0x1006c651f
00000001006c651b	shrl	%eax
00000001006c651d	jmp	0x1006c6527
00000001006c651f	movq	0x628(%r12), %rax
00000001006c6527	testq	%rax, %rax
00000001006c652a	je	0x1006c6581
00000001006c652c	leaq	_messageEngine(%rip), %rdi
00000001006c6533	leaq	0x4f15519(%rip), %rsi           ## literal pool for: "config"
00000001006c653a	leaq	0x4f58fb3(%rip), %rdx           ## literal pool for: "condition: "
00000001006c6541	xorl	%ecx, %ecx
00000001006c6543	callq	__ZN14CMessageEngine20getMessageFromStringEPKcS1_i ## CMessageEngine::getMessageFromString(char const*, char const*, int)
00000001006c6548	leaq	-0x80(%rbp), %rdi
00000001006c654c	movq	%rax, %rsi
00000001006c654f	movq	-0x48(%rbp), %rdx
00000001006c6553	callq	0x104fe86fc                     ## symbol stub for: __ZNSt3__1plIcNS_11char_traitsIcEENS_9allocatorIcEEEENS_12basic_stringIT_T0_T1_EEPKS6_RKS9_
00000001006c6558	movq	-0x48(%rbp), %rax
00000001006c655c	testb	$0x1, CONFIG_EMULATE_HARDWARE(%rax)
00000001006c655f	je	0x1006c656e
00000001006c6561	movq	0x630(%r12), %rdi
00000001006c6569	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
00000001006c656e	movq	-0x70(%rbp), %rax
00000001006c6572	movq	-0x48(%rbp), %rcx
00000001006c6576	movq	%rax, 0x10(%rcx)
00000001006c657a	movups	-0x80(%rbp), %xmm0
00000001006c657e	movups	%xmm0, CONFIG_EMULATE_HARDWARE(%rcx)
00000001006c6581	movq	0x618(%r12), %rax
00000001006c6589	movq	CONFIG_EMULATE_HARDWARE(%rax), %rcx
00000001006c658c	movq	0x8(%rax), %rdx
00000001006c6590	subq	%rcx, %rdx
00000001006c6593	je	0x1006c65b9
00000001006c6595	sarq	$0x3, %rdx
00000001006c6599	movl	_DLGCOLOR_ACTIONWIZARD_BLOCK(%rip), %esi
00000001006c659f	cmpq	$0x1, %rdx
00000001006c65a3	adcq	$0x0, %rdx
00000001006c65a7	xorl	%edi, %edi
00000001006c65a9	movq	CONFIG_EMULATE_HARDWARE(%rcx,%rdi,8), %r8
00000001006c65ad	movl	%esi, 0x10(%r8)
00000001006c65b1	incq	%rdi
00000001006c65b4	cmpq	%rdi, %rdx
00000001006c65b7	jne	0x1006c65a9
00000001006c65b9	movq	0x40(%rax), %rdi
00000001006c65bd	testq	%rdi, %rdi
00000001006c65c0	je	0x1006c65d5
00000001006c65c2	movl	_DLGCOLOR_ACTIONWIZARD_BLOCK(%rip), %esi
00000001006c65c8	callq	__ZN15DLGActionWizard5STree8setColorEj ## DLGActionWizard::STree::setColor(unsigned int)
00000001006c65cd	movq	0x618(%r12), %rax
00000001006c65d5	movq	0x18(%rax), %rdi
00000001006c65d9	testq	%rdi, %rdi
00000001006c65dc	je	0x1006c6605
00000001006c65de	movl	_DLGCOLOR_ACTIONWIZARD_BLOCKYES(%rip), %esi
00000001006c65e4	callq	__ZN15DLGActionWizard5STree8setColorEj ## DLGActionWizard::STree::setColor(unsigned int)
00000001006c65e9	movq	0x618(%r12), %rax
00000001006c65f1	movq	0x20(%rax), %rdi
00000001006c65f5	testq	%rdi, %rdi
00000001006c65f8	je	0x1006c6605
00000001006c65fa	movl	_DLGCOLOR_ACTIONWIZARD_BLOCKNO(%rip), %esi
00000001006c6600	callq	__ZN15DLGActionWizard5STree8setColorEj ## DLGActionWizard::STree::setColor(unsigned int)
00000001006c6605	movl	0x638(%r12), %eax
00000001006c660d	movl	%eax, 0x154(%r12)
00000001006c6615	movzbl	0x620(%r12), %eax
00000001006c661e	testb	$0x1, %al
00000001006c6620	jne	0x1006c6626
00000001006c6622	shrl	%eax
00000001006c6624	jmp	0x1006c662e
00000001006c6626	movq	0x628(%r12), %rax
00000001006c662e	testq	%rax, %rax
00000001006c6631	je	0x1006c66a3
00000001006c6633	movl	0x1c(%r12), %eax
00000001006c6638	leaq	-0x80(%rbp), %rdx
00000001006c663c	movl	%eax, CONFIG_EMULATE_HARDWARE(%rdx)
00000001006c663e	leaq	-0x68(%rbp), %rcx
00000001006c6642	movl	$0x7fffffff, CONFIG_EMULATE_HARDWARE(%rcx) ## imm = 0x7FFFFFFF
00000001006c6648	movq	0x8(%r12), %rax
00000001006c664d	movq	0x148(%rax), %rdi
00000001006c6654	leaq	0x160(%r12), %r8
00000001006c665c	movq	CONFIG_EMULATE_HARDWARE(%rdi), %rax
00000001006c665f	movq	-0x48(%rbp), %rsi
00000001006c6663	movl	$working_state.cur.put_buffer.simd, %r9d
00000001006c6669	callq	*0x70(%rax)
00000001006c666c	testb	%al, %al
00000001006c666e	je	0x1006c66a3
00000001006c6670	movl	-0x80(%rbp), %eax
00000001006c6673	movl	0x150(%r12), %ecx
00000001006c667b	cmpl	%eax, %ecx
00000001006c667d	cmovgl	%ecx, %eax
00000001006c6680	movl	0x188(%r12), %ecx
00000001006c6688	movl	%eax, 0x150(%r12)
00000001006c6690	addl	0x154(%r12), %ecx
00000001006c6698	addl	-0x68(%rbp), %ecx
00000001006c669b	movl	%ecx, 0x154(%r12)
00000001006c66a3	movq	0x50f997e(%rip), %rax           ## literal pool symbol address: ___stack_chk_guard
00000001006c66aa	movq	CONFIG_EMULATE_HARDWARE(%rax), %rax
00000001006c66ad	cmpq	-0x30(%rbp), %rax
00000001006c66b1	jne	0x1006c66c2
00000001006c66b3	addq	$0x78, %rsp
00000001006c66b7	popq	%rbx
00000001006c66b8	popq	%r12
00000001006c66ba	popq	%r13
00000001006c66bc	popq	%r14
00000001006c66be	popq	%r15
00000001006c66c0	popq	%rbp
00000001006c66c1	retq
00000001006c66c2	callq	0x104fe882e                     ## symbol stub for: ___stack_chk_fail
00000001006c66c7	movq	%rax, %rbx
00000001006c66ca	jmp	0x1006c66fc
00000001006c66cc	jmp	0x1006c66ea
00000001006c66ce	jmp	0x1006c66ea
00000001006c66d0	jmp	0x1006c66ea
00000001006c66d2	jmp	0x1006c66d4
00000001006c66d4	movq	%rax, %rbx
00000001006c66d7	testb	$0x1, -0x68(%rbp)
00000001006c66db	je	0x1006c66ed
00000001006c66dd	movq	-0x58(%rbp), %rdi
00000001006c66e1	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
00000001006c66e6	jmp	0x1006c66ed
00000001006c66e8	jmp	0x1006c66ea
00000001006c66ea	movq	%rax, %rbx
00000001006c66ed	testb	$0x1, -0x80(%rbp)
00000001006c66f1	je	0x1006c66fc
00000001006c66f3	movq	-0x70(%rbp), %rdi
00000001006c66f7	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
00000001006c66fc	movq	%rbx, %rdi
00000001006c66ff	callq	0x104fe8456                     ## symbol stub for: __Unwind_Resume
