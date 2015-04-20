#!/usr/bin/env python
# coding:utf-8

"""

"""

import os
import datetime
import codecs
from xml.etree import ElementTree


def gen(path, dst_dir):
    root = ElementTree.parse(path)
    head = root.find('Header')
    body = root.find('Body').text
    title = head.find('Title').text
    date_str = head.find('CreatedAt').text[:19]
    tags = head.find('Tags')
    cat = head.find('Category').text
    link = head.find('PermaLink').text
    date = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")

    cat = 'life'

    name = "{}-{}.md".format(date.strftime('%Y-%m-%d'), link)
    dst_path = os.path.join(dst_dir, name)

    with codecs.open(dst_path, 'w', 'utf-8') as f:
        f.write('---\n')
        f.write(u'title: "{}"\n'.format(title))
        if cat:
            f.write('category: {}\n'.format(cat))
        if tags is not None:
            f.write('tags: [{}]\n'.format(tags.text))
        f.write('---\n\n')
        f.write(body)


def gen_all(dir_path, dst_dir):
    if not os.path.exists(dst_dir):
        os.mkdir(dst_dir)
    import glob
    for path in glob.glob(os.path.join(dir_path, '*.xml')):
        gen(path, dst_dir)


if __name__ == '__main__':
    gen_all('baidu_posts', 'posts')
