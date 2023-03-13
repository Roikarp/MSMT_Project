#!/usr/bin/env python3
import os
import sys
from command import command
sys.path.insert(1, f'{os.getcwd()}/../')
from cmd_x86_dep_dict import cmd_x86

def lines_to_cmd_l(lines,thread):
    #initiate reg owner for dependancy calculation
    special_reg_names = ['di','si','ip','sp','bp']
    abc_reg_names     = ['a','b','c','d']
    numeral_reg_names = [f'r{i}' for i in range(8,15)]
    extended_reg_names = [f'xmm{i}' for i in range(8)]
    reg_names = special_reg_names + abc_reg_names + numeral_reg_names + extended_reg_names
    
    regs_owner = {}
    for r in reg_names:
        regs_owner[r] = None

    def find_regs_in_str(s):
        is_only_reg = True
        for r in numeral_reg_names:
            for c in ['w','b','d','']:
                if s == r or (s[:-1] == r and s[-1] == c) :
                    return [r] , is_only_reg

        for r in numeral_reg_names:
            if s == r:
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

            for r in numeral_reg_names:
                if r == s:
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
    cnt = 0
    a = set()
    for i,l in enumerate(lines):
        if l[0:10] == '[TRACE:0] ':
            continue
        if l[0:18] == 'Instruction count ':
            continue
        if i%50000 == 0:
            print(i)

        cmd = command()
        cmd.state      = "pending" #pending/issue/execution/done
        cmd.thread     = thread
        cmd.id         = i
        cmd.log        = []
        cmd.use_mem    = False

        cmd.org_cmd    = l.strip()
        cmd.org_adress = l.split(':')[0]
        cmd_right_part       = l.split(':',1)[1].strip()

        if cmd_right_part[0:7] == 'data16 ':
            cmd_right_part = cmd_right_part[7:]
        if cmd_right_part[0:4] == 'rep ': #### this is a problem! it changes depends on value of ECX
            cmd.dependency.add(regs_owner['c'])
            cmd_right_part = cmd_right_part[4:]
        if cmd_right_part[0:4] == 'bnd ':
            cmd_right_part = cmd_right_part[4:]
        if cmd_right_part[0:5] == 'lock ':
            cmd_right_part = cmd_right_part[5:]
        cmd_type  = cmd_right_part.split(' ',1)[0]
        cmd.cmd_type = cmd_type
        if ' ' in cmd_right_part:
            cmd_args = cmd_right_part.split(' ',1)[1].split(',')
        else:
            cmd_args = []

        if cmd_type not in cmd_x86:
            print(f'NO SUCH COMMAND!: {cmd.org_cmd}')
            cnt += 1
            if cnt > 30:
                sys.exit()
            continue
        # print(cmd)
        try:
            cur_cmd_data = cmd_x86[cmd_type][len(cmd_args)]
        except:
            print (l)

        if 'special_reg_dependancy' in cur_cmd_data:
            for r in cur_cmd_data['special_reg_dependancy']:
                cmd.dependency.add(regs_owner[r])

        #set dependancies
        for i ,arg in enumerate(cmd_args):
            regs , is_only_reg = find_regs_in_str(arg)
            if is_only_reg and len(regs) == 1:
                if cur_cmd_data[i]['only_reg']['dep']:
                    cmd.dependency.add(regs_owner[regs[0]])
            else:
                for r in regs:
                    cmd.use_mem = True
                    if cur_cmd_data[i]['reg_for_memory']['dep']:
                        cmd.dependency.add(regs_owner[r])

        #set ownership  
        for i ,arg in enumerate(cmd_args):
            if is_only_reg and len(regs) == 1:
                if cur_cmd_data[i]['only_reg']['change']:
                    regs_owner[regs[0]] = cmd
            else:
                for r in regs:
                    cmd.use_mem = True
                    if cur_cmd_data[i]['reg_for_memory']['change']:
                        regs_owner[r] = cmd

        if 'special_reg_change' in cur_cmd_data:
            for r in cur_cmd_data['special_reg_change']:
                regs_owner[r] = cmd


        cmd.dependency -= {None}
        cmds.append(cmd)
    return cmds

