#!/usr/bin/env python3

class command:
    def __init__(self,cmd_line=None):
        if not cmd_line:
            self.org_cmd    = None
            self.thread     = None
            self.org_adress = None
            self.state      = None #Pending/issue/execution/done
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
