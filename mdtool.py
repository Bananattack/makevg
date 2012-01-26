import os
import sys
import markdown # Requires Python-Markdown on the sys.path

if __name__ == '__main__':
    md = markdown.Markdown(output_format='html5')
    if len(sys.argv) < 3:
        exit('Usage: ' + os.path.basename(sys.argv[0]) + ' destdir ...files\n')

    destdir = sys.argv[1]
    if not os.path.exists(destdir):
        os.makedirs(destdir)
 
    for filename in sys.argv[2:]:
        result = md.convert(open(filename).read())
        dest = os.path.join(destdir, os.path.splitext(filename)[0] + '.html')
        open(dest, 'w').write(result)
