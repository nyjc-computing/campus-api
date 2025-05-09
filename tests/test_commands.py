# Unit tests for the command executor
import unittest
from cli.commands import CommandExecutor

class TestCommandExecutor(unittest.TestCase):
    def setUp(self):
        self.executor = CommandExecutor()

    def test_execute(self):
        result = self.executor.execute("echo Hello, World!")
        self.assertEqual(result, "Hello, World!")

    def test_execute_with_invalid_command(self):
        result = self.executor.execute("invalid_command")
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()