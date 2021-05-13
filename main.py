class WindowsInhibitor:
    '''Prevent OS sleep/hibernate in windows; code from:
    https://github.com/h3llrais3r/Deluge-PreventSuspendPlus/blob/master/preventsuspendplus/core.py
    API documentation:
    https://msdn.microsoft.com/en-us/library/windows/desktop/aa373208(v=vs.85).aspx'''
    ES_CONTINUOUS = 0x80000000
    ES_SYSTEM_REQUIRED = 0x00000001

    def __init__(self):
        pass

    def inhibit(self):
        import ctypes
        print("Preventing Windows from going to sleep")
        ctypes.windll.kernel32.SetThreadExecutionState(
            WindowsInhibitor.ES_CONTINUOUS | \
            WindowsInhibitor.ES_SYSTEM_REQUIRED)

    def uninhibit(self):
        import ctypes
        print("Allowing Windows to go to sleep")
        ctypes.windll.kernel32.SetThreadExecutionState(
            WindowsInhibitor.ES_CONTINUOUS)


# coding=utf-8
import pyglet
import schedule
import time
import os
import datetime

osSleep = None
# in Windows, prevent the OS from sleeping while we run
if os.name == 'nt':
    osSleep = WindowsInhibitor()
    osSleep.inhibit()

print("Песни должны лежать в каталоге: C:\Music")

songs = []

for cur_path, directories, files in os.walk("C:\\Music"):
    songs = files

sound = []
for song in songs:
    sound.append(pyglet.media.load('C:\Music\\' + song, streaming=False))

number_of_songs = len(songs)


print("Введите начало воспроизведения: (например 09:00 или 23:00)")
time_begin = input()
hour_begin_str, minutes_begin_str = time_begin.split(':')

hour_begin, minutes_begin = int(hour_begin_str), int(minutes_begin_str)


print("Введите конец воспроизведения: (например 09:00 или 23:00)")
time_end = input()
hour_end_str, minutes_end_str = time_end.split(':')

hour_end, minutes_end = int(hour_end_str), int(minutes_end_str)


iter = 0

def play_sound(dt):
    global iter
    sound[iter].play()
    pyglet.clock.schedule_once(play_sound, sound[iter].duration)
    iter = (iter + 1) % number_of_songs


def exit(dt):
    pyglet.clock.unschedule(play_sound)
    pyglet.app.exit()


def begin():
    global iter

    iter = (iter + 1) % number_of_songs

    sound[0].play()
    pyglet.clock.schedule_once(play_sound, sound[0].duration)

    pyglet.clock.schedule_once(exit, (hour_end - hour_begin)*60*60 + (minutes_end - minutes_begin)*60)
    pyglet.app.run()


schedule.every().day.at(time_begin).do(begin)

try:
    while True:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    if osSleep:
        osSleep.uninhibit()
