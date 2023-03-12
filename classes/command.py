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
        self.id             = 0 

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
        alu_l =  ['imul','xchg','cdqe','neg','add', 'sub','psubb', 'imul', 'xor', 'and', 'or', 'shl', 'shr', 'sar','pslldq','movzx','movdql','movdqa','movdqu','pmovmskb','cmovz','cmovnz','movsxd', 'cmp','pcmpeqb', 'test']
        br_l =  ['nop','jmp','jz', 'jb','jle', 'jbe', 'jnb', 'jnz', 'jnbe', 'syscall']
        misc_l =  ['cpuid','call', 'rdtsc', 'ret','pop','push','xgetbv']
        store_load_l =  ['lea','mov']
        known_type = alu_l + br_l + misc_l + store_load_l

        if unit_type == 'alu':
            if self.cmd_type in alu_l:
                return True
        if unit_type == 'br':
            if self.cmd_type in br_l:
                return True
        if unit_type == 'misc':
            if self.cmd_type in misc_l:
                return True
        if unit_type == 'store_load':
            if self.cmd_type in store_load_l:
                return True

        return self.cmd_type not in known_type

    def __str__(self):
        s = ''
        s += f'{self.thread.thread_id}_{self.id} -> {self.org_cmd}  : '
        s += f' state : {self.state}'
        if self.dependency:
            s += f'\n\tDependancies :\n'
            for c in self.dependency:
                s += f'\t{c.thread.thread_id}_{c.id}  {c.cmd_type}  ({c.state})\n'
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
        # print(f'{self.org_adress}   ==  Done')
        self.state = 'done'



