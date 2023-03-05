import sqlite3


class TaskDb:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()

        self.c.execute(
            """CREATE TABLE IF NOT EXISTS tasks
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_op TEXT,
                    task_id TEXT,
                    status TEXT)"""
        )
        self.conn.commit()

    def add_task(self, task_args):
        (task_op, task_id) = task_args

        self.c.execute(
            "INSERT INTO tasks (task_op, task_id, status) VALUES (?, ?, ?)",
            (task_op, task_id, "queued"),
        )
        self.conn.commit()

    def get_next_task(self):
        self.c.execute(
            "SELECT id, task_op, task_id FROM tasks WHERE status = ? ORDER BY id ASC LIMIT 1",
            ("queued",),
        )
        task = self.c.fetchone()

        if task:
            self.c.execute(
                "UPDATE tasks SET status = ? WHERE id = ?", ("in_progress", task[0])
            )
            self.conn.commit()

            return (task[1], task[2])
        else:
            return None

    def mark_task_complete(self, task_args):
        (task_op, task_id) = task_args
        self.c.execute(
            "UPDATE tasks SET status = ? WHERE task_op = ? AND task_id = ?",
            ("complete", task_op, task_id),
        )
        self.conn.commit()

    def __del__(self):
        self.conn.close()


def tast_db_test():
    db = TaskDb("tasks.db")
    assert db.get_next_task() == None
    db.add_task(("update", "task1"))
    assert db.get_next_task() == ("update", "task1")
    db.add_task(("update", "task2"))
    assert db.get_next_task() == ("update", "task2")
    assert db.get_next_task() == None


if __name__ == "__main__":
    tast_db_test()
