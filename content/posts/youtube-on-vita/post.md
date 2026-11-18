---
titulo: 'Youtube - Unofficial client for PS Vita (alpha)'
categoria: ports
grupo: Em andamento
data: '2026-11-17 23:20'
atualizado_em: 2026-11-18
tag: Client não oficial · YouTube · PS Vita
status: Alpha v0.34 · Testes no Vita real
novidade: Update
versao: v0.34
resumo: Interface original do YouTube on TV no PS Vita, com login, toque e reprodução H.264/AAC em até 720p.
chamada: YouTube no PS Vita real, com a experiência Starboard 15, controle por toque e vídeo até 720p.
capa: capa.png
capturas:
  - captura-1.png
  - captura-2.png
  - captura-3.png
  - captura-4.png
  - captura-5.png
  - captura-6.png
  - captura-7.png
ficha:
  Version: Alpha v0.34 (experimental)
  Platform: Starboard 15 / VitaGL (renderizador GXM direto planejado)
  Controls: Botões e gestos na tela sensível ao toque
  Video: H.264 até 720p, até 60 fps
  Status: Em testes no hardware real
  Title ID: YTVCB0001
  Plugin recomendado: CapUnlocker (4 núcleos de CPU; opcional)
links:
  Wolff's Store (PS Vita): https://wolffsroom.github.io/WolffsRoomSite/
fontes:
  GitHub - YouTubeOnVita: https://github.com/WolffsRoom/YouTubeOnVita
downloads:
  - tipo: vpk
    nome: Youtube - Unofficial client for PS Vita (alpha) v0.34
    url: https://drive.google.com/file/d/1PCtp1lwV3l4IUajHxlI6wJBF7YDhIprf/view?usp=sharing
    arquivo: YouTubeVita_v0.34.vpk
    versao: '0.34'
    titleid: YTVCB0001
    aviso_plugin: CapUnlocker
    app_min: '1.0.3'
---

Cliente experimental não oficial do YouTube para PlayStation Vita, utilizando a **interface genuína YouTube on TV (Starboard 15)**. A versão alpha v0.34 já funciona no PS Vita real e no Vita3K, superando as limitações dos primeiros testes da v0.22.

## O que já funciona nos testes

- A interface genuína do YouTube on TV roda no PS Vita real e no Vita3K.
- Navegação fluida, renderizando em até 60 FPS no hardware.
- D-pad e botões físicos, além de gestos na tela: tocar para selecionar, deslizar para rolar e tocar com dois dedos para voltar.
- Reprodução por hardware de H.264/AAC de 240p a 720p, incluindo fluxos de 60 fps.
- Login e configurações persistem entre sessões.
- Controles do player: pausar/retomar e legendas.
- Utiliza os quatro núcleos da CPU quando o plugin CapUnlocker está instalado.

## Status alpha e limitações

**Esta é uma versão experimental, não estável.** Problemas conhecidos: sombras de texto sobre vídeos e miniaturas podem aparecer como caixas escuras, a visualização de letras em videoclipes musicais não reproduz, e ainda podem ocorrer travamentos ocasionais (em investigação). Não há suporte a 1080p, pois o decodificador de vídeo disponibilizado a aplicativos no Vita tem limite de 720p. Controles de velocidade, VP9/AV1 e conteúdos protegidos também não são suportados.

## Instalação

- Instale a alpha v0.34 **somente pelo download integrado da Wolff's Store**, disponibilizado para o PS Vita. O link do arquivo está no catálogo da loja.
- **CapUnlocker é recomendado, mas não obrigatório.** Com ele instalado e ativado no taiHEN, o aplicativo pode utilizar todos os quatro núcleos da CPU. A loja exibe esse aviso antes da instalação.
- Reinicie o console após configurar o plugin, se necessário.
- Não é necessário um PC ou servidor auxiliar para acessar a interface do app.

## Observações

O login via QR Code, a persistência da sessão e o áudio durante a reprodução já foram validados em testes no Vita real. O projeto permanece em fase alpha e pode apresentar instabilidade.

## Créditos

- Port para PS Vita: Wolff's Room
- Interface: YouTube on TV / Starboard 15 (Cobalt)
- Renderização: VitaGL; backend GXM direto planejado
