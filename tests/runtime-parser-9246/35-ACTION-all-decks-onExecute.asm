__ZN16ACTION_all_decks9onExecuteEv [0x1000fe392, 0x1000fe4ee):
00000001000fe392	pushq	%rbp
00000001000fe393	movq	%rsp, %rbp
00000001000fe396	pushq	%r15
00000001000fe398	pushq	%r14
00000001000fe39a	pushq	%r13
00000001000fe39c	pushq	%r12
00000001000fe39e	pushq	%rbx
00000001000fe39f	subq	$0x28, %rsp
00000001000fe3a3	movq	%rdi, %rbx
00000001000fe3a6	callq	__ZN16ACTION_all_decks4initEv   ## ACTION_all_decks::init()
00000001000fe3ab	movl	$0x80004005, %r14d              ## imm = 0x80004005
00000001000fe3b1	testb	%al, %al
00000001000fe3b3	je	0x1000fe4c2
00000001000fe3b9	movq	0x70(%rbx), %rdi
00000001000fe3bd	testq	%rdi, %rdi
00000001000fe3c0	je	0x1000fe40c
00000001000fe3c2	leaq	__ZTI7IAction(%rip), %rsi       ## typeinfo for IAction
00000001000fe3c9	leaq	__ZTI13IActionSwitch(%rip), %rdx ## typeinfo for IActionSwitch
00000001000fe3d0	xorl	%ecx, %ecx
00000001000fe3d2	callq	0x104fe87c8                     ## symbol stub for: ___dynamic_cast
00000001000fe3d7	testq	%rax, %rax
00000001000fe3da	je	0x1000fe40c
00000001000fe3dc	movq	%rax, %r15
00000001000fe3df	movq	0x50(%rbx), %rdx
00000001000fe3e3	movq	%rax, %rdi
00000001000fe3e6	movl	$CONFIG_VP9, %esi
00000001000fe3eb	callq	__ZN7IAction9queryBoolEjP11IController ## IAction::queryBool(unsigned int, IController*)
00000001000fe3f0	movl	%eax, %r14d
00000001000fe3f3	movq	0x68(%rbx), %rax
00000001000fe3f7	movq	%rax, 0x68(%r15)
00000001000fe3fb	movl	0x70(%r15), %esi
00000001000fe3ff	movq	%r15, %rdi
00000001000fe402	callq	__ZN7IAction8getParamEi         ## IAction::getParam(int)
00000001000fe407	cmpl	$0x0, CONFIG_EMULATE_HARDWARE(%rax)
00000001000fe40a	je	0x1000fe44c
00000001000fe40c	leaq	_nbDecks(%rip), %r12
00000001000fe413	cmpq	$0x0, CONFIG_EMULATE_HARDWARE(%r12)
00000001000fe418	je	0x1000fe4bf
00000001000fe41e	xorl	%r15d, %r15d
00000001000fe421	xorl	%r14d, %r14d
00000001000fe424	movq	0x70(%rbx), %rdi
00000001000fe428	movq	0x68(%rbx), %rsi
00000001000fe42c	incq	%r15
00000001000fe42f	movl	0x58(%rbx), %ecx
00000001000fe432	movq	0x50(%rbx), %r8
00000001000fe436	movl	%r15d, %edx
00000001000fe439	callq	__ZN7IAction7executeEP12SActionParamjjP11IController ## IAction::execute(SActionParam*, unsigned int, unsigned int, IController*)
00000001000fe43e	testl	%eax, %eax
00000001000fe440	cmovnel	%eax, %r14d
00000001000fe444	cmpq	%r15, CONFIG_EMULATE_HARDWARE(%r12)
00000001000fe448	ja	0x1000fe424
00000001000fe44a	jmp	0x1000fe4c2
00000001000fe44c	xorps	%xmm0, %xmm0
00000001000fe44f	movups	%xmm0, -0x48(%rbp)
00000001000fe453	movq	$CONFIG_EMULATE_HARDWARE, -0x38(%rbp)
00000001000fe45b	xorb	$0x1, %r14b
00000001000fe45f	movzbl	%r14b, %eax
00000001000fe463	movl	$0x626f6f6c, -0x50(%rbp)        ## imm = 0x626F6F6C
00000001000fe46a	movl	%eax, -0x4c(%rbp)
00000001000fe46d	movb	$0x0, -0x30(%rbp)
00000001000fe471	leaq	_nbDecks(%rip), %r13
00000001000fe478	cmpq	$0x0, (%r13)
00000001000fe47d	je	0x1000fe4bf
00000001000fe47f	xorl	%r15d, %r15d
00000001000fe482	leaq	-0x50(%rbp), %r12
00000001000fe486	xorl	%r14d, %r14d
00000001000fe489	movq	0x70(%rbx), %rdi
00000001000fe48d	incq	%r15
00000001000fe490	movl	0x58(%rbx), %ecx
00000001000fe493	movq	0x50(%rbx), %r8
00000001000fe497	movq	%r12, %rsi
00000001000fe49a	movl	%r15d, %edx
00000001000fe49d	callq	__ZN7IAction7executeEP12SActionParamjjP11IController ## IAction::execute(SActionParam*, unsigned int, unsigned int, IController*)
00000001000fe4a2	testl	%eax, %eax
00000001000fe4a4	cmovnel	%eax, %r14d
00000001000fe4a8	cmpq	%r15, (%r13)
00000001000fe4ac	ja	0x1000fe489
00000001000fe4ae	testb	$0x1, -0x48(%rbp)
00000001000fe4b2	je	0x1000fe4c2
00000001000fe4b4	movq	-0x38(%rbp), %rdi
00000001000fe4b8	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
00000001000fe4bd	jmp	0x1000fe4c2
00000001000fe4bf	xorl	%r14d, %r14d
00000001000fe4c2	movl	%r14d, %eax
00000001000fe4c5	addq	$0x28, %rsp
00000001000fe4c9	popq	%rbx
00000001000fe4ca	popq	%r12
00000001000fe4cc	popq	%r13
00000001000fe4ce	popq	%r14
00000001000fe4d0	popq	%r15
00000001000fe4d2	popq	%rbp
00000001000fe4d3	retq
00000001000fe4d4	movq	%rax, %rbx
00000001000fe4d7	testb	$0x1, -0x48(%rbp)
00000001000fe4db	je	0x1000fe4e6
00000001000fe4dd	movq	-0x38(%rbp), %rdi
00000001000fe4e1	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
00000001000fe4e6	movq	%rbx, %rdi
00000001000fe4e9	callq	0x104fe8456                     ## symbol stub for: __Unwind_Resume
