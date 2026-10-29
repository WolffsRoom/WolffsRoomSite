# Wolff’s Room

Site editorial de Mods, Ports, Traduções e Reviews para PlayStation Vita, com código e conteúdo versionados neste repositório.

## Identidade e temas

A interface usa cinza, branco e preto, com o lobo e a marca em pixel art originais do WordPress. O botão de tema alterna entre modo claro e escuro, salva a escolha neste navegador e, antes de uma escolha manual, acompanha a preferência do sistema. Os ícones de interface são do Lucide, com os avisos de licença em `THIRD_PARTY_NOTICES.md`. As imagens dos jogos preservam suas cores.

## Publicação

Endereço previsto do GitHub Pages: **https://wolffsroom.github.io/WolffsRoomSite/**

O Pages precisa estar configurado em **Settings → Pages → Source → GitHub Actions**. O workflow `.github/workflows/pages.yml` testa, gera e publica o site. A confirmação da publicação aparece no histórico de Actions e no ambiente `github-pages`; um endereço previsto não comprova que a implantação já terminou.

## Criar um post sem editar código

1. Abra `/editor/` no site.
2. Preencha título, categoria, resumo, texto e os detalhes do projeto.
3. Use **Ver prévia** para revisar a página. A barra de formatação insere títulos, listas, destaques, links e imagens.
4. Clique em **Publicar no GitHub**. Uma solicitação é preparada na sua conta. Revise e confirme com **Submit new issue**.
5. A automação confere se o autor e a pessoa que enviou são `WolffsRoom`, salva o post em `content/posts/` e publica o site.

Para textos longos, o editor copia a solicitação para a área de transferência e abre o formulário; cole na descrição antes de confirmar. O editor avisa quando essa etapa for necessária. Não é preciso colocar um token no site.

Também há um formulário em **Issues → New issue → Publicar uma postagem**, como alternativa ao editor. Ele aceita as mesmas quatro categorias. Imagens podem ser anexadas no GitHub, que fornece um link HTTPS. Use esse link como capa ou insira a imagem no texto.

## Editar ou retirar uma publicação

Abra o artigo e clique em **Editar esta publicação**. Mantenha o mesmo endereço do post para atualizar o registro existente. O histórico anterior fica preservado no Git. Desmarque **Publicar no site** e confirme uma nova solicitação para retirar o artigo da listagem e da geração de páginas. Editar uma solicitação anterior de publicação também atualiza seu post.

## Rascunhos e privacidade

Rascunhos do editor são salvos somente no navegador atual; use **Exportar cópia** como backup. O repositório e as Issues são públicos: não guarde informações privadas neles. A opção de rascunho do formulário do GitHub remove o post do site, mas não torna seu texto privado no repositório.

## Desenvolvimento local

Requer Node.js 22 ou superior. Não há dependências para instalar.

```sh
npm test
npm run build
npm run dev
```

Abra a URL impressa, normalmente `http://127.0.0.1:4173/WolffsRoomSite/`. Após alterações, execute o build novamente. O servidor é somente uma prévia local; a hospedagem final é o GitHub Pages.

## Estrutura

- `config/site.json`: marca, endereço, caminho-base, conta autorizada e links.
- `content/posts/*.json`: cada publicação é um arquivo independente.
- `src/templates.mjs`: páginas e componentes de apresentação reutilizáveis.
- `src/app.mjs`: navegação, busca, filtros, editor, prévia e rascunhos.
- `src/model.mjs`: validação compartilhada e formato de publicação.
- `src/styles.css`: identidade editorial, tema e layout responsivo.
- `scripts/build.mjs`: gera HTML de cada artigo/categoria, feed RSS, sitemap e arquivos públicos.
- `scripts/publish-issue.mjs`: valida as publicações enviadas pelo proprietário.
- `.github/workflows/pages.yml`: testes, atualização de conteúdo e deploy.
- `tests/site.test.mjs`: testes de conteúdo, segurança, publicação e filtros.

## Conteúdo inicial

O site inclui resumos editoriais de publicações existentes do [Wolff’s Room no WordPress](https://wolffsroom.wordpress.com/), com datas, imagens e links para os artigos originais. O corpo completo do acervo não foi migrado. Os cards de Ports apontam para repositórios públicos da própria conta, e não afirmam que uma release jogável tenha sido verificada. As datas desses registros são datas de catalogação editorial, não datas de lançamento dos jogos.

As imagens permanecem hospedadas nas fontes originais. O site não inclui jogos comerciais nem espelha os arquivos de download. Use o editor para substituir resumos por textos de sua autoria e atualizar créditos, imagens e instruções.

## Comportamentos importantes

O conteúdo publicado é renderizado em HTML durante o build. A leitura e os links principais funcionam sem JavaScript; o editor e os filtros dinâmicos precisam dele. Datas futuras e posts despublicados são excluídos do site. HTML no texto é exibido como texto, sem execução. Links e imagens só aceitam HTTPS. Slugs são validados para impedir escrita fora da pasta de conteúdo. Eventos de pessoas externas são ignorados, mesmo quando imitam uma publicação.

O Pages é estático: a confirmação de publicação acontece no GitHub, e não por uma API secreta no navegador. Depois de enviar, consulte **Actions** para acompanhar o resultado. GitHub Actions pode levar alguns minutos para atualizar o site.
