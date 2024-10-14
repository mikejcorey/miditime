import pytz
import datetime

from src.miditime.MIDITime import MIDITime

def testDatetimeNaive():
    m = MIDITime()
    dt = datetime.datetime.strptime('1970-01-01', '%Y-%m-%d')
    assert m.days_since_epoch(dt) == 0

def testDatetimeAware():
    m = MIDITime()
    utc = pytz.utc
    dt = utc.localize(datetime.datetime.strptime('1970-01-01', '%Y-%m-%d'))
    assert m.days_since_epoch(dt) == 0

def testDate():
    m = MIDITime()
    dt = datetime.datetime.strptime('1970-01-01', '%Y-%m-%d').date()
    assert m.days_since_epoch(dt) == 0