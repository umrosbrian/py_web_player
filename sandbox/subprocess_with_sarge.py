from sarge import Command, Capture
from subprocess import PIPE


p = Command('mpg123 --remote', stdout=Capture(buffer_size=1))
p.run(input=PIPE, async_=True)
p.stdin.write('load /Users/rosbrian/Music/Music/Media.localized/Music/Adams,\ Ryan/ra\ 2005-06-03/02\ Let\ It\ Ride.mp3\n')

"""
LP /Users/rosbrian/Music/Music/Media.localized/Music/Adams, Ryan/ra 2005-06-03/01 Easy Plateau.mp3
LOAD /Users/rosbrian/Music/Music/Media.localized/Music/Adams, Ryan/ra 2005-06-03/10_The_Rescue_Blues.mp3


01 Easy Plateau.mp3					08 Shakedown On 9th Street.mp3				16 Beautiful Sorta.mp3					23 Rosebud.mp3
02 Let It Ride.mp3					09_New_York_New_York.mp3				17 Nightbirds.mp3					24 Harder Now That It's Over.mp3
03 Mockingbird.mp3					10_The_Rescue_Blues.mp3					18 Trains.mp3						25 I See Monsters.mp3
04 What Sin.mp3						11_Why_Do_They_Leave.mp3				19 Magnolia Mountain.mp3				26 My Winding Wheel.mp3
05 A Kiss Before I Go.mp3				12_She_Wants.mp3					20 Dance All Night.mp3					27 Come Pick Me Up.mp3
06 To Be Young (Is To Be Sad, Is To Be High).mp3	13 When the Stars Go Blue (aborted).mp3			21 When the Stars Go Blue.mp3				28 Love Is Hell.mp3
07 Please Do Not Let Me Go.mp3				14 Bird Song.mp3"""

"""
Got this by hitting h + enter while playing in remote mode:
@H {
@H HELP/H: command listing (LONG/SHORT forms), command case insensitve
@H LOAD/L <trackname>: load and start playing resource <trackname>
@H LOADPAUSED/LP <trackname>: load but do not start playing resource <trackname>
@H LOADLIST/LL <entry> <url>: load a playlist from given <url>, and display its entries, optionally load and play one of these specificed by the integer <entry> (<0: just list, 0: play last track, >0:play track with that position in list)
@H PAUSE/P: pause playback
@H STOP/S: stop playback (closes file)
@H JUMP/J <frame>|<+offset>|<-offset>|<[+|-]seconds>s: jump to mpeg frame <frame> or change position by offset, same in seconds if number followed by "s"
@H VOLUME/V <percent>: set volume in (0..100...); float value
@H MUTE: turn on software mute in output
@H UNMUTE: turn off software mute in output
@H RVA off|(mix|radio)|(album|audiophile): set rva mode
@H EQ/E <channel> <band> <value>: set equalizer value for frequency band 0 to 31 on channel 1 (left) or 2 (right) or 3 (both)
@H EQFILE <filename>: load EQ settings from a file
@H SHOWEQ: show all equalizer settings (as <channel> <band> <value> lines in a SHOWEQ block (like TAG))
@H SEEK/K <sample>|<+offset>|<-offset>: jump to output sample position <samples> or change position by offset
@H SCAN: scan through the file, building seek index
@H SAMPLE: print out the sample position and total number of samples
@H FORMAT: print out sampling rate in Hz and channel count
@H SEQ <bass> <mid> <treble>: simple eq setting...
@H PITCH <[+|-]value>: adjust playback speed (+0.01 is 1 % faster)
@H SILENCE: be silent during playback (no progress info, opposite of PROGRESS)
@H PROGRESS: turn on progress display (opposite of SILENCE)
@H STATE: Print auxiliary state info in several lines (just try it to see what info is there).
@H TAG/T: Print all available (ID3) tag info, for ID3v2 that gives output of all collected text fields, using the ID3v2.3/4 4-character names. NOTE: ID3v2 data will be deleted on non-forward seeks.
@H    The output is multiple lines, begin marked by "@T {", end by "@T }".
@H    ID3v1 data is like in the @I info lines (see below), just with "@T" in front.
@H    An ID3v2 data field is introduced via ([ ... ] means optional):
@H     @T ID3v2.<NAME>[ [lang(<LANG>)] desc(<description>)]:
@H    The lines of data follow with "=" prefixed:
@H     @T =<one line of content in UTF-8 encoding>
@H meaning of the @S stream info:
@H S <mpeg-version> <layer> <sampling freq> <mode(stereo/mono/...)> <mode_ext> <framesize> <stereo> <copyright> <error_protected> <emphasis> <bitrate> <extension> <vbr(0/1=yes/no)>
@H The @I lines after loading a track give some ID3 info, the format:
@H      @I ID3:artist  album  year  comment genretext
@H     where artist,album and comment are exactly 30 characters each, year is 4 characters, genre text unspecified.
@H     You will encounter "@I ID3.genre:<number>" and "@I ID3.track:<number>".
@H     Then, there is an excerpt of ID3v2 info in the structure
@H      @I ID3v2.title:Blabla bla Bla
@H     for every line of the "title" data field. Likewise for other fields (author, album, etc)."""

# Make a playlist for testing.
import os

playlist_path = '/Users/rosbrian/PycharmProjects/py_web_player/sandbox/playlist.txt'
dir = '/Users/rosbrian/Music/Music/Media.localized/Music/Creedence Clearwater Revival/The Concert'
os.chdir(dir)
with open(playlist_path, 'w') as f:
    for file_name in os.listdir(dir):
        file_path = os.path.join(dir, file_name)
        f.write(f"{file_path}\n")
        print(file_path)
