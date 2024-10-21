from miditime.MIDITime import MIDITime

def testSimpleMode0():
    m = MIDITime(base_octave=5, octave_range=3)
    pct = m.linear_scale_pct(0, 5.7, 0, reverse=False)
    assert m.scale_to_note(pct, ['C', 'D', 'E', 'F', 'G', 'A', 'B']) == 'C5'

def testSimpleMode70():
    m = MIDITime(base_octave=5, octave_range=3)
    pct = m.linear_scale_pct(0, 5.7, 4.0, reverse=False)
    assert m.scale_to_note(pct, ['C', 'D', 'E', 'F', 'G', 'A', 'B']) == 'C7'

def testSimpleMode100():
    m = MIDITime(base_octave=5, octave_range=3)
    pct = m.linear_scale_pct(0, 5.7, 5.7, reverse=False)
    assert m.scale_to_note(pct, ['C', 'D', 'E', 'F', 'G', 'A', 'B']) == 'B7'

def testComplexMode0():
    m = MIDITime(base_octave=5, octave_range=3)
    pct = m.linear_scale_pct(0, 5.7, 0, reverse=False)
    assert m.scale_to_note(pct, ['D', 'E', 'F', 'G', 'A', 'Bb', 'C']) == 'D5'

def testComplexMode70():
    m = MIDITime(base_octave=5, octave_range=3)
    pct = m.linear_scale_pct(0, 5.7, 4.0, reverse=False)
    assert m.scale_to_note(pct, ['D', 'E', 'F', 'G', 'A', 'Bb', 'C']) == 'D7'

def testComplexMode100():
    m = MIDITime(base_octave=5, octave_range=3)
    pct = m.linear_scale_pct(0, 5.7, 5.7, reverse=False)
    assert m.scale_to_note(pct, ['D', 'E', 'F', 'G', 'A', 'Bb', 'C']) == 'Bb7'