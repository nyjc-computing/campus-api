# Unit tests for the parser
import unittest
from cli.parser import CLIParser

class TestCLIParser(unittest.TestCase):
    def test_parse(self):
        parser = CLIParser()
        args = parser.parse(['--option', 'value'])
        self.assertEqual(args.option, 'value')

if __name__ == '__main__':
    unittest.main()