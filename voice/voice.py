import argparse
import queue
import sys
import traceback
import os
import datetime
import codecs
import time
import signal
import json
import time
from twitch_chat_irc import twitch_chat_irc  # [note] in future get rid of this lib

import pyaudio as pa

from vosk import Model, KaldiRecognizer, SetLogLevel

SetLogLevel(-1)  # [note] read file vosk_api.h in source code

from process_message import process_message
import db.settings
import db.messages
import db.keys
import db.blacklist
import db.whitelist
import db.dict

from base_logger.base_logger import logger, error_notification


def exc_handler(type, value, tb):
    error = "".join(traceback.format_exception(type, value, tb))
    logger.critical(error, stack_info=True)
    print(error)
    error_notification()


class TwitchConnection:
    def __init__(self):
        self.username = None
        self.oauth = None
        self.channel = None
        self.is_connected = False
        self.connection = None

    def set_data(self, username, channel):
        if self.username != username or self.channel != channel:
            self.username = username

            if self.username:
                db_error, self.oauth = db.keys.oauth(self.username)
                if db_error:
                    error_notification()

            self.channel = channel

            if self.is_connected:
                self.connection.close_connection()
                self.is_connected = False

            if (
                not self.is_connected
                and self.username != None
                and self.oauth != None
                and self.channel != None
            ):
                self.connection = twitch_chat_irc.TwitchChatIRC(
                    self.username,
                    self.oauth,
                    suppress_print=True,
                )
                self.is_connected = True

    def send_message(self, message):
        try:
            self.connection.send(self.channel, message)

        except Exception as e:
            error = "".join(traceback.format_exc())
            logger.critical(error, stack_info=True)
            print(error)
            error_notification()

            return False

        return True


class Voice:
    def __init__(self):
        self.to_exit = False
        self.raw_mic_q = queue.Queue()
        self.write_q = queue.Queue()
        self.twitch = TwitchConnection()
        signal.signal(signal.SIGTERM, self.exit)

    # [note] rewrite from sounddevice to pyaudio
    def callback(self, indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        self.raw_mic_q.put(bytes(indata))

    def handle_write_q(self):
        if not self.write_q.empty():
            message = self.write_q.get()

            db_error, settings = db.settings.settings()
            if db_error:
                error_notification()
                return

            if not settings["mic_on"]:
                return

            db_error, all_blacklist_entries = db.blacklist.all_blacklist_entries()
            if db_error:
                error_notification()
                return

            db_error, all_whitelist_entries = db.whitelist.all_whitelist_entries()
            if db_error:
                error_notification()
                return

            db_error, all_dict_entries = db.dict.all_dict_entries()
            if db_error:
                error_notification()
                return

            message = process_message.process_message(
                message=message,
                settings=settings,
                blacklist_entries=all_blacklist_entries,
                whitelist_entries=all_whitelist_entries,
                dict_entries=all_dict_entries,
            )

            self.twitch.set_data(
                settings["username_in_use"],
                settings["channel_in_use"],
            )

            is_sent = False

            if settings["twitch_on"]:
                is_sent = self.twitch.send_message(message)

            db_error = db.messages.add_messages_entry(
                datetime.datetime.now(),
                message,
                settings["username_in_use"],
                settings["channel_in_use"],
                is_sent,
            )[0]
            db.messages.handle_messages_limit()

    def handle_raw_mic_q(self, rec):
        if not self.raw_mic_q.empty():
            data = self.raw_mic_q.get()
            if rec.AcceptWaveform(data):
                res = rec.Result()
                temp = json.loads(res)["text"]
                if temp:
                    self.write_q.put(temp)

    def _read(
        self, rec, out
    ):  # [note] look at https://people.csail.mit.edu/hubert/pyaudio/#sources wire(callback)
        try:
            while not self.to_exit:
                time.sleep(0.1)  # [note] for low cpu usage

                data = out.read(16000)

                if len(data) != 0:
                    self.raw_mic_q.put(bytes(data))

                self.handle_raw_mic_q(rec)
                self.handle_write_q()

        except KeyboardInterrupt:
            pass

    def listen(self):
        device = None

        samplerate = 16000

        model = Model(lang="ru")

        self.stream = pa.PyAudio().open(
            rate=samplerate,
            channels=1,
            format=pa.paInt16,
            input=True,
            frames_per_buffer=16000,
        )

        rec = KaldiRecognizer(model, samplerate)

        self._read(rec, self.stream)

    def exit(self, signum, frame):
        self.to_exit = True
        self.stream.close()  # [note] https://people.csail.mit.edu/hubert/pyaudio/


def main():
    sys.excepthook = exc_handler

    v = Voice()
    v.listen()


if __name__ == "__main__":
    main()
