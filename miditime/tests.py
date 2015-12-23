import unittest
import datetime
import pytz
from MIDITime import MIDITime


class DateTest(unittest.TestCase):
    def testDatetimeNaive(self):
        m = MIDITime()
        dt = datetime.datetime.strptime('1970-01-01', '%Y-%m-%d')
        self.assertEqual(m.days_since_epoch(dt), 0)

    def testDatetimeAware(self):
        m = MIDITime()
        utc = pytz.utc
        dt = utc.localize(datetime.datetime.strptime('1970-01-01', '%Y-%m-%d'))
        self.assertEqual(m.days_since_epoch(dt), 0)

    def testDate(self):
        m = MIDITime()
        dt = datetime.datetime.strptime('1970-01-01', '%Y-%m-%d').date()
        self.assertEqual(m.days_since_epoch(dt), 0)


class OctaveTest(unittest.TestCase):
    def testSimpleMode0(self):
        m = MIDITime(base_octave=5, octave_range=3)
        pct = m.linear_scale_pct(0, 5.7, 0, reverse=False)
        self.assertEqual(m.scale_to_note(pct, ['C', 'D', 'E', 'F', 'G', 'A', 'B']), 'C5')

    def testSimpleMode70(self):
        m = MIDITime(base_octave=5, octave_range=3)
        pct = m.linear_scale_pct(0, 5.7, 4.0, reverse=False)
        self.assertEqual(m.scale_to_note(pct, ['C', 'D', 'E', 'F', 'G', 'A', 'B']), 'C7')

    def testSimpleMode100(self):
        m = MIDITime(base_octave=5, octave_range=3)
        pct = m.linear_scale_pct(0, 5.7, 5.7, reverse=False)
        self.assertEqual(m.scale_to_note(pct, ['C', 'D', 'E', 'F', 'G', 'A', 'B']), 'B7')

    def testComplexMode0(self):
        m = MIDITime(base_octave=5, octave_range=3)
        pct = m.linear_scale_pct(0, 5.7, 0, reverse=False)
        self.assertEqual(m.scale_to_note(pct, ['D', 'E', 'F', 'G', 'A', 'Bb', 'C']), 'D5')

    def testComplexMode70(self):
        m = MIDITime(base_octave=5, octave_range=3)
        pct = m.linear_scale_pct(0, 5.7, 4.0, reverse=False)
        self.assertEqual(m.scale_to_note(pct, ['D', 'E', 'F', 'G', 'A', 'Bb', 'C']), 'D7')

    def testComplexMode100(self):
        m = MIDITime(base_octave=5, octave_range=3)
        pct = m.linear_scale_pct(0, 5.7, 5.7, reverse=False)
        self.assertEqual(m.scale_to_note(pct, ['D', 'E', 'F', 'G', 'A', 'Bb', 'C']), 'Bb7')


def main():
    unittest.main()

if __name__ == '__main__':
    main()
