#!/usr/bin/env python3
'''
https://www.bpmnquickguide.com/view-bpmn-quick-guide/
cd C:\projects\asifhasan@github\visualization-explorations\bpmn-svg\src
python bpmn-parser.py < ../data/grp__hrm__award-and-publication.bpmn > ../data/grp__hrm__award-and-publication.json
'''
import sys
import os
import json
from re import MULTILINE
import pprint
from collections import namedtuple
from funcparserlib.util import pretty_tree
from funcparserlib.lexer import make_tokenizer, Token, LexerError
from funcparserlib.parser import (some, a, maybe, many, finished, skip, oneplus, forward_decl, NoParseError)

ENCODING = 'UTF-8'

Graph = namedtuple('Graph', 'type id stmts')
Lane = namedtuple('Lane', 'id stmts')
Pool = namedtuple('Pool', 'id stmts')
Node = namedtuple('Node', 'type id attrs')
Attr = namedtuple('Attr', 'name value')
Edge = namedtuple('Edge', 'node edges attrs')
DefAttrs = namedtuple('DefAttrs', 'object attrs')

def tokenize(str):
    # """str -> Sequence(Token)"""
    specs = [
        ('Comment', (r'/\*(.|[\r\n])*?\*/', MULTILINE)),
        ('Comment', (r'//.*',)),
        ('Comment', (r'#.*',)),
        ('NL', (r'[\r\n]+',)),
        ('Space', (r'[ \t\r\n]+',)),
        ('Name', (r'[A-Za-z\200-\377_][A-Za-z\200-\377_0-9]*',)),
        ('Op', (r'[{};,=\[\]]',)),
        ('Number', (r'-?(\.[0-9]+)|([0-9]+(\.[0-9]*)?)',)),
        ('String', (r'"[^"]*"',)), # '\"' escapes are ignored
        ('String', (r"'[^']*'",)), # "\'" escapes are ignored
        ('NodeType', (r'start',)),
        ('NodeType', (r'intermediate',)),
        ('NodeType', (r'end',)),
        ('NodeType', (r'task',)),
        ('NodeType', (r'process',)),
        ('NodeType', (r'inclusive',)),
        ('NodeType', (r'parallel',)),
        ('NodeType', (r'exclusive',)),
        ('EdgeOp', (r'---',)),
        ('EdgeOp', (r'-->',)),
        ('EdgeOp', (r'<--',)),
        ('EdgeOp', (r'<->',)),
        ('EdgeOp', (r'(...)',)),
        ('EdgeOp', (r'(..>)',)),
        ('EdgeOp', (r'(<..)',)),
        ('EdgeOp', (r'(<.>)',)),
    ]
    useless = ['Comment', 'NL', 'Space']
    t = make_tokenizer(specs)
    return [x for x in t(str) if x.type not in useless]

