---
titulo: Pokémon Emerald Voxel 3DS — PT-BR v0.5.1
categoria: ports
grupo: Outras equipes
autor: HctrRB
autor_url: https://github.com/HctrRB
data: 2026-11-16 01:01
tag: Port nativo · PS Vita · PT-BR · v0.5.1
status: Disponível · v0.5.1
novidade: Update
resumo: Pokémon Emerald v0.5.1 para PS Vita, com Pokémon selvagens aprimorados, PT-BR revisado e novos controles de câmera.
chamada: Pokémon Emerald v0.5.1 para PS Vita com Pokémon selvagens visíveis, cenário voxel 3D e tradução PT-BR.
capa: capa.png
capturas:
  - captura-1.png
  - captura-2.png
  - captura-3.png
  - captura-4.png
  - captura-5.png
  - captura-6.png
  - captura-7.png
  - captura-8.png
  - captura-9.png
  - captura-10.png
ficha:
  Versão: v0.5.1
  Versão Wolff's Room: PT-BR · LiveArea · Manual · Câmera
  Port original: HctrRB
  Plataforma: PS Vita / PSTV
  Tecnologia: Código nativo ARM · vitaGL
links:
  Download VPK (Google Drive): https://drive.google.com/file/d/1ZNVd7j6EZyGgYTHuwIL-Edj6r57hJCGn/view?usp=sharing
fontes:
  Código-fonte do port (HctrRB): https://github.com/HctrRB/pokeemerald-vita-3ds
  Pull request PT-BR: https://github.com/HctrRB/pokeemerald-vita-3ds/pull/3
  Tradução original (Pokebat): https://pokebat.net/2017/04/pokemon-emerald-portugues-pt-brgba.html
downloads:
  - tipo: vpk
    nome: Pokémon Emerald PT-BR v0.5.1
    url: https://drive.google.com/file/d/1ZNVd7j6EZyGgYTHuwIL-Edj6r57hJCGn/view?usp=sharing
    arquivo: Pokemon-Emerald-PTBR-v0.5-Com-Manual.vpk
    versao: "0.5.1"
    precisa_dados: false
---
**Pokémon Emerald** recebeu um port nativo não oficial para PS Vita, desenvolvido por **HctrRB** a partir da [descompilação pret/pokeemerald](https://github.com/pret/pokeemerald). Não é um emulador: o código C do jogo é compilado para o processador ARM do Vita, com uma camada de plataforma que substitui as funções do hardware do GBA.

Com **vitaGL** e recursos do [Emerald 3DS](https://github.com/ZallaxDev/emerald-3ds), o port transforma a experiência clássica com cenários e batalhas 3D, mantendo a aventura original.

## Novidades da v0.5.1 — Pokémon selvagens visíveis
- **População procedural:** conjunto de até 48 Pokémon selvagens (`VW_POOL_MAX = 48`) independente dos 12 slots ativos, permitindo que apareçam pelo mapa como NPCs.
- **Pré-população de mapas vizinhos:** seleção dos tiles válidos de encontros e leitura antecipada de até 24 tiles das áreas conectadas, com pré-carregamento das espécies.
- **Streaming adaptado à câmera de 25°:** distâncias assimétricas norte/sul (`VW_VIEW_NORTH = 20`, `VW_SHOW_NORTH = 24`, `VW_HIDE_NORTH = 26`), histerese de entrada/saída e limite de dois sprites por quadro.
- **Correções de surgimento e animação:** evita reaparecimentos na transição entre mapas; efeitos de grama/água e crescimento aparecem somente nos spawns ou respawns reais.

## Recursos do port
- Mundo voxel 3D gerado em tempo real a partir dos mapas, com sol, sombras, ciclo de dia e noite e clima
- Batalhas 3D em cenários derivados da área em que o confronto começa
- Interface de toque sobre o mundo 3D, substituindo menus e caixas originais do GBA, com cinco temas
- Pokémon seguidores no estilo HGSS, relógio acelerado, encontros por horário e melhorias opcionais de qualidade de vida

## Melhorias da Wolff's Room
- Revisão da **tradução PT-BR**, incluindo textos, menus e novas entradas da interface Voxel.
- Interface adaptada em diferentes temas: letreiros para textos longos e descrições das cidades traduzidas.
- **Controle da câmera pelo analógico direito**, opção experimental de **primeira pessoa** e árvores 2D acompanhando a câmera (opcional).
- **Splash screen do vitaGL removido** da compilação personalizada.
- Tela inicial traduzida (**Versão Esmeralda** e **PRESSIONE START**), LiveArea personalizada e manual em português.

*As opções de câmera e primeira pessoa são experimentais. É recomendado jogar inicialmente com o preset padrão.*

## Instalação
- Baixe o VPK v0.5.1 pelo Google Drive no botão Download
- Instale pelo VitaShell em um PS Vita desbloqueado
- Inicie o jogo pela LiveArea
- Antes de atualizar uma instalação anterior, faça backup dos seus saves

## Créditos e referências
- **Port original:** [HctrRB](https://github.com/HctrRB/pokeemerald-vita-3ds)
- **Versão PT-BR e personalização:** Wolff's Room
- **Tradução de referência:** [Pokebat](https://pokebat.net/2017/04/pokemon-emerald-portugues-pt-brgba.html)
- **Descompilação:** [pret/pokeemerald](https://github.com/pret/pokeemerald)
- **Recursos 3D:** [Emerald 3DS](https://github.com/ZallaxDev/emerald-3ds)
- **Fontes consultadas:** [Pokémon Classic](https://www.dafont.com/pt/pokemon-classic.font) e [Font Meme — Pokémon](https://fontmeme.com/pt/fonte-de-pokemon/)
- **Referência dos assets da LiveArea:** [ícones de Pokémon Geração 3 para 3DS](https://www.reddit.com/r/pokemon/comments/1n01ybd/i_did_3ds_menu_icons_for_gen_3_pokemon_games/?i=2)

## Observações
- Port não oficial, sem vínculo com Nintendo, Game Freak ou The Pokémon Company.
- A compilação VitaSDK foi concluída; os novos controles de câmera e recursos gráficos ainda aguardam validação no PS Vita físico.
