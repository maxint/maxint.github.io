#!/usr/bin/env python
# coding:utf-8

from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint

import re
import os


class Html2MarkdownParser(HTMLParser):
    def __init__(self):
        self._markdown = ''
        self._tag_stack = []
        self._tag_attr_data = {}
        self._handled_tag_body_data = ''
        self._convertible_tags = ['a', 'img', 'div',
                                  'b', 'blockquote',
                                  'em',
                                  'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr',
                                  'ol',
                                  'p', 'pre', 'br', 'span',
                                  'strong',
                                  'ul']
        self._ignore_tags = ['li', 'font', 'code', 'embed']
        self._table_tags = ['tbody', 'table', 'tr', 'td']
        # FIXME: special characters
        HTMLParser.__init__(self)

    def _append_to_markdown(self, new_markdown):
        if len(self._markdown) > 1:
            if re.match('\s', self._markdown[-1:]):
                self._markdown += new_markdown
            else:
                self._markdown += ' ' + new_markdown
        else:
            self._markdown += new_markdown

    # <a />
    def handle_start_a(self, attrs):
        self._tag_attr_data = dict(attrs)

    def handle_end_a(self):
        a_tag = ''
        a_tag += '[' + self._handled_tag_body_data + ']'
        a_tag += '(' + self._tag_attr_data.get('href').encode('utf-8')

        title = self._tag_attr_data.get('title')
        if title:
            a_tag += ' "' + title + '")'
        else:
            a_tag += ')'
        if self._handled_tag_body_data and self.lasttag == 'img':
            a_tag += os.linesep
        else:
            a_tag += ' '
        self._append_to_markdown(a_tag)

    # <img />
    def handle_start_img(self, attrs):
        attrs = dict(attrs)
        a_tag = '!'
        a_tag += '[' + attrs.get('alt', '') + ']'
        a_tag += '(' + attrs.get('src')

        title = attrs.get('title')
        if title:
            a_tag += ' "' + title + '")'
        else:
            a_tag += ')'

        if 'a' in self._tag_stack:
            self._handled_tag_body_data += a_tag
        else:
            self._append_to_markdown(a_tag)

    # <div />
    def handle_start_div(self, attrs):
        self.handle_start_p(attrs)

    def handle_end_div(self):
        if self._handled_tag_body_data:
            self.handle_end_p()

    # <b />
    def handle_end_b(self):
        self._handled_tag_body_data = self._handled_tag_body_data.replace(os.linesep, ' ')
        self._append_to_markdown('*' + self._handled_tag_body_data + '*')

    # <blockquote />
    def handle_end_blockquote(self):
        blockquote_body = self._handled_tag_body_data.split(os.linesep)

        for blockquote_line in blockquote_body:
            blockquote_line = blockquote_line.strip()
            self._append_to_markdown('> ' + blockquote_line + os.linesep)

    # <em />
    def handle_end_em(self):
        self._handled_tag_body_data = self._handled_tag_body_data.replace(os.linesep, ' ')
        self._append_to_markdown('*' + self._handled_tag_body_data + '*')

    def prepare_header_body_data(self):
        self._handled_tag_body_data = self._handled_tag_body_data.replace(os.linesep, ' ')
        if self._markdown[-2:] != '%s%s' % (os.linesep, os.linesep):
            self._markdown += os.linesep + os.linesep

    # <h1 />
    def handle_end_h1(self):
        self.prepare_header_body_data()
        self._append_to_markdown('\n# ' + self._handled_tag_body_data + ' #' + os.linesep)

    # <h2 />
    def handle_end_h2(self):
        self.prepare_header_body_data()
        self._append_to_markdown('\n## ' + self._handled_tag_body_data + ' ##' + os.linesep)

    # <h3 />
    def handle_end_h3(self):
        self.prepare_header_body_data()
        self._append_to_markdown('\n### ' + self._handled_tag_body_data + ' ###' + os.linesep)

    # <h4 />
    def handle_end_h4(self):
        self.prepare_header_body_data()
        self._append_to_markdown('\n#### ' + self._handled_tag_body_data + ' ####' + os.linesep)

    # <h5 />
    def handle_end_h5(self):
        self.prepare_header_body_data()
        self._append_to_markdown('\n##### ' + self._handled_tag_body_data + ' #####' + os.linesep)

    # <h6 />
    def handle_end_h6(self):
        self.prepare_header_body_data()
        self._append_to_markdown('\n###### ' + self._handled_tag_body_data + ' ######' + os.linesep)

    # <hr />
    def handle_start_hr(self, attrs):
        self._append_to_markdown('* * *' + os.linesep)

    # <li />
    def handle_end_li(self):
        if len(self._tag_stack):
            if self._tag_stack[-1] == 'ol':
                self._append_to_markdown('1.    ' + self._handled_tag_body_data + os.linesep)
            elif self._tag_stack[-1] == 'ul':
                self._append_to_markdown('*    ' + self._handled_tag_body_data + os.linesep)

    # <p />
    def handle_start_p(self, attrs):
        if len(self._markdown) > 1:
            if self._markdown[-2:] == '%s%s' % (os.linesep, os.linesep):
                pass
            elif self._markdown[-1:] == os.linesep:
                self._markdown += os.linesep
            else:
                self._markdown += os.linesep + os.linesep

    def handle_end_p(self):
        self._markdown += '%s%s' % (os.linesep, os.linesep)

    # <br />
    def handle_start_br(self, attrs):
        if 'pre' in self._tag_stack:
            self._handled_tag_body_data += os.linesep

    # <pre />
    def handle_start_pre(self, attrs):
        if self._markdown[-2:] != '%s%s' % (os.linesep, os.linesep):
            self._markdown += os.linesep + os.linesep
        self._append_to_markdown('```' + os.linesep)

    def handle_end_pre(self):
        code_lines = self._handled_tag_body_data.split('\n')
        for code_line in code_lines:
            self._append_to_markdown(code_line + os.linesep)
        self._append_to_markdown('```' + os.linesep)

    # <span />
    def handle_end_span(self):
        self._append_to_markdown(self._handled_tag_body_data)

    # <strong />
    def handle_end_strong(self):
        self._handled_tag_body_data = self._handled_tag_body_data.replace(os.linesep, ' ')
        self._append_to_markdown('**' + self._handled_tag_body_data + '**')

    ## ###
    def handle_starttag(self, tag, attrs):
        self._tag_stack.append(tag)
        try:
            eval('self.handle_start_' + tag + '(attrs)')
        except AttributeError, e:
            if tag not in (self._convertible_tags + self._ignore_tags):
                print 'start', tag
                self._append_to_markdown(self._handled_tag_body_data)
                if tag not in self._table_tags:
                    self._append_to_markdown('<' + tag)
                    if attrs:
                        for n, v in attrs:
                            self._markdown += ' ' + ('{}="{}"'.format(n, v) if v else n)
                    self._markdown += '>'

                self._handled_tag_body_data = ''
                if tag != 'td' and self._markdown[-1:] != os.linesep:
                    self._handled_tag_body_data += os.linesep
            pass

    def handle_endtag(self, tag):
        if not self._tag_stack:
            return

        self._tag_stack.pop()
        try:
            eval('self.handle_end_' + tag + '()')
            # Collapse three successive CRs into two before moving on
            while len(self._markdown) > 2 and\
                  self._markdown[-3:] == '%s%s%s' % (os.linesep, os.linesep, os.linesep):
                self._markdown = self._markdown[:-3] + '%s%s' % (os.linesep, os.linesep)
        except AttributeError, e:
            if tag not in (self._convertible_tags + self._ignore_tags):
                print 'end', tag
                self._append_to_markdown(self._handled_tag_body_data)
                if 'pre' not in self._tag_stack and tag not in self._table_tags:
                    self._append_to_markdown('</%s>' % tag)
            pass

        self._tag_attr_data = {}
        self._handled_tag_body_data = ''

    def handle_data(self, data):
        data = os.linesep.join(data.strip().split(os.linesep))
        if len(self._tag_stack) and self._tag_stack[-1] not in ['p']:
            self._handled_tag_body_data += data
        else:
            self._append_to_markdown(data)

    def handle_charref(self, name):
        if 'pre' in self._tag_stack:
            if name.startswith('x'):
                c = unichr(int(name[1:], 16))
            else:
                c = unichr(int(name))
            self._handled_tag_body_data += c.encode('utf-8')
        else:
            self._handled_tag_body_data = name

    def handle_entityref(self, name):
        if 'pre' in self._tag_stack:
            try:
                c = unichr(name2codepoint[name])
                self._handled_tag_body_data += c.encode('utf-8')
            except:
                print 'Ignore entityref', name
        else:
            self._handled_tag_body_data = name

    def get_markdown(self):
        return self._markdown.rstrip() + '\n'


