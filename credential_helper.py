import json
import os
import sys


def main():
    if len(sys.argv) < 2:
        print 'Usage: python %s credential_filename' % sys.argv[0]
        exit()

    with open(sys.argv[1], 'r') as file_obj:
        credentials = json.load(file_obj)

    config = ""
    for key, value in credentials.items():
        config += 'GCP_%s="%s" ' % (key.upper(), value)

    print config
    os.system('heroku config:set %s' % config)


if __name__ == '__main__':
    main()
