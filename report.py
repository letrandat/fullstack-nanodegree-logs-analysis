#!/usr/bin/env python2
from common import psql_util


def _get_most_popular_three_articles():
	"""
	Get the most popular 3 articles with format
	title - {num views} views
	line break
	"""
	print "The most popular three articles of all time:"
	sql = """
		select title, views
		from article_views 
		order by views desc 
		limit 3;
		"""
	query_result = psql_util.execute(sql)
	for row in query_result:
		print "{title} - {views} views".format(title=row[0], views=row[1])

	print ""


def _get_the_most_popular_article_authors_of_all_time():
	print "The most popular article authors of all time:"
	sql = """
		select authors.name, sum(article_views.views) as total_views
		from authors 
			join article_views 
			on authors.id = article_views.author
		group by authors.id
		order by total_views desc;
		"""

	query_result = psql_util.execute(sql)
	for row in query_result:
		print "{name} - {views} views".format(name=row[0], views=row[1])

	print ""


def _get_which_days_did_more_than_1_percent_of_requests_lead_to_errors():
	print "which days did more than 1% of requests lead to errors:"
	sql = """
		select *
		from daily_error_date
		where error_rate > 1
		"""

	query_result = psql_util.execute(sql)
	for row in query_result:
		print "{date} - {error_rate}% errors".format(date=row[0], error_rate=row[1])


def main():
	_get_most_popular_three_articles()
	_get_the_most_popular_article_authors_of_all_time()
	_get_which_days_did_more_than_1_percent_of_requests_lead_to_errors()


if __name__ == "__main__":
	main()
