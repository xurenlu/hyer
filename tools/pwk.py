#!/usr/bin/python
"""
pwyky - A Simple Wiki in Python.

Documentation: <http://infomesh.net/pwyky/>
Author: Sean B. Palmer, <http://purl.org/net/sbp/>
License: GPL 2; share and enjoy!
"""

import sys, os, re, cgi, glob, time
from cStringIO import StringIO
from HTMLParser import HTMLParser

config = {}
configvars = ('default', 'sname', 'lname', 'pedit', 'owner', 'logdir')
r_meta = re.compile('(?s)([^\n:]+): (.*?)(?=\n[^ \t]|\Z)')

if os.path.exists('config.txt'): 
   meta = r_meta.findall(open('config.txt').read())
   for key, value in filter(lambda (k, v): k in configvars, meta): 
      value = value.strip()
      if value in ('0', 'None', 'False'): 
         value = False
      config[key] = value

default = config.get('default', 'index')
shortname = config.get('sname', 'pwyky')
longname = config.get('lname', 'my pwyky site')
pedit = config.get('pedit', True)
owner = config.get('owner', '%s owner' % os.environ.get('SERVER_NAME', 'Site'))
logdir = config.get('logdir', False)

nedit = 'edit'
profile = 'http://infomesh.net/pwyky/profile#'
s_name = os.environ.get('SCRIPT_NAME', '/notes/index.cgi')
base, script = s_name[:s_name.rfind('/')], s_name[s_name.rfind('/')+1:]

if not os.path.exists('.htaccess'): 
   f = open('.htaccess', 'w')
   print >> f, 'DirectoryIndex %s' % script
   print >> f, 'Options -MultiViews'
   print >> f, 'RewriteEngine on'
   print >> f, 'RewriteBase %s' % base
   print >> f, 'RewriteRule ^@[a-z]+/([A-Za-z0-9-]+)$ %s [L]' % script
   print >> f, 'RewriteRule ^([A-Za-z0-9-]+)$ %s [L]' % script
   print >> f, 'RewriteRule ^([A-Za-z0-9-]+)\.html$ - [L]'
   f.close()

if not os.path.exists('style.css'): 
   from base64 import decodestring
   from zlib import decompress
   f = open('style.css', 'w')
   print >> f, decompress(decodestring("""
   eJyNUs1OwzAMvu8prHIBiVTdJpDaHTjuAeAFvNZdI9K4JN7oQLw72dLujx04pIrc78+xV1zt4Bsm
   ANCiW2tbwDR9ohZm4cTb4bs4QGq2ompstdkVsCQOBHwEj9YrT07XAfUzmTTTR2hmg+oF5Q0bbgMj
   WWpj4DXwkiv6yPgkvW6kAMuuRRN1saoceX8u7PUXFeADxERyF0DarpVwV0CWzo/RV+wqcrE+63rw
   bHQFd9lzfubqZWfotimmVGk5996i02hlsFcldj5SKr1NccWbI9owBpjbd7S4zp6lecy490otW+q1
   F7IjuWTDrghBs+wGqMBayA3QLTnRJRqFRq/DIEOvf+x6dfZYZajvRSB5SWJFqBdVUckORbPdP4Wl
   6Ns5Cj5xSZShWopxM8LPleHy/WPDQkOWcQ4RmKXXcxjr87BgwyjyvIxOJ7GL9m4P/NSDUgmgiLsv
   tdDDtRTE/P/e4l/8SPME"""))
   f.close()

class Parser(object): 
   EOF = 0

   def __init__(self, write=None, error=None): 
      self.text = None
      self.pos = 0

      if write is None: 
         write = sys.stdout.write
      self.write = write

      if error is None: 
         # example: sys.stderr.write("%s: %s" % (e, msg))
         error = lambda e, msg: None
      self.error = error

   def find(self, tokens): 
      """For each token in tokens, if the current position matches one of 
         those tokens, return True. Return False otherwise."""
      for token in tokens: 
         if token == self.EOF: 
            if self.pos == len(self.text): 
               return True
         elif self.text[self.pos:].startswith(token): 
            return True
      return False

   def eat(self, token): 
      """Eat the length of token if token's an int, or the token itself."""
      if type(token) is int: 
         if (self.pos + token) > len(self.text): 
            self.error("UnexpectedEOF", "Reached end of file")
            return None
         s = self.text[self.pos:self.pos+token]
         self.pos += token
         return s
      else: 
         assert self.find([token])
         self.pos += len(token)
         if self.pos > len(self.text): 
            self.error("UnexpectedEOF", "Reached end of file")
            return None
         return token

   def get(self, tokens, start=None, finish=None): 
      if start is not None: 
         self.eat(start)
      content = ''
      while not self.find(tokens): 
         s = self.eat(1)
         if s is not None: 
            content += s
         else: return content # reached EOF
      if finish is not None: 
         self.eat(finish)
      return content

