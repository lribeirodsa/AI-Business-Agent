# Guia de Deploy: Master Business Auditor no Streamlit Cloud

Este guia detalha os passos exatos para hospedar sua aplicação **Master Business Auditor** no Streamlit Cloud, tornando-a acessível publicamente e permanentemente [1].

## 1. Preparação dos Arquivos Essenciais

Você precisará de três arquivos principais no seu repositório GitHub:

| Arquivo | Conteúdo | Propósito |
| :--- | :--- | :--- |
| `master_business_auditor.py` | O código Python principal (já fornecido). | O Streamlit executa este arquivo. |
| `requirements.txt` | Lista de dependências Python (já fornecido). | O Streamlit Cloud instala estas bibliotecas. |
| `.streamlit/secrets.toml` | Sua chave de API da OpenAI. | Permite que o código acesse o GPT-4o mini na nuvem. |

### 1.1. Configuração da Chave de API

O Streamlit Cloud precisa da sua chave `OPENAI_API_KEY` para que os agentes de IA funcionem. Você tem duas opções:

**Opção A (Recomendada - Mais Segura):**
1.  **Não** crie o arquivo `.streamlit/secrets.toml` no seu repositório.
2.  Adicione a chave diretamente na interface do Streamlit Cloud durante o deploy (veja o Passo 2.5).

**Opção B (Alternativa):**
1.  Crie uma pasta chamada `.streamlit` na raiz do seu projeto.
2.  Dentro dela, crie um arquivo chamado `secrets.toml`.
3.  Adicione o seguinte conteúdo, substituindo `SUA_CHAVE_AQUI` pela sua chave real:
    ```toml
    OPENAI_API_KEY = "SUA_CHAVE_AQUI"
    ```
    *Nota: Se você usar esta opção, o Streamlit Cloud irá criptografar o arquivo, mas a Opção A é geralmente preferida para segredos.*

## 2. Implantação no GitHub

1.  **Crie um Repositório**: Crie um novo repositório público no GitHub (ex: `master-business-auditor`).
2.  **Faça o Upload**: Faça o upload dos arquivos `master_business_auditor.py` e `requirements.txt` para a raiz do seu novo repositório.

## 3. Deploy no Streamlit Cloud

1.  **Acesse o Streamlit Cloud**: Vá para [https://share.streamlit.io/](https://share.streamlit.io/) e faça login com sua conta GitHub.
2.  **Inicie o Deploy**: Clique no botão **"New App"** no canto superior direito.
3.  **Conecte o Repositório**:
    - **Repository**: Selecione o repositório que você acabou de criar (ex: `seu-usuario/master-business-auditor`).
    - **Branch**: Mantenha como `main` (ou `master`).
    - **Main file path**: Digite `master_business_auditor.py`.
4.  **Configure os Segredos (Opção A)**:
    - Clique em **"Advanced settings"**.
    - Na seção **"Secrets"**, adicione a variável de ambiente `OPENAI_API_KEY` e cole o valor da sua chave de API.
5.  **Finalize**: Clique em **"Deploy"**.

O Streamlit Cloud levará alguns minutos para instalar as dependências e iniciar o servidor. Ao final, você receberá um link público e permanente para sua ferramenta de auditoria.

## Referências

[1] Streamlit. *Deploy your app*. Disponível em: [https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app](https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app)
