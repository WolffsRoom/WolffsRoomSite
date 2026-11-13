#!/usr/bin/env python3
"""Gera o site do Wolff's Room a partir de content/posts/*/post.md.

Uso:
    python tools/build.py            # gera em _site/
    python -m http.server -d _site   # pré-visualiza em http://localhost:8000

Cada post é uma pasta em content/posts/<slug>/ com um post.md e as imagens
ao lado. Veja COMO-POSTAR.md para o formato.
"""
import datetime
import html
import json
import os
import re
import shutil
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, 'content', 'posts')
OUT = os.path.join(ROOT, '_site')
TEMPLATE = os.path.join(ROOT, 'tools', 'template.html')

e = html.escape
DF = "font-family: 'WR Start 2P', 'Press Start 2P', 'Pixelify Sans', monospace;"
CATS = [('ports', 'Ports'), ('ferramentas', 'Ferramentas'), ('traducoes', 'Traduções'), ('reviews', 'Reviews')]
CAT_NAMES = dict(CATS)
GROUPS = ['Em andamento', 'Finalizado', 'Próximos', 'Outras equipes']
SLUG_RE = re.compile(r'^[a-z0-9][a-z0-9-]*$')


class PostError(Exception):
    pass


# ---------------------------------------------------------------- leitura

def parse_markdown(body):
    """Separa o texto em 'sobre' (antes do primeiro ##) e seções (## Título + lista)."""
    about, secs, cur = [], [], None
    for line in body.splitlines():
        s = line.strip()
        if s.startswith('## '):
            cur = {'title': s[3:].strip(), 'items': [], 'paras': []}
            secs.append(cur)
        elif not s:
            continue
        elif cur is None:
            about.append(s)
        elif re.match(r'^[-*] ', s):
            cur['items'].append(s[2:].strip())
        else:
            cur['paras'].append(s)
    return ' '.join(about), secs


def inline(text):
    """Escapa o texto e converte [texto](url) e **negrito**."""
    out = e(text)
    out = re.sub(r'\[([^\]]+)\]\((https?://[^)\s]+)\)', r'<a href="\2" target="_blank" rel="noopener">\1</a>', out)
    out = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', out)
    return out


def parse_bars(raw):
    bars = []
    for label, val in (raw or {}).items():
        m = re.match(r'^\s*(\d{1,3})\s*%?\s*(?:\((.+)\))?\s*$', str(val))
        if not m:
            raise PostError(f'barra "{label}": use um número de 0 a 100, ex.: 80 ou "89 (192/216)"')
        bars.append((str(label), max(0, min(100, int(m.group(1)))), m.group(2)))
    return bars


TIPOS_DOWNLOAD = ('vpk', 'traducao', 'plugin', 'arquivo')


def parse_downloads(raw):
    """Campo `downloads:` do post (para o app Wolff's Store). Ver COMO-POSTAR.md."""
    if not raw:
        return []
    if not isinstance(raw, list):
        raise PostError('downloads: use uma lista (cada item começa com "- tipo: ...")')
    out = []
    for i, d in enumerate(raw, 1):
        if not isinstance(d, dict):
            raise PostError(f'downloads, item {i}: use campos como "tipo:" e "repo:" ou "url:"')
        tipo = str(d.get('tipo') or 'vpk').strip().lower().replace('ç', 'c').replace('ã', 'a')
        if tipo not in TIPOS_DOWNLOAD:
            raise PostError(f'downloads, item {i}: tipo "{d.get("tipo")}" inválido; use: ' + ', '.join(TIPOS_DOWNLOAD))
        if not d.get('url') and not d.get('repo'):
            raise PostError(f'downloads, item {i}: informe "repo:" (release do GitHub) ou "url:" (link direto)')
        if d.get('repo') and not re.fullmatch(r'[\w.-]+/[\w.-]+', str(d['repo'])):
            raise PostError(f'downloads, item {i}: repo deve ser "Dono/Repositorio"')
        tids = d.get('titleid') or []
        if isinstance(tids, str):
            tids = [t.strip() for t in re.split(r'[,\s]+', tids) if t.strip()]
        for t in tids:
            if not re.fullmatch(r'[A-Z]{4}\d{5}', str(t)):
                raise PostError(f'downloads, item {i}: titleid "{t}" inválido (ex.: PCSE00584)')
        if tipo == 'traducao' and not tids:
            raise PostError(f'downloads, item {i}: tradução precisa de "titleid:" (pasta do rePatch)')
        out.append({
            'tipo': tipo, 'nome': d.get('nome'), 'url': d.get('url'), 'repo': d.get('repo'),
            'arquivo': d.get('arquivo'), 'tag': d.get('tag'), 'versao': d.get('versao'),
            'tamanho': d.get('tamanho'), 'titleids': [str(t) for t in tids],
            'precisa_dados': bool(d.get('precisa_dados')), 'instrucoes': d.get('instrucoes'),
            'plugin': d.get('plugin') or ('rePatch' if tipo == 'traducao' else None),
        })
    return out


