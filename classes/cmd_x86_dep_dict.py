#!/usr/bin/env python3
cmd_x86 = {}


#commands that do a=a+b where + can be different operations
for cmd in ['add','addsd','sub','psubb','or','por','and','xor','pxor','rol','ror','adc','xadd','andpd',
            'pcmpeqb','pcmpeqw','pcmpeqd','pcmpgtd','psrldq',
            'punpcklbw','punpcklwd','punpckldq','punpckhqdq','punpckhdq','pminub','punpcklqdq','paddq','paddd']:
    cmd_data = {
        # 2 operand:
        2: {
            0: {
                'only_reg':       {'dep': True, 'change': True},
                'reg_for_memory': {'dep': True, 'change': False},
            },
            1: {
                'only_reg':       {'dep': True, 'change': False},
                'reg_for_memory': {'dep': True, 'change': False},
            },
        },
    }
    cmd_x86[cmd] = cmd_data

#commands that read single argument
for cmd in ['call','jmp','push','stmxcsr','fnstcw','fldcw','ldmxcsr']:
    cmd_data = {
        # 1 operand:
        1: {
            0: {
                'only_reg':       {'dep': True, 'change': False},
                'reg_for_memory': {'dep': True, 'change': False},
            }
        }
    }
    cmd_x86[cmd] = cmd_data

#comparsion commands - commands that read two arguments
for cmd in ['cmp','test','bt','ucomisd']:
    cmd_data = {
        # 2 operand:
        2: {
            0: {
                'only_reg':       {'dep': True, 'change': False},
                'reg_for_memory': {'dep': True, 'change': False},
            },
            1: {
                'only_reg':       {'dep': True, 'change': False},
                'reg_for_memory': {'dep': True, 'change': False},
            },
        },
    }
    cmd_x86[cmd] = cmd_data

#commands that read single argument and flags
for cmd in ['jz','js','jp','jl','jnl','jbe','jnbe','jns','jnle','jnz','jnb','jb','jle']: #add dependancy to last cmp?
    cmd_data = { 
        # jz 1 operand:
        1: {
            0: {
                'only_reg':       {'dep': True, 'change': False},
                'reg_for_memory': {'dep': True, 'change': False},
            },
        },
    }
    cmd_x86[cmd] = cmd_data

# shift operations
for cmd in ['shr','shl','pslldq','psllq','sar','sal','pslld']:
    cmd_data = {
        # 1 operand:
        1: {
            0: {
                'only_reg':       {'dep': True, 'change': True},
                'reg_for_memory': {'dep': True, 'change': False},
            },
        },
        # 2 operand:
        2: {
            0: {
                'only_reg':       {'dep': True, 'change': True},
                'reg_for_memory': {'dep': True, 'change': False},
            },
            1: {
                'only_reg':       {'dep': True, 'change': False},
                'reg_for_memory': {'dep': True, 'change': False},
            },
        },
    }
    cmd_x86[cmd] = cmd_data


# move operations
for cmd in ['mov','movd','movq','cmovs','cmovl','cmovns','cmovnle','cmovnl','cmovle','movzx','movsx','movsxd','movlpd','movhpd','movhps','movdqu','movdqa','movaps','pmovmskb','pmovmskpd','movmskpd','movups','lea','vmovq','vmovd','vmovdqu','vpmovmskb','vmovdqa','movsd','movapd','vmovsd','vmovss']: 
    cmd_data = {
        2: {
            0: {
                'only_reg':       {'dep': False, 'change': True},
                'reg_for_memory': {'dep': True, 'change': False}
            },
            1: {
                'only_reg':       {'dep': True, 'change': False},
                'reg_for_memory': {'dep': True, 'change': False}
            }
        }
    }
    cmd_x86[cmd] = cmd_data

#conditional move operations
for cmd in ['cmovz','cmovnz','cmovnbe','cmovb','cmovbe','cmovnb']: #add dependancy to last cmp?
    cmd_data = {
        2: {
            0: {
                'only_reg':       {'dep': False, 'change': True},
                'reg_for_memory': {'dep': True, 'change': False}
            },
            1: {
                'only_reg':       {'dep': True, 'change': False},
                'reg_for_memory': {'dep': True, 'change': False}
            }
        }
    }
    cmd_x86[cmd] = cmd_data

