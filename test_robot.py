import unittest
from unittest.mock import patch
from io import StringIO as io
import sys
import robot as bot

class test_robot(unittest.TestCase):

    maxDiff = None

    def setUp(self):
        sys.stdout = io()


    def tearDown(self):
        sys.stdout = sys.__stdout__


    @patch('sys.stdin', io('CASEE\nback 6\nright\nforward 3\nleft\nsprint 4\nreplay 1\noff\n'))
    def test_replay_1(self):

        with patch('sys.stdout', new=io()) as dummy_out:
            bot.robot_start()
            result = dummy_out.getvalue()
            expected = '''What do you want to name your robot? CASEE: Hello kiddo!
CASEE: What must I do next?  > CASEE moved back by 6 steps.
 > CASEE now at position (0,-6).
CASEE: What must I do next?  > CASEE turned right.
 > CASEE now at position (0,-6).
CASEE: What must I do next?  > CASEE moved forward by 3 steps.
 > CASEE now at position (3,-6).
CASEE: What must I do next?  > CASEE turned left.
 > CASEE now at position (3,-6).
CASEE: What must I do next?  > CASEE moved forward by 4 steps.
 > CASEE moved forward by 3 steps.
 > CASEE moved forward by 2 steps.
 > CASEE moved forward by 1 steps.
 > CASEE now at position (3,4).
CASEE: What must I do next?  > CASEE moved back by 6 steps.
 > CASEE now at position (3,-2).
 > CASEE turned right.
 > CASEE now at position (3,-2).
 > CASEE moved forward by 3 steps.
 > CASEE now at position (6,-2).
 > CASEE turned left.
 > CASEE now at position (6,-2).
 > CASEE moved forward by 4 steps.
 > CASEE moved forward by 3 steps.
 > CASEE moved forward by 2 steps.
 > CASEE moved forward by 1 steps.
 > CASEE now at position (6,8).
 > CASEE replayed 5 commands.
 > CASEE now at position (6,8).
CASEE: What must I do next? CASEE: Shutting down..
'''
        self.assertEqual(result, expected)


    @patch('sys.stdin', io('TARS\nleft\nforward 12\nleft\nback 14\nreplay 1\noff\n'))
    def test_replay_specific(self):
        with patch('sys.stdout', new=io()) as dummy_out:
            bot.robot_start()
            result = dummy_out.getvalue()
        expected = '''What do you want to name your robot? TARS: Hello kiddo!
TARS: What must I do next?  > TARS turned left.
 > TARS now at position (0,0).
TARS: What must I do next?  > TARS moved forward by 12 steps.
 > TARS now at position (-12,0).
TARS: What must I do next?  > TARS turned left.
 > TARS now at position (-12,0).
TARS: What must I do next?  > TARS moved back by 14 steps.
 > TARS now at position (-12,14).
TARS: What must I do next?  > TARS turned left.
 > TARS now at position (-12,14).
 > TARS moved forward by 12 steps.
 > TARS now at position (0,14).
 > TARS turned left.
 > TARS now at position (0,14).
 > TARS moved back by 14 steps.
 > TARS now at position (0,0).
 > TARS replayed 4 commands.
 > TARS now at position (0,0).
TARS: What must I do next? TARS: Shutting down..
'''

        self.assertEqual(result, expected)


    @patch('sys.stdin', io('CASEE\nback 6\nright\nforward 3\nleft\nsprint 4\nright\nback 13\nreplay silent\nreplay 1-4 silent\noff\n'))
    def test_range_of_three(self):
        with patch('sys.stdout', new=io()) as dummy_out:
            bot.robot_start()
            result = dummy_out.getvalue()
        expected = '''What do you want to name your robot? CASEE: Hello kiddo!
CASEE: What must I do next?  > CASEE moved back by 6 steps.
 > CASEE now at position (0,-6).
CASEE: What must I do next?  > CASEE turned right.
 > CASEE now at position (0,-6).
CASEE: What must I do next?  > CASEE moved forward by 3 steps.
 > CASEE now at position (3,-6).
CASEE: What must I do next?  > CASEE turned left.
 > CASEE now at position (3,-6).
CASEE: What must I do next?  > CASEE moved forward by 4 steps.
 > CASEE moved forward by 3 steps.
 > CASEE moved forward by 2 steps.
 > CASEE moved forward by 1 steps.
 > CASEE now at position (3,4).
CASEE: What must I do next?  > CASEE turned right.
 > CASEE now at position (3,4).
CASEE: What must I do next?  > CASEE moved back by 13 steps.
 > CASEE now at position (-10,4).
CASEE: What must I do next?  > CASEE replayed 7 commands silently.
 > CASEE now at position (-6,14).
CASEE: What must I do next?  > CASEE replayed 3 commands silently.
 > CASEE now at position (-9,20).
CASEE: What must I do next? CASEE: Shutting down..
'''
        self.assertEqual(result, expected)



if __name__ == '__main__':

    unittest.main()
