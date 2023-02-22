from engine import Space, WHITE, RED


STARTING_BOARD = [Space(0, 'bearoff_zone', RED),
                  Space(0, 'bar', WHITE),
                  Space(1, 'outer', WHITE, 2),
                  Space(2, 'outer'),
                  Space(3, 'outer'),
                  Space(4, 'outer'),
                  Space(5, 'outer'),
                  Space(6, 'outer', RED, 5),
                  Space(7, 'outer'),
                  Space(8, 'outer', RED, 3),
                  Space(9, 'outer'),
                  Space(10, 'outer'),
                  Space(11, 'outer'),
                  Space(12, 'outer', WHITE, 5),
                  Space(13, 'outer', RED, 5),
                  Space(14, 'outer'),
                  Space(15, 'outer'),
                  Space(16, 'outer'),
                  Space(17, 'outer', WHITE, 3),
                  Space(18, 'outer'),
                  Space(19, 'outer', WHITE, 5),
                  Space(20, 'outer'),
                  Space(21, 'outer'),
                  Space(22, 'outer'),
                  Space(23, 'outer'),
                  Space(24, 'outer', RED, 2),
                  Space(25, 'bearoff_zone', WHITE),
                  Space(25, 'bar', RED)
                  ]

TEST_LARGESE_MOVE_DICE_5_4 = [5, 4]
TEST_LARGESE_MOVE = [Space(0, 'bearoff_zone', RED),
                     Space(0, 'bar', WHITE),
                     Space(1, 'outer', RED, 12),
                     Space(2, 'outer'),
                     Space(3, 'outer', RED, 2),
                     Space(4, 'outer'),
                     Space(5, 'outer'),
                     Space(6, 'outer'),
                     Space(7, 'outer'),
                     Space(8, 'outer'),
                     Space(9, 'outer'),
                     Space(10, 'outer'),
                     Space(11, 'outer'),
                     Space(12, 'outer', WHITE, 5),
                     Space(13, 'outer'),
                     Space(14, 'outer'),
                     Space(15, 'outer'),
                     Space(16, 'outer'),
                     Space(17, 'outer'),
                     Space(18, 'outer'),
                     Space(19, 'outer', WHITE, 5),
                     Space(20, 'outer', WHITE, 5),
                     Space(21, 'outer', RED, 1),
                     Space(22, 'outer'),
                     Space(23, 'outer'),
                     Space(24, 'outer'),
                     Space(25, 'bearoff_zone', WHITE),
                     Space(25, 'bar', RED)
                     ]


TEST_ONE_ON_BAR_DICE_5_4 = [5, 4]
TEST_ONE_ON_BAR = [Space(0, 'bearoff_zone', RED),
                   Space(0, 'bar', WHITE),
                   Space(1, 'outer', RED, 12),
                   Space(2, 'outer'),
                   Space(3, 'outer'),
                   Space(4, 'outer'),
                   Space(5, 'outer', RED, 1),
                   Space(6, 'outer', RED, 1),
                   Space(7, 'outer'),
                   Space(8, 'outer'),
                   Space(9, 'outer'),
                   Space(10, 'outer'),
                   Space(11, 'outer'),
                   Space(12, 'outer'),
                   Space(13, 'outer'),
                   Space(14, 'outer'),
                   Space(15, 'outer'),
                   Space(16, 'outer'),
                   Space(17, 'outer'),
                   Space(18, 'outer'),
                   Space(19, 'outer', WHITE, 5),
                   Space(20, 'outer', WHITE, 5),
                   Space(21, 'outer'),
                   Space(22, 'outer', WHITE, 2),
                   Space(23, 'outer', WHITE, 3),
                   Space(24, 'outer'),
                   Space(25, 'bearoff_zone', WHITE),
                   Space(25, 'bar', RED, 1)
                   ]