r_tag = re.compile(r'(?<!\{)\{(?!\{)([^}]+)\}')
r_name = re.compile(r'^[A-Za-z0-9-]+$')
r_uri = re.compile(r'^[A-Za-z][A-Za-z0-9+.-]*:[^<>"]+$')
r_emdash = re.compile(r'[A-Za-z0-9"]--(?=[A-Za-z0-9"{])')
r_alpha = re.compile(r'[A-Za-z]+')

def makeID(s, current): 
   s = (''.join(r_alpha.findall(s)) or 'id') + str(len(s))
   while s in current: 
      s += 'n'
   return s

class TextParser(Parser): 
   LIST = 0
   HEADING = 1
   PRE = 2
   QUOT = 3
   PARAGRAPH = 4

   LI_START = '* '
   LI_OPEN = '\n* '
   PRE_START = '{{{\n'
   PRE_END = '\n}}}'
   QUOT_START = '[[[\n'
   QUOT_END = '\n]]]'
   H_START = '@ '
   SEPERATOR = '\n\n'

   def __init__(self, write=None, error=None, exists=None): 
      Parser.__init__(self, write=write, error=error)

      if exists is None: 
         exists = lambda: True
      self.exists = exists
      self.rawlinks = []
      self.ids = []

   def __call__(self, s): 
      self.text = s
      self.normalize()
      self.parse()

   def normalize(self): 
      self.text = self.text.strip() # ('\t\r\n ')
      self.text = self.text.replace('\r\n', '\n')
      self.text = self.text.replace('\r', '\n')
      self.text = re.sub(r'(?sm)\n[ \t]*\n', '\n\n', self.text)

   def parse(self): 
      blocks = []

      while 1: 
         blocks.append(self.blockElement())
         if self.find([Parser.EOF]): break

      for block in blocks: 
         blocktype, values = block[0], block[1:]
         {self.LIST: self.listElement, 
          self.HEADING: self.headingElement, 
          self.PRE: self.preElement, 
          self.QUOT: self.quotElement, 
          self.PARAGRAPH: self.paragraphElement
         }[blocktype](*values)

   def blockElement(self): 
      self.whitespace()

      if self.find([self.LI_START]): 
         content = self.get([self.SEPERATOR, Parser.EOF], self.LI_START)
         content = tuple(content.split('\n* '))
         return (self.LIST,) + content
      elif self.find([self.H_START]): 
         content = self.get(['\n', Parser.EOF], self.H_START)
         return (self.HEADING, content)
      elif self.find([self.PRE_START]): 
         content = self.get([self.PRE_END], self.PRE_START, self.PRE_END)
         return (self.PRE, content)
      elif self.find([self.QUOT_START]): 
         content = self.get([self.QUOT_END], self.QUOT_START, self.QUOT_END)
         if self.find([' - ']): 
            citation = self.get(['\n', Parser.EOF], ' - ')
            if not (r_uri.match(citation) and citation): 
               self.error('CitationURIError', # @@ allow other stuff?
                          'Citation (%s) must be a URI.' % citation)
         else: citation = None
         return (self.QUOT, content, citation)
      else: return (self.PARAGRAPH, self.get([self.SEPERATOR, Parser.EOF]))

   def whitespace(self): 
      while self.find(' \t\n'): 
         self.eat(1)

   def listElement(self, *items): 
      self.write('<ul>')
      self.write('\n')

      for item in items: 
         self.write('<li>')
         self.write(self.wikiParse(item))
         self.write('</li>')
         self.write('\n')

      self.write('</ul>')
      self.write('\n')

   def headingElement(self, content): 
      content = self.wikiParse(content)

      newid = makeID(content, self.ids)
      self.ids.append(newid)

      self.write('<h2 id="%s">' % newid)
      self.write(content)
      self.write('</h2>')
      self.write('\n')

   def preElement(self, content): 
      self.write('<pre>')

      self.write('\n')
      self.write(self.wikiParse(content, level=0))
      self.write('\n')

      self.write('</pre>')
      self.write('\n')

   def quotElement(self, content, cite): 
      self.write('<blockquote')
      if cite: 
         cite = self.iriParse(cite)
         cite = cgi.escape(cite, quote=1) # @@
         self.write(' cite="%s"' % cite)
      self.write('>')
      self.write('\n')

      self.write('<pre class="quote">') # @@
      self.write('\n')
      self.write(self.wikiParse(content, level=0))
      self.write('\n')
      self.write('</pre>')
      self.write('\n')

      self.write('</blockquote>')
      self.write('\n')

   def paragraphElement(self, content): 
      self.write('<p>')
      self.write(self.wikiParse(content))
      self.write('</p>')
      self.write('\n')

   def wikiParse(self, s, level=None): 
      if level is None: 
         level = 1
      # @@ use a proper parser, or catch the matches
      pos, result = 0, ''
      while pos < len(s): 
         m = r_tag.match(s[pos:])
         if m: 
            span = m.span()
            result += self.tag(s[pos:pos+span[1]], level=level)
            pos += span[1] - span[0]
         else: 
            m = r_emdash.match(s[pos:])
            if m and (level > 0): # unicode must be explicit in <pre>
               result += s[pos] + '&#8212;' # u'\u2014'.encode('utf-8')
               pos += 3
            elif (s[pos] == '{') and (s[pos+1:pos+2] != '{') and (level > 0): 
               if (s < 10): area = s[0:pos+10]
               else: area = s[pos-10:pos+10]
               msg = "The '{' must be escaped as '{{' in %r" % area
               raise "WikiParseError", msg
            elif (s[pos:pos+2] == '{{'): # d8uv bug "and (level > 0): "
               result += '{'
               pos += 2
            elif s[pos] == '&': 
               result += '&amp;'
               pos += 1
            elif s[pos] == '<': 
               result += '&lt;'
               pos += 1
            else: 
               result += s[pos]
               pos += 1
      return result

   def iriParse(self, uri): 
      r_unicode = re.compile(r'\{U\+([1-9A-F][0-9A-F]{1,5})\}')
      def escape(m): 
         bytes = unichr(int(m.group(1), 16)).encode('utf-8')
         return ''.join(['%%%02X' % ord(s) for s in bytes])
      return r_unicode.sub(escape, uri)

   def unicodeify(self, s): 
      if len(s) not in (2, 4, 6): 
         raise ValueError, 'Must be of length 2, 4, or 6'
      for letter in 'abcdef': 
         if letter in s: 
            raise ValueError, 'Unicode escapes must be lower-case'
      i = int(s.lstrip('0'), 16)
      raw = [0x9, 0xA, 0xD] + list(xrange(0x20, 0x7E))
      del raw[raw.index(0x2D)], raw[raw.index(0x5D)], raw[raw.index(0x7D)]
      if i in raw: return chr(i) # printable - '-]}'
      elif i > 0x10FFFF: 
         raise ValueError, 'Codepoint is out of range'
      return '&#x%s;' % s

   def tag(self, s, level=None): 
      if level is None: 
         level = 1 # @@ { {U+..}?
      s = s[1:-1] # @@ or s.strip('{}')
      if s.startswith('U+'): 
         try: result = self.unicodeify(s[2:])
         except ValueError: result = cgi.escape('{%s}' % s)
      elif s == '$timenow': 
         result = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
      elif s == '$datenow': 
         result = time.strftime('%Y-%m-%d', time.gmtime())
      elif level < 1: 
         result = '{' + self.wikiParse('%s}' % s)
      elif s.startswith('* '): 
         result = '<strong>%s</strong>' % s[2:]
      elif s.startswith('#'): 
         i = s.find(' ')
         href, title = s[:i], s[i+1:]
         result = '<a href="%s">%s</a>' % (href, title)
      elif not re.compile(r'[A-Za-z0-9_.-]').match(s): 
         result = cgi.escape('{%s}' % s)
      else: 
         self.rawlinks.append(s)
         words = s.split(' ')
         words = [word.strip() for word in words if word.strip()]
         if ('/' not in words[0]) and (':' not in words[0]): # @@!
            wn = ''.join(words)
            uri = './%s' % wn
            if not self.exists(wn): 
               cls = ' class="nonexistent"'
            else: cls = ''
         else: uri, s, cls = words[0], ' '.join(words[1:]), ''
         uri, s = cgi.escape(uri, quote=1), cgi.escape(s)
         result = '<a href="%s"%s>%s</a>' % (uri, cls, s)
      return result

