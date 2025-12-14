# CampusOps AI - Setup Guide

## API Configuration

CampusOps AI uses **OpenAI API** for both embeddings and language model responses.

### Requirements

- **OpenAI API Key** (Required)
- Active OpenAI account with credits/quota

### Configuration

Create a `.env` file in the project root:

```env
# OpenAI API Key (REQUIRED)
OPENAI_API_KEY=sk-your-openai-key-here

# Model Settings (Optional - defaults provided)
EMBEDDING_MODEL=text-embedding-3-small
LLM_MODEL=gpt-3.5-turbo

# Application Settings
APP_NAME=CampusOps AI
DEBUG=false

# ChromaDB Settings
CHROMA_DB_PATH=./chroma_db
COLLECTION_NAME=policies

# RAG Settings
TOP_K_CHUNKS=5
LLM_TEMPERATURE=0.3
```

### Getting Your OpenAI API Key

1. Visit: https://platform.openai.com/api-keys
2. Create an account (or log in)
3. Go to billing: https://platform.openai.com/account/billing
4. Add payment method and credits (minimum $5 recommended)
5. Generate a new API key
6. Copy the key and add it to your `.env` file


### How It Works

1. **Embeddings**: Converts document chunks into vector representations
2. **Vector Storage**: Stores embeddings in ChromaDB for fast retrieval
3. **Query Processing**: Converts user questions into embeddings
4. **Semantic Search**: Finds relevant document chunks
5. **LLM Response**: Generates answer using GPT with retrieved context

### Installation

```bash
# Install dependencies
pip install -r src/requirements.txt

# Run the application
python run.py
```

### Pricing

**OpenAI (pay-as-you-go):**
- GPT-3.5-turbo: $0.50 per 1M input tokens, $1.50 per 1M output tokens
- Embeddings: $0.02 per 1M tokens

**Typical Costs:**
- Document indexing (one-time): $0.01 - $0.10 per document
- User queries: $0.001 - $0.01 per query
- Small campus deployment: ~$5-20/month

### Troubleshooting

**Error: "No OPENAI_API_KEY found"**
- Create a `.env` file in the project root
- Add your API key: `OPENAI_API_KEY=sk-your-key-here`

**Error: "Quota exceeded" or "429 error"**
- Your OpenAI account has no credits
- Go to https://platform.openai.com/account/billing
- Add payment method and credits
- Wait 2-3 minutes for activation

**Error: "Invalid API key" or "401 error"**
- Your API key is incorrect or expired
- Generate a new key at https://platform.openai.com/api-keys
- Update your `.env` file

### Support

For issues or questions:
- OpenAI Documentation: https://platform.openai.com/docs
- OpenAI Help: https://help.openai.com/

