
#-----------------------------------------------------------------------------
# Name:        makemidi.py
# Purpose:     Convert time-series data to a .mid file.
#
# Author:      Michael Corey <mcorey) at (cironline . org>
#
# Created:     2015/05/12
# Copyright:   (c) 2015 Michael Corey
# License:     Please see README for the terms under which this
#              software is distributed.
#-----------------------------------------------------------------------------

import datetime
from midiutil.MidiFile import MIDIFile


class MIDITime(object):

    def __init__(self, tempo=120, outfile='miditime.mid', seconds_per_year=5, base_octave=5, octave_range=1):
        self.tempo = tempo
        self.outfile = outfile
        self.tracks = []
        self.epoch = datetime.datetime(1970, 1, 1)
        self.seconds_per_year = seconds_per_year
        self.base_octave = base_octave
        self.octave_range = octave_range
        self.note_chart = [["C"], ["C#", "Db"], ["D"], ["D#", "Eb"], ["E"], ["F"], ["F#", "Gb"], ["G"], ["G#", "Ab"], ["A"], ["A#", "Bb"], ["B"]]

    def beat(self, numdays):
        beats_per_second = self.tempo/60.0
        beats_per_datayear = self.seconds_per_year*beats_per_second
        beats_per_dataday = beats_per_datayear/365.25

        return round(beats_per_dataday*numdays, 2)

    def check_tz(self, input):
        if input.tzinfo:
            return input.tzinfo
        else:
            return None

    # Match the compare date to the timezone of whatever your input date is, if the input datetime is timezone-aware
    def normalize_datetime(self, input, compare_date):
        # if input is date, make epoch a date
        if type(input) is datetime.date:
            return compare_date.date()
        # # First, coerce to datetime in case it's a date
        # if type(input) is datetime.date:
        #     input = datetime.datetime.combine(input, datetime.datetime.min.time())

        # If tz data present, make epoch tz-aware
        tz = self.check_tz(input)
        if tz:
            return tz.localize(compare_date)
        else:
            return compare_date

    def days_since_epoch(self, input):
        normalized_epoch = self.normalize_datetime(input, self.epoch)
        return (input - normalized_epoch).total_seconds()/60/60/24  # How many days, with fractions

    def scale_to_note_classic(self, scale_pct, mode):  # Only works in multi-octave mode if in C Major (i.e. all the notes are used. Should not be used in other keys, unless octave range is 1.)
            full_mode = []
            n = 0
            while n < self.octave_range:
                for m in mode:
                    current_octave = str(self.base_octave + (n*1))
                    full_mode.append(m + current_octave)
                n += 1
            index = int(scale_pct*float(len(full_mode)))
            if index >= len(full_mode):
                index = len(full_mode) - 1
            print full_mode[index]
            return full_mode[index]

    def scale_to_note(self, scale_pct, mode):  # Manually go through notes so it doesn't inaccurately jump an octave sometimes.
        # First, write out a list of the possible notes for your octave range (i.e. all of the notes on the keyboard)
        full_c_haystack = []
        n = 0
        while n < self.octave_range:
            for note_group in self.note_chart:
                out_group = []
                for note in note_group:
                    current_octave = self.base_octave + (n*1)
                    out_group.append(note + str(current_octave))
                full_c_haystack.append(out_group)
            n += 1

        full_mode = []
        n = 0
        while n < self.octave_range:
            for note in mode:
                note_found = False
                note_key = None
                for groupkey, group in enumerate(full_c_haystack):
                    for gnote in group:
                        if gnote[:-1] == note:
                            full_mode.append(gnote)
                            note_found = True
                            note_key = groupkey
                    if note_found:
                        break
                full_c_haystack = full_c_haystack[note_key:]
            n += 1

        # Now run through your specified mode and pick the exact notes in those octaves
        index = int(scale_pct*float(len(full_mode)))
        if index >= len(full_mode):
            index = len(full_mode) - 1

        return full_mode[index]

    def note_to_midi_pitch(self, notename):
        midinum = 0
        letter = notename[:-1]
        octave = notename[-1]

        i = 0
        for note in self.note_chart:
            for form in note:
                if letter == form:
                    midinum = i
                    break
            i += 1
        midinum += (int(octave))*12
        return midinum

    def linear_scale_pct(self, domain_min, domain_max, input, reverse=False):
        domain_range = domain_max - domain_min
        domain_pct = (input - domain_min)/domain_range

        if reverse:
            domain_pct = 1 - domain_pct
        return domain_pct

    def log_scale_pct(self, domain_min, domain_max, input, reverse=False):
        min_log_domain = pow(10, domain_min)
        max_log_domain = pow(10, domain_max)
        domain_range = max_log_domain - min_log_domain

        log_input = pow(10, input)
        domain_pct = (log_input - min_log_domain)/domain_range

        if reverse:
            domain_pct = 1 - domain_pct
        return domain_pct

    def scale(self, range_min, range_max, input_pct):
        scale_range = range_max - range_min
        return range_min + (input_pct*scale_range)

    def add_track(self, note_list):
        self.tracks.append(note_list)

    def add_note(self, track, channel, note):
        time = note[0]
        pitch = note[1]
        volume = note[2]
        duration = note[3]

        print pitch, time, duration, volume

        # Now add the note.
        self.MIDIFile.addNote(track, channel, pitch, time, duration, volume)

    def save_midi(self):
        # Create the MIDIFile Object with 1 track
        self.MIDIFile = MIDIFile(len(self.tracks))

        for i, note_list in enumerate(self.tracks):

            # Tracks are numbered from zero. Times are measured in beats.
            track = i
            time = 0
            channel = 0

            # Add track name and tempo.
            self.MIDIFile.addTrackName(track, time, "Track 1")
            self.MIDIFile.addTempo(track, time, self.tempo)

            for n in note_list:
                self.add_note(track, channel, n)

        # And write it to disk.
        binfile = open(self.outfile, 'wb')
        self.MIDIFile.writeFile(binfile)
        binfile.close()
