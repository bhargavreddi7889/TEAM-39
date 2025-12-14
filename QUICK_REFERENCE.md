# CampusOps AI - Quick Reference Guide

## 🚀 Quick Start

### 1. Start the System
```bash
# Terminal 1: Start API Server
python run.py

# Terminal 2: Start UI (in another terminal)
cd src && streamlit run app_ui.py
```

### 2. Access the System
- **Student Portal:** http://localhost:8501 (or your configured port)
- **Admin Portal:** http://localhost:8501 (same URL, select Admin tab)
- **API Docs:** http://brahamand.ai:9000/docs

### 3. Login Credentials
```
Admin:
  Username: admin
  Password: admin123

Student:
  Username: student
  Password: student123
```

---

## 📁 File Operations (Admin)

### Upload a Document
1. Login as Admin
2. Go to "Files" section
3. Click "Choose a file"
4. Select .txt, .docx, or .pdf file
5. Click "Upload & Index"
6. ✅ File is automatically indexed into RAG!

### Delete a Document
1. Go to "Files" section
2. Find the file in the list
3. Click 🗑️ button
4. Confirm deletion
5. ✅ File and all its chunks are removed from RAG!

### Re-index All Files
1. Go to "Re-index" section
2. Choose whether to clear existing database
3. Click "Start Re-indexing"
4. ✅ All files are re-processed!

---

## 💬 Asking Questions (Student)

### Simple Query
1. Login as Student
2. Type your question in the input box
3. Click "Ask" or press Enter
4. ✅ Get instant AI-powered answer with sources!

### Example Questions
```
- What is the minimum attendance requirement?
- Tell me about the placement eligibility criteria
- What are the examination rules?
- When does the semester start?
- What is the hostel policy?
```

---

## 🔧 System Verification

### Run Full System Check
```bash
python verify_system.py
```

This will test:
- ✅ API server connectivity
- ✅ Database statistics
- ✅ Document processing (.txt, .docx, .pdf)
- ✅ Query system
- ✅ Answer generation
- ✅ Re-indexing

---

## 📊 Understanding the Dashboard (Admin)

### Key Metrics
- **Knowledge Chunks:** Total number of text chunks in the database
- **Policy Documents:** Total number of files uploaded
- **System Status:** Online/Offline indicator

### File Information
- Each file shows:
  - 📄 Filename
  - Size in bytes
  - File type (.txt, .docx, .pdf)
  - Upload timestamp

---

## 🎯 How RAG Updates Work

### Automatic Updates
The RAG system automatically updates when you:

1. **Upload a file:**
   ```
   File saved → Text extracted → Chunks created → Embeddings generated → 
   Stored in ChromaDB → ✅ Ready for queries immediately!
   ```

2. **Delete a file:**
   ```
   Find file's chunks → Remove from ChromaDB → Delete file → 
   ✅ RAG updated instantly!
   ```

3. **Modify a file:**
   ```
   Delete old file (removes old chunks) → Upload new file (adds new chunks) → 
   ✅ RAG reflects new content!
   ```

### No Manual Steps Required!
- ❌ No need to manually trigger indexing
- ❌ No need to restart the system
- ❌ No delays or waiting
- ✅ Everything is automatic and instant!

---

## 📄 Supported File Formats

### .txt (Text Files)
- ✅ Direct UTF-8 reading
- ✅ Simple and fast
- ✅ Best for plain text policies

### .docx (Word Documents)
- ✅ Extracts all paragraphs
- ✅ Smart chunking
- ✅ Preserves structure
- ✅ Best for formatted documents

### .pdf (PDF Documents)
- ✅ Extracts text from all pages
- ✅ Smart chunking
- ✅ Handles complex layouts
- ✅ Best for official documents

---

## 🐛 Troubleshooting

### API Not Starting
**Problem:** `python run.py` fails

**Solutions:**
1. Check if port 9000 is already in use
2. Verify OpenAI API key in `.env` file
3. Install dependencies: `pip install -r src/requirements.txt`

### No Answer Generated
**Problem:** Query returns "I don't have information"

**Solutions:**
1. Check if files are uploaded (Admin → Files)
2. Verify chunks in database (Admin → Dashboard)
3. Try re-indexing (Admin → Re-index)
4. Make sure files contain relevant content

### Upload Fails
**Problem:** File upload shows error

**Solutions:**
1. Check file format (.txt, .docx, .pdf only)
2. Verify file is not corrupted
3. Check file size (very large files may time out)
4. Look at API logs for specific error

### Slow Responses
**Problem:** Queries take too long

**Solutions:**
1. Check OpenAI API status
2. Reduce `TOP_K_CHUNKS` in config (default: 5)
3. Verify internet connection
4. Check API rate limits

