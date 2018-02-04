import csv

def csv_parser(db_file, output_file, max_line, columns, delimiter, quote_char, no_header):

    if output_file:
        output_file = open(output_file, 'w')
        writer = csv.writer(output_file, delimiter=':', quoting=csv.QUOTE_NONE, quotechar='')

    if max_line:
        max_line = int(max_line)

    if columns:
        column_list = []
        for val in columns.split(','):
            if val.startswith('?'):
                optional = True
                val = val[1:]
            else:
                optional = False

            if "=" in val:
                column_list.append((int(val.split('=')[0]), int(val.split('=')[1]), optional))
            else:
                column_list.append((int(val), None, optional))
    else:
        column_list = None

    if quote_char == None:
        quoting=csv.QUOTE_NONE
        quote_char=''
    else:
        quoting=csv.QUOTE_MINIMAL

    max_line_count = 0

    with open(db_file, errors='backslashreplace') as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter, quoting=quoting, quotechar='')
        for n, row in enumerate(reader):
            if no_header and n == 0:
                continue

            if column_list:
                try:
                    result_row = []
                    for col in column_list:
                        try:
                            item = row[col[0]]

                            # check length
                            if col[1] != None:
                                if len(item) == col[1]:
                                    pass
                                else:
                                    raise Exception("Wrong column size")

                            result_row.append(item)
                        except IndexError as e:
                            # if not optional
                            if col[2] == False:
                                raise e
                except Exception as e:
                    print("Error selecting columns in line %s" % (":".join(row),))
                    continue
            else:
                result_row = row

            if not output_file:
                print(':'.join(result_row))
                max_line_count += 1
            else:
                writer.writerow(result_row)
                max_line_count += 1

            if max_line and max_line_count >= max_line:
                break

    if output_file:
        output_file.close()
