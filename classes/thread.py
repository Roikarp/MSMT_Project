#!/usr/bin/env python3

class thread:
    def __init__(self):
        self.cmds      = []
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

