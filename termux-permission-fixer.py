#! /data/data/com.termux/files/usr/bin/python3

# Если у вас не установлен python или Termux вообще лежит, то вручную с другого терминала
# su -c chown -R $(whoami):$(whoami) /data/data/com.termux/
# su -c /system/bin/ls -alZ $(maketmp)
# Тут ищем подобный фрагмент (u:object_r:app_data_file:s0:cX,cY) и копируем его
# su -c chcon -R u:object_r:app_data_file:s0:cX,cY /data/data/com.termux/

from os import getuid, popen, chmod
from re import findall
from subprocess import run, PIPE
termux_path = '/data/data/com.termux'

def restorecon_checker():
    checker = run(['su', '-c', 'restorecon -RF '+termux_path], stdout=PIPE)
    if checker.returncode:
        return 0
    else: 
        return 1


def tmp_file_info_finder():
    tmp_file_name = popen('mktemp').read()
    file_info_getter = run(f'su -c /system/bin/ls -Z {tmp_file_name}'.split(), stdout=PIPE)
    if file_info_getter.returncode:
        return 0
    return file_info_getter.stdout.read()


script_path = f'{termux_path}/files/usr/bin/termux-fix-permissions'
writer = open(script_path, 'w')
uname = getuid()
fix_user_part = f'''#! /system/bin/sh
su -c chown -R {uname}:{uname} {termux_path}/'''
restorecoc_command = f'\nsu -c restorecon -RF {termux_path}'
if restorecon_checker():
    writer.write(fix_user_part+restorecoc_command)
else:
    tmp_file_info = tmp_file_info_finder()
    if not tmp_file_info:
        writer.write(fix_user_part)
    else:
        selinux_context = findall(r'u:object_r:app_data_file:s0:[^ ]+',
                                tmp_file_info)[0]
        fix_selinux_part = f'\nsu -c chcon -R {selinux_context} {termux_path}/'
        writer.write(fix_user_part + fix_selinux_part)
writer.close()
chmod(script_path, 0o700)
print(f'Теперь вы, скорей всего, можете восстанавливать права для Termux, запустив файл {script_path}')