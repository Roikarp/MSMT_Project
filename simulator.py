#!/usr/bin/env python3

get_global_params_from_file('global_params.json')

threads = []
for i in len(THREAD_NUM):
    cur_thread = get_cmd_fifo_from_file(threads_f['file_path'])
    threads.append(cur_thread)

execution_macro = execution_macro() #use global params to configure

# for i in len(NUM_EXECUTION_UNIT):
#     execution_macro.add(execution_unit())

cycle = 0
while set([t.is_done() for t in threads]) != {True}:
    # run all parts for 1 cycle
    cycle+1
    execution_macro.run()

    # handle communication between parts
    if execution_macro.has_stuck_threads():
        stuck_threads = execution_macro.pop_stuck_threads()
        scheduler.add_thread(stuck_threads)

    if execution_macro.has_free_space():
        new_thread = scheduler.pop_thread()
        execution_macro.add_thread(new_thread)

cpi_per_thread = []
total_inst = 0
for t in threads:
    inst_cnt = t.get_inst_cnt()
    cpi = cycle/inst_cnt
    cpi_per_thread.append(cpi)