def wikiParse(s, getlinks=False): 
   output = StringIO()
   parse = TextParser(write=output.write, 
                      exists=lambda wn: os.path.exists(wn + '.html'))
   parse(s)
   output.flush()
   output.seek(0)
   if getlinks: 
      return output.read(), parse.rawlinks
   return output.read()

class Wikify(HTMLParser): 
   def __init__(self, write=None): 
      HTMLParser.__init__(self)
      if write is None: 
         self.write = sys.stdout.write
      else: self.write = write
      self.content = False
      self.block = False
      self.blockquote = False
      self.anchor = False
      self.current = None

   def handle_starttag(self, tag, attrs): 
      self.current = tag
      attrs = dict(attrs)

      xhtmlxmlns = 'http://www.w3.org/1999/xhtml'
      if (tag == 'html') and (attrs.get('xmlns') != xhtmlxmlns): 
         raise "ParseError", "document is not XHTML"
      elif (tag == 'head') and (attrs.get('profile') != profile): 
         raise "ParseError", "document has incorrect profile"
      elif (tag == 'div') and (attrs.get('class') == 'content'): 
         self.content = True

      if self.content: 
         if tag in ('p', 'li', 'h1', 'h2', 'pre'): 
            self.block = True

         if tag == 'li': 
            self.write('* ')
         elif tag in ('h1', 'h2'): 
            self.write('@ ')
         elif tag == 'pre' and not self.blockquote: 
            self.write('{{{')
         elif tag == 'blockquote': 
            self.blockquote = attrs
            self.write('[[[')
         elif tag == 'strong': 
            self.write('{* ')
         elif tag == 'a': 
            self.anchor = attrs
            self.anchor['_'] = ''

   def handle_endtag(self, tag): 
      self.current = None

      if self.content: 
         if tag in ('p', 'li', 'h1', 'h2', 'pre'): 
            self.block = False

         if tag in ('p', 'h1', 'h2'): 
            self.write('\n\n')
         elif tag in ('ul', 'li'): 
            self.write('\n')
         elif tag == 'pre' and not self.blockquote: 
            self.write('}}}\n\n')
         elif tag == 'blockquote': 
            self.write(']]]')
            cite = self.blockquote.get('cite', None)
            if cite is not None: 
               self.write(' - %s' % cite)
            self.write('\n\n')
            self.blockquote = False
         elif tag == 'a': 
            attrs, dual = self.anchor, True
            uri, title = attrs.get('href', ''), attrs.get('_', '')
            stuff = [w.strip() for w in title.split(' ') if w.strip()]
            stitle = ''.join(stuff)
            if uri.startswith('./'): 
               wn = uri[2:]
               if r_name.match(wn): 
                  if wn == stitle: 
                     dual = False
            if not dual: self.write('{%s}' % title)
            else: self.write('{%s %s}' % (uri, title))
            self.anchor = False
         elif tag == 'strong': 
            self.write('}')
         elif tag == 'div': 
            self.content = False

   def handle_data(self, data): 
      if self.current in ('p', 'li', 'h1', 'h2', 'pre'): # d8uv, pre added
         data = data.replace('{', '{{')

      if self.content and self.block: 
         if not self.anchor: 
            self.write(data)
         else: self.anchor['_'] += data

   def handle_charref(self, name): 
      if self.content and self.block: 
         if name.startswith('x'): 
            result = '{U+%s}' % name.lstrip('x')
         elif name == '8212': 
            result = '--'
         else: raise "ParseError", "Unknown character reference: %s" % name

         if not self.anchor: 
            self.write(result)
         else: self.anchor['_'] += result

   def handle_entityref(self, name): 
      if self.content and self.block: 
         entities = {'lt':'<', 'gt':'>', 'amp':'&', 'quot':'"'}
         result = entities.get(name, '?')

         if not self.anchor: 
            self.write(result)
         else: self.anchor['_'] += result

