import argparse
import os
import sys
import datetime as dt

import pydantic

import qbtools.config
import qbtools.qbtsvc
import qbtools.feed

CONFIG_FILENAME = 'qbtools.conf'

def _read_config() -> qbtools.config.Config:
    if os.path.exists(CONFIG_FILENAME):
        return pydantic.parse_file_as(qbtools.config.Config, CONFIG_FILENAME)
    else:
        print("Cannot find config file")
        sys.exit(1) 

def default(args: argparse.Namespace):
    print("No subcommand used")
    print(args)
    sys.exit(1) 

def make_config(_: argparse.Namespace):
    if os.path.exists(CONFIG_FILENAME):
        print("File already exists.")
        sys.exit(1)
    else:
        config = qbtools.config.produce_default_config()
        fle = open(CONFIG_FILENAME, 'w')
        fle.write(config.json(indent=2))
        fle.close()
        print("File created!")

def pause_category(args: argparse.Namespace):
    category = args.category
    config = _read_config()
    svc = qbtools.qbtsvc.QbtSvc(config.qbt_access)
    svc.setup()
    count = svc.pause_category(category)
    print(f"Paused {count}.")

def resume_category(args: argparse.Namespace):
    category = args.category
    config = _read_config()
    svc = qbtools.qbtsvc.QbtSvc(config.qbt_access)
    svc.setup()
    count = svc.resume_category(category)
    print(f"Resumed {count}.")

def expire_category(args: argparse.Namespace):
    category = args.category
    config = _read_config()
    days = args.days if args.days is not None else config.expire_default
    if days < 0:
        raise 
    print(f"Expiring elements older than {days} days.")
    svc = qbtools.qbtsvc.QbtSvc(config.qbt_access)
    svc.setup()
    count = svc.remove_category_from_old(category, dt.datetime.now()-dt.timedelta(days=days))
    print(f"Removed {count}.")

def feed_update(args: argparse.Namespace):
    start_entry = not args.paused
    config = _read_config()
    svc = qbtools.qbtsvc.QbtSvc(config.qbt_access)
    svc.setup()
    count = 0
    for feed_config in config.feeds:
        feed = qbtools.feed.Feed(feed_config.url)
        feed.load()
        for rule in feed_config.rules:
            for entry in feed.filter_by_title(rule.phrase, rule.date_limit):
                print("saving to {rule.save_path}")
                svc.add_magnet(entry.link, start_entry, rule.category, rule.save_path)
                count += 1
    print(f"Found {count} entries!")

            