#commands that change a register based on its value
for cmd in ['not','neg','inc','dec']:
    cmd_data = {
        # neg 1 operand:
        1: {
            0: {
                'only_reg':       {'dep': True, 'change': True},
                'reg_for_memory': {'dep': True, 'change': False},
            },
        },
    }
    cmd_x86[cmd] = cmd_data

#commands that change a register based on cmp
for cmd in ['setnz','setnp','setnb','setnle','setnbe','setz','setbe','setb']: #add dependancy to last cmp?
    cmd_data = {  
        1: {
            0: {
                'only_reg':       {'dep': False, 'change': True},
                'reg_for_memory': {'dep': True, 'change': False},
            },
        },
    }
    cmd_x86[cmd] = cmd_data

# mul
cmd_data = {
    # mul 1 operand:
    1: {
        'special_reg_dependancy': ['a'],
        'special_reg_change': ['a', 'd'],
        0: {
            'only_reg':       {'dep': True, 'change': False},
            'reg_for_memory': {'dep': True, 'change': False}
        }
    },
}
cmd_x86['mul'] = cmd_data

# imul
cmd_data = {
    # imul 1 operand:
    1: {
        'special_reg_dependancy': ['a'],
        'special_reg_change': ['a', 'd'],
        0: {
            'only_reg':       {'dep': True, 'change': False},
            'reg_for_memory': {'dep': True, 'change': False}
        }
    },
    # imul 2 operand:
    2: {
        0: {
            'only_reg':       {'dep': True, 'change': True},
            'reg_for_memory': {'dep': True, 'change': False}
        },
        1: {
            'only_reg':       {'dep': True, 'change': False},
            'reg_for_memory': {'dep': True, 'change': False}
        }
    },
    # imul 3 operand:
    3: {
        0: {
            'only_reg':       {'dep': True, 'change': True},
            'reg_for_memory': {'dep': True, 'change': False}
        },
        1: {
            'only_reg':       {'dep': True, 'change': False},
            'reg_for_memory': {'dep': True, 'change': False}
        },
        2: {
            'only_reg':       {'dep': False, 'change': False},
            'reg_for_memory': {'dep': True, 'change': False}
        }
    }
}
cmd_x86['imul'] = cmd_data


# rdtsc
cmd_data = {
    # rdtsc 0 operand:
    0: {
        'special_reg_change': ['a', 'd'],
    },
}
cmd_x86['rdtsc'] = cmd_data

#commands that change destination based on source
for cmd in ['bsf','bsr','vpbroadcastb','tzcnt','popcnt']:
    cmd_data = {
        # 2 operand:
        2: {
            0: {
                'only_reg':       {'dep': False, 'change': True},
                'reg_for_memory': {'dep': True, 'change': False},
            },
            1: {
                'only_reg':       {'dep': True, 'change': False},
                'reg_for_memory': {'dep': True, 'change': False},
            },
        },
    }
    cmd_x86[cmd] = cmd_data

# pop
cmd_data = {
    # pop 1 operand:
    1: {
        0: {
            'only_reg':       {'dep': False, 'change': True},
            'reg_for_memory': {'dep': True, 'change': False},
        },
    },
}
cmd_x86['pop'] = cmd_data

# nop
cmd_data = {
    # nop 0 operand:
    0: {},
    # nop 2 operand:
    2: {
        0: {
            'only_reg':       {'dep': False, 'change': False},
            'reg_for_memory': {'dep': False, 'change': False},
        },
        1: {
            'only_reg':       {'dep': False, 'change': False},
            'reg_for_memory': {'dep': False, 'change': False},
        },

        },
}
cmd_x86['nop'] = cmd_data

