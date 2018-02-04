# LeakedDBParser

Just a quick'n'dirty tool to parse leaked databases (csv-like or sql format)

## Usage

```
./leakeddbparser.py <hashfile> [-o <output_file>] [-n max_lines] {csv|sql} [csv or sql options]
```

### CSV format options

* -c : select columns, and add some basic checks
example:
```
-c 1,2=40,?3
```
means: for each row, add columns 1 and 2 from csv file inthe output only if the length of the second columns equals 40, if column 3 exists if the row, add it to the output

* --no-header: ignore first line

### SQL format options

* --list-tables: list tables and its arguments
* --dump <table_name>: export the selected table to output
* -c : select columns

example:
First check the table name and its arguments in the file
```
./leakeddbparser.py sqldump.sql sql --list-tables
```

Once the table name hash been identified:
```
./leakeddbparser.py sqldump.sql -o export_user_hash.txt sql --dump users -c 3,5
```
