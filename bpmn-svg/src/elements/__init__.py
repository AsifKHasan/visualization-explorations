DEFAULT_THEME = {
    'bpmn': {
        # margin within the svg for the whole bpmn graph so that there are some blank area outside the graph
        'margin-spec': {
            'left': 2, 'top': 2, 'right': 2, 'bottom': 2
        },
        # the title rectangle on top
        'rectangle': {
            'pad-spec': {
                'left': 8, 'top': 8, 'right': 8, 'bottom': 8
            },
            'style': {
                'fill': '#F0F0F0', 'stroke-width': 2, 'stroke': '#A0A0A0'
            }
        },
        # the title text specs
        'text': {
            'vertical-text': False, 'max-lines': 2,
            'style': {
                'text-anchor': 'middle', 'dominant-baseline': 'middle', 'font-family': 'arial', 'font-size': 24, 'font-weight': 'bold', 'fill': '#02066F', 'stroke': '#000000', 'stroke-width': 0
            }
        },
        # the BPMN content rectangle below the title rectangle
        'bpmn-rect': {
            'pad-spec': {
                'left': 4, 'top': 4, 'right': 4, 'bottom': 4
            },
            'style': {
                'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#A0A0A0'
            }
        },
    },
    'swims': {
        'LaneCollection': {
            # min y gap between two adjacent lanes so that inter-lane edges between two adjacent lanes can be routed along this gap
            'dy-between-lanes': 24,
            # gaps to keep on sides for routing edges within lanes in this LaneCollection (which is actually the BPMN itself)
            'pad-spec': {
                'left': 24, 'top': 24, 'right': 24, 'bottom': 24
            },
            'style': {
                'fill': 'none', 'stroke-width': 0, 'stroke': '#FFB000'
            },
        },
        'SwimLane': {
            'rectangle': {
                'pad-spec': {
                    'left': 5, 'top': 5, 'right': 5, 'bottom': 5
                },
                'style': {
                    'fill': '#F0F0F0', 'stroke-width': 1, 'stroke': '#475F94'
                }
            },
            'text': {
                'vertical-text': True, 'max-lines': 3,
                'style': {
                    'text-anchor': 'middle', 'dominant-baseline': 'middle', 'font-family': 'arial', 'font-size': 20, 'font-weight': 'bold', 'fill': '#02066F', 'stroke': '#000000', 'stroke-width': 0
                }
            },
        },
        'PoolCollection': {
            # min y gap between two adjacent pools so that inter-pool edges between two adjacent pools can be routed along this gap
            'dy-between-pools': 24,
            # gaps to keep on sides for routing edges within pools in this PoolCollection (which is actually a Lane)
            'pad-spec': {
                'left': 24, 'top': 24, 'right': 24, 'bottom': 24
            },
            'style': {
                'fill': 'none', 'stroke-width': 0.25, 'stroke': '#FF8000'
            },
        },
        'SwimPool': {
            'rectangle': {
                'pad-spec': {
                    'left': 2, 'top': 2, 'right': 2, 'bottom': 2
                },
                'style': {
                    'fill': '#D0D0D0', 'stroke-width': 1, 'stroke': '#B8B8B8'
                }
            },
            'text': {
                'vertical-text': True, 'max-lines': 3,
                'style': {
                    'text-anchor': 'middle', 'dominant-baseline': 'middle', 'font-family': 'arial', 'font-size': 14, 'font-weight': 'bold', 'fill': '#1F3B4D', 'stroke': '#000000', 'stroke-width': 0
                }
            },
        },
        'ChannelCollection': {
            # min x gap between two adjacent nodes so that straight edges can be drawn there
            'dx-between-elements': 40,
            # min y gap between two adjacent channels so that inter-channel edges between two adjacent channels can be routed along this gap
            'dy-between-channels': 24,
            # min x gap between two side-by-side channels so that inter-channel edges between two adjacent channels can be routed along this gap
            'dx-between-channels': 24,
            # gaps to keep on sides for routing edges within channels in this ChannelCollection (which is actually the pool)
            'pad-spec': {
                'left': 24, 'top': 24, 'right': 24, 'bottom': 24
            },
            'style': {
                'fill': 'none', 'stroke-width': 0.25, 'stroke': '#0482FF'
            },
        },
        'SwimChannel': {
            # full channel area including the space for internal edge routing
            'channel-outer-rect': {
                # gaps to keep on sides for routing edges totally within this channel
                # normally we try to route internl edges over the top and left if required
                'pad-spec':{
                    'left': 24, 'top': 24, 'right': 24, 'bottom': 24
                },
                'style': {
                    'fill': 'none', 'stroke-width': 0, 'stroke': '#FF8243'
                },
            },
            # actual channel content area where the nodes are to be placed
            'channel-inner-rect': {
                # min x gap between two adjacent nodes so that straight edges can be drawn there
                'dx-between-elements': 40,
                'style': {
                    'fill': 'none', 'stroke-width': 0, 'stroke': '#008080'
                },
            },
        }
    },
    'events': {
        'Event': {
            'rectangle': {
                'min-width': 40, 'max-width': 120, 'rx': 0, 'ry': 0,
                'pad-spec': {
                    'left': 2, 'top': 2, 'right': 2, 'bottom': 2
                },
                'style': {
                    'fill': '#FFFFFF', 'stroke-width': 0, 'stroke': '#FF8080'
                }
            },
            'text': {
                'vertical-text': False, 'max-lines': 4,
                'style': {
                    'text-anchor': 'middle', 'dominant-baseline': 'middle', 'font-family': 'arial', 'font-size': 10, 'fill': '#202020', 'stroke': '#000000', 'stroke-width': 0
                }
            },
        },
        'ends': {
            'EventEnd': {
                'circle': {
                    'radius': 20,
                    'style': {
                        'fill': '#FFFFFF', 'stroke-width': 5, 'stroke': '#808080'
                    }
                },
                'inner-shape': {
                    'style': {
                        'fill': '#808080', 'stroke-width': 0, 'stroke': '#808080'
                    }
                }
            },
            'EventEndCancel':{
            },
            'EventEndCompensation':{
                'inner-shape': {
                    'style': {
                        'fill': '#808080', 'stroke-width': 1, 'stroke': '#808080'
                    }
                }
            },
            'EventEndError':{
            },
            'EventEndEscalation':{
            },
            'EventEndMessage':{
                'inner-shape': {
                    'style': {
                        'fill': '#808080', 'stroke-width': 2, 'stroke': '#FFFFFF'
                    }
                }
            },
            'EventEndMultiple':{
            },
            'EventEndSignal':{
            },
            'EventEndTerminate':{
            },
        },
        'intermediates': {
            'EventIntermediate': {
                'circle': {
                    'radius': 22,
                    'style': {
                        'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#808080'
                    }
                },
                'inner-circle': {
                    'radius': 18,
                    'style': {
                        'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#808080'
                    }
                },
                'inner-shape': {
                    'style': {
                        'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#808080'
                    }
                }
            },
            'EventIntermediateCatchCancel': {
            },
            'EventIntermediateCatchCompensation': {
            },
            'EventIntermediateThrowCompensation': {
                'inner-shape': {
                    'style': {
                        'fill': '#808080', 'stroke-width': 1, 'stroke': '#808080'
                    }
                }
            },
            'EventIntermediateCatchError': {
            },
            'EventIntermediateCatchEscalation': {
            },
            'EventIntermediateCatchEscalationNon': {
                'circle': {
                    'radius': 22,
                    'style': {
                        'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#808080', 'stroke-dasharray': '5,5'
                    }
                },
                'inner-circle': {
                    'radius': 18,
                    'style': {
                        'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#808080', 'stroke-dasharray': '5,5'
                    }
                }
            },
            'EventIntermediateThrowEscalation': {
                'inner-shape': {
                    'style': {
                        'fill': '#808080', 'stroke-width': 1, 'stroke': '#808080'
                    }
                }
            },
            'EventIntermediateCatchLink': {
            },
            'EventIntermediateThrowLink': {
                'inner-shape': {
                    'style': {
                        'fill': '#808080', 'stroke-width': 1, 'stroke': '#808080'
                    }
                }
            },
            'EventIntermediateCatchMessage': {
            },
            'EventIntermediateCatchMessageNon': {
                'circle': {
                    'radius': 22,
                    'style': {
                        'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#808080', 'stroke-dasharray': '5,5'
                    }
                },
                'inner-circle': {
                    'radius': 18,
                    'style': {
                        'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#808080', 'stroke-dasharray': '5,5'
                    }
                }
            },
            'EventIntermediateThrowMessage': {
                'inner-shape': {
                    'style': {
                        'fill': '#808080', 'stroke-width': 1.5, 'stroke': '#FFFFFF'
                    }
                }
            },
            'EventIntermediateCatchMultiple': {
            },
            'EventIntermediateCatchMultipleNon': {
                'circle': {
                    'radius': 22,
                    'style': {
                        'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#808080', 'stroke-dasharray': '5,5'
                    }
                },
                'inner-circle': {
                    'radius': 18,
                    'style': {
                        'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#808080', 'stroke-dasharray': '5,5'
                    }
                }
            },
            'EventIntermediateThrowMultiple': {
                'inner-shape': {
                    'style': {
                        'fill': '#808080', 'stroke-width': 1, 'stroke': '#808080'
                    }
                }
            },
            'EventIntermediateCatchParallelMultiple': {
            },
            'EventIntermediateCatchParallelMultipleNon': {
                'circle': {
                    'radius': 22,
                    'style': {
                        'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#808080', 'stroke-dasharray': '5,5'
                    }
                },
                'inner-circle': {
                    'radius': 18,
                    'style': {
                        'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#808080', 'stroke-dasharray': '5,5'
                    }
                }
            },
            'EventIntermediateCatchSignal': {
            },
            'EventIntermediateCatchSignalNon': {
                'circle': {
                    'radius': 22,
                    'style': {
                        'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#808080', 'stroke-dasharray': '5,5'
                    }
                },
                'inner-circle': {
                    'radius': 18,
                    'style': {
                        'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#808080', 'stroke-dasharray': '5,5'
                    }
                }
            },
            'EventIntermediateThrowSignal': {
                'inner-shape': {
                    'style': {
                        'fill': '#808080', 'stroke-width': 1, 'stroke': '#808080'
                    }
                }
            },
            'EventIntermediateConditional': {
            },
            'EventIntermediateConditionalNon': {
                'circle': {
                    'radius': 22,
                    'style': {
                        'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#808080', 'stroke-dasharray': '5,5'
                    }
                },
                'inner-circle': {
                    'radius': 18,
                    'style': {
                        'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#808080', 'stroke-dasharray': '5,5'
                    }
                }
            },
            'EventIntermediateTimer': {
            },
            'EventIntermediateTimerNon': {
                'circle': {
                    'radius': 22,
                    'style': {
                        'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#808080', 'stroke-dasharray': '5,5'
                    }
                },
                'inner-circle': {
                    'radius': 18,
                    'style': {
                        'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#808080', 'stroke-dasharray': '5,5'
                    }
                }
            },
        },
        'starts': {
            'EventStart': {
                'circle': {
                    'radius': 20,
                    'style': {
                        'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#808080'
                    }
                },
                'inner-shape': {
                    'style': {
                        'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#808080'
                    }
                }
            },
            'EventStartCompensation': {
            },
            'EventStartConditional': {
                'inner-shape': {
                    'rx': 2, 'ry': 2,
                    'style': {
                        'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#808080'
                    }
                }
            },
            'EventStartConditionalNon': {
                'circle': {
                    'radius': 20,
                    'style': {
                        'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#808080', 'stroke-dasharray': '5,5'
                    }
                },
                'inner-shape': {
                    'rx': 2, 'ry': 2,
                    'style': {
                        'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#808080'
                    }
                }
            },
            'EventStartError': {
            },
            'EventStartEscalation': {
            },
            'EventStartEscalationNon': {
                'circle': {
                    'radius': 20,
                    'style': {
                        'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#808080', 'stroke-dasharray': '5,5'
                    }
                }
            },
            'EventStartMessage': {
            },
            'EventStartMessageNon': {
                'circle': {
                    'radius': 20,
                    'style': {
                        'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#808080', 'stroke-dasharray': '5,5'
                    }
                }
            },
            'EventStartMultiple': {
            },
            'EventStartMultipleNon': {
                'circle': {
                    'radius': 20,
                    'style': {
                        'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#808080', 'stroke-dasharray': '5,5'
                    }
                }
            },
            'EventStartParallelMultiple': {
            },
            'EventStartParallelMultipleNon': {
                'circle': {
                    'radius': 20,
                    'style': {
                        'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#808080', 'stroke-dasharray': '5,5'
                    }
                }
            },
            'EventStartSignal': {
            },
            'EventStartSignalNon': {
                'circle': {
                    'radius': 20,
                    'style': {
                        'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#808080', 'stroke-dasharray': '5,5'
                    }
                }
            },
            'EventStartTimer': {
            },
            'EventStartTimerNon': {
                'circle': {
                    'radius': 20,
                    'style': {
                        'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#808080', 'stroke-dasharray': '5,5'
                    }
                }
            }
        }
    },
    'activities': {
        'Activity': {
            'rectangle': {
                'min-width': 80, 'max-width': 160,
                'rx': 5, 'ry': 5,
                'inner-shape-margin-spec': {
                    'left': 4, 'top': 4, 'right': 4, 'bottom': 4
                },
                'pad-spec': {
                    'left': 10, 'top': 10, 'right': 10, 'bottom': 10
                },
                'style': {
                    'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#808080'
                },
            },
            'text': {
                'vertical-text': False, 'max-lines': 4,
                'style': {
                    'text-anchor': 'middle', 'dominant-baseline': 'middle', 'font-family': 'arial', 'font-size': 12, 'fill': '#202020', 'stroke': '#000000', 'stroke-width': 0
                }
            },
            'bottom-center-inner-shape': {
                'style': {
                    'fill': '#808080', 'stroke-width': 1, 'stroke': '#808080'
                }
            },
            'bottom-center-inner-shape': {
                'style': {
                    'fill': '#808080', 'stroke-width': 1, 'stroke': '#808080'
                }
            }
        },
        'tasks': {
            'ActivityTask': {
                'rectangle': {
                    'min-width': 80, 'max-width': 160,
                    'rx': 5, 'ry': 5,
                    'inner-shape-margin-spec': {
                        'left': 4, 'top': 4, 'right': 4, 'bottom': 4
                    },
                    'pad-spec': {
                        'left': 10, 'top': 10, 'right': 10, 'bottom': 10
                    },
                    'style': {
                        'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#808080'
                    },
                },
                'top-left-inner-shape': {
                    'style': {
                        'fill': '#FFFFFF', 'stroke-width': 1.5, 'stroke': '#404040'
                    }
                }
            },
            'ActivityTaskBusinessRule': {
                'rectangle': {
                    'min-width': 80, 'max-width': 160,
                    'rx': 5, 'ry': 5,
                    'inner-shape-margin-spec': {
                        'left': 4, 'top': 4, 'right': 4, 'bottom': 4
                    },
                    'pad-spec': {
                        'left': 10, 'top': 24, 'right': 10, 'bottom': 10
                    },
                    'style': {
                        'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#808080'
                    },
                },
                'top-left-inner-shape': {
                    'width': 20, 'height': 15,
                    'svg-path': '../conf/business-rule.svg'
                }
            },
            'ActivityTaskManual': {
                'rectangle': {
                    'min-width': 80, 'max-width': 160,
                    'rx': 5, 'ry': 5,
                    'inner-shape-margin-spec': {
                        'left': 4, 'top': 4, 'right': 4, 'bottom': 4
                    },
                    'pad-spec': {
                        'left': 10, 'top': 24, 'right': 10, 'bottom': 10
                    },
                    'style': {
                        'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#808080'
                    },
                },
                'top-left-inner-shape': {
                    'width': 16, 'height': 16,
                    'svg-path': '../conf/manual.svg'
                }
            },
            'ActivityTaskReceive': {
                'rectangle': {
                    'min-width': 80, 'max-width': 160,
                    'rx': 5, 'ry': 5,
                    'inner-shape-margin-spec': {
                        'left': 4, 'top': 4, 'right': 4, 'bottom': 4
                    },
                    'pad-spec': {
                        'left': 10, 'top': 24, 'right': 10, 'bottom': 10
                    },
                    'style': {
                        'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#808080'
                    },
                },
                'top-left-inner-shape': {
                    'width': 18, 'height': 13,
                    'style': {
                        'fill': '#FFFFFF', 'stroke-width': 1.5, 'stroke': '#404040'
                    }
                }
            },
            'ActivityTaskScript': {
                'rectangle': {
                    'min-width': 80, 'max-width': 160,
                    'rx': 5, 'ry': 5,
                    'inner-shape-margin-spec': {
                        'left': 4, 'top': 4, 'right': 4, 'bottom': 4
                    },
                    'pad-spec': {
                        'left': 10, 'top': 24, 'right': 10, 'bottom': 10
                    },
                    'style': {
                        'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#808080'
                    },
                },
                'top-left-inner-shape': {
                    'width': 16, 'height': 16,
                    'svg-path': '../conf/script.svg'
                }
            },
            'ActivityTaskSend': {
                'rectangle': {
                    'min-width': 80, 'max-width': 160,
                    'rx': 5, 'ry': 5,
                    'inner-shape-margin-spec': {
                        'left': 4, 'top': 4, 'right': 4, 'bottom': 4
                    },
                    'pad-spec': {
                        'left': 10, 'top': 24, 'right': 10, 'bottom': 10
                    },
                    'style': {
                        'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#808080'
                    },
                },
                'top-left-inner-shape': {
                    'width': 20, 'height': 15,
                    'style': {
                        'fill': '#000000', 'stroke-width': 1.25, 'stroke': '#FFFFFF'
                    }
                }
            },
            'ActivityTaskService': {
                'rectangle': {
                    'min-width': 80, 'max-width': 160,
                    'rx': 5, 'ry': 5,
                    'inner-shape-margin-spec': {
                        'left': 4, 'top': 4, 'right': 4, 'bottom': 4
                    },
                    'pad-spec': {
                        'left': 10, 'top': 24, 'right': 10, 'bottom': 10
                    },
                    'style': {
                        'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#808080'
                    },
                },
                'top-left-inner-shape': {
                    'width': 20, 'height': 15,
                    'style': {
                        'fill': '#FFFFFF', 'stroke-width': 1.5, 'stroke': '#404040'
                    }
                }
            },
            'ActivityTaskUser': {
                'rectangle': {
                    'min-width': 80, 'max-width': 160,
                    'rx': 5, 'ry': 5,
                    'inner-shape-margin-spec': {
                        'left': 4, 'top': 4, 'right': 4, 'bottom': 4
                    },
                    'pad-spec': {
                        'left': 10, 'top': 24, 'right': 10, 'bottom': 10
                    },
                    'style': {
                        'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#808080'
                    },
                },
                'top-left-inner-shape': {
                    'width': 16, 'height': 16,
                    'svg-path': '../conf/user.svg'
                }
            }
        },
        'subprocesses': {
            'ActivitySubprocess': {
                'rectangle': {
                    'min-width': 80, 'max-width': 160,
                    'rx': 5, 'ry': 5,
                    'inner-shape-margin-spec': {
                        'left': 4, 'top': 4, 'right': 4, 'bottom': 4
                    },
                    'pad-spec': {
                        'left': 10, 'top': 10, 'right': 10, 'bottom': 20
                    },
                    'style': {
                        'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#808080'
                    },
                },
                'bottom-center-rectangle': {
                    'width': 14, 'height': 14,
                    'rx': 0, 'ry': 0,
                    'margin-spec': {
                        'left': 2, 'top': 2, 'right': 2, 'bottom': 4
                    },
                    'pad-spec': {
                        'left': 2, 'top': 2, 'right': 2, 'bottom': 2
                    },
                    'style': {
                        'fill': '#FFFFFF', 'stroke-width': 1, 'stroke': '#808080'
                    }
                },
                'bottom-center-inner-shape': {
                    'style': {
                        'fill': '#808080', 'stroke-width': 0.25, 'stroke': '#808080'
                    }
                }
            },
            'ActivityAdhocSubprocess': {
            },
            'ActivityTransactionSubprocess': {
                'outer-rectangle': {
                    'rx': 5, 'ry': 5,
                    'pad-spec': {
                        'left': 5, 'top': 5, 'right': 5, 'bottom': 5
                    },
                    'style': {
                        'fill': '#FFFFFF', 'stroke-width': 1.5, 'stroke': '#808080'
                    }
                }
            },
            'ActivityEventSubprocess': {
                'rectangle': {
                    'min-width': 80, 'max-width': 160,
                    'rx': 5, 'ry': 5,
                    'inner-shape-margin-spec': {
                        'left': 4, 'top': 4, 'right': 4, 'bottom': 4
                    },
                    'pad-spec': {
                        'left': 15, 'top': 22, 'right': 10, 'bottom': 20
                    },
                    'style': {
                        'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#808080', 'stroke-dasharray': '5,5'
                    },
                },
                'top-left-circle': {
                    'radius': 10,
                    'margin-spec': {
                        'left': 4, 'top': 4, 'right': 2, 'bottom': 2
                    },
                    'style': {
                        'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#808080'
                    }
                },
                'top-left-inner-shape': {
                    'style': {
                        'fill': '#FFFFFF', 'stroke-width': 1, 'stroke': '#404040'
                    }
                }
            },
            'event-subprocesses': {
                'ActivityEventCompensation': {
                },
                'ActivityEventConditional': {
                },
                'ActivityEventConditionalNon': {
                    'top-left-circle': {
                        'radius': 10,
                        'margin-spec': {
                            'left': 4, 'top': 4, 'right': 2, 'bottom': 2
                        },
                        'style': {
                            'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#404040', 'stroke-dasharray': '4,4'
                        }
                    }
                },
                'ActivityEventError': {
                },
                'ActivityEventEscalation': {
                },
                'ActivityEventEscalationNon': {
                    'top-left-circle': {
                        'radius': 10,
                        'margin-spec': {
                            'left': 4, 'top': 4, 'right': 2, 'bottom': 2
                        },
                        'style': {
                            'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#404040', 'stroke-dasharray': '4,4'
                        }
                    }
                },
                'ActivityEventMessage': {
                },
                'ActivityEventMessageNon': {
                    'top-left-circle': {
                        'radius': 10,
                        'margin-spec': {
                            'left': 4, 'top': 4, 'right': 2, 'bottom': 2
                        },
                        'style': {
                            'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#404040', 'stroke-dasharray': '4,4'
                        }
                    }
                },
                'ActivityEventMultiple': {
                },
                'ActivityEventMultipleNon': {
                    'top-left-circle': {
                        'radius': 10,
                        'margin-spec': {
                            'left': 4, 'top': 4, 'right': 2, 'bottom': 2
                        },
                        'style': {
                            'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#404040', 'stroke-dasharray': '4,4'
                        }
                    }
                },
                'ActivityEventParallelMultiple': {
                },
                'ActivityEventParallelMultipleNon': {
                    'top-left-circle': {
                        'radius': 10,
                        'margin-spec': {
                            'left': 4, 'top': 4, 'right': 2, 'bottom': 2
                        },
                        'style': {
                            'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#404040', 'stroke-dasharray': '4,4'
                        }
                    }
                },
                'ActivityEventSignal': {
                },
                'ActivityEventSignalNon': {
                    'top-left-circle': {
                        'radius': 10,
                        'margin-spec': {
                            'left': 4, 'top': 4, 'right': 2, 'bottom': 2
                        },
                        'style': {
                            'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#404040', 'stroke-dasharray': '4,4'
                        }
                    }
                },
                'ActivityEventTimer': {
                },
                'ActivityEventTimerNon': {
                    'top-left-circle': {
                        'radius': 10,
                        'margin-spec': {
                            'left': 4, 'top': 4, 'right': 2, 'bottom': 2
                        },
                        'style': {
                            'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#404040', 'stroke-dasharray': '4,4'
                        }
                    }
                },
            }
        },
        'calls': {
            'ActivityCall': {
                'rectangle': {
                    'min-width': 80, 'max-width': 160,
                    'rx': 5, 'ry': 5,
                    'inner-shape-margin-spec': {
                        'left': 4, 'top': 4, 'right': 4, 'bottom': 4
                    },
                    'pad-spec': {
                        'left': 10, 'top': 10, 'right': 10, 'bottom': 10
                    },
                    'style': {
                        'fill': '#FFFFFF', 'stroke-width': 4, 'stroke': '#808080'
                    },
                },
                'top-left-circle': {
                    'radius': 10,
                    'margin-spec': {
                        'left': 5, 'top': 5, 'right': 2, 'bottom': 2
                    },
                    'style': {
                        'fill': '#FFFFFF', 'stroke-width': 1, 'stroke': '#808080'
                    }
                },
                'top-left-inner-shape': {
                    'style': {
                        'fill': '#FFFFFF', 'stroke-width': 1, 'stroke': '#808080'
                    }
                }
            },
            'ActivityCallBusinessRule': {
                'rectangle': {
                    'min-width': 80, 'max-width': 160,
                    'rx': 5, 'ry': 5,
                    'inner-shape-margin-spec': {
                        'left': 4, 'top': 4, 'right': 4, 'bottom': 4
                    },
                    'pad-spec': {
                        'left': 10, 'top': 24, 'right': 10, 'bottom': 10
                    },
                    'style': {
                        'fill': '#FFFFFF', 'stroke-width': 4, 'stroke': '#808080'
                    },
                },
                'top-left-inner-shape': {
                    'width': 20, 'height': 15,
                    'svg-path': '../conf/business-rule.svg'
                }
            },
            'ActivityCallManual': {
                'rectangle': {
                    'min-width': 80, 'max-width': 160,
                    'rx': 5, 'ry': 5,
                    'inner-shape-margin-spec': {
                        'left': 4, 'top': 4, 'right': 4, 'bottom': 4
                    },
                    'pad-spec': {
                        'left': 10, 'top': 24, 'right': 10, 'bottom': 10
                    },
                    'style': {
                        'fill': '#FFFFFF', 'stroke-width': 4, 'stroke': '#808080'
                    },
                },
                'top-left-inner-shape': {
                    'width': 16, 'height': 16,
                    'svg-path': '../conf/manual.svg'
                }
            },
            'ActivityCallScript': {
                'rectangle': {
                    'min-width': 80, 'max-width': 160,
                    'rx': 5, 'ry': 5,
                    'inner-shape-margin-spec': {
                        'left': 4, 'top': 4, 'right': 4, 'bottom': 4
                    },
                    'pad-spec': {
                        'left': 10, 'top': 24, 'right': 10, 'bottom': 10
                    },
                    'style': {
                        'fill': '#FFFFFF', 'stroke-width': 4, 'stroke': '#808080'
                    },
                },
                'top-left-inner-shape': {
                    'width': 16, 'height': 16,
                    'svg-path': '../conf/script.svg'
                }
            },
            'ActivityCallUser': {
                'top-left-inner-shape': {
                    'width': 16, 'height': 16,
                    'svg-path': '../conf/user.svg'
                }
            }
        }
    },
    'gateways': {
        'Gateway': {
            'rectangle': {
                'min-width': 80, 'max-width': 120, 'rx': 5, 'ry': 5,
                'pad-spec': {
                    'left': 2, 'top': 2, 'right': 2, 'bottom': 2
                },
                'style': {
                    'fill': '#FFFFFF', 'stroke-width': 0, 'stroke': '#FF8080'
                }
            },
            'text': {
                'vertical-text': False, 'max-lines': 4,
                'style': {
                    'text-anchor': 'middle', 'dominant-baseline': 'middle', 'font-family': 'arial', 'font-size': 10, 'fill': '#202020', 'stroke': '#000000', 'stroke-width': 0
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
            },
            'inner-circle': {
                'style': {
                    'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#808080'
                }
            },
            'inner-shape': {
                'style': {
                    'fill': '#FFFFFF', 'stroke-width': 3, 'stroke': '#808080'
                }
            },
        },
        'GatewayExclusive': {
            'inner-shape': {
                'style': {
                    'fill': '#808080', 'stroke-width': 1, 'stroke': '#808080'
                }
            },
        },
        'GatewayInclusive': {
        },
        'GatewayParallel': {
            'inner-shape': {
                'style': {
                    'fill': '#808080', 'stroke-width': 1, 'stroke': '#808080'
                }
            },
        },
        'GatewayComplex': {
        },
        'GatewayEventBased': {
            'inner-circle': {
                'style': {
                    'fill': '#FFFFFF', 'stroke-width': 1.5, 'stroke': '#808080'
                }
            },
            'inner-shape': {
                'style': {
                    'fill': '#FFFFFF', 'stroke-width': 1.5, 'stroke': '#808080'
                }
            }
        },
        'GatewayEventBasedStart': {
            'inner-shape': {
                'style': {
                    'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#808080'
                }
            }
        },
        'GatewayEventBasedParallelStart': {
            'inner-shape': {
                'style': {
                    'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#808080'
                }
            }
        }
    },
    'flows': {
        'Sequence': {
            'from-arrow': False,
            'to-arrow': True,
            'style': {
                'fill': 'transparent', 'stroke-width': 1, 'stroke': '#404040'
            },
            'arrow-head': {
                'arrow-side-length': 10,
                'style': {
                    'fill': '#404040', 'stroke-width': 1, 'stroke': '#404040'
                },
            },
        },
        'Message': {
            'from-arrow': False,
            'to-arrow': True,
            'style': {
                'fill': 'none', 'stroke-width': 2, 'stroke': '#A0A0A0', 'stroke-dasharray': '5,5'
            },
            'arrow-head': {
                'arrow-side-length': 10,
                'style': {
                    'fill': '#404040', 'stroke-width': 2, 'stroke': '#A0A0A0'
                },
            },
        },
        'Association': {
            'from-arrow': False,
            'to-arrow': False,
            'style': {
                'fill': 'none', 'stroke-width': 2, 'stroke': '#A0A0A0', 'stroke-dasharray': '2,2'
            },
            'arrow-head': {
                'arrow-side-length': 12,
                'style': {
                    'fill': 'none', 'stroke-width': 2, 'stroke': '#A0A0A0'
                },
            },
        },
        'DirectedAssociation': {
            'from-arrow': False,
            'to-arrow': True,
            'style': {
                'fill': 'none', 'stroke-width': 2, 'stroke': '#A0A0A0', 'stroke-dasharray': '2,2'
            },
            'arrow-head': {
                'arrow-side-length': 12,
                'style': {
                    'fill': 'none', 'stroke-width': 2, 'stroke': '#A0A0A0'
                },
            },
        },
        'BidirectionalAssociation': {
            'from-arrow': True,
            'to-arrow': True,
            'style': {
                'fill': 'none', 'stroke-width': 2, 'stroke': '#A0A0A0', 'stroke-dasharray': '2,2'
            },
            'arrow-head': {
                'arrow-side-length': 12,
                'style': {
                    'fill': 'none', 'stroke-width': 2, 'stroke': '#A0A0A0'
                },
            },
        },
    },
    'datas': {
        'DataObject': {
            'rectangle': {
                'min-width': 60, 'max-width': 120, 'rx': 0, 'ry': 0,
                'pad-spec': {
                    'left': 2, 'top': 2, 'right': 2, 'bottom': 2
                },
                'style': {
                    'fill': '#FFFFFF', 'stroke-width': 0, 'stroke': '#FF8080'
                }
            },
            'text': {
                'vertical-text': False, 'max-lines': 4,
                'style': {
                    'text-anchor': 'middle', 'dominant-baseline': 'middle', 'font-family': 'arial', 'font-size': 10, 'fill': '#202020', 'stroke': '#000000', 'stroke-width': 0
                }
            },
            'folded-rectangle': {
                'width': 40, 'height': 60, 'fold-length': 15,
                'pad-spec': {
                    'left': 4, 'top': 4, 'right': 4, 'bottom': 4
                },
                'style': {
                    'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#808080'
                }
            },
            'top-left-inner-shape': {
                'width': 16, 'height': 12,
                'style': {
                    'fill': '#FFFFFF', 'stroke-width': 1, 'stroke': '#808080'
                }
            },
            'bottom-center-inner-shape': {
                'width': 20, 'height': 12,
                'style': {
                    'fill': '#000000', 'stroke-width': 1, 'stroke': '#FFFFFF'
                }
            }
        },
        'DataCollection': {
        },
        'DataInput': {
        },
        'DataInputCollection': {
        },
        'DataOutput': {
            'top-left-inner-shape': {
                'width': 16, 'height': 12,
                'style': {
                    'fill': '#404040', 'stroke-width': 1, 'stroke': '#808080'
                }
            },
        },
        'DataOutputCollection': {
            'top-left-inner-shape': {
                'width': 16, 'height': 12,
                'style': {
                    'fill': '#404040', 'stroke-width': 1, 'stroke': '#808080'
                }
            },
        },
        'DataStore': {
            'shape-spec': {
                'width': 50, 'height': 70,
                'svg-path': '../conf/data-store.svg'
            }
        }
    },
    'artifacts': {
    }
}
