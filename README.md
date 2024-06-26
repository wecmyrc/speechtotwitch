# Speech to twitch

Клавиатура для ног

## Установка

### Зависимости

Всё работает на [python 3.12](https://www.python.org/downloads/release/python-3124/), [micromamba](https://mamba.readthedocs.io/en/latest/index.html) ворочает пакетами:

- [vosk v0.3.45](https://pypi.org/project/vosk/)
- [sounddevice v0.4.7](https://pypi.org/project/sounddevice/)
- [twitch-chat-irc v0.0.4](https://pypi.org/project/twitch-chat-irc/)

### Windows

Экзешник, собранный через [pyinstaller](https://pyinstaller.org/en/stable/), можно найти в архиве с исходным кодом (Windows-build-stt.7z). Качать [тут](https://github.com/wecmyrc/speechtotwitch/releases/latest).

Запустить вручную:

```
  micromamba create -f env.yml
  micromamba activate mamba-environment
  python stt.py
```

### Linux

Если есть [nix](https://nixos.org/), то:

```
  nix-shell
  python3 stt.py
```

Если нет, то [ручной способ для windows](#Windows) должен сработать (возможно придется использовать `python3 stt.py`).

## Использование

Эта штука слушает микрофон и льет в твич все, что слышит. Для доступа к твоему аккаунту нужно сгенерировать `OAuth` ключ [здесь](https://twitchapps.com/tmi/). Ключ не теряем, а записываем в блокнотик или в файл `key.txt` в следющем виде:

```
  имя пользователя
  oauth ключ
```

> [!WARNING]
> Файл создаем рядом с `stt.py/stt.exe` и следи чтобы не закрался пробел в конце строки!

Первым делом при запуске программа предлагает потестить микрофон. Если хочешь пропустить тест, то смело жми <kbd>Enter</kbd>, в противном случае надо вводить <kbd>Y/y</kbd>.

Следующим следует вопрос - использовать ли файл `key.txt`? Нажатие <kbd>Enter</kbd> или ввод <kbd>Y/y</kbd> подтвердит загрузку из файла. Если хочешь вводить всё вручную, то вводи любой символ кроме предложенных. При ручном вводе имей в виду, что `Username` - твое имя пользователя, `OAuth` - ключ для этого пользователя.

После получения информации о пользователе указывай канал (`Channel`) куда будешь надиктовывать.

Чтобы выключить нажми <kbd>Ctrl-C</kbd>. Чтобы поменять канал просто перезапусти и введи новые данные.

Вроде на этом всё. Всем удачи, я погнал 👋 🐸
