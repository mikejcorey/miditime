It's MIDITime!
=======================

Do you have time time series data you want to play as music? Of course you do!

MIDITime converts any kind of time series data into pitch, attack and duration values based on musical options that you set up, then outputs a .mid file.

MIDI files aren't technically audio -- they're instructions on how software instruments should be played. You can either play .mid files directly in some music applications, or import them into a wide variety of music editors (like ProTools, Ableton, MaxMSP) and add a ton of bells and whistles to get broadcast-ready audio.

We used MIDITime to produce the data sonification in [this episode of Reveal](https://www.revealnews.org/episodes/power-struggle-the-perilous-price-of-americas-energy-boom/#segment-oklahomas-man-made-earthquakes). The musical track -- without the talking -- [is here](https://www.revealnews.org/article/listen-to-the-music-of-seismic-activity-in-oklahoma/).

Installing
----------

```python
pip install miditime
```

Usage
----------

### Very basic:
```python
from miditime.miditime import MIDITime

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

### A little more fun, a lot more control:

Instantiate the class with a tempo (120bpm is the default), an output file destination,  the number of seconds you want to represent a year in the final song (default is 5 sec/year), the base octave (C5 is middle C, so the default is 5, and how many octaves you want your output to range over (default is 1).

```python
from miditime.miditime import MIDITime
mymidi = MIDITime(120, 'myfile.mid', 5, 5, 1)
```

Bring in some data (this is some earthquakes). I'm assuming your data is already in date order, from oldest to newest.
```python
my_data = [
    {'event_date': <datetime object>, 'magnitude': 3.4},
    {'event_date': <datetime object>, 'magnitude': 3.2},
    {'event_date': <datetime object>, 'magnitude': 3.6},
    {'event_date': <datetime object>, 'magnitude': 3.0},
    {'event_date': <datetime object>, 'magnitude': 5.6},
    {'event_date': <datetime object>, 'magnitude': 4.0}
]
```

Convert your date/time data into an integer, like days since the epoch (Jan. 1, 1970). You can use the days_since_epoch() helper method, or not:

```python
my_data_epoched = [{'days_since_epoch': mymidi.days_since_epoch(d['event_date']), 'magnitude': d['magnitude']} for d in my_data]
```

Convert your integer date/time to something reasonable for a song. For example, at 120 beats per minute, you'll need to scale the data down a lot to avoid a very long song if your data spans years. This uses the seconds_per_year attribute you set at the top, so if your date is converted to something other than days you may need to do your own conversion. But if your dataset spans years and your dates are in days (with fractions is fine), use the beat() helper method.

```python
my_data_timed = [{'beat': mymidi.beat(d['days_since_epoch']), 'magnitude': d['magnitude']} for d in my_data_epoched]
```

Get the earliest date in your series so you can set that to 0 in the MIDI:

```python
start_time = my_data_timed[0]['beat']
```

Set up some functions to scale your other variable (magnitude in our case) to match your desired mode/key and octave range. There are helper methods to assist this scaling, very similar to a charting library like D3. You can choose a linear or logarithmic scale.

```python
def mag_to_pitch_tuned(magnitude):
    # Where does this data point sit in the domain of your data? (I.E. the min magnitude is 3, the max in 5.6). In this case the optional 'True' means the scale is reversed, so the highest value will return the lowest percentage.
    scale_pct = mymidi.linear_scale_pct(3, 5.7, magnitude)

    # Another option: Linear scale, reverse order
    # scale_pct = mymidi.linear_scale_pct(3, 5.7, magnitude, True)

    # Another option: Logarithmic scale, reverse order
    # scale_pct = mymidi.log_scale_pct(3, 5.7, magnitude, True)

    # Pick a range of notes. This allows you to play in a key.
    c_major = ['C', 'D', 'E', 'F', 'G', 'A', 'B']

    #Find the note that matches your data point
    note = mymidi.scale_to_note(scale_pct, c_major)

    #Translate that note to a MIDI pitch
    midi_pitch = mymidi.note_to_midi_pitch(note)

    return midi_pitch
```

Now build your note list

```python
note_list = []

for d in my_data_timed:
    note_list.append([
        d['beat'] - start_time,
        mag_to_pitch_tuned(d['magnitude']),
        100,  # attack
        1  # duration, in beats
    ])
```

And finish

```python
# Add a track with those notes
mymidi.add_track(note_list)

# Output the .mid file
mymidi.save_midi()

```

### Play your music:
There are many programs to work with MIDI, but [timidity](http://sourceforge.net/projects/timidity/) (installable with apt) is a simple command-line one if you just want to hear what you hath wrought.

```
timidity mymidifilename.mid
```

License
----------

This software is released under an MIT license. It would be awful nice if you credited Reveal and Michael Corey somehow if you use this to make something awesome.

Credits
----------

Many thanks to Julia Smith for helping me to understand musical keys/modes better.

MIDITime is a wrapper around the actual midi-making hotness of [midiutil](https://github.com/duggan/midiutil), produced by [Mark Conway Wirt](http://www.emergentmusics.org/site-information). I have included midiutil in this package [per his recommendation](https://github.com/duggan/midiutil/blob/master/README.txt).
