import os
from miditime.MIDITime import MIDITime

def test2Tracks():
    os.makedirs('tests/test_exports', exist_ok=True)

    m = MIDITime(120, 'tests/test_exports/trackdemo.mid')

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

    assert len(m.tracks) == 2
    assert out_midi_obj.numTracks == 3  # Not sure why it's not 2 but seems fine
    assert m.tracks[1]['program'] == 16