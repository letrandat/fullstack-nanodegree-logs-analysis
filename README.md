# Logs Analysis

## Prepare the software and data
1. Download and install a virtual machine [here](https://classroom.udacity.com/nanodegrees/nd004/parts/8d3e23e1-9ab6-47eb-b4f3-d5dc7ef27bf0/modules/bc51d967-cb21-46f4-90ea-caf73439dc59/lessons/5475ecd6-cfdb-4418-85a2-f2583074c08d/concepts/14c72fe3-e3fe-4959-9c4b-467cf5b7c3a0)
2. Download the data [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
3. To load the data, cd into the vagrant directory and use the command `psql -d news -f newsdata.sql`

## What report does the tool show?
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?


## Create views for project

Run the following commands to create views before run the script

1. `articles_views` view contains article title and view

```
drop view article_views;
create view article_views as
    select articles.author, articles.title, paths_views.views
    from (
        select path, count(*) as views
        from log
        where status = '200 OK'
        group by path
    ) as paths_views
    right join articles
        on paths_views.path like ('/article/' || articles.slug);
```

2. `daily_error_date` view to support "On which days did more than 1% of requests lead to errors?"

```
drop view daily_error_date;
create view daily_error_date as
    select daily_request.date, round(daily_error.error_request * 100.0 / daily_request.total_request, 2) as error_rate
    from (
        select time::date as date, count(*) as total_request
        from log
        group by date
    ) as daily_request
        join (
        select time::date as date, count(*) as error_request
        from log
        where status != '200 OK'
        group by date
    ) as daily_error
        on daily_request.date = daily_error.date;
```

## How to run report?

execute the script

```
python report.py
```

## Result

```
The most popular three articles of all time:
Candidate is jerk, alleges rival - 338647 views
Bears love berries, alleges bear - 253801 views
Bad things gone, say good people - 170098 views

The most popular article authors of all time:
Ursula La Multa - 507594 views
Rudolf von Treppenwitz - 423457 views
Anonymous Contributor - 170098 views
Markoff Chaney - 84557 views

which days did more than 1% of requests lead to errors:
2016-07-17 - 2.26% errors
```