def load_post(slug):
    folder = os.path.join(CONTENT, slug)
    path = os.path.join(folder, 'post.md')
    raw = open(path, encoding='utf-8').read()
    m = re.match(r'^---\s*\n(.*?)\n---\s*\n?(.*)$', raw, re.S)
    if not m:
        raise PostError('o arquivo precisa começar com um cabeçalho entre linhas ---')
    meta = yaml.safe_load(m.group(1)) or {}
    body = m.group(2)
    for req in ('titulo', 'categoria', 'grupo', 'data'):
        if not meta.get(req):
            raise PostError(f'campo obrigatório ausente: {req}')
    cat = str(meta['categoria']).strip().lower().replace('ç', 'c').replace('õ', 'o')
    if cat not in CAT_NAMES:
        raise PostError(f'categoria "{meta["categoria"]}" inválida; use: ' + ', '.join(CAT_NAMES))
    group = str(meta['grupo']).strip()
    if group not in GROUPS:
        raise PostError(f'grupo "{group}" inválido; use: ' + ', '.join(GROUPS))
    date = meta['data']
    if isinstance(date, str):
        date = datetime.date.fromisoformat(date)
    about, secs = parse_markdown(body)

    def img(name):
        if not name:
            return None
        if not os.path.isfile(os.path.join(folder, name)):
            raise PostError(f'imagem não encontrada na pasta do post: {name}')
        return f'posts/{slug}/{name}'

    video = meta.get('video')
    vid = None
    if video:
        mv = re.search(r'(?:v=|youtu\.be/|embed/|shorts/)([A-Za-z0-9_-]{6,})', str(video))
        if not mv:
            raise PostError('video: use um link do YouTube')
        vid = mv.group(1)
    progress = meta.get('progresso')
    if progress is not None and str(progress).strip() != '':
        progress = max(0, min(100, int(progress)))
    else:
        progress = None
    p = {
        'slug': slug, 'title': str(meta['titulo']), 'cat': cat, 'group': group, 'date': date,
        'tag': str(meta.get('tag') or CAT_NAMES[cat]), 'status': str(meta.get('status') or group),
        'desc': str(meta.get('resumo') or ''), 'about': about, 'secs': secs,
        'progress': progress, 'bars': parse_bars(meta.get('barras')),
        'meta': [(str(k), str(v)) for k, v in (meta.get('ficha') or {}).items()],
        'links': [(str(k), str(v)) for k, v in (meta.get('links') or {}).items()],
        'cover': img(meta.get('capa')), 'cover_style': str(meta.get('capa_estilo') or 'cobrir'),
        'pixel': bool(meta.get('pixelado')), 'shots': [img(s) for s in (meta.get('capturas') or [])],
        'video': vid,
        'feature': bool(meta.get('destaque')), 'feature_text': str(meta.get('chamada') or meta.get('resumo') or ''),
        'folder': folder,
    }
    p['downloads'] = parse_downloads(meta.get('downloads'))
    p['video_label'] = str(meta.get('video_legenda') or '')
    p['bars_title'] = str(meta.get('titulo_barras') or '')
    p['en'] = load_english(folder, p)
    return p


def load_english(folder, p):
    """post.en.md: mesmos campos de texto, em inglês. Tudo é opcional."""
    path = os.path.join(folder, 'post.en.md')
    if not os.path.isfile(path):
        return None
    raw = open(path, encoding='utf-8').read()
    m = re.match(r'^---\s*\n(.*?)\n---\s*\n?(.*)$', raw, re.S)
    meta, body = (yaml.safe_load(m.group(1)) or {}, m.group(2)) if m else ({}, raw)
    about, secs = parse_markdown(body)
    en = {'about': about, 'secs': secs}
    for src, dst in (('titulo', 'title'), ('tag', 'tag'), ('status', 'status'), ('resumo', 'desc'),
                     ('video_legenda', 'video_label'), ('titulo_barras', 'bars_title')):
        if meta.get(src):
            en[dst] = str(meta[src])
    if meta.get('chamada') or meta.get('resumo'):
        en['feature_text'] = str(meta.get('chamada') or meta.get('resumo'))
    if meta.get('barras'):
        en['bars'] = parse_bars(meta['barras'])
    if meta.get('ficha'):
        en['meta'] = [(str(k), str(v)) for k, v in meta['ficha'].items()]
    if meta.get('links'):
        en['links'] = [(str(k), str(v)) for k, v in meta['links'].items()]
    if not en['about']:
        del en['about']
    if not en['secs']:
        del en['secs']
    return en


