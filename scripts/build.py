"""Generate a dependency-free bilingual GitHub Pages documentation site."""
from pathlib import Path
import html, re, json
ROOT=Path(__file__).resolve().parents[1]
BASE='/worldcopy-site/'
ORIGIN='https://gptalgopro.github.io'
CONTACT=json.loads((ROOT/'content/site.json').read_text())
def e(s):return html.escape(s,quote=True)
def linkify(s):
 parts=re.split(r'(https://[^\s<>]+)',s)
 return ''.join(f'<a href="{e(t)}">{e(t)}</a>' if t.startswith('https://') else e(t) for t in parts)
def md(s):
 out=[]; para=[]; items=[]
 def flush():
  if para:out.append('<p>'+linkify(' '.join(para))+'</p>');para.clear()
  if items:out.append('<ul>'+''.join('<li>'+linkify(t)+'</li>' for t in items)+'</ul>');items.clear()
 for line in s.splitlines():
  if line.startswith('#'):
   flush(); n=min(3,len(line)-len(line.lstrip('#')));out.append(f'<h{n}>'+e(line.lstrip('# '))+f'</h{n}>')
  elif line.startswith('- '):
   if para:flush()
   items.append(line[2:])
  elif not line.strip() or line=='---':flush()
  else:para.append(line.strip())
 flush();return '\n'.join(out)
NAV={'zh':['产品','iOS 版','Mac 版','支持','隐私','条款'],'en':['Overview','For iOS','For Mac','Support','Privacy','Terms']}
PAGES=['','ios/','mac/','support/','privacy/','terms/']
def url(lang,page=''):return BASE+('en/' if lang=='en' else '')+page

def image(name,alt,cls='screen',lazy=True):
 return f'<img class="{cls}" src="{BASE}assets/{name}" alt="{e(alt)}" '+('loading="lazy" ' if lazy else 'fetchpriority="high" ')+ 'decoding="async">'
def figure(name,alt,caption,cls='screen'):
 return '<figure>'+image(name,alt,cls)+'<figcaption>'+e(caption)+'</figcaption></figure>'
def cards(items):return '<div class="features">'+''.join(f'<article><span class="num">0{i+1}</span><h3>{e(t)}</h3><p>{e(b)}</p></article>' for i,(t,b) in enumerate(items))+'</div>'
def page(lang,path,title,body):
 zh=lang=='zh'; dest=ROOT/('en' if not zh else '')/path;dest.mkdir(parents=True,exist_ok=True)
 nav=''.join('<a '+('aria-current="page"' if path==p else '')+' href="'+url(lang,p)+'">'+n+'</a>' for p,n in zip(PAGES[:4],NAV[lang][:4]))
 footer=''.join(f'<a href="{url(lang,p)}">{n}</a>' for p,n in zip(PAGES[3:],NAV[lang][3:]))
 description='摹界 WorldCopy：在 iPhone 上扫描与 AI 建模，在 Mac 上继续重建、编辑和交付。产品介绍、使用帮助与隐私说明。' if zh else 'WorldCopy brings object scanning and on-device AI modeling to iPhone, with reconstruction, editing and delivery on Mac. Product guides, support and privacy.'
 h=f'''<!doctype html><html lang="{'zh-Hans' if zh else 'en'}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{description}"><meta name="theme-color" content="#f4f3ee"><script src="{BASE}theme.js"></script><title>{e(title)} · WorldCopy 摹界</title><link rel="canonical" href="{ORIGIN}{url(lang,path)}"><link rel="alternate" hreflang="zh-Hans" href="{ORIGIN}{url('zh',path)}"><link rel="alternate" hreflang="en" href="{ORIGIN}{url('en',path)}"><link rel="icon" href="{BASE}assets/worldcopy-icon-light.png"><link rel="stylesheet" href="{BASE}style.css"></head><body><a class="skip" href="#main">{'跳转正文' if zh else 'Skip to content'}</a><header><a class="brand" href="{url(lang)}">{image('worldcopy-icon-light.png','WorldCopy','icon',False)}<span>{"摹界" if zh else "WorldCopy"} <b>{"WorldCopy" if zh else "摹界"}</b></span></a><nav aria-label="{'主导航' if zh else 'Main navigation'}">{nav}</nav><button class="theme-toggle" type="button" hidden aria-pressed="false" aria-label="{'深色外观' if zh else 'Dark appearance'}"><span class="theme-icon" aria-hidden="true">☾</span><span class="theme-label">{'深色' if zh else 'Dark'}</span></button><a class="language" href="{url('en' if zh else 'zh',path)}" lang="{'en' if zh else 'zh-Hans'}">{'EN' if zh else '中文'}</a></header><main id="main">{body}</main><footer><div><a class="wordmark" href="{url(lang)}">WorldCopy<span> / 摹界</span></a><p>{'摹写真实，塑造想象。' if zh else 'Capture reality. Shape imagination.'}</p><small>© 2026 {'孙凯' if zh else 'Kai Sun'}</small></div><div class="footer-links">{footer}<a href="https://github.com/GPTAlgoPro/worldcopy-site">{'网站项目' if zh else 'Website project'} ↗</a></div></footer></body></html>'''
 (dest/'index.html').write_text(h)

