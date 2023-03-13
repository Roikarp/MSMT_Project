#!/usr/bin/env python3
import copy

class Scheduler:
    def __init__(self, name, threads):
        self.threads = copy.copy(threads)
        self.policy  = ""
        self.name    = name
        self.valid   = []
        self.sim     = None

    def add_thread(self, threads):
        if type(threads) == list:
            for t in threads:
                self.threads.append(t)
        else:
            self.threads.append(threads)

    def pop_thread(self):
        chosen_t = self.choose_thread()
        if chosen_t:
            self.remove_thread(chosen_t)
        return chosen_t

    def choose_thread(self, inst_type=None, inst_window_size=None):
        if self.name == "inner":
            self.valid = [t.get_by_type(inst_type, inst_window_size) is not None for t in self.threads]
        if self.name == "outer":
            self.valid = [t.is_pending() for t in self.threads]
        return self.choose_thread_core()

    def choose_thread_core(self):
        for v, t in zip(self.valid,self.threads):
            if v:
                return t
        return None

    def remove_thread(self, t):
        self.threads.remove(t)

    def get_cycle(self):
        return self.sim.cycle


class RoundRobinScheduler(Scheduler):
    def __init__(self, name, threads):
        super().__init__(name, threads)
        self.policy = "Round Robin"

    def choose_thread_core(self):
        for v, t in zip(self.valid,self.threads):
            if v:
                # Choose the first valid thread and insert to the end of the list
                self.remove_thread(t)
                self.add_thread(t)
                return t
        return None


class FaintScheduler(Scheduler):
    def __init__(self, name, threads):
        super().__init__(name, threads)
        self.threads = [{'thread': t, 'accesses': 0} for t in self.threads]
        self.policy = "LRU"

    def add_thread(self, threads):
        if type(threads) is not list:
            threads = [threads]
        threads = [{'thread': t, 'accesses': t.accesses} for t in threads]
        super().add_thread(threads)

    def touch_thread(self, t):
        for t_dict in self.threads:
            if t == t_dict['thread']:
                t_dict['accesses'] += 1
                return
        print("The requested thread does not exist in Faint scheduler")

    def choose_thread(self, inst_type=None, inst_window_size=None):
        threads_only_list = [element['thread'] for element in self.threads]
        if self.name == "inner":
            self.valid = [t.get_by_type(inst_type, inst_window_size) is not None for t in threads_only_list]
        if self.name == "outer":
            self.valid = [t.is_pending() for t in threads_only_list]
        return self.choose_thread_core()

    def choose_thread_core(self):
        zipped_info = zip(self.valid, self.threads)
        zipped_info_sorted = sorted(zipped_info, key=lambda x: x[1]['accesses'])
        for v, t in zipped_info_sorted:
            if v:
                self.touch_thread(t['thread'])
                return t['thread']
        return None

    def remove_thread(self, t):
        for dict_elem in self.threads:
            if t == dict_elem['thread']:
                self.threads.remove(dict_elem)
                return
        print("The given thread does not exist in scheduler")


class LRUScheduler(Scheduler):
    def __init__(self, name, threads):
        super().__init__(name, threads)
        self.threads = [{'thread': t, 'last_use_cycle': t.last_use} for t in self.threads]
        self.policy = "LRU"

    def add_thread(self, threads):
        if type(threads) is not list:
            threads = [threads]
        threads = [{'thread': t, 'last_use_cycle': t.last_use} for t in threads]
        super().add_thread(threads)

    def touch_thread(self, t):
        for t_dict in self.threads:
            if t == t_dict['thread']:
                t_dict['accesses'] = self.get_cycle()
                return
        print("The requested thread does not exist in LRUScheduler")

    def choose_thread(self, inst_type=None, inst_window_size=None):
        threads_only_list = [element['thread'] for element in self.threads]
        if self.name == "inner":
            self.valid = [t.get_by_type(inst_type, inst_window_size) is not None for t in threads_only_list]
        if self.name == "outer":
            self.valid = [t.is_pending() for t in threads_only_list]
        return self.choose_thread_core()

    def choose_thread_core(self):
        zipped_info = zip(self.valid, self.threads)
        zipped_info_sorted = sorted(zipped_info, key=lambda x: x[1]['last_use_cycle'])
        for v, t in zipped_info_sorted:
            if v:
                self.touch_thread(t['thread'])
                return t['thread']
        return None

    def remove_thread(self, t):
        for dict_elem in self.threads:
            if t == dict_elem['thread']:
                self.threads.remove(dict_elem)
                return
        print("The given thread does not exist in scheduler")