def load_all():
    posts, errors = {}, []
    for slug in sorted(os.listdir(CONTENT)):
        if not os.path.isfile(os.path.join(CONTENT, slug, 'post.md')):
            continue
        if not SLUG_RE.match(slug):
            errors.append(f'{slug}: o nome da pasta deve ter só letras minúsculas, números e hífen')
            continue
        try:
            posts[slug] = load_post(slug)
        except (PostError, ValueError, yaml.YAMLError) as ex:
            errors.append(f'{slug}/post.md: {ex}')
    if errors:
        sys.exit('Erros nos posts:\n  - ' + '\n  - '.join(errors))
    order = sorted(posts, key=lambda k: (posts[k]['date'], k), reverse=True)
    return posts, order


# ---------------------------------------------------------------- HTML

UI = {
    'pt': {
        'cats': {'ports': 'Ports', 'ferramentas': 'Ferramentas', 'traducoes': 'Traduções', 'reviews': 'Reviews'},
        'groups': {g: g for g in GROUPS}, 'nothing': 'Nada por aqui ainda.', 'back': 'Voltar', 'back_home': 'Voltar ao início',
        'repos': 'Todos os repositórios no GitHub', 'shots': 'Capturas de tela', 'video': 'Vídeo', 'watch': 'Assistir no YouTube',
        'video_note': 'O vídeo abre no YouTube.', 'info': 'Detalhes', 'links': 'Links', 'total': 'Total', 'progress': 'Progresso',
        'latest': 'Últimos em', 'see_all': 'Ver todos', 'details': 'Ver detalhes', 'github': 'Ver no GitHub',
        'start': 'Pressione start', 'click': 'Clique para começar', 'kicker': 'O que será que o Wolff está fazendo...?',
        'cover_of': 'Capa de', 'shot_of': 'Captura de tela de', 'open': 'Abrir', 'video_default': 'Vídeo do projeto',
    },
    'en': {
        'cats': {'ports': 'Ports', 'ferramentas': 'Tools', 'traducoes': 'Translations', 'reviews': 'Reviews'},
        'groups': {'Em andamento': 'In progress', 'Finalizado': 'Finished', 'Próximos': 'Upcoming', 'Outras equipes': 'Other teams'},
        'nothing': 'Nothing here yet.', 'back': 'Back', 'back_home': 'Back to home', 'repos': 'All repositories on GitHub',
        'shots': 'Screenshots', 'video': 'Video', 'watch': 'Watch on YouTube', 'video_note': 'The video opens on YouTube.',
        'info': 'Details', 'links': 'Links', 'total': 'Total', 'progress': 'Progress', 'latest': 'Latest in', 'see_all': 'See all',
        'details': 'See details', 'github': 'View on GitHub', 'start': 'Press start', 'click': 'Click to begin',
        'kicker': 'What could Wolff be up to...?', 'cover_of': 'Cover of', 'shot_of': 'Screenshot of', 'open': 'Open',
        'video_default': 'Project video',
    },
}


def T(pt, en):
    """Texto nos dois idiomas (já em HTML). O CSS mostra só o idioma ativo."""
    if pt == en:
        return pt
    return f'<span data-l="pt">{pt}</span><span data-l="en">{en}</span>'


def U(key):
    return T(e(UI['pt'][key]), e(UI['en'][key]))


def V(p, lang):
    """Os campos do post no idioma pedido (inglês cai no português quando falta)."""
    if lang == 'pt' or not p.get('en'):
        return p
    q = dict(p)
    q.update({k: v for k, v in p['en'].items() if v not in (None, '', [])})
    return q


def F(p, field, fn=e):
    return T(fn(str(V(p, 'pt')[field])), fn(str(V(p, 'en')[field])))


