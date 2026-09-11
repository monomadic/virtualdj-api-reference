__ZN7IAction17getDeckFromStringERKNSt3__112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEERj [0x100599a88, 0x100599d60):
0000000100599a88	pushq	%rbp
0000000100599a89	movq	%rsp, %rbp
0000000100599a8c	pushq	%r15
0000000100599a8e	pushq	%r14
0000000100599a90	pushq	%r12
0000000100599a92	pushq	%rbx
0000000100599a93	movq	%rsi, %rbx
0000000100599a96	movq	%rdi, %r14
0000000100599a99	movzbl	CONFIG_EMULATE_HARDWARE(%rdi), %r15d
0000000100599a9d	movl	%r15d, %r12d
0000000100599aa0	andb	$0x1, %r12b
0000000100599aa4	je	0x100599aac
0000000100599aa6	movq	0x10(%r14), %rdi
0000000100599aaa	jmp	0x100599ab0
0000000100599aac	leaq	0x1(%r14), %rdi
0000000100599ab0	callq	0x104fe88d6                     ## symbol stub for: _atoi
0000000100599ab5	testl	%eax, %eax
0000000100599ab7	je	0x100599ac6
0000000100599ab9	movl	%eax, CONFIG_EMULATE_HARDWARE(%rbx)
0000000100599abb	movb	$0x1, %al
0000000100599abd	popq	%rbx
0000000100599abe	popq	%r12
0000000100599ac0	popq	%r14
0000000100599ac2	popq	%r15
0000000100599ac4	popq	%rbp
0000000100599ac5	retq
0000000100599ac6	shrl	%r15d
0000000100599ac9	testb	%r12b, %r12b
0000000100599acc	movq	0x8(%r14), %rax
0000000100599ad0	movq	%rax, %rcx
0000000100599ad3	cmoveq	%r15, %rcx
0000000100599ad7	cmpq	$0x7, %rcx
0000000100599adb	jne	0x100599b09
0000000100599add	leaq	0x504e92c(%rip), %rsi           ## literal pool for: "default"
0000000100599ae4	movq	%r14, %rdi
0000000100599ae7	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
0000000100599aec	movl	%eax, %ecx
0000000100599aee	movl	$0x646566, %eax                 ## imm = 0x646566
0000000100599af3	testb	%cl, %cl
0000000100599af5	jne	0x100599ab9
0000000100599af7	movzbl	CONFIG_EMULATE_HARDWARE(%r14), %r15d
0000000100599afb	movq	0x8(%r14), %rax
0000000100599aff	movl	%r15d, %r12d
0000000100599b02	andb	$0x1, %r12b
0000000100599b06	shrl	%r15d
0000000100599b09	testb	%r12b, %r12b
0000000100599b0c	movq	%rax, %rcx
0000000100599b0f	cmoveq	%r15, %rcx
0000000100599b13	cmpq	$0x6, %rcx
0000000100599b17	jne	0x100599b45
0000000100599b19	leaq	0x504ddd1(%rip), %rsi           ## literal pool for: "active"
0000000100599b20	movq	%r14, %rdi
0000000100599b23	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
0000000100599b28	movl	%eax, %ecx
0000000100599b2a	movl	$0x61637469, %eax               ## imm = 0x61637469
0000000100599b2f	testb	%cl, %cl
0000000100599b31	jne	0x100599ab9
0000000100599b33	movzbl	CONFIG_EMULATE_HARDWARE(%r14), %r15d
0000000100599b37	movq	0x8(%r14), %rax
0000000100599b3b	movl	%r15d, %r12d
0000000100599b3e	andb	$0x1, %r12b
0000000100599b42	shrl	%r15d
0000000100599b45	testb	%r12b, %r12b
0000000100599b48	movq	%rax, %rcx
0000000100599b4b	cmoveq	%r15, %rcx
0000000100599b4f	cmpq	$0x7, %rcx
0000000100599b53	jne	0x100599b85
0000000100599b55	leaq	0x5043e2e(%rip), %rsi           ## literal pool for: "automix"
0000000100599b5c	movq	%r14, %rdi
0000000100599b5f	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
0000000100599b64	movl	%eax, %ecx
0000000100599b66	movl	$0x6175746f, %eax               ## imm = 0x6175746F
0000000100599b6b	testb	%cl, %cl
0000000100599b6d	jne	0x100599ab9
0000000100599b73	movzbl	CONFIG_EMULATE_HARDWARE(%r14), %r15d
0000000100599b77	movq	0x8(%r14), %rax
0000000100599b7b	movl	%r15d, %r12d
0000000100599b7e	andb	$0x1, %r12b
0000000100599b82	shrl	%r15d
0000000100599b85	testb	%r12b, %r12b
0000000100599b88	movq	%rax, %rcx
0000000100599b8b	cmoveq	%r15, %rcx
0000000100599b8f	cmpq	$0x7, %rcx
0000000100599b93	jne	0x100599bc5
0000000100599b95	leaq	0x5042c34(%rip), %rsi           ## literal pool for: "karaoke"
0000000100599b9c	movq	%r14, %rdi
0000000100599b9f	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
0000000100599ba4	movl	%eax, %ecx
0000000100599ba6	movl	$0x6b617261, %eax               ## imm = 0x6B617261
0000000100599bab	testb	%cl, %cl
0000000100599bad	jne	0x100599ab9
0000000100599bb3	movzbl	CONFIG_EMULATE_HARDWARE(%r14), %r15d
0000000100599bb7	movq	0x8(%r14), %rax
0000000100599bbb	movl	%r15d, %r12d
0000000100599bbe	andb	$0x1, %r12b
0000000100599bc2	shrl	%r15d
0000000100599bc5	testb	%r12b, %r12b
0000000100599bc8	cmovneq	%rax, %r15
0000000100599bcc	cmpq	$0x4, %r15
0000000100599bd0	jne	0x100599bf0
0000000100599bd2	leaq	0x504fc67(%rip), %rsi           ## literal pool for: "left"
0000000100599bd9	movq	%r14, %rdi
0000000100599bdc	callq	__Z12strIsEqualCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## strIsEqualCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
0000000100599be1	movl	%eax, %ecx
0000000100599be3	movl	$0x6c656674, %eax               ## imm = 0x6C656674
0000000100599be8	testb	%cl, %cl
0000000100599bea	jne	0x100599ab9
0000000100599bf0	leaq	0x504fc4e(%rip), %rsi           ## literal pool for: "right"
0000000100599bf7	movq	%r14, %rdi
0000000100599bfa	callq	__Z13strIsEqualCILILm6EEbRKNSt3__112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEERAT__Kc ## bool strIsEqualCIL<6ul>(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const (&) [6ul])
0000000100599bff	movl	%eax, %ecx
0000000100599c01	movl	$0x72696768, %eax               ## imm = 0x72696768
0000000100599c06	testb	%cl, %cl
0000000100599c08	jne	0x100599ab9
0000000100599c0e	leaq	0x504e33b(%rip), %rsi           ## literal pool for: "master"
0000000100599c15	movq	%r14, %rdi
0000000100599c18	callq	__Z13strIsEqualCILILm7EEbRKNSt3__112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEERAT__Kc ## bool strIsEqualCIL<7ul>(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const (&) [7ul])
0000000100599c1d	movl	%eax, %ecx
0000000100599c1f	movl	$0x6d617374, %eax               ## imm = 0x6D617374
0000000100599c24	testb	%cl, %cl
0000000100599c26	jne	0x100599ab9
0000000100599c2c	leaq	0x5057a37(%rip), %rsi           ## literal pool for: "sandbox"
0000000100599c33	movq	%r14, %rdi
0000000100599c36	callq	__Z13strIsEqualCILILm8EEbRKNSt3__112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEERAT__Kc ## bool strIsEqualCIL<8ul>(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const (&) [8ul])
0000000100599c3b	movl	%eax, %ecx
0000000100599c3d	movl	$0x73616e64, %eax               ## imm = 0x73616E64
0000000100599c42	testb	%cl, %cl
0000000100599c44	jne	0x100599ab9
0000000100599c4a	leaq	0x50613c3(%rip), %rsi           ## literal pool for: "none"
0000000100599c51	movq	%r14, %rdi
0000000100599c54	callq	__Z13strIsEqualCILILm5EEbRKNSt3__112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEERAT__Kc ## bool strIsEqualCIL<5ul>(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const (&) [5ul])
0000000100599c59	movl	%eax, %ecx
0000000100599c5b	movl	$0x6e6f6e65, %eax               ## imm = 0x6E6F6E65
0000000100599c60	testb	%cl, %cl
0000000100599c62	jne	0x100599ab9
0000000100599c68	leaq	0x505a63e(%rip), %rsi           ## literal pool for: "all"
0000000100599c6f	movq	%r14, %rdi
0000000100599c72	callq	__Z13strIsEqualCILILm4EEbRKNSt3__112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEERAT__Kc ## bool strIsEqualCIL<4ul>(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const (&) [4ul])
0000000100599c77	movl	%eax, %ecx
0000000100599c79	movl	$0x616c6c, %eax                 ## imm = 0x616C6C
0000000100599c7e	testb	%cl, %cl
0000000100599c80	jne	0x100599ab9
0000000100599c86	leaq	0x5056ae8(%rip), %rsi           ## literal pool for: "leftvideo"
0000000100599c8d	movq	%r14, %rdi
0000000100599c90	callq	__Z13strIsEqualCILILm10EEbRKNSt3__112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEERAT__Kc ## bool strIsEqualCIL<10ul>(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const (&) [10ul])
0000000100599c95	movl	%eax, %ecx
0000000100599c97	movl	$0x766c6566, %eax               ## imm = 0x766C6566
0000000100599c9c	testb	%cl, %cl
0000000100599c9e	jne	0x100599ab9
0000000100599ca4	leaq	0x50576e5(%rip), %rsi           ## literal pool for: "rightvideo"
0000000100599cab	movq	%r14, %rdi
0000000100599cae	callq	__Z13strIsEqualCILILm11EEbRKNSt3__112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEERAT__Kc ## bool strIsEqualCIL<11ul>(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const (&) [11ul])
0000000100599cb3	movl	%eax, %ecx
0000000100599cb5	movl	$0x76726967, %eax               ## imm = 0x76726967
0000000100599cba	testb	%cl, %cl
0000000100599cbc	jne	0x100599ab9
0000000100599cc2	leaq	0x5077786(%rip), %rsi           ## literal pool for: "playing"
0000000100599cc9	movq	%r14, %rdi
0000000100599ccc	callq	__Z13strIsEqualCILILm8EEbRKNSt3__112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEERAT__Kc ## bool strIsEqualCIL<8ul>(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const (&) [8ul])
0000000100599cd1	movl	%eax, %ecx
0000000100599cd3	movl	$0x706c6179, %eax               ## imm = 0x706C6179
0000000100599cd8	testb	%cl, %cl
0000000100599cda	jne	0x100599ab9
0000000100599ce0	leaq	0x507dfa9(%rip), %rsi           ## literal pool for: "mixer1"
0000000100599ce7	movq	%r14, %rdi
0000000100599cea	callq	__Z13strIsEqualCILILm7EEbRKNSt3__112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEERAT__Kc ## bool strIsEqualCIL<7ul>(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const (&) [7ul])
0000000100599cef	movl	%eax, %ecx
0000000100599cf1	movl	$0x6d697831, %eax               ## imm = 0x6D697831
0000000100599cf6	testb	%cl, %cl
0000000100599cf8	jne	0x100599ab9
0000000100599cfe	leaq	0x507df92(%rip), %rsi           ## literal pool for: "mixer2"
0000000100599d05	movq	%r14, %rdi
0000000100599d08	callq	__Z13strIsEqualCILILm7EEbRKNSt3__112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEERAT__Kc ## bool strIsEqualCIL<7ul>(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const (&) [7ul])
0000000100599d0d	movl	%eax, %ecx
0000000100599d0f	movl	$0x6d697832, %eax               ## imm = 0x6D697832
0000000100599d14	testb	%cl, %cl
0000000100599d16	jne	0x100599ab9
0000000100599d1c	leaq	0x507df7b(%rip), %rsi           ## literal pool for: "mixer3"
0000000100599d23	movq	%r14, %rdi
0000000100599d26	callq	__Z13strIsEqualCILILm7EEbRKNSt3__112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEERAT__Kc ## bool strIsEqualCIL<7ul>(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const (&) [7ul])
0000000100599d2b	movl	%eax, %ecx
0000000100599d2d	movl	$0x6d697833, %eax               ## imm = 0x6D697833
0000000100599d32	testb	%cl, %cl
0000000100599d34	jne	0x100599ab9
0000000100599d3a	leaq	0x507df64(%rip), %rsi           ## literal pool for: "mixer4"
0000000100599d41	movq	%r14, %rdi
0000000100599d44	callq	__Z13strIsEqualCILILm7EEbRKNSt3__112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEERAT__Kc ## bool strIsEqualCIL<7ul>(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const (&) [7ul])
0000000100599d49	movl	%eax, %ecx
0000000100599d4b	movl	$0x6d697834, %eax               ## imm = 0x6D697834
0000000100599d50	testb	%cl, %cl
0000000100599d52	jne	0x100599ab9
0000000100599d58	xorl	%eax, %eax
0000000100599d5a	jmp	0x100599abd
0000000100599d5f	addb	%dl, 0x48(%rbp)
