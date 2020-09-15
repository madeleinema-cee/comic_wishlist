from db import Db


class ComicData:
    def __init__(self, wishlist=False, query=None):
        self.db = Db('comic_wishlist.db')
        if wishlist:
            if query is None:
                query = '''
                       select p.PublisherName, c.title, c.covertitleid, c.description, i.issuenumber, i.issueid,
                        i.coverdate, i.covervariantdescription from WishList w
                       join Issue i on  w.issueid = i.IssueId
                       Join CoverTitle c on i.covertitleid = c.covertitleid
                       join Publisher p on p.publisherid = c.publisherid
                       Order by PublisherName, title, issuenumber
                       '''

                self.results = self.db.fetchall(query)
            else:
                query = query
                self.results = self.db.fetchall(query)
        else:
            if query is None:
                query = '''
                        select p.PublisherName, c.title, c.covertitleid, c.description, i.issuenumber, i.issueid,
                         i.coverdate, i.covervariantdescription, u.cgccolor, u.cgcscore, u.cgccomments from Issue i
                        join UserIssue u on u.issueid = i.issueid
                        Join CoverTitle c on i.covertitleid = c.covertitleid
                        join Publisher p on p.publisherid = c.publisherid
                        Order by PublisherName, title, issuenumber
                        '''
                self.results = self.db.fetchall(query)
            else:
                query = query
                self.results = self.db.fetchall(query)

    def parse_data(self, wishlist= False):
        if wishlist:
            data = {}
            for row in self.results:
                pub_name = row['PublisherName']

                if pub_name not in data:
                    data[pub_name] = {
                        row['Title']: [
                            {'title_id': row['CoverTitleID'],
                             'cover_desc': row['Description'],
                             'issue_number': row['IssueNumber'],
                             'date': row['CoverDate'],
                             'desc': row['CoverVariantDescription'],
                             'issue_id': row['IssueID'],
                             'cover_id': row['IssueID'][0:3]}]
                    }

                else:
                    if row['Title'] not in data[pub_name]:
                        data[pub_name][row['Title']] = [
                            {'title_id': row['CoverTitleID'],
                             'cover_desc': row['Description'],
                             'issue_number': row['IssueNumber'],
                             'date': row['CoverDate'],
                             'desc': row['CoverVariantDescription'],
                             'issue_id': row['IssueID'],
                             'cover_id': row['IssueID'][0:3]}]

                    else:
                        data[pub_name][row['Title']].append(
                            {'title_id': row['CoverTitleID'],
                             'cover_desc': row['Description'],
                             'issue_number': row['IssueNumber'],
                             'date': row['CoverDate'],
                             'desc': row['CoverVariantDescription'],
                             'issue_id': row['IssueID'],
                             'cover_id': row['IssueID'][0:3]})
            return data

        else:
            data = {}
            for row in self.results:
                pub_name = row['PublisherName']

                if pub_name not in data:
                    data[pub_name] = {
                        row['Title']: [
                            {'title_id': row['CoverTitleID'],
                             'cover_desc': row['Description'],
                             'issue_number': row['IssueNumber'],
                             'date': row['CoverDate'],
                             'desc': row['CoverVariantDescription'],
                             'color': row['CGCColor'],
                             'score': row['CGCScore'],
                             'comment': row['CGCComments'],
                             'issue_id': row['IssueID'],
                             'cover_id': row['IssueID'][0:3]}]
                    }

                else:
                    if row['Title'] not in data[pub_name]:
                        data[pub_name][row['Title']] = [
                            {'title_id': row['CoverTitleID'],
                             'cover_desc': row['Description'],
                             'issue_number': row['IssueNumber'],
                             'date': row['CoverDate'],
                             'desc': row['CoverVariantDescription'],
                             'color': row['CGCColor'],
                             'score': row['CGCScore'],
                             'comment': row['CGCComments'],
                             'issue_id': row['IssueID'],
                             'cover_id': row['IssueID'][0:3]}]

                    else:
                        data[pub_name][row['Title']].append(
                            {'title_id': row['CoverTitleID'],
                             'cover_desc': row['Description'],
                             'issue_number': row['IssueNumber'],
                             'date': row['CoverDate'],
                             'desc': row['CoverVariantDescription'],
                             'color': row['CGCColor'],
                             'score': row['CGCScore'],
                             'comment': row['CGCComments'],
                             'issue_id': row['IssueID'],
                             'cover_id': row['IssueID'][0:3]})

            return data



if __name__ == '__main__':
    d = ComicData()
    d.parse_data()