def wikify(s): 
   output = StringIO()
   parser = Wikify(write=output.write)
   parser.feed(s) # @@ except?
   output.flush()
   output.seek(0)
   return output.read()

def inboundLinks(wn): 
   if not os.path.exists('@links'): # @@ isDir?
      os.mkdir('@links')
   return [fn[9:-(len(wn)+1)] for fn in glob.glob('./@links/*%%%s' % wn)]

def outboundLinks(wn): 
   if not os.path.exists('@links'): # @@ isDir?
      os.mkdir('@links')
   return [fn[len(wn)+10:] for fn in glob.glob('./@links/%s%%*' % wn)]

def html(title, body): 
   s = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" >\n\n'
   s += '<html xmlns="http://www.w3.org/1999/xhtml">\n'
   s += '<head profile="%s">\n' % profile
   s += '<title>%s</title>\n' % title
   if '/' in os.environ.get('REQUEST_URI')[len(base)+1:]: # heh
      s += '<link rel="stylesheet" type="text/css" href="../style.css" />\n'
   else: s += '<link rel="stylesheet" type="text/css" href="style.css" />\n'
   s += '</head>\n'
   s += '<body>\n'
   s += body + '\n'
   s += '</body>\n'
   s += '</html>\n'
   return s

def compile(wn, text, getlinks=False): 
   if getlinks: # @@ horky, but oh well
      content, rawlinks = wikiParse(text, getlinks=getlinks)
   else: content = wikiParse(text, getlinks=getlinks)

   s = '<div class="about">(<a href="./">home</a> | <a \n'
   s += 'href="./@meta/about">about</a> | <a \n'
   s += 'href="./@info/%s">stats</a>)</div>\n\n' % wn

   heading = None
   if content.startswith('<h2'): 
      i = content.find('\n')
      if i < 0: i = len(content)
      j = content.find('>')
      heading = content[:i][len('<h2'):-len('</h2>')]
      content = '<h1%s</h1>%s' % (heading, content[i:])
      heading = content[:i][j+1:-len('</h2>')]
   else: s += '<h1>%s: %s</h1>\n' % (shortname, wn)

   s += '<div class="content">\n%s\n</div>\n\n' % content
   s += '<address>%s. This is a <a \nhref="' % owner
   s += 'http://infomesh.net/pwyky/">pwyky</a> site.'
   if pedit: 
      s += ' <a \nhref="./@%s/%s" class="edit">' % (nedit, wn)
      s += 'Edit this document</a>.'
   s += '</address>'

   if (heading is not None) and (heading != wn): 
      title = '%s - %s' % (heading, wn)
   else: title = wn

   if getlinks: 
      return html(title, s), rawlinks
   return html(title, s)