def pic(p, lang='en'):
    alt = e(UI[lang]['cover_of'] + ' ' + V(p, lang)['title'])
    if not p['cover']:
        return f'<div style="aspect-ratio: 16 / 9; background: #161616; display: flex; align-items: center; justify-content: center; text-align: center; color: #a8a8a8; font-size: 16px; padding: 12px; box-sizing: border-box">{F(p, "title")}</div>'
    if p['cover_style'] == 'logo':
        return f'<div style="aspect-ratio: 16 / 9; background: #000000; display: flex; align-items: center; justify-content: center">\n<img src="{p["cover"]}" alt="{alt}" style="max-width: 70%; max-height: 70%; display: block">\n</div>'
    px = '; image-rendering: pixelated' if p['pixel'] else ''
    return f'<img src="{p["cover"]}" alt="{alt}" loading="lazy" style="width: 100%; aspect-ratio: 16 / 9; object-fit: cover; display: block{px}">'


def card(p):
    return ('<a class="wr-card wr-sh-s" href="#' + p['slug'] + '" data-act="open_' + p['slug'] + '" style="display: flex; flex-direction: column; border: 4px solid #5a5a5a; background: #0e0e0e; color: #ffffff; text-decoration: none">\n'
            '<div style="border-bottom: 4px solid #2e2e2e; background: #0b0b0b">\n' + pic(p) + '\n</div>\n'
            '<div style="padding: 16px; display: flex; flex-direction: column; gap: 10px; flex-grow: 1">\n'
            f'<span style="color: #a8a8a8; font-size: 15px; letter-spacing: 1px; text-transform: uppercase">{F(p, "tag")}</span>\n'
            f'<strong style="{DF} font-size: 16px; line-height: 1.5; font-weight: 400">{F(p, "title")}</strong>\n'
            f'<span style="color: #c4c4c4; flex-grow: 1">{F(p, "desc")}</span>\n'
            f'<span style="font-weight: 700">{F(p, "status")}</span>\n'
            '</div>\n</a>')


def bar(label, pct, text=None):
    text = text or f'{pct}%'
    return ('<div style="display: flex; flex-direction: column; gap: 8px">\n'
            f'<div style="display: flex; justify-content: space-between; align-items: baseline; gap: 12px"><span>{e(label)}</span><span style="{DF} font-size: 16px">{e(text)}</span></div>\n'
            f'<div class="wr-pb" role="img" aria-label="{e(label)}: {e(text)}"><div class="wr-pb-track"><div class="wr-pb-fill" style="width: {pct}%"></div></div></div>\n</div>')


BOX = 'border: 4px solid #5a5a5a; background: #0e0e0e; padding: 20px; display: flex; flex-direction: column; gap: 16px'
H2 = f'margin: 0; {DF} font-size: 16px; line-height: 1.5; font-weight: 400; text-transform: uppercase'
PLAY = ('<svg aria-hidden="true" width="64" height="64" viewBox="0 0 16 16" shape-rendering="crispEdges" style="display: block">'
        '<rect x="0" y="0" width="16" height="16" fill="#0b0b0b"/><rect x="1" y="1" width="14" height="14" fill="#ffffff"/><rect x="2" y="2" width="12" height="12" fill="#0b0b0b"/>'
        '<rect x="5" y="4" width="2" height="8" fill="#ffffff"/><rect x="7" y="5" width="2" height="6" fill="#ffffff"/><rect x="9" y="6" width="2" height="4" fill="#ffffff"/><rect x="11" y="7" width="1" height="2" fill="#ffffff"/></svg>')


def section(title, inner):
    return (f'<section style="display: flex; flex-direction: column; gap: 12px">\n<h2 style="{H2}; border-bottom: 4px solid #2e2e2e; padding-bottom: 10px">{e(title)}</h2>\n'
            + inner + '</section>\n')


