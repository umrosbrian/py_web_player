from flask import request, render_template
import os
import subprocess
from py_web_player import app, turbo
import logging
import datetime as dt
# from mpyg321.MPyg123Player import MPyg123Player
# from sarge import Feeder, run
import pexpect
from threading import Thread
# from turbo_flask import Turbo
import time


def start_logging():
    global logger
    if 'logger' not in globals():
        logger = logging.getLogger()
    else:  # wish there was a logger.close()
        for handler in logger.handlers[:]:  # make a copy of the list
            logger.removeHandler(handler)

    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(fmt='%(levelname)s-%(asctime)s-%(funcName)s - %(message)s', datefmt='%I:%M:%S')

    log_file_aps = os.path.join(os.path.dirname(os.path.dirname(app.root_path)), 'logs',
                                f"{dt.datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    fh = logging.FileHandler(log_file_aps)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    # disable for production
#    sh = logging.StreamHandler(sys.stdout)
#    sh.setFormatter(formatter)
#    logger.addHandler(sh)

start_logging()

# root_dir = os.environ['HOME']+'/Music/Music/Media.localized/Music'
root_dir = '/nas/album_id_dirs'
# root_dir = '/Volumes'
# root_dir = '/media/8TB/mp3'
logging.debug(f"Issuing os.chdir({root_dir})")
os.chdir(root_dir)
currently_playing_file_aps = None
# audio_player_command_name = 'mpg123'
# player = MPyg123Player()
# feeder = Feeder()
# run(cmd='mpg123 --remote', input=feeder, async_=True)
p = pexpect.spawn('mpg123 --remote', timeout=None)
# p.delaybeforesend = None
playlist_file_aps_lst = []
dir_aps_from_request = root_dir
mpg123_stdout = ''

#def print_mpg123_stdout(process = p):
#    global mpg123_stdout
#
#    while True:
#        mpg123_stdout_bytes = process.readline()
#        mpg123_stdout = mpg123_stdout_bytes.decode('utf-8').strip()
#
#
#Thread(target=print_mpg123_stdout).start()


## -------------------------------------------------------------------------------------------
## Start threads as soon as the server starts to asynchronously push to the widgets.
## -------------------------------------------------------------------------------------------
#@app.context_processor
#def prep_load_dict():
#    """This function will return a dict, which is available to all templates.  To access the values within the
#    templates, you only need to provide the dict's key.  Unused key/values are ignored so that you won't break anything
#     by creating a dict that's too big."""
#
#    return {'mpg123_stdout': mpg123_stdout}
#
#
#def update_load():
#    """Because this function is issued in its own thread, it's ignorant of whatever else is happening.  It simply
#    reloads the contents of the table with the data returned by prep_load_dict() every n seconds. """
#
#    with app.app_context(), app.test_request_context():
#        while True:  # Maybe toggle this on and off as needed?
#            time.sleep(.5)
#            turbo.push(turbo.replace(render_template(template_name_or_list='mpg123_status_widget.html'),
#                                     target='async_table'))
#
#Thread(target=update_load).start()

@app.route('/')
def index():
    global currently_playing_file_aps
    global playlist_file_aps_lst
    global dir_aps_from_request

    # Mount the drive if it's not already mounted.
    #df = commands.getoutput('df -h')
    #if root_dir not in df:
    #    os.system('sudo mount /dev/sda1 '+root_dir)

    # Each link in the view returns a variable.  Therefore, each GET is reassigning one variable and we have to \
    # figure out what to do with it.
    if request.args.get('dir_name'):
        logging.debug(f"request.args.get('dir_name'): {request.args.get('dir_name')}")
        dir_aps_from_request = os.path.join(os.getcwd(), request.args.get('dir_name'))
        logging.debug(f"Issuing os.chdir({dir_aps_from_request})")
        os.chdir(dir_aps_from_request)
    if request.args.get('cd_to_parent'):
        logging.debug('CDing to parent')
        os.chdir(os.pardir)
        dir_aps_from_request = os.getcwd()
        logging.debug(f"CWD is now {dir_aps_from_request}")

    # Find out what's in the dir.
    # Don't even check if the variable's value has changed.  An inspection of the directory occurs upon each GET. \
    # This isn't great but that's why using a database vs. trawling the file system is ideal.
    mp3_file_names_in_dir_from_request = []
    dir_names_in_dir_from_request = []
    items_in_dir_from_request = os.listdir(dir_aps_from_request)
    logging.debug(f"items_in_dir_from_request: {items_in_dir_from_request}")  # items in the CWD
    for item in items_in_dir_from_request:
        if os.path.isdir(dir_aps_from_request + '/' + item):
            dir_names_in_dir_from_request.append(item)
        elif item[-4:] == '.mp3':
            mp3_file_names_in_dir_from_request.append(item)
    logging.debug(f"dir_names_in_dir_from_request: {dir_names_in_dir_from_request}")
    logging.debug(f"mp3_file_names_in_dir_from_request: {mp3_file_names_in_dir_from_request}")
    mp3_file_names_in_dir_from_request.sort()
    dir_names_in_dir_from_request.sort()

    # Play a file that's been clicked on or stop the player.
    if request.args.get('mp3_file_name'):
        mp3_file_name_to_play_from_request = request.args.get('mp3_file_name')
        logging.debug(f"mp3_file_name_to_play_from_request: {mp3_file_name_to_play_from_request}")
        mp3_file_aps = os.path.join(dir_aps_from_request, mp3_file_name_to_play_from_request)
        logging.debug(f"Playing {mp3_file_aps}")
        # player.play_song(path=mp3_file_aps)
        # feeder.feed(f"load {mp3_file_aps}\n")
        p.sendline("LOAD " + mp3_file_aps)
    if request.args.get('command'):
        command_from_request = request.args.get('command')
        logging.debug(f"cmd: {command_from_request}")
        if command_from_request == 'pause':  # I could pass other commands to control mpg123.
            # player.pause()
            # feeder.feed('pause')
            p.sendline('pause')
        elif command_from_request == 'resume':
            # player.resume()
            # feeder.feed('pause')
            p.sendline('pause')
        elif command_from_request == 'fast_forward':
            # player.jump("1s")
            # feeder.feed('jump 2s')
            p.sendline('jump 200')
        elif command_from_request == 'play_all_files':
            # os.system('killall mpg123')
            # os.system(f"{audio_player_command_name} -v \"{dir_aps_from_request}\"/*\.mp3")
            logging.debug(f"Playing {mp3_file_names_in_dir_from_request}")
            for mp3_file_name in mp3_file_names_in_dir_from_request:
                mp3_file_aps = os.path.join(dir_aps_from_request, mp3_file_name)
                logging.debug(f"Playing {mp3_file_aps}")
                # player.play_song(path=mp3_file_aps)
                # feeder.feed(f"load \"{mp3_file_aps}\"")
                p.sendline(f"load {mp3_file_aps}")
                logging.debug("Moving on to the next file.")

    return render_template('views.html',
                           currently_playing_file_name = currently_playing_file_aps,
                           dir_aps_from_request = dir_aps_from_request,
                           dir_names_in_dir_from_request = dir_names_in_dir_from_request,
                           mp3_file_names_in_dir_from_request = mp3_file_names_in_dir_from_request)

@app.route('/playlist')
def playlist():
    # Make a list of file paths to pass to a view.
    dir = '/nas/album_id_dirs/10'
    file_lst = []
    for file_name in os.listdir(dir):
        file_lst.append(os.path.join(dir, file_name))
    return render_template(template_name_or_list='playlist.html',  )