def rebuild(fn): 
   stat = os.stat(fn)
   atime, mtime = stat.st_atime, stat.st_mtime
   s = open(fn).read()
   try: s = wikify(s)
   except "ParseError", e: 
      s = '<!--\n WikificationError: %s\n -->\n\n' % e
      s += open(fn).read()
   else: s = compile(fn[:-len('.html')], s)
   open(fn, 'w').write(s)
   try: os.utime(fn, (atime, mtime))
   except OSError: pass

def get(wn): 
   if os.path.exists(wn + '.html'): 
      return open(wn + '.html').read()
   else: 
      msg = '<h1>%s</h1>\n' % wn
      msg += '<p>This page does not yet exist.'
      if pedit: 
         msg += ' <a href="./@%s/%s">Create it!</a>' % (nedit, wn)
      msg += '</p>\n'
      return html('Create %s' % wn, msg)

def edit(wn): 
   if os.path.exists(wn + '.html'): 
      try: s = wikify(open(wn + '.html').read())
      except "ParseError", e: 
         s = "Error: couldn't wikify source! (%s)\n" % e
   else: s = ''
   if wn == default: 
      wn = ''
   return html('Editing %s' % (wn or default), '''
     <form action="../%s" method="POST">
        <div>
          <textarea rows="20" cols="80" name="text">%s</textarea>
        </div>
        <div><input type="submit" /></div>
     </form>
   ''' % (wn, cgi.escape(s)))

def info(wn): 
   if not os.path.exists(wn + '.html'): 
      return "Page doesn't exist: %s" % wn

   results = []
   for fn in glob.glob('*.html'): 
      fn = fn[:-len('.html')]
      for title in outboundLinks(fn): 
         words = title.split(' ')
         words = [word.strip() for word in words if word.strip()]
         if ('/' not in words[0]) and (':' not in words[0]): 
            if ''.join(words) == wn: results.append(fn) # @@ break
   r = ['* {../%s %s} ({../@info/%s @info})' % (f, f, f) for f in results]

   try: content = wikify(open(wn + '.html').read())
   except "ParseError": 
      content = open(wn + '.html').read()
   t = os.stat(wn + '.html').st_mtime
   lastmod = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(t))

   s = '<h1>About <a href="../%s">%s</a></h1>\n' % (wn, wn)
   if os.path.exists(wn + '.prev'): 
      pt = os.stat(wn + '.html').st_mtime
      plastmod = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(pt))
      s += '<p><a href="../%s.prev">Previous ' % wn
      s += 'version</a> (%s).</p>\n' % plastmod
      s += '<form action="../@meta/diff" method="POST"><p>'
      s += '<input type="hidden" name="diff" value="%s" /> ' % wn
      s += '<input type="submit" value="Compute diff" />\n'
      s += '</p></form>\n'
   else: s += '<p>(This is the first version).</p>\n'
   s += '<h2>Statistics</h2>\n'
   s += '<ul><li>Characters: %s</li>\n' % len(content)
   s += '<li>Word count: %s</li>\n' % len(content.split(' '))
   s += '<li>Last-modified: %s</li>\n</ul>\n' % lastmod
   if r: 
      s += '<h2>Inbound Links</h2>\n'
      s += wikiParse('\n'.join(r)) + '\n'
   else: s += '<p><em>This page has no inbound links</em>.</p>\n'
   s += '<address>%s. Nearby: <a href="../">home</a>.</address>\n' % owner

   return html('Information About %s' % wn, s)

