#!/usr/bin/env python3

get_global_params_from_file('global_params.json')

inst_queues = []
for i in len(THREAD_NUM):
    inst_queues.append(get_cmd_fifo_from_file(threads['file_path']))

execution_macro = execution_macro()

for i in len(NUM_EXECUTION_UNIT):
    execution_macro.add(execution_unit())

cycle = 0
while set([q.is_done() for q in inst_queues]) != {True}:
    # run all parts for 1 cycle
    for p in parts:
        p.run_cycle()
    cycle+1

    # handle communication between parts
    if execution_macro.has_free_space():
        new_queue = scheduler.get_new_queue()
        execution_macro.add_queue(new_queue)

