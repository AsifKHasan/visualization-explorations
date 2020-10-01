#!/usr/bin/env python3
bpmn_data  = {
        "styles": {
            "hide_labels": "true"
        },
        "label": "Pizza Order Process Modeling",
        "lanes": {
            "customer": {
                "styles": {},
                "label": "Customer",
                "pools": {
                    "pizza_customer": {
                        "styles": {},
                        "label": "Pizza Customer",
                        "nodes": {
                            "hungry": {
                                "type": "start",
                                "label": "Hungry",
                                "styles": {}
                            },
                            "select_pizza": {
                                "type": "task",
                                "label": "",
                                "styles": {}
                            },
                            "order_pizza": {
                                "type": "task",
                                "label": "",
                                "styles": {}
                            },
                            "on_order": {
                                "type": "eventBased",
                                "label": "Ordered",
                                "styles": {
                                    "label_pos": "bottom"
                                }
                            },
                            "pizza_received": {
                                "type": "throwMessage",
                                "label": "",
                                "styles": {}
                            },
                            "timer_45_mins": {
                                "type": "timer",
                                "label": "45 Minutes",
                                "styles": {}
                            },
                            "ask_for_pizza": {
                                "type": "task",
                                "label": "",
                                "styles": {}
                            },
                            "eat_pizza": {
                                "type": "task",
                                "label": "",
                                "styles": {}
                            },
                            "pay_for_pizza": {
                                "type": "task",
                                "label": "",
                                "styles": {}
                            },
                            "hunger_satisfied": {
                                "type": "end",
                                "label": "Hunger Satisfied",
                                "styles": {}
                            }
                        },
                        "edges": [
                            {
                                "from": "hungry",
                                "to": "select_pizza",
                                "type": "-->",
                                "label": "",
                                "styles": {}
                            },
                            {
                                "from": "select_pizza",
                                "to": "order_pizza",
                                "type": "-->",
                                "label": "",
                                "styles": {}
                            },
                            {
                                "from": "order_pizza",
                                "to": "on_order",
                                "type": "-->",
                                "label": "",
                                "styles": {}
                            },
                            {
                                "from": "on_order",
                                "to": "pizza_received",
                                "type": "-->",
                                "label": "",
                                "styles": {}
                            },
                            {
                                "from": "pizza_received",
                                "to": "pay_for_pizza",
                                "type": "-->",
                                "label": "",
                                "styles": {}
                            },
                            {
                                "from": "pay_for_pizza",
                                "to": "eat_pizza",
                                "type": "-->",
                                "label": "",
                                "styles": {}
                            },
                            {
                                "from": "eat_pizza",
                                "to": "hunger_satisfied",
                                "type": "-->",
                                "label": "",
                                "styles": {}
                            },
                            {
                                "from": "on_order",
                                "to": "timer_45_mins",
                                "type": "-->",
                                "label": "",
                                "styles": {}
                            },
                            {
                                "from": "timer_45_mins",
                                "to": "ask_for_pizza",
                                "type": "-->",
                                "label": "",
                                "styles": {}
                            },
                            {
                                "from": "ask_for_pizza",
                                "to": "on_order",
                                "type": "-->",
                                "label": "",
                                "styles": {}
                            }
                        ]
                    }
                },
                "edges": []
            },
            "pizza_store": {
                "styles": {},
                "label": "Pizza Store",
                "pools": {
                    "receptionist": {
                        "styles": {},
                        "label": "Receptionist",
                        "nodes": {
                            "order_received": {
                                "type": "startMessage",
                                "label": "Order Received",
                                "styles": {}
                            },
                            "on_order_received": {
                                "type": "parallel",
                                "label": "",
                                "styles": {}
                            },
                            "where_is_pizza": {
                                "type": "throwMessage",
                                "label": "Where is Pizza?",
                                "styles": {
                                    "label_pos": "bottom"
                                }
                            },
                            "deal_with_customer": {
                                "type": "task",
                                "label": "",
                                "styles": {}
                            }
                        },
                        "edges": [
                            {
                                "from": "order_received",
                                "to": "on_order_received",
                                "type": "-->",
                                "label": "",
                                "styles": {}
                            },
                            {
                                "from": "on_order_received",
                                "to": "where_is_pizza",
                                "type": "-->",
                                "label": "",
                                "styles": {}
                            },
                            {
                                "from": "where_is_pizza",
                                "to": "deal_with_customer",
                                "type": "-->",
                                "label": "",
                                "styles": {}
                            },
                            {
                                "from": "deal_with_customer",
                                "to": "where_is_pizza",
                                "type": "-->",
                                "label": "",
                                "styles": {}
                            },
                            {
                                "from": "on_order_received",
                                "to": "deal_with_customer",
                                "type": "-->",
                                "label": "",
                                "styles": {}
                            }
                        ]
                    },
                    "cook": {
                        "styles": {
                            "move_x": "200"
                        },
                        "label": "Pizza Cook",
                        "nodes": {
                            "bake_pizza": {
                                "type": "task",
                                "label": "",
                                "styles": {}
                            }
                        },
                        "edges": []
                    },
                    "delivery_person": {
                        "styles": {
                            "move_x": "310"
                        },
                        "label": "Delivery Person",
                        "nodes": {
                            "deliver_pizza": {
                                "type": "task",
                                "label": "",
                                "styles": {}
                            },
                            "collect_payment": {
                                "type": "task",
                                "label": "",
                                "styles": {}
                            },
                            "end_terminate": {
                                "type": "endTerminate",
                                "label": "",
                                "styles": {}
                            }
                        },
                        "edges": [
                            {
                                "from": "deliver_pizza",
                                "to": "collect_payment",
                                "type": "-->",
                                "label": "",
                                "styles": {}
                            },
                            {
                                "from": "collect_payment",
                                "to": "end_terminate",
                                "type": "-->",
                                "label": "",
                                "styles": {}
                            }
                        ]
                    }
                },
                "edges": [
                    {
                        "from": "on_order_received",
                        "to": "bake_pizza",
                        "type": "-->",
                        "label": "",
                        "styles": {}
                    },
                    {
                        "from": "bake_pizza",
                        "to": "deliver_pizza",
                        "type": "-->",
                        "label": "",
                        "styles": {}
                    },
                    {
                        "from": "where_is_pizza",
                        "to": "deliver_pizza",
                        "type": "-->",
                        "label": "",
                        "styles": {}
                    }
                ]
            }
        },
        "edges": [
            {
                "from": "order_pizza",
                "to": "order_received",
                "type": "~~>",
                "label": "pizza order",
                "styles": {}
            },
            {
                "from": "ask_for_pizza",
                "to": "where_is_pizza",
                "type": "~~>",
                "label": "",
                "styles": {}
            },
            {
                "from": "pay_for_pizza",
                "to": "collect_payment",
                "type": "~~>",
                "label": "money",
                "styles": {}
            },
            {
                "from": "deal_with_customer",
                "to": "ask_for_pizza",
                "type": "~~>",
                "label": "",
                "styles": {}
            },
            {
                "from": "deliver_pizza",
                "to": "pizza_received",
                "type": "~~>",
                "label": "pizza",
                "styles": {}
            },
            {
                "from": "collect_payment",
                "to": "pay_for_pizza",
                "type": "~~>",
                "label": "receipt",
                "styles": {}
            }
        ]
    }

pool_nodes = bpmn_data['lanes']['customer']['pools']['pizza_customer']['nodes']
# ['hungry', 'select_pizza', 'order_pizza', 'on_order', 'pizza_received', 'timer_45_mins', 'ask_for_pizza', 'eat_pizza', 'pay_for_pizza', 'hunger_satisfied']
