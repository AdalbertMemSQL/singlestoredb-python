#!/usr/bin/env python
# type: ignore
"""Utilities for testing."""
from __future__ import annotations

import os
import uuid
from urllib.parse import urlparse

import singlestore as s2
from singlestore.connection import build_params


def load_sql(sql_file: str) -> str:
    """
    Load a file containing SQL code.

    Parameters
    ----------
    sql_file : str
        Name of the SQL file to load.

    Returns
    -------
    str : name of database created for SQL file

    """
    dbname = None

    # Use an existing database name if given.
    if 'SINGLESTORE_URL' in os.environ:
        dbname = build_params(host=os.environ['SINGLESTORE_URL']).get('database')
    elif 'SINGLESTORE_HOST' in os.environ:
        dbname = build_params(host=os.environ['SINGLESTORE_HOST']).get('database')
    elif 'SINGLESTORE_DATABASE' in os.environ:
        dbname = os.environ['SINGLESTORE_DATBASE']

    # If no database name was specified, use initializer URL if given.
    # HTTP can't change databases, so you can't initialize from HTTP
    # while also creating a database.
    args = {}
    if not dbname and 'SINGLESTORE_INIT_DB_URL' in os.environ:
        args['host'] = os.environ['SINGLESTORE_INIT_DB_URL']

    http_port = 0
    if 'SINGLESTORE_URL' in os.environ:
        url = os.environ['SINGLESTORE_URL']
        if url.startswith('http:') or url.startswith('https:'):
            urlp = urlparse(url)
            if urlp.port:
                http_port = urlp.port

    if 'SINGLESTORE_HTTP_PORT' in os.environ:
        http_port = int(os.environ['SINGLESTORE_HTTP_PORT'])

    # Always use the default driver since not all operations are
    # permitted in the HTTP API.
    with open(sql_file, 'r') as infile:
        with s2.connect(**args) as conn:
            with conn.cursor() as cur:
                if not dbname:
                    dbname = 'TEST_{}'.format(uuid.uuid4()).replace('-', '_')
                    cur.execute(f'CREATE DATABASE {dbname};')
                    cur.execute(f'USE {dbname};')

                    # Execute lines in SQL.
                    for cmd in infile.read().split(';\n'):
                        cmd = cmd.strip()
                        if cmd:
                            cmd += ';'
                            cur.execute(cmd)

                # Start HTTP server as needed.
                if http_port:
                    cur.execute(f'SET GLOBAL HTTP_PROXY_PORT={http_port};')
                    cur.execute('SET GLOBAL HTTP_API=ON;')
                    cur.execute('RESTART PROXY;')

    return dbname


def drop_database(name: str) -> None:
    """Drop a database with the given name."""
    if name:
        args = {}
        if 'SINGLESTORE_INIT_DB_URL' in os.environ:
            args['host'] = os.environ['SINGLESTORE_INIT_DB_URL']
        with s2.connect(**args) as conn:
            with conn.cursor() as cur:
                cur.execute(f'DROP DATABASE {name};')
