---
titulo: Godot 4 Vita — Release v0.3
categoria: ferramentas
grupo: Em andamento
data: 2026-11-13 23:30
tag: Engine · C++
status: v0.3 lançada
resumo: Nova versão da Godot 4 para PS Vita, agora com editor para Windows, Linux e macOS.
capa: capa.png
ficha:
  Versão: v0.3
  Editor: Windows, Linux e macOS
  Base: Godot 4.8-dev7
  Showcase: VPK para PS Vita
  Requisitos: HENkaku/Ensō e kubridge
links:
  Baixar Showcase (VPK): https://github.com/WolffsRoom/godot4-psvita/releases/download/v0.3/Godot4Vita-v0.3-Showcase.vpk
fontes:
  Release v0.3 no GitHub: https://github.com/WolffsRoom/godot4-psvita/releases/tag/v0.3
  Ver o projeto: https://github.com/WolffsRoom/godot4-psvita
downloads:
  - tipo: vpk
    nome: Showcase v0.3
    url: https://github.com/WolffsRoom/godot4-psvita/releases/download/v0.3/Godot4Vita-v0.3-Showcase.vpk
    versao: "0.3"
    titleid: G4V030001
    instrucoes: https://github.com/WolffsRoom/godot4-psvita/releases/tag/v0.3
---

A v0.3 da Godot 4 Vita foca em memória, leitura de arquivos e no renderizador GXM nativo, e traz exportação para PS Vita também no Linux e no macOS.

## Aviso
**A Godot 4 Vita é um programa de computador.** O editor desta versão está disponível para **Windows, Linux e macOS**: você cria e exporta o jogo no PC e instala o VPK gerado no Vita. No Vita, o arquivo para testar é o [Showcase v0.3 (VPK)](https://github.com/WolffsRoom/godot4-psvita/releases/download/v0.3/Godot4Vita-v0.3-Showcase.vpk), uma demonstração com streaming do PCK, áudio e cenas 2D/3D.
A versão de macOS ainda não foi testada em um Mac de verdade, e a de Linux foi gerada no Ubuntu 22.04.

## Novidades
- Editores portáteis para Windows x64, Linux x86_64 e macOS universal (Intel e Apple Silicon), com a plataforma PS Vita embutida
- Pré-leitura do game.pck no quarto núcleo da CPU (com CapUnlocker), ligada por padrão
- Menos memória usada: texturas vão para a GPU ao carregar e a malha 3D foi para a CDRAM (cerca de 24 MiB livres em cenas 3D)
- Áudio no modo godot3 por padrão, com thread de mixagem própria
- Pasta de dados separada com game.pck e logs em ux0:data/<pasta>/logs/
- Correções no 3D em GXM (Sprite3D, AnimatedSprite3D, Label3D) e canvas 2D mais leve
- Compilador de shaders no console, experimental e desligado por padrão
- SelfTest VPK que roda todos os testes no aparelho em cerca de 6 minutos

## Instalação
- Baixe o editor do seu sistema na [página da release](https://github.com/WolffsRoom/godot4-psvita/releases/tag/v0.3), extraia a pasta inteira e mantenha a pasta vita/ ao lado do executável
- Em Project > Export, adicione o preset PS Vita e exporte o .vpk
- Instale o VPK com o VitaShell e copie a pasta de dados gerada para ux0:data/
- Projetos da v0.2 precisam ser exportados de novo com o editor da v0.3

## Limitações conhecidas
- 3D em GXM ainda é experimental
- Shaders e materiais de CanvasItem ainda não são renderizados
- Troféus são empacotados, mas ainda não desbloqueiam