TEST_TWO_ON_BAR_DICE_5_4 = [5, 4]
TEST_TWO_ON_BAR = [Space(0, 'bearoff_zone', RED),
                   Space(0, 'bar', WHITE),
                   Space(1, 'outer', RED, 11),
                   Space(2, 'outer'),
                   Space(3, 'outer'),
                   Space(4, 'outer'),
                   Space(5, 'outer', RED, 1),
                   Space(6, 'outer', RED, 1),
                   Space(7, 'outer'),
                   Space(8, 'outer'),
                   Space(9, 'outer'),
                   Space(10, 'outer'),
                   Space(11, 'outer'),
                   Space(12, 'outer'),
                   Space(13, 'outer'),
                   Space(14, 'outer'),
                   Space(15, 'outer'),
                   Space(16, 'outer'),
                   Space(17, 'outer'),
                   Space(18, 'outer'),
                   Space(19, 'outer', WHITE, 5),
                   Space(20, 'outer', WHITE, 5),
                   Space(21, 'outer'),
                   Space(22, 'outer', WHITE, 2),
                   Space(23, 'outer', WHITE, 3),
                   Space(24, 'outer'),
                   Space(25, 'bearoff_zone', WHITE),
                   Space(25, 'bar', RED, 2)
                   ]


TEST_BEAROFF_1_DICE_3_2 = [3, 2]
TEST_BEAROFF_1 = [Space(0, 'bearoff_zone', RED),
                  Space(0, 'bar', WHITE),
                  Space(1, 'outer', RED, 11),
                  Space(2, 'outer', RED, 1),
                  Space(3, 'outer', RED, 2),
                  Space(4, 'outer', RED, 1),
                  Space(5, 'outer'),
                  Space(6, 'outer'),
                  Space(7, 'outer'),
                  Space(8, 'outer'),
                  Space(9, 'outer'),
                  Space(10, 'outer'),
                  Space(11, 'outer'),
                  Space(12, 'outer'),
                  Space(13, 'outer', WHITE, 5),
                  Space(14, 'outer'),
                  Space(15, 'outer'),
                  Space(16, 'outer'),
                  Space(17, 'outer'),
                  Space(18, 'outer'),
                  Space(19, 'outer', WHITE, 5),
                  Space(20, 'outer', WHITE, 5),
                  Space(21, 'outer'),
                  Space(22, 'outer'),
                  Space(23, 'outer'),
                  Space(24, 'outer'),
                  Space(25, 'bearoff_zone', WHITE),
                  Space(25, 'bar', RED)
                  ]


TEST_BEAROFF_2_DICE_3_5 = [3, 5]
TEST_BEAROFF_2 = [Space(0, 'bearoff_zone', RED),
                  Space(0, 'bar', WHITE),
                  Space(1, 'outer', RED, 11),
                  Space(2, 'outer', RED, 4),
                  Space(3, 'outer'),
                  Space(4, 'outer'),
                  Space(5, 'outer'),
                  Space(6, 'outer'),
                  Space(7, 'outer'),
                  Space(8, 'outer'),
                  Space(9, 'outer'),
                  Space(10, 'outer'),
                  Space(11, 'outer'),
                  Space(12, 'outer'),
                  Space(13, 'outer', WHITE, 5),
                  Space(14, 'outer'),
                  Space(15, 'outer'),
                  Space(16, 'outer'),
                  Space(17, 'outer'),
                  Space(18, 'outer'),
                  Space(19, 'outer', WHITE, 5),
                  Space(20, 'outer', WHITE, 5),
                  Space(21, 'outer'),
                  Space(22, 'outer'),
                  Space(23, 'outer'),
                  Space(24, 'outer'),
                  Space(25, 'bearoff_zone', WHITE),
                  Space(25, 'bar', RED)
                  ]


TEST_DOUBLES_BEAROFF_DICE_5_5 = [5, 5]
TEST_DOUBLES_BEAROFF = [Space(0, 'bearoff_zone', RED),
                        Space(0, 'bar', WHITE),
                        Space(1, 'outer', RED, 11),
                        Space(2, 'outer', RED, 4),
                        Space(3, 'outer'),
                        Space(4, 'outer'),
                        Space(5, 'outer'),
                        Space(6, 'outer'),
                        Space(7, 'outer'),
                        Space(8, 'outer'),
                        Space(9, 'outer'),
                        Space(10, 'outer'),
                        Space(11, 'outer'),
                        Space(12, 'outer'),
                        Space(13, 'outer', WHITE, 5),
                        Space(14, 'outer'),
                        Space(15, 'outer'),
                        Space(16, 'outer'),
                        Space(17, 'outer'),
                        Space(18, 'outer'),
                        Space(19, 'outer', WHITE, 5),
                        Space(20, 'outer', WHITE, 5),
                        Space(21, 'outer'),
                        Space(22, 'outer'),
                        Space(23, 'outer'),
                        Space(24, 'outer'),
                        Space(25, 'bearoff_zone', WHITE),
                        Space(25, 'bar', RED)
                        ]

