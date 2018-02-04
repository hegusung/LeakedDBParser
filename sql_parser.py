import csv
import ast
import traceback

def sql_parser(db_file, output_file, max_line, action):

    if output_file:
        output_file = open(output_file, 'w')
        writer = csv.writer(output_file, delimiter=':', quoting=csv.QUOTE_NONE, quotechar='', escapechar='\\')

    if max_line:
        max_line = int(max_line)

    max_line_count = 0

    in_sql_file = open(db_file, errors='backslashreplace')

    if action[0] == "list_tables":
        for table_args in get_tables(in_sql_file):
            if table_args != None:
                print("table: %s => %s" % (table_args[0].ljust(25), ", ".join(["%d:%s" % (i, a) for i, a in enumerate(table_args[1])])))

                max_line_count += 1
                if max_line and max_line_count >= max_line:
                    break
    elif action[0] == "dump_table":
        table_name = action[1]
        columns = action[2]

        if columns:
            column_list = []
            for val in columns.split(','):
                column_list.append(int(val))
        else:
            column_list = None

        for dump in get_insert(in_sql_file, table_name, column_list):
            if dump != None:
                if not output_file:
                    print(':'.join(dump))
                    max_line_count += 1
                else:
                    writer.writerow(dump)
                    max_line_count += 1

                if max_line and max_line_count >= max_line:
                    break

def get_insert(sql_file, table_name, column_list):

    insert_str = "INSERT INTO `%s`" % table_name

    for line in sql_file:
        if line.startswith(insert_str):
            for insert in process_insert(line, sql_file, column_list):
                yield insert

def process_insert(line, sql_file, column_list):

    s = line[line.find('VALUES '):]

    if '(' in s:

        s = s[s.find('('):-2] # ), or ); + \n, conserve ()
        try:
            # ast understands None but not NULL
            s = s.replace(',NULL', ',None');
            entries = ast.literal_eval(s)

            if type(entries[0]) == tuple:
                for entry in entries:
                    if column_list != None:
                        yield [str(entry[i]) for i in column_list]
                    else:
                        yield [str(e) for e in entry]
            else:
                if column_list != None:
                    yield [str(entries[i]) for i in column_list]
                else:
                    yield [str(e) for e in entries]

        except SyntaxError:
            traceback.print_exc()
            pass
        except ValueError:
            traceback.print_exc()
            print(s)
            pass

        if line.endswith(');\n'):
            return

    for line in sql_file:
        s = line[:-2] # ), or );  + \n, conserve ()
        try:
            # ast understands None but not NULL
            s = s.replace(',NULL', ',None');
            entries = ast.literal_eval(s)

            if type(entries[0]) == tuple:
                for entry in entries:
                    if column_list != None:
                        yield [str(entry[i]) for i in column_list]
                    else:
                        yield [str(e) for e in entry]
            else:
                if column_list != None:
                    yield [str(entries[i]) for i in column_list]
                else:
                    yield [str(e) for e in entries]
        except SyntaxError:
            traceback.print_exc()
            pass
        except ValueError:
            traceback.print_exc()
            print(s)
            pass

        if line.endswith(');\n'):
            return

def get_tables(sql_file):

    for line in sql_file:
        if line.startswith("CREATE TABLE"):
            table_args = process_create_table(line, sql_file)

            if table_args != None:
                yield table_args

def process_create_table(line, sql_file):

    if not line.startswith("CREATE TABLE"):
        return

    table_name = None
    for word in line.split()[2:]:
        if word.startswith('`'):
            table_name = word[1:]
        elif table_name != None:
            table_name = "%s %s" % (table_name, word)

        if table_name != None and table_name.endswith('`'):
            table_name = table_name[:-1]
            break

    if table_name == None:
        print(line)
        print(line.split())

    args = []

    for line in sql_file:
        if line.startswith(')'):
            break

        arg = None
        for word in line.split():
            if word.startswith('`') and word.endswith('`'):
                arg = word[1:-1]
                break

        args.append(arg)

    return (table_name, args)

