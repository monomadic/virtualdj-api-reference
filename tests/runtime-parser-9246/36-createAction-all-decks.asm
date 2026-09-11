__Z22createAction_all_decksv [0x1000fe030, 0x1000fe0a0):
00000001000fe030	pushq	%rbp
00000001000fe031	movq	%rsp, %rbp
00000001000fe034	pushq	%r14
00000001000fe036	pushq	%rbx
00000001000fe037	movl	$FGData.ar_coeffs_uv, %edi
00000001000fe03c	callq	0x104fe8750                     ## symbol stub for: __Znwm
00000001000fe041	movq	%rax, %rbx
00000001000fe044	xorps	%xmm0, %xmm0
00000001000fe047	movaps	%xmm0, CONFIG_EMULATE_HARDWARE(%rax)
00000001000fe04a	movaps	%xmm0, 0x10(%rax)
00000001000fe04e	movaps	%xmm0, 0x20(%rax)
00000001000fe052	movaps	%xmm0, 0x30(%rax)
00000001000fe056	movaps	%xmm0, 0x40(%rax)
00000001000fe05a	movaps	%xmm0, 0x50(%rax)
00000001000fe05e	movaps	%xmm0, 0x60(%rax)
00000001000fe062	movq	$CONFIG_EMULATE_HARDWARE, 0x70(%rax)
00000001000fe06a	movq	%rax, %rdi
00000001000fe06d	callq	__ZN7IActionC2Ev                ## IAction::IAction()
00000001000fe072	leaq	0x56e04a7(%rip), %rax
00000001000fe079	movq	%rax, CONFIG_EMULATE_HARDWARE(%rbx)
00000001000fe07c	movq	$CONFIG_EMULATE_HARDWARE, 0x70(%rbx)
00000001000fe084	movq	%rbx, %rax
00000001000fe087	popq	%rbx
00000001000fe088	popq	%r14
00000001000fe08a	popq	%rbp
00000001000fe08b	retq
00000001000fe08c	movq	%rax, %r14
00000001000fe08f	movq	%rbx, %rdi
00000001000fe092	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
00000001000fe097	movq	%r14, %rdi
00000001000fe09a	callq	0x104fe8456                     ## symbol stub for: __Unwind_Resume
00000001000fe09f	addb	%dl, 0x48(%rbp)