def article(p0, lang):
    p, ui = V(p0, lang), UI[lang]
    secs = ''
    for s in p['secs']:
        inner = ''.join(f'<p style="margin: 0; color: #d6d6d6">{inline(t)}</p>\n' for t in s['paras'])
        if s['items']:
            lis = '\n'.join(f'<li>{inline(i)}</li>' for i in s['items'])
            inner += f'<ul style="margin: 0; padding-left: 22px; display: flex; flex-direction: column; gap: 6px; color: #d6d6d6; list-style: square">\n{lis}\n</ul>\n'
        secs += section(s['title'], inner)
    if p['shots']:
        imgs = '\n'.join(f'<div class="wr-shot" style="border: 4px solid #5a5a5a; background: #000000; line-height: 0"><img src="{s}" alt="{e(ui["shot_of"] + " " + p["title"])}" loading="lazy" style="width: 100%; height: auto; display: block"></div>' for s in p['shots'])
        secs += section(ui['shots'], f'<div class="wr-shots" style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px">\n{imgs}\n</div>\n')
    if p['video']:
        label = p['video_label'] or ui['video_default']
        bg = (f'<img src="{p["cover"]}" alt="" loading="lazy" style="width: 100%; aspect-ratio: 16 / 9; object-fit: cover; display: block; opacity: 0.45">'
              if p['cover'] and p['cover_style'] != 'logo' else '<div style="aspect-ratio: 16 / 9; background: #161616"></div>')
        url = 'https://www.youtube.com/watch?v=' + p['video']
        secs += section(ui['video'],
                        f'<a class="wr-video wr-sh-s" href="{url}" target="_blank" rel="noopener" aria-label="{e(label)} — {e(ui["watch"])}" style="position: relative; display: block; border: 4px solid #ffffff; background: #000000; line-height: 0; color: #ffffff; text-decoration: none">\n{bg}\n'
                        f'<span style="position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 16px; line-height: 1.5">{PLAY}<span style="{DF} font-size: 16px; text-transform: uppercase; text-shadow: 4px 4px 0 #000000">{e(ui["watch"])}</span></span>\n</a>\n'
                        f'<span style="color: #a8a8a8">{e(label)}. {e(ui["video_note"])}</span>\n')
    side = ''
    if p['meta']:
        rows = '\n'.join(f'<div style="display: flex; flex-wrap: wrap; justify-content: space-between; column-gap: 16px; row-gap: 2px; border-bottom: 4px solid #2e2e2e; padding-bottom: 8px"><dt style="flex: 0 0 auto; color: #a8a8a8">{e(k)}</dt><dd style="margin: 0 0 0 auto; flex: 0 1 auto; text-align: right; font-weight: 700">{inline(v)}</dd></div>' for k, v in p['meta'])
        side += f'<div class="wr-sh-s" style="{BOX}">\n<h2 style="{H2}">{e(ui["info"])}</h2>\n<dl style="margin: 0; display: flex; flex-direction: column; gap: 8px">\n{rows}\n</dl>\n</div>\n'
    bars = ([bar(ui['total'], p['progress'])] if p['progress'] is not None else []) + [bar(*b) for b in p['bars']]
    if bars:
        side += f'<div class="wr-sh-s" style="{BOX}">\n<h2 style="{H2}">{e(p["bars_title"] or ui["progress"])}</h2>\n' + '\n'.join(bars) + '\n</div>\n'
    if p['links']:
        links = ''
        for i, (lab, url) in enumerate(p['links']):
            st = 'background: #ffffff; color: #0b0b0b; border: 4px solid #ffffff' if i == 0 else 'background: #0b0b0b; color: #ffffff; border: 4px solid #8a8a8a'
            links += f'<a class="wr-btn" href="{e(url)}" target="_blank" rel="noopener" style="min-height: 48px; box-sizing: border-box; padding: 12px 14px; {st}; text-decoration: none; text-align: center; {DF} font-size: 16px; line-height: 1.6; text-transform: uppercase">{e(lab)}</a>\n'
        side += f'<div class="wr-sh-s" style="{BOX}">\n<h2 style="{H2}">{e(ui["links"])}</h2>\n{links}</div>\n'
    hero = (f'<div class="wr-sh-s" style="border: 4px solid #ffffff; background: #000000">\n{pic(p0, lang)}\n</div>\n' if p['cover'] else '')
    about = f'<p style="margin: 0; color: #e0e0e0; font-size: 19px">{inline(p["about"])}</p>\n' if p['about'] else ''
    return (f'<article lang="{"en" if lang == "en" else "pt-BR"}" data-l="{lang}" aria-label="{e(p["title"])}" style="display: flex; flex-direction: column; gap: 28px">\n'
            '<div style="display: flex; flex-wrap: wrap; gap: 12px 24px; justify-content: space-between; align-items: center">\n'
            f'<span style="color: #a8a8a8; letter-spacing: 1px; text-transform: uppercase">{e(p["tag"])} · {e(p["status"])}</span>\n'
            '<button class="wr-btn" type="button" data-act="back_' + p['slug'] + '" style="min-height: 44px; padding: 8px 16px; border: 4px solid #8a8a8a; background: #0b0b0b; color: #ffffff; ' + DF + ' font-size: 16px; line-height: 1.6; text-transform: uppercase; cursor: pointer">' + e(ui['back']) + '</button>\n'
            '</div>\n'
            f'<h1 style="margin: 0; {DF} font-size: 32px; line-height: 1.5; font-weight: 400; text-align: center; text-shadow: 4px 4px 0 #3a3a3a; border-bottom: 4px solid #2e2e2e; padding-bottom: 16px">{e(p["title"])}</h1>\n'
            '<div style="display: flex; flex-wrap: wrap; gap: 40px; align-items: flex-start">\n'
            '<div style="flex: 999 1 520px; min-width: 0; display: flex; flex-direction: column; gap: 28px">\n'
            + hero + about + secs +
            '</div>\n'
            '<aside style="flex: 1 1 280px; min-width: 0; display: flex; flex-direction: column; gap: 36px">\n' + side + '</aside>\n'
            '</div>\n</article>\n')


