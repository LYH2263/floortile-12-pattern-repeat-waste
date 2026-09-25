from app.db import connect


def list_tiles():
    conn = connect()
    try:
        return [dict(r) for r in conn.execute("SELECT * FROM tiles ORDER BY id").fetchall()]
    finally:
        conn.close()


def get_tile(tile_id: int):
    conn = connect()
    try:
        row = conn.execute("SELECT * FROM tiles WHERE id=?", (tile_id,)).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def update_pattern_cycle(tile_id: int, pattern_cycle: float):
    conn = connect()
    try:
        cur = conn.execute(
            "UPDATE tiles SET pattern_cycle=? WHERE id=?",
            (float(pattern_cycle), tile_id),
        )
        conn.commit()
        if cur.rowcount == 0:
            return None
        row = conn.execute("SELECT * FROM tiles WHERE id=?", (tile_id,)).fetchone()
        return dict(row)
    finally:
        conn.close()
