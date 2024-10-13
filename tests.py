import unittest
import datetime
import pytz
from miditime.miditime import MIDITime


class TrackTests(unittest.TestCase):
    def test2Tracks(self):
        m = MIDITime()

        track_1_program = 0
        track_1_notes = [
            [0, 60, 127, 3],  #At 0 beats (the start), Middle C with velocity 127, for 3 beats
            [10, 61, 127, 4]  #At 10 beats (12 seconds from start), C#5 with velocity 127, for 4 beats
        ]
        m.add_track(track_1_notes, track_1_program)
        
        track_2_program = 16
        track_2_notes = [
            [5, 50, 127, 3],  #At 0 beats (the start), C4 with velocity 127, for 3 beats
            [12, 51, 127, 4]  #At 10 beats (12 seconds from start), C#4 with velocity 127, for 4 beats
        ]
        m.add_track(track_2_notes, track_2_program)

        out_midi_obj = m.save_midi()

        self.assertEqual(len(m.tracks), 2)
        self.assertEqual(out_midi_obj.numTracks, 2)


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


class DemoTest(unittest.TestCase):
    def test_basic_example(self):
        # from miditime.miditime import MIDITime

        # Instantiate the class with a tempo (120bpm is the default) and an output file destination.
        mymidi = MIDITime(120, 'myfile.mid')

        # Create a list of notes. Each note is a list: [time, pitch, velocity, duration]
        midinotes = [
            [0, 60, 127, 3],  #At 0 beats (the start), Middle C with velocity 127, for 3 beats
            [10, 61, 127, 4]  #At 10 beats (12 seconds from start), C#5 with velocity 127, for 4 beats
        ]

        # Add a track with those notes
        mymidi.add_track(midinotes)

        # Output the .mid file
        mymidi.save_midi()


def main():
    unittest.main()

if __name__ == '__main__':
    main()
