---
titulo: Godot 4 PSVita
categoria: ferramentas
grupo: Em andamento
data: 2026-06-05
tag: Engine · C++
status: 2D em GXM nativo · 3D experimental
resumo: Godot Engine 4.x portada para o PS Vita, com exportação direto do editor.
capa: capa.png
capa_estilo: logo
ficha:
  Base: Godot 4.8-dev7
  2D: GXM nativo
  3D: Experimental
  Troféus: Em desenvolvimento
links:
  Ver no GitHub: https://github.com/WolffsRoom/godot4-psvita
  Releases: https://github.com/WolffsRoom/godot4-psvita/releases
---

Runtime customizado do Godot 4.8-dev7 com renderização GXM nativa, mais um editor para Windows que exporta VPKs de PS Vita diretamente. Não é um release oficial do Godot.

## As três partes

- Runtime — Godot compilado para ARM como libgodot.so, com camada de sistema do Vita, renderers GXM, áudio, entrada e arquivos
- Loader — eboot.bin que carrega e inicia a libgodot.so, mostra a animação de carregamento e gerencia CapUnlocker, logs e caminhos de dados
- Editor Windows — PS Vita como plataforma de exportação embutida

## Destaques

- Godot4Vita.exe portátil: exporta sem addon, Python, WSL ou VitaSDK
- Transforma projetos compatíveis em VPK instalável, com LiveArea e pasta de dados separada
- Seleção de template de LiveArea com prévia
