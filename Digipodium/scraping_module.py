from dputils.scrape import Scraper, Tag
import pandas as pd

class MyScraper:
    def __init__(self, query, page=1):
        self.query = query
        self.page = page
        self.url = f'https://www.flipkart.com/search?q=makeup&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'
        self.dataset = [ ]
    
    def collect(self):
        print(f'Collecting page {self.page}...')
        sc = Scraper(self.url)
        target = Tag(cls='__1YokD2  __3Mn1Gg')
        items = Tag(cls='__1AtVbe col-12-12')
        title = Tag(cls='__4rR01T')
        price = Tag(cls='__30jeq3 __1__WHN1')
        rating = Tag('span', cls='__2__R__DZ')
        out = sc.get_all(target, items, name=title, price=price, rr=rating)
        return out
    
    def collect_all(self):
        while True:
            result = self.collect()
            if len(result) == 0:
                break
            self.dataset.extend(result)
            self.page += 1
            self.url = f'https://www.flipkart.com/search?q=makeup&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'


    def save(self,filename):
        df = pd.DataFrame(self.dataset)
        df.dropna(how='all', inplace=True)
        df.to_csv(filename, index=False)


if __name__ == '__main__':
    # create object
    sc = MyScraper('makeup')
    # collect data
    sc.collect_all()
    # save data
    sc.save('makeup.csv')
    
