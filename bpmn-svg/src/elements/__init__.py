default_theme = {
    'Bpmn': {
        'margin-spec': {
            'left': 2, 'top': 2, 'right': 2, 'bottom': 2
        },
        'text-rect': {
            'max-lines': 2,
            'pad-spec': {
                'left': 10, 'top': 10, 'right': 10, 'bottom': 10
            },
            'style': {
                'fill': '#F0F0F0', 'stroke-width': 2, 'stroke': '#A0A0A0'
            },
            'vertical-text': False,
            'text-style': {
                'text-anchor': 'middle', 'dominant-baseline': 'middle', 'font-family': 'arial', 'font-size': 24, 'font-weight': 'bold', 'fill': '#02066F', 'stroke': '#000000', 'stroke-width': 0
            }
        },
        'bpmn-rect': {
            'pad-spec': {
                'left': 3, 'top': 3, 'right': 3, 'bottom': 3
            },
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
        'gap-between-text-and-pool-group': 1,
        'text-rect': {
            'pad-spec': {
                'left': 5, 'top': 5, 'right': 5, 'bottom': 5
            },
            'style': {
                'fill': '#F0F0F0', 'stroke-width': 1, 'stroke': '#475F94'
            },
            'vertical-text': True,
            'max-lines': 3,
            'text-style': {
                'text-anchor': 'middle', 'dominant-baseline': 'middle', 'font-family': 'arial', 'font-size': 20, 'font-weight': 'bold', 'fill': '#02066F', 'stroke': '#000000', 'stroke-width': 0
            }
        },
        'lane-rect': {
            'pad-spec': {
                'left': 1, 'top': 1, 'right': 1, 'bottom': 1
            },
            'style': {
                'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#475F94'
            }
        },
    },
    'SwimPool': {
        'gap-between-text-and-block-group': 0,
        'text-rect': {
            'pad-spec': {
                'left': 2, 'top': 2, 'right': 2, 'bottom': 2
            },
            'style': {
                'fill': '#D0D0D0', 'stroke-width': 1, 'stroke': '#B8B8B8'
            },
            'vertical-text': True,
            'max-lines': 3,
            'text-style': {
                'text-anchor': 'middle', 'dominant-baseline': 'middle', 'font-family': 'arial', 'font-size': 14, 'font-weight': 'bold', 'fill': '#1F3B4D', 'stroke': '#000000', 'stroke-width': 0
            }
        },
        'pool-rect': {
            'default-width': 600,
            'pad-spec': {
                'left': 1, 'top': 1, 'right': 1, 'bottom': 1
            },
            'style': {
                'fill': '#FFFFFF', 'stroke-width': 1, 'stroke': '#475F94'
            }
        },
    },
    'BlockGroup': {
        'pad-spec': {
            'left': 10, 'top': 40, 'right': 10, 'bottom': 40
        },
        'style': {
            'fill': '#FFFFFF', 'stroke-width': 0, 'stroke': '#048243'
        },
        'dx-between-elements': 40
    },
    'EventStart': {
        'text-rect': {
            'min-width': 40, 'max-width': 120,
            'max-lines': 4,
            'rx': 0, 'ry': 0,
            'pad-spec': {
                'left': 2, 'top': 5, 'right': 2, 'bottom': 5
            },
            'style': {
                'fill': '#FFFFFF', 'stroke-width': 0, 'stroke': '#FF8080'
            },
            'vertical-text': False,
            'text-style': {
                'text-anchor': 'middle', 'dominant-baseline': 'middle', 'font-family': 'arial', 'font-size': 12, 'fill': '#202020', 'stroke': '#000000', 'stroke-width': 0
            }
        },
        'outer-circle': {
            'radius': 20,
            'style': {
                'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#808080'
            }
        }
    },
    'EventIntermediate': {
        'text-rect': {
            'min-width': 40, 'max-width': 120,
            'max-lines': 4,
            'rx': 0, 'ry': 0,
            'pad-spec': {
                'left': 2, 'top': 5, 'right': 2, 'bottom': 5
            },
            'style': {
                'fill': '#FFFFFF', 'stroke-width': 0, 'stroke': '#FF8080'
            },
            'vertical-text': False,
            'text-style': {
                'text-anchor': 'middle', 'dominant-baseline': 'middle', 'font-family': 'arial', 'font-size': 12, 'fill': '#202020', 'stroke': '#000000', 'stroke-width': 0
            }
        },
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
        'text-rect': {
            'min-width': 40, 'max-width': 120,
            'max-lines': 4,
            'rx': 0, 'ry': 0,
            'pad-spec': {
                'left': 2, 'top': 5, 'right': 2, 'bottom': 5
            },
            'style': {
                'fill': '#FFFFFF', 'stroke-width': 0, 'stroke': '#FF8080'
            },
            'vertical-text': False,
            'text-style': {
                'text-anchor': 'middle', 'dominant-baseline': 'middle', 'font-family': 'arial', 'font-size': 12, 'fill': '#202020', 'stroke': '#000000', 'stroke-width': 0
            }
        },
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
                'text-anchor': 'middle', 'dominant-baseline': 'middle', 'font-family': 'arial', 'font-size': 12, 'fill': '#202020', 'stroke': '#000000', 'stroke-width': 0
            }
        }
    },
    'ActivitySubprocess': {
        'text-rect': {
            'min-width': 80, 'max-width': 160,
            'max-lines': 4,
            'rx': 4, 'ry': 4,
            'pad-spec': {
                'left': 10, 'top': 10, 'right': 10, 'bottom': 20
            },
            'style': {
                'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#808080'
            },
            'vertical-text': False,
            'text-style': {
                'text-anchor': 'middle', 'dominant-baseline': 'middle', 'font-family': 'arial', 'font-size': 12, 'fill': '#202020', 'stroke': '#000000', 'stroke-width': 0
            }
        },
        'inner-rect': {
            'width': 10, 'height': 10,
            'rx': 0, 'ry': 0,
            'style': {
                'fill': '#FFFFFF', 'stroke-width': 1.5, 'stroke': '#808080'
            }
        }
    },
    'ActivityTransactionSubprocess': {
        'outer-rect': {
            'rx': 4, 'ry': 4,
            'pad-spec': {
                'left': 4, 'top': 4, 'right': 4, 'bottom': 4
            },
            'style': {
                'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#808080'
            },
        },
        'text-rect': {
            'min-width': 80, 'max-width': 160,
            'max-lines': 4,
            'rx': 4, 'ry': 4,
            'pad-spec': {
                'left': 10, 'top': 10, 'right': 10, 'bottom': 20
            },
            'style': {
                'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#808080'
            },
            'vertical-text': False,
            'text-style': {
                'text-anchor': 'middle', 'dominant-baseline': 'middle', 'font-family': 'arial', 'font-size': 12, 'fill': '#202020', 'stroke': '#000000', 'stroke-width': 0
            }
        },
        'inner-rect': {
            'width': 10, 'height': 10,
            'rx': 0, 'ry': 0,
            'style': {
                'fill': '#FFFFFF', 'stroke-width': 1.5, 'stroke': '#808080'
            }
        }
    },
    'ActivityEventSubprocess': {
        'text-rect': {
            'min-width': 80, 'max-width': 160,
            'max-lines': 4,
            'rx': 4, 'ry': 4,
            'pad-spec': {
                'left': 10, 'top': 10, 'right': 10, 'bottom': 20
            },
            'style': {
                'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#808080', 'stroke-dasharray': '2,2'
            },
            'vertical-text': False,
            'text-style': {
                'text-anchor': 'middle', 'dominant-baseline': 'middle', 'font-family': 'arial', 'font-size': 12, 'fill': '#202020', 'stroke': '#000000', 'stroke-width': 0
            }
        },
        'inner-rect': {
            'width': 10, 'height': 10,
            'rx': 0, 'ry': 0,
            'style': {
                'fill': '#FFFFFF', 'stroke-width': 1.5, 'stroke': '#808080'
            }
        }
    },
    'ActivityAdhocSubprocess': {
        'text-rect': {
            'min-width': 80, 'max-width': 160,
            'max-lines': 4,
            'rx': 4, 'ry': 4,
            'pad-spec': {
                'left': 10, 'top': 10, 'right': 10, 'bottom': 25
            },
            'style': {
                'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#808080'
            },
            'vertical-text': False,
            'text-style': {
                'text-anchor': 'middle', 'dominant-baseline': 'middle', 'font-family': 'arial', 'font-size': 12, 'fill': '#202020', 'stroke': '#000000', 'stroke-width': 0
            }
        },
        'inner-rect': {
            'width': 10, 'height': 10,
            'rx': 0, 'ry': 0,
            'style': {
                'fill': '#FFFFFF', 'stroke-width': 1.5, 'stroke': '#808080'
            }
        },
        'wave-rect': {
            'min-width': 20, 'max-width': 50,
            'max-lines': 1,
            'rx': 0, 'ry': 0,
            'pad-spec': {
                'left': 1, 'top': 1, 'right': 1, 'bottom': 1
            },
            'style': {
                'fill': '#FFFFFF', 'stroke-width': 0, 'stroke': '#808080'
            },
            'vertical-text': False,
            'text-style': {
                'text-anchor': 'middle', 'dominant-baseline': 'middle', 'font-family': 'times', 'font-size': 18, 'font-weight': 'bold', 'fill': '#202020', 'stroke': '#000000', 'stroke-width': 1
            }
        }
    },
    'ActivityCall': {
        'text-rect': {
            'min-width': 80, 'max-width': 160,
            'max-lines': 4,
            'rx': 5, 'ry': 5,
            'pad-spec': {
                'left': 10, 'top': 10, 'right': 10, 'bottom': 10
            },
            'style': {
                'fill': '#FFFFFF', 'stroke-width': 4, 'stroke': '#808080'
            },
            'vertical-text': False,
            'text-style': {
                'text-anchor': 'middle', 'dominant-baseline': 'middle', 'font-family': 'arial', 'font-size': 12, 'fill': '#202020', 'stroke': '#000000', 'stroke-width': 0
            }
        }
    },
    'GatewayInclusive': {
        'text-rect': {
            'min-width': 80, 'max-width': 120,
            'max-lines': 4,
            'rx': 5, 'ry': 5,
            'pad-spec': {
                'left': 5, 'top': 5, 'right': 5, 'bottom': 5
            },
            'style': {
                'fill': '#FFFFFF', 'stroke-width': 0, 'stroke': '#FF8080'
            },
            'vertical-text': False,
            'text-style': {
                'text-anchor': 'middle', 'dominant-baseline': 'middle', 'font-family': 'arial', 'font-size': 12, 'fill': '#202020', 'stroke': '#000000', 'stroke-width': 0
            }
        },
        'diamond': {
            'diagonal-x': 40, 'diagonal-y': 40,
            'style': {
                'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#808080'
            },
            'inner-shape-style': {
                'fill': '#FFFFFF', 'stroke-width': 3, 'stroke': '#808080'
            },
        }
    },
    'GatewayExclusive': {
        'text-rect': {
            'min-width': 80, 'max-width': 120,
            'max-lines': 4,
            'rx': 5, 'ry': 5,
            'pad-spec': {
                'left': 5, 'top': 5, 'right': 5, 'bottom': 5
            },
            'style': {
                'fill': '#FFFFFF', 'stroke-width': 0, 'stroke': '#FF8080'
            },
            'vertical-text': False,
            'text-style': {
                'text-anchor': 'middle', 'dominant-baseline': 'middle', 'font-family': 'arial', 'font-size': 12, 'fill': '#202020', 'stroke': '#000000', 'stroke-width': 0
            }
        },
        'diamond': {
            'diagonal-x': 40, 'diagonal-y': 40,
            'style': {
                'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#808080'
            },
            'inner-shape-style': {
                'fill': '#FFFFFF', 'stroke-width': 3, 'stroke': '#808080'
            },
        }
    },
    'GatewayParallel': {
        'text-rect': {
            'min-width': 80, 'max-width': 120,
            'max-lines': 4,
            'rx': 5, 'ry': 5,
            'pad-spec': {
                'left': 5, 'top': 5, 'right': 5, 'bottom': 5
            },
            'style': {
                'fill': '#FFFFFF', 'stroke-width': 0, 'stroke': '#FF8080'
            },
            'vertical-text': False,
            'text-style': {
                'text-anchor': 'middle', 'dominant-baseline': 'middle', 'font-family': 'arial', 'font-size': 12, 'fill': '#202020', 'stroke': '#000000', 'stroke-width': 0
            }
        },
        'diamond': {
            'diagonal-x': 40, 'diagonal-y': 40,
            'style': {
                'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#808080'
            },
            'inner-shape-style': {
                'fill': '#FFFFFF', 'stroke-width': 3, 'stroke': '#808080'
            },
        }
    }
}
