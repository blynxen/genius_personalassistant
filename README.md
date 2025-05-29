Genius as Personal Assistent
O Genius Personal Assistent é um assistente multimodal que utiliza inteligência artificial para responder a consultas de voz, realizar buscas locais e web, e processar diversos formatos de documentos como PDFs, DOCX, e textos. O projeto inclui integração com APIs externas, como o Ollama, MongoDB e serviços de busca como Tavily e Google Search. Ele também suporta transcrição de áudio, geração de respostas em voz (TTS), moderação de conteúdo, e visualização compartilhada da tela com o usuário.

Funcionalidades Principais
Transcrição de voz: Utilizando o modelo Whisper para transcrever áudio capturado.
Resposta por voz: Converte o texto gerado pela LLM em áudio utilizando TTS (Text-to-Speech).
Consulta em bases de conhecimento: Faz buscas em bases de conhecimento locais (arquivos PDF, DOCX, TXT) e remotas (MongoDB).
Moderação de conteúdo: Filtra conteúdo inapropriado em diferentes idiomas (português, inglês e espanhol).
Busca na Web: Se não houver uma resposta na base de conhecimento, o assistente realiza uma busca na web utilizando APIs como Tavily e Google Search.
Interação e visualização de tela: O assistente pode compartilhar a tela com o usuário, permitindo uma experiência visual durante a navegação ou execução de tarefas.
Agentes especializados: Inclui agentes para busca de legislação, governança de dados e segurança no trabalho.
Pré-requisitos
Antes de começar, certifique-se de ter o seguinte instalado:

Python 3.11 ou superior
CUDA 11.8 (para aceleração por GPU)
MongoDB Atlas (ou outro MongoDB configurado)
Edge WebDriver compatível com sua versão do Microsoft Edge
Instalação
Passo 1: Clone o repositório
bash
Copiar código
git clone xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
cd personal_assistent
Passo 2: Crie um ambiente virtual
bash
Copiar código
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate      # Windows
Passo 3: Instale as dependências
Execute o comando abaixo para instalar todas as dependências:

bash
Copiar código
pip install -r requirements.txt
Passo 4: Configuração do MongoDB
Certifique-se de configurar corretamente seu MongoDB Atlas ou local. Crie um arquivo .env na raiz do projeto com as seguintes variáveis:

bash
Copiar código
MONGO_URI=mongodb+srv://<usuario>:<senha>@cluster0.mongodb.net/<seu-banco>?retryWrites=true&w=majority
MONGO_DB_NAME=
MONGO_COLLECTION_NAME=
MONGO_VECTOR_INDEX=

NEWS_API_KEY=<sua-chave-news-api>
TAVILY_API_KEY=<sua-chave-tavily>
GOOGLE_API_KEY=<sua-chave-google>
GOOGLE_CX=<seu-cx-google-search>
Passo 5: Baixe e configure o WebDriver do Edge
Baixe o WebDriver correto para a versão do Microsoft Edge que você está usando e configure-o no caminho correto. Coloque o arquivo msedgedriver.exe na pasta raiz do projeto ou ajuste o caminho no arquivo agents/legal_agent.py:

python
Copiar código
self.driver_path = r"D:/Personal_Assistent/msedgedriver.exe"
Passo 6: Iniciar o Projeto
Após configurar tudo, você pode iniciar o projeto com:

bash
Copiar código
python talking_llm.py
Arquitetura do Projeto
bash
Copiar código
/Personal_Assistent/
│
├── /agents/                # Agentes especializados
│   ├── __init__.py
│   ├── knowledge_agent.py   # Busca em base local e MongoDB
│   ├── legal_agent.py       # Agente de legislação
│   ├── safety_agent.py      # Agente de segurança no trabalho
│   ├── data_governance_agent.py  # Agente de governança de dados
│   ├── screen_interaction.py     # Controle de interação e visualização de tela do usuário
│
├── /apis/                  # Integrações com APIs externas
│   ├── __init__.py
│   ├── mongodb.py           # Integração com MongoDB
│   ├── openai_integration.py  # Integração com OpenAI
│   ├── scraping_utils.py    # Funções de scraping de dados
│
├── /config/                # Arquivos de configuração
│   ├── __init__.py
│   ├── config.py            # Configurações gerais
│   ├── .env                 # Variáveis de ambiente sensíveis
│
├── /data/                  # Dados e arquivos de conhecimento
│   ├── knowledge_base/      # Base de conhecimento local (PDF, DOCX, etc.)
│   ├── voice_sampler/       # Amostras de voz para o TTS
│
├── /docs/                  # Documentação do projeto
├── /models/                # Modelos de TTS e Text-to-Image
├── /utils/                 # Ferramentas auxiliares
│   ├── moderation.py        # Moderação de conteúdo
│   ├── logger.py            # Logging personalizado
│
├── agent.py                # Arquivo principal do agente
├── talking_llm.py          # Gerenciador do agente multimodal
├── requirements.txt        # Dependências do projeto
├── README.md               # Documentação do projeto
Uso
Ativação por palavra-chave: Use uma das palavras de ativação como "genius" ou "gênio" para ativar o assistente.

Comandos:

Pergunte sobre legislação para usar o agente de legislação.
Pergunte sobre segurança no trabalho para consultas relacionadas a NRs.
Pergunte sobre LGPD ou governança de dados para questões de proteção de dados.
Caso não haja uma resposta local, o sistema buscará na web automaticamente.
Interação com a tela:

O assistente pode visualizar a tela com o usuário, permitindo que ele navegue junto em páginas web, visualize documentos e auxilie com atividades que envolvem interação visual.
Utilize os comandos de ativação para pedir que o assistente "veja a tela".
Respostas por voz: O assistente responderá em áudio utilizando o modelo TTS configurado.

Moderação de conteúdo: Todo o conteúdo inapropriado é filtrado antes da resposta ser dada.

Variáveis de Ambiente
As seguintes variáveis de ambiente devem ser configuradas no arquivo .env:

MONGO_URI: URI de conexão com o MongoDB.
MONGO_DB_NAME: Nome do banco de dados no MongoDB.
MONGO_COLLECTION_NAME: Nome da coleção no MongoDB.
MONGO_VECTOR_INDEX: Índice de vetores do MongoDB.
NEWS_API_KEY: Chave da API para News.
TAVILY_API_KEY: Chave da API Tavily para busca web.
GOOGLE_API_KEY: Chave da API do Google para busca web.
GOOGLE_CX: Código do motor de busca personalizado do Google.
Testes
Você pode testar o assistente simplesmente fazendo perguntas e verificando se o sistema transcreve corretamente o áudio, busca as respostas no MongoDB ou na web, e responde com o áudio gerado.

Para testar a moderação de conteúdo, tente usar palavras inapropriadas e veja se elas são filtradas corretamente.

Para testar a interação de tela, solicite que o assistente visualize sua tela e acompanhe suas ações.

Contribuição
Se desejar contribuir, faça um fork do projeto, crie uma branch, faça suas modificações e envie um pull request.

Problemas Conhecidos
A latência de resposta pode aumentar se a base de conhecimento local ou MongoDB for muito grande.
Algumas buscas na web podem não retornar resultados relevantes, dependendo da qualidade da API externa utilizada.
Futuras Implementações
Melhorar o desempenho em bases de conhecimento grandes com otimização de consultas.
Adicionar suporte para mais línguas no TTS.
Implementar integração com mais serviços de busca.
Expansão da interação com tela para inclusão de reconhecimento visual avançado.