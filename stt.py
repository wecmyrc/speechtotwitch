import argparse
import queue
import sys
import os
import datetime
import codecs

import sounddevice as sd

from twitch_chat_irc import twitch_chat_irc
from vosk import Model, KaldiRecognizer

parser = argparse.ArgumentParser(add_help=False)

raw_mic_q = queue.Queue()
write_q = queue.Queue()


def write_log(message):
    try:
        if getattr(sys, "frozen", False):
            app_path = os.path.dirname(sys.executable)
        else:
            app_path = os.path.dirname(__file__)

        with open(os.path.join(app_path, "messages_log.txt"), "a") as file:
            file.write(str(datetime.datetime.now()) + ": " + message + "\n")

    except Exception as e:
        print(e)


def twitch_send_message(message):
    twitch_connection.send(channel, message)


def apply_dict(message):
    message_parts = message.split(" ")

    glued_words = []

    if getattr(sys, "frozen", False):
        app_path = os.path.dirname(sys.executable)
    else:
        app_path = os.path.dirname(__file__)

    with codecs.open(os.path.join(app_path, "dict.txt"), "r", "utf-8") as file:
        for line in file:
            is_glued = line.find("+") != -1

            line_content = line.rstrip().split("=")

            if len(line_content) != 2:
                break

            first = line_content[0]
            second = line_content[1]

            if (
                (first.find("[") == -1)
                or (first.find("]") == -1)
                or (second.find("[") == -1)
                or (second.find("]") == -1)
            ):
                break

            first = first[first.index("[") + 1 : first.index("]")]
            second = second[second.index("[") + 1 : second.index("]")]

            for i in range(len(message_parts)):
                if message_parts[i] == first:
                    message_parts[i] = second

                    if is_glued:
                        glued_words.append(i)

                if len(first.split(" ")) != 0:
                    first_parts = first.split(" ")

                    check = False
                    for j in range(len(first_parts)):
                        if i + j >= len(message_parts):
                            check = True
                            break

                        if message_parts[i + j] != first_parts[j]:
                            check = True
                            break

                    if not check:
                        message_parts[i] = second

                        if is_glued:
                            glued_words.append(i)

                        for k in range(i + 1, i + len(first_parts)):
                            message_parts[k] = ""

    list.sort(glued_words, reverse=True)

    while "" in message_parts:
        index = message_parts.index("")

        for i in range(len(glued_words)):
            if glued_words[i] > index:
                glued_words[i] = glued_words[i] - 1

        message_parts.remove("")

    for i in glued_words:
        if i > 0:
            message_parts[i - 1] = message_parts[i - 1] + message_parts[i]
            message_parts[i] = ""

    while "" in message_parts:
        message_parts.remove("")

    return " ".join(message_parts)


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
        processed_message = apply_dict(message)

        write_log(message + "   ->   " + processed_message)

        if is_testing:
            print(processed_message)
        else:
            twitch_send_message(processed_message)


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
