#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
import os
import cStringIO
import json
from common import encoder_command_keys


special_chars = ['@',
                 '\\',
                 '#',
                 '~',
                 '$',
                 '|',
                 '+',
                 '-',
                 '!',
                 '^',
                 '&',
                 '*',
                 '{',
                 '}',
                 '[',
                 ']',
                 '(',
                 ')',
                 '=',
                 ',',
                 '%',
                 '?',
                 '_',
                 ';',
                 ':',
                 '<',
                 '>',
                 '.',
                 '/',
                 '"',
                 '`',
                 '\'',
                 '1',
                 '2',
                 '3',
                 '4',
                 '5',
                 '6',
                 '7',
                 '8',
                 '9',
                 '0']


def parse_text(duck_text, lang_file):
    line_count = 0
    encoded_file = []
    duck_text = duck_text.replace("\r", "")
    cmd = instruction = False


    for line in duck_text.split('\n'):
        if len(line) > 0:
            # REM Comments
            if line.startswith('REM') or line.startswith('rem'):
                continue

            # Last Command
            last_command = cmd
            last_instruction = instruction

            line_count += 1
            line = line.lstrip().rstrip()
            parsed_line = line.split(' ', 1)

            if len(parsed_line) >= 2:
                cmd = parsed_line[0].strip()
                instruction = parsed_line[1].rstrip()
                if cmd != "STRING":
                    if instruction not in encoder_command_keys:
                        instruction = instruction.lower()
            else:
                cmd = parsed_line[0].strip()
                instruction = False

            # Repeat
            repeat_count = 1
            if cmd in ['REPEAT', 'repeat']:
                try:
                    repeat_count = int(instruction)
                except Exception as e:
                    print e
                    error_line = 'Repeat value not valid'

                cmd = last_command
                instruction = last_instruction

            for i in range(repeat_count):

                if cmd == 'STRING':
                    for char in instruction:

                        if char in special_chars:
                            if len(lang_file[char]) <= 2:
                                encoded_file.append(lang_file[char])
                                encoded_file.append('00')
                            else:
                                encoded_file.append(lang_file[char])
                        elif not char.isupper():

                            encoded_file.append(lang_file[char])
                            encoded_file.append('00')
                        else:
                            encoded_file.append(lang_file[char])

                elif cmd == 'DELAY':
                    delay = int(instruction)

                    # divide by 255 add that many 0xff
                    # convert the reminder to hex
                    # e.g. 750 = FF FF F0
                    while delay > 0:
                        if delay > 255:
                            encoded_file.append('00FF')
                            delay -= 255
                        else:
                            _delay = hex(delay)[2:].zfill(2)
                            encoded_file.append('00{0}'.format(str(_delay)))
                            delay = 0

                elif cmd in lang_file.iterkeys():
                    if not instruction:
                        encoded_file.append(lang_file[cmd.upper()])
                        if len(lang_file[cmd.upper()]) == 2:
                            encoded_file.append('00')
                        # encoded_file.append('00')
                    else:
                        # print "CMD: {0}".format(cmd)
                        encoded_file.append(lang_file[instruction])
                        encoded_file.append(lang_file[cmd].upper())

                else:
                    err_line = "Command {0} Not in Language File".format(cmd)
                    return err_line
    return encoded_file


def encode_script(duck_text, duck_lang):

    lang_dir = os.path.join(os.path.dirname(__file__), 'languages')
    language_dict = os.path.join(lang_dir, '{0}.json'.format(duck_lang))
    lang_file = json.load(open(language_dict))

    try:
        encoded_file = parse_text(duck_text, lang_file)
    except Exception as e:
        print "Error parsing duck_text: {0}".format(e)
        return False

    if encoded_file:
        if 'Not in Language' in encoded_file:
            return encoded_file
        else:

            try:
                encoded_file = "".join(encoded_file)
                duck_blob = cStringIO.StringIO()

                duck_blob.write(encoded_file.decode('hex'))

                '''for char in encoded_file:
                    duck_blob.write(char.)'''
                duck_bin = duck_blob.getvalue()
                duck_blob.close()
                return duck_bin

            except Exception as e:
                print "Error creating inject.bin: {0}".format(e)
                return False
