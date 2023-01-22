import subprocess

audio_player_command_name='mpg123'
str(subprocess.check_output("ps aux | grep "+audio_player_command_name,shell=True))
byte_obj = subprocess.check_output("ps aux | grep "+audio_player_command_name,shell=True)
byte_obj

processes = subprocess.check_output("ps aux | grep "+audio_player_command_name,shell=True).decode('utf-8')
processes_lst = processes.split('\n')
for processes in processes_lst:
    print(processes)
if len(processes_lst) > 3:
    print(processes_lst[0].split()[11:])