TEST_DOUBLES_BEAROFF_STARTING_OUTSIDE_HOMEBOARD = [Space(0, 'bearoff_zone', RED),
                                                   Space(0, 'bar', WHITE),
                                                   Space(1, 'outer', RED, 12),
                                                   Space(2, 'outer'),
                                                   Space(3, 'outer', RED, 2),
                                                   Space(4, 'outer'),
                                                   Space(5, 'outer'),
                                                   Space(6, 'outer'),
                                                   Space(7, 'outer'),
                                                   Space(8, 'outer'),
                                                   Space(9, 'outer'),
                                                   Space(10, 'outer'),
                                                   Space(11, 'outer'),
                                                   Space(12, 'outer'),
                                                   Space(
                                                       13, 'outer', WHITE, 5),
                                                   Space(14, 'outer'),
                                                   Space(15, 'outer'),
                                                   Space(16, 'outer'),
                                                   Space(17, 'outer'),
                                                   Space(18, 'outer'),
                                                   Space(
                                                       19, 'outer', WHITE, 5),
                                                   Space(
                                                       20, 'outer', RED, 1),
                                                   Space(
                                                       21, 'outer', WHITE, 5),
                                                   Space(22, 'outer'),
                                                   Space(23, 'outer'),
                                                   Space(24, 'outer'),
                                                   Space(
    25, 'bearoff_zone', WHITE),
    Space(25, 'bar', RED)
]


TEST_NO_LEGAL_MOVES_BAR_DICE_5_6 = [5, 6]
TEST_NO_LEGAL_MOVES_BAR = [Space(0, 'bearoff_zone', RED),
                           Space(0, 'bar', WHITE, 1),
                           Space(1, 'outer'),
                           Space(2, 'outer', RED, 2),
                           Space(3, 'outer', RED, 2),
                           Space(4, 'outer', RED, 2),
                           Space(5, 'outer', RED, 2),
                           Space(6, 'outer', RED, 2),
                           Space(7, 'outer', RED, 5),
                           Space(8, 'outer'),
                           Space(9, 'outer'),
                           Space(10, 'outer'),
                           Space(11, 'outer'),
                           Space(12, 'outer'),
                           Space(13, 'outer', WHITE, 14),
                           Space(14, 'outer'),
                           Space(15, 'outer'),
                           Space(16, 'outer'),
                           Space(17, 'outer'),
                           Space(18, 'outer'),
                           Space(19, 'outer'),
                           Space(20, 'outer'),
                           Space(21, 'outer'),
                           Space(22, 'outer'),
                           Space(23, 'outer'),
                           Space(24, 'outer'),
                           Space(25, 'bearoff_zone', WHITE),
                           Space(25, 'bar', RED)
                           ]

TEST_NO_LEGAL_MOVES_BLOCKED_DICE_1_1 = [1, 1]
TEST_NO_LEGAL_MOVES_BLOCKED = [Space(0, 'bearoff_zone', RED),
                               Space(0, 'bar', WHITE),
                               Space(1, 'outer', WHITE, 15),
                               Space(2, 'outer', RED, 15),
                               Space(3, 'outer'),
                               Space(4, 'outer'),
                               Space(5, 'outer'),
                               Space(6, 'outer'),
                               Space(7, 'outer'),
                               Space(8, 'outer'),
                               Space(9, 'outer'),
                               Space(10, 'outer'),
                               Space(11, 'outer'),
                               Space(12, 'outer'),
                               Space(13, 'outer'),
                               Space(14, 'outer'),
                               Space(15, 'outer'),
                               Space(16, 'outer'),
                               Space(17, 'outer'),
                               Space(18, 'outer'),
                               Space(19, 'outer'),
                               Space(20, 'outer'),
                               Space(21, 'outer'),
                               Space(22, 'outer'),
                               Space(23, 'outer'),
                               Space(24, 'outer'),
                               Space(25, 'bearoff_zone', WHITE),
                               Space(25, 'bar', RED)
                               ]