def meta(wn): 
   if wn == 'about': 
      pages = {
         'about': 'This page.', 
         'archive': 'Create a .tar.gz of the whole site.', 
         'diff': 'Find differences between a page and its previous version.', 
         'grep': 'Grep (search) the text in the site.', 
         'names': 'Provide a list of all pages.', 
         'needed': 'List of pages that are linked to but not yet made.', 
         'todo': 'List of todo items in the site.', 
         'unlinked': 'Pages that are not linked to elsewhere.', 
         'updates': 'Shows the most recent changes.'
      }.items()
      pages.sort()
      pages = ['* {./%s %s} - %s' % (k, k, v) for k, v in pages]
      pagelist = wikiParse('\n'.join(pages))

      s = '<h1>@meta: About This Site</h1>\n'
      s += '<p>This site is a pwyky installation (<a \n'
      s += 'href="http://infomesh.net/pwyky/pwyky.py.txt"'
      s += '>source</a>); the <a href="http://infomesh.net/pwyky/'
      s += '">pwyky homepage</a> explains how to use it. The \n'
      s += '@meta directory contains tools for providing information \n'
      s += 'about this particular site.</p>\n'
      s += pagelist
      s += '<p>Contact the site owner for questions about this site.</p>\n'
      s += '<address>%s. Nearby: <a href="../">home</a>.</address>\n' % owner
      return html("@meta: About This Site", s)

   elif wn == 'names': 
      results = [fn[:-len('.html')] for fn in glob.glob('*.html')]
      results.sort()
      results = ['* {../%s %s}' % (fn, fn) for fn in results]
      s = '<h1>All Pages</h1>\n'
      s += '<p>There are %s pages in this site: </p>\n' % len(results)
      s += wikiParse('\n'.join(results))
      s += '<address>%s. Nearby: <a href="../">home</a>.</address>\n' % owner
      return html("@meta/names: Site Pages List", s)

   elif wn == 'archive': 
      if not os.path.exists('.notar'): 
         import tarfile
         tar = tarfile.open("archive.tar.gz", "w:gz")
         for fn in glob.glob('*.html'): 
            tar.add(fn)
         tar.close()
         open('.notar', 'w').write('')
         return html(wn, '.tar.gz updated (../archive.tar.gz)')
      else: return html(wn, '.tar.gz not updated (../archive.tar.gz)')

   elif wn == 'updates': 
      i = 100 # Number of results to show
      result = {}
      for fn in glob.glob('*.html'): 
         t = os.stat(fn).st_mtime
         lastmod = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(t))
         while result.has_key(lastmod): 
            lastmod += '_'
         result[lastmod] = fn[:-len('.html')]
      keys = result.keys()
      keys.sort()
      keys.reverse()
      keys = keys[:i]

      today = time.strftime('%Y-%m-%d', time.gmtime())
      s = '<h1>Updates: Recently Changed Pages</h1>\n'
      s += '<p>Today is <strong>%s</strong>. ' % today
      s += 'The %s most recent changes in this site are: </p>\n' % len(keys)
      s += '<ul>\n'
      for n in keys: 
         pdate, ptime = tuple(n.split(' '))
         ptime = ptime.rstrip('_')
         s += '<li><strong>%s</strong>: ' % pdate
         s += '<a href="../%s">%s</a> %s' % (result[n], result[n], ptime)
         if os.path.exists(result[n] + '.prev'): 
            before = len(open(result[n] + '.prev').read())
            after = len(open(result[n] + '.html').read())
            s += ' (changed by %s characters)</li>\n' % (after - before)
         else: s += ' <strong>New!</strong></li>\n'
      s += '</ul>\n<p>Up to %s updates will be shown.</p>\n' % i
      s += '<address>%s. Nearby: <a href="../">home</a>.</address>\n' % owner
      return html('%s - Updates: Recent Changes' % longname, s)

   elif wn == 'grep': 
      s = '<form action="./grep" method="POST">\n'
      s += '<div>grep: <input type="text" name="regexp" size="25" /> \n'
      s += '<input type="submit" /></div>\n'
      s += '</form>\n'

      if os.environ.get('REQUEST_METHOD') == 'POST': 
         form = cgi.parse_qs(sys.stdin.read()).items()
         form = dict([(item[0], ''.join(item[1])) for item in form])
         regexp = form.get('regexp', '')
         r_regexp = re.compile(regexp)

         results = {}
         for fn in glob.glob('*.html'): 
            for line in open(fn).read().splitlines(): 
               find = r_regexp.findall(line)
               if find: 
                  if results.has_key(fn): 
                     results[fn] += len(find)
                  else: results[fn] = len(find)
         results = [(v, k) for k, v in results.items()]
         results.sort()
         results.reverse()
         results = [(k, v) for v, k in results][:10] # 10 results only!

         s += '<h2>Search Result for %r</h2>\n' % regexp
         s += '<ul>\n'
         for (fn, count) in results: 
            wn = fn[:-len('.html')]
            s += '<li><a href="../%s">%s</a> ' % (wn, wn)
            s += '- %s matches</a></li>\n' % count
         s += '</ul>\n'

      s += '<address>%s. Nearby: <a \n' % owner
      s += 'href="../">home</a>.</address>\n'
      return html(wn, s)

   elif wn == 'diff': 
      s = '<form action="./diff" method="POST">\n'
      s += '<div>diff: <input type="text" name="diff" size="25" /> \n'
      s += '<input type="submit" /></div>\n'
      s += '</form>\n'

      if os.environ.get('REQUEST_METHOD') == 'POST': 
         form = cgi.parse_qs(sys.stdin.read()).items()
         form = dict([(item[0], ''.join(item[1])) for item in form])
         diff = form.get('diff', '')

         if not os.path.exists(diff + '.prev'): 
            s += '<p>%s has no previous versions.</p>\n' % diff
         else: 
            from difflib import Differ
            before = open(diff + '.prev').read()
            after = open(diff + '.html').read()
            before = before.replace('. ', '. \n').splitlines()
            after = after.replace('. ', '. \n').splitlines()

            s += '<h2>Result of diff for %s</h2>\n' % diff
            s += '<p style="font-family:monospace;">\n'
            for line in list(Differ().compare(before, after)): 
               if (line.startswith('+ ') or 
                   line.startswith('- ') or 
                   line.startswith('? ')): 
                  s += '<strong>%s</strong><br />' % cgi.escape(line)
               else: s += '%s<br />' % cgi.escape(line)
            s += '</p>\n'

      s += '<address>%s. Nearby: <a \n' % owner
      s += 'href="../">home</a>.</address>\n'
      return html(wn, s)

   elif wn == 'needed': 
      results = {}
      for fn in glob.glob('*.html'): 
         fn = fn[:-len('.html')]
         for title in outboundLinks(fn): 
            words = title.split(' ')
            words = [word.strip() for word in words if word.strip()]
            if ('/' not in words[0]) and (':' not in words[0]): 
               needed = ''.join(words)
               if not os.path.exists(needed + '.html'): 
                  if results.has_key(needed): 
                     results[needed].append(fn)
                  else: results[needed] = [fn]
      keys = results.keys()
      keys.sort()
      result = ''
      for key in keys: 
         frompages = dict([(uniq, None) for uniq in results[key]]).keys()
         frompages.sort()
         result += '* {../%s %s} (from: ' % (key, key)
         result += ', '.join(['{../%s %s}' % (v, v) for v in frompages])
         result += ')\n'

      s = '<h1>Needed Pages (or: Broken Links)</h1>\n'
      s += "<p>List of pages that are linked to but not yet made:</p>\n"
      s += wikiParse(result or '[No such pages found].\n')
      s += '<address>%s. Nearby: <a \n' % owner
      s += 'href="../">home</a>.</address>\n'

      return html("Needed Pages", s)

   elif wn == 'unlinked': 
      result = ''
      for fn in glob.glob('*.html'): 
         fn = fn[:-len('.html')]
         links = inboundLinks(fn)
         if len(links) == 0: 
            result += '* {../%s %s} ({../@info/%s info})\n' % (fn, fn, fn)

      s = '<h1>Unlinked Pages</h1>\n'
      s += "<p>The following is a list of pages which aren't linked \n"
      s += 'to from any other page: </p>\n'
      s += wikiParse(result or '[No such pages found].\n')
      s += '<address>%s. Nearby: <a \n' % owner
      s += 'href="../">home</a>.</address>\n'

      return html('Unlinked Pages', s)

   elif wn == 'rebuild': 
      # @@ dark corner
      os.environ['REQUEST_URI'] = base + '/'
      for fn in glob.glob('*.html'): 
         rebuild(fn)
      return html('Rebuilt Pages', '<p>All pages have been rebuilt.</p>\n')

   elif wn == 'todo': 
      todo = '@@'
      r = '(?sm)%s[ \n].+?(?:\.(?=[ \n<])|\?(?=[ \n<])|.(?=<)|\n\n)' % todo
      r_regexp = re.compile(r)

      results = {}
      for fn in glob.glob('*.html'): 
         for line in open(fn).read().splitlines(): 
            find = r_regexp.findall(line)
            if find: 
               if results.has_key(fn): 
                  results[fn] += find
               else: results[fn] = find
      results = results.items()
      results.sort()
      s = '<h2>Todo Items</h2>\n'
      s += '<dl>\n'
      for (fn, found) in results: 
         wn = fn[:-len('.html')]
         s += '<dt><strong><a href="../%s">%s</a></strong></dt>\n' % (wn, wn)
         for find in found: 
            s += '<dd>%s</dd>\n' % find
      s += '</dl>\n'

      s += '<address>%s. Nearby: <a \n' % owner
      s += 'href="../">home</a>.</address>\n'
      return html(wn, s)

   else: return html(wn, 'Unknown function: %s' % wn)

