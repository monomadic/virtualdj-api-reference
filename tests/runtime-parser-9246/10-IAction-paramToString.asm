__ZN7IAction13paramToStringEP12SActionParam [0x100598b82, 0x100598f88):
0000000100598b82	pushq	%rbp
0000000100598b83	movq	%rsp, %rbp
0000000100598b86	pushq	%r14
0000000100598b88	pushq	%rbx
0000000100598b89	subq	$0x50, %rsp
0000000100598b8d	movq	%rsi, %r14
0000000100598b90	movq	%rdi, %rbx
0000000100598b93	movl	CONFIG_EMULATE_HARDWARE(%rsi), %eax
0000000100598b95	cmpl	$0x696e73, %eax                 ## imm = 0x696E73
0000000100598b9a	jg	0x100598be2
0000000100598b9c	cmpl	$0x6d72, %eax                   ## imm = 0x6D72
0000000100598ba1	jg	0x100598c22
0000000100598ba3	cmpl	$0x25, %eax
0000000100598ba6	je	0x100598c8e
0000000100598bac	cmpl	$0x6274, %eax                   ## imm = 0x6274
0000000100598bb1	jne	0x100598da7
0000000100598bb7	movss	0x4(%r14), %xmm0
0000000100598bbd	leaq	-0x30(%rbp), %r14
0000000100598bc1	movq	%r14, %rdi
0000000100598bc4	callq	__Z14floatToPackStrf            ## floatToPackStr(float)
0000000100598bc9	leaq	0x5043e3b(%rip), %rsi           ## literal pool for: "bt"
0000000100598bd0	movl	$0x2, %edx
0000000100598bd5	movq	%r14, %rdi
0000000100598bd8	callq	0x104fe8516                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm
0000000100598bdd	jmp	0x100598de2
0000000100598be2	cmpl	$0x76616b, %eax                 ## imm = 0x76616B
0000000100598be7	jg	0x100598c49
0000000100598be9	cmpl	$0x696e74, %eax                 ## imm = 0x696E74
0000000100598bee	je	0x100598cec
0000000100598bf4	cmpl	$0x747874, %eax                 ## imm = 0x747874
0000000100598bf9	jne	0x100598da7
0000000100598bff	testb	$0x1, 0x8(%r14)
0000000100598c04	jne	0x100598e30
0000000100598c0a	addq	$0x8, %r14
0000000100598c0e	movq	0x10(%r14), %rax
0000000100598c12	movq	%rax, 0x10(%rbx)
0000000100598c16	movups	CONFIG_EMULATE_HARDWARE(%r14), %xmm0
0000000100598c1a	movups	%xmm0, CONFIG_EMULATE_HARDWARE(%rbx)
0000000100598c1d	jmp	0x100598ec5
0000000100598c22	cmpl	$0x6d73, %eax                   ## imm = 0x6D73
0000000100598c27	je	0x100598d26
0000000100598c2d	cmpl	$0x636f6c, %eax                 ## imm = 0x636F6C
0000000100598c32	jne	0x100598da7
0000000100598c38	movl	0x4(%r14), %esi
0000000100598c3c	movq	%rbx, %rdi
0000000100598c3f	callq	__Z10colorToStrj                ## colorToStr(unsigned int)
0000000100598c44	jmp	0x100598ec5
0000000100598c49	cmpl	$0x76616c, %eax                 ## imm = 0x76616C
0000000100598c4e	je	0x100598d51
0000000100598c54	cmpl	$0x626f6f6c, %eax               ## imm = 0x626F6F6C
0000000100598c59	jne	0x100598da7
0000000100598c5f	cmpl	$0x0, 0x4(%r14)
0000000100598c64	leaq	0x505eceb(%rip), %rax           ## literal pool for: "off"
0000000100598c6b	leaq	0x5043d96(%rip), %rcx           ## literal pool for: "on"
0000000100598c72	cmoveq	%rax, %rcx
0000000100598c76	leaq	0x505419e(%rip), %rsi           ## literal pool for: "toggle"
0000000100598c7d	cmovnsq	%rcx, %rsi
0000000100598c81	movq	%rbx, %rdi
0000000100598c84	callq	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEC2B8ne200100ILi0EEEPKc ## std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>::basic_string[abi:ne200100]<0>(char const*)
0000000100598c89	jmp	0x100598ec5
0000000100598c8e	movss	0x4(%r14), %xmm0
0000000100598c94	cmpb	$0x1, 0x20(%r14)
0000000100598c99	jne	0x100598dba
0000000100598c9f	xorps	%xmm1, %xmm1
0000000100598ca2	ucomiss	%xmm1, %xmm0
0000000100598ca5	jbe	0x100598dba
0000000100598cab	leaq	0x504f29c(%rip), %rsi           ## literal pool for: "+"
0000000100598cb2	leaq	-0x48(%rbp), %rdi
0000000100598cb6	callq	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEC2B8ne200100ILi0EEEPKc ## std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>::basic_string[abi:ne200100]<0>(char const*)
0000000100598cbb	movss	0x4(%r14), %xmm0
0000000100598cc1	mulss	0x4bf49f7(%rip), %xmm0
0000000100598cc9	leaq	-0x60(%rbp), %rdi
0000000100598ccd	callq	__Z14floatToPackStrf            ## floatToPackStr(float)
0000000100598cd2	movzbl	-0x60(%rbp), %edx
0000000100598cd6	testb	$0x1, %dl
0000000100598cd9	je	0x100598e45
0000000100598cdf	movq	-0x50(%rbp), %rsi
0000000100598ce3	movq	-0x58(%rbp), %rdx
0000000100598ce7	jmp	0x100598e4b
0000000100598cec	movl	0x4(%r14), %esi
0000000100598cf0	testl	%esi, %esi
0000000100598cf2	setg	%al
0000000100598cf5	andb	0x20(%r14), %al
0000000100598cf9	cmpb	$0x1, %al
0000000100598cfb	jne	0x100598e23
0000000100598d01	leaq	-0x30(%rbp), %r8
0000000100598d05	movl	%esi, CONFIG_EMULATE_HARDWARE(%r8)
0000000100598d08	leaq	0x50668de(%rip), %rsi           ## literal pool for: "+{}"
0000000100598d0f	movl	$0x3, %edx
0000000100598d14	movl	$CONFIG_VP9, %ecx
0000000100598d19	movq	%rbx, %rdi
0000000100598d1c	callq	__ZN3fmt3v127vformatENS0_17basic_string_viewIcEENS0_17basic_format_argsINS0_7contextEEE ## fmt::v12::vformat(fmt::v12::basic_string_view<char>, fmt::v12::basic_format_args<fmt::v12::context>)
0000000100598d21	jmp	0x100598ec5
0000000100598d26	movss	0x4(%r14), %xmm0
0000000100598d2c	leaq	-0x30(%rbp), %r14
0000000100598d30	movq	%r14, %rdi
0000000100598d33	callq	__Z14floatToPackStrf            ## floatToPackStr(float)
0000000100598d38	leaq	0x5043ccf(%rip), %rsi           ## literal pool for: "ms"
0000000100598d3f	movl	$0x2, %edx
0000000100598d44	movq	%r14, %rdi
0000000100598d47	callq	0x104fe8516                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm
0000000100598d4c	jmp	0x100598de2
0000000100598d51	movss	0x4(%r14), %xmm0
0000000100598d57	cmpb	$0x1, 0x20(%r14)
0000000100598d5c	jne	0x100598e16
0000000100598d62	xorps	%xmm1, %xmm1
0000000100598d65	ucomiss	%xmm1, %xmm0
0000000100598d68	jbe	0x100598e16
0000000100598d6e	leaq	0x504f1d9(%rip), %rsi           ## literal pool for: "+"
0000000100598d75	leaq	-0x30(%rbp), %rdi
0000000100598d79	callq	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEC2B8ne200100ILi0EEEPKc ## std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>::basic_string[abi:ne200100]<0>(char const*)
0000000100598d7e	movss	0x4(%r14), %xmm0
0000000100598d84	leaq	-0x48(%rbp), %rdi
0000000100598d88	callq	__Z14floatToPackStrf            ## floatToPackStr(float)
0000000100598d8d	movzbl	-0x48(%rbp), %edx
0000000100598d91	testb	$0x1, %dl
0000000100598d94	je	0x100598ed1
0000000100598d9a	movq	-0x38(%rbp), %rsi
0000000100598d9e	movq	-0x40(%rbp), %rdx
0000000100598da2	jmp	0x100598ed7
0000000100598da7	xorps	%xmm0, %xmm0
0000000100598daa	movups	%xmm0, CONFIG_EMULATE_HARDWARE(%rbx)
0000000100598dad	movq	$CONFIG_EMULATE_HARDWARE, 0x10(%rbx)
0000000100598db5	jmp	0x100598ec5
0000000100598dba	mulss	0x4bf48fe(%rip), %xmm0
0000000100598dc2	leaq	-0x30(%rbp), %r14
0000000100598dc6	movq	%r14, %rdi
0000000100598dc9	callq	__Z14floatToPackStrf            ## floatToPackStr(float)
0000000100598dce	leaq	0x505c28b(%rip), %rsi           ## literal pool for: "%"
0000000100598dd5	movl	$CONFIG_VP9, %edx
0000000100598dda	movq	%r14, %rdi
0000000100598ddd	callq	0x104fe8516                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm
0000000100598de2	movq	0x10(%rax), %rcx
0000000100598de6	movq	%rcx, 0x10(%rbx)
0000000100598dea	movups	CONFIG_EMULATE_HARDWARE(%rax), %xmm0
0000000100598ded	movups	%xmm0, CONFIG_EMULATE_HARDWARE(%rbx)
0000000100598df0	xorps	%xmm0, %xmm0
0000000100598df3	movups	%xmm0, CONFIG_EMULATE_HARDWARE(%rax)
0000000100598df6	movq	$CONFIG_EMULATE_HARDWARE, 0x10(%rax)
0000000100598dfe	testb	$0x1, -0x30(%rbp)
0000000100598e02	je	0x100598ec5
0000000100598e08	movq	-0x20(%rbp), %rdi
0000000100598e0c	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
0000000100598e11	jmp	0x100598ec5
0000000100598e16	movq	%rbx, %rdi
0000000100598e19	callq	__Z14floatToPackStrf            ## floatToPackStr(float)
0000000100598e1e	jmp	0x100598ec5
0000000100598e23	movq	%rbx, %rdi
0000000100598e26	callq	__Z8intToStri                   ## intToStr(int)
0000000100598e2b	jmp	0x100598ec5
0000000100598e30	movq	0x10(%r14), %rdx
0000000100598e34	movq	0x18(%r14), %rsi
0000000100598e38	movq	%rbx, %rdi
0000000100598e3b	callq	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE25__init_copy_ctor_externalEPKcm ## std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>::__init_copy_ctor_external(char const*, unsigned long)
0000000100598e40	jmp	0x100598ec5
0000000100598e45	shrl	%edx
0000000100598e47	leaq	-0x5f(%rbp), %rsi
0000000100598e4b	leaq	-0x48(%rbp), %rdi
0000000100598e4f	callq	0x104fe8516                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm
0000000100598e54	movq	0x10(%rax), %rcx
0000000100598e58	leaq	-0x30(%rbp), %rdi
0000000100598e5c	movq	%rcx, 0x10(%rdi)
0000000100598e60	movups	CONFIG_EMULATE_HARDWARE(%rax), %xmm0
0000000100598e63	movaps	%xmm0, CONFIG_EMULATE_HARDWARE(%rdi)
0000000100598e66	xorps	%xmm0, %xmm0
0000000100598e69	movups	%xmm0, CONFIG_EMULATE_HARDWARE(%rax)
0000000100598e6c	movq	$CONFIG_EMULATE_HARDWARE, 0x10(%rax)
0000000100598e74	leaq	0x505c1e5(%rip), %rsi           ## literal pool for: "%"
0000000100598e7b	movl	$CONFIG_VP9, %edx
0000000100598e80	callq	0x104fe8516                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm
0000000100598e85	movq	0x10(%rax), %rcx
0000000100598e89	movq	%rcx, 0x10(%rbx)
0000000100598e8d	movups	CONFIG_EMULATE_HARDWARE(%rax), %xmm0
0000000100598e90	movups	%xmm0, CONFIG_EMULATE_HARDWARE(%rbx)
0000000100598e93	xorps	%xmm0, %xmm0
0000000100598e96	movups	%xmm0, CONFIG_EMULATE_HARDWARE(%rax)
0000000100598e99	movq	$CONFIG_EMULATE_HARDWARE, 0x10(%rax)
0000000100598ea1	testb	$0x1, -0x30(%rbp)
0000000100598ea5	je	0x100598eb0
0000000100598ea7	movq	-0x20(%rbp), %rdi
0000000100598eab	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
0000000100598eb0	testb	$0x1, -0x60(%rbp)
0000000100598eb4	je	0x100598ebf
0000000100598eb6	movq	-0x50(%rbp), %rdi
0000000100598eba	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
0000000100598ebf	testb	$0x1, -0x48(%rbp)
0000000100598ec3	jne	0x100598f14
0000000100598ec5	movq	%rbx, %rax
0000000100598ec8	addq	$0x50, %rsp
0000000100598ecc	popq	%rbx
0000000100598ecd	popq	%r14
0000000100598ecf	popq	%rbp
0000000100598ed0	retq
0000000100598ed1	shrl	%edx
0000000100598ed3	leaq	-0x47(%rbp), %rsi
0000000100598ed7	leaq	-0x30(%rbp), %rdi
0000000100598edb	callq	0x104fe8516                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm
0000000100598ee0	movq	0x10(%rax), %rcx
0000000100598ee4	movq	%rcx, 0x10(%rbx)
0000000100598ee8	movups	CONFIG_EMULATE_HARDWARE(%rax), %xmm0
0000000100598eeb	movups	%xmm0, CONFIG_EMULATE_HARDWARE(%rbx)
0000000100598eee	xorps	%xmm0, %xmm0
0000000100598ef1	movups	%xmm0, CONFIG_EMULATE_HARDWARE(%rax)
0000000100598ef4	movq	$CONFIG_EMULATE_HARDWARE, 0x10(%rax)
0000000100598efc	testb	$0x1, -0x48(%rbp)
0000000100598f00	je	0x100598dfe
0000000100598f06	movq	-0x38(%rbp), %rdi
0000000100598f0a	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
0000000100598f0f	jmp	0x100598dfe
0000000100598f14	movq	-0x38(%rbp), %rdi
0000000100598f18	jmp	0x100598e0c
0000000100598f1d	movq	%rax, %rbx
0000000100598f20	testb	$0x1, -0x30(%rbp)
0000000100598f24	je	0x100598f48
0000000100598f26	movq	-0x20(%rbp), %rdi
0000000100598f2a	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
0000000100598f2f	jmp	0x100598f48
0000000100598f31	movq	%rax, %rbx
0000000100598f34	testb	$0x1, -0x48(%rbp)
0000000100598f38	je	0x100598f71
0000000100598f3a	movq	-0x38(%rbp), %rdi
0000000100598f3e	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
0000000100598f43	jmp	0x100598f71
0000000100598f45	movq	%rax, %rbx
0000000100598f48	testb	$0x1, -0x60(%rbp)
0000000100598f4c	je	0x100598f5e
0000000100598f4e	movq	-0x50(%rbp), %rdi
0000000100598f52	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
0000000100598f57	jmp	0x100598f5e
0000000100598f59	jmp	0x100598f6e
0000000100598f5b	movq	%rax, %rbx
0000000100598f5e	testb	$0x1, -0x48(%rbp)
0000000100598f62	je	0x100598f80
0000000100598f64	movq	-0x38(%rbp), %rdi
0000000100598f68	jmp	0x100598f7b
0000000100598f6a	jmp	0x100598f6e
0000000100598f6c	jmp	0x100598f6e
0000000100598f6e	movq	%rax, %rbx
0000000100598f71	testb	$0x1, -0x30(%rbp)
0000000100598f75	je	0x100598f80
0000000100598f77	movq	-0x20(%rbp), %rdi
0000000100598f7b	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
0000000100598f80	movq	%rbx, %rdi
0000000100598f83	callq	0x104fe8456                     ## symbol stub for: __Unwind_Resume
