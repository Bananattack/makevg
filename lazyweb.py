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

import os
import shutil
import urlparse

def listdir(base, extensions=None):
    result = []
    for path in os.listdir(base):   
        path = os.path.join(base, path)
        if os.path.isdir(path):
            result.extend(listdir(path, extensions))
        elif os.path.isfile(path) and (extensions is None or os.path.splitext(path)[1].lower() in extensions):
            result.append(os.path.normpath(path))
    return result

template = '''<!doctype html>
<html>
<head>
    <title>{title}</title>
    <link rel='stylesheet' type='text/css' href='{css_url}'>
    <link rel='shortcut icon' type='image/png' href='{favicon_url}' />
    <link rel='icon' type='image/png' href='{favicon_url}' />
    <link rel='image_src' href='{preview_image_url}' />
    <link rel='canonical' href='{canonical_url}' />
    <meta property='og:title' content='{title}' /> 
    <meta property='og:type' content='website' /> 
    <meta property='og:image' content='{preview_image_url}' /> 
    <meta property='og:url' content='{canonical_url}' /> 
    <meta property='og:description' content='{description}' />
</head>
<body class='page'>
    <h1><a class='header' href='#'>make.vg</a></h1>
    {content}
</body>
</html>
'''

if __name__ == '__main__':
    src = 'source'
    out = 'output'
    inc = 'include'
    rooturl = 'http://make.vg/'
    docs = listdir(src, ['.md'])

    if os.path.isdir(out):
        shutil.rmtree(out)

    if os.path.isdir(inc):
        shutil.copytree(inc, out)
    else:
        os.makedirs(out)

    if not len(docs):
        exit('- lazyweb - fatal: Source tree "' + src + '" contains no .md files.')
    for doc in docs:
        lines = open(doc).read().splitlines()
        found = False
        settings = []
        content = []
        for line in lines:
            if not found:
                if line.strip() == '//':
                    found = True
                else:
                    before, _, after = line.partition(':')
                    before = before.strip().lower()
                    after = after.strip()
                    settings.append((before, after))
            else:
                content.append(line)

        paths = [os.path.relpath(os.path.splitext(doc)[0], src)] + [v for k, v in settings if k == 'path']
        title = next((v for k, v in settings if k == 'title'), os.path.basename(paths[0]))
        description = next((v for k, v in settings if k == 'description'),
            'Andrew G. Crowell is an independent game developer / programmer / pixel artist from Sarnia, Ontario. He is working on Revenants, an exploratory action sidescroller.'
        )
        if next((k for k, v in settings if k == 'explicit_path'), False):
            paths.pop(0)
        if next((k for k, v in settings if k == 'sticky'), False):
            paths.append('')
        
        print(title)
        print(paths)
        for path in paths:
            if not os.path.exists(os.path.join(out, path)):
                os.makedirs(os.path.join(out, path))
            with open(os.path.join(out, path, 'index.html'), 'w') as result:
                result.write(template.format(
                    title = (title + ' - ' if path else '') + 'make.vg',
                    canonical_url = urlparse.urljoin(rooturl, path),
                    css_url = urlparse.urljoin(rooturl, 'style.css'),
                    favicon_url = urlparse.urljoin(rooturl, 'favicon.ico'),
                    preview_image_url = urlparse.urljoin(rooturl, 'images/make.vg.logo.png'),
                    description = description,
                    content = '\n'.join(content),
                ))

