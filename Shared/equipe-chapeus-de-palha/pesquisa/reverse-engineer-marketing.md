# Avaliação Técnica: Reverse Engineer Marketing (REM)

**Data de verificação:** 12/11/2026  
**Avaliador:** Jinbe (Pesquisa e Leitura de Contexto Longo)  
**Solicitante:** Bot Builder / Luan (Chapéus de Palha)  
**Contexto de referência:** Post no X (`https://x.com/magdiel_rb/status/2120986575878385871`)  

---

## 1. Repositório Oficial e Atividade
- **Link oficial:** [https://github.com/dansugc/reverse-engineer-marketing](https://github.com/dansugc/reverse-engineer-marketing)
- **Autor / Organização:** DansUGC
- **Status:** **Ativo** (mantido e atualizado entre 2025 e final de 2026, com releases e suporte a MCP).

---

## 2. Licença do Código e Uso Comercial
- **Licença:** **MIT License** (código aberto permissivo).
- **Uso comercial:** **Permitido.** A licença MIT autoriza uso comercial, modificação, distribuição e integração interna sem pagamento de royalties, exigindo apenas a manutenção do copyright original.

---

## 3. Gratuito vs. APIs Pagas (Scrape Creators e Custos)
- **Funcionalidades 100% gratuitas (Zero Keys / Modo `--no-ai`):**
  - **Forensics de Domínio/HTML:** Detecção de pixels de rastreamento (Meta Pixel, Google Tag Manager/Analytics, TikTok Pixel, LinkedIn Insight Tag) e funis de conversão.
  - **SEO e Estrutura:** Varredura de `sitemap.xml` e `robots.txt` (SEO programático).
  - **Histórico:** Consulta à Wayback Machine (Internet Archive) para evolução de cópias e posicionamento.
  - **Bibliotecas de Anúncios:** Coleta de links e metadados públicos de transparência (Meta Ad Library, Google Ads Transparency Center, LinkedIn).
- **Funcionalidades que exigem API paga:**
  - **Scrape Creators (`SCRAPECREATORS_API_KEY`):** Utilizada para extração aprofundada de dados sociais orgânicos (Instagram, TikTok, YouTube, X, Reddit) contornando defesas anti-bot.
    - *Preço (scrapecreators.com):* Modelo de créditos pré-pagos (sem mensalidade fixa obrigatória). Teste grátis de 100 créditos (até 1.200 via dashboard); Pacote avulso de **$10**; Pacote Freelance de **$47** por 25.000 créditos (~$1,88/1.000 requisições); Pacote Business de **$497** por 500.000 créditos (~$0,99/1.000 requisições). Em geral, 1 requisição = 1 crédito.
  - **Síntese de IA (Opcional):** Se optar por gerar o relatório analítico formatado via LLM em vez dos dados brutos, consome a cota do Claude Code/Codex ou uma chave da Anthropic/OpenAI.

---

## 4. Compatibilidade com Windows, Dependências e Agentes
- **Linguagem / Runtime:** **TypeScript / Node.js** (Node 18+ ou 22+).
- **Dependências pesadas:** Nenhuma. Não precisa de Python, Docker ou compiladores C++.
- **Roda no Windows:** **Sim.** Executa perfeitamente via PowerShell / CMD com `npm install`, `npm run build` e execução via Node CLI (`node dist/cli.js <dominio> --no-ai`) ou pacote global.
- **Chamada a partir de agentes:** **Nativa.** O projeto implementa um servidor **MCP (Model Context Protocol)** e interface CLI com saída em Markdown (`report.md`), permitindo integração direta com Claude Code, Codex ou ferramentas do OpenBot.

---

## 5. Riscos: Termos de Uso (ToS), Privacidade e Dados
- **Termos de Uso das Plataformas:**
  - Varredura de site próprio ou de terceiros (HTML/DOM público) e Wayback Machine apresenta **risco negligenciável**.
  - O acesso direto a redes sociais é protegido; o uso do Scrape Creators transfere a camada de proxy para um provedor externo, reduzindo o risco de bloqueio do IP local.
  - As bibliotecas de anúncios (Meta / Google) são ferramentas públicas de transparência regulatória.
- **Privacidade e Dados Pessoais:**
  - O escopo da ferramenta é estritamente **B2B e dados técnicos públicos** (pixels, tags, sitemaps, perfis institucionais e fundadores divulgados publicamente no site ou LinkedIn).
  - Não coleta e não intercepta dados pessoais de clientes, pacientes ou fiéis.

---

## 6. Recomendação e Alternativa Gratuita
- **Recomendação em uma linha:** **Vale instalar apenas se for usado como MCP pela Vivi** (para auditar rapidamente presença digital, pixels e maturidade de parceiros na prospecção B2B); é dispensável para a Kureha (podólogos locais em Mogi raramente têm sites próprios estruturados) e para o Sanji (marcas de velas/artesanato podem ser checadas manualmente).
- **Alternativa gratuita sem instalar nada:** Consulta direta na **[Biblioteca de Anúncios da Meta](https://www.facebook.com/ads/library/)** + inspeção do código-fonte do site (`Ctrl+U` buscando `fbq` para Meta Pixel ou `GTM-` para Google Tag Manager) + verificação de histórico no **[Wayback Machine](https://web.archive.org/)**.
