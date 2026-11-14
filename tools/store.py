"""Exporta o catálogo para o app Wolff's Store (PS Vita): _site/store.json e imagens em _site/store/.

Chamado por tools/build.py. Os textos saem só com caracteres Latin-1 (a fonte do app é Latin-1),
capas em 512x288 e capturas em 480x270 (PNG se pixelado, JPG nos outros), com o hash no nome
do arquivo para o app saber quando baixar de novo.

Downloads de cada post (campo `downloads:` no post.md) são resolvidos aqui:
  - `url:` link direto (versão em `versao:`), ou
  - `repo:` + `arquivo:` asset da última release do repo (ou da `tag:`), versão = tag.
A versão do próprio app vem das releases deste repo com tag `store-v*`.
"""
import fnmatch
import hashlib
import io
import json
import os
import re
import urllib.request

from PIL import Image

APP_REPO = 'WolffsRoom/WolffsRoomSite'
APP_TAG_PREFIX = 'store-v'
APP_ASSET = 'WolffsStore-*.vpk'
COVER = (512, 288)
SHOT = (480, 270)
DEFAULT_ASSET = {'vpk': '*.vpk', 'traducao': '*.zip', 'plugin': '*.*', 'arquivo': '*.*'}

LATIN = {'—': '-', '–': '-', '“': '"', '”': '"', '‘': "'", '’': "'", '…': '...', '→': '>', '←': '<',
         '•': '·', '×': 'x', ' ': ' ', '™': '(TM)', '®': '(R)'}


def latin(s):
    s = str(s or '')
    s = re.sub(r'\[([^\]]+)\]\((https?://[^)\s]+)\)', r'\1', s)
    s = re.sub(r'\*\*([^*]+)\*\*', r'\1', s)
    out = []
    for ch in s:
        ch = LATIN.get(ch, ch)
        try:
            ch.encode('latin-1')
            out.append(ch)
        except UnicodeEncodeError:
            out.append('?')
    return ''.join(out).replace('\t', ' ').replace('\n', ' ').strip()


# ------------------------------------------------------------------ GitHub releases

_cache = {}


def _api(path):
    if path in _cache:
        return _cache[path]
    req = urllib.request.Request('https://api.github.com' + path, headers={
        'Accept': 'application/vnd.github+json', 'User-Agent': 'WolffsRoomSite-build'})
    tok = os.environ.get('GITHUB_TOKEN')
    if tok:
        req.add_header('Authorization', 'Bearer ' + tok)
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            data = json.load(r)
    except Exception as e:  # sem rede, repo privado, limite da API...
        print(f'aviso: GitHub {path}: {e}')
        data = None
    _cache[path] = data
    return data


def _pick_asset(release, pattern):
    for a in (release or {}).get('assets') or []:
        if fnmatch.fnmatch(a['name'].lower(), pattern.lower()):
            return a
    return None


def _version_from_tag(tag, prefix=''):
    t = tag[len(prefix):] if prefix and tag.startswith(prefix) else tag
    return t[1:] if t[:1] in 'vV' and t[1:2].isdigit() else t


def resolve_download(d, post_links):
    """Devolve o download pronto para o app, ou None (com aviso) se não deu para resolver."""
    tipo = d['tipo']
    out = {'tipo': tipo, 'nome': latin(d.get('nome') or ''), 'precisa_dados': bool(d.get('precisa_dados')),
           'titleids': d.get('titleids') or [], 'plugin': latin(d.get('plugin') or '')}
    if d.get('url'):
        out['url'] = d['url']
        out['versao'] = latin(d.get('versao') or '')
        out['tamanho'] = int(d.get('tamanho') or 0)
        out['arquivo'] = os.path.basename(d['url'].split('?')[0])
    else:
        repo = d['repo']
        rel = _api(f'/repos/{repo}/releases/tags/{d["tag"]}') if d.get('tag') else _api(f'/repos/{repo}/releases/latest')
        asset = _pick_asset(rel, d.get('arquivo') or DEFAULT_ASSET[tipo])
        if not asset:
            print(f'aviso: download sem arquivo na release de {repo} ({d.get("arquivo") or DEFAULT_ASSET[tipo]})')
            return None
        out['url'] = asset['browser_download_url']
        out['versao'] = latin(d.get('versao') or _version_from_tag(rel.get('tag_name') or ''))
        out['tamanho'] = int(asset.get('size') or 0)
        out['arquivo'] = asset['name']
    if not out['nome']:
        out['nome'] = out['arquivo']
    gh = next((u for _, u in post_links if 'github.com' in u), '')
    out['instrucoes'] = d.get('instrucoes') or gh
    return out


