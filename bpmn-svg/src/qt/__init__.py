'''
inkscape -w 75 -h 25 flow-sequence.svg --export-filename flow-sequence.png
inkscape -w 75 -h 25 flow-message.svg --export-filename flow-message.png
inkscape -w 75 -h 25 flow-association.svg --export-filename flow-association.png
inkscape -w 75 -h 25 flow-directed.svg --export-filename flow-directed.png
inkscape -w 75 -h 25 flow-bidirectional.svg --export-filename flow-bidirectional.png
'''
EDGE_MAP = {
    '-->': './resources/bpmn/flow-sequence.png',
    '~~>': './resources/bpmn/flow-message.png',
    '...': './resources/bpmn/flow-association.png',
    '..>': './resources/bpmn/flow-directed.png',
    '<.>': './resources/bpmn/flow-bidirectional.png',
}

ACTION_ICONS = {
    'arrow-up': './resources/arrow-up.png',
    'arrow-down': './resources/arrow-down.png',
    'new-edge': './resources/new-edge.png',
    'remove-edge': './resources/remove-edge.png',
    'new-node': './resources/new-node.png',
    'remove-node': './resources/remove-node.png',
    'new-pool': './resources/new-pool.png',
    'remove-pool': './resources/remove-pool.png',
    'new-lane': './resources/new-lane.png',
    'remove-lane': './resources/remove-lane.png',
}

