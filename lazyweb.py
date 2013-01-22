#!/usr/bin/env python

# Copyright (C) 2013 Andrew G. Crowell
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
import datetime
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


SRC = 'source'
OUT = 'output'
INC = 'include'
REPO_URL = 'https://github.com/Bananattack/makevg/blob/master/'
ROOT_URL = 'http://make.vg/'
ROOT_TITLE = 'make.vg'
ROOT_DESCRIPTION = 'Andrew G. Crowell is an independent game developer / programmer / pixel artist from Sarnia, Ontario. He is working on Revenants, an exploratory action sidescroller.'
STYLESHEET_PATH = 'style.css'
FAVICON_PATH = 'favicon.ico'
PREVIEW_IMAGE_PATH = 'images/make.vg.logo.png'
TEMPLATE = '''<!doctype html>
<html>
<head>
    <meta charset='utf-8' />
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
    <h1><a class='header' href='{root_url}'>{header}</a></h1>
    {content}
    <p class='article_tools'><a href='{source_code_url}'>source</a> &mdash; <a href='{permalink_url}'>permalink</a></p>
    <p class='footnote'>
    <a href='http://bananattack.com/'>bananattack.com</a> for my other, older stuff. &mdash; <a href='https://github.com/Bananattack/wiz'>wiz</a> is a high-level 8-bit 6502 / Z80 assembly language I made.<br/><br/>
    Copyright &copy; {year} Andrew G. Crowell. All rights reserved.<br/>Some content of this site is available under more permissive terms, see <a href='https://github.com/Bananattack/makevg'>here</a>.</p>
</body>
</html>
'''

if __name__ == '__main__':
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)

    if os.path.isdir(INC):
        shutil.copytree(INC, OUT)
    else:
        os.makedirs(OUT)

    docs = listdir(SRC, ['.md'])
    stickied = False
    if not len(docs):
        exit('*** fatal: Source tree "' + SRC + '" contains no .md files.')
    for doc in docs:
        lines = open(doc).read().splitlines()
        count = 2
        settings = {}
        content = []
        for line in lines:
            if not count:
                content.append(line)
            else:
                if line.strip() == '```':
                    count -= 1
                else:
                    key, _, value = line.partition(':')
                    settings.setdefault(key.strip().lower(), []).append(value.strip())

        paths = [os.path.relpath(os.path.splitext(doc)[0], SRC)] + settings.get('path', [])
        title = settings['title'][0] if 'title' in settings else os.path.basename(paths[0])
        description = settings['description'][0] if 'description' in settings else ROOT_DESCRIPTION

        if 'explicit_path' in settings:
            paths.pop(0)

        canonical_path = settings['canonical'][0] if 'canonical' in settings else paths[0]

        if 'sticky' in settings:
            stickied = True
            paths.append('')
        
        print(title + ' -> ' + ', '.join(urlparse.urljoin(ROOT_URL, path) for path in paths))
        for path in paths:
            if not os.path.exists(os.path.join(OUT, path)):
                os.makedirs(os.path.join(OUT, path))
            with open(os.path.join(OUT, path, 'index.html'), 'w') as result:
                result.write(TEMPLATE.format(
                    root_url = ROOT_URL,
                    header = ROOT_TITLE,
                    year = datetime.date.today().year,
                    title = (title + ' - ' if path else '') + ROOT_TITLE,
                    canonical_url = urlparse.urljoin(ROOT_URL, canonical_path) if path else ROOT_URL,
                    permalink_url = urlparse.urljoin(ROOT_URL, canonical_path),
                    css_url = urlparse.urljoin(ROOT_URL, STYLESHEET_PATH),
                    favicon_url = urlparse.urljoin(ROOT_URL, FAVICON_PATH),
                    preview_image_url = urlparse.urljoin(ROOT_URL, PREVIEW_IMAGE_PATH),
                    source_code_url = urlparse.urljoin(REPO_URL, doc),
                    description = description,
                    content = '\n'.join(content),
                ))
    if not stickied:
        exit('\n*** warning: Source tree "' + SRC + '" contains no file with the "sticky" attribute! There will be no index page at ' + ROOT_URL)

