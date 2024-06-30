#!/usr/bin/python3

import argparse
import sys
import re
import sqlite3
from tqdm.auto import tqdm
import process
from process import *

sql_union = """
SELECT 'sam' AS type, sampleid AS nid, sample AS `text`, oewnsynsetid FROM samples INNER JOIN synsets USING(synsetid)
UNION
SELECT 'def' AS type, synsetid AS nid, definition AS `text`, oewnsynsetid FROM synsets
"""
sql = f"SELECT oewnsynsetid, nid, type, `text` FROM ({sql_union}) ORDER BY oewnsynsetid, nid" #+ " LIMIT 10"
sql_count = f"SELECT COUNT(*) FROM ({sql_union})"
print(sql, file=sys.stderr)

progress = False


def sub_acute(input_text):
    return re.sub(r'´', "'", input_text)  # Ctr+Shift+ U then 0 0 B 4


def sub_acute_apostrophe(input_text):
    r =  sub_acute( input_text)
    return re.sub(r'＇', "'", r)  # Ctr+Shift+ U then F F 0 7


def process_rows(row1, row2, processing1f, processing2f):
    rowid1 = row1[0]
    rowid2 = row2[0]
    if rowid1 != rowid2:
        raise Exception("Unsync", (rowid1, rowid2))
    text1 = processing1f(row1[1])
    text2 = processing2f(row2[1])

    if text1 != text2:
        print(f"{rowid1}\t{text1}\t{text2}")
        return 1
    return 0


def count(conn, resume):
    cursor = conn.cursor()
    sql2 = build_sql(sql_count, resume)
    cursor.execute(sql2)
    return cursor.fetchone()[0]


def build_sql(sql_statement, resume):
    return sql_statement + f" WHERE oewnsynsetid >= {resume}" if resume else sql_statement


def read(file, resume):
    conn = sqlite3.connect(file)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    sql2 = build_sql(sql, resume)
    cursor.execute(sql2)
    while True:
        row = cursor.fetchone()
        if row is None:
            break
        row_text = row["text"]
        row_nid = row["nid"]
        row_type = row["type"]
        oewnsynsetid = row["oewnsynsetid"]
        rowid = f"{oewnsynsetid}\t{row_nid}\t{row_text}"
        yield rowid, row_text
    conn.close()


def read2(file1, file2, resume, processing1f, processing2f):
    pb = tqdm(disable=not progress)
    process_count = 0
    for rows in zip(read(file1, resume), read(file2, resume)):
        process_count += process_rows(rows[0], rows[1], processing1f, processing2f)
        pb.update(1)
    print(f"{process_count} found/processed", file=sys.stderr)


def get_processing(name):
    return globals()[name] if name else process.default_process


def main():
    parser = argparse.ArgumentParser(description="scans the examples and definitions from sqlite file")
    parser.add_argument('database1', type=str, help='database')
    parser.add_argument('database2', type=str, help='database')
    parser.add_argument('--resume', type=int, help='row to resume from')
    parser.add_argument('--processing1', type=str, help='processing function to apply to db1')
    parser.add_argument('--processing2', type=str, help='processing function to apply to db2')
    args = parser.parse_args()
    processing1f = get_processing(args.processing1)
    if processing1f:
        print(f"processing1 {processing1f}", file=sys.stderr)
    processing2f = get_processing(args.processing2)
    if processing2f:
        print(f"processing2 {processing2f}", file=sys.stderr)
    read2(args.database1, args.database2, args.resume, processing1f, processing2f)


if __name__ == '__main__':
    main()
