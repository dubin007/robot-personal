from src.spider.TXSpider import TXSpider
import multiprocessing

def start_tx_spider():
    p = multiprocessing.Process(target=TXSpider)
    p.start()

if __name__=='__main__':
    pass