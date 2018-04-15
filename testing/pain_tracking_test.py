import unittest
from pain_tracking_app.main import MultipleScreenApp


class MyTestCase(unittest.TestCase):
    def test_open_medication_entry_screen(self):
        screen = self.root.current = 'first'
        MultipleScreenApp.open_medication_entry_screen(screen)
        self.assertEqual(self.root.current, 'third')


if __name__ == '__main__':
    unittest.main()