def parse(seq):
    """Sequence(Token) -> object"""
    unarg = lambda f: lambda args: f(*args)
    tokval = lambda x: x.value
    flatten = lambda list: sum(list, [])
    n = lambda s: a(Token('Name', s)) >> tokval
    op = lambda s: a(Token('Op', s)) >> tokval
    op_ = lambda s: skip(op(s))

    node_type = some(lambda t: t.value in ['start', 'intermediate', 'end', 'task', 'process', 'inclusive', 'exclusive', 'parallel']).named('type') >> tokval

    id_types = ['Name', 'Number', 'String']
    id = some(lambda t: t.type in id_types).named('id') >> tokval
    make_graph_attr = lambda args: DefAttrs('graph', [Attr(*args)])

    node_id = id

    a_list = (
        id +
        maybe(op_('=') + id) +
        skip(maybe(op(';')))
        >> unarg(Attr))

    attr_list = (
        many(op_('[') + many(a_list) + op_(']'))
        >> flatten)

    attr_stmt = (
        (n('_') | n('node') | n('edge')) +
        attr_list
        >> unarg(DefAttrs))

    graph_attr = id + op_('=') + id >> make_graph_attr
    node_stmt = node_type + node_id + attr_list >> unarg(Node)

    # We use a forward_decl becaue of circular definitions like (stmt_list -> stmt -> subgraph -> stmt_list)
    lane = forward_decl()
    pool = forward_decl()

    edge_type = some(lambda t: t.type == 'EdgeOp') >> tokval
    edge_rhs = (edge_type + node_id) >> (lambda t: [t[0], t[1]])
    edge_stmt = (
        node_id +
        oneplus(edge_rhs) +
        attr_list
        >> unarg(Edge))

    stmt = (
        attr_stmt
        | edge_stmt
        | lane
        | pool
        | graph_attr
        | node_stmt
    )

    stmt_list = many(stmt + skip(maybe(op(';'))))

    pool.define(
        skip(n('pool')) +
        maybe(id) +
        op_('{') +
        stmt_list +
        op_('}')
        >> unarg(Pool))

    lane.define(
        skip(n('lane')) +
        maybe(id) +
        op_('{') +
        stmt_list +
        op_('}')
        >> unarg(Lane))

    graph = (
        maybe(n('graph')) +
        maybe(id) +
        op_('{') +
        stmt_list +
        op_('}')
        >> unarg(Graph))

    dotfile = graph + skip(finished)

    return dotfile.parse(seq)

def pretty_parse_tree(x):
    """object -> str"""
    Pair = namedtuple('Pair', 'first second')
    p = lambda x, y: Pair(x, y)

    def kids(x):
        """object -> list(object)"""
        # if isinstance(x, (Graph, SubGraph)):
        if isinstance(x, (Graph, Lane)):
            return [p('stmts', x.stmts)]
        elif isinstance(x, (Graph, Pool)):
            return [p('stmts', x.stmts)]
        elif isinstance(x, (Node, DefAttrs)):
            return [p('attrs', x.attrs)]
        elif isinstance(x, Edge):
            return [p('nodes', x.nodes), p('attrs', x.attrs)]
        elif isinstance(x, Pair):
            return x.second
        else:
            return []

    def show(x):
        """object -> str"""
        if isinstance(x, Pair):
            return x.first
        elif isinstance(x, Graph):
            return 'Graph [id=%s, type=%s]' % (
                x.id, x.type)
        # elif isinstance(x, SubGraph):
        #     return 'SubGraph [id=%s]' % (x.id,)
        elif isinstance(x, Lane):
            return 'Lane [id=%s]' % (x.id,)
        elif isinstance(x, Pool):
            return 'Pool [id=%s]' % (x.id,)
        elif isinstance(x, Edge):
            return 'Edge'
        elif isinstance(x, Attr):
            return 'Attr [name=%s, value=%s]' % (x.name, x.value)
        elif isinstance(x, DefAttrs):
            return 'DefAttrs [object=%s]' % (x.object,)
        elif isinstance(x, Node):
            return 'Node [id=%s]' % (x.id,)
        else:
            return x

    return pretty_tree(x, kids, show)

def process_defattrs(o, parent):
    if o.object == '_':
        for attr in o.attrs:
            parent['styles'][attr.name] = attr.value.strip("'").strip('"')
    elif o.object == 'graph':
        for attr in o.attrs:
            parent[attr.name] = attr.value.strip("'").strip('"')
    else:
        print('unknown object in DefAttrs: {0}. exiting ...'.format(o.object))
        sys.exit(1)

def process_edges(o, parent):
    styles = {}
    for attr in o.attrs:
        styles[attr.name] = attr.value.strip("'").strip('"')

    current_head = o.node
    for t in o.edges:
        parent.append({'head': current_head, 'tail': t[1], 'type': t[0], 'styles': styles})
        current_head = t[1]

