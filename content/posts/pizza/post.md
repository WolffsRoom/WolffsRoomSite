---
titulo: Pizza Tower - SAGE 2019 Demo
categoria: ports
grupo: Finalizado
data: 2026-11-14 17:59
tag: Port · GameMaker · PS Vita
status: v0.62 · Jogável
novidade: Update
versao: v0.62
resumo: "Atualização v0.62 do port de Pizza Tower SAGE 2019 Demo (v14), com texturas BC3 residentes e correções de controles."
chamada: Pizza Tower SAGE 2019 chegou ao PS Vita! Demo v14 jogável em 60 FPS com Pizzascape, Oregano Desert e Snick Challenge.
progresso: 95
capa: capa.png
pixelado: true
ficha:
  Status: Lançado · Jogável (95% de progresso)
  Versão: v0.62
  Demo original: Pizza Tower SAGE 2019 (v14)
  Criadores: Tour de Pizza
  Engine original: GameMaker
  Runtime: Butterscotch + VitaGL + OpenAL
  Title ID: PTSAGE001
  Dados: ux0:data/pizzatowersage/data.win
capturas:
  - captura-1.png
  - captura-2.png
  - captura-3.png
  - captura-4.png
  - captura-5.png
  - captura-6.png
video_arquivo: trailer-vita-v2.mp4
video_legenda: Trailer do port para PS Vita
links:
  Baixar VPK: https://github.com/WolffsRoom/PizzaTowerSage2019Vita/releases/download/v0.62/PizzaTowerSAGE-v0.62.vpk
  Baixar dados: https://drive.google.com/file/d/1CBof60EExpF4IrZMhyix6CvRicqSONRA/view?usp=sharing
fontes:
  GitHub: https://github.com/WolffsRoom/PizzaTowerSage2019Vita
  Demo oficial: https://pizzatowerguy.itch.io/pizza-tower-demo
  Pizza Tower Wiki: https://pizzatower.wiki/SAGE_2019_Demo
clock:
  CPU / GPU: 500 MHz / 222 MHz
  Desempenho: 60 FPS (conforme testes do projeto)
downloads:
  - tipo: vpk
    nome: Pizza Tower SAGE 2019 v0.62 (VPK)
    repo: WolffsRoom/PizzaTowerSage2019Vita
    tag: v0.62
    arquivo: PizzaTowerSAGE-v0.62.vpk
    versao: "0.62"
    titleid: PTSAGE001
    precisa_dados: true
    instrucoes: https://github.com/WolffsRoom/PizzaTowerSage2019Vita
  - tipo: dados
    nome: Dados do jogo (SAGE 2019)
    url: https://drive.google.com/file/d/1CBof60EExpF4IrZMhyix6CvRicqSONRA/view?usp=sharing
    instrucoes: https://pizzatowerguy.itch.io/pizza-tower-demo

---

Port não oficial da demo gratuita **Pizza Tower SAGE 2019 (v14)** para PlayStation Vita, lançado na versão **v0.62**. Utiliza o runner Butterscotch com VitaGL e OpenAL. O projeto relata jogabilidade completa do início ao fim, com **95% de progresso geral**.

## Novidades da v0.62

- Texturas BC3 (DXT5) residentes: 35 páginas de texturas (~87 MiB), reduzindo evicções durante a renderização e adicionando uma barreira de sincronização da GPU na troca de salas
- Roupa azul SAGE de Peppino renderizada com shader pal_swapper, sem duplicar a VRAM em atlas descompactados
- Dash / Super Jump corrigidos: a entrada VK_NOKEY inválida em saveData.ini não aciona mais o pulo automaticamente em Mach 3
- Seletores de fases e drift analógico ajustados: **Cima** utiliza D-pad Up (ou toque configurado), evitando entradas fantasma
- **Start** abre o menu de pausa original SAGE 2019; **Select** abre os ajustes nativos do port


- Três fases jogáveis: **Pizzascape**, **Oregano Desert** e **The Snick Challenge**
- Renderização acelerada pelo VitaGL a 60 FPS nos testes em hardware
- Super Jump corrigido: acione com X (Pular) ou soltando o direcional
- Deadzone do analógico corrigida para evitar movimentos involuntários
- Shader de troca de cores adaptado à GPU SGX543
- Streaming de áudio OpenAL com menor consumo de memória e menos distorções
- Fontes do menu de opções e glifos PlayStation revisados
- LiveArea e manual próprios, separados do port do jogo completo

## Instalação

- Baixe o [VPK v0.62](https://github.com/WolffsRoom/PizzaTowerSage2019Vita/releases/download/v0.62/PizzaTowerSAGE-v0.62.vpk) e instale pelo VitaShell
- Obtenha a demo original gratuita na [página oficial do Pizza Tower no itch.io](https://pizzatowerguy.itch.io/pizza-tower-demo)
- Extraia o arquivo data.win e copie-o para **ux0:data/pizzatowersage/data.win**
- O botão Baixar dados mantém o arquivo externo já disponibilizado; confira se ele corresponde à demo v14
- Abra o jogo pela LiveArea

## Requisitos

- PS Vita desbloqueado (HENkaku ou Ensō)
- Plugins kubridge.suprx, FdFix e libshacccg.suprx
- Arquivo original data.win da demo SAGE 2019 (v14), não incluído no VPK

## Créditos

- **Port de PS Vita:** Wolff's Room
- **Jogo original:** Tour de Pizza
- **Runner:** Butterscotch com VitaGL e OpenAL
