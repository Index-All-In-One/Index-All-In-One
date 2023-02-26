import sqlite3

class PluginInstanceDb:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()

        self.c.execute(
            """CREATE TABLE IF NOT EXISTS request_table
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    request_op TEXT,
                    plugin_name TEXT,
                    plugin_instance_id TEXT,
                    update_interval INTEGER)"""
        )
        self.conn.commit()

    def add_request(self, request_args):
        (request_op, plugin_name, plugin_instance_id, update_interval) = request_args

        self.c.execute(
            "INSERT INTO request_table (request_op, plugin_name, plugin_instance_id, update_interval) VALUES (?, ?, ?, ?)",
            (request_op, plugin_name, plugin_instance_id,update_interval),
        )
        self.conn.commit()

    def get_next_request(self):
        self.c.execute(
            "SELECT id, request_op, plugin_name, plugin_instance_id, update_interval FROM request_table ORDER BY id ASC LIMIT 1",
        )
        PI_request = self.c.fetchone()

        if PI_request:
            self.c.execute(
                "DELETE FROM request_table WHERE id = ?", (PI_request[0],),
            )
            self.conn.commit()

            return (PI_request[1], PI_request[2], PI_request[3], PI_request[4])
        else:
            return None

    def __del__(self):
        self.conn.close()

def PI_db_test():
    db = PluginInstanceDb("PI_test.db")
    assert db.get_next_request() == None
    db.add_request(("add", "Plugin1", "", 1000))
    assert db.get_next_request() == ("add", "Plugin1", "" , 1000)
    db.add_request(("del", "Plugin2", "cwiu3h4t2ir", 314159))
    assert db.get_next_request() == ("del", "Plugin2", "cwiu3h4t2ir", 314159)
    assert db.get_next_request() == None


if __name__ == "__main__":
    PI_db_test()
