from psycopg2.pool import ThreadedConnectionPool


class Postgres:
    def __init__(
            self, host: str, dbname: str, port: str,
            user: str, password: str,
            minconn=1, maxconn=10
    ):
        self.pool = ThreadedConnectionPool(
            minconn,
            maxconn,
            host=host,
            port=int(port),
            dbname=dbname,
            user=user,
            password=password
        )

    def query(self, query):
        result = None
        conn = self.pool.getconn()
        with conn.cursor() as cur:
            cur.execute(query)
            if 'SELECT' in query:
                result = cur.fetchall()
            else:
                conn.commit()
                result = "SUCCESS"
            cur.close()
        self.pool.putconn(conn)
        return result
