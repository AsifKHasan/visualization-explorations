default_theme = {
    'Bpmn': {
        'margin-spec': {
            'left': 2, 'top': 2, 'right': 2, 'bottom': 2
        },
        'pad-spec': {
            'left': 4, 'top': 4, 'right': 4, 'bottom': 4
        },
        'text-rect': {
            'max-lines': 2,
            'pad-spec': {
                'left': 10, 'top': 5, 'right': 10, 'bottom': 5
            },
            'style': {
                'fill': '#F0F0F0', 'stroke-width': 2, 'stroke': '#A0A0A0'
            },
            'vertical-text': False,
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
            'pad-spec': {
                'left': 2, 'top': 2, 'right': 2, 'bottom': 2
            },
            'style': {
                'fill': '#F0F0F0', 'stroke-width': 2, 'stroke': '#404040'
            },
            'vertical-text': True,
            'max-lines': 3,
            'text-style': {
                'text-anchor': 'middle', 'dominant-baseline': 'middle', 'font-family': 'calibri', 'font-size': 20, 'fill': '#101010', 'stroke': '#000000', 'stroke-width': 0
            }
        },
        'lane-rect': {
            'pad-spec': {
                'left': 1, 'top': 1, 'right': 1, 'bottom': 1
            },
            'style': {
                'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#404040'
            }
        },
    },
    'SwimPool': {
        'text-rect': {
            'pad-spec': {
                'left': 10, 'top': 5, 'right': 10, 'bottom': 5
            },
            'style': {
                'fill': '#F8F8F8', 'stroke-width': 1, 'stroke': '#A0A0A0'
            },
            'vertical-text': True,
            'max-lines': 3,
            'text-style': {
                'text-anchor': 'middle', 'dominant-baseline': 'middle', 'font-family': 'calibri', 'font-size': 14, 'fill': '#080808', 'stroke': '#000000', 'stroke-width': 0
            }
        },
        'pool-rect': {
            'default-width': 600,
            'style': {
                'fill': '#FFFFFF', 'stroke-width': 1, 'stroke': '#A0A0A0'
            }
        },
    },
    'BlockGroup': {
        'pad-spec': {
            'left': 10, 'top': 5, 'right': 10, 'bottom': 5
        },
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
            'pad-spec': {
                'left': 10, 'top': 10, 'right': 10, 'bottom': 10
            },
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