def post(wn): 
   if os.path.exists('.notar'): 
      os.remove('.notar')
   # archive the previous version, if need be
   recompile = True
   if os.path.exists('%s.html' % wn): 
      prev = open('%s.html' % wn).read()
      open('%s.prev' % wn, 'w').write(prev)
      recompile = False

   # create the new version
   form = cgi.parse_qs(sys.stdin.read())
   form = dict([(item[0], ''.join(item[1])) for item in form.items()])
   s = form.get('text', '')
   # @@ if s and not s.endswith('\n'): s += '\n'
   if s: 
      # do this before writing out!
      compiled, rawlinks = compile(wn, s, getlinks=True)
      open('%s.html' % wn, 'w').write(compiled)
      # Now record the links in @links...
      prev, now = outboundLinks(wn), []
      for link in rawlinks: 
         words = [w.strip() for w in link.split(' ') if w.strip()]
         if ('/' not in words[0]) and (':' not in words[0]): 
            now.append(''.join(words))
         elif words[0].startswith('./'): 
            if r_name.match(words[0][2:]): 
               now.append(words[0][2:])
      for link in prev: 
         if link not in now: 
            os.remove('./@links/%s%%%s' % (wn, link))
      for link in now: 
         if link not in prev: 
            open('./@links/%s%%%s' % (wn, link), 'w').write('')
   else: # @@ give some kind of "really?" thing?
      if os.path.exists('%s.html' % wn): 
         os.remove('%s.html' % wn)
      if os.path.exists('%s.prev' % wn): 
         os.remove('%s.prev' % wn)
      # Update @links: remove all outbound links
      for fn in glob.glob('./@links/%s%%*' % wn): 
         os.remove(fn)

   # Rebuild all pages that link to this one
   # if (not s) or recompile: # @@ didn't work because it barfed?
   for iwn in inboundLinks(wn): 
      rebuild(iwn + '.html')

