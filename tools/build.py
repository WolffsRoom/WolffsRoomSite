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
DF = "font-family: 'Press Start 2P', 'Pixelify Sans', monospace;"
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
    out = re.sub(r'\[([^\]]+)\]\((https?://[^)\s]+)\)', r'<a href="\2">\1</a>', out)
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
    return {
        'slug': slug, 'title': str(meta['titulo']), 'cat': cat, 'group': group, 'date': date,
        'tag': str(meta.get('tag') or CAT_NAMES[cat]), 'status': str(meta.get('status') or group),
        'desc': str(meta.get('resumo') or ''), 'about': about, 'secs': secs,
        'progress': progress, 'bars': parse_bars(meta.get('barras')),
        'bars_title': str(meta.get('titulo_barras') or 'Progresso'),
        'meta': [(str(k), str(v)) for k, v in (meta.get('ficha') or {}).items()],
        'links': [(str(k), str(v)) for k, v in (meta.get('links') or {}).items()],
        'cover': img(meta.get('capa')), 'cover_style': str(meta.get('capa_estilo') or 'cobrir'),
        'pixel': bool(meta.get('pixelado')), 'shots': [img(s) for s in (meta.get('capturas') or [])],
        'video': vid, 'video_label': str(meta.get('video_legenda') or 'Vídeo do projeto'),
        'feature': bool(meta.get('destaque')), 'feature_text': str(meta.get('chamada') or meta.get('resumo') or ''),
        'folder': folder,
    }


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

def pic(p):
    alt = e('Capa de ' + p['title'])
    if not p['cover']:
        return f'<div style="aspect-ratio: 16 / 9; background: #161616; display: flex; align-items: center; justify-content: center; text-align: center; color: #a8a8a8; font-size: 16px; padding: 12px; box-sizing: border-box">{e(p["title"])}</div>'
    if p['cover_style'] == 'logo':
        return f'<div style="aspect-ratio: 16 / 9; background: #000000; display: flex; align-items: center; justify-content: center">\n<img src="{p["cover"]}" alt="{alt}" style="max-width: 70%; max-height: 70%; display: block">\n</div>'
    px = '; image-rendering: pixelated' if p['pixel'] else ''
    return f'<img src="{p["cover"]}" alt="{alt}" loading="lazy" style="width: 100%; aspect-ratio: 16 / 9; object-fit: cover; display: block{px}">'


