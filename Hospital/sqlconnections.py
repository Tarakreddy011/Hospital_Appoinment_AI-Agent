import os
import sqlite3
from datetime import datetime

try:
    import mysql.connector
    from mysql.connector import Error as MySQLError
    MYSQL_AVAILABLE = True
except ImportError:
    MYSQL_AVAILABLE = False
    MySQLError = Exception

MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "Tarak@2005")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "hospital_db")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQLITE_DB_PATH = os.path.join(BASE_DIR, "hospital.db")


class DatabaseManager:
    """
    Unified database manager supporting MySQL with automatic SQLite fallback.
    Prevents crashes if MySQL server is not started or credentials differ.
    """
    _mode = None  # 'mysql' or 'sqlite'

    @classmethod
    def get_connection(cls):
        # 1. Attempt MySQL connection
        if MYSQL_AVAILABLE:
            try:
                server_conn = mysql.connector.connect(
                    host=MYSQL_HOST,
                    port=MYSQL_PORT,
                    user=MYSQL_USER,
                    password=MYSQL_PASSWORD,
                    connection_timeout=2
                )
                if server_conn.is_connected():
                    cursor = server_conn.cursor()
                    cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{MYSQL_DATABASE}`")
                    cursor.close()
                    server_conn.close()

                    db_conn = mysql.connector.connect(
                        host=MYSQL_HOST,
                        port=MYSQL_PORT,
                        user=MYSQL_USER,
                        password=MYSQL_PASSWORD,
                        database=MYSQL_DATABASE,
                        connection_timeout=2
                    )
                    cls._mode = "mysql"
                    cls._init_mysql_tables(db_conn)
                    return db_conn
            except Exception:
                pass

        # 2. Resilient SQLite fallback
        cls._mode = "sqlite"
        sqlite_conn = sqlite3.connect(SQLITE_DB_PATH, check_same_thread=False)
        sqlite_conn.row_factory = sqlite3.Row
        cls._init_sqlite_tables(sqlite_conn)
        return sqlite_conn

    @classmethod
    def get_mode(cls):
        if cls._mode is None:
            conn = cls.get_connection()
            if conn:
                conn.close()
        return "MySQL (" + MYSQL_DATABASE + ")" if cls._mode == "mysql" else "SQLite (Local: hospital.db)"

    @classmethod
    def _init_mysql_tables(cls, conn):
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS patient_records (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            phone VARCHAR(50) NOT NULL,
            last_concern TEXT NOT NULL,
            routed_department VARCHAR(255) NOT NULL,
            visit_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        conn.commit()
        cursor.close()

    @classmethod
    def _init_sqlite_tables(cls, conn):
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS patient_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            last_concern TEXT NOT NULL,
            routed_department TEXT NOT NULL,
            visit_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        conn.commit()
        cursor.close()


def get_db_connection():
    return DatabaseManager.get_connection()


def get_active_db_type():
    return DatabaseManager.get_mode()


def get_patient_last_visit(phone: str):
    conn = get_db_connection()
    last_record = None
    try:
        if DatabaseManager._mode == "mysql":
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM patient_records WHERE phone = %s ORDER BY visit_date DESC LIMIT 1", (phone,))
            last_record = cursor.fetchone()
            cursor.close()
        else:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM patient_records WHERE phone = ? ORDER BY visit_date DESC LIMIT 1", (phone,))
            row = cursor.fetchone()
            if row:
                last_record = dict(row)
            cursor.close()
    finally:
        conn.close()
    return last_record


def insert_patient_record(name: str, phone: str, concern: str, department: str = "Pending Triage"):
    conn = get_db_connection()
    record_id = None
    try:
        if DatabaseManager._mode == "mysql":
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO patient_records (name, phone, last_concern, routed_department) VALUES (%s, %s, %s, %s)",
                (name, phone, concern, department)
            )
            conn.commit()
            record_id = cursor.lastrowid
            cursor.close()
        else:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO patient_records (name, phone, last_concern, routed_department, visit_date) VALUES (?, ?, ?, ?, ?)",
                (name, phone, concern, department, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            )
            conn.commit()
            record_id = cursor.lastrowid
            cursor.close()
    finally:
        conn.close()
    return record_id


def update_patient_department(phone: str, routed_department_with_slot: str):
    conn = get_db_connection()
    try:
        if DatabaseManager._mode == "mysql":
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE patient_records SET routed_department = %s WHERE phone = %s ORDER BY visit_date DESC LIMIT 1",
                (routed_department_with_slot, phone)
            )
            conn.commit()
            cursor.close()
        else:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM patient_records WHERE phone = ? ORDER BY visit_date DESC, id DESC LIMIT 1", (phone,))
            row = cursor.fetchone()
            if row:
                cursor.execute("UPDATE patient_records SET routed_department = ? WHERE id = ?", (routed_department_with_slot, row["id"]))
                conn.commit()
            cursor.close()
    finally:
        conn.close()


def get_all_patient_records(limit: int = 50):
    conn = get_db_connection()
    records = []
    try:
        if DatabaseManager._mode == "mysql":
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM patient_records ORDER BY visit_date DESC LIMIT %s", (limit,))
            records = cursor.fetchall()
            cursor.close()
        else:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM patient_records ORDER BY visit_date DESC, id DESC LIMIT ?", (limit,))
            records = [dict(r) for r in cursor.fetchall()]
            cursor.close()
    finally:
        conn.close()
    return records
