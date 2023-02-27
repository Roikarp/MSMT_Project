#!/usr/bin/env python3
import os
import sys
sys.path.insert(1, f'{os.getcwd()}/../')
from cycle import *

class command:
    def __init__(self,cmd_line=None):
        self.org_cmd        = ""
        self.thread         = None
        self.org_adress     = ""
        self.state          = "" #Pending/issue/execution/done/missed
        self.cmd_type       = ""
        self.dependency     = set()
        self.log            = []
        self.penalty_finish = 0

    def is_done(self):
        return self.state == 'done'
    def is_missed(self):
        return self.state == 'missed'

    def is_ready(self):
        for c in self.dependency:
            if not c.is_done():
                return False
        return True

    def is_type(self, unit_type):
        if unit_type == 'alu':
            return self.cmd_type in ['imul','xchg','cdqe','neg','add', 'sub','psubb', 'imul', 'xor', 'and', 'or', 'shl', 'shr', 'sar','pslldq','mov','movzx','movdql','movdqa','movdqu','pmovmskb','cmovz','cmovnz','movsxd', 'cmp','pcmpeqb', 'test']
        if unit_type == 'br':
            return self.cmd_type in ['nop','jmp','jz', 'jb','jle', 'jbe', 'jnb', 'jnz', 'jnbe', 'syscall']
        if unit_type == 'misc':
            return self.cmd_type in ['cpuid','call', 'rdtsc', 'ret','pop','push']
        if unit_type == 'store_load':
            return self.cmd_type in ['lea']

        return False

    def __str__(self):
        s = ''
        s += f'{self.org_cmd}  :\n'
        s += f'\tstate : {self.state}\n'
        if self.dependency:
            s += f'\tdependancies :\n'
            for c in self.dependency:
                s += f'\t{c.org_adress}\n'
        return s

    def add_to_thread(self):
        if self.is_done():
            self.thread.done_cmds.append(self)
        elif self.is_missed():
            self.thread.cmds = [self] + self.thread.cmds
    
    def set_missed(self,miss_penalty):
        self.state = 'missed'
        self.penalty_finish = get_cycle() + miss_penalty
        self.thread.penalty_finish = self.penalty_finish
        self.thread.state = 'missed_penalty'

    def set_done(self):
        self.state = 'done'