def detail(p):
    return '\n<div class="dc-if" data-if="p_' + p['slug'] + '">\n' + article(p, 'en') + article(p, 'pt') + '</div>\n'


def lists_html(posts, order):
    out = ''
    for n, (cid, _t) in enumerate(CATS, 1):
        body = ''
        groups = GROUPS if any(posts[k]['group'] == 'Outras equipes' and posts[k]['cat'] == cid for k in order) else GROUPS[:3]
        for g in groups:
            ids = [k for k in order if posts[k]['cat'] == cid and posts[k]['group'] == g]
            gname = T(e(UI['pt']['groups'][g]), e(UI['en']['groups'][g]))
            body += ('<div style="display: flex; flex-direction: column; gap: 28px">\n'
                     f'<h2 style="margin: 0; {DF} font-size: 16px; line-height: 1.5; font-weight: 400; text-transform: uppercase; text-align: center; color: #c4c4c4">{gname} <span style="color: #8a8a8a">({len(ids)})</span></h2>\n')
            if ids:
                body += '<div class="wr-grid" style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 36px">\n\n' + '\n\n'.join(card(posts[i]) for i in ids) + '\n\n</div>\n'
            else:
                body += f'<p style="margin: 0; text-align: center; color: #8a8a8a">{U("nothing")}</p>\n'
            body += '</div>\n'
        if cid in ('ports', 'ferramentas'):
            body += ('<a class="wr-btn" href="https://github.com/WolffsRoom?tab=repositories" target="_blank" rel="noopener" style="align-self: center; min-height: 48px; box-sizing: border-box; padding: 12px 20px; border: 4px solid #8a8a8a; background: #0b0b0b; color: #ffffff; text-decoration: none; text-align: center; ' + DF + ' font-size: 16px; line-height: 1.6; text-transform: uppercase">' + U('repos') + '</a>\n')
        title = T(e(UI['pt']['cats'][cid]), e(UI['en']['cats'][cid]))
        out += ('\n<div class="dc-if" data-if="on' + str(n) + '">\n'
                f'<section aria-label="{e(UI["en"]["cats"][cid])}" style="display: flex; flex-direction: column; gap: 44px">\n'
                '<div style="display: flex; flex-wrap: wrap; gap: 12px 24px; justify-content: space-between; align-items: center; border-bottom: 4px solid #2e2e2e; padding-bottom: 12px">\n'
                f'<h1 style="margin: 0; {DF} font-size: 32px; line-height: 1.5; font-weight: 400; text-transform: uppercase; text-shadow: 4px 4px 0 #3a3a3a">{title}</h1>\n'
                '<button class="wr-btn" type="button" data-act="goHome" style="min-height: 44px; padding: 8px 16px; border: 4px solid #8a8a8a; background: #0b0b0b; color: #ffffff; ' + DF + ' font-size: 16px; line-height: 1.6; text-transform: uppercase; cursor: pointer">' + U('back_home') + '</button>\n'
                '</div>\n' + body + '</section>\n</div>\n')
    return out


def kicker_words(text):
    """Letras com atraso próprio, agrupadas por palavra para a linha só quebrar entre palavras."""
    out, i, words = [], 0, text.split(' ')
    for w, word in enumerate(words):
        spans = ''
        for ch in word:
            spans += '<span class="wr-ch" aria-hidden="true" style="animation-delay: %.2fs">%s</span>' % (0.3 + i * 0.045, e(ch))
            i += 1
        if w == len(words) - 1:
            spans += '<span class="wr-caret" aria-hidden="true"></span>'
        out.append('<span class="wr-word">' + spans + '</span>')
        i += 1  # o espaço também conta no tempo da digitação
    return ' '.join(out)


