0x1002581e4: ldr w8, [x0, #0xa0]
0x1002581e8: mov w9, #0xa0
0x1002581ec: adrp x10, #0x103fee000
0x1002581f0: add x10, x10, #0xa0
0x1002581f4: umaddl x9, w8, w9, x10
0x1002581f8: cmp w8, #0
0x1002581fc: csel x0, xzr, x9, lt
0x100258200: ret 
