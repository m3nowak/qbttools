from qbtools import cli, logic
if __name__ == '__main__':
    args = cli.parser.parse_args()
    if 'func' in args:
        args.func(args)
    else:
        logic.default(args)
