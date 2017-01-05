from urllib.parse import urlparse
import time
import feedparser
import sqlite3

def print_list(string_list):
    """print each string in list"""
    for element in string_list:
        if isinstance(element, dict):
            for key in element.keys():
                print("\t{0}: {1}".format(key, element[key]), end='')
        else:
            print("\t{0}".format(element), end='')

def main():
    """ This is the main function """
    # Display current time
    now = time.strftime("%c")
    print(now)
    print("------------------------------------------------------------")
    # --------------------
    #  (feedparser)
    # --------------------

    target_website = 'craigslist'
    conn = sqlite3.connect(target_website + '.db')
    print("Opened database successfully")
    conn.execute("drop table if exists Post_history")
    conn.execute("drop table if exists Post")


    conn.execute('''CREATE TABLE IF NOT EXISTS Post_History
        (ID INTEGER PRIMARY KEY   AUTOINCREMENT,
            PostID         TEXT   NOT NULL,
        Cost            INT     NOT NULL,
        SysCreateDate       DATETIME    NOT NULL
        );''')
    print("Table created successfully")

    conn.execute('''CREATE TABLE IF NOT EXISTS Post
        (PostID         TEXT PRIMARY KEY     NOT NULL,
        Link            TEXT,
        Description            TEXT,
        PostDate            DateTime,
        Language            char(255),
        Source            TEXT,
        Title             Text,
        Type              Char(255),
        IssueDate           DATETIME
        SysCreateDate       DATETIME    NOT NULL
        );''')

    #parseUrl = 'https://vancouver.craigslist.ca/search/sso?format=rss&query=macbook%20pro%2016gb&sort=rel'
    file_to_parse = 'C:\\Users\\Mansun\\Dropbox\\Learning\\Python\\RssParser\\sample.xml'
    current_feed = feedparser.parse(file_to_parse)
    print("{0}: {1}".format("version", current_feed.version))

    for post in current_feed.entries:
        print("Processing: {0}".format(post.title), end='')

        # Get item ID
        item_url = urlparse(post.dc_source)
        url = item_url.geturl()
        item_id = url[url.rfind('/')+1:url.rfind('.')]

        # Get item cost
        post_title = post.title
        item_cost = post_title[post_title.rfind('&#x0024;'):].replace('&#x0024;', '')

        post_history_insert_sql = "INSERT INTO Post_History (PostID, Cost, SysCreateDate) VALUES('{0}', '{1}', '{2}')".format(
            item_id, item_cost, time.strftime('%Y-%m-%d %H:%M:%S'))

        try:
            conn.execute(post_history_insert_sql)
            # conn.execute("INSERT INTO Post (PostID, Link, Description, PostDate, Language, Source, Title, Type, IssueDate,SysCreateDate) VALUES(?,?,?,?,?,?,?,?,?,?)",
            # [(item_id, post.link, post.description, post.post )])
        except sqlite3.Error as er:
            print('database error {0}'.format(er))
        #print(post.about, end='')
    #    count += 1

    print("Script completes.")

if __name__ == '__main__':
    main()
