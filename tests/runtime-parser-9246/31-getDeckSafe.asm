__Z11getDeckSafei [0x10047e085, 0x10047e0b0):
000000010047e085	pushq	%rbp
000000010047e086	movq	%rsp, %rbp
000000010047e089	callq	__Z7getDecki                    ## getDeck(int)
000000010047e08e	testq	%rax, %rax
000000010047e091	jne	0x10047e0ad
000000010047e093	movq	_defaultDeck(%rip), %rax
000000010047e09a	testq	%rax, %rax
000000010047e09d	jne	0x10047e0ad
000000010047e09f	movq	__ZN5CDeck5decksE(%rip), %rax   ## CDeck::decks
000000010047e0a6	movq	%rax, _defaultDeck(%rip)
000000010047e0ad	popq	%rbp
000000010047e0ae	retq
000000010047e0af	nop