def card(p):
    return ('<a class="wr-card wr-sh-s" href="#topo" data-act="open_' + p['slug'] + '" style="display: flex; flex-direction: column; border: 4px solid #5a5a5a; background: #0e0e0e; color: #ffffff; text-decoration: none">\n'
            '<div style="border-bottom: 4px solid #2e2e2e; background: #0b0b0b">\n' + pic(p) + '\n</div>\n'
            '<div style="padding: 16px; display: flex; flex-direction: column; gap: 10px; flex-grow: 1">\n'
            f'<span style="color: #a8a8a8; font-size: 15px; letter-spacing: 1px; text-transform: uppercase">{e(p["tag"])}</span>\n'
            f'<strong style="{DF} font-size: 16px; line-height: 1.5; font-weight: 400">{e(p["title"])}</strong>\n'
            f'<span style="color: #c4c4c4; flex-grow: 1">{e(p["desc"])}</span>\n'
            f'<span style="font-weight: 700">{e(p["status"])}</span>\n'
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


def detail(p):
    secs = ''
    for s in p['secs']:
        inner = ''.join(f'<p style="margin: 0; color: #d6d6d6">{inline(t)}</p>\n' for t in s['paras'])
        if s['items']:
            lis = '\n'.join(f'<li>{inline(i)}</li>' for i in s['items'])
            inner += f'<ul style="margin: 0; padding-left: 22px; display: flex; flex-direction: column; gap: 6px; color: #d6d6d6; list-style: square">\n{lis}\n</ul>\n'
        secs += section(s['title'], inner)
    if p['shots']:
        imgs = '\n'.join(f'<div class="wr-shot" style="border: 4px solid #5a5a5a; background: #000000; line-height: 0"><img src="{s}" alt="Captura de tela de {e(p["title"])}" loading="lazy" style="width: 100%; height: auto; display: block"></div>' for s in p['shots'])
        secs += section('Capturas de tela', f'<div class="wr-shots" style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px">\n{imgs}\n</div>\n')
    if p['video']:
        bg = (f'<img src="{p["cover"]}" alt="" loading="lazy" style="width: 100%; aspect-ratio: 16 / 9; object-fit: cover; display: block; opacity: 0.45">'
              if p['cover'] and p['cover_style'] != 'logo' else '<div style="aspect-ratio: 16 / 9; background: #161616"></div>')
        url = 'https://www.youtube.com/watch?v=' + p['video']
        secs += section('Vídeo',
                        f'<a class="wr-video wr-sh-s" href="{url}" aria-label="{e(p["video_label"])} — assistir no YouTube" style="position: relative; display: block; border: 4px solid #ffffff; background: #000000; line-height: 0; color: #ffffff; text-decoration: none">\n{bg}\n'
                        f'<span style="position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 16px; line-height: 1.5">{PLAY}<span style="{DF} font-size: 16px; text-transform: uppercase; text-shadow: 4px 4px 0 #000000">Assistir no YouTube</span></span>\n</a>\n'
                        f'<span style="color: #a8a8a8">{e(p["video_label"])}. O vídeo abre no YouTube.</span>\n')
    side = ''
    if p['meta']:
        rows = '\n'.join(f'<div style="display: flex; justify-content: space-between; gap: 16px; border-bottom: 4px solid #2e2e2e; padding-bottom: 8px"><dt style="color: #a8a8a8">{e(k)}</dt><dd style="margin: 0; text-align: right; font-weight: 700">{inline(v)}</dd></div>' for k, v in p['meta'])
        side += f'<div class="wr-sh-s" style="{BOX}">\n<h2 style="{H2}">Ficha</h2>\n<dl style="margin: 0; display: flex; flex-direction: column; gap: 8px">\n{rows}\n</dl>\n</div>\n'
    bars = ([bar('Total', p['progress'])] if p['progress'] is not None else []) + [bar(*b) for b in p['bars']]
    if bars:
        side += f'<div class="wr-sh-s" style="{BOX}">\n<h2 style="{H2}">{e(p["bars_title"])}</h2>\n' + '\n'.join(bars) + '\n</div>\n'
    if p['links']:
        links = ''
        for i, (lab, url) in enumerate(p['links']):
            st = 'background: #ffffff; color: #0b0b0b; border: 4px solid #ffffff' if i == 0 else 'background: #0b0b0b; color: #ffffff; border: 4px solid #8a8a8a'
            links += f'<a class="wr-btn" href="{e(url)}" style="min-height: 48px; box-sizing: border-box; padding: 12px 14px; {st}; text-decoration: none; text-align: center; {DF} font-size: 16px; line-height: 1.6; text-transform: uppercase">{e(lab)}</a>\n'
        side += f'<div class="wr-sh-s" style="{BOX}">\n<h2 style="{H2}">Links</h2>\n{links}</div>\n'
    hero = (f'<div class="wr-sh-s" style="border: 4px solid #ffffff; background: #000000">\n{pic(p)}\n</div>\n' if p['cover'] else '')
    about = f'<p style="margin: 0; color: #e0e0e0; font-size: 19px">{inline(p["about"])}</p>\n' if p['about'] else ''
    return ('\n<div class="dc-if" data-if="p_' + p['slug'] + '">\n'
            f'<article aria-label="{e(p["title"])}" style="display: flex; flex-direction: column; gap: 28px">\n'
            '<div style="display: flex; flex-wrap: wrap; gap: 12px 24px; justify-content: space-between; align-items: center">\n'
            f'<span style="color: #a8a8a8; letter-spacing: 1px; text-transform: uppercase">{e(p["tag"])} · {e(p["status"])}</span>\n'
            '<button class="wr-btn" type="button" data-act="back_' + p['slug'] + '" style="min-height: 44px; padding: 8px 16px; border: 4px solid #8a8a8a; background: #0b0b0b; color: #ffffff; ' + DF + ' font-size: 16px; line-height: 1.6; text-transform: uppercase; cursor: pointer">Voltar</button>\n'
            '</div>\n'
            f'<h1 style="margin: 0; {DF} font-size: 32px; line-height: 1.5; font-weight: 400; text-align: center; text-shadow: 4px 4px 0 #3a3a3a; border-bottom: 4px solid #2e2e2e; padding-bottom: 16px">{e(p["title"])}</h1>\n'
            '<div style="display: flex; flex-wrap: wrap; gap: 40px; align-items: flex-start">\n'
            '<div style="flex: 999 1 520px; min-width: 0; display: flex; flex-direction: column; gap: 28px">\n'
            + hero + about + secs +
            '</div>\n'
            '<aside style="flex: 1 1 280px; min-width: 0; display: flex; flex-direction: column; gap: 36px">\n' + side + '</aside>\n'
            '</div>\n</article>\n</div>\n')


def lists_html(posts, order):
    out = ''
    for n, (cid, title) in enumerate(CATS, 1):
        body = ''
        groups = GROUPS if any(posts[k]['group'] == 'Outras equipes' and posts[k]['cat'] == cid for k in order) else GROUPS[:3]
        for g in groups:
            ids = [k for k in order if posts[k]['cat'] == cid and posts[k]['group'] == g]
            body += ('<div style="display: flex; flex-direction: column; gap: 28px">\n'
                     f'<h2 style="margin: 0; {DF} font-size: 16px; line-height: 1.5; font-weight: 400; text-transform: uppercase; text-align: center; color: #c4c4c4">{e(g)} <span style="color: #8a8a8a">({len(ids)})</span></h2>\n')
            if ids:
                body += '<div class="wr-grid" style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 36px">\n\n' + '\n\n'.join(card(posts[i]) for i in ids) + '\n\n</div>\n'
            else:
                body += '<p style="margin: 0; text-align: center; color: #8a8a8a">Nada por aqui ainda.</p>\n'
            body += '</div>\n'
        if cid in ('ports', 'ferramentas'):
            body += ('<a class="wr-btn" href="https://github.com/WolffsRoom?tab=repositories" style="align-self: center; min-height: 48px; box-sizing: border-box; padding: 12px 20px; border: 4px solid #8a8a8a; background: #0b0b0b; color: #ffffff; text-decoration: none; text-align: center; ' + DF + ' font-size: 16px; line-height: 1.6; text-transform: uppercase">Todos os repositórios no GitHub</a>\n')
        out += ('\n<div class="dc-if" data-if="on' + str(n) + '">\n'
                f'<section aria-label="{e(title)}" style="display: flex; flex-direction: column; gap: 44px">\n'
                '<div style="display: flex; flex-wrap: wrap; gap: 12px 24px; justify-content: space-between; align-items: center; border-bottom: 4px solid #2e2e2e; padding-bottom: 12px">\n'
                f'<h1 style="margin: 0; {DF} font-size: 32px; line-height: 1.5; font-weight: 400; text-transform: uppercase; text-shadow: 4px 4px 0 #3a3a3a">{e(title)}</h1>\n'
                '<button class="wr-btn" type="button" data-act="goHome" style="min-height: 44px; padding: 8px 16px; border: 4px solid #8a8a8a; background: #0b0b0b; color: #ffffff; ' + DF + ' font-size: 16px; line-height: 1.6; text-transform: uppercase; cursor: pointer">Voltar ao início</button>\n'
                '</div>\n' + body + '</section>\n</div>\n')
    return out


KT = 'O que será que o Wolff está fazendo...?'


def kicker_words():
    """Letras com atraso próprio, agrupadas por palavra para a linha só quebrar entre palavras."""
    out, i, words = [], 0, KT.split(' ')
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
    kicker = ('<p class="wr-type" aria-label="' + KT + '" style="margin: 0; ' + DF + ' font-size: 32px; line-height: 1.5; color: #ffffff; text-shadow: 4px 4px 0 #3a3a3a; text-align: center; max-width: 1100px">'
              + kicker_words() + '</p>\n')
    art = (f'<img src="{p["cover"]}" alt="{e("Capa de " + p["title"])}" data-onload="featLoad" style="width: 100%; height: auto; display: block{px}">\n'
           if p['cover'] else f'<div style="aspect-ratio: 16 / 9; background: #161616"></div>\n')
    buttons = '<a class="wr-btn" href="#topo" data-act="open_' + feat + '" style="' + BTN + '; border: 4px solid #ffffff; background: #ffffff; color: #0b0b0b; box-shadow: 4px 4px 0 #4a4a4a">Ver detalhes</a>\n'
    if gh:
        buttons += f'<a class="wr-btn" href="{e(gh)}" style="{BTN}; border: 4px solid #8a8a8a; background: #0b0b0b; color: #ffffff">Ver no GitHub</a>\n'
    feat_html = (
        '<div class="dc-if" data-if="on0">\n'
        '<section class="wr-home" aria-label="Projeto em andamento" style="display: flex; flex-direction: column; align-items: center; gap: 28px; text-align: center">\n'
        '<div class="wr-feat-wrap" data-bbase="wr-feat-wrap" data-bclass="featCls" style="width: 100%; max-width: 720px; display: flex; flex-direction: column; align-items: center; gap: 44px">\n'
        '<div class="wr-stage">\n<div class="wr-tvbox">\n'
        '<a class="wr-link wr-feat-art wr-sh" href="#topo" data-act="open_' + feat + '" aria-label="Abrir ' + e(p['title']) + '" style="position: relative; display: block; width: 100%; line-height: 0; background: #000000">\n'
        + art + mos + '</a>\n</div>\n<div class="wr-kick">\n' + kicker + '</div>\n'
        '<button class="wr-start" type="button" data-act="startIntro"><span>&#9654; Pressione start</span><small>Clique para começar</small></button>\n</div>\n' +
        '<div class="wr-feat-info" style="display: flex; flex-direction: column; align-items: center; gap: 14px">\n'
        f'<span style="color: #a8a8a8; letter-spacing: 1px; text-transform: uppercase">{e(p["tag"])} · {e(p["status"])}</span>\n'
        f'<h1 style="margin: 0; {DF} font-size: 32px; line-height: 1.4; font-weight: 400; text-shadow: 4px 4px 0 #3a3a3a">{e(p["title"])}</h1>\n'
        f'<p style="margin: 0; color: #c4c4c4; max-width: 640px">{inline(p["feature_text"])}</p>\n'
        '<div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 16px; margin-top: 6px">\n' + buttons + '</div>\n'
        '</div>\n</div>\n</section>\n</div>\n')
    btns = '\n'.join(
        f'<button class="wr-btn wr-sh-s wr-cat" type="button" data-hover="hov" data-act="pick{n}" data-b-aria-expanded="pk{n}" style="min-height: 64px; padding: 12px; border: 4px solid #8a8a8a; background: #141414; color: #ffffff; {DF} font-size: 16px; line-height: 1.5; text-transform: uppercase; cursor: pointer">{e(t)}</button>'
        for n, (c, t) in enumerate(CATS, 1))
    nav = ('<div class="dc-if" data-if="on0">\n'
           f'<nav class="wr-nav" aria-label="Categorias" style="display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 32px">\n{btns}\n</nav>\n</div>\n')
    peeks = ''
    for n, (c, t) in enumerate(CATS, 1):
        ids = [k for k in order if posts[k]['cat'] == c]
        cards = '\n'.join(card(posts[i]) for i in ids[:3]) or '<p style="margin: 0; text-align: center; color: #8a8a8a">Nada por aqui ainda.</p>'
        peeks += ('<div class="dc-if" data-if="pk' + str(n) + '">\n'
                  f'<section class="wr-peek" aria-label="Últimos em {e(t)}" style="display: flex; flex-direction: column; gap: 24px">\n'
                  f'<h2 style="margin: 0; {DF} font-size: 16px; line-height: 1.5; font-weight: 400; text-transform: uppercase; text-align: center; color: #c4c4c4">Últimos em {e(t)}</h2>\n'
                  f'<div class="wr-grid" style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 36px">\n{cards}\n</div>\n'
                  '<button class="wr-btn" type="button" data-act="all' + str(n) + '" style="align-self: center; min-height: 48px; padding: 12px 20px; border: 4px solid #ffffff; background: #ffffff; color: #0b0b0b; ' + DF + f' font-size: 16px; line-height: 1.5; text-transform: uppercase; cursor: pointer; box-shadow: 4px 4px 0 #4a4a4a">Ver todos ({len(ids)})</button>\n'
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
    print(f'ok: {len(posts)} posts, destaque = {feat}, saída em {os.path.relpath(OUT, ROOT)}/')


if __name__ == '__main__':
    build()
