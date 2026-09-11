1004a7596: push rbp 
1004a7597: mov rbp, rsp 
1004a759a: push r15 
1004a759c: push r14 
1004a759e: push r13 
1004a75a0: push r12 
1004a75a2: push rbx 
1004a75a3: push rax 
1004a75a4: mov r13, r8 
1004a75a7: mov r12, rcx 
1004a75aa: mov qword ptr [rbp - 0x30], rdx 
1004a75ae: mov r15, rsi 
1004a75b1: mov rbx, rdi 
1004a75b4: call 0x1004a6050 CZip::close()
1004a75b9: mov edi, 0x1068 
1004a75be: call 0x104fe8e94 
1004a75c3: test rax, rax 
1004a75c6: je 0x1004a761c 
1004a75c8: mov r14, rax 
1004a75cb: mov rdi, rax 
1004a75ce: mov esi, r13d 
1004a75d1: mov rdx, r12 
1004a75d4: call 0x100af2670 _BF_set_key
1004a75d9: mov qword ptr [r14 + 0x1048], r15 
1004a75e0: mov rax, qword ptr [rbp - 0x30] 
1004a75e4: mov dword ptr [r14 + 0x1054], eax 
1004a75eb: mov dword ptr [r14 + 0x1050], 0 
1004a75f6: mov dword ptr [r14 + 0x1058], 0xffffffff 
1004a7601: lea rsi, [rip + 0x5595140] 
1004a7608: mov rdi, r14 
1004a760b: call 0x10041ff7c _unzOpen2
1004a7610: mov qword ptr [rbx + 0x40], rax 
1004a7614: test rax, rax 
1004a7617: setne al 
1004a761a: jmp 0x1004a761e 
1004a761c: xor eax, eax 
1004a761e: add rsp, 8 
1004a7622: pop rbx 
1004a7623: pop r12 
1004a7625: pop r13 
1004a7627: pop r14 
1004a7629: pop r15 
1004a762b: pop rbp 
1004a762c: ret  
1004a762d: nop  
