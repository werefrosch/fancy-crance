WEAPONS = {
    "bastard's sting": {
        # magic enhancement, weight, value, dmg, and other attributes would go here.
        "magic": 2,

        # Those lists would contain the name of effects the weapon provides by default.
        # They are empty because, in this example, the effects are only available in a
        # specific condition.
        "on_turn_actions": [],
        "on_hit_actions": [],
        "on_equip": [
            {
                "type": "check",
                "condition": {
                    'object': 'owner',
                    'attribute': 'char_class',
                    'value': "antipaladin"
                },
                True: [
                    {
                        "type": "action",
                        "action": "add_to",
                        "args": {
                            "category": "on_hit",
                            "actions": ["unholy"]
                        }
                    },
                    {
                        "type": "action",
                        "action": "add_to",
                        "args": {
                            "category": "on_turn",
                            "actions": ["unholy aurea"]
                        }
                    },
                    {
                        "type": "action",
                        "action": "set_attribute",
                        "args": {
                            "field": "magic",
                            "value": 5
                        }
                    }
                ],
                False: [
                    {
                        "type": "action",
                        "action": "set_attribute",
                        "args": {
                            "field": "magic",
                            "value": 2
                        }
                    }
                ]
            }
        ],
        "on_unequip": [
            {
                "type": "action",
                "action": "remove_from",
                "args": {
                    "category": "on_hit",
                    "actions": ["unholy"]
                },
            },
            {
                "type": "action",
                "action": "remove_from",
                "args": {
                    "category": "on_turn",
                    "actions": ["unholy aurea"]
                },
            },
            {
                "type": "action",
                "action": "set_attribute",
                "args": ["magic", 2]
            }
        ]
    }
}