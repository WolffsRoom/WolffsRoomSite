# Wolff's Room

Site de projetos do Wolff's Room: ports, ferramentas, traduções e reviews para PlayStation Vita.

Site publicado: https://wolffsroom.github.io/WolffsRoomSite/

**Novo post:** [abrir o formulário](https://github.com/WolffsRoom/WolffsRoomSite/issues/new?template=novo-post.yml) · guia completo em [COMO-POSTAR.md](COMO-POSTAR.md)

## Estrutura

- `content/posts/<slug>/` — um post por pasta: `post.md` (dados e texto) e as imagens.
- `assets/` — elementos gráficos do site (texturas, halos, ícone da pata).
- `tools/build.py` — gera o site em `_site/` a partir dos posts.
- `tools/template.html` — layout, estilos, sons e animações da página.
- `tools/issue_to_post.py` — transforma uma issue do formulário em post.
- `.github/workflows/pages.yml` — gera e publica o site a cada push na `main`.
- `.github/workflows/novo-post.yml` — cria o post quando a issue "Novo post" é aberta.

Os jogos, marcas e artes pertencem aos seus respectivos donos. Ports e traduções são projetos de fã, não oficiais.
