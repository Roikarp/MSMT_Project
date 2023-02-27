#!/usr/bin/env python3
import sys
from command import command

def lines_to_cmd_l(lines,thread):
    #initiate reg owner for dependancy calculation
    special_reg_names = ['di','si','ip','sp','bp']
    abc_reg_names     = ['a','b','c','d']
    numeral_reg_names = [f'r{i}' for i in range(8,15)]
    reg_names = special_reg_names + abc_reg_names + numeral_reg_names
    
    regs_owner = {}
    for r in reg_names:
        regs_owner[r] = None

    def find_regs_in_str(s):
        is_only_reg = True
        for r in numeral_reg_names:
            for c in ['w','b','d','']:
                if s == r or (s[:-1] == r and s[-1] == c) :
                    return [r] , is_only_reg

        for r in abc_reg_names:
            if s in [f'r{r}x',f'e{r}x',f'{r}x',f'{r}l']:
                return [r] , is_only_reg

        for r in special_reg_names:
            if s in [f'r{r}',f'e{r}',r,f'{r}l']:
                return [r] , is_only_reg
        
        regs = []
        if '[' in s:
            is_only_reg = False
            s = s.split('[')[1].split(']')[0]

            for r in numeral_reg_names:
                if r in s :
                    regs.append(r)

            for r in abc_reg_names:
                for er in [f'r{r}x',f'e{r}x',f'{r}x',f'{r}l']:
                    if er in s:
                        regs.append(r)

            for r in special_reg_names:
                for er in [f'r{r}',f'e{r}',r,f'{r}l']:
                    if er in s:
                        regs.append(r)

        return regs , is_only_reg

    cmds = []
    for l in lines:
        cmd = command()
        cmd.state      = "Pending" #Pending/issue/execution/done
        cmd.thread     = thread
        cmd.log        = []

        cmd.org_cmd    = l.strip()
        cmd.org_adress = l.split(':')[0]

        cmd_right_part       = l.split(':')[1][1:]
        cmd_type  , cmd_args = cmd_right_part.split(' ',1)
        cmd.cmd_type         = cmd_type

        # all commands that are in the shape of : [cmd_type] [something], [something]
        if cmd_type in ['add', 'bt', 'sub', 'xor', 'pxor', 'or', 'and', 'cmp', 'test', 'mov', 'shl', 'shr', 'sar', 'lea']:
            sides        = cmd_args.split(',')
            left , right = sides[0].strip() , sides[1].strip()
            # if right side is something like 'rax' or 'r11d'
            regs , is_only_reg = find_regs_in_str(right)
            if is_only_reg and len(regs) == 1:
                cmd.dependency.add(regs_owner[regs[0]])
            else:
                # if right side is something like 'qword ptr [rsi+rax*8]'
                for r in regs:
                    cmd.dependency.add(regs_owner[r])

            # if left side is something like 'rax' or 'r11d'
            regs , is_only_reg = find_regs_in_str(left)
            if is_only_reg and len(regs) == 1:
                if cmd_type not in ['mov', 'lea']:
                    cmd.dependency.add(regs_owner[regs[0]])
                if cmd_type not in ['cmp', 'test', 'bt']:
                    regs_owner[regs[0]] = cmd
            else:
                # if left side is something like 'qword ptr [rsi+rax*8]'
                for r in regs:
                    cmd.dependency.add(regs_owner[r])
        elif cmd_type in ['call', 'rdtsc', 'jz', 'jb', 'jbe', 'jnb', 'jnz', 'jnbe', 'ret', 'syscall']:
            pass
        # commands that only have a single identifier after the cmd_type
        elif cmd_type in ['neg','pop','push','jmp']:
            regs , is_only_reg = find_regs_in_str(cmd_args)
            if is_only_reg and len(regs) == 1:
                if cmd_type not in ['pop']:
                    cmd.dependency.add(regs_owner[regs[0]])
                if cmd_type not in ['push', 'jmp']:
                    regs_owner[regs[0]] = cmd
            else:
                for r in regs:
                    cmd.dependency.add(regs_owner[r])
        else:
            print(f'NO SUCH COMMAND!: {cmd.org_cmd}')
        cmd.dependency -= {None}
        cmds.append(cmd)

    return cmds


class thread:
    def __init__(self,path):
        with open(path,'r') as f:
            lines = f.readlines()

        self.cmds = lines_to_cmd_l(lines, self)
        self.cmd_to_run = len(self.cmds)
        self.done_cmds = []
        self.state = None

    def is_done(self):
        if len(self.done_cmds) == self.cmd_to_run:
            return True
        return False

    def pop_by_type(self,inst_type,inst_window_size):
        cmd = self.get_by_type(inst_type,inst_window_size)
        if cmd:
            self.cmds.remove(cmd)
            return cmd
        return None

    def get_by_type(self, inst_type, inst_window_size):
        self._update_state()
        if self.state == "context_switch_delay":
            return None

        for i in range(inst_window_size):
            if self.cmds[i].is_ready() and self.cmds[i].is_type(inst_type):
                return cmds[i]
        return None

    def set_context_switch(self, penalty):
        global cycle
        self.state = "context_switch_delay"
        self.delay_finish = cycle + penalty

    def _update_state(self):
        if self.state == "context_switch_delay":
            global cycle
            if cycle > self.delay_finish:
                self.state = "running"

