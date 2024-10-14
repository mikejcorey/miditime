import os
from src.miditime.MIDITime import MIDITime


def test_basic_example():
    os.makedirs('tests/test_exports', exist_ok=True)

    # from miditime.MIDITime import MIDITime

    # Instantiate the class with a tempo (120bpm is the default) and an output file destination.
    mymidi = MIDITime(120, 'tests/test_exports/demo.mid')

    # Create a list of notes. Each note is a list: [time, pitch, velocity, duration]
    midinotes = [
        [0, 60, 127, 3],  #At 0 beats (the start), Middle C with velocity 127, for 3 beats
        [10, 61, 127, 4]  #At 10 beats (12 seconds from start), C#5 with velocity 127, for 4 beats
    ]

    # Add a track with those notes
    mymidi.add_track(midinotes)

    # Output the .mid file
    mymidi.save_midi()