def app_release():
    rels = _api(f'/repos/{APP_REPO}/releases?per_page=30') or []
    for r in rels:
        if r.get('draft') or not str(r.get('tag_name', '')).startswith(APP_TAG_PREFIX):
            continue
        a = _pick_asset(r, APP_ASSET)
        if a:
            return {'versao': _version_from_tag(r['tag_name'], APP_TAG_PREFIX), 'url': a['browser_download_url'],
                    'tamanho': int(a.get('size') or 0), 'notas': latin((r.get('body') or '')[:400])}
    return None


# ------------------------------------------------------------------ imagens

def _fit(img, size, style, pixel):
    W, H = size
    rs = Image.NEAREST if pixel else Image.LANCZOS
    img = img.convert('RGBA')
    bg = Image.new('RGBA', size, (0, 0, 0, 255))
    if style in ('logo', 'conter'):
        k = min(W / img.width, H / img.height) * (0.8 if style == 'logo' else 1)
        im = img.resize((max(1, round(img.width * k)), max(1, round(img.height * k))), rs)
        bg.alpha_composite(im, ((W - im.width) // 2, (H - im.height) // 2))
        return bg
    k = max(W / img.width, H / img.height)
    im = img.resize((max(W, round(img.width * k)), max(H, round(img.height * k))), rs)
    x, y = (im.width - W) // 2, (im.height - H) // 2
    bg.alpha_composite(im.crop((x, y, x + W, y + H)))
    return bg


def _save(img, pixel, folder, base, out_dir):
    buf = io.BytesIO()
    if pixel:
        rgb = img.convert('RGB')
        colors = rgb.getcolors(256)
        (rgb.quantize(colors=len(colors)) if colors else rgb).save(buf, 'PNG', optimize=True)
        ext = 'png'
    else:
        img.convert('RGB').save(buf, 'JPEG', quality=85, optimize=True)
        ext = 'jpg'
    data = buf.getvalue()
    name = f'{base}-{hashlib.sha1(data).hexdigest()[:8]}.{ext}'
    os.makedirs(os.path.join(out_dir, folder), exist_ok=True)
    open(os.path.join(out_dir, folder, name), 'wb').write(data)
    return f'{folder}/{name}'


# ------------------------------------------------------------------ export

def _texts(src):
    blocks = []
    for s in src.get('secs') or []:
        blocks.append(['sec', latin(s['title'])])
        blocks += [['para', latin(x)] for x in s['paras']]
        blocks += [['item', latin(x)] for x in s['items']]
    return {
        'titulo': latin(src.get('title')), 'tag': latin(src.get('tag')), 'status': latin(src.get('status')),
        'resumo': latin(src.get('desc')), 'chamada': latin(src.get('feature_text')),
        'titulo_barras': latin(src.get('bars_title')), 'sobre': latin(src.get('about')), 'blocos': blocks,
        'barras': [[latin(a), int(b), latin(c or '')] for a, b, c in src.get('bars') or []],
        'ficha': [[latin(k), latin(v)] for k, v in src.get('meta') or []],
        'links': [[latin(k), v] for k, v in (src.get('links') or []) + (src.get('sources') or [])],
    }


def write_store(posts, order, feat, groups, out_dir):
    store_dir = 'store'
    items = []
    for slug in order:
        p = posts[slug]
        en = {**p, **(p['en'] or {})}
        it = {
            'slug': slug, 'cat': p['cat'], 'grupo': groups.index(p['group']), 'data': p['date'].isoformat(),
            'destaque': slug == feat, 'pixel': p['pixel'],
            'progresso': p['progress'] if p['progress'] is not None else -1,
            'pt': _texts(p), 'en': _texts(en), 'capturas': [],
            'video': f'https://youtu.be/{p["video"]}' if p['video'] else '',
            'downloads': [],
        }
        if p['cover']:
            img = Image.open(os.path.join(p['folder'], os.path.basename(p['cover'])))
            it['capa'] = _save(_fit(img, COVER, p['cover_style'], p['pixel']), p['pixel'], f'{store_dir}/{slug}', 'capa', out_dir)
        for i, s in enumerate(p['shots']):
            img = Image.open(os.path.join(p['folder'], os.path.basename(s)))
            it['capturas'].append(_save(_fit(img, SHOT, 'conter', p['pixel']), p['pixel'], f'{store_dir}/{slug}', f'cap{i}', out_dir))
        for d in p.get('downloads') or []:
            r = resolve_download(d, p['links'] + p.get('sources', []))
            if r:
                it['downloads'].append(r)
        items.append(it)
    store = {'formato': 1, 'app': app_release(), 'posts': items}
    with open(os.path.join(out_dir, 'store.json'), 'w', encoding='utf-8') as f:
        json.dump(store, f, ensure_ascii=False, separators=(',', ':'))
    nd = sum(len(i['downloads']) for i in items)
    app = store['app']['versao'] if store['app'] else 'nenhuma'
    print(f'store.json: {len(items)} posts, {nd} downloads, app {app}')
