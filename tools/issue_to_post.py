#!/usr/bin/env python3
"""Converte uma issue do formulário "Novo post" em content/posts/<slug>/post.md.

Lê o corpo da issue da variável de ambiente ISSUE_BODY (ou de um arquivo
passado como argumento). Imprime o slug criado. Em caso de erro, escreve a
mensagem em _issue_error.txt e sai com código 1.
"""
import datetime
import io
import os
import re
import sys
import unicodedata
import urllib.request

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS = os.path.join(ROOT, 'content', 'posts')
CATS = {'ports': 'ports', 'ferramentas': 'ferramentas', 'traduções': 'traducoes', 'traducoes': 'traducoes', 'reviews': 'reviews'}
GROUPS = ['Em andamento', 'Finalizado', 'Próximos', 'Outras equipes']
FIELDS = {
    'Título': 'titulo', 'Categoria': 'categoria', 'Grupo': 'grupo', 'Etiqueta': 'tag', 'Status': 'status',
    'Progresso (%)': 'progresso', 'Resumo': 'resumo', 'Texto do post': 'texto', 'Capa': 'capa',
    'Capturas de tela': 'capturas', 'Vídeo (opcional)': 'video', 'Links (opcional)': 'links',
    'Ficha (opcional)': 'ficha', 'Barras de progresso (opcional)': 'barras', 'Destaque': 'destaque',
}
MAX_W = 1600


class Fail(Exception):
    pass


def parse_issue(body):
    data, cur = {}, None
    for line in body.replace('\r\n', '\n').split('\n'):
        m = re.match(r'^###\s+(.+?)\s*$', line)
        if m and m.group(1) in FIELDS:
            cur = FIELDS[m.group(1)]
            data[cur] = []
        elif cur:
            data[cur].append(line)
    out = {}
    for k, lines in data.items():
        v = '\n'.join(lines).strip()
        out[k] = '' if v == '_No response_' else v
    return out


def slugify(text):
    t = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode().lower()
    t = re.sub(r'[^a-z0-9]+', '-', t).strip('-')
    return (t[:48].rstrip('-')) or 'post'


def image_urls(text):
    urls = re.findall(r'!\[[^\]]*\]\((https?://[^)\s]+)\)', text or '')
    urls += re.findall(r'<img[^>]+src="(https?://[^"]+)"', text or '')
    seen, res = set(), []
    for u in urls:
        if u not in seen:
            seen.add(u)
            res.append(u)
    return res


def download(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'wolffsroom-site'})
    token = os.environ.get('GITHUB_TOKEN')
    try:
        return urllib.request.urlopen(req, timeout=60).read()
    except Exception:
        if not token:
            raise
        req.add_header('Authorization', 'Bearer ' + token)
        return urllib.request.urlopen(req, timeout=60).read()


def save_image(url, folder, base):
    from PIL import Image
    try:
        raw = download(url)
        im = Image.open(io.BytesIO(raw))
        im.load()
    except Exception as ex:
        raise Fail(f'não consegui baixar ou abrir a imagem {url} ({ex})')
    fmt = (im.format or '').upper()
    if im.width > MAX_W:
        im = im.resize((MAX_W, round(im.height * MAX_W / im.width)), Image.LANCZOS)
    if fmt == 'PNG' or im.mode in ('P', 'RGBA', 'LA'):
        name = base + '.png'
        im.save(os.path.join(folder, name), optimize=True)
    else:
        name = base + '.jpg'
        im.convert('RGB').save(os.path.join(folder, name), quality=88, optimize=True)
    return name


def pairs(text, numeric=False):
    res = {}
    for line in (text or '').splitlines():
        line = line.strip().lstrip('-').strip()
        if not line:
            continue
        if '|' not in line:
            raise Fail(f'a linha "{line}" precisa estar no formato "Nome | valor"')
        k, v = [x.strip() for x in line.split('|', 1)]
        if numeric:
            mm = re.match(r'^(\d{1,3})\s*%?$', v)
            if not mm:
                raise Fail(f'barra "{k}": use só um número de 0 a 100')
            v = min(100, int(mm.group(1)))
        res[k] = v
    return res


def clear_feature():
    for slug in os.listdir(POSTS):
        path = os.path.join(POSTS, slug, 'post.md')
        if not os.path.isfile(path):
            continue
        txt = open(path, encoding='utf-8').read()
        new = re.sub(r'^(destaque: true|chamada: .*)\n', '', txt, flags=re.M)
        if new != txt:
            open(path, 'w', encoding='utf-8').write(new)


def main():
    body = open(sys.argv[1], encoding='utf-8').read() if len(sys.argv) > 1 else os.environ.get('ISSUE_BODY', '')
    f = parse_issue(body)
    title = f.get('titulo', '').strip()
    if not title:
        raise Fail('o título está vazio')
    cat = CATS.get(f.get('categoria', '').strip().lower())
    if not cat:
        raise Fail('categoria inválida')
    group = f.get('grupo', '').strip()
    if group not in GROUPS:
        raise Fail('grupo inválido')
    if not f.get('resumo'):
        raise Fail('o resumo está vazio')
    covers = image_urls(f.get('capa'))
    if not covers:
        raise Fail('arraste uma imagem para o campo Capa')

    slug = base = slugify(title)
    n = 2
    while os.path.exists(os.path.join(POSTS, slug)):
        slug = f'{base}-{n}'
        n += 1
    folder = os.path.join(POSTS, slug)
    os.makedirs(folder)

    fm = {'titulo': title, 'categoria': cat, 'grupo': group, 'data': datetime.date.today()}
    if f.get('tag'):
        fm['tag'] = f['tag']
    fm['status'] = f.get('status') or group
    fm['resumo'] = f['resumo']
    prog = (f.get('progresso') or '').strip().rstrip('%')
    if prog:
        if not prog.isdigit():
            raise Fail('progresso: use só um número de 0 a 100')
        fm['progresso'] = min(100, int(prog))
    if '[x]' in (f.get('destaque') or '').lower():
        clear_feature()
        fm['destaque'] = True
        fm['chamada'] = f['resumo']
    fm['capa'] = save_image(covers[0], folder, 'capa')
    shots = [save_image(u, folder, f'captura-{i}') for i, u in enumerate(image_urls(f.get('capturas')), 1)]
    if shots:
        fm['capturas'] = shots
    if f.get('video'):
        if not re.search(r'(youtube\.com|youtu\.be)/', f['video']):
            raise Fail('vídeo: use um link do YouTube')
        fm['video'] = f['video'].strip()
    bars = pairs(f.get('barras'), numeric=True)
    if bars:
        fm['barras'] = bars
    ficha = pairs(f.get('ficha'))
    if ficha:
        fm['ficha'] = ficha
    links = pairs(f.get('links'))
    if links:
        fm['links'] = links

    text = (f.get('texto') or '').strip()
    # imagens coladas no texto viram capturas extras
    for i, u in enumerate(image_urls(text), len(shots) + 1):
        fm.setdefault('capturas', []).append(save_image(u, folder, f'captura-{i}'))
    text = re.sub(r'!\[[^\]]*\]\([^)]+\)|<img[^>]*>', '', text).strip()

    head = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True, width=1000)
    open(os.path.join(folder, 'post.md'), 'w', encoding='utf-8').write('---\n' + head + '---\n\n' + text + '\n')
    print(slug)


if __name__ == '__main__':
    try:
        main()
    except Fail as ex:
        open(os.path.join(ROOT, '_issue_error.txt'), 'w', encoding='utf-8').write(str(ex))
        print('erro:', ex, file=sys.stderr)
        sys.exit(1)
