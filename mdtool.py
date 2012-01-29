#!/usr/bin/env python

# Copyright (C) 2012 Andrew G. Crowell
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import re
import os
import sys
import markdown # Requires Python-Markdown.
import xml.etree.ElementTree
import pprint

def listdir(base, extensions):
    result = []
    for path in os.listdir(base):   
        path = os.path.join(base, path)
        if os.path.isdir(path):
            result.extend(listdir(path, extensions))
        elif os.path.isfile(path) and os.path.splitext(path)[1].lower() in extensions:
            result.append(os.path.normpath(path))
    return result

def build_toc(content):
    ids = set()
    toc = []
    stack = []
    depth = 0
    parent = (toc,)
    for item in list(content):
        tag = item.tag
        if tag[0] == 'h' and tag[1].isdigit():
            tag_depth = int(tag[1])
            # Trim leading whitspace, and convert to lowercase.
            tag_id = item.text.lstrip().lower()
            # Replace spaces with dashes.
            tag_id = re.sub('[ \t]', '-', tag_id)
            # Strip weird special characters.
            tag_id = re.sub('[^-a-zA-Z0-9._]', '', tag_id)
            # Strip trailing underscores/dashes/dots
            tag_id = tag_id.rstrip('_-.')
            
            if tag_id in ids:
                n = 1
                conflict_id = tag_id
                while conflict_id in ids:
                    n += 1
                    conflict_id = tag_id + '-' + str(n)
                tag_id = conflict_id
            item.set('id', tag_id)
            ids.add(tag_id)

            anchor = xml.etree.ElementTree.Element('a', {'href': '#' + tag_id})
            anchor.text = item.text
            item.text = None
            item.append(anchor)
            
            child = ([], tag_id)

            if depth < tag_depth:
                parent[0].append(child)
                stack.append((depth, parent))
                parent = child
                depth = tag_depth
            elif depth >= tag_depth:
                while depth > tag_depth:
                    if stack[-1][0] < tag_depth:
                        depth = tag_depth
                    else:
                        depth, parent = stack.pop()
                stack[-1][1][0].append(child)
                parent = child
    return toc

SITE_TITLE = 'make.vg'
SITE_ROOT_URL = '/'
TEMPLATE = '''<!doctype html>
<html>
    <head>
        <link rel='stylesheet' type="text/css" href='/style.css' />
        <title>{title}</title>
    </head>
    <body>
        <div class='header'>
            <h1><a href="''' + SITE_ROOT_URL + '''">''' + SITE_TITLE + '''</a></h1>
            <div class='separator'></div>
        </div>
        <div class='countdown'>
            <div class='wrapper'>
                <div class='subwrapper'>
                </div>
            </div>
        </div>
        {content}
    </body>
</html>
'''


if __name__ == '__main__':
    APPNAME = os.path.basename(sys.argv[0])
    if len(sys.argv) != 3:
        if len(sys.argv) > 3:
            sys.stderr.write('  (Too many arguments.)\n')
        exit('- Usage: ' + APPNAME + ' destdir sourcedir')

    srcdir = sys.argv[2]
    if not os.path.exists(srcdir):
        exit('- ' + APPNAME + ' - fatal: Could not find source directory "' + srcdir + '".')
    if not os.path.isdir(srcdir):
        exit('- ' + APPNAME + ' - fatal: Source path "' + srcdir + '" is a file, not a directory. Whoops.')

    destdir = sys.argv[1]
    if not os.path.exists(destdir):
        os.makedirs(destdir)

    docs = listdir(srcdir, ['.md']) 
    if not len(docs):
        exit('- ' + APPNAME + ' - fatal: Source tree "' + srcdir + '" contains no .md files.')

    print('- Building ' + str(len(docs)) + ' document(s)...')
    md = markdown.Markdown()
    for filename in docs:
        content = md.convert(open(filename).read())
        content = xml.etree.ElementTree.fromstring('<div class="content">{0}</div>'.format(content))

        # Make a title.
        title = content.find('h1').text
        title = (title + ' - ' if title else '') + SITE_TITLE

        # Build pretty links, and a table of contents we could potentially use later.
        toc = build_toc(content)
        result = TEMPLATE.format(title=title, content=xml.etree.ElementTree.tostring(content))

        dirname = os.path.normpath(os.path.join(destdir, os.path.relpath(srcdir, os.path.dirname(filename))))
        dest = os.path.join(dirname, os.path.basename(os.path.splitext(filename)[0] + '.html'))
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        with open(dest, 'w') as out:
            out.write(result)
        print('  ' + filename + ' -> ' + dest)
    print('- Done!')