def home_html(posts, order, feat, mosaic):
    p = posts[feat]
    gh = next((u for l, u in p['links'] if 'github' in u.lower()), None)
    BTN = f'min-height: 48px; box-sizing: border-box; padding: 12px 20px; text-decoration: none; text-align: center; {DF} font-size: 16px; line-height: 1.5; text-transform: uppercase'
    px = '; image-rendering: pixelated' if p['pixel'] else ''
    mos = ''.join(f'<img class="wr-mos" src="{src}" alt="" aria-hidden="true" style="animation-delay: {t}s">\n' for src, t in reversed(mosaic))
    kicker = ''.join(
        f'<p class="wr-type" data-l="{lg}" aria-label="{e(UI[lg]["kicker"])}" style="margin: 0; {DF} font-size: 32px; line-height: 1.5; color: #ffffff; text-shadow: 4px 4px 0 #3a3a3a; text-align: center; max-width: 1100px">'
        + kicker_words(UI[lg]['kicker']) + '</p>\n' for lg in ('en', 'pt'))
    art = (f'<img src="{p["cover"]}" alt="{e(UI["en"]["cover_of"] + " " + V(p, "en")["title"])}" data-onload="featLoad" style="width: 100%; height: auto; display: block{px}">\n'
           if p['cover'] else f'<div style="aspect-ratio: 16 / 9; background: #161616"></div>\n')
    buttons = '<a class="wr-btn" href="#' + feat + '" data-act="open_' + feat + '" style="' + BTN + '; border: 4px solid #ffffff; background: #ffffff; color: #0b0b0b; box-shadow: 4px 4px 0 #4a4a4a">' + U('details') + '</a>\n'
    if gh:
        buttons += f'<a class="wr-btn" href="{e(gh)}" target="_blank" rel="noopener" style="{BTN}; border: 4px solid #8a8a8a; background: #0b0b0b; color: #ffffff">{U("github")}</a>\n'
    feat_html = (
        '<div class="dc-if" data-if="on0">\n'
        '<section class="wr-home" aria-label="' + e(UI['en']['open']) + ' ' + e(V(p, 'en')['title']) + '" style="display: flex; flex-direction: column; align-items: center; gap: 28px; text-align: center">\n'
        '<div class="wr-feat-wrap" data-bbase="wr-feat-wrap" data-bclass="featCls" style="width: 100%; max-width: 720px; display: flex; flex-direction: column; align-items: center; gap: 44px">\n'
        '<div class="wr-stage">\n<div class="wr-tvbox">\n'
        '<a class="wr-link wr-feat-art wr-sh" href="#' + feat + '" data-act="open_' + feat + '" aria-label="' + e(UI['en']['open']) + ' ' + e(V(p, 'en')['title']) + '" style="position: relative; display: block; width: 100%; line-height: 0; background: #000000">\n'
        + art + mos + '</a>\n</div>\n<div class="wr-kick">\n' + kicker + '</div>\n'
        '<button class="wr-start" type="button" data-act="startIntro"><span>&#9654; ' + U('start') + '</span><small>' + U('click') + '</small></button>\n</div>\n' +
        '<div class="wr-feat-info" style="display: flex; flex-direction: column; align-items: center; gap: 14px">\n'
        f'<span style="color: #a8a8a8; letter-spacing: 1px; text-transform: uppercase">{F(p, "tag")} · {F(p, "status")}</span>\n'
        f'<h1 style="margin: 0; {DF} font-size: 32px; line-height: 1.4; font-weight: 400; text-shadow: 4px 4px 0 #3a3a3a">{F(p, "title")}</h1>\n'
        f'<p style="margin: 0; color: #c4c4c4; max-width: 640px">{F(p, "feature_text", inline)}</p>\n'
        '<div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 16px; margin-top: 6px">\n' + buttons + '</div>\n'
        '</div>\n</div>\n</section>\n</div>\n')
    btns = '\n'.join(
        f'<button class="wr-btn wr-sh-s wr-cat" type="button" data-hover="hov" data-act="pick{n}" data-b-aria-expanded="pk{n}" style="min-height: 64px; padding: 12px; border: 4px solid #8a8a8a; background: #141414; color: #ffffff; {DF} font-size: 16px; line-height: 1.5; text-transform: uppercase; cursor: pointer">{T(e(UI["pt"]["cats"][c]), e(UI["en"]["cats"][c]))}</button>'
        for n, (c, t) in enumerate(CATS, 1))
    nav = ('<div class="dc-if" data-if="on0">\n'
           f'<nav class="wr-nav" aria-label="Categories" style="display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 32px">\n{btns}\n</nav>\n</div>\n')
    peeks = ''
    for n, (c, t) in enumerate(CATS, 1):
        ids = [k for k in order if posts[k]['cat'] == c]
        cards = '\n'.join(card(posts[i]) for i in ids[:3]) or f'<p style="margin: 0; text-align: center; color: #8a8a8a">{U("nothing")}</p>'
        head = T(e(UI['pt']['latest'] + ' ' + UI['pt']['cats'][c]), e(UI['en']['latest'] + ' ' + UI['en']['cats'][c]))
        peeks += ('<div class="dc-if" data-if="pk' + str(n) + '">\n'
                  f'<section class="wr-peek" aria-label="{e(UI["en"]["latest"] + " " + UI["en"]["cats"][c])}" style="display: flex; flex-direction: column; gap: 24px">\n'
                  f'<h2 style="margin: 0; {DF} font-size: 16px; line-height: 1.5; font-weight: 400; text-transform: uppercase; text-align: center; color: #c4c4c4">{head}</h2>\n'
                  f'<div class="wr-grid" style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 36px">\n{cards}\n</div>\n'
                  '<button class="wr-btn" type="button" data-act="all' + str(n) + '" style="align-self: center; min-height: 48px; padding: 12px 20px; border: 4px solid #ffffff; background: #ffffff; color: #0b0b0b; ' + DF + f' font-size: 16px; line-height: 1.5; text-transform: uppercase; cursor: pointer; box-shadow: 4px 4px 0 #4a4a4a">{U("see_all")} ({len(ids)})</button>\n'
                  '</section>\n</div>\n')
    return feat_html + nav + peeks


