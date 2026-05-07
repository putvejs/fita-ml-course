"""
Step 2: Connect to MySQL server and extract schema metadata.
Saves table names, column names, data types and constraints to context.json.
"""
import json
from datetime import datetime
import mysql.connector

DB_HOST = "87.110.123.151"
DB_PORT = 3306
DB_USER = "fita"
DB_PASS = "2026-04-28"

SYSTEM_DBS = {"information_schema", "mysql", "performance_schema", "sys"}


def explore_schema():
    conn = mysql.connector.connect(
        host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASS
    )
    cursor = conn.cursor()

    cursor.execute("SHOW DATABASES")
    all_dbs = [row[0] for row in cursor.fetchall()]
    user_dbs = [db for db in all_dbs if db not in SYSTEM_DBS]

    schema = {}

    for db_name in user_dbs:
        cursor.execute(f"USE `{db_name}`")
        cursor.execute("SHOW TABLES")
        tables = [row[0] for row in cursor.fetchall()]

        schema[db_name] = {}

        for table_name in tables:
            # Column info: Field, Type, Null, Key, Default, Extra
            cursor.execute(f"DESCRIBE `{table_name}`")
            columns = [
                {
                    "name": col[0],
                    "type": col[1],
                    "nullable": col[2] == "YES",
                    "key": col[3],
                    "default": col[4],
                    "extra": col[5],
                }
                for col in cursor.fetchall()
            ]

            try:
                cursor.execute(f"SELECT COUNT(*) FROM `{table_name}`")
                row_count = cursor.fetchone()[0]
            except Exception:
                row_count = None

            cursor.execute(
                """
                SELECT kcu.COLUMN_NAME, kcu.REFERENCED_TABLE_NAME, kcu.REFERENCED_COLUMN_NAME
                FROM information_schema.KEY_COLUMN_USAGE kcu
                WHERE kcu.TABLE_SCHEMA = %s
                  AND kcu.TABLE_NAME = %s
                  AND kcu.REFERENCED_TABLE_NAME IS NOT NULL
                """,
                (db_name, table_name),
            )
            foreign_keys = [
                {"column": fk[0], "references_table": fk[1], "references_column": fk[2]}
                for fk in cursor.fetchall()
            ]

            schema[db_name][table_name] = {
                "columns": columns,
                "row_count": row_count,
                "foreign_keys": foreign_keys,
            }

    cursor.close()
    conn.close()

    context = {
        "server": DB_HOST,
        "extracted_at": datetime.now().isoformat(),
        "databases": schema,
    }

    with open("context.json", "w", encoding="utf-8") as f:
        json.dump(context, f, indent=2, ensure_ascii=False, default=str)

    print(f"Schema extracted from {len(user_dbs)} database(s):")
    for db, tables in schema.items():
        print(f"  {db}: {len(tables)} table(s)")
        for tbl, info in tables.items():
            print(f"    - {tbl}: {len(info['columns'])} columns, {info['row_count']} rows")

    return context


if __name__ == "__main__":
    explore_schema()
