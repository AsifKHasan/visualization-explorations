default_theme = {
    'Bpmn': {
        'margin-left': 2, 'margin-top': 2, 'margin-right': 2, 'margin-bottom': 2,
        'pad-left': 4, 'pad-top': 4, 'pad-right': 4, 'pad-bottom': 4,
        'text-rect': {
            'default-height': 60,
            'style': {
                'fill': '#F0F0F0', 'stroke-width': 2, 'stroke': '#A0A0A0'
            },
            'vertical-text': False,
            'text-wrap-at': 50,
            'text-style': {
                'text-anchor': 'middle', 'dominant-baseline': 'middle', 'font-family': 'calibri', 'font-size': 24, 'fill': '#404040', 'stroke': '#000000', 'stroke-width': 0
            }
        },
        'bpmn-rect': {
            'style': {
                'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#A0A0A0'
            }
        },
    },
    'LaneGroup': {
        'gap-between-lanes': 0,
    },
    'PoolGroup': {
        'gap-between-pools': 0,
    },
    'SwimLane': {
        'text-rect': {
            'default-width': 60,
            'pad-left': 2, 'pad-top': 2, 'pad-right': 2, 'pad-bottom': 2,
            'style': {
                'fill': '#F0F0F0', 'stroke-width': 2, 'stroke': '#404040'
            },
            'vertical-text': True,
            'text-wrap-at': 20,
            'text-style': {
                'text-anchor': 'middle', 'dominant-baseline': 'middle', 'font-family': 'calibri', 'font-size': 20, 'fill': '#101010', 'stroke': '#000000', 'stroke-width': 0
            }
        },
        'lane-rect': {
            'pad-left': 1, 'pad-top': 1, 'pad-right': 1, 'pad-bottom': 1,
            'style': {
                'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#404040'
            }
        },
    },
    'SwimPool': {
        'text-rect': {
            'default-width': 50, 'default-height': 120,
            'style': {
                'fill': '#F8F8F8', 'stroke-width': 1, 'stroke': '#A0A0A0'
            },
            'vertical-text': True,
            'text-wrap-at': 15,
            'text-style': {
                'text-anchor': 'middle', 'dominant-baseline': 'middle', 'font-family': 'calibri', 'font-size': 14, 'fill': '#080808', 'stroke': '#000000', 'stroke-width': 0
            }
        },
        'pool-rect': {
            'default-width': 600, 'default-height': 120,
            'style': {
                'fill': '#FFFFFF', 'stroke-width': 1, 'stroke': '#A0A0A0'
            }
        },
    },
    'BlockGroup': {
        'pad-left': 10, 'pad-top': 5, 'pad-right': 10, 'pad-bottom': 5,
        'dx-between-elements': 30
    },
    'EventStart': {
        'outer-circle': {
            'radius': 20,
            'style': {
                'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#808080'
            }
        }
    },
    'EventIntermediate': {
        'outer-circle': {
            'radius': 20,
            'style': {
                'fill': '#FFFFFF', 'stroke-width': 1, 'stroke': '#808080'
            }
        },
        'inner-circle': {
            'radius': 15,
            'style': {
                'fill': '#FFFFFF', 'stroke-width': 1, 'stroke': '#808080'
            }
        }
    },
    'EventEnd': {
        'outer-circle': {
            'radius': 20,
            'style': {
                'fill': '#FFFFFF', 'stroke-width': 4, 'stroke': '#808080'
            }
        }
    },
    'ActivityTask': {
        'text-rect': {
            'min-width': 80, 'max-width': 160,
            'max-lines': 4,
            'rx': 5, 'ry': 5,
            'pad-left': 10, 'pad-top': 10, 'pad-right': 10, 'pad-bottom': 10,
            'style': {
                'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#808080'
            },
            'vertical-text': False,
            'text-style': {
                'text-anchor': 'middle', 'dominant-baseline': 'middle', 'font-family': 'calibri', 'font-size': 10, 'fill': '#202020', 'stroke': '#000000', 'stroke-width': 0
            }
        }
    }
}