TEST_HIT_PIECE_3_1 = [3, 1]
TEST_HIT_PIECE = [Space(0, 'bearoff_zone', RED),
                  Space(0, 'bar', WHITE),
                  Space(1, 'outer', WHITE, 15),
                  Space(2, 'outer'),
                  Space(3, 'outer'),
                  Space(4, 'outer', RED, 1),
                  Space(5, 'outer'),
                  Space(6, 'outer'),
                  Space(7, 'outer'),
                  Space(8, 'outer'),
                  Space(9, 'outer'),
                  Space(10, 'outer'),
                  Space(11, 'outer'),
                  Space(12, 'outer'),
                  Space(13, 'outer'),
                  Space(14, 'outer'),
                  Space(15, 'outer', RED, 14),
                  Space(16, 'outer'),
                  Space(17, 'outer'),
                  Space(18, 'outer'),
                  Space(19, 'outer'),
                  Space(20, 'outer'),
                  Space(21, 'outer'),
                  Space(22, 'outer'),
                  Space(23, 'outer'),
                  Space(24, 'outer'),
                  Space(25, 'bearoff_zone', WHITE),
                  Space(25, 'bar', RED)
                  ]


TEST_BEAROFF_BUG_4_1 = [4, 1]
TEST_BEAROFF_BUG = [Space(0, 'bearoff_zone', RED),
                    Space(0, 'bar', WHITE),
                    Space(1, 'outer', RED, 15),
                    Space(2, 'outer'),
                    Space(3, 'outer'),
                    Space(4, 'outer'),
                    Space(5, 'outer'),
                    Space(6, 'outer'),
                    Space(7, 'outer'),
                    Space(8, 'outer'),
                    Space(9, 'outer'),
                    Space(10, 'outer'),
                    Space(11, 'outer'),
                    Space(12, 'outer'),
                    Space(13, 'outer'),
                    Space(14, 'outer'),
                    Space(15, 'outer'),
                    Space(16, 'outer'),
                    Space(17, 'outer'),
                    Space(18, 'outer'),
                    Space(19, 'outer'),
                    Space(20, 'outer'),
                    Space(21, 'outer'),
                    Space(22, 'outer'),
                    Space(23, 'outer'),
                    Space(24, 'outer', WHITE, 1),
                    Space(25, 'bearoff_zone', WHITE, 14),
                    Space(25, 'bar', RED)
                    ]

TEST_NEGATIVE_OUTER_SPACE_BUG_DICE_6_6 = [6, 6]
TEST_NEGATIVE_OUTER_SPACE_BUG = [Space(0, 'bearoff_zone', RED),
                                 Space(0, 'bar', WHITE),
                                 Space(1, 'outer', RED, 15),
                                 Space(2, 'outer'),
                                 Space(3, 'outer'),
                                 Space(4, 'outer'),
                                 Space(5, 'outer'),
                                 Space(6, 'outer'),
                                 Space(7, 'outer'),
                                 Space(8, 'outer'),
                                 Space(9, 'outer'),
                                 Space(10, 'outer'),
                                 Space(11, 'outer', WHITE, 1),
                                 Space(12, 'outer'),
                                 Space(13, 'outer'),
                                 Space(14, 'outer'),
                                 Space(15, 'outer'),
                                 Space(16, 'outer'),
                                 Space(17, 'outer', WHITE, 1),
                                 Space(18, 'outer'),
                                 Space(19, 'outer'),
                                 Space(20, 'outer'),
                                 Space(21, 'outer'),
                                 Space(22, 'outer'),
                                 Space(23, 'outer'),
                                 Space(24, 'outer', WHITE, 13),
                                 Space(25, 'bearoff_zone', WHITE),
                                 Space(25, 'bar', RED)
                                 ]
