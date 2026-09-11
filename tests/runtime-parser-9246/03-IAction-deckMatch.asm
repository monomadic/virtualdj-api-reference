__ZN7IAction9deckMatchERPKcRi [0x100599000, 0x1005991f8):
0000000100599000	pushq	%rbp
0000000100599001	movq	%rsp, %rbp
0000000100599004	pushq	%r15
0000000100599006	pushq	%r14
0000000100599008	pushq	%rbx
0000000100599009	pushq	%rax
000000010059900a	movq	%rsi, %r14
000000010059900d	movq	%rdi, %r15
0000000100599010	callq	__Z11numberMatchRPKcRi          ## numberMatch(char const*&, int&)
0000000100599015	movb	$0x1, %bl
0000000100599017	testb	%al, %al
0000000100599019	jne	0x1005991e6
000000010059901f	leaq	0x504f3ea(%rip), %rsi           ## literal pool for: "default"
0000000100599026	movq	%r15, %rdi
0000000100599029	callq	__ZN7IAction11stringMatchERPKcS1_ ## IAction::stringMatch(char const*&, char const*)
000000010059902e	movl	$0x646566, %ecx                 ## imm = 0x646566
0000000100599033	testb	%al, %al
0000000100599035	jne	0x1005991e3
000000010059903b	leaq	0x504e8af(%rip), %rsi           ## literal pool for: "active"
0000000100599042	movq	%r15, %rdi
0000000100599045	callq	__ZN7IAction11stringMatchERPKcS1_ ## IAction::stringMatch(char const*&, char const*)
000000010059904a	movl	$0x61637469, %ecx               ## imm = 0x61637469
000000010059904f	testb	%al, %al
0000000100599051	jne	0x1005991e3
0000000100599057	leaq	0x504492c(%rip), %rsi           ## literal pool for: "automix"
000000010059905e	movq	%r15, %rdi
0000000100599061	callq	__ZN7IAction11stringMatchERPKcS1_ ## IAction::stringMatch(char const*&, char const*)
0000000100599066	movl	$0x6175746f, %ecx               ## imm = 0x6175746F
000000010059906b	testb	%al, %al
000000010059906d	jne	0x1005991e3
0000000100599073	leaq	0x5043756(%rip), %rsi           ## literal pool for: "karaoke"
000000010059907a	movq	%r15, %rdi
000000010059907d	callq	__ZN7IAction11stringMatchERPKcS1_ ## IAction::stringMatch(char const*&, char const*)
0000000100599082	movl	$0x6b617261, %ecx               ## imm = 0x6B617261
0000000100599087	testb	%al, %al
0000000100599089	jne	0x1005991e3
000000010059908f	leaq	0x50507aa(%rip), %rsi           ## literal pool for: "left"
0000000100599096	movq	%r15, %rdi
0000000100599099	callq	__ZN7IAction11stringMatchERPKcS1_ ## IAction::stringMatch(char const*&, char const*)
000000010059909e	movl	$0x6c656674, %ecx               ## imm = 0x6C656674
00000001005990a3	testb	%al, %al
00000001005990a5	jne	0x1005991e3
00000001005990ab	leaq	0x5050793(%rip), %rsi           ## literal pool for: "right"
00000001005990b2	movq	%r15, %rdi
00000001005990b5	callq	__ZN7IAction11stringMatchERPKcS1_ ## IAction::stringMatch(char const*&, char const*)
00000001005990ba	movl	$0x72696768, %ecx               ## imm = 0x72696768
00000001005990bf	testb	%al, %al
00000001005990c1	jne	0x1005991e3
00000001005990c7	leaq	0x504ee82(%rip), %rsi           ## literal pool for: "master"
00000001005990ce	movq	%r15, %rdi
00000001005990d1	callq	__ZN7IAction11stringMatchERPKcS1_ ## IAction::stringMatch(char const*&, char const*)
00000001005990d6	movl	$0x6d617374, %ecx               ## imm = 0x6D617374
00000001005990db	testb	%al, %al
00000001005990dd	jne	0x1005991e3
00000001005990e3	leaq	0x5058580(%rip), %rsi           ## literal pool for: "sandbox"
00000001005990ea	movq	%r15, %rdi
00000001005990ed	callq	__ZN7IAction11stringMatchERPKcS1_ ## IAction::stringMatch(char const*&, char const*)
00000001005990f2	movl	$0x73616e64, %ecx               ## imm = 0x73616E64
00000001005990f7	testb	%al, %al
00000001005990f9	jne	0x1005991e3
00000001005990ff	leaq	0x5061f0e(%rip), %rsi           ## literal pool for: "none"
0000000100599106	movq	%r15, %rdi
0000000100599109	callq	__ZN7IAction11stringMatchERPKcS1_ ## IAction::stringMatch(char const*&, char const*)
000000010059910e	movl	$0x6e6f6e65, %ecx               ## imm = 0x6E6F6E65
0000000100599113	testb	%al, %al
0000000100599115	jne	0x1005991e3
000000010059911b	leaq	0x505b18b(%rip), %rsi           ## literal pool for: "all"
0000000100599122	movq	%r15, %rdi
0000000100599125	callq	__ZN7IAction11stringMatchERPKcS1_ ## IAction::stringMatch(char const*&, char const*)
000000010059912a	movl	$0x616c6c, %ecx                 ## imm = 0x616C6C
000000010059912f	testb	%al, %al
0000000100599131	jne	0x1005991e3
0000000100599137	leaq	0x5057637(%rip), %rsi           ## literal pool for: "leftvideo"
000000010059913e	movq	%r15, %rdi
0000000100599141	callq	__ZN7IAction11stringMatchERPKcS1_ ## IAction::stringMatch(char const*&, char const*)
0000000100599146	movl	$0x766c6566, %ecx               ## imm = 0x766C6566
000000010059914b	testb	%al, %al
000000010059914d	jne	0x1005991e3
0000000100599153	leaq	0x5058236(%rip), %rsi           ## literal pool for: "rightvideo"
000000010059915a	movq	%r15, %rdi
000000010059915d	callq	__ZN7IAction11stringMatchERPKcS1_ ## IAction::stringMatch(char const*&, char const*)
0000000100599162	movl	$0x76726967, %ecx               ## imm = 0x76726967
0000000100599167	testb	%al, %al
0000000100599169	jne	0x1005991e3
000000010059916b	leaq	0x50782dd(%rip), %rsi           ## literal pool for: "playing"
0000000100599172	movq	%r15, %rdi
0000000100599175	callq	__ZN7IAction11stringMatchERPKcS1_ ## IAction::stringMatch(char const*&, char const*)
000000010059917a	movl	$0x706c6179, %ecx               ## imm = 0x706C6179
000000010059917f	testb	%al, %al
0000000100599181	jne	0x1005991e3
0000000100599183	leaq	0x507eb06(%rip), %rsi           ## literal pool for: "mixer1"
000000010059918a	movq	%r15, %rdi
000000010059918d	callq	__ZN7IAction11stringMatchERPKcS1_ ## IAction::stringMatch(char const*&, char const*)
0000000100599192	movl	$0x6d697831, %ecx               ## imm = 0x6D697831
0000000100599197	testb	%al, %al
0000000100599199	jne	0x1005991e3
000000010059919b	leaq	0x507eaf5(%rip), %rsi           ## literal pool for: "mixer2"
00000001005991a2	movq	%r15, %rdi
00000001005991a5	callq	__ZN7IAction11stringMatchERPKcS1_ ## IAction::stringMatch(char const*&, char const*)
00000001005991aa	movl	$0x6d697832, %ecx               ## imm = 0x6D697832
00000001005991af	testb	%al, %al
00000001005991b1	jne	0x1005991e3
00000001005991b3	leaq	0x507eae4(%rip), %rsi           ## literal pool for: "mixer3"
00000001005991ba	movq	%r15, %rdi
00000001005991bd	callq	__ZN7IAction11stringMatchERPKcS1_ ## IAction::stringMatch(char const*&, char const*)
00000001005991c2	movl	$0x6d697833, %ecx               ## imm = 0x6D697833
00000001005991c7	testb	%al, %al
00000001005991c9	jne	0x1005991e3
00000001005991cb	leaq	0x507ead3(%rip), %rsi           ## literal pool for: "mixer4"
00000001005991d2	movq	%r15, %rdi
00000001005991d5	callq	__ZN7IAction11stringMatchERPKcS1_ ## IAction::stringMatch(char const*&, char const*)
00000001005991da	movl	$0x6d697834, %ecx               ## imm = 0x6D697834
00000001005991df	testb	%al, %al
00000001005991e1	je	0x1005991f3
00000001005991e3	movl	%ecx, CONFIG_EMULATE_HARDWARE(%r14)
00000001005991e6	movl	%ebx, %eax
00000001005991e8	addq	$0x8, %rsp
00000001005991ec	popq	%rbx
00000001005991ed	popq	%r14
00000001005991ef	popq	%r15
00000001005991f1	popq	%rbp
00000001005991f2	retq
00000001005991f3	xorl	%ebx, %ebx
00000001005991f5	jmp	0x1005991e6
00000001005991f7	nop
