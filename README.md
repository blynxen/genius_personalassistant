
# Genius as Personal Assistant

O **Genius Personal Assistant** é um assistente multimodal que utiliza inteligência artificial para responder a consultas de voz, realizar buscas locais e web, e processar diversos formatos de documentos como PDFs, DOCX e textos. O projeto inclui integração com APIs externas, como Ollama, MongoDB, Tavily e Google Search. Ele também suporta transcrição de áudio, geração de respostas em voz (TTS), moderação de conteúdo e visualização compartilhada da tela com o usuário.

---

## Funcionalidades Principais

- **Transcrição de voz**: Utiliza o modelo Whisper para transcrever áudio capturado.
- **Resposta por voz**: Converte o texto gerado pela LLM em áudio com TTS (Text-to-Speech).
- **Consulta em bases de conhecimento**: Busca em arquivos locais (PDF, DOCX, TXT) e MongoDB.
- **Moderação de conteúdo**: Filtra conteúdo inapropriado em português, inglês e espanhol.
- **Busca na Web**: Realiza buscas via Tavily e Google Search quando não encontra resposta local.
- **Interação visual**: Compartilha a tela com o usuário para navegação assistida e apoio visual.
- **Agentes especializados**: Inclui agentes para legislação, governança de dados e segurança no trabalho.

---

## Pré-requisitos

- Python 3.11 ou superior  
- CUDA 11.8 (para uso com GPU)  
- MongoDB Atlas (ou local configurado)  
- Edge WebDriver compatível com sua versão do Microsoft Edge  

---

## Instalação

### Passo 1: Clonar o repositório
```bash
git clone https://github.com/blynxen/genius_personalassistant.git
cd genius_personalassistant
```

### Passo 2: Criar ambiente virtual
```bash
python -m venv venv
# Linux/MacOS
source venv/bin/activate
# Windows
venv\Scripts\activate
```

### Passo 3: Instalar dependências
```bash
pip install -r requirements.txt
```

### Passo 4: Configurar MongoDB e variáveis
Crie um arquivo `.env` na raiz do projeto com:
```env
MONGO_URI=mongodb+srv://<usuario>:<senha>@cluster.mongodb.net/<banco>
MONGO_DB_NAME=<nome-db>
MONGO_COLLECTION_NAME=<colecao>
MONGO_VECTOR_INDEX=<index-vetor>

NEWS_API_KEY=<sua-chave-news-api>
TAVILY_API_KEY=<sua-chave-tavily>
GOOGLE_API_KEY=<sua-chave-google>
GOOGLE_CX=<seu-cx-google>
```

### Passo 5: Configurar o WebDriver
Baixe o `msedgedriver.exe` compatível e configure o caminho no arquivo `agents/legal_agent.py`:
```python
self.driver_path = r"D:/Personal_Assistent/msedgedriver.exe"
```

### Passo 6: Executar o projeto
```bash
python talking_llm.py
```

---

## Arquitetura do Projeto

```
/genius_personalassistant/
│
├── agents/
│   ├── knowledge_agent.py
│   ├── legal_agent.py
│   ├── safety_agent.py
│   ├── data_governance_agent.py
│   └── screen_interaction.py
│
├── apis/
│   ├── mongodb.py
│   ├── openai_integration.py
│   └── scraping_utils.py
│
├── config/
│   └── config.py
│
├── data/
│   ├── knowledge_base/
│   └── voice_sampler/
│
├── models/
├── utils/
│   ├── moderation.py
│   └── logger.py
│
├── talking_llm.py
├── agent.py
├── requirements.txt
└── README.md
```

---

## Uso

### Ativação por voz
Utilize palavras como **"genius"** ou **"gênio"** para ativar o assistente.

### Exemplos de comandos
- Pergunte sobre **legislação** para usar o agente jurídico.
- Pergunte sobre **segurança no trabalho** para consultar NRs.
- Pergunte sobre **LGPD ou governança** para questões de compliance.

### Interação com tela
O assistente pode “**ver a tela**” do usuário e acompanhar sua navegação, leitura ou tarefas.

### Resposta por voz
As respostas são convertidas em áudio automaticamente com o modelo TTS.

### Moderação
O conteúdo é filtrado automaticamente antes de ser respondido.

---

## Variáveis de Ambiente (.env)

```env
MONGO_URI=
MONGO_DB_NAME=
MONGO_COLLECTION_NAME=
MONGO_VECTOR_INDEX=
NEWS_API_KEY=
TAVILY_API_KEY=
GOOGLE_API_KEY=
GOOGLE_CX=
```

---

## Testes

- Teste a transcrição de voz com perguntas faladas.
- Teste busca em MongoDB e web.
- Teste respostas em TTS.
- Teste filtros de conteúdo com palavras sensíveis.
- Teste visualização de tela pedindo "veja a tela".

---

## Contribuição

1. Faça um fork do projeto.
2. Crie uma nova branch (`git checkout -b minha-feature`).
3. Commit suas mudanças (`git commit -m 'Nova feature'`).
4. Envie um pull request.

---

## Problemas Conhecidos

- Latência pode crescer em bases grandes.
- Qualidade de busca depende da API utilizada.

---

## Futuras Implementações

- Otimizar performance em grandes bases.
- Suporte a múltiplos idiomas no TTS.
- Mais integrações de busca web.
- Reconhecimento visual avançado na interação de tela.
