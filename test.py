INF = 'INF'
graph = {'A':{'A':0,'B':6,'C':INF,'D':6,'E':7},

         'B':{'A':INF,'B':0,'C':5,'D':INF,'E':INF},

         'C':{'A':INF,'B':INF,'C':0,'D':9,'E':3},

         'D':{'A':INF,'B':INF,'C':9,'D':0,'E':7},

         'E':{'A':INF,'B':4,'C':INF,'D':INF,'E':0}
         }
import pandas as pd
pd.DataFrame(graph).to_csv('OUTPUT.xls')


import pandas as pd


def covert_data_to_excel(self):
    conn = sqlite3.connect('comic_wishlist.db', isolation_level=None,
                           detect_types=sqlite3.PARSE_COLNAMES)
    db = pd.read_sql_query('''select p.PublisherName, c.title, c.covertitleid, i.issuenumber, i.issueid, i.coverdate, i.covervariantdescription from WishList w join Issue i on  w.issueid = i.IssueId Join CoverTitle c on i.covertitleid = c.covertitleid
    join Publisher p on p.publisherid = c.publisherid
    Order by PublisherName, title, issuenumber''', conn)
    db.to_excel('test.xls', index=False)


