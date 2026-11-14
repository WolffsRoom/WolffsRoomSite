---
titulo: DeltaruneVita
categoria: ports
grupo: Em andamento
data: 2026-11-10
tag: Port · GameMaker · PS Vita
status: 81% · Jogável
resumo: Deltarune, capítulos 1 a 5, no PS Vita.
progresso: 81
capa: capa.jpg
pixelado: true
trofeus: true
capturas:
  - captura-1.png
  - captura-2.png
  - captura-3.png
  - captura-4.png
  - captura-5.png
  - captura-6.png
  - captura-7.png
  - captura-8.png
video_arquivo: trailer-vita-v2.mp4
video_legenda: Trailer do DeltaruneVita
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
  Troféus: Sim (NoTrpDrm)
links:
  Baixar VPK (v0.81): https://github.com/WolffsRoom/DeltaruneVita/releases/download/v0.81/Deltarune-v0.81.vpk
fontes:
  Ver no GitHub (PS Vita): https://wolffsroom.github.io/WolffsStore/WolffsRoom/DeltaruneVita/
  Releases (PS Vita): https://wolffsroom.github.io/WolffsStore/WolffsRoom/DeltaruneVita/releases/
downloads:
  - tipo: vpk
    nome: DeltaruneVita v0.81 (VPK)
    url: https://github.com/WolffsRoom/DeltaruneVita/releases/download/v0.81/Deltarune-v0.81.vpk
    versao: "0.81"
    titleid: DELT00001
    precisa_dados: true
    instrucoes: https://wolffsroom.github.io/WolffsStore/WolffsRoom/DeltaruneVita/
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
- CapUnlocker, para melhorar o desempenho
- NoTrpDrm, para os troféus (opcional)

## Instalação

- Gere os dados do Vita com um dos patchers
- Copie a pasta deltarune gerada para ux0:data/
- Instale o VPK no Vita
