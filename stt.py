import argparse
import queue
import sys
import os

import sounddevice as sd

from twitch_chat_irc import twitch_chat_irc
from vosk import Model, KaldiRecognizer

parser = argparse.ArgumentParser(add_help=False)

raw_mic_q = queue.Queue()
write_q = queue.Queue()


def twitch_send_message(message):
    if is_testing:
        print(message)
    else:
        twitch_connection.send(channel, message)


def handle_raw_mic_q():
    data = raw_mic_q.get()
    if rec.AcceptWaveform(data):
        res = rec.Result()
        temp = res.split("\n")
        for t in temp:
            if t.find("text") != -1:
                text = t.split(" : ")[-1][1:-1]
                if text != "" and text != '""':
                    write_q.put(text)


def handle_write_q():
    if not write_q.empty():
        message = write_q.get()
        twitch_send_message(message)


def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    raw_mic_q.put(bytes(indata))


is_testing = input("Mic test? (no output to twitch) [y/N]: ").lower()
is_testing = is_testing == "y"

if not is_testing:
    username = ""
    oauth = ""

    key_usage = input("Use key.txt? [Y/n/s]: ").lower()
    specific_key = key_usage == "s"
    standard_key = (key_usage == "") or (key_usage == "y")

    if specific_key or standard_key:
        try:
            if getattr(sys, "frozen", False):
                app_path = os.path.dirname(sys.executable)
            else:
                app_path = os.path.dirname(__file__)

            key = "key.txt"
            if specific_key:
                key = input("Key-file: ")

            with open(os.path.join(app_path, key)) as file:
                lines = [line.rstrip() for line in file]
                username = lines[0]
                oauth = lines[1]
        except Exception as e:
            print(e)
            parser.exit(0)
    else:
        username = input("Username: ")
        oauth = input("OAuth: ")

    print("\n" + "#" * 80 + "\n")

    channel = input("Channel: ")

    twitch_connection = twitch_chat_irc.TwitchChatIRC(username, oauth)

print("\n" + "#" * 80 + "\n")

try:
    device = None
    device_info = sd.query_devices(device, "input")
    samplerate = int(device_info["default_samplerate"])

    model = Model(lang="ru")

    print("\n" + "#" * 80 + "\n")

    with sd.RawInputStream(
        samplerate=samplerate,
        blocksize=8000,
        device=device,
        dtype="int16",
        channels=1,
        callback=callback,
    ):
        rec = KaldiRecognizer(model, samplerate)

        while True:
            handle_raw_mic_q()
            handle_write_q()

except KeyboardInterrupt:
    print("\nDone")
    parser.exit(0)
except Exception as e:
    parser.exit(type(e).__name__ + ": " + str(e))
