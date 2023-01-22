from flask import request,render_template
import os
import subprocess
from py_web_player import app
import logging
import datetime as dt


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
# root_dir = '/Volumes'
root_dir = '/media/8TB/mp3'
logging.debug(f"Issuing os.chdir({root_dir})")
os.chdir(root_dir)
currently_playing_file_name = None
audio_player_command_name = 'mpg123'
playlist_file_aps_lst = []
dir_aps_from_request = root_dir


def get_aps_of_file_being_played(audio_player_command_name):
    """Get the file's aps from the process.  Don't know why mp3_file_aps_from_request isn't being used.  We already
    know the file_aps from that.  The only time they'd differ is when the app is started while there's already a
    file being played."""
    processes = subprocess.check_output("ps aux | grep " + audio_player_command_name, shell=True).decode('utf-8')
    processes_lst = processes.split('\n')
    if len(processes_lst) > 3:
        currently_playing = processes_lst[0].split()[11:]
        logging.debug(f"currently_playing: {currently_playing}")
        return currently_playing


@app.route('/')
def index():
    global currently_playing_file_name
    global playlist_file_aps_lst
    global dir_aps_from_request
    global root_dir
    global last_dir_aps

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
    # if request.args.get('dir_aps') and os.path.isdir(request.args.get('dir_aps')):
        # dir_aps_from_request = request.args.get('dir_aps')
    # logging.debug(f"dir_aps_from_request: {dir_aps_from_request}")
    if request.args.get('cd_to_parent'):
        logging.debug('CDing to parent')
        os.chdir(os.pardir)
        dir_aps_from_request = os.getcwd()
        logging.debug(f"CWD is now {dir_aps_from_request}")

    # Figure out if anything is currently being played.
    number_of_mpg123_processes = subprocess.check_output('ps aux | grep mpg123  | wc -l', shell=True)
    mp3_file_names_in_dir_from_request = []
    dir_names_in_dir_from_request = []
    if number_of_mpg123_processes == 1 :
        currently_playing_file_aps = None
    else:
        # Because this is re-issuing pretty much the same subprocess command, I could change the one above and \
        # blow away the function since it's redundant.
        currently_playing_file_aps = get_aps_of_file_being_played(audio_player_command_name)
        logging.debug(f"currently_playing_file_name: {currently_playing_file_name}")

    # Find out what's in the dir.
    # Don't even check if the variable's value has changed.  An inspection of the directory occurs upon each GET. \
    # This isn't great but that's why using a database vs. trawling the file system is ideal.
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
        logging.debug(f"mp3_file_aps_from_request: {mp3_file_name_to_play_from_request}")
        os.system("killall mpg123" )  # stop the currently playing file
        mp3_file_aps = os.path.join(dir_aps_from_request, mp3_file_name_to_play_from_request)
        os.system(f"{audio_player_command_name} -v \"{mp3_file_aps}\"")
        os.system(audio_player_command_name +' "'+ mp3_file_aps+'" &')
    if request.args.get('command'):
        command_from_request = request.args.get('command')
        logging.debug(f"cmd: {command_from_request}")
        if command_from_request == 'stop':  # I could pass other commands to control mpg123.
            os.system("killall mpg123" )
            currently_playing_file_name =  None
        elif command_from_request == 'play_all_files':
            os.system('killall mpg123')
            os.system(f"{audio_player_command_name} -v \"{dir_aps_from_request}\"/*\.mp3")

    return render_template('views.html', currently_playing_file_name = currently_playing_file_name, dir_aps_from_request = dir_aps_from_request, dir_names_in_dir_from_request = dir_names_in_dir_from_request, mp3_file_names_in_dir_from_request = mp3_file_names_in_dir_from_request)
