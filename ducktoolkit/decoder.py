#!/usr/local/bin/python
import os
import json
from common import decoder_command_keys


def decode_script(duck_lang, ducky_bin):
    lang_dir = os.path.join(os.path.dirname(__file__), 'languages')
    language_dict = os.path.join(lang_dir, '{0}.json'.format(duck_lang))
    lang_file = json.load(open(language_dict))
    ducky_hex = ducky_bin.encode('hex')
    decoded_bin = ""
    duck_decoded = ""

    for i in range(0, len(ducky_hex), 4):
        decoded_key = ""
        last_key = duck_decoded
        duck_decoded = ducky_hex[i:i+4]

        for key, value in lang_file.iteritems():
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
