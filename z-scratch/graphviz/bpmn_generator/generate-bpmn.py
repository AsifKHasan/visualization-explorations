#!/usr/bin/env python3
'''
usage:
python generate-bpmn.py
'''

import bpmn_python.bpmn_diagram_rep as diagram

bpmn_graph = diagram.BpmnDiagramGraph()
bpmn_graph.create_new_diagram_graph(diagram_name="diagram1")
process_id = bpmn_graph.add_process_to_diagram()
[start_id, _] = bpmn_graph.add_start_event_to_diagram(process_id, start_event_name="start_event")
[task1_id, _] = bpmn_graph.add_task_to_diagram(process_id, task_name="task1")
bpmn_graph.add_sequence_flow_to_diagram(process_id, start_id, task1_id, "start_to_one")

[exclusive_gate_fork_id, _] = bpmn_graph.add_exclusive_gateway_to_diagram(process_id,
                                                                          gateway_name="exclusive_gate_fork")
[task1_ex_id, _] = bpmn_graph.add_task_to_diagram(process_id, task_name="task1_ex")
[task2_ex_id, _] = bpmn_graph.add_task_to_diagram(process_id, task_name="task2_ex")
[exclusive_gate_join_id, _] = bpmn_graph.add_exclusive_gateway_to_diagram(process_id,
                                                                          gateway_name="exclusive_gate_join")

bpmn_graph.add_sequence_flow_to_diagram(process_id, task1_id, exclusive_gate_fork_id, "one_to_ex_fork")
bpmn_graph.add_sequence_flow_to_diagram(process_id, exclusive_gate_fork_id, task1_ex_id, "ex_fork_to_ex_one")
bpmn_graph.add_sequence_flow_to_diagram(process_id, exclusive_gate_fork_id, task2_ex_id, "ex_fork_to_ex_two")
bpmn_graph.add_sequence_flow_to_diagram(process_id, task1_ex_id, exclusive_gate_join_id, "ex_one_to_ex_join")
bpmn_graph.add_sequence_flow_to_diagram(process_id, task2_ex_id, exclusive_gate_join_id, "ex_two_to_ex_join")

[task2_id, _] = bpmn_graph.add_task_to_diagram(process_id, task_name="task2")
[end_id, _] = bpmn_graph.add_end_event_to_diagram(process_id, end_event_name="end_event")
bpmn_graph.add_sequence_flow_to_diagram(process_id, exclusive_gate_join_id, task2_id, "ex_join_to_two")
bpmn_graph.add_sequence_flow_to_diagram(process_id, task2_id, end_id, "two_to_end")

bpmn_graph.export_xml_file('./', 'bpmn.xml')
