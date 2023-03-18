#!/usr/bin/env python3
import os

benchmark_names = ['bwave', 'deepsjeng', 'fotonik3d', 'gcc', 'mcf', 'perl', 'x264']
path_to_threads = './cfg/different_schedulers/threads'
for bench in benchmark_names:
    for n in [1, 5, 10, 15, 20, 25]:
        list_to_write = str([bench for i in range(n)])
        list_to_write = "[" + list_to_write[1:-1] + "]"
        file_name = f"{path_to_threads}/{bench}_{n}_threads.cfg"
        with open(file_name, "w") as f:
            f.write(list_to_write)