def main(env=None): 
   if env is None: 
      env = os.environ

   method = env.get('REQUEST_METHOD')
   if method not in ('GET', 'POST'): 
      raise "UnsupportedMethodError", "Unsupported method: %s" % method

   # @@ redo @links on each rebuild?

   sys.stdout.write('Content-Type: text/html; charset=utf-8\r\n\r\n')

   uri = env.get('REQUEST_URI')
   assert uri.startswith(base) # @@
   path = uri[len(base):]

   if logdir: # Log the request
      t = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
      f = open('%s/%s-%s.log' % (logdir, shortname, t[:7]), 'a')
      addr = env.get('REMOTE_ADDR')
      referer = env.get('HTTP_REFERER', '[direct]').replace(' ', '')
      print >> f, t, method, path, addr, referer
      f.close()

   if path == '/': 
      path = '/%s' % default

   if not path.startswith('/@'): 
      action = 'get'
      wn = path[len('/'):]
   else: 
      i = path.rfind('/')
      action = path[2:i]
      wn = path[(i+1):]

   if (not r_name.match(wn)) and (wn != script): 
      raise 'ScriptError', 'Invalid filename: %s' % wn

   if wn == script: 
      print '<p>Welcome to this pwyky site. '
      print 'Try: <a href="./">home page</a>.</p>'
   elif action == 'get': 
      if method == 'POST': 
         post(wn)
      print get(wn)
   elif action == nedit: 
      print edit(wn)
   elif action == 'info': 
      print info(wn)
   elif action == 'meta': 
      print meta(wn)
   else: print '<p>Unknown action: %s</p>' % action

def run(argv=None): 
   if argv is None: 
      argv = sys.argv[1:]

   if argv: 
      if argv[0] in ('-h', '--help'): 
         print __doc__.lstrip()
      else: 
         if argv[0] in ('-w', '--wikify'): 
            func = wikify
         elif argv[0] in ('-p', '--parse'): 
            func = wikiParse

         if len(argv) > 1: 
            import urllib
            s = urllib.urlopen(argv[1]).read()
         else: s = sys.stdin.read()
         sys.stdout.write(func(s))

import os,sys

if __name__=='__main__': 
   if os.environ.has_key('SCRIPT_NAME'): 
      try: main()
      except: cgi.print_exception()
   else: run()
