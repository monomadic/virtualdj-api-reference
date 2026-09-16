0x1001c12ac: sub sp, sp, #0x70
0x1001c12b0: stp x28, x27, [sp, #0x10]
0x1001c12b4: stp x26, x25, [sp, #0x20]
0x1001c12b8: stp x24, x23, [sp, #0x30]
0x1001c12bc: stp x22, x21, [sp, #0x40]
0x1001c12c0: stp x20, x19, [sp, #0x50]
0x1001c12c4: stp x29, x30, [sp, #0x60]
0x1001c12c8: add x29, sp, #0x60
0x1001c12cc: cmp w7, #0x320
0x1001c12d0: b.lt #0x1001c1468
0x1001c12d4: mov x23, x1
0x1001c12d8: ldr x8, [x1, #0x28]
0x1001c12dc: cbz x8, #0x1001c1468
0x1001c12e0: mov x19, x6
0x1001c12e4: mov x20, x4
0x1001c12e8: mov x26, x2
0x1001c12ec: ldr w8, [x23]
0x1001c12f0: cmp w6, #0
0x1001c12f4: csel w9, w5, w6, eq
0x1001c12f8: madd w9, w9, w4, w2
0x1001c12fc: cmp w8, w9
0x1001c1300: b.lt #0x1001c1328
0x1001c1304: mov x22, x3
0x1001c1308: ldr w8, [x23, #4]
0x1001c130c: mov x9, x20
0x1001c1310: cbz w19, #0x1001c131c
0x1001c1314: mul w9, w5, w20
0x1001c1318: sdiv w9, w9, w19
0x1001c131c: add w9, w9, w22
0x1001c1320: cmp w8, w9
0x1001c1324: b.ge #0x1001c135c
0x1001c1328: adrp x0, #0x104012000
0x1001c132c: add x0, x0, #0x658
0x1001c1330: adrp x1, #0x103c05000 ; 'Error in skin icon definition! (Icons file too small to fit all icons)\n'
0x1001c1334: add x1, x1, #0xf4b
0x1001c1338: mov w2, #0x47
0x1001c133c: ldp x29, x30, [sp, #0x60]
0x1001c1340: ldp x20, x19, [sp, #0x50]
0x1001c1344: ldp x22, x21, [sp, #0x40]
0x1001c1348: ldp x24, x23, [sp, #0x30]
0x1001c134c: ldp x26, x25, [sp, #0x20]
0x1001c1350: ldp x28, x27, [sp, #0x10]
0x1001c1354: add sp, sp, #0x70
0x1001c1358: b #0x10014dfbc
0x1001c135c: bic w8, w5, w5, asr #31
0x1001c1360: mov w9, #0x99
0x1001c1364: cmp w8, #0x99
0x1001c1368: csel w21, w8, w9, lt
0x1001c136c: cmp w5, #1
0x1001c1370: b.lt #0x1001c1468
0x1001c1374: mov x25, #0
0x1001c1378: sxtw x8, w19
0x1001c137c: str x8, [sp, #8]
0x1001c1380: sxtw x27, w20
0x1001c1384: cbz w19, #0x1001c139c
0x1001c1388: ldr x8, [sp, #8]
0x1001c138c: udiv x9, x25, x8
0x1001c1390: msub x10, x9, x8, x25
0x1001c1394: cbnz w20, #0x1001c13a8
0x1001c1398: b #0x1001c145c
0x1001c139c: mov w9, #0
0x1001c13a0: mov x10, x25
0x1001c13a4: cbz w20, #0x1001c145c
0x1001c13a8: mov x8, #0
0x1001c13ac: madd w2, w20, w10, w26
0x1001c13b0: madd w3, w9, w20, w22
0x1001c13b4: ldr x10, [x23, #0x28]
0x1001c13b8: sxtw x9, w3
0x1001c13bc: ldrsw x11, [x23]
0x1001c13c0: add x10, x10, w2, sxtw #2
0x1001c13c4: add x10, x10, #3
0x1001c13c8: lsl x11, x11, #2
0x1001c13cc: mov w12, #1
0x1001c13d0: add x13, x9, x8
0x1001c13d4: madd x13, x11, x13, x10
0x1001c13d8: mov x14, x27
0x1001c13dc: mov x15, x13
0x1001c13e0: ldrb w16, [x15], #4
0x1001c13e4: cbnz w16, #0x1001c1404
0x1001c13e8: subs x14, x14, #1
0x1001c13ec: b.ne #0x1001c13e0
0x1001c13f0: add x8, x8, #1
0x1001c13f4: add x13, x13, x11
0x1001c13f8: cmp x8, x27
0x1001c13fc: b.ne #0x1001c13d8
0x1001c1400: b #0x1001c1418
0x1001c1404: mov w12, #0
0x1001c1408: add x8, x8, #1
0x1001c140c: cmp x8, x27
0x1001c1410: b.ne #0x1001c13d0
0x1001c1414: b #0x1001c141c
0x1001c1418: tbnz w12, #0, #0x1001c145c
0x1001c141c: adrp x24, #0x103ff9000
0x1001c1420: ldr x8, [x24, #0xba8]
0x1001c1424: add x28, x25, x25, lsl #2
0x1001c1428: add x0, x8, x28, lsl #5
0x1001c142c: mov x1, x23
0x1001c1430: mov x4, x20
0x1001c1434: mov x5, x20
0x1001c1438: bl #0x10037a7dc
0x1001c143c: ldr x8, [x24, #0xba8]
0x1001c1440: add x8, x8, x28, lsl #5
0x1001c1444: mov w9, #1
0x1001c1448: strb w9, [x8, #0x10]
0x1001c144c: ldrb w9, [x8, #0x11]
0x1001c1450: mov w10, #0x14
0x1001c1454: orr w9, w9, w10
0x1001c1458: strb w9, [x8, #0x11]
0x1001c145c: add x25, x25, #1
0x1001c1460: cmp x25, x21
0x1001c1464: b.ne #0x1001c1384
0x1001c1468: ldp x29, x30, [sp, #0x60]
0x1001c146c: ldp x20, x19, [sp, #0x50]
0x1001c1470: ldp x22, x21, [sp, #0x40]
0x1001c1474: ldp x24, x23, [sp, #0x30]
0x1001c1478: ldp x26, x25, [sp, #0x20]
0x1001c147c: ldp x28, x27, [sp, #0x10]
0x1001c1480: add sp, sp, #0x70
0x1001c1484: ret 
