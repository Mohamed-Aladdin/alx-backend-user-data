#!/usr/bin/env python3
"""Task 0, 1, 2, 3, 4 Module"""

import re
import logging
import mysql.connector
import os
from typing import List


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """returns the log message obfuscated
    """
    for f in fields:
        message = re.sub(f'{f}=.*?{separator}',
                         f'{f}={redaction}{separator}', message)
    return message


def get_logger() -> logging.Logger:
    """returns a logging.Logger object
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """returns a connector to the database
    """
    username = os.get("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.get("PERSONAL_DATA_DB_PASSWORD", "")
    host_name = os.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.get("PERSONAL_DATA_DB_NAME")
    conn = mysql.connector.connection.MySQLConnection(user=username,
                                                     password=password,
                                                     host=host_name,
                                                     database=db_name)
    return conn


def main():
    """
    Main function that returns nothing
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    fields = [f[0] for f in cursor.description]
    logger = get_logger()

    for row in cursor:
        stringfy_row = ''.join(f'{f}={str(r)}; ' for r, f in zip(row, fields))
        logger.info(stringfy_row.strip())

    cursor.close()
    db.close()


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Constructor method for RedactingFormatter class

        Args:
            fields: list of fields to redact in log messages
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats the specified log record as text.

        Filters values in incoming log records using filter_datum.
        """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


if __name__ == '__main__':
    main()
