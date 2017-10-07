import psycopg2


def execute(sql, db_name="news", *args, **kwargs):
	"""
	Execute a sql command to a db_name and
	automatically close the connection after that
	:param sql: input sql
	:param db_name: default as news
	:param args: reserved
	:param kwargs: reserved
	:return: query result
	"""
	with psycopg2.connect("dbname={}".format(db_name)) as conn:
		with conn.cursor() as curs:
			curs.execute(sql, *args, **kwargs)
			query_result = curs.fetchall()
			conn.commit()
			return query_result
