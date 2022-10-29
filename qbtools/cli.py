import argparse

import qbtools.logic

parser = argparse.ArgumentParser(
                    prog = 'qbtools',
                    description = 'Qbittorrent utility tools',
                    epilog = 'Suit yourself')
subparsers = parser.add_subparsers(help='sub-command help')

parser_makeconf = subparsers.add_parser('makeconf', help='create config file')
parser_makeconf.set_defaults(func=qbtools.logic.make_config)

parser_cat_resume = subparsers.add_parser('catresume', help='resume category')
parser_cat_resume.add_argument('category', type=str, help='category to be resumed')
parser_cat_resume.set_defaults(func=qbtools.logic.resume_category)

parser_cat_pause = subparsers.add_parser('catpause', help='pause category')
parser_cat_pause.add_argument('category', type=str, help='category to be paused')
parser_cat_pause.set_defaults(func=qbtools.logic.pause_category)

parser_cat_pause = subparsers.add_parser('catexpire', help='expire old elements in category')
parser_cat_pause.add_argument('category', type=str, help='category to be cleared')
parser_cat_pause.add_argument('-d', '--days', type=int, help='days to keep', required=False)
parser_cat_pause.set_defaults(func=qbtools.logic.expire_category)
