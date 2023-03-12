#!/usr/bin/env python3
import os
import sys
sys.path.insert(1, f'{os.getcwd()}/../')
from cycle import *
from cmd_x86_exec_dict import fp_l, br_l, alu_l, st_ld_l, misc_l


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
        self.use_mem        = False

    def is_done(self):
        return self.state == 'done'
    def is_missed(self):
        return 'missed' in self.state

    def is_ready(self):
        for c in self.dependency:
            if not c.is_done():
                return False
        return True

    def is_type(self, unit_type):
        known_type = alu_l + br_l + fp_l + st_ld_l + misc_l

        if self.use_mem:
            if unit_type == 'alu_st_ld':
                if self.cmd_type in alu_l:
                    return True
            if unit_type == 'br_st_ld':
                if self.cmd_type in br_l:
                    return True
            if unit_type == 'misc_st_ld':
                if self.cmd_type in misc_l:
                    return True
        else:
            if unit_type == 'alu':
                if self.cmd_type in alu_l:
                    return True
            if unit_type == 'br':
                if self.cmd_type in br_l:
                    return True
            if unit_type == 'misc':
                if self.cmd_type in misc_l:
                    return True

        if unit_type == 'st_ld':
            if self.cmd_type in st_ld_l:
                return True



        if self.cmd_type not in known_type:
            print(f'UNKNOWN EXEC TYPE:\n{self}\n {unit_type}')
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
        self.log.append({'cycle':get_cycle(),'event':'back_to_thread'})
        if self.is_done():
            self.thread.done_cmds.append(self)
        elif self.is_missed():
            self.thread.cmds = [self] + self.thread.cmds
    
    def set_missed_mem(self,miss_penalty):
        self.log.append({'cycle':get_cycle(),'event':'missed_mem'})
        self.state = 'missed_mem'
        self.penalty_finish = get_cycle() + miss_penalty
        self.thread.penalty_finish = self.penalty_finish
        self.thread.state = 'missed_mem_penalty'

    def set_missed_pred(self,miss_penalty):
        self.log.append({'cycle':get_cycle(),'event':'missed_pred'})
        self.state = 'missed_pred'
        self.penalty_finish = get_cycle() + miss_penalty
        self.thread.set_missed(self.penalty_finish)

    def set_done(self):
        self.log.append({'cycle':get_cycle(),'event':'done'})
        self.state = 'done'



