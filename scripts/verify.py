from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse,unquote
r=Path(__file__).resolve().parents[1]
errors=[]
class Check(HTMLParser):
 def __init__(self,p):super().__init__();self.p=p;self.h1=0;self.title=0;self.lang=False
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if tag=='h1':self.h1+=1
  if tag=='title':self.title+=1
  if tag=='html':self.lang=bool(d.get('lang'))
  if tag=='img' and not d.get('alt'):errors.append(f'{self.p}: image lacks alt')
  for attr in ('href','src'):
   v=d.get(attr,'')
   if v.startswith('/worldcopy-site/'):
    p=r/unquote(urlparse(v).path.removeprefix('/worldcopy-site/'))
    if p.is_dir():p=p/'index.html'
    if not p.exists():errors.append(f'{self.p}: missing {p}')
for p in r.rglob('*.html'):
 t=p.read_text();c=Check(p);c.feed(t)
 if c.h1!=1 or c.title!=1 or not c.lang:errors.append(f'{p}: invalid document landmarks')
 for bad in ('[REQUIRED]','localhost:','127.0.0.1','GPTAlgoPro/Snap3D','/Users/kaisun'):
  if bad in t:errors.append(f'{p}: unexpected {bad}')
for lang in ('','en/'):
 for page in ('support','privacy','terms'):
  if 'sunkai4u@gmail.com' not in (r/lang/page/'index.html').read_text():errors.append(f'{lang}{page}: missing contact')
if errors:raise SystemExit('\n'.join(errors))
print('PASS: 12 bilingual pages + 404; local links/assets, language, headings, alt text, contact and placeholder checks.')
