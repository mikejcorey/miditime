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

Using
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

License
----------

This software is released under an MIT license. It would be awful nice if you credited Reveal and Michael Corey somehow if you use this to make something awesome.

Credits
----------

MIDITime is a wrapper around the actual midi-making hotness of [midiutil](https://github.com/duggan/midiutil), produced by [Ross Duggan](https://github.com/duggan). I have included midiutil in this package [per his recommendation](https://github.com/duggan/midiutil/blob/master/README.txt).

