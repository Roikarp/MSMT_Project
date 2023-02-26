#!/usr/bin/env python3

class command:
    def __init__(self,cmd_line=None):
        self.org_cmd    = ""
        self.thread     = None
        self.org_adress = ""
        self.state      = "" #Pending/issue/execution/done
        self.cmd_type   = ""
        self.dependency = []
        self.log        = []

    def is_done(self):
        return self.state==done

    def is_ready(self):
        for c in self.dependency:
            if not c.is_done():
                reurn False
        return True

    def add_to_thread(self):
        # if inst.is_done():
        #     inst.add_to_thread_done()
        # elif inst.missed():
        #     inst.add_to_thread_pending()
