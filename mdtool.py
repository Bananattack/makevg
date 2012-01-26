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
import sys
import markdown # Requires Python-Markdown.

if __name__ == '__main__':
    if len(sys.argv) < 3:
        exit('Usage: ' + os.path.basename(sys.argv[0]) + ' destdir ...files\n')

    destdir = sys.argv[1]
    if not os.path.exists(destdir):
        os.makedirs(destdir)

    print('- Building...')
    md = markdown.Markdown(output_format='html5')
    for filename in sys.argv[2:]:
        result = md.convert(open(filename).read())
        dest = os.path.join(destdir, os.path.splitext(filename)[0] + '.html')
        open(dest, 'w').write(result)
        print('  ' + filename + ' -> ' + dest)
    print('- Done!')
