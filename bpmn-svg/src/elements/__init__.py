default_theme = {
    'bpmn': {
        'margin-spec': {
            'left': 2, 'top': 2, 'right': 2, 'bottom': 2
        },
        'rectangle': {
            'pad-spec': {
                'left': 10, 'top': 10, 'right': 10, 'bottom': 10
            },
            'style': {
                'fill': '#F0F0F0', 'stroke-width': 2, 'stroke': '#A0A0A0'
            }
        },
        'text': {
            'vertical-text': False, 'max-lines': 2,
            'style': {
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
    'swims': {
        'LaneGroup': {
            'gap-between-lanes': 0,
        },
        'PoolGroup': {
            'gap-between-pools': 0,
        },
        'SwimLane': {
            'gap-between-text-and-pool-group': 1,
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
        }
    },
    'events': {
        'Event': {
            'rectangle': {
                'min-width': 40, 'max-width': 120, 'rx': 0, 'ry': 0,
                'pad-spec': {
                    'left': 2, 'top': 5, 'right': 2, 'bottom': 5
                },
                'style': {
                    'fill': '#FFFFFF', 'stroke-width': 0, 'stroke': '#FF8080'
                }
            },
            'text': {
                'vertical-text': False, 'max-lines': 4,
                'style': {
                    'text-anchor': 'middle', 'dominant-baseline': 'middle', 'font-family': 'arial', 'font-size': 12, 'fill': '#202020', 'stroke': '#000000', 'stroke-width': 0
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
                'inner-shape-style': {
                    'fill': '#808080', 'stroke-width': 0, 'stroke': '#808080'
                }
            },
            'EventEndCancel':{
            },
            'EventEndCompensate':{
            },
            'EventEndError':{
            },
            'EventEndEscalation':{
            },
            'EventEndMessage':{
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
                'inner-shape-style': {
                    'fill': '#000000', 'stroke-width': 0, 'stroke': '#808080'
                }
            },
            'EventIntermediateCatchCancel': {
            },
            'EventIntermediateCatchCompensation': {
            },
            'EventIntermediateThrowCompensation': {
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
            },
            'EventIntermediateCatchLink': {
            },
            'EventIntermediateThrowLink': {
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
                'inner-shape-style': {
                    'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#808080'
                }
            },
            'EventStartCompensation': {
            },
            'EventStartConditional': {
            },
            'EventStartConditionalNon': {
                'circle': {
                    'radius': 20,
                    'style': {
                        'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#808080', 'stroke-dasharray': '5,5'
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
                'pad-spec': {
                    'left': 10, 'top': 15, 'right': 10, 'bottom': 10
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
            }
        },
        'tasks': {
            'ActivityTask': {
            }
        },
        'subprocesses': {
            'ActivitySubprocess': {
                'rectangle': {
                    'min-width': 80, 'max-width': 160,
                    'rx': 5, 'ry': 5,
                    'pad-spec': {
                        'left': 10, 'top': 10, 'right': 10, 'bottom': 15
                    },
                    'style': {
                        'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#808080'
                    },
                },
                'bottom-center-rectangle': {
                    'width': 10, 'height': 10,
                    'rx': 0, 'ry': 0,
                    'margin-spec': {
                        'left': 2, 'top': 2, 'right': 2, 'bottom': 5
                    },
                    'pad-spec': {
                        'left': 2, 'top': 2, 'right': 2, 'bottom': 2
                    },
                    'style': {
                        'fill': '#FFFFFF', 'stroke-width': 1, 'stroke': '#808080'
                    }
                }
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
                    'pad-spec': {
                        'left': 10, 'top': 15, 'right': 10, 'bottom': 15
                    },
                    'style': {
                        'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#808080', 'stroke-dasharray': '5,5'
                    },
                }
            },
            'ActivityAdhocSubprocess': {
            }
        },
        'calls': {
            'ActivityCall': {
                'rectangle': {
                    'min-width': 80, 'max-width': 160,
                    'rx': 5, 'ry': 5,
                    'pad-spec': {
                        'left': 10, 'top': 10, 'right': 10, 'bottom': 10
                    },
                    'style': {
                        'fill': '#FFFFFF', 'stroke-width': 4, 'stroke': '#808080'
                    },
                }
            }
        }
    },
    'gateways': {
        'Gateway': {
            'rectangle': {
                'min-width': 80, 'max-width': 120, 'rx': 5, 'ry': 5,
                'pad-spec': {
                    'left': 5, 'top': 5, 'right': 5, 'bottom': 5
                },
                'style': {
                    'fill': '#FFFFFF', 'stroke-width': 0, 'stroke': '#FF8080'
                }
            },
            'text': {
                'vertical-text': False, 'max-lines': 4,
                'style': {
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
            },
            'inner-circle-style': {
                'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#808080'
            },
            'inner-shape-style': {
                'fill': '#FFFFFF', 'stroke-width': 3, 'stroke': '#808080'
            },
        },
        'GatewayExclusive': {
        },
        'GatewayInclusive': {
        },
        'GatewayParallel': {
            'inner-shape-style': {
                'fill': '#808080', 'stroke-width': 1, 'stroke': '#808080'
            },
        },
        'GatewayComplex': {
        },
        'GatewayEventBased': {
            'inner-circle-style': {
                'fill': '#FFFFFF', 'stroke-width': 1.5, 'stroke': '#808080'
            },
            'inner-shape-style': {
                'fill': '#FFFFFF', 'stroke-width': 1.5, 'stroke': '#808080'
            }
        },
        'GatewayEventBasedStart': {
            'inner-shape-style': {
                'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#808080'
            }
        },
        'GatewayEventBasedParallelStart': {
            'inner-shape-style': {
                'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#808080'
            }
        }
    },
    'flows': {
    },
    'datas': {
    },
    'artifacts': {
    }
}
