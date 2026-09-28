import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
from sovereign_core.engine import SovereignChatEngine


class TestSovereignChat(unittest.TestCase):
    def test_mode_architect(self):
        e = SovereignChatEngine()
        r = e.chat("Build a complete AI system architecture for my company")
        self.assertEqual(r["mode"], "architect")

    def test_mode_sovereign(self):
        e = SovereignChatEngine()
        r = e.chat("Give me the full strength unprecedented response")
        self.assertEqual(r["mode"], "sovereign")

    def test_memory_extraction(self):
        e = SovereignChatEngine()
        e.chat("My name is Garrett and I have built the full AI system")
        self.assertTrue(any("Garrett" in m for m in e.memories))

    def test_intensity_scales(self):
        e = SovereignChatEngine()
        a = e.chat("Hi")
        b = e.chat("This is a detailed strategic question about building unprecedented AI business systems for maximum leverage and wealth generation")
        self.assertGreater(b["intensity"], a["intensity"])

    def test_multiple_turns(self):
        e = SovereignChatEngine()
        e.chat("I want to build an AI company")
        r = e.chat("What is the best strategy")
        self.assertIn("mode", r)
        self.assertIn("answer", r)
        self.assertGreater(len(r["answer"]), 20)

    def test_offer_attached(self):
        e = SovereignChatEngine()
        r = e.chat("Build a revenue system")
        self.assertIn("offer", r)
        self.assertEqual(r["offer"]["price"], 47)

    def test_reset(self):
        e = SovereignChatEngine()
        e.chat("My name is Garrett Wayne")
        e.reset()
        self.assertEqual(e.memories, [])
        self.assertEqual(e.mode, "architect")


if __name__ == "__main__":
    unittest.main()
