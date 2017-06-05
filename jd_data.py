import argparse
from pymongo import MongoClient
from jd_spider import JDong


client = MongoClient('mongodb://localhost:27017')
db = client.jd


def print_search_result(results):
    for result in results:
        print "=========================================="
        print "UID: %s" % result['uid']
        print "Link: %s" % result['link']
        print "Name: %s" % result['name']
        print "Comments: %s" % result['comment']
        print "Price: %s%s" % (result['price_type'], result['price_data'])
        print "Image: %s" % result['img']


def print_color_size(color_sizes):
    for color_size in color_sizes:
        print "=========================================="
        for key, value in color_size.items():
            print key, value


def print_comments(comments):
    for comment in comments:
        print "=========================================="
        print comment['content']


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', dest='keyword', help='specify search keyword')
    parser.add_argument('-p', dest='page', help='specify comment page number', default=0, type=int)
    args = parser.parse_args()
    keyword = args.keyword
    comment_page = args.page
    if keyword == None:
        parser.print_help()
        exit(0)

    # Search
    jd = JDong()
    results = jd.search(keyword)
    print "[+] Performing a search for %s" % keyword
    print "[+] Total result: %d" % len(results)
    print "[+] Listing the top 10"
    print_search_result(results[:10])

    # UID
    uid = results[0]['uid']
    link = results[0]['link']
    print "[+] Looking into the first item: %s" % uid
    print "[+] Link: " + link

    # SKU
    print "[+] Looking into the sku items"
    color_sizes = jd.get_color_size(uid)
    print_color_size(color_sizes)

    # Comment Pages
    comment_pages = jd.get_comment_page(uid)
    print "[+] Total comment pages: %s" % comment_pages

    # Comments
    comments = jd.comment(uid, comment_page).get('comments')
    print "[+] Reading comments on page %d" % comment_page
    print_comments(comments)


if __name__ == '__main__':
    main()
