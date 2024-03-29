#!/usr/bin/env python3

import random

class unit:
    def __init__(self,cfg_dct,sim):
        self.unit_type     = cfg_dct['unit_type']
        self.latency       = cfg_dct['latency']
        self.cmd           = None
        self.cur_cycle     = 0
        self.active_cycles = 0 #total active cycles
        self.sim           = sim

        #mem miss data
        self.miss_mem_rate    = cfg_dct.get('miss_mem_rate',self.sim.get_mem_miss_rate())
        self.miss_mem_penalty = cfg_dct.get('miss_mem_penalty',0)
        self.miss_mem_cycle   = cfg_dct.get('miss_mem_cycle',0)
        self.missed_mem       = False
        
        #br miss data
        self.miss_pred_rate    = cfg_dct.get('miss_pred_rate',0)
        self.miss_pred_penalty = cfg_dct.get('miss_pred_penalty',0)
        self.miss_pred_cycle   = cfg_dct.get('miss_pred_cycle',0)
        self.missed_pred       = False


    def run(self):
        self.cur_cycle += 1
        self.active_cycles += 1

    def add_inst(self,cmd):
        self.cmd         = cmd
        self.cur_cycle   = 0
        prob_comparison_val = 1 if cmd.already_missed else random.random()
        self.missed_mem  = prob_comparison_val < self.miss_mem_rate 
        self.missed_pred = prob_comparison_val < self.miss_pred_rate 


    def is_active(self):
        if not self.cmd:
            return False
        if self.missed_mem and self.cur_cycle >= self.miss_mem_cycle:
            return False

        if self.missed_pred and self.cur_cycle >= self.miss_pred_cycle:
            return False

        if self.cur_cycle == self.latency:
            return False

        return True

    def pop_inst_output(self):
        if not self.cmd:
            return None

        if self.missed_mem and self.cur_cycle >= self.miss_mem_cycle:
            self.cmd.set_missed_mem(self.miss_mem_penalty)

        if self.missed_pred and self.cur_cycle >= self.miss_pred_cycle:
            self.cmd.set_missed_pred(self.miss_pred_penalty)

        if self.cur_cycle == self.latency:
            self.cmd.set_done(self.unit_type)

        cmd = self.cmd
        self.cmd = None
        return cmd

    def free(self):
        return self.cmd is None

    def pop_by_type(self,inst_type):
        for i in range(self.inst_window_size):
            if self.cmds[i].is_ready() and self.cmds[i].is_type(inst_type):
                cmd = cmds[i]
                del cmds[i]
                return cmd
        return None

    def __str__(self):
        s = ''
        s += f'== {self.unit_type} Unit =={"="*(10-len(self.unit_type))} '
        if self.sim_done():
            s += f'\nUsage: {round((100*self.active_cycles) / self.get_cycle(),3)}%'
        else:
            s += f'Current Command: {self.cmd}'
        return s

    def sim_done(self):
        return self.sim.sim_done

    def get_cycle(self):
        return self.sim.cycle

