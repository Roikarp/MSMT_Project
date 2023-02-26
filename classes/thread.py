#!/usr/bin/env python3

class thread:
    def __init__(self,path):
        #initiate reg owner for dependancy calculation
        regs_owner = {}
        for r in ['rdi','rax','rcx','rsi','cl']:
            regs_owner[r] = None
        for i in range(8,15):
            regs_owner[f'r{i}'] = None
        reg_names = list(regs_owner.keys())

        self.cmds       = []
        with open(path,'r') as f:
            for l in f:
                cmd = command()
                cmd.state      = "Pending" #Pending/issue/execution/done
                cmd.thread     = self
                cmd.log        = []

                cmd.org_cmd    = l
                cmd.org_adress = l.split(':')[0]

                cmd_right_part       = l.split(':')[1][1:]
                cmd_type  , cmd_args = cmd_right_part.split(' ',1)
                cmd.cmd_type         = cmd_type
                
                sides        = cmd_args.split(',')
                left , right = sides[0].strip() , sides[1].strip()

                if cmd_type in ['add','sub','xor','or','cmp','test','mov','shl','sar','lea']:
                    # if right side is something like 'rax' or 'r11d'
                    if right in reg_names or (right[:-1] in reg_names and right[-1]=='d'):
                        cmd.dependency.append(regs_owner[right])
                    else:
                        # if right side is something 'qword ptr [rsi+rax*8]'
                        for r in reg_names:
                            if r in right:
                                cmd.dependency.append(regs_owner[right])

                    # if left side is something like 'rax' or 'r11d'
                    if left in reg_names or (left[:-1] in reg_names and left[-1]=='d'):
                        if cmd_type not in ['mov','lea']:
                            cmd.dependency.append(regs_owner[left])
                        if cmd_type not in ['cmp','test']:
                            regs_owner[target] = cmd
                    else:
                        # if left side is something 'qword ptr [rsi+rax*8]'
                        for r in reg_names:
                            if r in left:
                                cmd.dependency.append(regs_owner[left])
                elif cmd_type in ['call','rdtsc','jz','jbe','jnz']:
                    pass
                elif cmd_type in ['push','jmp']:
                    if left in reg_names:
                        cmd.dependency.append(regs_owner[left])
                    else:
                        if cmd_type not in ['jmp']
                            print(f'ERROR!: {cmd.org_cmd}')
                else:
                    print(f'NO SUCH COMMAND!: {cmd.org_cmd}')
                self.cmds.append(cmd)



        self.done_cmds = []
        self.inst_window_size = 10
        self.state = None

    def is_done(self):
        return False

    def pop_by_type(self,inst_type):
        cmd = self.get_by_type(inst_type)
        if cmd:
            self.cmds.remove(cmd)
            return cmd
        return None

    def get_by_type(self,inst_type):
        self._update_state()
        if self.state == "context_switch_delay":
            return None

        for i in range(self.inst_window_size):
            if self.cmds[i].is_ready() and self.cmds[i].is_type(inst_type):
                return cmds[i]
        return None

    def set_context_switch(self,penalty):
        global cycle
        self.state = "context_switch_delay"
        self.delay_finish = cycle + penalty

    def _update_state(self):
        if self.state == "context_switch_delay":
            global cycle
            if cycle > self.delay_finish:
                self.state = "running"

