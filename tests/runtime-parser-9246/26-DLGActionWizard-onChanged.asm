__ZN15DLGActionWizard9onChangedEv [0x1006c45ee, 0x1006c4ca6):
00000001006c45ee	pushq	%rbp
00000001006c45ef	movq	%rsp, %rbp
00000001006c45f2	pushq	%r15
00000001006c45f4	pushq	%r14
00000001006c45f6	pushq	%r13
00000001006c45f8	pushq	%r12
00000001006c45fa	pushq	%rbx
00000001006c45fb	subq	$0x68, %rsp
00000001006c45ff	movl	0x570(%rdi), %eax
00000001006c4605	addl	$-0x7d, %eax
00000001006c4608	cmpl	$0x2, %eax
00000001006c460b	jb	0x1006c4b5f
00000001006c4611	movq	%rdi, %rbx
00000001006c4614	addq	$0x578, %rdi                    ## imm = 0x578
00000001006c461b	movq	0x578(%rbx), %rsi
00000001006c4622	movq	%rdi, -0x70(%rbp)
00000001006c4626	callq	__ZNSt3__16vectorINS_12basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEENS4_IS6_EEE22__base_destruct_at_endB8ne200100EPS6_ ## std::__1::vector<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>, std::__1::allocator<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>>>::__base_destruct_at_end[abi:ne200100](std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>*)
00000001006c462b	movl	0x570(%rbx), %eax
00000001006c4631	cmpq	$0x7f, %rax
00000001006c4635	ja	0x1006c4b5f
00000001006c463b	movq	0x50fb9ce(%rip), %r15           ## literal pool symbol address: __DefaultRuneLocale
00000001006c4642	testb	$0x1, 0x3d(%r15,%rax,4)
00000001006c4648	jne	0x1006c4659
00000001006c464a	cmpq	$0x5f, %rax
00000001006c464e	je	0x1006c4659
00000001006c4650	cmpl	$0x20, %eax
00000001006c4653	jne	0x1006c4b5f
00000001006c4659	movl	$CONFIG_EMULATE_HARDWARE, 0x570(%rbx)
00000001006c4663	testb	$0x1, 0x50(%rbx)
00000001006c4667	jne	0x1006c467e
00000001006c4669	leaq	0x50(%rbx), %rax
00000001006c466d	movq	0x10(%rax), %rcx
00000001006c4671	movq	%rcx, -0x30(%rbp)
00000001006c4675	movups	CONFIG_EMULATE_HARDWARE(%rax), %xmm0
00000001006c4678	movaps	%xmm0, -0x40(%rbp)
00000001006c467c	jmp	0x1006c468f
00000001006c467e	movq	0x58(%rbx), %rdx
00000001006c4682	movq	0x60(%rbx), %rsi
00000001006c4686	leaq	-0x40(%rbp), %rdi
00000001006c468a	callq	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE25__init_copy_ctor_externalEPKcm ## std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>::__init_copy_ctor_external(char const*, unsigned long)
00000001006c468f	movq	0x4c0(%rbx), %rax
00000001006c4696	movq	0x4c8(%rbx), %rcx
00000001006c469d	cmpq	%rax, %rcx
00000001006c46a0	movq	%rax, %r14
00000001006c46a3	cmovlq	%rcx, %r14
00000001006c46a7	testq	%rcx, %rcx
00000001006c46aa	cmovsq	%rax, %r14
00000001006c46ae	movzbl	-0x40(%rbp), %ecx
00000001006c46b2	movl	%ecx, %eax
00000001006c46b4	andb	$0x1, %al
00000001006c46b6	je	0x1006c46be
00000001006c46b8	movq	-0x38(%rbp), %rcx
00000001006c46bc	jmp	0x1006c46c0
00000001006c46be	shrl	%ecx
00000001006c46c0	cmpq	%rcx, %r14
00000001006c46c3	jae	0x1006c471d
00000001006c46c5	testb	%al, %al
00000001006c46c7	je	0x1006c46cf
00000001006c46c9	movq	-0x30(%rbp), %rcx
00000001006c46cd	jmp	0x1006c46d3
00000001006c46cf	leaq	-0x3f(%rbp), %rcx
00000001006c46d3	cmpb	$0x20, CONFIG_EMULATE_HARDWARE(%rcx,%r14)
00000001006c46d8	je	0x1006c471d
00000001006c46da	testb	%al, %al
00000001006c46dc	je	0x1006c46e4
00000001006c46de	movq	-0x30(%rbp), %rcx
00000001006c46e2	jmp	0x1006c46e8
00000001006c46e4	leaq	-0x3f(%rbp), %rcx
00000001006c46e8	cmpb	$0x3f, CONFIG_EMULATE_HARDWARE(%rcx,%r14)
00000001006c46ed	je	0x1006c471d
00000001006c46ef	testb	%al, %al
00000001006c46f1	je	0x1006c46f9
00000001006c46f3	movq	-0x30(%rbp), %rcx
00000001006c46f7	jmp	0x1006c46fd
00000001006c46f9	leaq	-0x3f(%rbp), %rcx
00000001006c46fd	cmpb	$0x26, CONFIG_EMULATE_HARDWARE(%rcx,%r14)
00000001006c4702	je	0x1006c471d
00000001006c4704	testb	%al, %al
00000001006c4706	je	0x1006c470e
00000001006c4708	movq	-0x30(%rbp), %rcx
00000001006c470c	jmp	0x1006c4712
00000001006c470e	leaq	-0x3f(%rbp), %rcx
00000001006c4712	cmpb	$0x3a, CONFIG_EMULATE_HARDWARE(%rcx,%r14)
00000001006c4717	jne	0x1006c4b52
00000001006c471d	testq	%r14, %r14
00000001006c4720	movq	%r14, -0x68(%rbp)
00000001006c4724	je	0x1006c4787
00000001006c4726	movq	%r14, %r12
00000001006c4729	leaq	-0x3f(%rbp), %r14
00000001006c472d	movl	$0x100, %r13d                   ## imm = 0x100
00000001006c4733	testb	$0x1, -0x40(%rbp)
00000001006c4737	movq	%r14, %rax
00000001006c473a	je	0x1006c4740
00000001006c473c	movq	-0x30(%rbp), %rax
00000001006c4740	movsbl	-0x1(%rax,%r12), %edi
00000001006c4746	testl	%edi, %edi
00000001006c4748	js	0x1006c4756
00000001006c474a	movl	%edi, %eax
00000001006c474c	movl	0x3c(%r15,%rax,4), %eax
00000001006c4751	andl	%r13d, %eax
00000001006c4754	jmp	0x1006c4760
00000001006c4756	movl	$0x100, %esi                    ## imm = 0x100
00000001006c475b	callq	0x104fe87f2                     ## symbol stub for: ___maskrune
00000001006c4760	testl	%eax, %eax
00000001006c4762	jne	0x1006c4779
00000001006c4764	testb	$0x1, -0x40(%rbp)
00000001006c4768	movq	%r14, %rax
00000001006c476b	je	0x1006c4771
00000001006c476d	movq	-0x30(%rbp), %rax
00000001006c4771	cmpb	$0x5f, -0x1(%rax,%r12)
00000001006c4777	jne	0x1006c4781
00000001006c4779	decq	%r12
00000001006c477c	jne	0x1006c4733
00000001006c477e	xorl	%r12d, %r12d
00000001006c4781	movq	-0x68(%rbp), %r14
00000001006c4785	jmp	0x1006c478a
00000001006c4787	xorl	%r12d, %r12d
00000001006c478a	movq	%r14, %rcx
00000001006c478d	subq	%r12, %rcx
00000001006c4790	leaq	-0x60(%rbp), %rdi
00000001006c4794	leaq	-0x40(%rbp), %rsi
00000001006c4798	leaq	-0x41(%rbp), %r8
00000001006c479c	movq	%r12, %rdx
00000001006c479f	callq	0x104fe855e                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEC2ERKS5_mmRKS4_
00000001006c47a4	testq	%r12, %r12
00000001006c47a7	je	0x1006c47b5
00000001006c47a9	testb	$0x1, -0x40(%rbp)
00000001006c47ad	je	0x1006c47bd
00000001006c47af	movq	-0x30(%rbp), %rax
00000001006c47b3	jmp	0x1006c47c1
00000001006c47b5	movl	$CONFIG_VP9, %r13d
00000001006c47bb	jmp	0x1006c47fa
00000001006c47bd	leaq	-0x3f(%rbp), %rax
00000001006c47c1	movl	$CONFIG_VP9, %r13d
00000001006c47c7	movabsq	$-0x7bffffc000000000, %rcx      ## imm = 0x8400004000000000
00000001006c47d1	movq	%r12, %r15
00000001006c47d4	movzbl	-0x1(%rax,%r15), %edx
00000001006c47da	cmpq	$0x3f, %rdx
00000001006c47de	ja	0x1006c47e6
00000001006c47e0	btq	%rdx, %rcx
00000001006c47e4	jb	0x1006c47fd
00000001006c47e6	decq	%r15
00000001006c47e9	xorl	%esi, %esi
00000001006c47eb	cmpb	$0x20, %dl
00000001006c47ee	sete	%sil
00000001006c47f2	addq	%rsi, %r13
00000001006c47f5	testq	%r15, %r15
00000001006c47f8	jne	0x1006c47d4
00000001006c47fa	xorl	%r15d, %r15d
00000001006c47fd	cmpq	%r12, %r15
00000001006c4800	jae	0x1006c4831
00000001006c4802	leaq	CONFIG_EMULATE_HARDWARE(%r15,%r13), %rax
00000001006c4806	testb	$0x1, -0x40(%rbp)
00000001006c480a	je	0x1006c4812
00000001006c480c	movq	-0x30(%rbp), %rcx
00000001006c4810	jmp	0x1006c4816
00000001006c4812	leaq	-0x3f(%rbp), %rcx
00000001006c4816	subq	%r12, %rax
00000001006c4819	cmpb	$0x20, CONFIG_EMULATE_HARDWARE(%rcx,%r15)
00000001006c481e	jne	0x1006c4831
00000001006c4820	decq	%r13
00000001006c4823	incq	%r15
00000001006c4826	cmpq	%r15, %r12
00000001006c4829	jne	0x1006c4819
00000001006c482b	movq	%r12, %r15
00000001006c482e	movq	%rax, %r13
00000001006c4831	cmpq	%r12, %r15
00000001006c4834	setne	%al
00000001006c4837	cmpq	%r12, %r14
00000001006c483a	setbe	%cl
00000001006c483d	orb	%al, %cl
00000001006c483f	jne	0x1006c4888
00000001006c4841	leaq	0x4f17267(%rip), %rdi           ## literal pool for: "deck"
00000001006c4848	leaq	-0x60(%rbp), %rsi
00000001006c484c	callq	__Z11canCompletePKcRKNSt3__112basic_stringIcNS1_11char_traitsIcEENS1_9allocatorIcEEEE ## canComplete(char const*, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&)
00000001006c4851	testb	%al, %al
00000001006c4853	je	0x1006c4888
00000001006c4855	movq	0x580(%rbx), %r15
00000001006c485c	cmpq	0x588(%rbx), %r15
00000001006c4863	jae	0x1006c4a21
00000001006c4869	leaq	0x4f1723f(%rip), %rsi           ## literal pool for: "deck"
00000001006c4870	movq	%r15, %rdi
00000001006c4873	callq	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEC2B8ne200100ILi0EEEPKc ## std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>::basic_string[abi:ne200100]<0>(char const*)
00000001006c4878	addq	$0x18, %r15
00000001006c487c	movq	%r15, 0x580(%rbx)
00000001006c4883	jmp	0x1006c4a34
00000001006c4888	leaq	0x5(%r15), %rax
00000001006c488c	cmpq	%r12, %rax
00000001006c488f	jne	0x1006c48bd
00000001006c4891	testb	$0x1, -0x40(%rbp)
00000001006c4895	je	0x1006c489d
00000001006c4897	movq	-0x30(%rbp), %rdi
00000001006c489b	jmp	0x1006c48a1
00000001006c489d	leaq	-0x3f(%rbp), %rdi
00000001006c48a1	addq	%r15, %rdi
00000001006c48a4	leaq	0x4f258bf(%rip), %rsi           ## literal pool for: "deck "
00000001006c48ab	movl	$0x5, %edx
00000001006c48b0	callq	0x104fe92b4                     ## symbol stub for: _strncasecmp
00000001006c48b5	testl	%eax, %eax
00000001006c48b7	je	0x1006c49a2
00000001006c48bd	cmpq	%r12, %r14
00000001006c48c0	jbe	0x1006c4a3b
00000001006c48c6	cmpq	%r12, %r15
00000001006c48c9	jne	0x1006c4985
00000001006c48cf	leaq	_actionList(%rip), %r12
00000001006c48d6	movq	CONFIG_EMULATE_HARDWARE(%r12), %r15
00000001006c48da	testq	%r15, %r15
00000001006c48dd	je	0x1006c4946
00000001006c48df	leaq	-0x60(%rbp), %r14
00000001006c48e3	cmpb	$0x0, 0xc(%r12)
00000001006c48e9	jne	0x1006c4938
00000001006c48eb	movq	%r15, %rdi
00000001006c48ee	movq	%r14, %rsi
00000001006c48f1	callq	__Z11canCompletePKcRKNSt3__112basic_stringIcNS1_11char_traitsIcEENS1_9allocatorIcEEEE ## canComplete(char const*, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&)
00000001006c48f6	testb	%al, %al
00000001006c48f8	je	0x1006c4938
00000001006c48fa	movq	0x580(%rbx), %r13
00000001006c4901	cmpq	0x588(%rbx), %r13
00000001006c4908	jae	0x1006c4922
00000001006c490a	movq	%r13, %rdi
00000001006c490d	movq	%r15, %rsi
00000001006c4910	callq	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEC2B8ne200100ILi0EEEPKc ## std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>::basic_string[abi:ne200100]<0>(char const*)
00000001006c4915	addq	$0x18, %r13
00000001006c4919	movq	%r13, 0x580(%rbx)
00000001006c4920	jmp	0x1006c4931
00000001006c4922	movq	-0x70(%rbp), %rdi
00000001006c4926	movq	%r12, %rsi
00000001006c4929	callq	__ZNSt3__16vectorINS_12basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEENS4_IS6_EEE24__emplace_back_slow_pathIJRPKcEEEPS6_DpOT_ ## std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>* std::__1::vector<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>, std::__1::allocator<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>>>::__emplace_back_slow_path<char const*&>(char const*&)
00000001006c492e	movq	%rax, %r13
00000001006c4931	movq	%r13, 0x580(%rbx)
00000001006c4938	movq	0x10(%r12), %r15
00000001006c493d	addq	$0x10, %r12
00000001006c4941	testq	%r15, %r15
00000001006c4944	jne	0x1006c48e3
00000001006c4946	movq	0x580(%rbx), %rax
00000001006c494d	subq	0x578(%rbx), %rax
00000001006c4954	sarq	$0x3, %rax
00000001006c4958	movabsq	$-0x5555555555555555, %r13      ## imm = 0xAAAAAAAAAAAAAAAB
00000001006c4962	imulq	%r13, %rax
00000001006c4966	cmpq	$0x5, %rax
00000001006c496a	jae	0x1006c4a3b
00000001006c4970	movzbl	-0x60(%rbp), %eax
00000001006c4974	testb	$0x1, %al
00000001006c4976	je	0x1006c4b6e
00000001006c497c	movq	-0x58(%rbp), %rax
00000001006c4980	jmp	0x1006c4b70
00000001006c4985	cmpq	$0x3, %r13
00000001006c4989	jne	0x1006c4a3b
00000001006c498f	testb	$0x1, -0x40(%rbp)
00000001006c4993	je	0x1006c4c16
00000001006c4999	movq	-0x30(%rbp), %rdi
00000001006c499d	jmp	0x1006c4c1a
00000001006c49a2	xorl	%r13d, %r13d
00000001006c49a5	leaq	__ZZN15DLGActionWizard9onChangedEvE13deckArguments(%rip), %r14 ## DLGActionWizard::onChanged()::deckArguments
00000001006c49ac	leaq	-0x60(%rbp), %r12
00000001006c49b0	movzbl	-0x60(%rbp), %eax
00000001006c49b4	testb	$0x1, %al
00000001006c49b6	je	0x1006c49be
00000001006c49b8	movq	-0x58(%rbp), %rax
00000001006c49bc	jmp	0x1006c49c0
00000001006c49be	shrl	%eax
00000001006c49c0	testq	%rax, %rax
00000001006c49c3	je	0x1006c49d6
00000001006c49c5	movq	(%r13,%r14), %rdi
00000001006c49ca	movq	%r12, %rsi
00000001006c49cd	callq	__Z11canCompletePKcRKNSt3__112basic_stringIcNS1_11char_traitsIcEENS1_9allocatorIcEEEE ## canComplete(char const*, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&)
00000001006c49d2	testb	%al, %al
00000001006c49d4	je	0x1006c4a15
00000001006c49d6	leaq	CONFIG_EMULATE_HARDWARE(%r14,%r13), %rsi
00000001006c49da	movq	0x580(%rbx), %r15
00000001006c49e1	cmpq	0x588(%rbx), %r15
00000001006c49e8	jae	0x1006c4a02
00000001006c49ea	movq	CONFIG_EMULATE_HARDWARE(%rsi), %rsi
00000001006c49ed	movq	%r15, %rdi
00000001006c49f0	callq	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEC2B8ne200100ILi0EEEPKc ## std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>::basic_string[abi:ne200100]<0>(char const*)
00000001006c49f5	addq	$0x18, %r15
00000001006c49f9	movq	%r15, 0x580(%rbx)
00000001006c4a00	jmp	0x1006c4a0e
00000001006c4a02	movq	-0x70(%rbp), %rdi
00000001006c4a06	callq	__ZNSt3__16vectorINS_12basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEENS4_IS6_EEE24__emplace_back_slow_pathIJRKPKcEEEPS6_DpOT_ ## std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>* std::__1::vector<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>, std::__1::allocator<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>>>::__emplace_back_slow_path<char const* const&>(char const* const&)
00000001006c4a0b	movq	%rax, %r15
00000001006c4a0e	movq	%r15, 0x580(%rbx)
00000001006c4a15	addq	$0x8, %r13
00000001006c4a19	cmpq	$0x40, %r13
00000001006c4a1d	jne	0x1006c49b0
00000001006c4a1f	jmp	0x1006c4a3b
00000001006c4a21	leaq	0x4f17087(%rip), %rsi           ## literal pool for: "deck"
00000001006c4a28	movq	-0x70(%rbp), %rdi
00000001006c4a2c	callq	__ZNSt3__16vectorINS_12basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEENS4_IS6_EEE24__emplace_back_slow_pathIJRA5_KcEEEPS6_DpOT_ ## std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>* std::__1::vector<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>, std::__1::allocator<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>>>::__emplace_back_slow_path<char const (&) [5]>(char const (&) [5])
00000001006c4a31	movq	%rax, %r15
00000001006c4a34	movq	%r15, 0x580(%rbx)
00000001006c4a3b	movq	0x578(%rbx), %r15
00000001006c4a42	movb	-0x60(%rbp), %al
00000001006c4a45	cmpq	%r15, 0x580(%rbx)
00000001006c4a4c	je	0x1006c4b40
00000001006c4a52	testb	$0x1, %al
00000001006c4a54	je	0x1006c4a5c
00000001006c4a56	movq	-0x58(%rbp), %rax
00000001006c4a5a	jmp	0x1006c4a61
00000001006c4a5c	movzbl	%al, %eax
00000001006c4a5f	shrl	%eax
00000001006c4a61	movq	-0x68(%rbp), %r14
00000001006c4a65	movq	%rax, 0x590(%rbx)
00000001006c4a6c	leaq	-0x60(%rbp), %rsi
00000001006c4a70	movq	%r15, %rdi
00000001006c4a73	callq	__Z8isLeftCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEES7_ ## isLeftCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&)
00000001006c4a78	testb	%al, %al
00000001006c4a7a	je	0x1006c4b32
00000001006c4a80	movzbl	CONFIG_EMULATE_HARDWARE(%r15), %ecx
00000001006c4a84	testb	$0x1, %cl
00000001006c4a87	jne	0x1006c4a9b
00000001006c4a89	movq	0x590(%rbx), %rax
00000001006c4a90	leaq	CONFIG_EMULATE_HARDWARE(%r15,%rax), %rdx
00000001006c4a94	incq	%rdx
00000001006c4a97	shrl	%ecx
00000001006c4a99	jmp	0x1006c4aad
00000001006c4a9b	movq	0x590(%rbx), %rax
00000001006c4aa2	movq	0x10(%r15), %rdx
00000001006c4aa6	addq	%rax, %rdx
00000001006c4aa9	movq	0x8(%r15), %rcx
00000001006c4aad	subq	%rax, %rcx
00000001006c4ab0	leaq	-0x40(%rbp), %rdi
00000001006c4ab4	movq	%r14, %rsi
00000001006c4ab7	callq	0x104fe8534                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6insertEmPKcm
00000001006c4abc	testb	$0x1, -0x40(%rbp)
00000001006c4ac0	jne	0x1006c4ad7
00000001006c4ac2	movq	-0x30(%rbp), %rax
00000001006c4ac6	movq	%rax, -0x80(%rbp)
00000001006c4aca	movaps	-0x40(%rbp), %xmm0
00000001006c4ace	movaps	%xmm0, -0x90(%rbp)
00000001006c4ad5	jmp	0x1006c4aeb
00000001006c4ad7	movq	-0x38(%rbp), %rdx
00000001006c4adb	movq	-0x30(%rbp), %rsi
00000001006c4adf	leaq	-0x90(%rbp), %rdi
00000001006c4ae6	callq	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE25__init_copy_ctor_externalEPKcm ## std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>::__init_copy_ctor_external(char const*, unsigned long)
00000001006c4aeb	leaq	-0x90(%rbp), %rsi
00000001006c4af2	movq	%rbx, %rdi
00000001006c4af5	callq	__ZN7DLGEdit8setValueENSt3__112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEE ## DLGEdit::setValue(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>)
00000001006c4afa	testb	$0x1, -0x90(%rbp)
00000001006c4b01	je	0x1006c4b0c
00000001006c4b03	movq	-0x80(%rbp), %rdi
00000001006c4b07	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
00000001006c4b0c	movzbl	CONFIG_EMULATE_HARDWARE(%r15), %edx
00000001006c4b10	testb	$0x1, %dl
00000001006c4b13	jne	0x1006c4b19
00000001006c4b15	shrl	%edx
00000001006c4b17	jmp	0x1006c4b1d
00000001006c4b19	movq	0x8(%r15), %rdx
00000001006c4b1d	addq	%r14, %rdx
00000001006c4b20	subq	0x590(%rbx), %rdx
00000001006c4b27	movq	%rbx, %rdi
00000001006c4b2a	movq	%r14, %rsi
00000001006c4b2d	callq	__ZN7DLGEdit12setSelectionEmm   ## DLGEdit::setSelection(unsigned long, unsigned long)
00000001006c4b32	movq	%rbx, %rdi
00000001006c4b35	movq	%r15, %rsi
00000001006c4b38	callq	__ZN15DLGActionWizard7setHelpERKNSt3__112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEE ## DLGActionWizard::setHelp(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&)
00000001006c4b3d	movb	-0x60(%rbp), %al
00000001006c4b40	testb	$0x1, %al
00000001006c4b42	je	0x1006c4b4d
00000001006c4b44	movq	-0x50(%rbp), %rdi
00000001006c4b48	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
00000001006c4b4d	movb	-0x40(%rbp), %al
00000001006c4b50	andb	$0x1, %al
00000001006c4b52	testb	%al, %al
00000001006c4b54	je	0x1006c4b5f
00000001006c4b56	movq	-0x30(%rbp), %rdi
00000001006c4b5a	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
00000001006c4b5f	addq	$0x68, %rsp
00000001006c4b63	popq	%rbx
00000001006c4b64	popq	%r12
00000001006c4b66	popq	%r13
00000001006c4b68	popq	%r14
00000001006c4b6a	popq	%r15
00000001006c4b6c	popq	%rbp
00000001006c4b6d	retq
00000001006c4b6e	shrl	%eax
00000001006c4b70	cmpq	$0x3, %rax
00000001006c4b74	jb	0x1006c4a3b
00000001006c4b7a	leaq	_actionList(%rip), %r12
00000001006c4b81	movq	CONFIG_EMULATE_HARDWARE(%r12), %rdi
00000001006c4b85	testq	%rdi, %rdi
00000001006c4b88	je	0x1006c4a3b
00000001006c4b8e	leaq	-0x60(%rbp), %r14
00000001006c4b92	cmpb	$0x0, 0xc(%r12)
00000001006c4b98	jne	0x1006c4c03
00000001006c4b9a	movq	%r14, %rsi
00000001006c4b9d	callq	__Z9strFindCIPKcRKNSt3__112basic_stringIcNS1_11char_traitsIcEENS1_9allocatorIcEEEE ## strFindCI(char const*, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&)
00000001006c4ba2	decq	%rax
00000001006c4ba5	cmpq	$-0x3, %rax
00000001006c4ba9	ja	0x1006c4c03
00000001006c4bab	movq	0x580(%rbx), %r15
00000001006c4bb2	cmpq	0x588(%rbx), %r15
00000001006c4bb9	jae	0x1006c4bd4
00000001006c4bbb	movq	CONFIG_EMULATE_HARDWARE(%r12), %rsi
00000001006c4bbf	movq	%r15, %rdi
00000001006c4bc2	callq	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEC2B8ne200100ILi0EEEPKc ## std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>::basic_string[abi:ne200100]<0>(char const*)
00000001006c4bc7	addq	$0x18, %r15
00000001006c4bcb	movq	%r15, 0x580(%rbx)
00000001006c4bd2	jmp	0x1006c4be3
00000001006c4bd4	movq	-0x70(%rbp), %rdi
00000001006c4bd8	movq	%r12, %rsi
00000001006c4bdb	callq	__ZNSt3__16vectorINS_12basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEENS4_IS6_EEE24__emplace_back_slow_pathIJRPKcEEEPS6_DpOT_ ## std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>* std::__1::vector<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>, std::__1::allocator<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>>>::__emplace_back_slow_path<char const*&>(char const*&)
00000001006c4be0	movq	%rax, %r15
00000001006c4be3	movq	%r15, 0x580(%rbx)
00000001006c4bea	subq	0x578(%rbx), %r15
00000001006c4bf1	sarq	$0x3, %r15
00000001006c4bf5	imulq	%r13, %r15
00000001006c4bf9	cmpq	$0x9, %r15
00000001006c4bfd	ja	0x1006c4a3b
00000001006c4c03	movq	0x10(%r12), %rdi
00000001006c4c08	addq	$0x10, %r12
00000001006c4c0c	testq	%rdi, %rdi
00000001006c4c0f	jne	0x1006c4b92
00000001006c4c11	jmp	0x1006c4a3b
00000001006c4c16	leaq	-0x3f(%rbp), %rdi
00000001006c4c1a	addq	%r15, %rdi
00000001006c4c1d	leaq	0x4f25546(%rip), %rsi           ## literal pool for: "deck "
00000001006c4c24	movl	$0x5, %edx
00000001006c4c29	callq	0x104fe92b4                     ## symbol stub for: _strncasecmp
00000001006c4c2e	testl	%eax, %eax
00000001006c4c30	jne	0x1006c4a3b
00000001006c4c36	jmp	0x1006c48cf
00000001006c4c3b	jmp	0x1006c4c6a
00000001006c4c3d	jmp	0x1006c4c78
00000001006c4c3f	jmp	0x1006c4c6a
00000001006c4c41	movq	%rax, %r14
00000001006c4c44	testb	$0x1, -0x90(%rbp)
00000001006c4c4b	je	0x1006c4c7b
00000001006c4c4d	movq	-0x80(%rbp), %rdi
00000001006c4c51	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
00000001006c4c56	jmp	0x1006c4c7b
00000001006c4c58	movq	%rax, %r14
00000001006c4c5b	movq	%r13, 0x580(%rbx)
00000001006c4c62	jmp	0x1006c4c7b
00000001006c4c64	jmp	0x1006c4c78
00000001006c4c66	jmp	0x1006c4c78
00000001006c4c68	jmp	0x1006c4c8c
00000001006c4c6a	movq	%rax, %r14
00000001006c4c6d	movq	%r15, 0x580(%rbx)
00000001006c4c74	jmp	0x1006c4c7b
00000001006c4c76	jmp	0x1006c4c78
00000001006c4c78	movq	%rax, %r14
00000001006c4c7b	testb	$0x1, -0x60(%rbp)
00000001006c4c7f	je	0x1006c4c8f
00000001006c4c81	movq	-0x50(%rbp), %rdi
00000001006c4c85	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
00000001006c4c8a	jmp	0x1006c4c8f
00000001006c4c8c	movq	%rax, %r14
00000001006c4c8f	testb	$0x1, -0x40(%rbp)
00000001006c4c93	je	0x1006c4c9e
00000001006c4c95	movq	-0x30(%rbp), %rdi
00000001006c4c99	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
00000001006c4c9e	movq	%r14, %rdi
00000001006c4ca1	callq	0x104fe8456                     ## symbol stub for: __Unwind_Resume
