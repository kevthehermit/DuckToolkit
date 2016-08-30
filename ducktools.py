#!/usr/bin/env python
import sys
from optparse import OptionParser

from ducktoolkit import encoder, decoder
from ducktoolkit.common import list_languages

__description__ = 'Ducky Tools'
__author__ = 'Kevin Breen, James Hall, https://ducktoolkit.com'
__version__ = '0.2'
__date__ = '25/08/2016'


if __name__ == "__main__":
    parser = OptionParser(usage='usage: %prog [options] inputfile outputfile\n' + __description__,
                          version='%prog ' + __version__)
    parser.add_option("-e", "--encode", action='store_true', default=False, help="Encode")
    parser.add_option("-d", "--decode", action='store_true', default=False, help="Decode")
    parser.add_option("-l", "--language", dest='lang_file', default=False, help="Select Keyboard Language")
    (options, args) = parser.parse_args()

    if len(args) < 2:
        print "[!] You need to set an input and output file"
        parser.print_help()
        print "[+] Supported Languages"
        for lang in list_languages():
            print "  [-] {0}".format(lang.split('.')[0])
        sys.exit()

    input_file = args[0]
    output_file = args[1]
    language = options.lang_file

    if not language:
        print "[!] You need to specify a supported language"
        parser.print_help()
        sys.exit()

    if "{0}.json".format(language) not in list_languages():
        print "[!] Language {0} is not supported at this time.".format(language)
        print "[+] Supported Languages"
        for lang in list_languages():
            print "  [-] {0}".format(lang.split('.')[0])
        parser.print_help()
        sys.exit()


    if options.encode:
        print "[+] Reading Input file."

        try:
            duck_text = open(input_file, 'rb').read()
        except Exception as e:
            print "  [!] Unable to open input file: {0}".format(input_file)
            sys.exit()

        print "  [-] Encoding File"
        duck_bin = encoder.encode_script(duck_text, language)

        if not duck_bin or 'Not in Language' in duck_bin:
            if duck_bin:
                print "[!] {0} Is not supported as a valid command".format(duck_bin)
            else:
                print "[!] Something went wrong"
        print "  [-] Encoding complete"

        print "  [-] Writing inject.bin to {0}".format(output_file)
        with open(output_file, 'wb') as out:
            out.write(duck_bin)
        print "[+] Process Complete"

    if options.decode:
        print "[+] Reading Duck Bin file"
        try:
            duck_bin = open(input_file, 'rb').read()
        except Exception as e:
            print "  [!] Unable to open input file: {0}".format(input_file)
            sys.exit()

        print "  [-] Decoding file"
        duck_text = decoder.decode_script(language, duck_bin)

        if duck_text:
            print "  [-] Writing ducky text to {0}".format(output_file)
            with open(output_file, 'wb') as out:
                out.write(duck_text)
            print "[+] Process Complete"

