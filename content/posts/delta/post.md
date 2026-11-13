---
titulo: DeltaruneVita
categoria: ports
grupo: Em andamento
data: 2026-11-10
tag: Port · C
status: 81% · Jogável
resumo: Deltarune, capítulos 1 a 5, no PS Vita.
progresso: 81
capa: capa.jpg
pixelado: true
titulo_barras: Revisão por capítulo
barras:
  Capítulo 1: 100
  Capítulo 2: 100
  Capítulo 3: 95
  Capítulo 4: 85
  Capítulo 5: 80
ficha:
  Status: Jogável
  Fonte: Steam v0.0.253
  Runtime: Butterscotch + VitaGL + OpenAL
  Build: Deltarune-v0.81.vpk
links:
  Ver no GitHub: https://github.com/WolffsRoom/DeltaruneVita
  Releases: https://github.com/WolffsRoom/DeltaruneVita/releases
---

Port não oficial de DELTARUNE, capítulos 1 a 5. Executa os dados oficiais do GameMaker (Windows/Steam) em uma implementação do Butterscotch voltada ao Vita, com VitaGL nos gráficos e OpenAL no áudio. O repositório e os releases não incluem os dados comerciais do jogo.

## Estado dos capítulos

- Capítulo 1 — tudo funciona
- Capítulo 2 — pequenas quedas de desempenho em algumas salas
- Capítulo 3 — alguns minigames engasgam no primeiro carregamento
- Capítulo 4 — algumas salas ainda precisam de otimização
- Capítulo 5 — otimização incompleta; conclusão total ainda não verificada

## Destaques

- Controles do Vita e toque opcional
- Gráficos e áudio configuráveis
- Bordas de console
- Suporte a idiomas e mods
- Troféus
- Reprodução nativa de vídeo
- Patchers que geram os dados do Vita a partir da sua cópia do jogo

## Requisitos

- PS Vita desbloqueado
- kubridge (kubridge.skprx)
- FdFix (fd_fix.skprx), exceto se você usa rePatch
- libshacccg.suprx instalado no Vita
- Instalação oficial e sem modificações de DELTARUNE na Steam (v0.0.253)

## Instalação

- Gere os dados do Vita com um dos patchers
- Copie a pasta deltarune gerada para ux0:data/
- Instale o VPK no Vita
