#!/usr/bin/python3
import argparse
from csv_parser import csv_parser
from sql_parser import sql_parser

def main():
    parser = argparse.ArgumentParser(prog='Leaked database parser')
    parser.add_argument('db_file', help='database file')
    parser.add_argument('-o', help='output_file', type=str, dest="output")
    parser.add_argument('-n', help='maximum line number', type=str, dest="max_line")
    subparsers = parser.add_subparsers(help='sub-command help', dest="parser")

    parser_csv = subparsers.add_parser('csv', help='csv parser help')
    parser_csv.add_argument('-c', help='columns (comma separated)', type=str, dest="columns")
    parser_csv.add_argument('--no-header', action="store_true", help='ignore first line (header)', dest='no_header')

    parser_sql = subparsers.add_parser('sql', help='sql parser help')
    parser_sql.add_argument('--list-tables', action="store_true", help='list tables', dest='list_tables')
    parser_sql.add_argument('--dump', help='dump table', type=str, dest='dump_table')
    parser_sql.add_argument('-c', help='columns (comma separated)', type=str, dest="columns")

    args = parser.parse_args()

    if args.parser == "csv":
        csv_parser(args.db_file, args.output, args.max_line, args.columns, ':', None, args.no_header)
    if args.parser == "sql":
        action = None
        if args.list_tables:
            action = ("list_tables",)
        elif args.dump_table:
            action = ("dump_table", args.dump_table, args.columns)
        sql_parser(args.db_file, args.output, args.max_line, action)
    else:
        parser.print_help()

if __name__=="__main__":
    main()
