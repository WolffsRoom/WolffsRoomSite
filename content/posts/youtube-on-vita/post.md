---
titulo: YouTube on Vita — Alpha
categoria: ports
grupo: Em andamento
data: 2026-11-17 23:20
tag: Aplicativo · PS Vita
status: Alpha experimental
resumo: O YouTube on TV real, executado no PS Vita por meio de um port experimental do Google Cobalt e Starboard.
chamada: O verdadeiro YouTube on TV no PlayStation Vita — um port experimental do motor Cobalt, não uma interface imitada.
capa: capa.png
capturas:
  - navegacao.gif
ficha:
  Versão: Alpha v0.22 (experimental)
  Motor: Google Cobalt Evergreen 5.50.2
  Plataforma: Starboard 15 / VitaGL
  Controles: Botões e touchscreen
  Situação: Em testes
fontes:
  Código e desenvolvimento: https://github.com/WolffsRoom/YouTubeOnVita
---
**YouTube on Vita** é um cliente não oficial para PlayStation Vita que busca executar a experiência verdadeira do **YouTube on TV**, semelhante à utilizada em Smart TVs e consoles, sem recriar sua interface manualmente.

O projeto adapta o runtime **Google Cobalt Evergreen** e a camada **Starboard** aos recursos do PS Vita: gráficos via VitaGL/GXM, memória, rede, entrada, áudio e decodificação de mídia.

## O que já funciona nos testes

- A interface real do YouTube on TV é carregada e renderizada no Vita3K.
- Navegação por D-pad e botões, com entrada touchscreen experimental.
- Carregamento de páginas, miniaturas, navegação lateral e vídeos do serviço.
- Reprodução experimental de H.264 e AAC usando decodificadores nativos do Vita.
- Ajustes de cache de shaders, inicialização, memória e áudio.
- Um vídeo de teste foi reproduzido no Vita3K com avanço do tempo de mídia e fim de reprodução detectado.

## Alpha e limitações

**Ainda é uma versão experimental.** O desempenho no PS Vita físico, o áudio sob carga, a estabilidade e a persistência do login ainda precisam de validação e melhorias. Login por QR code e demais funcionalidades de conta não devem ser considerados totalmente verificados. Alguns formatos, resoluções, transmissões e conteúdos protegidos não são suportados.

O projeto não é oficial nem possui qualquer associação com Google, YouTube ou Sony.

## Distribuição

As versões alpha instaláveis serão disponibilizadas **exclusivamente pelo aplicativo Wolff's Store para PS Vita**, quando liberadas. **O VPK não será oferecido como download neste site nem nas releases do GitHub.**

Acompanhe a evolução pelo [repositório YouTubeOnVita](https://github.com/WolffsRoom/YouTubeOnVita).
