#!/usr/bin/env python3
fp_l    = ['divsd','mulsd', 'subsd', 'addsd', 'andpd', 'ucomisd', 'movsd', 'movapd', 'vmovsd', 'vmovss', 'vdivss', 'vxorps','vxorpd', 'vcvtsi2ss', 'vcvtss2sd','idiv','vmulsd','vcvtsi2sd']
br_l    = ['setbe', 'setnz','setz','setb','jmp','js', 'jz','jo' 'js', 'jp', 'jl', 'jnl', 'jbe', 'jnbe', 'jns', 'cmovs', 'cmovl', 'cmovns', 'cmovnle', 'cmovnl', 'cmovle', 'jnle', 'jnz', 'jnb', 'jb', 'jle', 'cmovz', 'cmovnz', 'cmovnbe', 'cmovb', 'cmovbe', 'cmovnb']
alu_l   = ['add','mul','imul', 'sub', 'psubb', 'or', 'por', 'and', 'xor', 'pxor', 'rol', 'mov', 'movd', 'movq', 'movzx', 'movsx', 'movsxd', 'movlpd', 'movhpd', 'movhps', 'movdqu', 'movdqa', 'movaps', 'pmovmskb', 'pmovmskpd', 'movmskpd', 'movups', 'lea', 'vmovq', 'vmovd', 'vmovdqu', 'vpmovmskb', 'vmovdqa', 'ror', 'adc', 'xadd', 'pcmpeqb', 'pcmpeqw', 'pcmpeqd', 'pcmpgtd', 'psrldq', 'punpcklbw', 'punpcklwd', 'punpckldq', 'punpckhqdq', 'punpckhdq', 'pminub', 'punpcklqdq', 'paddq', 'paddd', 'cmp', 'test', 'bt', 'shr', 'shl', 'pslldq', 'psllq', 'sar', 'sal', 'pslld', 'not', 'neg', 'inc', 'dec', 'sbb', 'pshufd', 'vpxor', 'vpcmpeqb', 'vpcmpgtb', 'shld', 'shrd', 'vpor', 'vpand', 'vpandn', 'vpsubb', 'vpcmpistri', 'vpslldq', 'vpalignr']
st_ld_l = ['push', 'stmxcsr', 'fnstcw', 'fldcw', 'ldmxcsr', 'cmpxchg', 'div', 'xsavec', 'xrstor', 'cqo', 'idiv', 'cmpsb', 'movsq', 'vzeroupper', 'rdtsc', 'bsf', 'bsr', 'vpbroadcastb', 'tzcnt', 'popcnt', 'pop', 'xchg', 'ret', 'cdqe', 'xgetbv', 'stosq','stosb']
misc_l  = ['call', 'nop', 'ret', 'int', 'into', 'iret', 'hlt', 'clc', 'stc', 'cli', 'sti', 'cld', 'std', 'wait', 'syscall', 'cpuid']
