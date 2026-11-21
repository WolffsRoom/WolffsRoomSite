---
titulo: YouTube on Vita
categoria: ferramentas
subcategoria: apps
grupo: Em andamento
data: '2026-11-17 23:20'
atualizado_em: '2026-11-20 18:55'
tag: YouTube on TV · Cobalt · PS Vita
status: v0.58 · First Release
novidade: Release
versao: v0.58
resumo: YouTube on Vita — cliente não oficial do YouTube para PS Vita. A experiência real do YouTube on TV através do Cobalt. Disponível nas versões Full e Lite.
chamada: |-
  **YouTube on Vita — *Cliente não oficial do YouTube para PS Vita***

  A experiência real do YouTube on TV, trazida ao PlayStation Vita através do Cobalt.

  Disponível em duas versões: Full e Lite.
capa: capa.png
capturas:
  - captura-1.png
  - captura-2.png
  - captura-3.png
  - captura-4.png
  - captura-5.png
  - captura-6.png
  - captura-7.png
  - addons-home.png
  - addons-player.png
  - addons-download.png
  - addons-settings.png
  - addons-display.png
ficha:
  Version: v0.58 · First Release
  Platform: PlayStation Vita / Vita3K
  Engine: Cobalt / Starboard 15 / VitaGL
  Video: H.264 / AAC · até 720p
  Controls: Botões, toque e microfone nativo
  Builds: Full (RAM estendida) / Lite (menor uso de RAM)
  Title IDs: YTVCB0001 (Full) / YTVCB0002 (Lite)
links:
  YouTube Full - Download recomendado: https://github.com/WolffsRoom/YouTubeOnVita/releases/download/v0.58/YouTube.vpk
  YouTube Lite - Menos RAM: https://github.com/WolffsRoom/YouTubeOnVita/releases/download/v0.58/YouTube-Lite.vpk
  Release v0.58 no GitHub: https://github.com/WolffsRoom/YouTubeOnVita/releases/tag/v0.58
fontes:
  Repositório e README: https://github.com/WolffsRoom/YouTubeOnVita
downloads:
  - tipo: vpk
    nome: YouTube Full (normal) - Recomendado
    url: https://github.com/WolffsRoom/YouTubeOnVita/releases/download/v0.58/YouTube.vpk
    arquivo: YouTube.vpk
    versao: '0.58'
    titleid: YTVCB0001
    tamanho: 21954021
    instrucoes: https://github.com/WolffsRoom/YouTubeOnVita#download
  - tipo: vpk
    nome: YouTube Lite - Menor uso de RAM
    url: https://github.com/WolffsRoom/YouTubeOnVita/releases/download/v0.58/YouTube-Lite.vpk
    arquivo: YouTube-Lite.vpk
    versao: '0.58'
    titleid: YTVCB0002
    tamanho: 21954225
    instrucoes: https://github.com/WolffsRoom/YouTubeOnVita#download
---

E aí, pessoal! Wolff aqui.

O **YouTube on Vita v0.58** chegou à sua **primeira versão pública**! O projeto traz a interface original do **YouTube on TV** para o PlayStation Vita, utilizando Cobalt e integração com os recursos nativos do console.

## O que oferece

- **YouTube de verdade:** navegação, pesquisa, login e player da interface de TV.
- **Controles nativos:** botões físicos, touchscreen e suporte ao microfone para recursos de voz compatíveis.
- **Reprodução de vídeo:** H.264/AAC, até 720p e suporte a vídeos de até 60 FPS quando disponíveis e compatíveis.
- **Add-ons:** capturas de tela, temporizador, tela preta ou escurecida, ajustes de desempenho e sons de navegação.
- **Downloads:** vídeos em MP4 e músicas em MP3, com capas quadradas nos novos arquivos de áudio.
- **Sessão protegida:** comunicação HTTPS e armazenamento local criptografado dos dados de sessão.

## Cobalt e desempenho

**Sobre o FPS da interface:** o Cobalt evita redesenhar telas paradas desnecessariamente. Por isso, contadores de FPS podem indicar valores baixos nos menus, mesmo sem lentidão perceptível. Esse comportamento também ajuda a economizar energia.

A reprodução também foi testada com o Vita configurado a **222 MHz de CPU / 111 MHz de GPU**, com resultado satisfatório no conteúdo testado.

## Qual versão baixar?

As duas versões possuem ícones próprios na LiveArea e podem ser instaladas pelo **VitaShell**. Nenhum PC ou servidor auxiliar é necessário para usar o YouTube.

- **YouTube Full — recomendado:** o YouTube.vpk utiliza RAM estendida para favorecer a reprodução de vídeos.
- **YouTube Lite — menos RAM:** o YouTube-Lite.vpk utiliza o perfil de memória normal, mais adequado para manter outros aplicativos abertos em segundo plano.

## Limitações conhecidas

O **AdBlock é parcial** e não bloqueia todos os anúncios do YouTube. Alguns vídeos podem ter restrições de formato ou conteúdo. Travamentos ocasionais ao trocar vídeos em HD, especialmente durante downloads, continuam em investigação.

Para instruções de compilação, detalhes sobre o login e mais imagens, acesse o [README do projeto](https://github.com/WolffsRoom/YouTubeOnVita).

**Vita means life!**
