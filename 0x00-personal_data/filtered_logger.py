#!/usr/bin/env python3
"""Defines filtered_loger module."""

from typing import List
import logging
import mysql.connector
import os
import re

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Returns the log message obfuscated."""
    for field in fields:
        pattern = rf"{field}=.*?{separator}"
        replacement = f"{field}={redaction}{separator}"
        message = re.sub(pattern, replacement, message)

    return message


def get_logger() -> logging.Logger:
    """Returns a logging.Logger object"""
    logger = logging.getLogger('user_data')
    logger.propagate = False

    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    handler.setFormatter(RedactingFormatter(PII_FIELDS))

    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Returns a connector to the database."""
    host = os.getenv('PERSONAL_DATA_DB_HOST') or 'localhost'
    user = os.getenv('PERSONAL_DATA_DB_USERNAME') or 'root'
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD') or ''
    database = os.getenv('PERSONAL_DATA_DB_NAME')

    return mysql.connector.connect(
        host=host,
        port=3306,
        user=user,
        password=password,
        database=database
    )


def main() -> None:
    """
    Obtain a database connection using get_db and retrieve all rows in
    the users table and display each row under a filtered format.
    """
    logger = get_logger()

    connector = get_db()
    cursor = connector.cursor()

    cursor.execute('SELECT * FROM `users`;')
    users = cursor.fetchall()

    column_names = cursor.column_names

    for user in users:
        formatted_user = "".join(f"{attribute}={value}; " for
                                 attribute, value in zip(column_names, user))
        logger.info(formatted_user)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class.
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Formats a LogRecord."""
        msg = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)


if __name__ == '__main__':
    main()
