import testingtools
import crawler
import searchdata
import search
crawler.crawl('http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html')
print(search.search('banana papaya banana papaya orange',True))
