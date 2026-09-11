10002a4c6: push rbp 
10002a4c7: mov rbp, rsp 
10002a4ca: push r15 
10002a4cc: push r14 
10002a4ce: push r13 
10002a4d0: push r12 
10002a4d2: push rbx 
10002a4d3: sub rsp, 0x18 
10002a4d7: mov rbx, rdi 
10002a4da: mov dword ptr [rdi], 0 
10002a4e0: xorps xmm0, xmm0 
10002a4e3: movups xmmword ptr [rdi + 8], xmm0 
10002a4e7: movups xmmword ptr [rdi + 0x18], xmm0 
10002a4eb: movups xmmword ptr [rdi + 0x28], xmm0 
10002a4ef: movups xmmword ptr [rdi + 0x38], xmm0 
10002a4f3: movups xmmword ptr [rdi + 0x48], xmm0 
10002a4f7: movups xmmword ptr [rdi + 0x58], xmm0 
10002a4fb: movups xmmword ptr [rdi + 0x68], xmm0 
10002a4ff: mov qword ptr [rdi + 0x78], 0 
10002a507: call 0x100d41dc0 _RSA_new
10002a50c: mov qword ptr [rbx + 0x80], rax 
10002a513: lea rdi, [rip + 0x59fc856] 
10002a51a: mov esi, 0x81 
10002a51f: xor edx, edx 
10002a521: call 0x100b15ed0 _BN_bin2bn
10002a526: mov r14, rax 
10002a529: lea rdi, [rip + 0x59fc8c1] 
10002a530: mov esi, 3 
10002a535: xor edx, edx 
10002a537: call 0x100b15ed0 _BN_bin2bn
10002a53c: mov rdi, qword ptr [rbx + 0x80] 
10002a543: mov rsi, r14 
10002a546: mov rdx, rax 
10002a549: xor ecx, ecx 
10002a54b: call 0x100d42840 _RSA_set0_key
10002a550: add rsp, 0x18 
10002a554: pop rbx 
10002a555: pop r12 
10002a557: pop r13 
10002a559: pop r14 
10002a55b: pop r15 
10002a55d: pop rbp 
