#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
import os
import cStringIO
import json
import time
from common import convert_hex

DEBUG = False

def hidg_write(elements):
    values = bytearray(elements)
    not_hold = bytearray([0, 0, 0, 0, 0, 0, 0, 0])

    hidg = open("/dev/hidg0", "wb")
    hidg.write(values)
    hidg.write(not_hold)
    hidg.close()


def parse_text(duck_text, lang_file, bunny):
    line_count = 0
    encoded_file = []
    duck_text = duck_text.replace("\r", "")
    cmd = instruction = False

    default_delay = 0

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
            else:
                cmd = parsed_line[0].strip()
                instruction = False

            if DEBUG:
                print "CMD: ", cmd, "Instruction: ", instruction

            # Default Delay
            if cmd in ['DEFAULT_DELAY', 'DEFAULTDELAY']:
                try:
                    default_delay = int(instruction)
                    continue
                except Exception as e:
                    error_line = e
                    return error_line

            # Repeat
            repeat_count = 1
            if cmd.lower() in ['repeat', 'replay']:
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

                        elements = lang_file[char].split(',')
                        elements = [int(i, 16) for i in elements]
                        # Bunny Support
                        if bunny:
                            for i in range(5):
                                elements.append(0)
                            hidg_write(elements)
                        else:
                            encoded_file.append(convert_hex(elements[2]))
                            encoded_file.append(convert_hex(elements[0]))
                        if DEBUG:
                            print char, ': ', convert_hex(elements[2]), convert_hex(elements[0])

                elif cmd == 'DELAY':
                    #Bunny Support
                    if bunny:
                        time.sleep(0.001 * int(instruction))
                    else:
                        delay = add_delay(int(instruction))
                        encoded_file.append(delay)

                elif cmd in lang_file.iterkeys():

                    elements = lang_file[cmd].split(',')
                    elements = [int(i, 16) for i in elements]
                    # Bunny Support
                    for i in range(5):
                        elements.append(0)

                    if instruction:
                        param = lang_file[instruction].split(',')
                        param = [int(i, 16) for i in param]
                        elements[0] |= param[0]
                        elements[2] |= param[2]

                    # Bunny Support
                    if bunny:
                        hidg_write(elements)
                    else:
                        encoded_file.append(convert_hex(elements[2]))
                        encoded_file.append(convert_hex(elements[0]))

                    if DEBUG:
                        print instruction, ': ', convert_hex(elements[2]), convert_hex(elements[0])
                else:
                    err_line = "Command {0} Not in Language File".format(cmd)
                    return err_line

                # Add Default Delay
                if default_delay:
                    if bunny:
                        time.sleep(0.001 * int(default_delay))
                    else:
                        encoded_file.append(add_delay(int(default_delay)))

    return encoded_file


def add_delay(delay_value):

    delay_return = ''

    # divide by 255 add that many 0xff
    # convert the reminder to hex
    # e.g. 750 = FF FF F0
    while delay_value > 0:
        if delay_value > 255:
            delay_return += '00FF'
            delay_value -= 255
        else:
            _delay = hex(delay_value)[2:].zfill(2)
            delay_return += '00{0}'.format(str(_delay))
            delay_value = 0
    return delay_return


def encode_script(duck_text, duck_lang, bunny=None):

    lang_dir = os.path.join(os.path.dirname(__file__), 'languages')
    language_dict = os.path.join(lang_dir, '{0}.json'.format(duck_lang))
    lang_file = json.load(open(language_dict))

    try:
        encoded_file = parse_text(duck_text, lang_file, bunny)
    except Exception as e:
        print "Error parsing duck_text: {0}".format(e)
        return False

    if encoded_file and not bunny:
        if 'Not in Language' in encoded_file:
            return encoded_file
        else:
            try:
                encoded_file = "".join(encoded_file)
                duck_blob = cStringIO.StringIO()

                duck_blob.write(encoded_file.decode('hex'))

                duck_bin = duck_blob.getvalue()
                duck_blob.close()
                return duck_bin

            except Exception as e:
                print "Error creating inject.bin: {0}".format(e)
                return False
