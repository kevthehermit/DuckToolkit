#!/usr/local/bin/python3
import os
import sys
import json
from binascii import hexlify
from .common import decoder_command_keys

major_version = sys.version_info[0]

def decode_script(duck_lang, ducky_bin):
    lang_dir = os.path.join(os.path.dirname(__file__), 'languages')
    language_dict = os.path.join(lang_dir, '{0}.json'.format(duck_lang))
    lang_file = json.load(open(language_dict))
    ducky_hex = hexlify(ducky_bin)
    decoded_bin = ""
    duck_decoded = ""


    for i in range(0, len(ducky_hex), 4):
        decoded_key = ""
        last_key = duck_decoded
        duck_decoded = ducky_hex[i:i+4]
        
        #print(last_key, duck_decoded)

        for key, value in lang_file.items():
            
            

            # Convert value from new format
            try:
                new_value = value.split(',')
                if len(new_value) == 3:
                    value = '{0}{1}'.format(new_value[2], new_value[0])
                    
                    if major_version == 3:
                        value = bytes(value, 'utf-8')


            except Exception as e:
                continue
            
            
            # Fix for spacing in STRING statements
            if duck_decoded == b"2c00":
                decoded_key = " "

            elif duck_decoded == b"00ff" and last_key !=b"00ff":
                decoded_key = "DELAY"

            elif duck_decoded == value:
                decoded_key = key

            else:
                if duck_decoded[-2:] == b"00":
                    if duck_decoded[:2] == value:
                        if len(key) == 1:
                            decoded_key = key

        if decoded_key in decoder_command_keys:
            decoded_bin += decoded_key + "\n"
        else:
            decoded_bin += decoded_key

    return decoded_bin
