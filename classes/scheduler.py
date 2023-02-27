#!/usr/bin/env python3
import copy

class scheduler:
    def __init__(self, name, threads):
        self.threads = copy.copy(threads)
        self.policy  = ""
        self.name    = name
        self.valid   = []

    def add_thread(self,threads):
        if type(threads) == list:
            for t in threads:
                self.threads.append(t)
        else:
            self.threads.append(threads)

    def pop_thread(self):
        chosen_t = self.choose_thread()
        if chosen_t:
            self.threads.remove(chosen_t)
        return chosen_t

    def choose_thread(self,inst_type=None,inst_window_size=None):
        if self.name == "inner":
            self.valid = [t.get_by_type(inst_type,inst_window_size) is not None for t in self.threads]
        if self.name == "outer":
            self.valid = [t.is_pending() for t in self.threads]
        return self.choose_thread_core()

    def choose_thread_core(self):
        for v,t in zip(self.valid,self.threads):
            if v:
                return t
        return None

    def remove_thread(self,t):
        self.threads.remove(t)