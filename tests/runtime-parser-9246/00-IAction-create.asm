__ZN7IAction6createEPKcPS1_i [0x100596f1c, 0x1005984e0):
0000000100596f1c	pushq	%rbp
0000000100596f1d	movq	%rsp, %rbp
0000000100596f20	pushq	%r15
0000000100596f22	pushq	%r14
0000000100596f24	pushq	%r13
0000000100596f26	pushq	%r12
0000000100596f28	pushq	%rbx
0000000100596f29	subq	$rf.n_mfmvs, %rsp
0000000100596f30	movq	%rsi, %r13
0000000100596f33	movq	%rdi, %r14
0000000100596f36	movl	%edx, -0x34(%rbp)
0000000100596f39	testq	%rdi, %rdi
0000000100596f3c	je	0x100596f78
0000000100596f3e	movb	CONFIG_EMULATE_HARDWARE(%r14), %al
0000000100596f41	testb	%al, %al
0000000100596f43	je	0x100596f78
0000000100596f45	cmpb	$0x1, __ZN7IAction8isRemoteE(%rip) ## IAction::isRemote
0000000100596f4c	movabsq	$0x100002600, %r12              ## imm = 0x100002600
0000000100596f56	jne	0x1005974cf
0000000100596f5c	movq	%r14, %rbx
0000000100596f5f	cmpb	$0x20, %al
0000000100596f61	ja	0x100596f89
0000000100596f63	movzbl	%al, %eax
0000000100596f66	btq	%rax, %r12
0000000100596f6a	jae	0x100596f89
0000000100596f6c	movb	0x1(%r14), %al
0000000100596f70	incq	%r14
0000000100596f73	incq	%rbx
0000000100596f76	jmp	0x100596f5f
0000000100596f78	testq	%r13, %r13
0000000100596f7b	je	0x100596f81
0000000100596f7d	movq	%r14, (%r13)
0000000100596f81	xorl	%r15d, %r15d
0000000100596f84	jmp	0x100598350
0000000100596f89	movq	%r14, -0xa0(%rbp)
0000000100596f90	leaq	0x4(%r14), %rax
0000000100596f94	xorl	%ecx, %ecx
0000000100596f96	leaq	0x5044b12(%rip), %rdx           ## literal pool for: "deck"
0000000100596f9d	cmpq	$0x4, %rcx
0000000100596fa1	je	0x100597006
0000000100596fa3	movzbl	CONFIG_EMULATE_HARDWARE(%r14,%rcx), %esi
0000000100596fa8	leal	-0x41(%rsi), %edi
0000000100596fab	movl	%esi, %r8d
0000000100596fae	orb	$0x20, %r8b
0000000100596fb2	cmpb	$0x1a, %dil
0000000100596fb6	movzbl	%r8b, %edi
0000000100596fba	cmovael	%esi, %edi
0000000100596fbd	leaq	0x1(%rcx), %rsi
0000000100596fc1	cmpb	CONFIG_EMULATE_HARDWARE(%rcx,%rdx), %dil
0000000100596fc5	movq	%rsi, %rcx
0000000100596fc8	je	0x100596f9d
0000000100596fca	leaq	0x4(%r14), %rax
0000000100596fce	xorl	%ecx, %ecx
0000000100596fd0	leaq	0x5080c2d(%rip), %rdx           ## literal pool for: "zone"
0000000100596fd7	cmpq	$0x4, %rcx
0000000100596fdb	je	0x100597035
0000000100596fdd	movzbl	CONFIG_EMULATE_HARDWARE(%r14,%rcx), %esi
0000000100596fe2	leal	-0x41(%rsi), %edi
0000000100596fe5	movl	%esi, %r8d
0000000100596fe8	orb	$0x20, %r8b
0000000100596fec	cmpb	$0x1a, %dil
0000000100596ff0	movzbl	%r8b, %edi
0000000100596ff4	cmovael	%esi, %edi
0000000100596ff7	leaq	0x1(%rcx), %rsi
0000000100596ffb	cmpb	CONFIG_EMULATE_HARDWARE(%rcx,%rdx), %dil
0000000100596fff	movq	%rsi, %rcx
0000000100597002	je	0x100596fd7
0000000100597004	jmp	0x100597077
0000000100597006	movzbl	CONFIG_EMULATE_HARDWARE(%rax), %ecx
0000000100597009	cmpq	$0x29, %rcx
000000010059700d	ja	0x100596fca
000000010059700f	movabsq	$0x20100000001, %rdx            ## imm = 0x20100000001
0000000100597019	btq	%rcx, %rdx
000000010059701d	jae	0x100596fca
000000010059701f	cmpb	$0x20, %cl
0000000100597022	ja	0x100597064
0000000100597024	movzbl	%cl, %ecx
0000000100597027	btq	%rcx, %r12
000000010059702b	jae	0x100597064
000000010059702d	movb	0x1(%rax), %cl
0000000100597030	incq	%rax
0000000100597033	jmp	0x10059701f
0000000100597035	movzbl	CONFIG_EMULATE_HARDWARE(%rax), %ecx
0000000100597038	cmpq	$0x29, %rcx
000000010059703c	ja	0x100597077
000000010059703e	movabsq	$0x20100000001, %rdx            ## imm = 0x20100000001
0000000100597048	btq	%rcx, %rdx
000000010059704c	jae	0x100597077
000000010059704e	cmpb	$0x20, %cl
0000000100597051	ja	0x100597064
0000000100597053	movzbl	%cl, %ecx
0000000100597056	btq	%rcx, %r12
000000010059705a	jae	0x100597064
000000010059705c	movb	0x1(%rax), %cl
000000010059705f	incq	%rax
0000000100597062	jmp	0x10059704e
0000000100597064	leaq	-0xa0(%rbp), %rdi
000000010059706b	movq	%rax, CONFIG_EMULATE_HARDWARE(%rdi)
000000010059706e	leaq	-0x34(%rbp), %rsi
0000000100597072	callq	__ZN7IAction9deckMatchERPKcRi   ## IAction::deckMatch(char const*&, int&)
0000000100597077	leaq	0x505aa7a(%rip), %rsi           ## literal pool for: "skin_pannel"
000000010059707e	movq	%r14, %rdi
0000000100597081	callq	0x104fe92de                     ## symbol stub for: _strstr
0000000100597086	testq	%rax, %rax
0000000100597089	jne	0x1005974cf
000000010059708f	leaq	0x505aa2d(%rip), %rsi           ## literal pool for: "skin_panel"
0000000100597096	movq	%r14, %rdi
0000000100597099	callq	0x104fe92de                     ## symbol stub for: _strstr
000000010059709e	testq	%rax, %rax
00000001005970a1	jne	0x1005974cf
00000001005970a7	leaq	0x5059174(%rip), %rsi           ## literal pool for: "get_time"
00000001005970ae	movq	%r14, %rdi
00000001005970b1	callq	__Z8isLeftCIPKcS0_              ## isLeftCI(char const*, char const*)
00000001005970b6	testb	%al, %al
00000001005970b8	jne	0x1005974cf
00000001005970be	leaq	0x5053d05(%rip), %rsi           ## literal pool for: "get rotation"
00000001005970c5	movq	%r14, %rdi
00000001005970c8	callq	__Z8isLeftCIPKcS0_              ## isLeftCI(char const*, char const*)
00000001005970cd	testb	%al, %al
00000001005970cf	jne	0x1005974cf
00000001005970d5	leaq	0x5058fca(%rip), %rsi           ## literal pool for: "get_rotation"
00000001005970dc	movq	%r14, %rdi
00000001005970df	callq	__Z8isLeftCIPKcS0_              ## isLeftCI(char const*, char const*)
00000001005970e4	testb	%al, %al
00000001005970e6	jne	0x1005974cf
00000001005970ec	leaq	0x505aa97(%rip), %rsi           ## literal pool for: "songpos_remain"
00000001005970f3	movq	%r14, %rdi
00000001005970f6	callq	__Z8isLeftCIPKcS0_              ## isLeftCI(char const*, char const*)
00000001005970fb	testb	%al, %al
00000001005970fd	jne	0x1005974cf
0000000100597103	leaq	0x5053ce4(%rip), %rsi           ## literal pool for: "get position"
000000010059710a	movq	%r14, %rdi
000000010059710d	callq	__Z8isLeftCIPKcS0_              ## isLeftCI(char const*, char const*)
0000000100597112	testb	%al, %al
0000000100597114	jne	0x1005974cf
000000010059711a	leaq	0x5058ee6(%rip), %rsi           ## literal pool for: "get_position"
0000000100597121	movq	%r14, %rdi
0000000100597124	callq	__Z8isLeftCIPKcS0_              ## isLeftCI(char const*, char const*)
0000000100597129	testb	%al, %al
000000010059712b	jne	0x1005974cf
0000000100597131	leaq	0x505ae46(%rip), %rsi           ## literal pool for: "zoom"
0000000100597138	movq	%r14, %rdi
000000010059713b	callq	__Z8isLeftCIPKcS0_              ## isLeftCI(char const*, char const*)
0000000100597140	testb	%al, %al
0000000100597142	jne	0x1005974cf
0000000100597148	leaq	0x5057abf(%rip), %rsi           ## literal pool for: "browser_window"
000000010059714f	movq	%r14, %rdi
0000000100597152	callq	__Z8isLeftCIPKcS0_              ## isLeftCI(char const*, char const*)
0000000100597157	testb	%al, %al
0000000100597159	jne	0x1005974cf
000000010059715f	leaq	0x505444e(%rip), %rsi           ## literal pool for: "sideview"
0000000100597166	movq	%r14, %rdi
0000000100597169	callq	__Z8isLeftCIPKcS0_              ## isLeftCI(char const*, char const*)
000000010059716e	testb	%al, %al
0000000100597170	jne	0x1005974cf
0000000100597176	leaq	0x505adbe(%rip), %rsi           ## literal pool for: "view_options"
000000010059717d	movq	%r14, %rdi
0000000100597180	callq	__Z8isLeftCIPKcS0_              ## isLeftCI(char const*, char const*)
0000000100597185	testb	%al, %al
0000000100597187	jne	0x1005974cf
000000010059718d	leaq	0x5058469(%rip), %rsi           ## literal pool for: "font_size"
0000000100597194	movq	%r14, %rdi
0000000100597197	callq	__Z8isLeftCIPKcS0_              ## isLeftCI(char const*, char const*)
000000010059719c	testb	%al, %al
000000010059719e	jne	0x1005974cf
00000001005971a4	leaq	0x505927b(%rip), %rsi           ## literal pool for: "goto_last_folder"
00000001005971ab	movq	%r14, %rdi
00000001005971ae	callq	__Z8isLeftCIPKcS0_              ## isLeftCI(char const*, char const*)
00000001005971b3	testb	%al, %al
00000001005971b5	jne	0x1005974cf
00000001005971bb	leaq	0x50579f0(%rip), %rsi           ## literal pool for: "browser_options"
00000001005971c2	movq	%r14, %rdi
00000001005971c5	callq	__Z8isLeftCIPKcS0_              ## isLeftCI(char const*, char const*)
00000001005971ca	testb	%al, %al
00000001005971cc	jne	0x1005974cf
00000001005971d2	leaq	0x5057a44(%rip), %rsi           ## literal pool for: "browser_zoom"
00000001005971d9	movq	%r14, %rdi
00000001005971dc	callq	__Z8isLeftCIPKcS0_              ## isLeftCI(char const*, char const*)
00000001005971e1	testb	%al, %al
00000001005971e3	jne	0x1005974cf
00000001005971e9	leaq	0x5058364(%rip), %rsi           ## literal pool for: "file_count"
00000001005971f0	movq	%r14, %rdi
00000001005971f3	callq	__Z8isLeftCIPKcS0_              ## isLeftCI(char const*, char const*)
00000001005971f8	testb	%al, %al
00000001005971fa	jne	0x1005974cf
0000000100597200	leaq	0x5059249(%rip), %rsi           ## literal pool for: "grid_view"
0000000100597207	movq	%r14, %rdi
000000010059720a	callq	__Z8isLeftCIPKcS0_              ## isLeftCI(char const*, char const*)
000000010059720f	testb	%al, %al
0000000100597211	jne	0x1005974cf
0000000100597217	leaq	0x50511b4(%rip), %rsi           ## literal pool for: "browser"
000000010059721e	movq	%r14, %rdi
0000000100597221	callq	__Z12strIsEqualCIPKcS0_         ## strIsEqualCI(char const*, char const*)
0000000100597226	testb	%al, %al
0000000100597228	jne	0x1005974cf
000000010059722e	movq	-0xa0(%rbp), %r15
0000000100597235	leaq	0x5050629(%rip), %rsi           ## literal pool for: "load"
000000010059723c	movq	%r15, %rdi
000000010059723f	callq	__Z12strIsEqualCIPKcS0_         ## strIsEqualCI(char const*, char const*)
0000000100597244	testb	%al, %al
0000000100597246	jne	0x1005974cf
000000010059724c	leaq	0x50809b6(%rip), %rsi           ## literal pool for: "load "
0000000100597253	movq	%r15, %rdi
0000000100597256	callq	__Z8isLeftCIPKcS0_              ## isLeftCI(char const*, char const*)
000000010059725b	testb	%al, %al
000000010059725d	jne	0x1005974cf
0000000100597263	leaq	0x5059f31(%rip), %rsi           ## literal pool for: "prelisten_options"
000000010059726a	movq	%r14, %rdi
000000010059726d	callq	__Z8isLeftCIPKcS0_              ## isLeftCI(char const*, char const*)
0000000100597272	testb	%al, %al
0000000100597274	jne	0x1005974cf
000000010059727a	leaq	0x505a7a7(%rip), %rsi           ## literal pool for: "sidereco_options"
0000000100597281	movq	%r14, %rdi
0000000100597284	callq	__Z8isLeftCIPKcS0_              ## isLeftCI(char const*, char const*)
0000000100597289	testb	%al, %al
000000010059728b	jne	0x1005974cf
0000000100597291	leaq	0x505a7a1(%rip), %rsi           ## literal pool for: "sidereco_song"
0000000100597298	movq	%r14, %rdi
000000010059729b	callq	__Z8isLeftCIPKcS0_              ## isLeftCI(char const*, char const*)
00000001005972a0	testb	%al, %al
00000001005972a2	jne	0x1005974cf
00000001005972a8	leaq	0x5057952(%rip), %rsi           ## literal pool for: "browser_sort"
00000001005972af	movq	%r14, %rdi
00000001005972b2	callq	__Z8isLeftCIPKcS0_              ## isLeftCI(char const*, char const*)
00000001005972b7	testb	%al, %al
00000001005972b9	jne	0x1005974cf
00000001005972bf	leaq	0x505791b(%rip), %rsi           ## literal pool for: "browser_scroll"
00000001005972c6	movq	%r14, %rdi
00000001005972c9	callq	__Z8isLeftCIPKcS0_              ## isLeftCI(char const*, char const*)
00000001005972ce	testb	%al, %al
00000001005972d0	jne	0x1005974cf
00000001005972d6	leaq	0x5059f2f(%rip), %rsi           ## literal pool for: "quick_filter"
00000001005972dd	movq	%r14, %rdi
00000001005972e0	callq	__Z8isLeftCIPKcS0_              ## isLeftCI(char const*, char const*)
00000001005972e5	testb	%al, %al
00000001005972e7	jne	0x1005974cf
00000001005972ed	leaq	0x50591e9(%rip), %rsi           ## literal pool for: "has_quick_filter"
00000001005972f4	movq	%r14, %rdi
00000001005972f7	callq	__Z8isLeftCIPKcS0_              ## isLeftCI(char const*, char const*)
00000001005972fc	testb	%al, %al
00000001005972fe	jne	0x1005974cf
0000000100597304	leaq	0x5055d7c(%rip), %rsi           ## literal pool for: "settings"
000000010059730b	movq	%r14, %rdi
000000010059730e	callq	__Z12strIsEqualCIPKcS0_         ## strIsEqualCI(char const*, char const*)
0000000100597313	testb	%al, %al
0000000100597315	jne	0x1005974cf
000000010059731b	leaq	0x50594fb(%rip), %rsi           ## literal pool for: "load_skin"
0000000100597322	movq	%r14, %rdi
0000000100597325	callq	__Z8isLeftCIPKcS0_              ## isLeftCI(char const*, char const*)
000000010059732a	testb	%al, %al
000000010059732c	jne	0x1005974cf
0000000100597332	leaq	0x505a5f3(%rip), %rsi           ## literal pool for: "setting_setdefault"
0000000100597339	movq	%r14, %rdi
000000010059733c	callq	__Z12strIsEqualCIPKcS0_         ## strIsEqualCI(char const*, char const*)
0000000100597341	testb	%al, %al
0000000100597343	jne	0x1005974cf
0000000100597349	leaq	0x5055b29(%rip), %rsi           ## literal pool for: "constant"
0000000100597350	movq	%r15, %rdi
0000000100597353	callq	__Z8isLeftCIPKcS0_              ## isLeftCI(char const*, char const*)
0000000100597358	testb	%al, %al
000000010059735a	jne	0x1005974cf
0000000100597360	leaq	0x50446b4(%rip), %rsi           ## literal pool for: "color"
0000000100597367	movq	%r14, %rdi
000000010059736a	callq	__Z8isLeftCIPKcS0_              ## isLeftCI(char const*, char const*)
000000010059736f	testb	%al, %al
0000000100597371	jne	0x1005974cf
0000000100597377	leaq	0x504568a(%rip), %rsi           ## literal pool for: "on"
000000010059737e	movq	%r14, %rdi
0000000100597381	callq	__Z12strIsEqualCIPKcS0_         ## strIsEqualCI(char const*, char const*)
0000000100597386	testb	%al, %al
0000000100597388	jne	0x1005974cf
000000010059738e	leaq	0x508087a(%rip), %rsi           ## literal pool for: "on "
0000000100597395	movq	%r14, %rdi
0000000100597398	callq	__Z8isLeftCIPKcS0_              ## isLeftCI(char const*, char const*)
000000010059739d	testb	%al, %al
000000010059739f	jne	0x1005974cf
00000001005973a5	leaq	0x50605aa(%rip), %rsi           ## literal pool for: "off"
00000001005973ac	movq	%r14, %rdi
00000001005973af	callq	__Z12strIsEqualCIPKcS0_         ## strIsEqualCI(char const*, char const*)
00000001005973b4	testb	%al, %al
00000001005973b6	jne	0x1005974cf
00000001005973bc	leaq	0x5080850(%rip), %rsi           ## literal pool for: "off "
00000001005973c3	movq	%r14, %rdi
00000001005973c6	callq	__Z8isLeftCIPKcS0_              ## isLeftCI(char const*, char const*)
00000001005973cb	testb	%al, %al
00000001005973cd	jne	0x1005974cf
00000001005973d3	leaq	0x5058f41(%rip), %rsi           ## literal pool for: "get_var"
00000001005973da	movq	%r15, %rdi
00000001005973dd	callq	__Z8isLeftCIPKcS0_              ## isLeftCI(char const*, char const*)
00000001005973e2	testb	%al, %al
00000001005973e4	jne	0x1005974cf
00000001005973ea	leaq	0x505a4d5(%rip), %rsi           ## literal pool for: "set_var"
00000001005973f1	movq	%r15, %rdi
00000001005973f4	callq	__Z8isLeftCIPKcS0_              ## isLeftCI(char const*, char const*)
00000001005973f9	testb	%al, %al
00000001005973fb	jne	0x1005974cf
0000000100597401	leaq	0x5071cb0(%rip), %rsi           ## literal pool for: "set "
0000000100597408	movq	%r15, %rdi
000000010059740b	callq	__Z8isLeftCIPKcS0_              ## isLeftCI(char const*, char const*)
0000000100597410	testb	%al, %al
0000000100597412	jne	0x1005974cf
0000000100597418	leaq	0x5057a5a(%rip), %rsi           ## literal pool for: "cycle"
000000010059741f	movq	%r15, %rdi
0000000100597422	callq	__Z8isLeftCIPKcS0_              ## isLeftCI(char const*, char const*)
0000000100597427	testb	%al, %al
0000000100597429	jne	0x1005974cf
000000010059742f	leaq	0x505a96d(%rip), %rsi           ## literal pool for: "var"
0000000100597436	movq	%r15, %rdi
0000000100597439	callq	__Z8isLeftCIPKcS0_              ## isLeftCI(char const*, char const*)
000000010059743e	testb	%al, %al
0000000100597440	jne	0x1005974cf
0000000100597446	leaq	0x50559ce(%rip), %rsi           ## literal pool for: "toggle"
000000010059744d	movq	%r15, %rdi
0000000100597450	callq	__Z8isLeftCIPKcS0_              ## isLeftCI(char const*, char const*)
0000000100597455	testb	%al, %al
0000000100597457	jne	0x1005974cf
0000000100597459	leaq	0x5058db9(%rip), %rsi           ## literal pool for: "get_text"
0000000100597460	movq	%r15, %rdi
0000000100597463	callq	__Z8isLeftCIPKcS0_              ## isLeftCI(char const*, char const*)
0000000100597468	testb	%al, %al
000000010059746a	jne	0x1005974cf
000000010059746c	leaq	0x5059ea5(%rip), %rsi           ## literal pool for: "remote_action"
0000000100597473	movq	%r14, %rdi
0000000100597476	callq	__Z8isLeftCIPKcS0_              ## isLeftCI(char const*, char const*)
000000010059747b	testb	%al, %al
000000010059747d	jne	0x1005974cf
000000010059747f	leaq	0x5054b32(%rip), %rsi           ## literal pool for: "custom_button"
0000000100597486	movq	%r14, %rdi
0000000100597489	callq	__Z8isLeftCIPKcS0_              ## isLeftCI(char const*, char const*)
000000010059748e	testb	%al, %al
0000000100597490	jne	0x1005974cf
0000000100597492	leaq	0x5058ff1(%rip), %rsi           ## literal pool for: "has_custom_button"
0000000100597499	movq	%r14, %rdi
000000010059749c	callq	__Z8isLeftCIPKcS0_              ## isLeftCI(char const*, char const*)
00000001005974a1	testb	%al, %al
00000001005974a3	jne	0x1005974cf
00000001005974a5	leaq	0x505a67a(%rip), %rsi           ## literal pool for: "skin_width"
00000001005974ac	movq	%r14, %rdi
00000001005974af	callq	__Z8isLeftCIPKcS0_              ## isLeftCI(char const*, char const*)
00000001005974b4	testb	%al, %al
00000001005974b6	jne	0x1005974cf
00000001005974b8	leaq	0x505a5f8(%rip), %rsi           ## literal pool for: "skin_height"
00000001005974bf	movq	%r14, %rdi
00000001005974c2	callq	__Z8isLeftCIPKcS0_              ## isLeftCI(char const*, char const*)
00000001005974c7	testb	%al, %al
00000001005974c9	je	0x100598365
00000001005974cf	xorps	%xmm0, %xmm0
00000001005974d2	movaps	%xmm0, -0xa0(%rbp)
00000001005974d9	movq	$CONFIG_EMULATE_HARDWARE, -0x90(%rbp)
00000001005974e4	movq	%r14, -0x30(%rbp)
00000001005974e8	movzbl	CONFIG_EMULATE_HARDWARE(%r14), %eax
00000001005974ec	cmpq	$0x28, %rax
00000001005974f0	ja	0x1005975af
00000001005974f6	btq	%rax, %r12
00000001005974fa	jae	0x100597501
00000001005974fc	incq	%r14
00000001005974ff	jmp	0x1005974e4
0000000100597501	cmpq	$0x28, %rax
0000000100597505	jne	0x1005975af
000000010059750b	incq	%r14
000000010059750e	movq	%r14, -0x30(%rbp)
0000000100597512	movzbl	CONFIG_EMULATE_HARDWARE(%r14), %eax
0000000100597516	cmpq	$0x20, %rax
000000010059751a	ja	0x100597522
000000010059751c	btq	%rax, %r12
0000000100597520	jb	0x10059750b
0000000100597522	movq	%r12, %rbx
0000000100597525	movl	-0x34(%rbp), %r12d
0000000100597529	leaq	-0x30(%rbp), %rsi
000000010059752d	movq	%r14, %rdi
0000000100597530	movl	%r12d, %edx
0000000100597533	callq	__ZN7IAction6createEPKcPS1_i    ## IAction::create(char const*, char const**, int)
0000000100597538	movq	%rax, %r15
000000010059753b	movq	-0x30(%rbp), %rax
000000010059753f	movb	CONFIG_EMULATE_HARDWARE(%rax), %cl
0000000100597541	cmpb	$0x29, %cl
0000000100597544	jne	0x10059755c
0000000100597546	incq	%rax
0000000100597549	movq	%rax, -0x30(%rbp)
000000010059754d	movzbl	CONFIG_EMULATE_HARDWARE(%rax), %ecx
0000000100597550	cmpq	$0x20, %rcx
0000000100597554	ja	0x10059755c
0000000100597556	btq	%rcx, %rbx
000000010059755a	jb	0x100597546
000000010059755c	cmpb	$0x3f, %cl
000000010059755f	jne	0x1005982b2
0000000100597565	movq	%r15, %rdi
0000000100597568	callq	__Z26createAction_combine_queryP7IAction ## createAction_combine_query(IAction*)
000000010059756d	movq	%rax, %r15
0000000100597570	leaq	-0x30(%rbp), %rsi
0000000100597574	movq	CONFIG_EMULATE_HARDWARE(%rsi), %rdi
0000000100597577	incq	%rdi
000000010059757a	movq	%rdi, CONFIG_EMULATE_HARDWARE(%rsi)
000000010059757d	movl	%r12d, %edx
0000000100597580	callq	__ZN7IAction6createEPKcPS1_i    ## IAction::create(char const*, char const**, int)
0000000100597585	movq	%rax, 0x40(%r15)
0000000100597589	testq	%rax, %rax
000000010059758c	je	0x100597760
0000000100597592	testb	$0x10, 0x15(%r15)
0000000100597597	movl	0x14(%rax), %ecx
000000010059759a	jne	0x100597752
00000001005975a0	btl	$0xc, %ecx
00000001005975a4	jb	0x10059775b
00000001005975aa	jmp	0x100597760
00000001005975af	leaq	0x5(%r14), %r15
00000001005975b3	xorl	%eax, %eax
00000001005975b5	leaq	0x508065c(%rip), %rcx           ## literal pool for: "press"
00000001005975bc	cmpq	$0x5, %rax
00000001005975c0	je	0x10059768a
00000001005975c6	movzbl	CONFIG_EMULATE_HARDWARE(%r14,%rax), %edx
00000001005975cb	leal	-0x41(%rdx), %esi
00000001005975ce	movl	%edx, %edi
00000001005975d0	orb	$0x20, %dil
00000001005975d4	cmpb	$0x1a, %sil
00000001005975d8	movzbl	%dil, %esi
00000001005975dc	cmovael	%edx, %esi
00000001005975df	leaq	0x1(%rax), %rdx
00000001005975e3	cmpb	CONFIG_EMULATE_HARDWARE(%rax,%rcx), %sil
00000001005975e7	movq	%rdx, %rax
00000001005975ea	je	0x1005975bc
00000001005975ec	leaq	0x7(%r14), %r15
00000001005975f0	xorl	%eax, %eax
00000001005975f2	leaq	0x5080625(%rip), %rcx           ## literal pool for: "unpress"
00000001005975f9	cmpq	$0x7, %rax
00000001005975fd	je	0x1005976d2
0000000100597603	movzbl	CONFIG_EMULATE_HARDWARE(%r14,%rax), %edx
0000000100597608	leal	-0x41(%rdx), %esi
000000010059760b	movl	%edx, %edi
000000010059760d	orb	$0x20, %dil
0000000100597611	cmpb	$0x1a, %sil
0000000100597615	movzbl	%dil, %esi
0000000100597619	cmovael	%edx, %esi
000000010059761c	leaq	0x1(%rax), %rdx
0000000100597620	cmpb	CONFIG_EMULATE_HARDWARE(%rax,%rcx), %sil
0000000100597624	movq	%rdx, %rax
0000000100597627	je	0x1005975f9
0000000100597629	leaq	0x3(%r14), %r15
000000010059762d	xorl	%eax, %eax
000000010059762f	leaq	0x50805f0(%rip), %rcx           ## literal pool for: "not"
0000000100597636	cmpq	$0x3, %rax
000000010059763a	je	0x10059771a
0000000100597640	movzbl	CONFIG_EMULATE_HARDWARE(%r14,%rax), %edx
0000000100597645	leal	-0x41(%rdx), %esi
0000000100597648	movl	%edx, %edi
000000010059764a	orb	$0x20, %dil
000000010059764e	cmpb	$0x1a, %sil
0000000100597652	movzbl	%dil, %esi
0000000100597656	cmovael	%edx, %esi
0000000100597659	leaq	0x1(%rax), %rdx
000000010059765d	cmpb	CONFIG_EMULATE_HARDWARE(%rax,%rcx), %sil
0000000100597661	movq	%rdx, %rax
0000000100597664	je	0x100597636
0000000100597666	leaq	0x50805bd(%rip), %rsi           ## literal pool for: "isok"
000000010059766d	leaq	-0x30(%rbp), %r14
0000000100597671	movq	%r14, %rdi
0000000100597674	callq	__ZN7IAction11stringMatchERPKcS1_ ## IAction::stringMatch(char const*&, char const*)
0000000100597679	movzbl	%al, %eax
000000010059767c	shll	$0x18, %eax
000000010059767f	movl	%eax, -0x38(%rbp)
0000000100597682	movq	CONFIG_EMULATE_HARDWARE(%r14), %r15
0000000100597685	jmp	0x1005977b4
000000010059768a	movzbl	CONFIG_EMULATE_HARDWARE(%r15), %eax
000000010059768e	cmpq	$0x29, %rax
0000000100597692	ja	0x1005975ec
0000000100597698	movabsq	$0x20100000001, %rcx            ## imm = 0x20100000001
00000001005976a2	btq	%rax, %rcx
00000001005976a6	jae	0x1005975ec
00000001005976ac	cmpb	$0x20, %al
00000001005976ae	ja	0x1005976c2
00000001005976b0	movzbl	%al, %eax
00000001005976b3	btq	%rax, %r12
00000001005976b7	jae	0x1005976c2
00000001005976b9	movb	0x1(%r15), %al
00000001005976bd	incq	%r15
00000001005976c0	jmp	0x1005976ac
00000001005976c2	movq	%r15, -0x30(%rbp)
00000001005976c6	movl	$CONFIG_VP9, -0x38(%rbp)
00000001005976cd	jmp	0x1005977b4
00000001005976d2	movzbl	CONFIG_EMULATE_HARDWARE(%r15), %eax
00000001005976d6	cmpq	$0x29, %rax
00000001005976da	ja	0x100597629
00000001005976e0	movabsq	$0x20100000001, %rcx            ## imm = 0x20100000001
00000001005976ea	btq	%rax, %rcx
00000001005976ee	jae	0x100597629
00000001005976f4	cmpb	$0x20, %al
00000001005976f6	ja	0x10059770a
00000001005976f8	movzbl	%al, %eax
00000001005976fb	btq	%rax, %r12
00000001005976ff	jae	0x10059770a
0000000100597701	movb	0x1(%r15), %al
0000000100597705	incq	%r15
0000000100597708	jmp	0x1005976f4
000000010059770a	movq	%r15, -0x30(%rbp)
000000010059770e	movl	$0x2, -0x38(%rbp)
0000000100597715	jmp	0x1005977b4
000000010059771a	movzbl	CONFIG_EMULATE_HARDWARE(%r15), %eax
000000010059771e	cmpq	$0x29, %rax
0000000100597722	ja	0x100597666
0000000100597728	movabsq	$0x20100000001, %rcx            ## imm = 0x20100000001
0000000100597732	btq	%rax, %rcx
0000000100597736	jae	0x100597666
000000010059773c	cmpb	$0x20, %al
000000010059773e	ja	0x1005977a9
0000000100597740	movzbl	%al, %eax
0000000100597743	btq	%rax, %r12
0000000100597747	jae	0x1005977a9
0000000100597749	movb	0x1(%r15), %al
000000010059774d	incq	%r15
0000000100597750	jmp	0x10059773c
0000000100597752	orl	$0x1000, %ecx                   ## imm = 0x1000
0000000100597758	movl	%ecx, 0x14(%rax)
000000010059775b	orb	$0x10, 0x15(%r15)
0000000100597760	movq	-0x30(%rbp), %rdi
0000000100597764	cmpb	$0x3a, CONFIG_EMULATE_HARDWARE(%rdi)
0000000100597767	jne	0x1005982b2
000000010059776d	incq	%rdi
0000000100597770	leaq	-0x30(%rbp), %rsi
0000000100597774	movq	%rdi, CONFIG_EMULATE_HARDWARE(%rsi)
0000000100597777	movl	%r12d, %edx
000000010059777a	callq	__ZN7IAction6createEPKcPS1_i    ## IAction::create(char const*, char const**, int)
000000010059777f	movq	%rax, 0x48(%r15)
0000000100597783	testq	%rax, %rax
0000000100597786	je	0x1005982b2
000000010059778c	testb	$0x10, 0x15(%r15)
0000000100597791	movl	0x14(%rax), %ecx
0000000100597794	jne	0x1005982a4
000000010059779a	btl	$0xc, %ecx
000000010059779e	jb	0x1005982ad
00000001005977a4	jmp	0x1005982b2
00000001005977a9	movq	%r15, -0x30(%rbp)
00000001005977ad	movl	$0x8000, -0x38(%rbp)            ## imm = 0x8000
00000001005977b4	leaq	0x4(%r15), %rax
00000001005977b8	xorl	%ecx, %ecx
00000001005977ba	leaq	0x50442ee(%rip), %rdx           ## literal pool for: "deck"
00000001005977c1	cmpq	$0x4, %rcx
00000001005977c5	je	0x100597826
00000001005977c7	movzbl	CONFIG_EMULATE_HARDWARE(%r15,%rcx), %esi
00000001005977cc	leal	-0x41(%rsi), %edi
00000001005977cf	movl	%esi, %r8d
00000001005977d2	orb	$0x20, %r8b
00000001005977d6	cmpb	$0x1a, %dil
00000001005977da	movzbl	%r8b, %edi
00000001005977de	cmovael	%esi, %edi
00000001005977e1	leaq	0x1(%rcx), %rsi
00000001005977e5	cmpb	CONFIG_EMULATE_HARDWARE(%rcx,%rdx), %dil
00000001005977e9	movq	%rsi, %rcx
00000001005977ec	je	0x1005977c1
00000001005977ee	xorl	%ecx, %ecx
00000001005977f0	leaq	0x508040d(%rip), %rdx           ## literal pool for: "zone"
00000001005977f7	cmpq	$0x4, %rcx
00000001005977fb	je	0x100597855
00000001005977fd	movzbl	CONFIG_EMULATE_HARDWARE(%r15,%rcx), %esi
0000000100597802	leal	-0x41(%rsi), %edi
0000000100597805	movl	%esi, %r8d
0000000100597808	orb	$0x20, %r8b
000000010059780c	cmpb	$0x1a, %dil
0000000100597810	movzbl	%r8b, %edi
0000000100597814	cmovael	%esi, %edi
0000000100597817	leaq	0x1(%rcx), %rsi
000000010059781b	cmpb	CONFIG_EMULATE_HARDWARE(%rcx,%rdx), %dil
000000010059781f	movq	%rsi, %rcx
0000000100597822	je	0x1005977f7
0000000100597824	jmp	0x10059789a
0000000100597826	movzbl	CONFIG_EMULATE_HARDWARE(%rax), %ecx
0000000100597829	cmpq	$0x29, %rcx
000000010059782d	ja	0x1005977ee
000000010059782f	movabsq	$0x20100000001, %rdx            ## imm = 0x20100000001
0000000100597839	btq	%rcx, %rdx
000000010059783d	jae	0x1005977ee
000000010059783f	cmpb	$0x20, %cl
0000000100597842	ja	0x100597884
0000000100597844	movzbl	%cl, %ecx
0000000100597847	btq	%rcx, %r12
000000010059784b	jae	0x100597884
000000010059784d	movb	0x1(%rax), %cl
0000000100597850	incq	%rax
0000000100597853	jmp	0x10059783f
0000000100597855	movzbl	CONFIG_EMULATE_HARDWARE(%rax), %ecx
0000000100597858	cmpq	$0x29, %rcx
000000010059785c	ja	0x10059789a
000000010059785e	movabsq	$0x20100000001, %rdx            ## imm = 0x20100000001
0000000100597868	btq	%rcx, %rdx
000000010059786c	jae	0x10059789a
000000010059786e	cmpb	$0x20, %cl
0000000100597871	ja	0x100597884
0000000100597873	movzbl	%cl, %ecx
0000000100597876	btq	%rcx, %r12
000000010059787a	jae	0x100597884
000000010059787c	movb	0x1(%rax), %cl
000000010059787f	incq	%rax
0000000100597882	jmp	0x10059786e
0000000100597884	leaq	-0x30(%rbp), %r14
0000000100597888	movq	%rax, CONFIG_EMULATE_HARDWARE(%r14)
000000010059788b	leaq	-0x34(%rbp), %rsi
000000010059788f	movq	%r14, %rdi
0000000100597892	callq	__ZN7IAction9deckMatchERPKcRi   ## IAction::deckMatch(char const*&, int&)
0000000100597897	movq	CONFIG_EMULATE_HARDWARE(%r14), %r15
000000010059789a	movl	-0x34(%rbp), %ebx
000000010059789d	xorl	%ecx, %ecx
000000010059789f	cmpl	$0x616c6c, %ebx                 ## imm = 0x616C6C
00000001005978a5	movl	%ebx, %r9d
00000001005978a8	cmovel	%ecx, %r9d
00000001005978ac	movl	%r9d, -0x34(%rbp)
00000001005978b0	xorps	%xmm0, %xmm0
00000001005978b3	movaps	%xmm0, -0x80(%rbp)
00000001005978b7	movq	$CONFIG_EMULATE_HARDWARE, -0x70(%rbp)
00000001005978bf	leaq	0x7(%r15), %rax
00000001005978c3	leaq	0x5044fe5(%rip), %rdx           ## literal pool for: "sampler"
00000001005978ca	movl	%r9d, -0xb0(%rbp)
00000001005978d1	cmpq	$0x7, %rcx
00000001005978d5	je	0x1005979b2
00000001005978db	movzbl	CONFIG_EMULATE_HARDWARE(%r15,%rcx), %esi
00000001005978e0	leal	-0x41(%rsi), %edi
00000001005978e3	movl	%esi, %r8d
00000001005978e6	orb	$0x20, %r8b
00000001005978ea	cmpb	$0x1a, %dil
00000001005978ee	movzbl	%r8b, %edi
00000001005978f2	cmovael	%esi, %edi
00000001005978f5	leaq	0x1(%rcx), %rsi
00000001005978f9	cmpb	CONFIG_EMULATE_HARDWARE(%rcx,%rdx), %dil
00000001005978fd	movq	%rsi, %rcx
0000000100597900	je	0x1005978d1
0000000100597902	leaq	0x6(%r15), %rax
0000000100597906	xorl	%ecx, %ecx
0000000100597908	leaq	0x5080329(%rip), %rdx           ## literal pool for: "effect"
000000010059790f	cmpq	$0x6, %rcx
0000000100597913	je	0x100597a3f
0000000100597919	movzbl	CONFIG_EMULATE_HARDWARE(%r15,%rcx), %esi
000000010059791e	leal	-0x41(%rsi), %edi
0000000100597921	movl	%esi, %r8d
0000000100597924	orb	$0x20, %r8b
0000000100597928	cmpb	$0x1a, %dil
000000010059792c	movzbl	%r8b, %edi
0000000100597930	cmovael	%esi, %edi
0000000100597933	leaq	0x1(%rcx), %rsi
0000000100597937	cmpb	CONFIG_EMULATE_HARDWARE(%rcx,%rdx), %dil
000000010059793b	movq	%rsi, %rcx
000000010059793e	je	0x10059790f
0000000100597940	leaq	0x3(%r15), %rax
0000000100597944	xorl	%ecx, %ecx
0000000100597946	leaq	0x505a6c2(%rip), %rdx           ## literal pool for: "get"
000000010059794d	cmpq	$0x3, %rcx
0000000100597951	je	0x100597ad4
0000000100597957	movzbl	CONFIG_EMULATE_HARDWARE(%r15,%rcx), %esi
000000010059795c	leal	-0x41(%rsi), %edi
000000010059795f	movl	%esi, %r8d
0000000100597962	orb	$0x20, %r8b
0000000100597966	cmpb	$0x1a, %dil
000000010059796a	movzbl	%r8b, %edi
000000010059796e	cmovael	%esi, %edi
0000000100597971	leaq	0x1(%rcx), %rsi
0000000100597975	cmpb	CONFIG_EMULATE_HARDWARE(%rcx,%rdx), %dil
0000000100597979	movq	%rsi, %rcx
000000010059797c	je	0x10059794d
000000010059797e	leaq	0x50802c7(%rip), %rsi           ## literal pool for: "loop select"
0000000100597985	movl	$0xb, %edx
000000010059798a	movq	%r15, %rdi
000000010059798d	callq	0x104fe92b4                     ## symbol stub for: _strncasecmp
0000000100597992	testl	%eax, %eax
0000000100597994	jne	0x100597b24
000000010059799a	addq	$0x5, %r15
000000010059799e	movl	$0x5, %edx
00000001005979a3	leaq	0x50802ae(%rip), %rsi           ## literal pool for: "loop_"
00000001005979aa	movq	%r15, %rax
00000001005979ad	jmp	0x100597b17
00000001005979b2	movzbl	CONFIG_EMULATE_HARDWARE(%rax), %ecx
00000001005979b5	cmpq	$0x29, %rcx
00000001005979b9	ja	0x100597902
00000001005979bf	movabsq	$0x20100000001, %rdx            ## imm = 0x20100000001
00000001005979c9	btq	%rcx, %rdx
00000001005979cd	jae	0x100597902
00000001005979d3	cmpb	$0x20, %cl
00000001005979d6	ja	0x1005979e9
00000001005979d8	movzbl	%cl, %ecx
00000001005979db	btq	%rcx, %r12
00000001005979df	jae	0x1005979e9
00000001005979e1	movb	0x1(%rax), %cl
00000001005979e4	incq	%rax
00000001005979e7	jmp	0x1005979d3
00000001005979e9	movq	%rax, -0x30(%rbp)
00000001005979ed	leaq	0x508023b(%rip), %rsi           ## literal pool for: "sampler_"
00000001005979f4	leaq	-0x80(%rbp), %rdi
00000001005979f8	movl	$msac.end, %edx
00000001005979fd	callq	0x104fe8516                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm
0000000100597a02	xorps	%xmm0, %xmm0
0000000100597a05	leaq	-0x60(%rbp), %rsi
0000000100597a09	movaps	%xmm0, 0x10(%rsi)
0000000100597a0d	movaps	%xmm0, CONFIG_EMULATE_HARDWARE(%rsi)
0000000100597a10	movb	$0x0, 0x20(%rsi)
0000000100597a14	leaq	-0x30(%rbp), %rdi
0000000100597a18	movl	$CONFIG_VP9, %edx
0000000100597a1d	callq	__ZN7IAction14stringGetParamERPKcR12SActionParamb ## IAction::stringGetParam(char const*&, SActionParam&, bool)
0000000100597a22	testb	%al, %al
0000000100597a24	je	0x100597ac3
0000000100597a2a	leaq	-0xa0(%rbp), %rdi
0000000100597a31	leaq	-0x60(%rbp), %rsi
0000000100597a35	callq	__ZNSt3__16vectorI12SActionParamNS_9allocatorIS1_EEE9push_backB8ne200100EOS1_ ## std::__1::vector<SActionParam, std::__1::allocator<SActionParam>>::push_back[abi:ne200100](SActionParam&&)
0000000100597a3a	jmp	0x100597ac3
0000000100597a3f	movzbl	CONFIG_EMULATE_HARDWARE(%rax), %ecx
0000000100597a42	cmpq	$0x29, %rcx
0000000100597a46	ja	0x100597940
0000000100597a4c	movabsq	$0x20100000001, %rdx            ## imm = 0x20100000001
0000000100597a56	btq	%rcx, %rdx
0000000100597a5a	jae	0x100597940
0000000100597a60	cmpb	$0x20, %cl
0000000100597a63	ja	0x100597a76
0000000100597a65	movzbl	%cl, %ecx
0000000100597a68	btq	%rcx, %r12
0000000100597a6c	jae	0x100597a76
0000000100597a6e	movb	0x1(%rax), %cl
0000000100597a71	incq	%rax
0000000100597a74	jmp	0x100597a60
0000000100597a76	movq	%rax, -0x30(%rbp)
0000000100597a7a	leaq	0x50801be(%rip), %rsi           ## literal pool for: "effect_"
0000000100597a81	leaq	-0x80(%rbp), %rdi
0000000100597a85	movl	$0x7, %edx
0000000100597a8a	callq	0x104fe8516                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm
0000000100597a8f	xorps	%xmm0, %xmm0
0000000100597a92	leaq	-0x60(%rbp), %rsi
0000000100597a96	movaps	%xmm0, 0x10(%rsi)
0000000100597a9a	movaps	%xmm0, CONFIG_EMULATE_HARDWARE(%rsi)
0000000100597a9d	movb	$0x0, 0x20(%rsi)
0000000100597aa1	leaq	-0x30(%rbp), %rdi
0000000100597aa5	movl	$CONFIG_VP9, %edx
0000000100597aaa	callq	__ZN7IAction14stringGetParamERPKcR12SActionParamb ## IAction::stringGetParam(char const*&, SActionParam&, bool)
0000000100597aaf	testb	%al, %al
0000000100597ab1	je	0x100597ac3
0000000100597ab3	leaq	-0xa0(%rbp), %rdi
0000000100597aba	leaq	-0x60(%rbp), %rsi
0000000100597abe	callq	__ZNSt3__16vectorI12SActionParamNS_9allocatorIS1_EEE9push_backB8ne200100EOS1_ ## std::__1::vector<SActionParam, std::__1::allocator<SActionParam>>::push_back[abi:ne200100](SActionParam&&)
0000000100597ac3	testb	$0x1, -0x58(%rbp)
0000000100597ac7	je	0x100597b24
0000000100597ac9	movq	-0x48(%rbp), %rdi
0000000100597acd	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
0000000100597ad2	jmp	0x100597b24
0000000100597ad4	movzbl	CONFIG_EMULATE_HARDWARE(%rax), %ecx
0000000100597ad7	cmpq	$0x29, %rcx
0000000100597adb	ja	0x10059797e
0000000100597ae1	movabsq	$0x20100000001, %rdx            ## imm = 0x20100000001
0000000100597aeb	btq	%rcx, %rdx
0000000100597aef	jae	0x10059797e
0000000100597af5	cmpb	$0x20, %cl
0000000100597af8	ja	0x100597b0b
0000000100597afa	movzbl	%cl, %ecx
0000000100597afd	btq	%rcx, %r12
0000000100597b01	jae	0x100597b0b
0000000100597b03	movb	0x1(%rax), %cl
0000000100597b06	incq	%rax
0000000100597b09	jmp	0x100597af5
0000000100597b0b	movl	$FGData.num_y_points, %edx
0000000100597b10	leaq	0x5080130(%rip), %rsi           ## literal pool for: "get_"
0000000100597b17	movq	%rax, -0x30(%rbp)
0000000100597b1b	leaq	-0x80(%rbp), %rdi
0000000100597b1f	callq	0x104fe8516                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm
0000000100597b24	movl	%ebx, -0xac(%rbp)
0000000100597b2a	movq	-0x30(%rbp), %r14
0000000100597b2e	xorl	%r15d, %r15d
0000000100597b31	movabsq	$-0xbfffdbcffffdbff, %rax       ## imm = 0xF400024300002401
0000000100597b3b	movzbl	CONFIG_EMULATE_HARDWARE(%r14,%r15), %ecx
0000000100597b40	cmpq	$0x3f, %rcx
0000000100597b44	ja	0x100597b4c
0000000100597b46	btq	%rcx, %rax
0000000100597b4a	jb	0x100597b51
0000000100597b4c	incq	%r15
0000000100597b4f	jmp	0x100597b3b
0000000100597b51	leaq	-0x80(%rbp), %rdi
0000000100597b55	movq	%r14, %rsi
0000000100597b58	movq	%r15, %rdx
0000000100597b5b	callq	0x104fe8516                     ## symbol stub for: __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm
0000000100597b60	addq	%r15, %r14
0000000100597b63	leaq	-0x7f(%rbp), %rax
0000000100597b67	xorl	%ecx, %ecx
0000000100597b69	movzbl	-0x80(%rbp), %edx
0000000100597b6d	testb	$0x1, %dl
0000000100597b70	jne	0x100597b7e
0000000100597b72	shrl	%edx
0000000100597b74	movq	%rax, %r15
0000000100597b77	cmpq	%rdx, %rcx
0000000100597b7a	jb	0x100597b88
0000000100597b7c	jmp	0x100597b99
0000000100597b7e	movq	-0x70(%rbp), %r15
0000000100597b82	cmpq	-0x78(%rbp), %rcx
0000000100597b86	jae	0x100597b9c
0000000100597b88	cmpb	$0x2d, CONFIG_EMULATE_HARDWARE(%r15,%rcx)
0000000100597b8d	jne	0x100597b94
0000000100597b8f	movb	$0x5f, CONFIG_EMULATE_HARDWARE(%r15,%rcx)
0000000100597b94	incq	%rcx
0000000100597b97	jmp	0x100597b69
0000000100597b99	movq	%rax, %r15
0000000100597b9c	movq	%r13, -0xa8(%rbp)
0000000100597ba3	movq	%r15, %rdi
0000000100597ba6	callq	__Z6strlwrPc                    ## strlwr(char*)
0000000100597bab	xorl	%eax, %eax
0000000100597bad	movl	$c_derived_tbl.ehufsi, %ebx
0000000100597bb2	movq	%rax, -0x68(%rbp)
0000000100597bb6	addl	%ebx, %eax
0000000100597bb8	movl	%eax, %r12d
0000000100597bbb	shrl	$0x1f, %r12d
0000000100597bbf	addl	%eax, %r12d
0000000100597bc2	sarl	%r12d
0000000100597bc5	movslq	%r12d, %r13
0000000100597bc8	shlq	$0x4, %r13
0000000100597bcc	leaq	_actionList(%rip), %rax
0000000100597bd3	leaq	CONFIG_EMULATE_HARDWARE(%rax,%r13), %rcx
0000000100597bd7	movq	%rcx, -0xb8(%rbp)
0000000100597bde	movq	CONFIG_EMULATE_HARDWARE(%rax,%r13), %rdi
0000000100597be2	movq	%r15, %rsi
0000000100597be5	callq	0x104fe9284                     ## symbol stub for: _strcmp
0000000100597bea	testl	%eax, %eax
0000000100597bec	jns	0x100597bf6
0000000100597bee	incl	%r12d
0000000100597bf1	movl	%r12d, %eax
0000000100597bf4	jmp	0x100597c02
0000000100597bf6	je	0x100597c0f
0000000100597bf8	decl	%r12d
0000000100597bfb	movl	%r12d, %ebx
0000000100597bfe	movq	-0x68(%rbp), %rax
0000000100597c02	cmpl	%eax, %ebx
0000000100597c04	jge	0x100597bb2
0000000100597c06	movl	$CONFIG_EMULATE_HARDWARE, -0x68(%rbp)
0000000100597c0d	jmp	0x100597c1c
0000000100597c0f	movq	-0xb8(%rbp), %rax
0000000100597c16	movl	0x8(%rax), %eax
0000000100597c19	movl	%eax, -0x68(%rbp)
0000000100597c1c	leaq	_actionList(%rip), %rax
0000000100597c23	cmpb	$0x1, 0xc(%rax,%r13)
0000000100597c29	movabsq	$0x100002600, %rbx              ## imm = 0x100002600
0000000100597c33	movl	-0x38(%rbp), %r12d
0000000100597c37	jne	0x100597c58
0000000100597c39	leaq	0x505337d(%rip), %rsi           ## literal pool for: "_slider"
0000000100597c40	leaq	-0x80(%rbp), %rdi
0000000100597c44	callq	__Z9isRightCIRKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEPKc ## isRightCI(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, char const*)
0000000100597c49	movl	%r12d, %ecx
0000000100597c4c	orl	$0x200000, %ecx                 ## imm = 0x200000
0000000100597c52	testb	%al, %al
0000000100597c54	cmovnel	%ecx, %r12d
0000000100597c58	movq	%r14, -0x30(%rbp)
0000000100597c5c	movzbl	CONFIG_EMULATE_HARDWARE(%r14), %eax
0000000100597c60	cmpq	$0x20, %rax
0000000100597c64	ja	0x1005980d7
0000000100597c6a	btq	%rax, %rbx
0000000100597c6e	jae	0x1005980d7
0000000100597c74	incq	%r14
0000000100597c77	jmp	0x100597c58
0000000100597c79	xorps	%xmm0, %xmm0
0000000100597c7c	movaps	%xmm0, -0x50(%rbp)
0000000100597c80	movaps	%xmm0, -0x60(%rbp)
0000000100597c84	movb	$0x0, -0x40(%rbp)
0000000100597c88	leaq	0x5(%rax), %rcx
0000000100597c8c	xorl	%edx, %edx
0000000100597c8e	cmpq	$0x5, %rdx
0000000100597c92	je	0x100597e20
0000000100597c98	leaq	0x5056d77(%rip), %rsi           ## literal pool for: "blink"
0000000100597c9f	movzbl	CONFIG_EMULATE_HARDWARE(%rax,%rdx), %edi
0000000100597ca3	leal	-0x41(%rdi), %r8d
0000000100597ca7	movl	%edi, %r9d
0000000100597caa	orb	$0x20, %r9b
0000000100597cae	cmpb	$0x1a, %r8b
0000000100597cb2	movzbl	%r9b, %r8d
0000000100597cb6	cmovael	%edi, %r8d
0000000100597cba	leaq	0x1(%rdx), %rdi
0000000100597cbe	cmpb	CONFIG_EMULATE_HARDWARE(%rdx,%rsi), %r8b
0000000100597cc2	movq	%rdi, %rdx
0000000100597cc5	je	0x100597c8e
0000000100597cc7	leaq	0x9(%rax), %rdx
0000000100597ccb	xorl	%ecx, %ecx
0000000100597ccd	cmpq	$0x9, %rcx
0000000100597cd1	je	0x100597e67
0000000100597cd7	leaq	0x507ff80(%rip), %rsi           ## literal pool for: "blinkfast"
0000000100597cde	movzbl	CONFIG_EMULATE_HARDWARE(%rax,%rcx), %edi
0000000100597ce2	leal	-0x41(%rdi), %r8d
0000000100597ce6	movl	%edi, %r9d
0000000100597ce9	orb	$0x20, %r9b
0000000100597ced	cmpb	$0x1a, %r8b
0000000100597cf1	movzbl	%r9b, %r8d
0000000100597cf5	cmovael	%edi, %r8d
0000000100597cf9	leaq	0x1(%rcx), %rdi
0000000100597cfd	cmpb	CONFIG_EMULATE_HARDWARE(%rcx,%rsi), %r8b
0000000100597d01	movq	%rdi, %rcx
0000000100597d04	je	0x100597ccd
0000000100597d06	leaq	0xd(%rax), %rcx
0000000100597d0a	xorl	%esi, %esi
0000000100597d0c	cmpq	$0xd, %rsi
0000000100597d10	je	0x100597eae
0000000100597d16	leaq	0x507ff4b(%rip), %rdi           ## literal pool for: "while_pressed"
0000000100597d1d	movzbl	CONFIG_EMULATE_HARDWARE(%rax,%rsi), %r8d
0000000100597d22	leal	-0x41(%r8), %r9d
0000000100597d26	movl	%r8d, %r10d
0000000100597d29	orb	$0x20, %r10b
0000000100597d2d	cmpb	$0x1a, %r9b
0000000100597d31	movzbl	%r10b, %r9d
0000000100597d35	cmovael	%r8d, %r9d
0000000100597d39	leaq	0x1(%rsi), %r8
0000000100597d3d	cmpb	CONFIG_EMULATE_HARDWARE(%rsi,%rdi), %r9b
0000000100597d41	movq	%r8, %rsi
0000000100597d44	je	0x100597d0c
0000000100597d46	xorl	%esi, %esi
0000000100597d48	cmpq	$0x9, %rsi
0000000100597d4c	je	0x100597eee
0000000100597d52	leaq	0x505e78f(%rip), %rdi           ## literal pool for: "temporary"
0000000100597d59	movzbl	CONFIG_EMULATE_HARDWARE(%rax,%rsi), %r8d
0000000100597d5e	leal	-0x41(%r8), %r9d
0000000100597d62	movl	%r8d, %r10d
0000000100597d65	orb	$0x20, %r10b
0000000100597d69	cmpb	$0x1a, %r9b
0000000100597d6d	movzbl	%r10b, %r9d
0000000100597d71	cmovael	%r8d, %r9d
0000000100597d75	leaq	0x1(%rsi), %r8
0000000100597d79	cmpb	CONFIG_EMULATE_HARDWARE(%rsi,%rdi), %r9b
0000000100597d7d	movq	%r8, %rsi
0000000100597d80	je	0x100597d48
0000000100597d82	leaq	0xb(%rax), %rdx
0000000100597d86	xorl	%esi, %esi
0000000100597d88	cmpq	$0xb, %rsi
0000000100597d8c	je	0x100597f28
0000000100597d92	leaq	0x507fedd(%rip), %rdi           ## literal pool for: "momentarily"
0000000100597d99	movzbl	CONFIG_EMULATE_HARDWARE(%rax,%rsi), %r8d
0000000100597d9e	leal	-0x41(%r8), %r9d
0000000100597da2	movl	%r8d, %r10d
0000000100597da5	orb	$0x20, %r10b
0000000100597da9	cmpb	$0x1a, %r9b
0000000100597dad	movzbl	%r10b, %r9d
0000000100597db1	cmovael	%r8d, %r9d
0000000100597db5	leaq	0x1(%rsi), %r8
0000000100597db9	cmpb	CONFIG_EMULATE_HARDWARE(%rsi,%rdi), %r9b
0000000100597dbd	movq	%r8, %rsi
0000000100597dc0	je	0x100597d88
0000000100597dc2	xorl	%edx, %edx
0000000100597dc4	cmpq	$0xd, %rdx
0000000100597dc8	je	0x100597f8a
0000000100597dce	leaq	0x507fead(%rip), %rsi           ## literal pool for: "smart_pressed"
0000000100597dd5	movzbl	CONFIG_EMULATE_HARDWARE(%rax,%rdx), %edi
0000000100597dd9	leal	-0x41(%rdi), %r8d
0000000100597ddd	movl	%edi, %r9d
0000000100597de0	orb	$0x20, %r9b
0000000100597de4	cmpb	$0x1a, %r8b
0000000100597de8	movzbl	%r9b, %r8d
0000000100597dec	cmovael	%edi, %r8d
0000000100597df0	leaq	0x1(%rdx), %rdi
0000000100597df4	cmpb	CONFIG_EMULATE_HARDWARE(%rdx,%rsi), %r8b
0000000100597df8	movq	%rdi, %rdx
0000000100597dfb	je	0x100597dc4
0000000100597dfd	movzbl	CONFIG_EMULATE_HARDWARE(%rax), %ecx
0000000100597e00	cmpl	$0x3c, %ecx
0000000100597e03	jg	0x100597fce
0000000100597e09	cmpl	$0x21, %ecx
0000000100597e0c	je	0x100598038
0000000100597e12	cmpl	$0x3c, %ecx
0000000100597e15	je	0x100597fe1
0000000100597e1b	jmp	0x100597fea
0000000100597e20	movzbl	CONFIG_EMULATE_HARDWARE(%rcx), %edx
0000000100597e23	cmpq	$0x29, %rdx
0000000100597e27	ja	0x100597cc7
0000000100597e2d	movabsq	$0x20100000001, %rsi            ## imm = 0x20100000001
0000000100597e37	btq	%rdx, %rsi
0000000100597e3b	jae	0x100597cc7
0000000100597e41	cmpb	$0x20, %dl
0000000100597e44	ja	0x100597e57
0000000100597e46	movzbl	%dl, %eax
0000000100597e49	btq	%rax, %rbx
0000000100597e4d	jae	0x100597e57
0000000100597e4f	movb	0x1(%rcx), %dl
0000000100597e52	incq	%rcx
0000000100597e55	jmp	0x100597e41
0000000100597e57	movq	%rcx, -0x30(%rbp)
0000000100597e5b	orl	$c_derived_tbl.ehufsi, %r12d
0000000100597e62	jmp	0x100597f6a
0000000100597e67	movzbl	CONFIG_EMULATE_HARDWARE(%rdx), %ecx
0000000100597e6a	cmpq	$0x29, %rcx
0000000100597e6e	ja	0x100597d06
0000000100597e74	movabsq	$0x20100000001, %rsi            ## imm = 0x20100000001
0000000100597e7e	btq	%rcx, %rsi
0000000100597e82	jae	0x100597d06
0000000100597e88	cmpb	$0x20, %cl
0000000100597e8b	ja	0x100597e9e
0000000100597e8d	movzbl	%cl, %eax
0000000100597e90	btq	%rax, %rbx
0000000100597e94	jae	0x100597e9e
0000000100597e96	movb	0x1(%rdx), %cl
0000000100597e99	incq	%rdx
0000000100597e9c	jmp	0x100597e88
0000000100597e9e	movq	%rdx, -0x30(%rbp)
0000000100597ea2	orl	$0x100000, %r12d                ## imm = 0x100000
0000000100597ea9	jmp	0x100597f6a
0000000100597eae	movzbl	CONFIG_EMULATE_HARDWARE(%rcx), %esi
0000000100597eb1	cmpq	$0x29, %rsi
0000000100597eb5	ja	0x100597d46
0000000100597ebb	movabsq	$0x20100000001, %rdi            ## imm = 0x20100000001
0000000100597ec5	btq	%rsi, %rdi
0000000100597ec9	jae	0x100597d46
0000000100597ecf	cmpb	$0x20, %sil
0000000100597ed3	ja	0x100597ee8
0000000100597ed5	movzbl	%sil, %eax
0000000100597ed9	btq	%rax, %rbx
0000000100597edd	jae	0x100597ee8
0000000100597edf	movb	0x1(%rcx), %sil
0000000100597ee3	incq	%rcx
0000000100597ee6	jmp	0x100597ecf
0000000100597ee8	movq	%rcx, -0x30(%rbp)
0000000100597eec	jmp	0x100597f66
0000000100597eee	movzbl	CONFIG_EMULATE_HARDWARE(%rdx), %esi
0000000100597ef1	cmpq	$0x29, %rsi
0000000100597ef5	ja	0x100597d82
0000000100597efb	movabsq	$0x20100000001, %rdi            ## imm = 0x20100000001
0000000100597f05	btq	%rsi, %rdi
0000000100597f09	jae	0x100597d82
0000000100597f0f	cmpb	$0x20, %sil
0000000100597f13	ja	0x100597f62
0000000100597f15	movzbl	%sil, %eax
0000000100597f19	btq	%rax, %rbx
0000000100597f1d	jae	0x100597f62
0000000100597f1f	movb	0x1(%rdx), %sil
0000000100597f23	incq	%rdx
0000000100597f26	jmp	0x100597f0f
0000000100597f28	movzbl	CONFIG_EMULATE_HARDWARE(%rdx), %esi
0000000100597f2b	cmpq	$0x29, %rsi
0000000100597f2f	ja	0x100597dc2
0000000100597f35	movabsq	$0x20100000001, %rdi            ## imm = 0x20100000001
0000000100597f3f	btq	%rsi, %rdi
0000000100597f43	jae	0x100597dc2
0000000100597f49	cmpb	$0x20, %sil
0000000100597f4d	ja	0x100597f62
0000000100597f4f	movzbl	%sil, %eax
0000000100597f53	btq	%rax, %rbx
0000000100597f57	jae	0x100597f62
0000000100597f59	movb	0x1(%rdx), %sil
0000000100597f5d	incq	%rdx
0000000100597f60	jmp	0x100597f49
0000000100597f62	movq	%rdx, -0x30(%rbp)
0000000100597f66	orl	$0x4, %r12d
0000000100597f6a	movb	$0x1, %r14b
0000000100597f6d	testb	$0x1, -0x58(%rbp)
0000000100597f71	je	0x100597f7c
0000000100597f73	movq	-0x48(%rbp), %rdi
0000000100597f77	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
0000000100597f7c	testb	%r14b, %r14b
0000000100597f7f	jne	0x1005980d7
0000000100597f85	jmp	0x1005980fc
0000000100597f8a	movzbl	CONFIG_EMULATE_HARDWARE(%rcx), %edx
0000000100597f8d	cmpq	$0x29, %rdx
0000000100597f91	ja	0x100597dfd
0000000100597f97	movabsq	$0x20100000001, %rsi            ## imm = 0x20100000001
0000000100597fa1	btq	%rdx, %rsi
0000000100597fa5	jae	0x100597dfd
0000000100597fab	cmpb	$0x20, %dl
0000000100597fae	ja	0x100597fc1
0000000100597fb0	movzbl	%dl, %eax
0000000100597fb3	btq	%rax, %rbx
0000000100597fb7	jae	0x100597fc1
0000000100597fb9	movb	0x1(%rcx), %dl
0000000100597fbc	incq	%rcx
0000000100597fbf	jmp	0x100597fab
0000000100597fc1	movq	%rcx, -0x30(%rbp)
0000000100597fc5	orl	$0x2000004, %r12d               ## imm = 0x2000004
0000000100597fcc	jmp	0x100597f6a
0000000100597fce	cmpl	$0x3e, %ecx
0000000100597fd1	je	0x100597fe1
0000000100597fd3	cmpl	$0x3d, %ecx
0000000100597fd6	jne	0x100597fea
0000000100597fd8	orl	$0x40000, %r12d                 ## imm = 0x40000
0000000100597fdf	jmp	0x10059803f
0000000100597fe1	orl	$0x10000, %r12d                 ## imm = 0x10000
0000000100597fe8	jmp	0x10059803f
0000000100597fea	leaq	-0x30(%rbp), %rdi
0000000100597fee	leaq	-0x60(%rbp), %rsi
0000000100597ff2	xorl	%edx, %edx
0000000100597ff4	callq	__ZN7IAction14stringGetParamERPKcR12SActionParamb ## IAction::stringGetParam(char const*&, SActionParam&, bool)
0000000100597ff9	testb	%al, %al
0000000100597ffb	je	0x1005980cf
0000000100598001	movl	$0x666c6167, %eax               ## imm = 0x666C6167
0000000100598006	leaq	-0x60(%rbp), %rsi
000000010059800a	xorl	CONFIG_EMULATE_HARDWARE(%rsi), %eax
000000010059800c	movl	0x4(%rsi), %ecx
000000010059800f	xorl	$0x76616c, %ecx                 ## imm = 0x76616C
0000000100598015	movl	%r12d, %edx
0000000100598018	orl	$0x1000, %edx                   ## imm = 0x1000
000000010059801e	orl	%eax, %ecx
0000000100598020	cmovel	%edx, %r12d
0000000100598024	movb	$0x1, %r14b
0000000100598027	leaq	-0xa0(%rbp), %rdi
000000010059802e	callq	__ZNSt3__16vectorI12SActionParamNS_9allocatorIS1_EEE9push_backB8ne200100EOS1_ ## std::__1::vector<SActionParam, std::__1::allocator<SActionParam>>::push_back[abi:ne200100](SActionParam&&)
0000000100598033	jmp	0x100597f6d
0000000100598038	xorl	$0x8000, %r12d                  ## imm = 0x8000
000000010059803f	leaq	0x1(%rax), %rcx
0000000100598043	movq	%rcx, -0x30(%rbp)
0000000100598047	movzbl	0x1(%rax), %edx
000000010059804b	cmpl	$0x3e, %edx
000000010059804e	je	0x10059805e
0000000100598050	cmpl	$0x3d, %edx
0000000100598053	jne	0x100598082
0000000100598055	orl	$0x40000, %r12d                 ## imm = 0x40000
000000010059805c	jmp	0x100598071
000000010059805e	cmpb	$0x3c, CONFIG_EMULATE_HARDWARE(%rax)
0000000100598061	jne	0x100598082
0000000100598063	andl	$0xfffaffff, %r12d              ## imm = 0xFFFAFFFF
000000010059806a	xorl	$0x48000, %r12d                 ## imm = 0x48000
0000000100598071	addq	$0x2, %rax
0000000100598075	movq	%rax, -0x30(%rbp)
0000000100598079	movq	%rax, %rcx
000000010059807c	jmp	0x100598082
000000010059807e	movq	%rcx, -0x30(%rbp)
0000000100598082	incq	%rcx
0000000100598085	movzbl	-0x1(%rcx), %eax
0000000100598089	cmpq	$0x20, %rax
000000010059808d	ja	0x100598095
000000010059808f	btq	%rax, %rbx
0000000100598093	jb	0x10059807e
0000000100598095	leaq	-0x30(%rbp), %rdi
0000000100598099	leaq	-0x60(%rbp), %rsi
000000010059809d	movl	$CONFIG_VP9, %edx
00000001005980a2	callq	__ZN7IAction14stringGetParamERPKcR12SActionParamb ## IAction::stringGetParam(char const*&, SActionParam&, bool)
00000001005980a7	testb	%al, %al
00000001005980a9	je	0x1005980c3
00000001005980ab	movb	$0x1, %r14b
00000001005980ae	leaq	-0xa0(%rbp), %rdi
00000001005980b5	leaq	-0x60(%rbp), %rsi
00000001005980b9	callq	__ZNSt3__16vectorI12SActionParamNS_9allocatorIS1_EEE9push_backB8ne200100EOS1_ ## std::__1::vector<SActionParam, std::__1::allocator<SActionParam>>::push_back[abi:ne200100](SActionParam&&)
00000001005980be	jmp	0x100597f6d
00000001005980c3	andl	$0xfffcffff, %r12d              ## imm = 0xFFFCFFFF
00000001005980ca	jmp	0x100597f6a
00000001005980cf	xorl	%r14d, %r14d
00000001005980d2	jmp	0x100597f6d
00000001005980d7	movq	-0x30(%rbp), %rax
00000001005980db	movzbl	CONFIG_EMULATE_HARDWARE(%rax), %ecx
00000001005980de	cmpq	$0x3f, %rcx
00000001005980e2	ja	0x100597c79
00000001005980e8	movabsq	$-0x7ffffdbfffffffff, %rdx      ## imm = 0x8000024000000001
00000001005980f2	btq	%rcx, %rdx
00000001005980f6	jae	0x100597c79
00000001005980fc	movl	-0x68(%rbp), %ebx
00000001005980ff	movslq	%ebx, %rax
0000000100598102	leaq	_actionFactory(%rip), %r13
0000000100598109	callq	*(%r13,%rax,8)
000000010059810e	movq	%rax, %r15
0000000100598111	movl	%ebx, 0xc(%rax)
0000000100598114	movl	-0xb0(%rbp), %edx
000000010059811a	movl	%edx, 0x10(%rax)
000000010059811d	orl	%r12d, 0x14(%rax)
0000000100598121	movaps	-0xa0(%rbp), %xmm0
0000000100598128	movups	0x20(%rax), %xmm1
000000010059812c	movups	%xmm0, 0x20(%rax)
0000000100598130	movaps	%xmm1, -0xa0(%rbp)
0000000100598137	movq	0x30(%rax), %rax
000000010059813b	movq	-0x90(%rbp), %rcx
0000000100598142	movq	%rcx, 0x30(%r15)
0000000100598146	xorl	%r14d, %r14d
0000000100598149	cmpl	$0x17e, %ebx                    ## imm = 0x17E
000000010059814f	cmovnel	%edx, %r14d
0000000100598153	movq	%rax, -0x90(%rbp)
000000010059815a	movq	-0x30(%rbp), %rdi
000000010059815e	movzbl	CONFIG_EMULATE_HARDWARE(%rdi), %eax
0000000100598161	cmpl	$0x26, %eax
0000000100598164	je	0x10059819c
0000000100598166	cmpl	$0x3f, %eax
0000000100598169	jne	0x10059823c
000000010059816f	incq	%rdi
0000000100598172	leaq	-0x30(%rbp), %rsi
0000000100598176	movq	%rdi, CONFIG_EMULATE_HARDWARE(%rsi)
0000000100598179	movl	%r14d, %edx
000000010059817c	callq	__ZN7IAction6createEPKcPS1_i    ## IAction::create(char const*, char const**, int)
0000000100598181	movq	%rax, 0x40(%r15)
0000000100598185	testq	%rax, %rax
0000000100598188	je	0x1005981f5
000000010059818a	testb	$0x10, 0x15(%r15)
000000010059818f	movl	0x14(%rax), %ecx
0000000100598192	jne	0x1005981e7
0000000100598194	btl	$0xc, %ecx
0000000100598198	jb	0x1005981f0
000000010059819a	jmp	0x1005981f5
000000010059819c	leaq	0x1(%rdi), %rax
00000001005981a0	movq	%rax, -0x30(%rbp)
00000001005981a4	movb	0x1(%rdi), %bl
00000001005981a7	cmpb	$0x26, %bl
00000001005981aa	jne	0x1005981b7
00000001005981ac	addq	$0x2, %rdi
00000001005981b0	movq	%rdi, -0x30(%rbp)
00000001005981b4	movq	%rdi, %rax
00000001005981b7	leaq	-0x30(%rbp), %rsi
00000001005981bb	movq	%rax, %rdi
00000001005981be	movl	%r14d, %edx
00000001005981c1	callq	__ZN7IAction6createEPKcPS1_i    ## IAction::create(char const*, char const**, int)
00000001005981c6	movq	%rax, 0x38(%r15)
00000001005981ca	cmpb	$0x26, %bl
00000001005981cd	jne	0x1005981dd
00000001005981cf	testq	%rax, %rax
00000001005981d2	je	0x1005981dd
00000001005981d4	orb	$0x40, 0x16(%rax)
00000001005981d8	movl	-0x68(%rbp), %ebx
00000001005981db	jmp	0x100598219
00000001005981dd	testq	%rax, %rax
00000001005981e0	movl	-0x68(%rbp), %ebx
00000001005981e3	jne	0x100598219
00000001005981e5	jmp	0x10059823c
00000001005981e7	orl	$0x1000, %ecx                   ## imm = 0x1000
00000001005981ed	movl	%ecx, 0x14(%rax)
00000001005981f0	orb	$0x10, 0x15(%r15)
00000001005981f5	movq	-0x30(%rbp), %rdi
00000001005981f9	cmpb	$0x3a, CONFIG_EMULATE_HARDWARE(%rdi)
00000001005981fc	jne	0x10059823c
00000001005981fe	incq	%rdi
0000000100598201	leaq	-0x30(%rbp), %rsi
0000000100598205	movq	%rdi, CONFIG_EMULATE_HARDWARE(%rsi)
0000000100598208	movl	%r14d, %edx
000000010059820b	callq	__ZN7IAction6createEPKcPS1_i    ## IAction::create(char const*, char const**, int)
0000000100598210	movq	%rax, 0x48(%r15)
0000000100598214	testq	%rax, %rax
0000000100598217	je	0x10059823c
0000000100598219	testb	$0x10, 0x15(%r15)
000000010059821e	movl	0x14(%rax), %ecx
0000000100598221	jne	0x10059822b
0000000100598223	btl	$0xc, %ecx
0000000100598227	jb	0x100598237
0000000100598229	jmp	0x10059823c
000000010059822b	addq	$0x14, %rax
000000010059822f	orl	$0x1000, %ecx                   ## imm = 0x1000
0000000100598235	movl	%ecx, CONFIG_EMULATE_HARDWARE(%rax)
0000000100598237	orb	$0x10, 0x15(%r15)
000000010059823c	movq	-0xa8(%rbp), %rcx
0000000100598243	testq	%rcx, %rcx
0000000100598246	je	0x10059824f
0000000100598248	movq	-0x30(%rbp), %rax
000000010059824c	movq	%rax, CONFIG_EMULATE_HARDWARE(%rcx)
000000010059824f	movl	-0xac(%rbp), %eax
0000000100598255	cmpl	$0x616c6c, %eax                 ## imm = 0x616C6C
000000010059825a	jne	0x10059827d
000000010059825c	cmpl	$0x17a, %ebx                    ## imm = 0x17A
0000000100598262	je	0x10059827d
0000000100598264	callq	*0x28(%r13)
0000000100598268	movq	$0x5, 0xc(%rax)
0000000100598270	movl	%r12d, 0x14(%rax)
0000000100598274	movq	%r15, 0x38(%rax)
0000000100598278	movq	%rax, %r15
000000010059827b	jmp	0x10059828c
000000010059827d	cmpl	$0x616c6c, %eax                 ## imm = 0x616C6C
0000000100598282	jne	0x10059828c
0000000100598284	movl	$0x616c6c, 0x10(%r15)           ## imm = 0x616C6C
000000010059828c	testb	$0x1, -0x80(%rbp)
0000000100598290	je	0x10059833d
0000000100598296	movq	-0x70(%rbp), %rdi
000000010059829a	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
000000010059829f	jmp	0x10059833d
00000001005982a4	orl	$0x1000, %ecx                   ## imm = 0x1000
00000001005982aa	movl	%ecx, 0x14(%rax)
00000001005982ad	orb	$0x10, 0x15(%r15)
00000001005982b2	movq	-0x30(%rbp), %rax
00000001005982b6	cmpb	$0x26, CONFIG_EMULATE_HARDWARE(%rax)
00000001005982b9	jne	0x100598330
00000001005982bb	movq	%r15, %rdi
00000001005982be	callq	__Z26createAction_combine_queryP7IAction ## createAction_combine_query(IAction*)
00000001005982c3	movq	%rax, %r15
00000001005982c6	movq	-0x30(%rbp), %rax
00000001005982ca	leaq	0x1(%rax), %rdi
00000001005982ce	movq	%rdi, -0x30(%rbp)
00000001005982d2	movb	0x1(%rax), %bl
00000001005982d5	cmpb	$0x26, %bl
00000001005982d8	jne	0x1005982e5
00000001005982da	addq	$0x2, %rax
00000001005982de	movq	%rax, -0x30(%rbp)
00000001005982e2	movq	%rax, %rdi
00000001005982e5	leaq	-0x30(%rbp), %rsi
00000001005982e9	movl	%r12d, %edx
00000001005982ec	callq	__ZN7IAction6createEPKcPS1_i    ## IAction::create(char const*, char const**, int)
00000001005982f1	cmpb	$0x26, %bl
00000001005982f4	setne	%cl
00000001005982f7	movq	%rax, 0x38(%r15)
00000001005982fb	testq	%rax, %rax
00000001005982fe	sete	%dl
0000000100598301	orb	%cl, %dl
0000000100598303	je	0x10059830c
0000000100598305	testq	%rax, %rax
0000000100598308	jne	0x100598310
000000010059830a	jmp	0x100598330
000000010059830c	orb	$0x40, 0x16(%rax)
0000000100598310	testb	$0x10, 0x15(%r15)
0000000100598315	movl	0x14(%rax), %ecx
0000000100598318	jne	0x100598322
000000010059831a	btl	$0xc, %ecx
000000010059831e	jb	0x10059832b
0000000100598320	jmp	0x100598330
0000000100598322	orl	$0x1000, %ecx                   ## imm = 0x1000
0000000100598328	movl	%ecx, 0x14(%rax)
000000010059832b	orb	$0x10, 0x15(%r15)
0000000100598330	testq	%r13, %r13
0000000100598333	je	0x10059833d
0000000100598335	movq	-0x30(%rbp), %rax
0000000100598339	movq	%rax, (%r13)
000000010059833d	leaq	-0xa0(%rbp), %rax
0000000100598344	leaq	-0x60(%rbp), %rdi
0000000100598348	movq	%rax, CONFIG_EMULATE_HARDWARE(%rdi)
000000010059834b	callq	__ZNSt3__16vectorI12SActionParamNS_9allocatorIS1_EEE16__destroy_vectorclB8ne200100Ev ## std::__1::vector<SActionParam, std::__1::allocator<SActionParam>>::__destroy_vector::operator()[abi:ne200100]()
0000000100598350	movq	%r15, %rax
0000000100598353	addq	$rf.n_mfmvs, %rsp
000000010059835a	popq	%rbx
000000010059835b	popq	%r12
000000010059835d	popq	%r13
000000010059835f	popq	%r14
0000000100598361	popq	%r15
0000000100598363	popq	%rbp
0000000100598364	retq
0000000100598365	movq	%r13, -0xa8(%rbp)
000000010059836c	testq	%r13, %r13
000000010059836f	je	0x1005983aa
0000000100598371	movb	CONFIG_EMULATE_HARDWARE(%r14), %cl
0000000100598374	movq	%r14, %r12
0000000100598377	testb	%cl, %cl
0000000100598379	je	0x1005983ad
000000010059837b	xorl	%eax, %eax
000000010059837d	movq	%r14, %r12
0000000100598380	testl	%eax, %eax
0000000100598382	jne	0x100598389
0000000100598384	cmpb	$0x3a, %cl
0000000100598387	je	0x1005983ad
0000000100598389	cmpb	$0x3a, %cl
000000010059838c	je	0x10059839a
000000010059838e	movzbl	%cl, %ecx
0000000100598391	cmpl	$0x3f, %ecx
0000000100598394	jne	0x10059839c
0000000100598396	incl	%eax
0000000100598398	jmp	0x10059839c
000000010059839a	decl	%eax
000000010059839c	movb	0x1(%r12), %cl
00000001005983a1	incq	%r12
00000001005983a4	testb	%cl, %cl
00000001005983a6	jne	0x100598380
00000001005983a8	jmp	0x1005983ad
00000001005983aa	xorl	%r12d, %r12d
00000001005983ad	leaq	_actionFactory(%rip), %rax
00000001005983b4	callq	*0x1e8(%rax)
00000001005983ba	movq	%rax, %r15
00000001005983bd	movl	$0x3d, 0xc(%rax)
00000001005983c4	movl	-0x34(%rbp), %eax
00000001005983c7	movl	%eax, 0x10(%r15)
00000001005983cb	leaq	0x20(%r15), %rdi
00000001005983cf	xorps	%xmm0, %xmm0
00000001005983d2	leaq	-0x60(%rbp), %rsi
00000001005983d6	movaps	%xmm0, 0x10(%rsi)
00000001005983da	movaps	%xmm0, CONFIG_EMULATE_HARDWARE(%rsi)
00000001005983dd	movq	$CONFIG_EMULATE_HARDWARE, 0x20(%rsi)
00000001005983e5	callq	__ZNSt3__16vectorI12SActionParamNS_9allocatorIS1_EEE9push_backB8ne200100EOS1_ ## std::__1::vector<SActionParam, std::__1::allocator<SActionParam>>::push_back[abi:ne200100](SActionParam&&)
00000001005983ea	testb	$0x1, -0x58(%rbp)
00000001005983ee	je	0x1005983f9
00000001005983f0	movq	-0x48(%rbp), %rdi
00000001005983f4	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
00000001005983f9	movq	0x28(%r15), %r13
00000001005983fd	testq	%r12, %r12
0000000100598400	je	0x100598416
0000000100598402	movq	%r12, %rdx
0000000100598405	subq	%rbx, %rdx
0000000100598408	leaq	-0x60(%rbp), %rdi
000000010059840c	movq	%r14, %rsi
000000010059840f	callq	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEC2B8ne200100EPKcm ## std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>::basic_string[abi:ne200100](char const*, unsigned long)
0000000100598414	jmp	0x100598422
0000000100598416	leaq	-0x60(%rbp), %rdi
000000010059841a	movq	%r14, %rsi
000000010059841d	callq	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEC2B8ne200100ILi0EEEPKc ## std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>::basic_string[abi:ne200100]<0>(char const*)
0000000100598422	movl	$0x747874, -0x28(%r13)          ## imm = 0x747874
000000010059842a	leaq	-0x20(%r13), %rbx
000000010059842e	testb	$0x1, -0x20(%r13)
0000000100598433	je	0x10059843e
0000000100598435	movq	-0x10(%r13), %rdi
0000000100598439	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
000000010059843e	movq	-0x50(%rbp), %rax
0000000100598442	movq	%rax, 0x10(%rbx)
0000000100598446	movups	-0x60(%rbp), %xmm0
000000010059844a	movups	%xmm0, CONFIG_EMULATE_HARDWARE(%rbx)
000000010059844d	movb	$0x0, -0x8(%r13)
0000000100598452	cmpq	$0x0, -0xa8(%rbp)
000000010059845a	je	0x100598350
0000000100598460	movq	-0xa8(%rbp), %rax
0000000100598467	movq	%r12, CONFIG_EMULATE_HARDWARE(%rax)
000000010059846a	jmp	0x100598350
000000010059846f	movq	%rax, %rbx
0000000100598472	testb	$0x1, -0x58(%rbp)
0000000100598476	je	0x1005984d7
0000000100598478	movq	-0x48(%rbp), %rdi
000000010059847c	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
0000000100598481	jmp	0x1005984d7
0000000100598483	jmp	0x1005984b2
0000000100598485	jmp	0x100598491
0000000100598487	jmp	0x1005984b2
0000000100598489	jmp	0x1005984b2
000000010059848b	jmp	0x1005984ad
000000010059848d	jmp	0x1005984ad
000000010059848f	jmp	0x100598491
0000000100598491	movq	%rax, %rbx
0000000100598494	testb	$0x1, -0x58(%rbp)
0000000100598498	je	0x1005984b5
000000010059849a	movq	-0x48(%rbp), %rdi
000000010059849e	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
00000001005984a3	jmp	0x1005984b5
00000001005984a5	jmp	0x1005984b2
00000001005984a7	jmp	0x1005984b2
00000001005984a9	jmp	0x1005984b2
00000001005984ab	jmp	0x1005984ad
00000001005984ad	movq	%rax, %rbx
00000001005984b0	jmp	0x1005984c4
00000001005984b2	movq	%rax, %rbx
00000001005984b5	testb	$0x1, -0x80(%rbp)
00000001005984b9	je	0x1005984c4
00000001005984bb	movq	-0x70(%rbp), %rdi
00000001005984bf	callq	0x104fe873e                     ## symbol stub for: __ZdlPv
00000001005984c4	leaq	-0xa0(%rbp), %rax
00000001005984cb	leaq	-0x60(%rbp), %rdi
00000001005984cf	movq	%rax, CONFIG_EMULATE_HARDWARE(%rdi)
00000001005984d2	callq	__ZNSt3__16vectorI12SActionParamNS_9allocatorIS1_EEE16__destroy_vectorclB8ne200100Ev ## std::__1::vector<SActionParam, std::__1::allocator<SActionParam>>::__destroy_vector::operator()[abi:ne200100]()
00000001005984d7	movq	%rbx, %rdi
00000001005984da	callq	0x104fe8456                     ## symbol stub for: __Unwind_Resume
00000001005984df	nop