def convert_file(path):
    try:
        s0 = open(path).read()
        s0 = s0.replace('　', '')
        s0 = s0.replace('<br>', os.linesep)
        s0 = s0.replace('<br><br/>', os.linesep)
        p = Html2MarkdownParser()
        p.feed(s0)
        p.close()
        s = p.get_markdown()
        print s
        open(path, 'wt').write(s)
    except SyntaxError, e:
        print '  Ignore markdown code'
    except Exception, e:
        print ' ', e
        raise



def convert_all(pattern):
    import glob
    for path in glob.glob(pattern):
        print 'Converting', path
        convert_file(path)


if __name__ == '__main__':
    # import argparse
    #
    # parser = argparse.ArgumentParser(description='Convert HTML to Markdown')
    # parser.add_argument('path', help='file to be processed')
    #
    # args = parser.parse_args()
    #
    # convert_all(args.path)

    convert_all('../_posts/*.md')
    # convert_file('../_posts/2009-09-09-167552924.md')
    # convert_file('../_posts/2010-01-09-189668670.md')
    # convert_file('../_posts/2009-06-01-149027288.md')
    # convert_file('../_posts/2013-06-01-how-setup-this-blog.md')
    # convert_file('../_posts/2008-03-29-zju-acm.md')
    # convert_file('../_posts/2010-09-23-243559145.md')
    # convert_file('../_posts/2008-09-04-109600544.md')
    # convert_file('../_posts/2008-07-28-102875886.md')