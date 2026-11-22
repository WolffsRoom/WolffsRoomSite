---
titulo: "Pizza Tower - Noise's Hardoween Demo"
categoria: ports
grupo: Finalizado
data: 2026-11-22 17:14
tag: Port · GameMaker · PS Vita
status: v0.41 · Jogável
novidade: Release
versao: v0.41
resumo: "Noise's Hardoween Demo chega ao PS Vita na v0.41, com correções gráficas e otimização automática do data.win no primeiro boot."
chamada: "The Noise chega ao PlayStation Vita! A demo de Halloween de Pizza Tower em um port nativo com otimizações de textura, gráficos e áudio."
progresso: 95
capa: capa.png
pixelado: true
ficha:
  Status: Lançado · Jogável (95% de progresso)
  Versão: v0.41
  Demo original: "Pizza Tower: Noise's Hardoween Demo"
  Criadores: Tour de Pizza
  Engine original: GameMaker
  Runtime: Butterscotch + VitaGL + OpenAL
  Title ID: PTNHW0001
  Dados: ux0:data/noisehardoween/data.win
capturas:
  - captura-1.png
  - captura-2.png
  - captura-3.png
  - captura-4.png
  - captura-5.png
  - captura-6.png
links:
  Baixar VPK: https://github.com/WolffsRoom/PizzaTowerNoisesHardoween/releases/download/v0.41/PizzaTowerHardoween-v0.41.vpk
  Baixar dados: https://drive.google.com/file/d/1X9lZ5Y_hcBPbsNbI_hIj6bz8I8johboy/view?usp=sharing
fontes:
  GitHub: https://github.com/WolffsRoom/PizzaTowerNoisesHardoween
  Demo original: https://pizza-t0w3rfan.itch.io/noises-hardoween
clock:
  Desempenho: 60 FPS (conforme informações dos testes do projeto)
downloads:
  - tipo: vpk
    nome: "Pizza Tower Noise's Hardoween v0.41 (VPK)"
    repo: WolffsRoom/PizzaTowerNoisesHardoween
    tag: v0.41
    arquivo: PizzaTowerHardoween-v0.41.vpk
    versao: "0.41"
    titleid: PTNHW0001
    tamanho: 17210652
    precisa_dados: true
    instrucoes: https://github.com/WolffsRoom/PizzaTowerNoisesHardoween
  - tipo: dados
    nome: "Dados da demo (data.win)"
    url: https://drive.google.com/file/d/1X9lZ5Y_hcBPbsNbI_hIj6bz8I8johboy/view?usp=sharing
    instrucoes: https://pizza-t0w3rfan.itch.io/noises-hardoween
---

Port não oficial da demo gratuita **Pizza Tower: Noise's Hardoween** para PlayStation Vita, lançado na versão **v0.41**. Jogue como **The Noise** em uma aventura temática de Halloween. O projeto está marcado com **95% de progresso geral**.

## Novidades da v0.41

- **Travamento na transformação de cavaleiro corrigido:** shader de troca de paletas adaptado para a GPU do PS Vita, incluindo as roupas desbloqueáveis de The Noise e cores dos inimigos.
- **Texturas em resolução nativa:** páginas de textura ativas em 2048×2048, com melhorias na nitidez dos cenários, sprites e interface.
- **Fundos corrigidos:** maior precisão dos shaders para evitar linhas vermelhas e artefatos entre texturas.
- **Ordem de desenho corrigida:** The Noise não aparece indevidamente atrás de portas e escadas.
- **Áudio otimizado:** streaming OpenAL para reduzir o consumo de memória.
- **Otimização automática:** o port prepara as texturas do jogo diretamente no PS Vita no primeiro boot.

## Instalação

- Baixe o **VPK v0.41** pelo botão de download e instale usando o VitaShell.
- Obtenha o arquivo original **data.win** da demo gratuita pelo botão **Baixar dados** ou pela página da [demo original](https://pizza-t0w3rfan.itch.io/noises-hardoween).
- Coloque o arquivo **data.win** na pasta **/ux0:/data/noisehardoween/** do PS Vita (caminho VitaShell: **ux0:data/noisehardoween/data.win**).
- Abra o jogo pela LiveArea.

## Observações importantes

- **O primeiro boot pode demorar mais.** O próprio VPK ajustará o arquivo **data.win** do jogo, otimizando os atlas de texturas para o PS Vita. Não é necessário usar patchers em outro dispositivo.
- O port mantém um backup do arquivo original como **data.original.win** durante a otimização inicial.
- O VPK não inclui os dados proprietários da demo. É necessário fornecer o **data.win** original, compatível com a versão indicada no projeto.

## Requisitos

- PS Vita desbloqueado (HENkaku/Ensō).
- Plugins **kubridge**, **FdFix** e **libshacccg.suprx**.
- Arquivo **data.win** da demo original.

## Créditos

- **Port para PS Vita:** Wolff's Room
- **Demo original:** Tour de Pizza
- **Disponibilização da demo:** Pizza Tower Fan (itch.io)
- **Runtime:** Butterscotch, VitaGL e OpenAL