# xchg
cmd_data = {
    # xchg 2 operand:
    2: {
        0: {
            'only_reg':       {'dep': True, 'change': True},
            'reg_for_memory': {'dep': True, 'change': False},
        },
        1: {
            'only_reg':       {'dep': True, 'change': True},
            'reg_for_memory': {'dep': True, 'change': False},
        },

    },
}
cmd_x86['xchg'] = cmd_data

# ret
cmd_data = {
    # ret 0 operand:
    0: {},
}
cmd_x86['ret'] = cmd_data

# cdqe
cmd_data = {
    # cdqe 0 operand:
    0: {
        'special_reg_dependancy': ['a'],
        'special_reg_change': ['a'],
    },
}
cmd_x86['cdqe'] = cmd_data

# syscall
cmd_data = {
    # syscall 0 operand:
    0: {
        'special_reg_dependancy': ['a','di','si','r10','r8','r9'],
    },
}
cmd_x86['syscall'] = cmd_data

# cpuid
cmd_data = {
    # cpuid 0 operand:
    0: {
        'special_reg_dependancy': ['a'],
        'special_reg_change': ['a','b','c','d'],
    },
}
cmd_x86['cpuid'] = cmd_data

# xgetbv
cmd_data = {
    # xgetbv 0 operand:
    0: {
        'special_reg_dependancy': ['c'],
    },
}
cmd_x86['xgetbv'] = cmd_data

#sbb
cmd_data = {  #add dependancy to last cmp?
    #sbb 2 operand:
    2: {
        0: {
            'only_reg':       {'dep': True, 'change': True},
            'reg_for_memory': {'dep': True, 'change': False},
        },
        1: {
            'only_reg':       {'dep': True, 'change': False},
            'reg_for_memory': {'dep': True, 'change': False},
        },
    },
}
cmd_x86['sbb'] = cmd_data

# pshufd 
cmd_data = {
    # pshufd  3 operand:
    3: {
        0: {
            'only_reg':       {'dep': False, 'change': True},
            'reg_for_memory': {'dep': True, 'change': False}
        },
        1: {
            'only_reg':       {'dep': True, 'change': False},
            'reg_for_memory': {'dep': True, 'change': False}
        },
        2: {
            'only_reg':       {'dep': True, 'change': False},
            'reg_for_memory': {'dep': True, 'change': False}
        }
    }
}
cmd_x86['pshufd'] = cmd_data

for cmd in ['stosq','stosb']:
    cmd_data = {
        # 0 operand:
        0: {
            'special_reg_dependancy': ['di','a'],
            'special_reg_change': ['di'],
        },
        # 1 operand:
        1: {
            'special_reg_dependancy': ['di','a'],
            'special_reg_change': ['di'],
            0: {
                'only_reg':       {'dep': True, 'change': False},
                'reg_for_memory': {'dep': True, 'change': False}
            }
        },
    }
    cmd_x86[cmd] = cmd_data

# div
cmd_data = {
    # div 1 operand:
    1: {
        'special_reg_dependancy': ['d','a'],
        'special_reg_change': ['d','a'],
        0: {
            'only_reg':       {'dep': True, 'change': False},
            'reg_for_memory': {'dep': True, 'change': False}
        }
    },
}
cmd_x86['div'] = cmd_data

# xsavec
cmd_data = {
    # xsavec 1 operand:
    1: {
        0: {
            'only_reg':       {'dep': True, 'change': False},
            'reg_for_memory': {'dep': True, 'change': False}
        }
    },
    # xsavec 2 operand:
    2: {
        0: {
            'only_reg':       {'dep': True, 'change': False},
            'reg_for_memory': {'dep': True, 'change': False}
        },
        0: {
            'only_reg':       {'dep': True, 'change': False},
            'reg_for_memory': {'dep': True, 'change': False}
        }
    },
}
cmd_x86['xsavec'] = cmd_data

# xrstor
cmd_data = {
    # xrstor 1 operand:
    1: {
        0: {
            'only_reg':       {'dep': True, 'change': False},
            'reg_for_memory': {'dep': True, 'change': False}
        }
    },
}
cmd_x86['xrstor'] = cmd_data