# ---------------------------------------------------------------- build

def make_mosaic(p, out_dir):
    """Versões em baixa resolução da capa do destaque, para a animação de entrada."""
    if not p['cover']:
        return []
    try:
        from PIL import Image
    except ImportError:
        print('aviso: Pillow não instalado; a animação de mosaico fica desligada')
        return []
    im = Image.open(os.path.join(ROOT, 'content', p['cover'])).convert('RGB')
    res = []
    widths = (12, 20, 32, 48, 72, 112, 176, 288)
    for k, w in enumerate(widths):
        t = round(3.18 + k * 0.13, 2)
        h = max(1, round(im.height * w / im.width))
        name = f'destaque-m{w}.png'
        im.resize((w, h), Image.BOX).save(os.path.join(out_dir, name), optimize=True)
        res.append((f'assets/{name}', t))
    return res


def build():
    posts, order = load_all()
    feats = [k for k in order if posts[k]['feature']]
    if not feats:
        sys.exit('Nenhum post com "destaque: true". Marque o projeto que aparece na página inicial.')
    feat = feats[0]
    if len(feats) > 1:
        print(f'aviso: mais de um post com destaque; usando o mais recente ({feat})')

    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    shutil.copytree(os.path.join(ROOT, 'assets'), os.path.join(OUT, 'assets'))
    for slug, p in posts.items():
        dst = os.path.join(OUT, 'posts', slug)
        os.makedirs(dst, exist_ok=True)
        for f in os.listdir(p['folder']):
            if f != 'post.md':
                shutil.copy(os.path.join(p['folder'], f), dst)
    mosaic = make_mosaic(posts[feat], os.path.join(OUT, 'assets'))

    main = home_html(posts, order, feat, mosaic) + lists_html(posts, order) + ''.join(detail(posts[k]) for k in order)
    cats = '{' + ', '.join(f"'{k}': '{posts[k]['cat']}'" for k in order) + '}'
    page = open(TEMPLATE, encoding='utf-8').read()
    page = page.replace('<!--MAIN-->', main).replace('/*CATS*/{}', cats)
    page = page.replace('<!--OGIMAGE-->', posts[feat]['cover'] or 'assets/favicon.png')
    open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(page)
    open(os.path.join(OUT, '.nojekyll'), 'w').write('')
    import store  # catálogo do app Wolff's Store (PS Vita)
    store.write_store(posts, order, feat, GROUPS, OUT)
    en = sum(1 for p in posts.values() if p['en'])
    print(f'ok: {len(posts)} posts ({en} com inglês), destaque = {feat}, saída em {os.path.relpath(OUT, ROOT)}/')


if __name__ == '__main__':
    build()
