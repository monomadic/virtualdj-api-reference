__ZN15DLGActionWizard5STree5clearEv [0x1006c6748, 0x1006c67ea):
00000001006c6748	pushq	%rbp
00000001006c6749	movq	%rsp, %rbp
00000001006c674c	pushq	%r14
00000001006c674e	pushq	%rbx
00000001006c674f	movq	%rdi, %rbx
00000001006c6752	movq	0x18(%rdi), %r14
00000001006c6756	testq	%r14, %r14
00000001006c6759	je	0x1006c6773
00000001006c675b	movq	%r14, %rdi
00000001006c675e	callq	__ZN15DLGActionWizard5STreeD2Ev ## DLGActionWizard::STree::~STree()
00000001006c6763	movq	%r14, %rdi
00000001006c6766	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
00000001006c676b	movq	$CONFIG_EMULATE_HARDWARE, 0x18(%rbx)
00000001006c6773	movq	0x20(%rbx), %r14
00000001006c6777	testq	%r14, %r14
00000001006c677a	je	0x1006c6794
00000001006c677c	movq	%r14, %rdi
00000001006c677f	callq	__ZN15DLGActionWizard5STreeD2Ev ## DLGActionWizard::STree::~STree()
00000001006c6784	movq	%r14, %rdi
00000001006c6787	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
00000001006c678c	movq	$CONFIG_EMULATE_HARDWARE, 0x20(%rbx)
00000001006c6794	movq	0x28(%rbx), %r14
00000001006c6798	testq	%r14, %r14
00000001006c679b	je	0x1006c67b5
00000001006c679d	movq	%r14, %rdi
00000001006c67a0	callq	__ZN15DLGActionWizard5STreeD2Ev ## DLGActionWizard::STree::~STree()
00000001006c67a5	movq	%r14, %rdi
00000001006c67a8	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
00000001006c67ad	movq	$CONFIG_EMULATE_HARDWARE, 0x28(%rbx)
00000001006c67b5	movq	0x40(%rbx), %r14
00000001006c67b9	testq	%r14, %r14
00000001006c67bc	je	0x1006c67d6
00000001006c67be	movq	%r14, %rdi
00000001006c67c1	callq	__ZN15DLGActionWizard5STreeD2Ev ## DLGActionWizard::STree::~STree()
00000001006c67c6	movq	%r14, %rdi
00000001006c67c9	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
00000001006c67ce	movq	$CONFIG_EMULATE_HARDWARE, 0x40(%rbx)
00000001006c67d6	movq	CONFIG_EMULATE_HARDWARE(%rbx), %rax
00000001006c67d9	movq	%rax, 0x8(%rbx)
00000001006c67dd	xorps	%xmm0, %xmm0
00000001006c67e0	movups	%xmm0, 0x30(%rbx)
00000001006c67e4	popq	%rbx
00000001006c67e5	popq	%r14
00000001006c67e7	popq	%rbp
00000001006c67e8	retq
00000001006c67e9	nop
