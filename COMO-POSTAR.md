# Como cadastrar e editar posts

Há dois jeitos. Os dois publicam o site sozinhos em cerca de 1 minuto.

## 1. Pelo formulário (mais fácil, funciona até no celular)

1. Abra **Issues → New issue → Novo post**:
   https://github.com/WolffsRoom/WolffsRoomSite/issues/new?template=novo-post.yml
2. Preencha os campos. Para imagens, **arraste os arquivos** para dentro dos campos *Capa* e *Capturas de tela*.
3. Clique em **Submit new issue**.

A automação cria a pasta do post, publica o site e fecha a issue com o link do post. Se algo estiver errado (por exemplo, faltou a capa), ela comenta na issue explicando o problema e a issue continua aberta.

Só issues abertas por você (dono ou colaboradores do repositório) viram post.

## 2. Pelo arquivo (para editar posts ou criar com mais controle)

Cada post é uma pasta em `content/posts/` com um `post.md` e as imagens ao lado:

```
content/posts/pizza/
├── post.md
├── capa.png
├── captura-1.jpg
└── captura-2.jpg
```

O nome da pasta é o endereço do post (`…/WolffsRoomSite/#pizza`). Use só letras minúsculas, números e hífen.

Para editar pelo navegador: abra o `post.md` no GitHub, clique no lápis, altere e clique em **Commit changes**. Para trocar ou adicionar imagens: **Add file → Upload files** dentro da pasta do post.

### Modelo de `post.md`

```markdown
---
titulo: Nome do projeto
categoria: ports          # ports | ferramentas | traducoes | reviews
grupo: Em andamento       # Em andamento | Finalizado | Próximos | Outras equipes
data: 2026-11-13          # define a ordem: o mais recente aparece primeiro
tag: Port · PS Vita       # linha pequena acima do título no card
status: Em andamento      # texto de status no card
resumo: Uma frase curta para o card.
progresso: 60             # opcional, 0 a 100
capa: capa.png            # arquivo na mesma pasta
capturas:                 # opcional
  - captura-1.jpg
  - captura-2.jpg
video: https://www.youtube.com/watch?v=XXXXXXXXXXX   # opcional
video_legenda: Trailer    # opcional
barras:                   # opcional
  Scripts: 90
  Gráficos: 40
ficha:                    # opcional
  Versão do jogo: PCSE00000
  Senha do arquivo: wolffsroom
links:                    # opcional; o primeiro vira o botão principal
  Ver no GitHub: https://github.com/WolffsRoom/...
  Google Drive: https://drive.google.com/...
---

Primeiro parágrafo: apresentação do projeto.

## Destaques
- Item
- Item com [link](https://exemplo.com)

## Instalação
- Passo 1
- Passo 2
```

### Versão em inglês (`post.en.md`)

O site abre em **inglês** (o visitante pode trocar para português no botão EN/PT, acima do botão de som). Para cada post, um arquivo `post.en.md` na mesma pasta traz os textos em inglês. Tudo nele é opcional: o que faltar aparece em português.

```markdown
---
titulo: Pizza Tower — SAGE 2019 Demo   # só se mudar
tag: Port · PS Vita
status: In progress
resumo: Port of the SAGE 2019 demo to PS Vita.
chamada: Text for the home page highlight.
video_legenda: Trailer
titulo_barras: Progress
barras:                 # mesmos números, nomes em inglês
  Scripts: 90
  Graphics: 40
ficha:
  Game version: PCSE00000
links:
  View on GitHub: https://github.com/WolffsRoom/...
---

First paragraph: the project in English.

## Highlights
- Item
```

Pelo formulário, preencha os campos "(inglês)" e o `post.en.md` é criado junto.

### Campos extras

| Campo | Para que serve |
|---|---|
| `destaque: true` | Coloca o post no destaque da página inicial. Deixe em só um post. |
| `chamada:` | Texto do destaque na página inicial (se faltar, usa o `resumo`). |
| `pixelado: true` | Mantém a capa nítida, sem suavização (bom para pixel art). |
| `capa_estilo: logo` | Mostra a capa inteira centralizada em fundo preto (para logos). |
| `titulo_barras:` | Título da caixa de barras (padrão: "Progresso"). |
| `barras` com texto | `Nota final: 89 (192/216)` mostra a barra em 89% com o texto "192/216". |

## Pré-visualizar no computador

```powershell
pip install pyyaml pillow
python tools/build.py
python -m http.server -d _site
```

Depois abra http://localhost:8000. Se algum `post.md` tiver erro, o `build.py` diz qual arquivo e o que corrigir.