---

## ⚙️ Configuration

### Environment Variables (.env)
```env
# Required
OPENAI_API_KEY=sk-your-key-here

# Optional (defaults shown)
EMBEDDING_MODEL=text-embedding-3-small
LLM_MODEL=gpt-3.5-turbo
TOP_K_CHUNKS=5
LLM_TEMPERATURE=0.3
COLLECTION_NAME=policies
```

### Changing Models
To use different models, update `.env`:

```env
# Use GPT-4 for better quality (more expensive)
LLM_MODEL=gpt-4-turbo-preview

# Use larger embeddings for better search
EMBEDDING_MODEL=text-embedding-3-large
```

---

## 📈 Best Practices

### Document Preparation
1. **Use clear headings** - Helps chunking
2. **Break into paragraphs** - Better separation
3. **Remove noise** - Clean up before upload
4. **Use proper formatting** - Maintains structure

### Query Tips
1. **Be specific** - "What is the attendance policy for B.Tech?" vs "attendance?"
2. **Use keywords** - Include terms from your documents
3. **Ask complete questions** - Better context for AI
4. **One topic per query** - Don't combine multiple questions

### System Maintenance
1. **Regular backups** - Backup `chroma_db/` folder
2. **Monitor chunks** - Check dashboard metrics
3. **Clean old files** - Remove outdated policies
4. **Re-index periodically** - Keeps database optimal

---

## 📞 API Endpoints

### Health Check
```bash
curl http://brahamand.ai:9000/
```

### Query
```bash
curl -X POST http://brahamand.ai:9000/query/ \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the attendance policy?"}'
```

### Upload File
```bash
curl -X POST http://brahamand.ai:9000/admin/files \
  -F "file=@path/to/document.pdf"
```

### Get Stats
```bash
curl http://brahamand.ai:9000/admin/stats
```

### List Files
```bash
curl http://brahamand.ai:9000/admin/files
```

### Re-index
```bash
curl -X POST http://brahamand.ai:9000/admin/reindex?clear_existing=true
```

---

## 🔒 Security Notes

### Production Deployment
1. **Change default passwords** - Don't use admin/admin123!
2. **Use HTTPS** - Secure your connections
3. **Restrict API access** - Use authentication
4. **Protect .env** - Never commit API keys
5. **Regular updates** - Keep dependencies current

### API Key Safety
- ✅ Store in `.env` file (not in code)
- ✅ Add `.env` to `.gitignore`
- ✅ Rotate keys periodically
- ✅ Monitor usage on OpenAI dashboard
- ❌ Never commit keys to git
- ❌ Never share keys publicly

---

## 📚 Additional Resources

### Documentation
- Main README: `README.md`
- Setup Guide: `SETUP.md`
- Improvements: `IMPROVEMENTS_SUMMARY.md`
- Guidelines: `GUIDELINES.md`

### OpenAI Resources
- API Docs: https://platform.openai.com/docs
- Usage Dashboard: https://platform.openai.com/usage
- API Keys: https://platform.openai.com/api-keys

### Technology Stack
- FastAPI: https://fastapi.tiangolo.com/
- Streamlit: https://docs.streamlit.io/
- ChromaDB: https://docs.trychroma.com/
- OpenAI: https://platform.openai.com/docs

---

## 💡 Tips & Tricks

### Faster Development
```bash
# Auto-reload on code changes
uvicorn src.main:app --reload --host 0.0.0.0 --port 9000
```

### Debugging
```bash
# Check logs in real-time
python run.py | tee logs.txt
```

### Batch Upload
Use the API to upload multiple files:
```bash
for file in data/*.pdf; do
  curl -X POST http://brahamand.ai:9000/admin/files -F "file=@$file"
done
```

### Backup Database
```bash
# Backup ChromaDB
tar -czf chroma_backup_$(date +%Y%m%d).tar.gz chroma_db/

# Restore
tar -xzf chroma_backup_20240101.tar.gz
```

---

## ✅ Quick Checklist

### Before Going Live
- [ ] `.env` file created with valid API key
- [ ] All dependencies installed
- [ ] Documents uploaded and indexed
- [ ] Test queries working correctly
- [ ] Default passwords changed
- [ ] System verification passed
- [ ] Backup created

### Daily Operations
- [ ] Check API server is running
- [ ] Monitor OpenAI usage
- [ ] Review query accuracy
- [ ] Update documents as needed
- [ ] Check system metrics

---

## 🎉 You're All Set!

Your CampusOps AI system is now ready to handle all campus policy queries with perfect accuracy!

For questions or issues, review the troubleshooting section or check the full documentation.