# cmpxchg
cmd_data = {
    # cmpxchg 2 operand:
    2: {
        0: {
            'only_reg':       {'dep': True, 'change': False}, # shouldn't get here
            'reg_for_memory': {'dep': True, 'change': False}
        },
        1: {
            'only_reg':       {'dep': True, 'change': True},
            'reg_for_memory': {'dep': True, 'change': False}
        }
    },
}
cmd_x86['cmpxchg'] = cmd_data


for cmd in ['vpxor','vpcmpeqb','vpcmpgtb','shld','shrd','vpor','vpand','vpandn','vdivss','vpsubb','vpcmpistri','vpslldq','vxorps','vcvtsi2ss','vcvtss2sd']:
    cmd_data = {
        3: {
            0: {
                'only_reg':       {'dep': False, 'change': True},
                'reg_for_memory': {'dep': True, 'change': False}
            },
            1: {
                'only_reg':       {'dep': True, 'change': False},
                'reg_for_memory': {'dep': True, 'change': False}
            },
            2: {
                'only_reg':       {'dep': True, 'change': False},
                'reg_for_memory': {'dep': True, 'change': False}
            }
        },
    }
    cmd_x86[cmd] = cmd_data

# cqo
cmd_data = {
    # cqo 0 operand:
    0: {
        'special_reg_dependancy': ['a'],
        'special_reg_change': ['a']
    }
}
cmd_x86['cqo'] = cmd_data

# idiv
cmd_data = {
    # idiv 1 operand:
    1: {
        'special_reg_dependancy': ['d'],
        'special_reg_change': ['d'],
        0: {
                'only_reg':       {'dep': True, 'change': False},
                'reg_for_memory': {'dep': True, 'change': False}
            },
    },

}
cmd_x86['idiv'] = cmd_data

# cmpsb
cmd_data = {
    # cmpsb 0 operand:
    0: {
        'special_reg_dependancy': ['si','di'],
    },
    2: {
        'special_reg_dependancy': ['si','di'],
        'special_reg_change': ['si','di'],
        0: {
                'only_reg':       {'dep': True, 'change': False},
                'reg_for_memory': {'dep': True, 'change': False}
            },
        1: {
                'only_reg':       {'dep': True, 'change': False},
                'reg_for_memory': {'dep': True, 'change': False}
            },
    },

}
cmd_x86['cmpsb'] = cmd_data


# movsq
cmd_data = {
    # movsq 0 operand:
    0: {
        'special_reg_dependancy': ['si','di'],
        'special_reg_change': ['si','di'],
    },
    # movsq 2 operand:
    2: {
        'special_reg_dependancy': ['si','di'],
        'special_reg_change': ['si','di'],
        0: {
                'only_reg':       {'dep': True, 'change': True},
                'reg_for_memory': {'dep': True, 'change': False}
            },
        1: {
                'only_reg':       {'dep': True, 'change': False},
                'reg_for_memory': {'dep': True, 'change': False}
            },
    },

}
cmd_x86['movsq'] = cmd_data

# vpalignr
cmd_data = {
    # vpalignr 4 operand:
    4: {
        'special_reg_dependancy': ['si','di'],
        'special_reg_change': ['si','di'],
        0: {
                'only_reg':       {'dep': False, 'change': True},
                'reg_for_memory': {'dep': True, 'change': False}
            },
        1: {
                'only_reg':       {'dep': True, 'change': False},
                'reg_for_memory': {'dep': True, 'change': False}
            },
        2: {
                'only_reg':       {'dep': True, 'change': False},
                'reg_for_memory': {'dep': True, 'change': False}
            },
        3: {
                'only_reg':       {'dep': True, 'change': False},
                'reg_for_memory': {'dep': True, 'change': False}
            },
    },

}
cmd_x86['vpalignr'] = cmd_data

# vzeroupper
cmd_data = {
    # vzeroupper 0 operand:
    0: {
        'special_reg_dependancy': [f'xmm{i}' for i in range(8)],
        'special_reg_change': [f'xmm{i}' for i in range(8)]
    }
}
cmd_x86['vzeroupper'] = cmd_data