NODE_TYPES = {
    'Activities': {
        'Tasks': ['task', 'businessRuleTask', 'manualTask', 'receiveTask', 'scriptTask', 'sendTask', 'serviceTask', 'userTask',],
        'Calls': ['call', 'businessRuleCall', 'manualCall', 'scriptCall', 'userCall',],
        'Subprocesses': ['process', 'adhoc', 'transaction',],
        'Event Subprocesses': ['event', 'eventCompensation', 'eventConditional', 'eventConditionalNon', 'eventError', 'eventEscalation', 'eventEscalationNon', 'eventMessage', 'eventMessageNon', 'eventMultiple', 'eventMultipleNon', 'eventParallelMultiple', 'eventParallelMultipleNon', 'eventSignal', 'eventSignalNon', 'eventTimer', 'eventTimerNon',],
    },
    'Artifacts': ['group', 'annotation',],
    'Data': ['data', 'dataCollection', 'dataInput', 'dataInputCollection', 'dataOutput', 'dataOutputCollection', 'dataStore',],
    'Events': {
        'Start Events': ['start', 'startCompensation', 'startConditional', 'startConditionalNon', 'startError', 'startEscalation', 'startEscalationNon', 'startMessage', 'startMessageNon', 'startMultiple', 'startMultipleNon', 'startParallelMultiple', 'startParallelMultipleNon', 'startSignal', 'startSignalNon', 'startTimer', 'startTimerNon',],
        'Intermetiate Events': ['intermediate', 'catchCancel', 'catchCompensation', 'throwCompensation', 'catchError', 'catchEscalation', 'catchEscalationNon', 'throwEscalation', 'catchLink', 'throwLink', 'catchMessage', 'catchMessageNon', 'throwMessage', 'catchMultiple', 'catchMultipleNon', 'throwMultiple', 'catchParallelMultiple', 'catchParallelMultipleNon', 'catchSignal', 'catchSignalNon', 'throwSignal', 'conditional', 'conditionalNon', 'timer', 'timerNon',],
        'End Events': ['end', 'endCancel', 'endCompensation', 'endError', 'endEscalation', 'endMessage', 'endMultiple', 'endSignal', 'endTerminate',],
    },
    'Gateways': ['inclusive', 'exclusive', 'parallel', 'complex', 'eventBased', 'eventBasedStart', 'eventBasedParallelStart',],
}

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

    'task': './resources/bpmn/task.png',
    'businessRuleTask': './resources/bpmn/businessRuleTask.png',
    'manualTask': './resources/bpmn/manualTask.png',
    'receiveTask': './resources/bpmn/receiveTask.png',
    'scriptTask': './resources/bpmn/scriptTask.png',
    'sendTask': './resources/bpmn/sendTask.png',
    'serviceTask': './resources/bpmn/serviceTask.png',
    'userTask': './resources/bpmn/userTask.png',

    'call': './resources/bpmn/call.png',
    'businessRuleCall': './resources/bpmn/.png',
    'manualCall': './resources/bpmn/.png',
    'scriptCall': './resources/bpmn/.png',
    'userCall': './resources/bpmn/.png',

    'process': './resources/bpmn/process.png',
    'adhoc': './resources/bpmn/.png',
    'transaction': './resources/bpmn/.png',
    'event': './resources/bpmn/.png',

    'eventCompensation': './resources/bpmn/.png',
    'eventConditional': './resources/bpmn/.png',
    'eventConditionalNon': './resources/bpmn/.png',
    'eventError': './resources/bpmn/.png',
    'eventEscalation': './resources/bpmn/.png',
    'eventEscalationNon': './resources/bpmn/.png',
    'eventMessage': './resources/bpmn/.png',
    'eventMessageNon': './resources/bpmn/.png',
    'eventMultiple': './resources/bpmn/.png',
    'eventMultipleNon': './resources/bpmn/.png',
    'eventParallelMultiple': './resources/bpmn/.png',
    'eventParallelMultipleNon': './resources/bpmn/.png',
    'eventSignal': './resources/bpmn/.png',
    'eventSignalNon': './resources/bpmn/.png',
    'eventTimer': './resources/bpmn/.png',
    'eventTimerNon': './resources/bpmn/.png',

    'group': './resources/bpmn/.png',
    'annotation': './resources/bpmn/.png',

    'data': './resources/bpmn/data.png',
    'dataCollection': './resources/bpmn/.png',
    'dataInput': './resources/bpmn/dataInput.png',
    'dataInputCollection': './resources/bpmn/dataInputCollection.png',
    'dataOutput': './resources/bpmn/dataOutput.png',
    'dataOutputCollection': './resources/bpmn/dataOutputCollection.png',
    'dataStore': './resources/bpmn/dataStore.png',

    'start': './resources/bpmn/start.png',
    'startCompensation': './resources/bpmn/startCompensation.png',
    'startConditional': './resources/bpmn/startConditional.png',
    'startConditionalNon': './resources/bpmn/startConditionalNon.png',
    'startError': './resources/bpmn/startError.png',
    'startEscalation': './resources/bpmn/startEscalation.png',
    'startEscalationNon': './resources/bpmn/startEscalationNon.png',
    'startMessage': './resources/bpmn/startMessage.png',
    'startMessageNon': './resources/bpmn/startMessageNon.png',
    'startMultiple': './resources/bpmn/startMultiple.png',
    'startMultipleNon': './resources/bpmn/startMultipleNon.png',
    'startParallelMultiple': './resources/bpmn/startParallelMultiple.png',
    'startParallelMultipleNon': './resources/bpmn/startParallelMultipleNon.png',
    'startSignal': './resources/bpmn/startSignal.png',
    'startSignalNon': './resources/bpmn/startSignalNon.png',
    'startTimer': './resources/bpmn/startTimer.png',
    'startTimerNon': './resources/bpmn/startTimerNon.png',

    'end': './resources/bpmn/end.png',
    'endCancel': './resources/bpmn/endCancel.png',
    'endCompensation': './resources/bpmn/endCompensation.png',
    'endError': './resources/bpmn/endError.png',
    'endEscalation': './resources/bpmn/endEscalation.png',
    'endMessage': './resources/bpmn/endMessage.png',
    'endMultiple': './resources/bpmn/endMultiple.png',
    'endSignal': './resources/bpmn/endSignal.png',
    'endTerminate': './resources/bpmn/endTerminate.png',

    'intermediate': './resources/bpmn/intermediate.png',
    'catchCancel': './resources/bpmn/catchCancel.png',
    'catchCompensation': './resources/bpmn/catchCompensation.png',
    'throwCompensation': './resources/bpmn/throwCompensation.png',
    'catchError': './resources/bpmn/catchError.png',
    'catchEscalation': './resources/bpmn/catchEscalation.png',
    'catchEscalationNon': './resources/bpmn/catchEscalationNon.png',
    'throwEscalation': './resources/bpmn/throwEscalation.png',
    'catchLink': './resources/bpmn/catchLink.png',
    'throwLink': './resources/bpmn/throwLink.png',
    'catchMessage': './resources/bpmn/catchMessage.png',
    'catchMessageNon': './resources/bpmn/catchMessageNon.png',
    'throwMessage': './resources/bpmn/throwMessage.png',
    'catchMultiple': './resources/bpmn/catchMultiple.png',
    'catchMultipleNon': './resources/bpmn/catchMultipleNon.png',
    'throwMultiple': './resources/bpmn/throwMultiple.png',
    'catchParallelMultiple': './resources/bpmn/catchParallelMultiple.png',
    'catchParallelMultipleNon': './resources/bpmn/catchParallelMultipleNon.png',
    'catchSignal': './resources/bpmn/catchSignal.png',
    'catchSignalNon': './resources/bpmn/catchSignalNon.png',
    'throwSignal': './resources/bpmn/throwSignal.png',
    'conditional': './resources/bpmn/conditional.png',
    'conditionalNon': './resources/bpmn/conditionalNon.png',
    'timer': './resources/bpmn/timer.png',
    'timerNon': './resources/bpmn/timerNon.png',

    'inclusive': './resources/bpmn/inclusive.png',
    'exclusive': './resources/bpmn/exclusive.png',
    'parallel': './resources/bpmn/parallel.png',
    'complex': './resources/bpmn/complex.png',
    'eventBased': './resources/bpmn/eventBased.png',
    'eventBasedStart': './resources/bpmn/eventBasedStart.png',
    'eventBasedParallelStart': './resources/bpmn/eventBasedParallelStart.png',

    '-->': './resources/bpmn/flow-sequence.png',
    '~~>': './resources/bpmn/flow-message.png',
    '...': './resources/bpmn/flow-association.png',
    '..>': './resources/bpmn/flow-directed.png',
    '<.>': './resources/bpmn/flow-bidirectional.png',
}

NEW_NODE = {
    "type": "task",
    "label": "",
    "styles": {}
}

NEW_EDGE = {
    'from': '__UNDEFINED__',
    'to': '__UNDEFINED__',
    'type': '-->',
    'label': '',
    'styles': {}
}

NEW_POOL = {
    "styles": {},
    "label": "",
    "nodes": {},
    "edges": []
}

NEW_LANE = {
    "styles": {},
    "label": "",
    "pools": {},
    "edges": []
}

NEW_BPMN_SCRIPT = '''graph bpmn_id {
}'''
