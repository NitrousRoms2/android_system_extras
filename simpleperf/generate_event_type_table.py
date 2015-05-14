#!/usr/bin/python
#
# Copyright (C) 2015 The Android Open Source Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


def gen_event_type_entry_str(event_type_name, event_type, event_config):
    """
    return string like:
    {"cpu-cycles", PERF_TYPE_HARDWARE, PERF_COUNT_HW_CPU_CYCLES},
    """
    return '{"%s", %s, %s},\n' % (event_type_name, event_type, event_config)


def gen_hardware_events():
    hardware_configs = ["cpu-cycles",
                        "instructions",
                        "cache-references",
                        "cache-misses",
                        "branch-instructions",
                        "branch-misses",
                        "bus-cycles",
                        "stalled-cycles-frontend",
                        "stalled-cycles-backend",
                        ]
    generated_str = ""
    for config in hardware_configs:
        event_type_name = config
        event_config = "PERF_COUNT_HW_" + config.replace('-', '_').upper()

        generated_str += gen_event_type_entry_str(
            event_type_name, "PERF_TYPE_HARDWARE", event_config)

    return generated_str


def gen_software_events():
    software_configs = ["cpu-clock",
                        "task-clock",
                        "page-faults",
                        "context-switches",
                        "cpu-migrations",
                        ["minor-faults", "PERF_COUNT_SW_PAGE_FAULTS_MIN"],
                        ["major-faults", "PERF_COUNT_SW_PAGE_FAULTS_MAJ"],
                        "alignment-faults",
                        "emulation-faults",
                        ]
    generated_str = ""
    for config in software_configs:
        if type(config) is list:
            event_type_name = config[0]
            event_config = config[1]
        else:
            event_type_name = config
            event_config = "PERF_COUNT_SW_" + config.replace('-', '_').upper()

        generated_str += gen_event_type_entry_str(
            event_type_name, "PERF_TYPE_SOFTWARE", event_config)

    return generated_str


def gen_hw_cache_events():
    hw_cache_types = [["L1-dcache", "PERF_COUNT_HW_CACHE_L1D"],
                      ["L1-icache", "PERF_COUNT_HW_CACHE_L1I"],
                      ["LLC", "PERF_COUNT_HW_CACHE_LL"],
                      ["dTLB", "PERF_COUNT_HW_CACHE_DTLB"],
                      ["iTLB", "PERF_COUNT_HW_CACHE_ITLB"],
                      ["branch", "PERF_COUNT_HW_CACHE_BPU"],
                      ["node", "PERF_COUNT_HW_CACHE_NODE"],
                      ]
    hw_cache_ops = [["loades", "load", "PERF_COUNT_HW_CACHE_OP_READ"],
                    ["stores", "store", "PERF_COUNT_HW_CACHE_OP_WRITE"],
                    ["prefetches", "prefetch",
                     "PERF_COUNT_HW_CACHE_OP_PREFETCH"],
                    ]
    hw_cache_op_results = [["accesses", "PERF_COUNT_HW_CACHE_RESULT_ACCESS"],
                           ["misses", "PERF_COUNT_HW_CACHE_RESULT_MISS"],
                           ]
    generated_str = ""
    for (type_name, type_config) in hw_cache_types:
        for (op_name_access, op_name_miss, op_config) in hw_cache_ops:
            for (result_name, result_config) in hw_cache_op_results:
                if result_name == "accesses":
                    event_type_name = type_name + '-' + op_name_access
                else:
                    event_type_name = type_name + '-' + \
                        op_name_miss + '-' + result_name
                event_config = "((%s) | (%s << 8) | (%s << 16))" % (
                    type_config, op_config, result_config)
                generated_str += gen_event_type_entry_str(
                    event_type_name, "PERF_TYPE_HW_CACHE", event_config)

    return generated_str


def gen_events():
    generated_str = "// This file is auto-generated by generate-event_table.py.\n\n"
    generated_str += gen_hardware_events() + '\n'
    generated_str += gen_software_events() + '\n'
    generated_str += gen_hw_cache_events() + '\n'
    return generated_str

generated_str = gen_events()
fh = open('event_type_table.h', 'w')
fh.write(generated_str)
fh.close()