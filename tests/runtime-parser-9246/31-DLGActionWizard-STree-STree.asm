__ZN15DLGActionWizard5STreeD2Ev [0x1006c76f4, 0x1006c779c):
00000001006c76f4	pushq	%rbp
00000001006c76f5	movq	%rsp, %rbp
00000001006c76f8	pushq	%r14
00000001006c76fa	pushq	%rbx
00000001006c76fb	movq	%rdi, %rbx
00000001006c76fe	movq	0x18(%rdi), %r14
00000001006c7702	testq	%r14, %r14
00000001006c7705	je	0x1006c771f
00000001006c7707	movq	%r14, %rdi
00000001006c770a	callq	__ZN15DLGActionWizard5STreeD2Ev ## DLGActionWizard::STree::~STree()
00000001006c770f	movq	%r14, %rdi
00000001006c7712	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
00000001006c7717	movq	$CONFIG_EMULATE_HARDWARE, 0x18(%rbx)
00000001006c771f	movq	0x20(%rbx), %r14
00000001006c7723	testq	%r14, %r14
00000001006c7726	je	0x1006c7740
00000001006c7728	movq	%r14, %rdi
00000001006c772b	callq	__ZN15DLGActionWizard5STreeD2Ev ## DLGActionWizard::STree::~STree()
00000001006c7730	movq	%r14, %rdi
00000001006c7733	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
00000001006c7738	movq	$CONFIG_EMULATE_HARDWARE, 0x20(%rbx)
00000001006c7740	movq	0x28(%rbx), %r14
00000001006c7744	testq	%r14, %r14
00000001006c7747	je	0x1006c7761
00000001006c7749	movq	%r14, %rdi
00000001006c774c	callq	__ZN15DLGActionWizard5STreeD2Ev ## DLGActionWizard::STree::~STree()
00000001006c7751	movq	%r14, %rdi
00000001006c7754	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
00000001006c7759	movq	$CONFIG_EMULATE_HARDWARE, 0x28(%rbx)
00000001006c7761	movq	0x40(%rbx), %r14
00000001006c7765	testq	%r14, %r14
00000001006c7768	je	0x1006c7782
00000001006c776a	movq	%r14, %rdi
00000001006c776d	callq	__ZN15DLGActionWizard5STreeD2Ev ## DLGActionWizard::STree::~STree()
00000001006c7772	movq	%r14, %rdi
00000001006c7775	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
00000001006c777a	movq	$CONFIG_EMULATE_HARDWARE, 0x40(%rbx)
00000001006c7782	movq	CONFIG_EMULATE_HARDWARE(%rbx), %rdi
00000001006c7785	testq	%rdi, %rdi
00000001006c7788	je	0x1006c7797
00000001006c778a	movq	%rdi, 0x8(%rbx)
00000001006c778e	popq	%rbx
00000001006c778f	popq	%r14
00000001006c7791	popq	%rbp
00000001006c7792	jmp	0x104fe873e                     ## symbol stub for: __ZdlPv
00000001006c7797	popq	%rbx
00000001006c7798	popq	%r14
00000001006c779a	popq	%rbp
00000001006c779b	retq
