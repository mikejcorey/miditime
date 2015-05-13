It's MIDITime!
=======================

Do you have time time series data you want to play as music? Of course you do!

MIDITime converts any kind of time series data into pitch, attack and duration values based on musical options that you set up, then outputs a .mid file.

MIDI files aren't technically audio -- they're instructions on how software instruments should be played. You can either play .mid files directly in some music applications, or import them into a wide variety of music editors (like ProTools, Ableton, MaxMSP) and add a ton of bells and whistles to get broadcast-ready audio.

Installing
----------

```python
pip install miditime
```

Usage
----------

Very basic:
```python
from miditime.MIDITime import MIDITime

# Instantiate the class with a tempo (120bpm is the default) and an output file destination.
mymidi = MIDITime(120, 'myfile.mid')

# Create a list of notes. Each note is a list: [time, pitch, attack, duration]
midinotes = [
    [0, 60, 200, 3],  #At 0 beats (the start), Middle C with attack 200, for 3 beats
    [10, 61, 200, 4]  #At 10 beats (12 seconds from start), C#5 with attack 200, for 4 beats
]

# Add a track with those notes
mymidi.add_track(midinotes)

# Output the .mid file
mymidi.save_midi()

```

A little more fun, a lot more control:
```python
from miditime.MIDITime import MIDITime

# Instantiate the class with a tempo (120bpm is the default) and an output file destination.
mymidi = MIDITime(120, 'myfile.mid')

# Bring in some data (this is some earthquakes)

my_data = [
    {'event_date': '2011-11-05 11:24:15+00:00', 'magnitude': 3.4},
    {'event_date': '2011-11-05 13:42:25+00:00', 'magnitude': 3.2},
    {'event_date': '2011-11-05 14:36:30+00:00', 'magnitude': 3.6},
    {'event_date': '2011-11-06 01:03:58+00:00', 'magnitude': 3.0},
    {'event_date': '2011-11-06 03:53:10+00:00', 'magnitude': 5.6},
    {'event_date': '2011-11-06 04:03:40+00:00', 'magnitude': 4.0}
]

# Create a list of notes. Each note is a list: [time, pitch, attack, duration]
midinotes = [
    [0, 60, 200, 3],  #At 0 beats (the start), Middle C with attack 200, for 3 beats
    [10, 61, 200, 4]  #At 10 beats (12 seconds from start), C#5 with attack 200, for 4 beats
]

# Add a track with those notes
mymidi.add_track(midinotes)

# Output the .mid file
mymidi.save_midi()

```

License
----------

This software is released under an MIT license. It would be awful nice if you credited Reveal and Michael Corey somehow if you use this to make something awesome.

Credits
----------

MIDITime is a wrapper around the actual midi-making hotness of [midiutil](https://github.com/duggan/midiutil), produced by [Ross Duggan](https://github.com/duggan). I have included midiutil in this package [per his recommendation](https://github.com/duggan/midiutil/blob/master/README.txt).

