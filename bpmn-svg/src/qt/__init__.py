ICONS = {
    'bpmn': './resources/bpmn/bpmn.png',
    'lanes': './resources/bpmn/lanes.png',
    'lane': './resources/bpmn/lane.png',
    'pools': './resources/bpmn/pools.png',
    'pool': './resources/bpmn/pool.png',
    'edges': './resources/bpmn/edges.png',
    'edge': './resources/bpmn/edge.png',
    'nodes': './resources/bpmn/nodes.png',
    'node': './resources/bpmn/node.png',
}

NEW_BPMN_SCRIPT = '''graph bpmn_id {
    label = "BPMN Title"

    lane lane_a {
        label = "Lane A Label"
        pool pool_a1 {
            label = "Pool A1 Label"

            start       start1              [label="start";]
            task        task_a1_01          [label="Task A1-01";]

            start1      --> task_a1_01
        }
        pool pool_a2 {
            label = "Pool A2 Label"

            task        task_a2_01          [label="Task A2-01";]
        }
        pool pool_a3 {
            label = "Pool A3 Label"

            task        task_a3_01          [label="Task A3-01";]
            end         end1                [label="end";]

            task_a3_01  --> end1
        }

        task_a1_01      --> task_a2_01
        task_a2_01      --> task_a3_01
    }
}'''
