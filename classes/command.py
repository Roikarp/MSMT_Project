#!/usr/bin/env python3

class command:
    def __init__(self,cmd_line=None):
        self.org_cmd    = ""
        self.thread     = None
        self.org_adress = ""
        self.state      = "" #Pending/issue/execution/done
        self.cmd_type   = ""
        self.dependency = set()
        self.log        = []

    def is_done(self):
        return self.state == done

    def is_ready(self):
        for c in self.dependency:
            if not c.is_done():
                return False
        return True

    def is_type(self, unit_type):
        if unit_type == 'alu':
            # return self.cmd_type in ['add', 'sub', 'imul', 'xor', 'and', 'or', 'shl', 'shr', 'sar', 'mov', 'cmp', 'test']
            return True
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

    # def add_to_thread(self):
        # if inst.is_done():
        #     inst.add_to_thread_done()
        # elif inst.missed():
        #     inst.add_to_thread_pending()
