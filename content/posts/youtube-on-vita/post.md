---
titulo: YouTube on Vita
categoria: ferramentas
subcategoria: apps
grupo: Em andamento
data: 2026-11-17 23:20
atualizado_em: '2026-11-22'
tag: YouTube on TV · Cobalt · PS Vita
status: v0.65 · Release
novidade: Release
versao: v0.65
resumo: 'YouTube on Vita v0.65: novos controles, Shorts verticais, Aspect Ratio, sons de UI e melhorias em reprodução
  e downloads.'
chamada: '**YouTube on Vita — *Cliente não oficial para PS Vita***


  A experiência real do YouTube on TV, agora na **Release v0.65**: Shorts, novos controles, Aspect Ratio e interface
  aprimorada.


  Full e Lite disponíveis.'
capa: release-v065.png
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
  Version: v0.65 · Release
  Platform: PlayStation Vita / Vita3K
  Engine: Cobalt / Starboard 15 / VitaGL
  Video: H.264 / AAC · até 720p; Full HD experimental
  Controls: Botões, analógicos, touch e microfone
  Builds: Full (RAM estendida) / Lite (menor uso de RAM)
  Title IDs: YTVCB0001 (Full) / YTVCB0002 (Lite)
  Requirement: kubridge v0.3.1 ou superior
links:
  YouTube Full - Download recomendado: https://github.com/WolffsRoom/YouTubeOnVita/releases/download/v0.65/YouTube.vpk
  YouTube Lite - Menos RAM: https://github.com/WolffsRoom/YouTubeOnVita/releases/download/v0.65/YouTube-Lite.vpk
  Release v0.65 no GitHub: https://github.com/WolffsRoom/YouTubeOnVita/releases/tag/v0.65
fontes:
  Repositório e README: https://github.com/WolffsRoom/YouTubeOnVita
downloads:
- tipo: vpk
  nome: YouTube Full (normal) - Recomendado
  url: https://github.com/WolffsRoom/YouTubeOnVita/releases/download/v0.65/YouTube.vpk
  arquivo: YouTube.vpk
  versao: '0.65'
  titleid: YTVCB0001
  tamanho: 22923055
  instrucoes: https://github.com/WolffsRoom/YouTubeOnVita#download
- tipo: vpk
  nome: YouTube Lite - Menor uso de RAM
  url: https://github.com/WolffsRoom/YouTubeOnVita/releases/download/v0.65/YouTube-Lite.vpk
  arquivo: YouTube-Lite.vpk
  versao: '0.65'
  titleid: YTVCB0002
  tamanho: 22923400
  instrucoes: https://github.com/WolffsRoom/YouTubeOnVita#download
---

E aí, pessoal! Wolff aqui.

A **release v0.65 do YouTube on Vita** chegou! Desde a primeira versão pública, a experiência original do **YouTube on TV** no PlayStation Vita ganhou novos controles, recursos e otimizações.

## Novidades da v0.65

- **Shorts e Vertical Mode:** reprodução de vídeos verticais com navegação por gestos ao girar o Vita. Inverted screen ainda é experimental.
- **Player:** H.264 até 720p, modos Aspect Ratio (Original, Zoom e Stretch), filtros Bilinear/Nearest e melhor compatibilidade com resoluções não convencionais.
- **Controles:** navegação pelo analógico esquerdo, ajuste de volume/brilho pelo direito e Player settings pelo Triângulo.
- **Interface:** nova animação de inicialização a 60 FPS, sons nativos com volume ajustável e melhorias no Add-ons.
- **Sleep Timer:** opção de 5 minutos, contador final de 60 segundos e alertas sonoros.
- **Downloads:** melhorias de MP3/MP4, conversão do áudio durante o download, lista paginada e aviso quando a qualidade selecionada não está disponível.
- **Estabilidade:** otimizações de memória, renderização, reconexão de rede e preservação dos logs da sessão anterior.

## Qual versão baixar?

Instale pelo **VitaShell**. As edições Full e Lite possuem ícones próprios na LiveArea e podem coexistir.

- **YouTube Full — recomendado:** RAM estendida para favorecer a reprodução de vídeos.
- **YouTube Lite — menos RAM:** menor consumo de memória, útil para manter outros aplicativos em segundo plano.

**Requisito:** instale o [kubridge v0.3.1 ou superior](https://github.com/bythos14/kubridge/releases/latest) em `*KERNEL` e reinicie o console. Versões antigas podem causar falhas após a animação de abertura. Você não precisa apagar as configurações ou os dados de login para atualizar.

## Limitações conhecidas

**Full HD, Inverted screen e alguns controles dos Shorts ainda são experimentais.** O AdBlock é parcial, downloads MP4 podem apresentar resolução inferior à solicitada e travamentos ocasionais ao trocar vídeos continuam em investigação. O atalho para comentários pelo Quadrado ainda está pendente.

Se encontrar problemas, compartilhe os logs `cobalt_boot_prev.log`, `starboard15_prev.log` e, quando disponível, o dump `.psp2dmp`.

Para instruções técnicas e mais detalhes, consulte o [README do YouTube on Vita](https://github.com/WolffsRoom/YouTubeOnVita#readme).

**Vita means life!**