def creation_campaign(lang, platform='iphone'):
 zh=lang=='zh'
 title='一张照片的下一种可能。' if zh else 'A new dimension for your photo.'
 lead='从照片创建模型，先保存形状，再选择材质。作品在你的设备上处理，由你决定如何分享。' if zh else 'Create a model from a photo. Save the shape, then choose its textures. Process your work on-device and decide how to share it.'
 stages=['选择照片','生成模型','可选贴图','预览与交付'] if zh else ['Choose a photo','Generate a model','Add optional textures','Preview and deliver']
 free='iPhone / iPad 的创作、保存、预览、编辑与照片分享免费。' if zh else 'Create, save, preview, edit and share photos on iPhone and iPad for free.'
 pro='Pro 一次买断：解锁 iPhone / iPad 专业模型文件导出、Mac AI 引擎与扫描资产交付，以及 .wc3d 工程传输。双端共享，无需订阅；已生成的 Mac AI 作品可自由导出。' if zh else 'One Pro purchase unlocks model-file exports on iPhone and iPad, Mac AI engines and scan-file delivery, plus .wc3d project transfer. No subscription. Existing Mac AI creations remain freely exportable.'
 gallery=''.join(figure(f'campaign/{lang}-{platform}-{i}.png',('真实应用界面与功能介绍' if zh else 'Actual app interface and feature guide')+f' {i}',c,'campaign-poster') for i,c in zip([1,2,5],(['本机 AI 创作','模型与材质','Pro 专业交付'] if zh else ['On-device AI','Shape and texture','Pro workflows'])))
 return f'<section class="creation-campaign"><div><span class="eyebrow">WORLDCOPY / CREATE</span><h2>{title}</h2><p>{lead}</p><ol>'+''.join(f'<li>{e(x)}</li>' for x in stages)+f'</ol><p class="campaign-note">'+('AI 建模与贴图为 Beta 功能。iPhone / iPad 至少需要 8 GB 运存（含 8 GB）；低于此门槛时关闭 AI 和引擎下载入口，Pro 不能解除限制。Mac 使用独立硬件要求。支持的设备使用前需下载对应引擎。' if zh else 'AI modeling and texturing are Beta features. iPhone / iPad require at least 8 GB RAM, including 8 GB. AI and engine downloads are disabled below this threshold; Pro does not remove the limit. Mac has separate hardware requirements. Supported devices must download the engines before use.')+f'</p></div><div class="creation-phones">{image(f"campaign/{lang}-02-teddy.png", "真实泰迪熊模型预览" if zh else "Actual teddy model preview", "campaign-phone")}{image(f"campaign/{lang}-03-cat.png", "真实招财猫贴图预览" if zh else "Actual lucky cat texture preview", "campaign-phone")}</div></section><section class="pro-story"><span class="eyebrow">WORLDCOPY PRO</span><h2>'+('创作自由，交付专业。' if zh else 'Create freely. Deliver professionally.')+f'</h2><p>{free}</p><p>{pro}</p><a class="text-link" href="{url(lang,"support/")}">'+('了解设备与权益 →' if zh else 'Explore capabilities and access →')+f'</a></section><section class="campaign-gallery">{gallery}</section>'

