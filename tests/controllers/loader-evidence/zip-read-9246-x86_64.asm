1004a73fd: push rbp 
1004a73fe: mov rbp, rsp 
1004a7401: push r15 
1004a7403: push r14 
1004a7405: push r13 
1004a7407: push r12 
1004a7409: push rbx 
1004a740a: push rax 
1004a740b: mov qword ptr [rbp - 0x30], rdx 
1004a740f: test rsi, rsi 
1004a7412: je 0x1004a74c5 
1004a7418: mov rbx, rcx 
1004a741b: mov r15, rsi 
1004a741e: mov eax, dword ptr [rsi + 0x1050] 
1004a7424: mov ecx, dword ptr [rsi + 0x1054] 
1004a742a: add ebx, eax 
1004a742c: cmp ecx, ebx 
1004a742e: cmovl ebx, ecx 
1004a7431: xor r12d, r12d 
1004a7434: cmp eax, ebx 
1004a7436: jge 0x1004a74cc 
1004a743c: lea r13, [r15 + 0x105c] 
1004a7443: mov r14d, eax 
1004a7446: and r14d, 0xfffffff8 
1004a744a: cmp r14d, dword ptr [r15 + 0x1058] 
1004a7451: je 0x1004a7478 
1004a7453: movsxd rdi, r14d 
1004a7456: add rdi, qword ptr [r15 + 0x1048] 
1004a745d: mov rsi, r13 
1004a7460: mov rdx, r15 
1004a7463: xor ecx, ecx 
1004a7465: call 0x100af0110 _BF_ecb_encrypt
1004a746a: mov dword ptr [r15 + 0x1058], r14d 
1004a7471: mov eax, dword ptr [r15 + 0x1050] 
1004a7478: mov ecx, r14d 
1004a747b: sub ecx, eax 
1004a747d: add ecx, 8 
1004a7480: mov edx, ebx 
1004a7482: sub edx, eax 
1004a7484: cmp edx, ecx 
1004a7486: cmovge edx, ecx 
1004a7489: movsxd r12, r12d 
1004a748c: mov rcx, qword ptr [rbp - 0x30] 
1004a7490: lea rdi, [rcx + r12] 
1004a7494: sub eax, r14d 
1004a7497: movsxd rsi, eax 
1004a749a: add rsi, r13 
1004a749d: movsxd r14, edx 
1004a74a0: mov rdx, r14 
1004a74a3: call 0x104fe8ed0 
1004a74a8: mov eax, dword ptr [r15 + 0x1050] 
1004a74af: add eax, r14d 
1004a74b2: mov dword ptr [r15 + 0x1050], eax 
1004a74b9: add r12d, r14d 
1004a74bc: cmp eax, ebx 
1004a74be: jl 0x1004a7443 
1004a74c0: movsxd r12, r12d 
1004a74c3: jmp 0x1004a74cc 
1004a74c5: mov r12, 0xffffffffffffffff 
1004a74cc: mov rax, r12 
1004a74cf: add rsp, 8 
1004a74d3: pop rbx 
1004a74d4: pop r12 
1004a74d6: pop r13 
1004a74d8: pop r14 
1004a74da: pop r15 
1004a74dc: pop rbp 
1004a74dd: ret  