def process_node(o, parent):
    node = {'type': o.type, 'label': {}, 'styles': {}}
    for attr in o.attrs:
        if attr.name == 'label':
            node[attr.name] = attr.value.strip("'").strip('"')
        else:
            node['styles'][attr.name] = attr.value.strip("'").strip('"')

    parent[o.id] = node

def process_pool(o, parent):
    parent[o.id] = {'styles': {}, 'label': {}, 'nodes': {}, 'edges': []}

    # statements are children
    for stmt in o.stmts:
        if isinstance(stmt, DefAttrs):
            process_defattrs(stmt, parent[o.id])
        elif isinstance(stmt, Lane):
            print('lanes can not be under a pool, must be inside a graph. exiting ...')
            sys.exit(1)
        elif isinstance(stmt, Pool):
            print('pools can not be under a pool, must be inside a lane. exiting ...')
            sys.exit(1)
        elif isinstance(stmt, Edge):
            process_edges(stmt, parent[o.id]['edges'] )
        elif isinstance(stmt, Attr):
            print('attrs can not be directly under a pool, must be inside a pool. exiting ...')
            sys.exit(1)
        elif isinstance(stmt, Node):
            process_node(stmt, parent[o.id]['nodes'] )
        else:
            print('unknown statement in pool: {0}. exiting ...'.format(type(stmt)))
            sys.exit(1)

def process_lane(o, parent):
    parent[o.id] = {'styles': {}, 'label': {}, 'pools': {}}

    # statements are children
    for stmt in o.stmts:
        if isinstance(stmt, DefAttrs):
            process_defattrs(stmt, parent[o.id])
        elif isinstance(stmt, Lane):
            print('lanes can not be under another lane, must be inside a graph. exiting ...')
            sys.exit(1)
        elif isinstance(stmt, Pool):
            process_pool(stmt, parent[o.id]['pools'])
        elif isinstance(stmt, Edge):
            print(type(stmt), dir(stmt))
            print()
        elif isinstance(stmt, Attr):
            print('attrs can not be directly under a lane, must be inside a pool. exiting ...')
            sys.exit(1)
        elif isinstance(stmt, Node):
            print('nodes can not be directly under a lane, must be inside a pool. exiting ...')
            sys.exit(1)
        else:
            print('unknown statement in lane: {0}. exiting ...'.format(type(stmt)))
            sys.exit(1)

def to_json(x):
    if not isinstance(x, Graph):
        print('the parsed tree does not represent a Graph. exiting ...')
        sys.exit(1)

    # root of the graph
    json_data = {x.id: {'styles': {}, 'label': {}, 'lanes': {}}}

    # statements are children
    for stmt in x.stmts:
        if isinstance(stmt, DefAttrs):
            process_defattrs(stmt, json_data[x.id])
        elif isinstance(stmt, Lane):
            process_lane(stmt, json_data[x.id]['lanes'])
        elif isinstance(stmt, Pool):
            print('pools can not be directly under a graph, must be inside a lane. exiting ...')
            sys.exit(1)
        elif isinstance(stmt, Edge):
            print(type(stmt), dir(stmt))
            print()
        elif isinstance(stmt, Attr):
            print('attrs can not be directly under a graph, must be inside a pool. exiting ...')
            sys.exit(1)
        elif isinstance(stmt, Node):
            print('nodes can not be directly under a graph, must be inside a pool. exiting ...')
            sys.exit(1)
        else:
            print('unknown statement in graph: {0}. exiting ...'.format(type(stmt)))
            sys.exit(1)

    return json_data

def write_json(json_data):
    sys.stdout.write(json.dumps(json_data, sort_keys=False, indent=4))

def main():
    try:
        stdin = os.fdopen(sys.stdin.fileno(), 'rb')
        input = stdin.read().decode(ENCODING)
        tree = parse(tokenize(input))
        # print(pretty_parse_tree(tree))
        write_json(to_json(tree))
    except (NoParseError, LexerError) as e:
        msg = ('syntax error: {0}'.format(e))
        print(msg)
        sys.exit(1)

if __name__ == '__main__':
    main()
