---
titulo: Vampire Survivors Vita
categoria: ports
grupo: Outras equipes
data: 2026-11-14 15:31
tag: Port · C · PS Vita
status: v1.2.1 · Jogável
autor: Federicoilgrandebardo
autor_url: https://github.com/Federicoilgrandebardo
resumo: Port nativo de Vampire Survivors para PS Vita, desenvolvido por Federicoilgrandebardo.
capa: capa.png
trofeus: true
capturas:
  - captura-menu.png
  - captura-level-up.png
  - captura-moonspell.png
  - captura-foscari.png
  - captura-abyss.png
  - captura-coop.png
ficha:
  Desenvolvedor: Federicoilgrandebardo
  Versão: v1.2.1
  Title ID: VSPH00001
  Motor: C / raylib / vitaGL
  Troféus: Sim (NoTrpDrm)
  Dados: Necessita jogo original
links:
  Release oficial v1.2.1: https://github.com/Federicoilgrandebardo/vampire-survivors-vita/releases/tag/v1.2.1
  Dados externos (Google Drive): https://drive.google.com/file/d/1oKKnLI7tvSPWEDa0kmUkbIHeTsWXw4VF/view?usp=sharing
  Dados externos (MediaFire): https://www.mediafire.com/file/1627gt47emp57zb/VampireSurvivors+v1.1.zip/file
fontes:
  GitHub Vita Lite: https://wolffsroom.github.io/WolffsStore/Federicoilgrandebardo/vampire-survivors-vita/
  Repositório original: https://github.com/Federicoilgrandebardo/vampire-survivors-vita
downloads:
  - tipo: vpk
    nome: Vampire Survivors v1.2.1 (VPK)
    repo: Federicoilgrandebardo/vampire-survivors-vita
    tag: v1.2.1
    arquivo: VampireSurvivors-Vita-v1.2.1.vpk
    versao: "1.2.1"
    titleid: VSPH00001
    precisa_dados: true
    instrucoes: https://wolffsroom.github.io/WolffsStore/Federicoilgrandebardo/vampire-survivors-vita/
  - tipo: dados
    nome: Dados Vampire Survivors (Drive)
    url: https://drive.google.com/file/d/1oKKnLI7tvSPWEDa0kmUkbIHeTsWXw4VF/view?usp=sharing
    arquivo: VampireSurvivors-v1.1.zip
    versao: "1.1"
    tamanho: 136529441
    instrucoes: https://github.com/Federicoilgrandebardo/vampire-survivors-vita#setup-instructions-for-end-users
---

Port nativo de Vampire Survivors para PlayStation Vita criado e mantido por **Federicoilgrandebardo**. A Wolff's Room divulga o projeto; **Wolff contribuiu com sugestões de interface (UI) e jogabilidade, além dos frames da animação de abertura** creditados na release v1.2.1.

## Destaques
- Port nativo reescrito em C, com suporte a controles do PS Vita
- Co-op local entre dois consoles PS Vita
- Fases, personagens, itens, Arcanas, DLCs compatíveis e importação de saves de PC
- Troféus nativos, incluindo platina (requer NoTrpDrm)
- Interface adaptada ao Vita e animação de abertura

## Instalação
- Instale o VPK v1.2.1 de Federicoilgrandebardo
- O jogo **não inclui seus arquivos comerciais de dados** no VPK; obtenha os dados da sua própria cópia legítima do Vampire Survivors para PC, seguindo a ferramenta de extração do repositório original
- Alternativamente, há links externos de dados compartilhados para consulta: Google Drive ou MediaFire; a Wolff's Room não hospeda nem verifica a autorização de redistribuição desses arquivos
- Caso use um ZIP de dados compatível, extraia a pasta `VampireSurvivors` dentro de `ux0:data/`, resultando em `ux0:data/VampireSurvivors/`
- O ZIP do Drive foi verificado quanto à estrutura e contém essa pasta na raiz; o MediaFire exige baixar pelo navegador, pois não fornece um link direto estável
- Instale `libshacccg.suprx` conforme o README; troféus requerem o plugin `NoTrpDrm`

## Créditos
- **Port e desenvolvimento:** Federicoilgrandebardo
- **Sugestões de UI e jogabilidade / frames da abertura:** Wolff (Wolff's Room)
- **Jogo original:** poncle
