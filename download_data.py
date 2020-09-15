import xlsxwriter
from find_data import ComicData


class ExcelCovert:
    def __init__(self, wishlist='False', one_sheet='False'):
        if one_sheet == 'False':
            if wishlist == 'True':
                w = ComicData(wishlist=True)
                self.data = w.parse_data(wishlist=True)
                self.output_file = 'comic_wishlist/wishlist(multi_sheet).xlsx'
            else:
                c = ComicData(wishlist=False)
                self.data = c.parse_data(wishlist=False)
                self.output_file = 'comic_wishlist/collection(multi_sheet).xlsx'
        else:
            if wishlist == 'True':
                w = ComicData(wishlist=True)
                self.data = w.parse_data(wishlist=True)
                self.output_file = 'comic_wishlist/wishlist(one_sheet).xlsx'
            else:
                c = ComicData(wishlist=False)
                self.data = c.parse_data(wishlist=False)
                self.output_file = 'comic_wishlist/collection(one_sheet).xlsx'

        self.workbook = xlsxwriter.Workbook(self.output_file)
        self.worksheet = None
        self.bold_format = self.workbook.add_format({'bold': True})

        self.row = 0

    def download_multi_sheet(self, wishlist='False'):
        for pub, comic_list in self.data.items():
            self.row = 1
            self.worksheet = self.workbook.add_worksheet(
                self.format_publisher_for_sheet_name(pub))
            for title, issues in comic_list.items():
                for issue in issues:
                    self.write_issue_data_to_output_file(title, issue)
                    self.row += 1

        self.workbook.close()

    def download_one_sheet(self):
        self.write_headers_one_sheet()
        self.row = 1
        for pub, comic_list in self.data.items():
            for title, issues in comic_list.items():
                for issue in issues:
                    self.worksheet.write(self.row, 0, pub)
                    self.worksheet.write(self.row, 1, title)
                    self.worksheet.write(self.row, 2, issue['cover_desc'])
                    self.worksheet.write(self.row, 3, issue['issue_number'])
                    self.worksheet.write(self.row, 4, issue['date'])
                    self.worksheet.write(self.row, 5, issue['desc'])
                    self.row += 1
        self.workbook.close()


    @staticmethod
    def format_publisher_for_sheet_name(publisher_name):
        publisher_name = publisher_name.replace(':', '')
        if len(publisher_name) >= 31:
            publisher_name = f'{publisher_name[0:27]}...'
        return publisher_name

    def write_headers_one_sheet(self):
        self.worksheet = self.workbook.add_worksheet()
        self.worksheet.write(0, 0, 'Publisher', self.bold_format)
        self.worksheet.write(0, 1, 'Title', self.bold_format)
        self.worksheet.write(0, 2, 'Description', self.bold_format)
        self.worksheet.write(0, 3, 'IssueNumber', self.bold_format)
        self.worksheet.write(0, 4, 'CoverDate', self.bold_format)
        self.worksheet.write(0, 5, 'CoverVariantDescription', self.bold_format)

    def write_headers_multi_sheet(self):
        self.worksheet.write(0, 0, 'Title', self.bold_format)
        self.worksheet.write(0, 1, 'Description', self.bold_format)
        self.worksheet.write(0, 2, 'IssueNumber', self.bold_format)
        self.worksheet.write(0, 3, 'CoverDate', self.bold_format)
        self.worksheet.write(0, 4, 'CoverVariantDescription', self.bold_format)

    def write_issue_data_to_output_file(self, title, issue):
        self.worksheet.write(self.row, 0, title)
        self.worksheet.write(self.row, 1, issue['cover_desc'])
        self.worksheet.write(self.row, 2, issue['issue_number'])
        self.worksheet.write(self.row, 3, issue['date'])
        self.worksheet.write(self.row, 4, issue['desc'])


if __name__ == '__main__':
    c = ExcelCovert()
    c.download_one_sheet()
