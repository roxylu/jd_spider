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


def print_color_size(sku_list):
    for color_size in sku_list:
        print "=========================================="
        for key, value in color_size.items():
            print key, value


def print_comments(comments):
    for comment in comments:
        print "=========================================="
        print comment['content']


def bulk_update_collection(entries, key, collection="products"):
    """
    Perform bulk update to collection to keep it updated.
    Insert a new entry if key does not exist.
    Using products collection by default.
    """
    for entry in entries:
        db[collection].update({key: entry[key]}, entry, upsert=True)


def update_fields(key_name, key_value, field, value, collection="products"):
    """
    Update field with provided value for entries
    that match key_name - key_value.
    Using products collection by default.
    """
    db[collection].update({key_name: key_value}, {"$set": {field: value}})


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', dest='keyword', help='specify search keyword')
    parser.add_argument('-p', dest='page', help='specify comment page number', default=0, type=int)
    args = parser.parse_args()
    keyword = args.keyword
    comment_page = args.page
    if keyword is None:
        parser.print_help()
        exit(0)

    # Search
    jd = JDong()
    results = jd.search(keyword)
    print "[+] Performing a search for %s" % keyword
    print "[+] Total result: %d" % len(results)
    print "[+] Listing the top 10"
    print_search_result(results[:10])
    bulk_update_collection(results, "uid")

    # UID
    uid = results[0]['uid']
    link = results[0]['link']
    print "[+] Looking into the first item: %s" % uid
    print "[+] Link: " + link

    # SKU
    print "[+] Looking into the sku items"
    sku_list = jd.get_color_size(uid)
    print_color_size(sku_list)
    update_fields("uid", uid, "sku", sku_list)

    # Comment Pages
    comment_pages = jd.get_comment_page(uid)
    print "[+] Total comment pages: %s" % comment_pages
    update_fields("uid", uid, "comment_pages", comment_pages)

    # Comments
    comments = jd.comment(uid, comment_page).get('comments')
    print "[+] Reading comments on page %d" % comment_page
    print_comments(comments)
    bulk_update_collection(comments, "id", collection="comments")


if __name__ == '__main__':
    main()
