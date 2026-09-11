__ZN15DLGActionWizard5STree8toStringEv [0x1006c68d2, 0x1006c6a46):
00000001006c68d2	pushq	%rbp
00000001006c68d3	movq	%rsp, %rbp
00000001006c68d6	pushq	%r15
00000001006c68d8	pushq	%r14
00000001006c68da	pushq	%rbx
00000001006c68db	subq	$0x18, %rsp
00000001006c68df	movq	%rsi, %r14
00000001006c68e2	movq	%rdi, %rbx
00000001006c68e5	xorps	%xmm0, %xmm0
00000001006c68e8	movups	%xmm0, CONFIG_EMULATE_HARDWARE(%rdi)
00000001006c68eb	movq	$CONFIG_EMULATE_HARDWARE, 0x10(%rdi)
00000001006c68f3	movq	CONFIG_EMULATE_HARDWARE(%rsi), %rax
00000001006c68f6	cmpq	%rax, 0x8(%rsi)
00000001006c68fa	je	0x1006c693a
00000001006c68fc	xorl	%r15d, %r15d
00000001006c68ff	movq	CONFIG_EMULATE_HARDWARE(%rax,%r15,8), %rsi
00000001006c6903	movzbl	0x18(%rsi), %edx
00000001006c6907	testb	$0x1, %dl
00000001006c690a	je	0x1006c6916
00000001006c690c	movq	0x20(%rsi), %rdx
00000001006c6910	movq	0x28(%rsi), %rsi
00000001006c6914	jmp	0x1006c691c
00000001006c6916	addq	$0x19, %rsi
00000001006c691a	shrl	%edx
00000001006c691c	movq	%rbx, %rdi
00000001006c691f	callq	0x104fe8516                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm
00000001006c6924	incq	%r15
00000001006c6927	movq	CONFIG_EMULATE_HARDWARE(%r14), %rax
00000001006c692a	movq	0x8(%r14), %rcx
00000001006c692e	subq	%rax, %rcx
00000001006c6931	sarq	$0x3, %rcx
00000001006c6935	cmpq	%rcx, %r15
00000001006c6938	jb	0x1006c68ff
00000001006c693a	movq	0x28(%r14), %rsi
00000001006c693e	testq	%rsi, %rsi
00000001006c6941	je	0x1006c697c
00000001006c6943	leaq	-0x30(%rbp), %rdi
00000001006c6947	callq	__ZN15DLGActionWizard5STree8toStringEv ## DLGActionWizard::STree::toString()
00000001006c694c	movzbl	-0x30(%rbp), %edx
00000001006c6950	testb	$0x1, %dl
00000001006c6953	je	0x1006c695f
00000001006c6955	movq	-0x20(%rbp), %rsi
00000001006c6959	movq	-0x28(%rbp), %rdx
00000001006c695d	jmp	0x1006c6965
00000001006c695f	shrl	%edx
00000001006c6961	leaq	-0x2f(%rbp), %rsi
00000001006c6965	movq	%rbx, %rdi
00000001006c6968	callq	0x104fe8516                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm
00000001006c696d	testb	$0x1, -0x30(%rbp)
00000001006c6971	je	0x1006c697c
00000001006c6973	movq	-0x20(%rbp), %rdi
00000001006c6977	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
00000001006c697c	movq	0x18(%r14), %rsi
00000001006c6980	testq	%rsi, %rsi
00000001006c6983	je	0x1006c69be
00000001006c6985	leaq	-0x30(%rbp), %rdi
00000001006c6989	callq	__ZN15DLGActionWizard5STree8toStringEv ## DLGActionWizard::STree::toString()
00000001006c698e	movzbl	-0x30(%rbp), %edx
00000001006c6992	testb	$0x1, %dl
00000001006c6995	je	0x1006c69a1
00000001006c6997	movq	-0x20(%rbp), %rsi
00000001006c699b	movq	-0x28(%rbp), %rdx
00000001006c699f	jmp	0x1006c69a7
00000001006c69a1	shrl	%edx
00000001006c69a3	leaq	-0x2f(%rbp), %rsi
00000001006c69a7	movq	%rbx, %rdi
00000001006c69aa	callq	0x104fe8516                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm
00000001006c69af	testb	$0x1, -0x30(%rbp)
00000001006c69b3	je	0x1006c69be
00000001006c69b5	movq	-0x20(%rbp), %rdi
00000001006c69b9	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
00000001006c69be	movq	0x20(%r14), %rsi
00000001006c69c2	testq	%rsi, %rsi
00000001006c69c5	je	0x1006c6a00
00000001006c69c7	leaq	-0x30(%rbp), %rdi
00000001006c69cb	callq	__ZN15DLGActionWizard5STree8toStringEv ## DLGActionWizard::STree::toString()
00000001006c69d0	movzbl	-0x30(%rbp), %edx
00000001006c69d4	testb	$0x1, %dl
00000001006c69d7	je	0x1006c69e3
00000001006c69d9	movq	-0x20(%rbp), %rsi
00000001006c69dd	movq	-0x28(%rbp), %rdx
00000001006c69e1	jmp	0x1006c69e9
00000001006c69e3	shrl	%edx
00000001006c69e5	leaq	-0x2f(%rbp), %rsi
00000001006c69e9	movq	%rbx, %rdi
00000001006c69ec	callq	0x104fe8516                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm
00000001006c69f1	testb	$0x1, -0x30(%rbp)
00000001006c69f5	je	0x1006c6a00
00000001006c69f7	movq	-0x20(%rbp), %rdi
00000001006c69fb	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
00000001006c6a00	movq	%rbx, %rax
00000001006c6a03	addq	$0x18, %rsp
00000001006c6a07	popq	%rbx
00000001006c6a08	popq	%r14
00000001006c6a0a	popq	%r15
00000001006c6a0c	popq	%rbp
00000001006c6a0d	retq
00000001006c6a0e	jmp	0x1006c6a16
00000001006c6a10	jmp	0x1006c6a2c
00000001006c6a12	jmp	0x1006c6a16
00000001006c6a14	jmp	0x1006c6a2c
00000001006c6a16	movq	%rax, %r14
00000001006c6a19	testb	$0x1, -0x30(%rbp)
00000001006c6a1d	je	0x1006c6a2f
00000001006c6a1f	movq	-0x20(%rbp), %rdi
00000001006c6a23	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
00000001006c6a28	jmp	0x1006c6a2f
00000001006c6a2a	jmp	0x1006c6a2c
00000001006c6a2c	movq	%rax, %r14
00000001006c6a2f	testb	$0x1, CONFIG_EMULATE_HARDWARE(%rbx)
00000001006c6a32	je	0x1006c6a3d
00000001006c6a34	movq	0x10(%rbx), %rdi
00000001006c6a38	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
00000001006c6a3d	movq	%r14, %rdi
00000001006c6a40	callq	0x104fe8456                     ## symbol stub for: __Unwind_Resume
00000001006c6a45	nop
