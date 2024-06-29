#!/usr/bin/python3

import argparse
import sys
import sqlite3
from tqdm.auto import tqdm
import process
from process import *

sql = "SELECT sampleid, oewnsynsetid, sample FROM samples INNER JOIN synsets USING(synsetid)"
sql_count = "SELECT COUNT(*) FROM samples"
print(sql, file=sys.stderr)

progress = False


def process_text(input_text, rowid):
    r = process.process(input_text)
    if r:
        print(f"{rowid}\t{input_text}\t▶\t{r}")
        return 1
    return 0


def count(conn, resume):
    cursor = conn.cursor()
    sql2 = build_sql(sql_count, resume)
    cursor.execute(sql2)
    return cursor.fetchone()[0]


def build_sql(sql, resume):
    return sql + f" WHERE sampleid >= {resume}" if resume else sql


def read(file, resume, checkf):
    conn = sqlite3.connect(file)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    sql2 = build_sql(sql, resume)
    cursor.execute(sql2)
    n = count(conn, resume)
    pb = tqdm(total=n, disable=not progress)
    process_count = 0
    while True:
        row = cursor.fetchone()
        if row is None:
            break
        sample = row["sample"]
        sampleid = row["sampleid"]
        oewnsynsetid = row["oewnsynsetid"]
        rowid = f"{sampleid}\t{oewnsynsetid}"
        if checkf(sample, rowid):
            process_count += 1
        pb.update(1)
    conn.close()
    print(f"{process_count} processed")


def get_processing(name):
    return globals()[name] if name else process_text


def main():
    parser = argparse.ArgumentParser(description="scans the samples from sqlite file")
    parser.add_argument('database', type=str, help='database')
    parser.add_argument('--resume', type=int, help='row to resume from')
    parser.add_argument('--processing', type=str, help='processing function to apply')
    args = parser.parse_args()
    processing = get_processing(args.processing)
    read(args.database, args.resume, processing)


if __name__ == '__main__':
    main()
