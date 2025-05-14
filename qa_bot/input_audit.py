#! coding: utf-8

import unittest
from utils.tools import get_model_name, get_completion, get_completion_from_messages


class TestLLMInputAudit(unittest.TestCase):
    def setUp(self) -> None:
        self.model = get_model_name()

    pass


if __name__ == '__main__':
    unittest.main(verbosity=2)