for lang in ['zh','en']:
 zh=lang=='zh'
 phone=f'campaign/{lang}-02-teddy.png'
 hasphone=(ROOT/'assets'/phone).exists()
 phoneimg=image(phone,'摹界 iPhone 实际界面' if zh else 'WorldCopy on iPhone','phone-screen',False) if hasphone else ''
 title='把现实与想象，<br><em>变成 3D 作品。</em>' if zh else 'From the world.<br><em>Into your world.</em>'
 intro='从一次环绕拍摄、一张照片开始。在 iPhone 上捕捉灵感，在 Mac 上细化作品。建模在你的设备上完成。' if zh else 'Start with a walk around an object, or a single photo. Capture ideas on iPhone. Refine them on Mac. Create on your own device.'
 body=f'''<section class="hero"><div class="hero-copy"><div class="eyebrow">WORLDCOPY / {'本机 3D 创作' if zh else 'ON-DEVICE 3D CREATION'}</div><h1>{title}</h1><p class="lead">{intro}</p><div class="actions"><a class="button" href="{url(lang,'ios/')}">{'认识 iOS 版' if zh else 'Explore iOS'} <span>↗</span></a><a class="text-link" href="{url(lang,'mac/')}">{'认识 Mac 版' if zh else 'Explore Mac'} →</a></div><p class="availability">{'iOS 与 Mac 版正在准备上架。' if zh else 'iOS and Mac editions are preparing for App Store release.'}</p></div><div class="hero-art">{image(f'mac-model-{lang}.png','Mac 上的真实 AI 建模工作区' if zh else 'An actual AI model in WorldCopy for Mac','hero-mac',False)}{phoneimg}<span class="art-caption">{'真实 App 界面 · AI 生成作品' if zh else 'Actual app interface · AI-generated model'}</span></div></section>'''
 body+=f'<section class="intro"><span class="eyebrow">01 / {"一个创作过程，两种工作方式" if zh else "ONE CREATIVE FLOW. TWO WORKSPACES."}</span><h2>{"随手开始，<br>在更大的画布上继续。" if zh else "Begin wherever you are.<br>Continue on a bigger canvas."}</h2></section>'
 body+=cards([('iPhone · 捕捉与创作','扫描物体、从单张照片建模，再用 AR 或照片分享作品。') if zh else ('iPhone · Capture & create','Scan objects, create from a single photo, and share your work through AR photography or photo compositions.'),('Mac · 细化与交付','接续 iPhone 扫描包，或从单图、四视图开始，编辑、检查并导出模型。') if zh else ('Mac · Refine & deliver','Continue from an iPhone capture package, or start with one or four views. Edit, inspect and export your model.'),('本机 · 你的作品','照片和模型在设备上处理。导出和分享由你主动发起。') if zh else ('On-device · Your work','Photos and models are processed on your device. You choose when to export or share.')])
 body+='<section class="gallery">'+figure(f'mac-library-{lang}.png','Mac 模型库，包含扫描与 AI 作品' if zh else 'Mac library with scanned and AI-generated models','扫描作品与 AI 作品，保存在同一个模型库。' if zh else 'Scanned and AI-generated work, together in one library.')+'</section>'
 body+=creation_campaign(lang)
 body+=f'<section class="closing"><h2>{"从第一件作品开始。" if zh else "Start with your first object."}</h2><p>{"了解设备要求、建模步骤与常见问题。" if zh else "Learn about supported devices, creation steps and common questions."}</p><a class="button" href="{url(lang,"support/")}">{"查看使用帮助" if zh else "Read the guide"} →</a></section>'
 page(lang,'','产品介绍' if zh else 'Overview',body)
 # iOS product
 items=[('扫描现实物体','在支持 Apple Object Capture 的设备上，跟随框选、环绕拍摄与重建引导完成模型。'),('一张照片，创建模型','从相册选图或拍摄主体，检查分割预览，再在本机运行 AI 建模。'),('先保存，再加纹理','模型完成即可保存。可选 PBR 纹理单独处理；取消或失败保留已完成模型。'),('让作品走进照片','将模型融入自己的照片，或在支持的设备上通过 AR 实景拍照，保存并分享成片。')]
 if not zh:items=[('Scan a real object','On devices that support Apple Object Capture, follow the framing, capture and reconstruction guidance.'),('One photo to a model','Choose a photo or photograph an object. Check the prepared subject before starting on-device AI modeling.'),('Save first. Add texture next.','Save the completed mesh, then optionally create PBR texture. Cancellation or texture failure preserves the completed model.'),('Place your work in a photo','Compose a model into your own photo, or photograph it in AR on supported devices. Save and share the finished picture.')]
 body=f'<section class="page-top"><span class="eyebrow">WORLDCOPY / iOS</span><h1>{"把身边的灵感，<br><em>带进模型库。</em>" if zh else "Everyday inspiration.<br><em>Made three-dimensional.</em>"}</h1><p class="lead">{"为 iPhone 打造的扫描、单图 AI 建模与作品分享体验。" if zh else "Object scanning, single-photo AI modeling and visual sharing, designed for iPhone."}</p></section>'
 if hasphone:body+='<section class="phone-gallery">'+figure(phone,'iPhone 上的摹界实际界面' if zh else 'Actual WorldCopy iPhone interface','iPhone 实机界面' if zh else 'Actual iPhone capture;','phone-detail')+'</section>'
 body+=cards(items)
 body+=f'<section class="requirements"><h2>{"设备与资源" if zh else "Devices & resources"}</h2><p>{"需要 iOS / iPadOS 26 或更高版本。扫描和 AR 以当前设备运行时支持情况为准；iPad 并不因此具备与 iPhone 相同的扫描能力。本机 AI 建模与 PBR 仅支持至少 8 GB 运存的 iPhone / iPad（包含 8 GB）。低于 8 GB 的设备会关闭本机 AI 入口、引擎下载和首次下载提醒；购买 Pro 不会解除硬件限制。兼容设备仍可扫描、查看已有作品。AI 还需要对应引擎资源，以及足够的实时可用内存和磁盘空间。温度、地区和资源状态也会影响可用性。" if zh else "Requires iOS / iPadOS 26 or later. Scanning and AR depend on runtime device support; iPad does not necessarily offer the same capture capabilities as iPhone. On-device AI modeling and PBR require an iPhone or iPad with at least 8 GB RAM (8 GB included). Below 8 GB, AI entry points, engine downloads and the initial download prompt are disabled. Buying Pro does not remove this hardware requirement. Scanning on compatible devices and viewing existing works remain available. AI also requires the corresponding engines and sufficient available memory and storage. Temperature, region and resource status also affect availability."}</p><p>{"支持简体中文和英文。AI 结果及处理时间因输入和设备而异，生成模型不应当作实物测量结果。" if zh else "Available in Simplified Chinese and English. AI results and processing time vary with input and device. Generated geometry is not a measurement of the real object."}</p></section>'
 body+=creation_campaign(lang, 'iphone')
 page(lang,'ios/','iOS 版' if zh else 'For iOS',body)
 # Mac product
 body=f'<section class="page-top"><span class="eyebrow">WORLDCOPY / macOS</span><h1>{"给你的作品，<br><em>更大的发挥空间。</em>" if zh else "More room<br><em>for your next creation.</em>"}</h1><p class="lead">{"从扫描包重建到 AI 创作，把编辑、检查和交付放进同一个工作区。" if zh else "From capture reconstruction to AI creation, bring editing, inspection and delivery into one workspace."}</p></section><section class="gallery">'+figure(f'mac-model-{lang}.png','Mac 上的 AI 模型预览' if zh else 'An AI-generated model in the Mac workspace','Mac 实际界面 · AI 生成作品' if zh else 'Actual Mac interface · AI-generated model')+'</section>'
 body+=cards([('从 iPhone 继续','选择或拖入 .wc3d 扫描包，校验后保存私有项目副本；源文件保持不变。'),('单图与四视图建模','用一张照片，或正、后、左、右四个视图创建模型，再选择匹配的纹理流程。'),('编辑、检查、导出','在模型画布中编辑作品，查看拓扑、UV、材质与尺度信息，按模型能力导出 USDZ、GLB、OBJ 等格式。')] if zh else [('Continue from iPhone','Open or drop a .wc3d capture package. WorldCopy validates it and saves a private project copy without changing the source file.'),('One photo or four views','Create from a single image or front, back, left and right views, then choose the matching texture workflow.'),('Edit, inspect, export','Work on the model canvas, inspect topology, UVs, materials and scale, and export supported formats including USDZ, GLB and OBJ.')])
 body+='<section class="gallery">'+figure(f'mac-library-{lang}.png','Mac 模型库' if zh else 'WorldCopy Mac library','在模型库中重新打开作品，继续处理。' if zh else 'Reopen your saved work and continue.')+'</section>'
 body+=f'<section class="requirements"><h2>{"为 Apple 芯片 Mac 打造" if zh else "Made for Apple silicon"}</h2><p>{"需要 macOS 26 或更高版本、Apple 芯片及至少 16 GB 统一内存。AI 功能还会检查实时内存、磁盘与资源状态。引擎按需下载，安装完成后在本机处理。" if zh else "Requires macOS 26 or later, Apple silicon and at least 16 GB unified memory. AI features also check available memory, storage and resource status. Download the engines you need, then process on-device."}</p><p>{"支持简体中文和英文。.wc3d 用于文件交接，不代表自动云同步。" if zh else "Available in Simplified Chinese and English. .wc3d transfers projects as files; it does not provide automatic cloud sync."}</p></section>'
 body+=creation_campaign(lang, 'mac')
 page(lang,'mac/','Mac 版' if zh else 'For Mac',body)
 # Support
 faqs=[('如何开始扫描？','在兼容的 iPhone 上打开“扫描建模”，按照画面引导环绕静止物体。选择均匀光线和有纹理的主体，避免透明、强反光或移动物体。'),('AI 建模前需要什么？','iPhone / iPad 须至少有 8 GB 运存，Mac 须满足其独立硬件要求。购买 Pro 不能绕过硬件门槛。准备主体完整、清晰的照片，安装对应建模引擎，并留出 App 提示的磁盘和内存空间。首次资源下载需要网络。'),('贴图失败会丢失模型吗？','模型与可选纹理分阶段保存。纹理取消或失败时，已完成的模型会保留，可以返回模型库继续查看。'),('怎样从 iPhone 继续到 Mac？','从 iPhone 导出受支持的 .wc3d 文件，再在 Mac 中选择、拖放或打开它。Mac 会验证并复制到自己的模型库。文件交接不自动同步后续修改。'),('为什么功能不可用？','请检查系统版本、设备能力、引擎安装状态、可用内存、温度和存储空间。等待设备降温或释放空间后重试。付费也不能改变硬件限制。'),('怎样删除作品？','在模型库中删除不再需要的作品，并阅读删除确认。已导出到其他文件夹、设备或备份的副本需要分别删除。Mac 上只删除 App 可能保留数据容器。'),('什么时候可以下载？','iOS 和 Mac 版正在准备 App Store 发布。正式下载入口将在上架后更新；本网站不提供安装包或付款入口。')]
 if not zh:faqs=[('How do I start scanning?','Open Scan Modeling on a compatible iPhone and follow the guidance around a stationary object. Use even lighting and a textured subject; avoid transparent, reflective or moving objects.'),('What do I need for AI modeling?','iPhone / iPad require at least 8 GB RAM; Mac has separate hardware requirements. Pro cannot override these limits. Choose a clear image with the entire subject visible, install the matching engine and keep the memory and storage requested by the app available. The initial resource download needs a network connection.'),('Will a texture failure remove my model?','No. The model and optional texture are saved in separate stages. If texturing fails or is cancelled, the completed model remains available in the library.'),('How do I continue on Mac?','Export a supported .wc3d file from iPhone and select, drop or open it on Mac. WorldCopy verifies and copies it into the Mac library. Later changes do not sync automatically.'),('Why is a feature unavailable?','Check system version, device capability, engine installation, available memory, temperature and storage. Allow the device to cool down or free up space before retrying. A purchase cannot remove hardware restrictions.'),('How do I delete my work?','Delete unwanted projects in the model library and read the confirmation. Exported copies and backups must be deleted separately. Removing the Mac application may leave its data container behind.'),('When can I download the apps?','The iOS and Mac editions are preparing for App Store release. Official download links will be added after launch. This website does not distribute installers or accept payments.')]
 contact=f'<a class="button" href="mailto:{e(CONTACT["email"])}">{e(CONTACT["email"])}</a>' if CONTACT['email'] else '<a class="button" href="https://github.com/GPTAlgoPro/worldcopy-site/issues/new?template=feedback.yml">'+('提交公开反馈' if zh else 'Send public feedback')+' ↗</a>'
 body=f'<section class="page-top"><span class="eyebrow">WORLDCOPY / SUPPORT</span><h1>{"让创作继续。" if zh else "Keep creating."}</h1><p class="lead">{"iOS 与 Mac 的使用帮助和反馈入口。" if zh else "Help and feedback for WorldCopy on iOS and Mac."}</p></section><section class="support-contact"><h2>{"联系开发者" if zh else "Contact the developer"}</h2><p>{'孙凯' if zh else 'Kai Sun'} · WorldCopy / 摹界</p>{contact}<p>{"反馈时请提供平台、App 版本、系统版本和复现步骤。请勿在公开问题中上传私人照片、模型、联系方式或设备标识。" if zh else "Include your platform, app version, OS version and steps to reproduce. Do not post private photos, models, contact details or device identifiers in public issues."}</p><a href="https://github.com/GPTAlgoPro/worldcopy-site/issues">GitHub · {"公开问题" if zh else "Public issues"} ↗</a></section><section class="faq">'+''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q,a in faqs)+'</section>'
 page(lang,'support/','支持与帮助' if zh else 'Support',body)
 # Legal: preserve full existing policy and license restrictions, split languages.
 for name in ['privacy','terms']:
  text=(ROOT/f'content/{name}.md').read_text()
  en,cn=text.split('\n---\n',1)
  if name=='privacy':
   cn,hosting=cn.split('\n\n## Website hosting / 网站托管',1)
   en+='\n\n## Website hosting\n'+hosting.split('\n\n本站')[0]
   cn+='\n\n## 网站托管\n本站'+hosting.split('\n\n本站')[1]+'\n\nhttps://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement'
  selected=cn if zh else en
  if CONTACT['email']:selected+='\n\n'+('联系邮箱：' if zh else 'Contact email: ')+CONTACT['email']
  extra=f'<p><a href="{BASE}content/hunyuan-2-license.txt">Hunyuan 2.0 Community License</a> · <a href="{BASE}content/hunyuan-2.1-license.txt">Hunyuan 2.1 Community License</a></p>' if name=='terms' else ''
  body='<article class="legal"><span class="eyebrow">WORLDCOPY / '+name.upper()+'</span>'+md(selected)+extra+'</article>'
  page(lang,name+'/',NAV[lang][4 if name=='privacy' else 5],body)
(ROOT/'.nojekyll').touch()
(ROOT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+ORIGIN+BASE+'sitemap.xml\n')
(ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+ORIGIN+url(l,p)+'</loc></url>' for l in ['zh','en'] for p in PAGES)+'</urlset>')
(ROOT/'404.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Page not found · WorldCopy</title><link rel="stylesheet" href="'+BASE+'style.css"><main class="legal"><h1>Page not found / 页面不存在</h1><p><a href="'+BASE+'">WorldCopy · 返回首页</a></p></main></html>')
print('Built 12 bilingual pages, sitemap, robots and 404.')