class thread:
    def __init__(self,path,i):
        with open(path,'r') as f:
            lines = f.readlines()
        print(path)

        self.thread_id      = i
        self.bench          = path.split('.')[-2].split('/')[-1]
        # Edit here for shorter lines
        self.cmds           = lines_to_cmd_l(lines[:100000], self)
        self.cmd_to_run     = len(self.cmds)
        self.done_cmds      = []
        self.state          = 'pending'
        self.delay_finish   = 0
        self.penalty_finish = 0
        self.log            = []
        self.sim            = None

    def is_done(self):
        self._update_state()
        if len(self.done_cmds) == self.cmd_to_run:
            return True
        return False
    
    def is_pending(self):
        self._update_state()
        return self.state == 'pending'
    
    def is_missed(self):
        self._update_state()
        return self.state in ['missed_mem_penalty','missed_pred_penalty','missed_penalty']

    def pop_by_type(self,inst_type,inst_window_size):
        self._update_state()
        cmd = self.get_by_type(inst_type,inst_window_size)
        if cmd:
            self.cmds.remove(cmd)
            return cmd
        return None

    def get_by_type(self, inst_type, inst_window_size):
        self._update_state()
        if self.state in ['missed_mem_penalty','missed_pred_penalty','context_switch_delay']:
            return None

        for i in range(min(inst_window_size,len(self.cmds))):
            if self.cmds[i].is_ready() and self.cmds[i].is_type(inst_type):
                return self.cmds[i]
        return None

    def set_context_switch(self, penalty):
        self.log.append({'cycle':self.get_cycle(),'event':'context_switch_delay'})
        self.state = "context_switch_delay"
        self.delay_finish = self.get_cycle() + penalty

    def _update_state(self):
        if self.state == "context_switch_delay":
            if self.get_cycle() > self.delay_finish:
                self.log.append({'cycle':self.get_cycle(),'event':'running'})
                self.state = "running"
        if self.state in ['missed_mem_penalty','missed_pred_penalty','missed_penalty']:
            if self.get_cycle() > self.penalty_finish:
                self.log.append({'cycle':self.get_cycle(),'event':'pending'})
                self.state = "pending"

    def get_inst_cnt(self):
        return self.cmd_to_run

    def set_missed(self,penalty_finish):
        self.log.append({'cycle':self.get_cycle(),'event':'missed_mem_penalty'})
        self.penalty_finish = penalty_finish
        self.state = 'missed_mem_penalty'

    def set_done(self):
        self.log.append({'cycle':self.get_cycle(),'event':'done'})
        self.state = 'done'

    def get_cpi(self):
        for l in self.log:
            if l['event'] in ['context_switch_delay']:
                start = l['cycle']
                break
        for l in reversed(self.log):
            if l['event'] in ['done']:
                end = l['cycle']
                break

        return (end-start)/self.cmd_to_run

    def get_cycle(self):
        return self.sim.cycle

    def sim_done(self):
        return self.sim.sim_done

    def get_hist(self):
        hist = {}
        for c in self.done_cmds:
            if c.unit_type in hist:
                hist[c.unit_type] += 1
            else:
                hist[c.unit_type] = 1
        hist = list(hist.items())
        hist.sort(reverse=True,key=lambda x: x[1])
        return hist

    def __str__(self):
        tot_cmds = len(self.done_cmds)
        s = ''
        s += f'thread #{self.thread_id}{(3-len(str(self.thread_id)))*" "}- '
        s += f'{self.bench}{(10-len(str(self.bench)))*" "}'
        if self.sim_done():
            s += f', {tot_cmds} commands, cpi {round(self.get_cpi(),3)}:\n'
            hist = self.get_hist()
            for i , (ut , cnt) in enumerate(hist):
                s += f'{i}: {ut} - {cnt} cmds ({(100*cnt)/tot_cmds}%)\n'
        else:
            s += f': cmd left: {len(self.cmds)} ,done: {tot_cmds} ({self.state})'
        return s

