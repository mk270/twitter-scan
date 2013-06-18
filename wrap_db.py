#!/usr/bin/env python

from contextlib import contextmanager
import psycopg2

@contextmanager
def transaction(db):
    cursor = db.cursor()
    try:
        yield cursor
    except:
        db.rollback()
	raise
    else:
        db.commit()
        cursor.close()

db = None
database_name = 'mk_blog'

def make_db_handle(**args):
    return psycopg2.connect(**args)

def get_db_handle():
    global db

    if db is None:
        db = make_db_handle(database=database_name)
    return db

def store_short_url(url):
    db = get_db_handle()
    with transaction(db) as c:
	c.execute("insert into twitter_url (short_url) values (%(url)s);",
		  { "url": url }
		  )

def store_url(url):
    db = get_db_handle()
    with transaction(db) as c:
	c.execute("insert into article (url, active) values (%(url)s, 't');",
		  { "url": url }
		  )

def url_cached(url):
    db = get_db_handle()
    c = db.cursor()
    c.execute("select * from article where url = %(url)s", { "url": url })
    rows = c.fetchall()
    return rows != []

def short_url_cached(url):
    db = get_db_handle()
    c = db.cursor()
    c.execute("select * from twitter_url where short_url = %(url)s", { "url": url })
    rows = c.fetchall()
    return rows != []

def run():
    db = get_db_handle()

    store_url("myurl")


if __name__ == '__main__':
	run()
