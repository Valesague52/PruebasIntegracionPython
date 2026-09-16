import sqlite3
import pytest
from db.repo import SQLiteUserRepository
from layers.service import UserService

def test_user_service_with_sqlite_in_memory():
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.executescript(
        """
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            first TEXT NOT NULL,
            last  TEXT NOT NULL
        );
        INSERT INTO users (id, first, last) VALUES (1, 'Ada', 'Lovelace');
        INSERT INTO users (id, first, last) VALUES (2, 'Alan', 'Turing');
        """
    )
    conn.commit()

    repo = SQLiteUserRepository(conn)
    service = UserService(repo)

    assert service.get_full_name(1) == "Ada Lovelace"
    assert service.get_full_name(2) == "Alan Turing"
    assert service.get_full_name(999) is None

def test_sqlite_insert_invalid_user_violates_not_null():
    # Creamos la base de datos en memoria con los constraints NOT NULL
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.executescript(
        """
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            first TEXT NOT NULL,
            last  TEXT NOT NULL
        );
        """
    )
    conn.commit()

    # Intentamos insertar un registro con 'first' como NULL, lo cual debe fallar por el constraint
    with pytest.raises(sqlite3.IntegrityError):
        cur.execute(
            "INSERT INTO users (id, first, last) VALUES (?, ?, ?)",
            (10, None, "Invalido")
        )
        conn.commit()