CHECK_TABLE = """
SELECT EXISTS (
    SELECT FROM 
        pg_tables
    WHERE 
        schemaname = '{}' 
    AND 
        tablename  = '{}');
"""

CREATE_TABLE = """
    CREATE TABLE 
    rss_feeds.livemint
    (
        id serial PRIMARY KEY,
        insertion_date date,
        livemint_feed json);
"""

INSERT_INTO_TABLE = """
INSERT INTO 
    rss_feeds.livemint 
    (
        insertion_date, 
        livemint_feed
    ) 
VALUES (%s, %s)"""

DATA_CHECK = "SELECT * FROM news_data.rss_feeds.livemint WHERE livemint.insertion_date='{}';"
