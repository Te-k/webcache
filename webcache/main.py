import argparse
from .google import Google
from .yandex import Yandex
from .bing import Bing
from .archiveis import ArchiveIs
from .archiveorg import ArchiveOrg


def main():
    parser = argparse.ArgumentParser(description='Search or do cache')
    subparsers = parser.add_subparsers(help='subcommand')
    parser_a = subparsers.add_parser('search', help='Search in cache')
    parser_a.add_argument('URL', help='URL of the cache')
    parser_a.set_defaults(subcommand='search')
    parser_b = subparsers.add_parser('save', help='Save in cache platforms')
    parser_b.add_argument('URL', help='URL ')
    parser_b.set_defaults(subcommand='save')
    args = parser.parse_args()

    if 'subcommand' in args:
        if args.subcommand == 'search':
            # Google
            google = Google.cache(args.URL)
            if google['success']:
                if 'date' in google:
                    print('Google: FOUND %s (%s)' % (
                        google['cacheurl'],
                        google['date']
                    ))
                else:
                    print('Google: FOUND %s' % (google['cacheurl']))
            else:
                print("Google: NOT FOUND")
            # Yandex
            yandex = Yandex.cache(args.URL)
            if yandex['success']:
                if yandex['found']:
                    print('Yandex: FOUND %s' % yandex['cacheurl'])
                else:
                    print("Yandex: NOT FOUND")
            else:
                print("Yandex : Query failed (captcha likely)")
            # Bing
            bing = Bing.cache(args.URL)
            if bing['success']:
                print('Bing: FOUND %s (%s)' % (
                    bing['cacheurl'],
                    bing['date']
                ))
            else:
                print("Bing: NOT FOUND")
            # Archive.is
            try:
                arch = ArchiveIs.snapshots(args.URL)
                if len(arch) > 0:
                    print('Archive.is: FOUND')
                    for s in arch:
                        print('-%s: %s' % (s['date'], s['archive']))
                else:
                    print('Archive.is: NOT FOUND')
            except requests.exceptions.ConnectTimeout:
                print('Archive.is: TIME OUT')
            # Web Archive
            web = ArchiveOrg.snapshots(args.URL)
            if len(web) > 0:
                print('Archive.org: FOUND')
                for s in web:
                    print('-%s: %s' % (s['date'], s['archive']))
            else:
                print('Archive.org: NOT FOUND')
        elif args.subcommand == "save":
            # Archive.ord
            res = ArchiveOrg.capture(args.URL)
            print("Saved in Internet Archive : {}".format(res))

            # Archive.is
            res = ArchiveIs.capture(args.URL)
            print("Saved in Archive.is : {}".format(res))
        else:
            parser.print_help()
    else:
        parser.print_help()
