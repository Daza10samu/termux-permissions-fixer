#! /data/data/com.termux/files/usr/bin/python3

# Если у вас не установлен python или Termux вообще лежит, то вручную с другого терминала
# su -c chown -R $(whoami):$(whoami) /data/data/com.termux/
# su -c /system/bin/ls -alZ $(maketmp)
# Тут ищем подобный фрагмент (u:object_r:app_data_file:s0:cX,cY) и копируем его
# su -c chcon -R u:object_r:app_data_file:s0:cX,cY /data/data/com.termux/

from os import getuid, popen, chmod
from re import findall
from subprocess import 


script_path = '/data/data/com.termux/files/usr/bin/termux-fix-permissions'
writer = open(script_path, 'w')
uname = getuid()
fix_user_part = f'''#! /system/bin/sh
su -c chown -R {uname}:{uname} /data/data/com.termux/'''
try:
    tmp_file_name = popen('mktemp').read()
    tmp_file_info = popen(f'su -c /system/bin/ls -Z {tmp_file_name}').read()
    selinux_context = findall(r'u:object_r:app_data_file:s0:[^ ]+',
                              tmp_file_info)[0]
    fix_selinux_part = f'\nsu -c chcon -R {selinux_context} /data/data/com.termux/'
    writer.write(fix_user_part + fix_selinux_part)
except IndexError:
    writer.write(fix_user_part)
writer.close()
chmod(script_path, 0o700)
print(f'Теперь вы, скорей всего, можете восстанавливать права для Termux, запустив файл {script_path}')