__Z26createAction_combine_queryP7IAction [0x1000fddf5, 0x1000fde45):
00000001000fddf5	pushq	%rbp
00000001000fddf6	movq	%rsp, %rbp
00000001000fddf9	pushq	%r14
00000001000fddfb	pushq	%rbx
00000001000fddfc	movq	%rdi, %r14
00000001000fddff	movl	$FGData.ar_coeffs_uv, %edi
00000001000fde04	callq	0x104fe8750                     ## symbol stub for: __Znwm
00000001000fde09	movq	%rax, %rbx
00000001000fde0c	movq	%rax, %rdi
00000001000fde0f	callq	__ZN7IActionC2Ev                ## IAction::IAction()
00000001000fde14	leaq	0x56e045d(%rip), %rax
00000001000fde1b	movq	%rax, CONFIG_EMULATE_HARDWARE(%rbx)
00000001000fde1e	movl	$FGData.num_y_points, 0xc(%rbx)
00000001000fde25	movq	%r14, 0x70(%rbx)
00000001000fde29	movq	%rbx, %rax
00000001000fde2c	popq	%rbx
00000001000fde2d	popq	%r14
00000001000fde2f	popq	%rbp
00000001000fde30	retq
00000001000fde31	movq	%rax, %r14
00000001000fde34	movq	%rbx, %rdi
00000001000fde37	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
00000001000fde3c	movq	%r14, %rdi
00000001000fde3f	callq	0x104fe8456                     ## symbol stub for: __Unwind_Resume
00000001000fde44	addb	%dl, 0x48(%rbp)
