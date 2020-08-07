from db import Db


class CollectionData:
    def __init__(self):
        self.db = Db('comic_wishlist.db')

    # Issue.coverdate, issue.covervariant, issue.covervariantdescription, Issue.version

    def retrieve_data(self):
        query = '''
        select p.PublisherName, c.title, c.covertitleid, i.issuenumber, i.issueid, i.coverdate, i.covervariantdescription from Issue i
        Join CoverTitle c on i.covertitleid = c.covertitleid
        join Publisher p on p.publisherid = c.publisherid
        Order by PublisherName, title, issuenumber
        '''

        results = self.db.fetchall(query)
        return results

    def parse_data(self):
        data = {}

        for row in self.retrieve_data():
            pub_name = row['PublisherName']

            if pub_name not in data:
                data[pub_name] = {
                    row['Title']: [
                        {'title_id': row['CoverTitleID'],
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
                         'issue_number': row['IssueNumber'],
                         'date': row['CoverDate'],
                         'desc': row['CoverVariantDescription'],
                         'issue_id': row['IssueID'],
                         'cover_id': row['IssueID'][0:3]}]

                else:
                    data[pub_name][row['Title']].append(
                        {'title_id': row['CoverTitleID'],
                         'issue_number': row['IssueNumber'],
                         'date': row['CoverDate'],
                         'desc': row['CoverVariantDescription'],
                         'issue_id': row['IssueID'],
                         'cover_id': row['IssueID'][0:3]})

        return data


if __name__ == '__main__':
    d = CollectionData()
    d.retrieve_data()
    d.parse_data()


