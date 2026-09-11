10002c6e6: push rbp 
10002c6e7: mov rbp, rsp 
10002c6ea: push r14 
10002c6ec: push rbx 
10002c6ed: sub rsp, 0x90 
10002c6f4: mov rax, qword ptr [rip + 0x579392d] 
10002c6fb: mov rax, qword ptr [rax] 
10002c6fe: mov qword ptr [rbp - 0x18], rax 
10002c702: cmp rcx, 0x90 
10002c709: jb 0x10002c762 
10002c70b: mov rbx, rdx 
10002c70e: mov eax, dword ptr [rdx] 
10002c710: and eax, 0xfffffff8 
10002c713: add rax, 0x94 
10002c719: cmp rax, rcx 
10002c71c: ja 0x10002c762 
10002c71e: mov r14, rsi 
10002c721: lea rsi, [rbx + 0xc] 
10002c725: mov rcx, qword ptr [rdi + 0x80] 
10002c72c: lea rdx, [rbp - 0xa0] 
10002c733: mov edi, 0x80 
10002c738: mov r8d, 1 
10002c73e: call 0x100d3f8c0 _RSA_public_decrypt
10002c743: cmp eax, 4 
10002c746: jl 0x10002c762 
10002c748: mov ecx, 0x4456 
10002c74d: xor ecx, dword ptr [rbp - 0xa0] 
10002c753: movzx edx, byte ptr [rbp - 0x9e] 
10002c75a: xor edx, 0x4a 
10002c75d: or dx, cx 
10002c760: je 0x10002c780 
10002c762: xor eax, eax 
10002c764: mov rcx, qword ptr [rip + 0x57938bd] 
10002c76b: mov rcx, qword ptr [rcx] 
10002c76e: cmp rcx, qword ptr [rbp - 0x18] 
10002c772: jne 0x10002c7a3 
10002c774: add rsp, 0x90 
10002c77b: pop rbx 
10002c77c: pop r14 
10002c77e: pop rbp 
10002c77f: ret  
10002c780: mov edx, dword ptr [rbx] 
10002c782: add rbx, 0x8c 
10002c789: lea rcx, [rbp - 0x9d] 
10002c790: add eax, -3 
10002c793: mov rdi, r14 
10002c796: mov rsi, rbx 
10002c799: mov r8, rax 
10002c79c: call 0x1004a7596 CZip::openEncrypted(unsigned char const*, unsigned long, unsigned char const*, unsigned long)
10002c7a1: jmp 0x10002c764 
10002c7a3: call 0x104fe882e 
