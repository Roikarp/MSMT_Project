#!/usr/bin/env python3

import random

class unit:
    def __init__(self):
        self.unit_type    = None
        self.latency      = 0
        self.cmd          = None
        self.cur_cycle    = 0

        self.miss_rate    = 0
        self.miss_penalty = 0
        self.missed       = False
        self.miss_cycle   = 0

    def run(self):
        self.cur_cycle += 1

    def add_inst(self,cmd):
        self.cmd       = cmd
        self.cur_cycle = 0
        self.missed    = random.random() < miss_rate

    def active(self):
        if not self.cmd:
            return False
        if self.missed and self.cur_cycle >= self.miss_cycle:
            self.cmd.set_missed(miss_penalty)
            return False
        if self.cur_cycle == self.latency:
            self.cmd.set_done()
            return False
        return True

    def pop_inst_output(self):
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
