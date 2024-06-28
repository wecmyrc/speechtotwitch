# Speech to twitch

Клавиатура для ног

## Установка

### Зависимости

Всё работает на [python 3.12](https://www.python.org/downloads/release/python-3124/), [micromamba](https://mamba.readthedocs.io/en/latest/index.html) ворочает пакетами:

- [vosk v0.3.45](https://pypi.org/project/vosk/)
- [sounddevice v0.4.7](https://pypi.org/project/sounddevice/)
- [twitch-chat-irc v0.0.4](https://pypi.org/project/twitch-chat-irc/)

### Windows

Экзешник, собранный через [pyinstaller](https://pyinstaller.org/en/stable/), можно найти в архиве с исходным кодом (Windows-build-stt-v101.7z). Качать [тут](https://github.com/wecmyrc/speechtotwitch/releases/latest).

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

Эта штука слушает микрофон и льет в чат твича все, что слышит.

### Подготовка

Для доступа к твоему аккаунту нужно сгенерировать `OAuth` ключ [здесь](https://twitchapps.com/tmi/). Ключ не теряем, а записываем в блокнотик или в файл `key.txt` в следющем виде:

```
  имя пользователя
  oauth ключ
```

> [!WARNING]
> Файл `key.txt` живет рядом с `stt.py/stt.exe` и следи чтобы не закрался пробел в конце строки!

### Запуск

```
Mic test? (no output to twitch) [y/N]:
```

Проверка микрофона? Ты говоришь - консоль выводит, а в твич ничего не идет.

<kbd>y</kbd> - тестируем микрофон

<kbd>Enter</kbd> - идем дальше

<br>

```
Use key.txt? [Y/n/s]:
```

Используем `key.txt`? Если заполнишь `key.txt`, то не придется каждый раз вручную писать ключ. Также ты можешь иметь несколько файлов ключей, например для разных пользователей. Свои файлы ключей заполняются также как и `key.txt` и хранятся в той же директории.

<kbd>Enter</kbd> - используем `key.txt`

<kbd>n</kbd> - хочу вручную ввести данные

<kbd>s</kbd> - хочу указать свой файл

<br>

```
Channel:
```

Канал, куда будут идти сообщения.

<br>

Чтобы выключить нажми <kbd>Ctrl-C</kbd>. Чтобы поменять канал просто перезапусти и введи новые данные.

Вроде на этом всё. Всем удачи, я погнал 👋 🐸

## Troubleshooting

### Вылетает

Нужный файл с ключом на месте?

<br>

### list index out of range

Заполни файл ключа

## TODO

- [x] несколько файлов ключей
- [ ] фильтрация плохих слов
- [ ] подмена слов
- [ ] логирование сказанного
