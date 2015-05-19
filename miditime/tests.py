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


def main():
    unittest.main()

if __name__ == '__main__':
    main()
