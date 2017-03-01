#!/usr/bin/env python
import os
import sys
from optparse import OptionParser
from ducktoolkit import encoder, common


# This python script is heavily based on DuckToolkit (https://ducktoolkit.com),
# thanks to DuckToolkit developers Kevin Breen and James Hall.

__description__ = 'Interpreter of Ducky Scripts'
__author__ = 'Bash Bunny Development Team & @kevthehermit'
__version__ = '0.3'
__date__ = '03/01/2017'

base_path = "/root/udisk/payloads/"


if __name__ == "__main__":
    parser = OptionParser(usage='usage: %prog [options] inputfile \n' + __description__,
                          version='%prog ' + __version__)
    parser.add_option("-l", "--language", dest='lang_file', default=False, help="Select Keyboard Language")
    (options, args) = parser.parse_args()

    if len(args) < 1:
        print "[!] You need to select an Ducky Script"
        parser.print_help()
        sys.exit()

    input_line = args[0]
    language = options.lang_file

    if not language:
        print "[!] You need to specify a supported language"
        parser.print_help()
        print "[+] Supported Languages"
        for lang in common.list_languages():
            print "  [-] {0}".format(lang.split('.')[0])
        sys.exit()

    if "{0}.json".format(language) not in common.list_languages():
        print "[!] Language {0} is not supported at this time.".format(language)
        print "[+] Supported Languages"
        for lang in common.list_languages():
            print "  [-] {0}".format(lang.split('.')[0])
        parser.print_help()
        sys.exit()

    # All files should be relative to payloads and start with a switch1 or switch2 so
    if input_line.startswith('switch'):
        # shoudl be a filename
        try:
            duck_filename = os.path.join(base_path, input_line)
            print "[+] Opening File: ", duck_filename
            duck_text = open(duck_filename, 'rb').read()
        except Exception as e:
            print "[!] Error opening ducky file {0} : {1}".format(duck_filename, e)

    else:
        # Should be valid duck language
        duck_text = input_line

    try:
        encoder.encode_script(duck_text, language, bunny=True)
    except Exception as e:
        print e

