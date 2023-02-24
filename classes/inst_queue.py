#!/usr/bin/env python3

class inst_queues:
    def __init__(self):
        self.cmds = []
        self.inst_window_size = 10

    def is_done(self):
        return False

    def pop(self):
        for i in range(self.inst_window_size):
            if self.cmds[i].is_ready():
                cmd = cmds[i]
                del cmds[i]
                return cmd
