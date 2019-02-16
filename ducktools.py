#!/usr/bin/env python3
import io
import sys
import binascii
from optparse import OptionParser

from ducktoolkit import encoder, decoder
from ducktoolkit.common import list_languages

__description__ = 'Ducky Tools'
__author__ = 'Kevin Breen, James Hall, https://ducktoolkit.com'
__version__ = '1.0.3'
__date__ = '16/02/2019'

major_version = sys.version_info[0]


if __name__ == "__main__":
    parser = OptionParser(usage='usage: %prog [options] inputfile outputfile\n' + __description__,
                          version='%prog ' + __version__)
    parser.add_option("-e", "--encode", action='store_true', default=False, help="Encode")
    parser.add_option("-d", "--decode", action='store_true', default=False, help="Decode")
    parser.add_option("-l", "--language", dest='lang_file', default=False, help="Select Keyboard Language")
    (options, args) = parser.parse_args()

    if len(args) < 2:
        print("[!] You need to set an input and output file")
        parser.print_help()
        print("[+] Supported Languages")
        for lang in list_languages():
            print("  [-] {0}".format(lang.split('.')[0]))
        sys.exit()

    input_file = args[0]
    output_file = args[1]
    language = options.lang_file

    if not language:
        print("[!] You need to specify a supported language")
        parser.print_help()
        sys.exit()

    if "{0}.json".format(language) not in list_languages():
        print("[!] Language {0} is not supported at this time.".format(language))
        print("[+] Supported Languages")
        for lang in list_languages():
            print("  [-] {0}".format(lang.split('.')[0]))
        parser.print_help()
        sys.exit()


    if options.encode:
        print("[+] Reading Input file.")

        try:
            duck_text = open(input_file, 'rb').read()
        except Exception as e:
            print("  [!] Unable to open input file: {0}".format(input_file))
            sys.exit()

        print("  [-] Encoding File")
        encoder_response = encoder.encode_script(duck_text, language)
        
        if not encoder_response['valid']:
            print("[!] Error on line {0}: {1}".format(encoder_response['line_count'], encoder_response['message']))
            sys.exit(0)

        print("  [-] Encoding complete")

        print("  [-] Writing inject.bin to {0}".format(output_file))
        
        try:
            encoded_file = "".join(encoder_response['encoded_file'])
            duck_blob = io.BytesIO()
            write_bytes = encoded_file.encode()
            duck_blob.write(write_bytes)
            duck_bin = duck_blob.getvalue()
            duck_blob.close()

        except Exception as e:
            print("Error creating inject.bin: {0}".format(e))
            sys.exit()
        
        with open(output_file, 'wb') as out:
            out.write(binascii.unhexlify(duck_bin))
        print("[+] Process Complete")

    if options.decode:
        print("[+] Reading Duck Bin file")
        try:
            duck_bin = open(input_file, 'rb').read()
        except Exception as e:
            print("  [!] Unable to open input file: {0}".format(input_file))
            sys.exit()

        print("  [-] Decoding file")
        duck_text = decoder.decode_script(language, duck_bin)

        if duck_text:
            print("  [-] Writing ducky text to {0}".format(output_file))
            with open(output_file, 'wb') as out:
                if major_version == 3:
                    out.write(bytes(duck_text, 'utf-8'))
                else:
                    out.write(duck_text)
            print("[+] Process Complete")

