#!/usr/bin/env python3
class scheduler:
    def __init__(self):
        self.threads = []
        self.policy  = ""
        self.name    = ""
        self.valid   = []

    def add_thread(self,threads):
        for t in threads:
            self.threads.append(t)

    def pop_thread(self):
        chosen_t = self.choose_thread()
        if chosen_t:
            self.threads.remove(chosen_t)
        return chosen_t

    def choose_thread(self,inst_type=None):
        if self.name == "inner":
            self.valid = [t.get_by_type(inst_type) is not None for t in self.threads]
        if self.name == "outer":
            self.valid = [not t.is_stuck() for t in self.threads]\

        return self.choose_thread_core()

    def choose_thread_core(self):
        for v,t in zip(self.valid,self.threads):
            if v:
                return t
        return None