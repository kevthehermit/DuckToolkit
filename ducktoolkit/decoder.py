#!/usr/local/bin/python
import os
import json
import codecs
from ducktoolkit.common import decoder_command_keys


def decode_script(duck_lang, ducky_bin):
    lang_dir = os.path.join(os.path.dirname(__file__), 'languages')
    language_dict = os.path.join(lang_dir, '{0}.json'.format(duck_lang))
    lang_file = json.load(open(language_dict))
    ducky_hex = codecs.encode(ducky_bin, 'hex')
    decoded_bin = ""
    duck_decoded = ""

    for i in range(0, len(ducky_hex), 4):
        decoded_key = ""
        last_key = duck_decoded
        duck_decoded = ducky_hex[i:i+4]

        for key, value in iter(lang_file.items()):

            # Convert value from new format
            try:
                new_value = value.split(',')
                if len(new_value) == 3:
                    value = '{0}{1}'.format(new_value[2], new_value[0])
            except:
                continue


            # Fix for spacing in STRING statements
            if duck_decoded == "2c00":
                decoded_key = " "

            elif duck_decoded == "00ff" and last_key != "00ff":
                decoded_key = "DELAY"

            elif duck_decoded == value:
                decoded_key = key

            else:
                if duck_decoded[-2:] == "00":
                    if duck_decoded[:2] == value:
                        if len(key) == 1:
                            decoded_key = key

        if decoded_key in decoder_command_keys:
            decoded_bin += decoded_key + "\n"
        else:
            decoded_bin += decoded_key

    return decoded_bin
