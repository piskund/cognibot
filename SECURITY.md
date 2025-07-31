# CogniBot Security Guidelines

## 🔒 Critical Security Requirements

### **1. API Key Management**

**❌ NEVER COMMIT SECRETS TO GIT**

Your `.env` file contains sensitive credentials and should NEVER be committed to version control.

**✅ Proper Setup:**
```bash
# 1. Copy template
cp src/env_template.txt .env

# 2. Add your real credentials to .env
# 3. NEVER commit .env to git (it's in .gitignore)
```

**🚨 If you accidentally committed secrets:**
1. **Immediately rotate all API keys**
2. **Remove from git history:** `git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch .env' --prune-empty --tag-name-filter cat -- --all`
3. **Force push:** `git push origin --force --all`

### **2. Production Deployment**

**Environment Variables (Recommended):**
```bash
# Set in your production environment
export TELEGRAM_BOT_TOKEN="your_token_here"
export OPENAI_API_KEY="your_key_here"
export TELEGRAM_CHANNEL_ID="@your_channel"
```

**Docker Secrets (Advanced):**
```dockerfile
# Use Docker secrets or environment variables
FROM python:3.11
COPY . /app
WORKDIR /app
RUN pip install -r src/requirements.txt
CMD ["python", "src/run_bot.py"]
```

### **3. Access Control**

**Bot Permissions:**
- Only grant necessary permissions to your bot
- Use specific channel admin rights, not owner rights
- Regularly audit bot access

**API Key Restrictions:**
- Set OpenAI API usage limits
- Monitor usage regularly
- Use separate keys for development/production

### **4. Monitoring**

**Set up alerts for:**
- Unusual API usage spikes
- Bot errors or crashes
- Unauthorized access attempts

## 🛡️ Security Checklist

- [ ] `.env` file is in `.gitignore`
- [ ] No secrets in git history
- [ ] OpenAI API key has usage limits
- [ ] Bot has minimal required permissions
- [ ] Monitoring and alerting configured
- [ ] Regular security audits planned

## 🚨 Incident Response

**If credentials are compromised:**
1. **Immediately revoke/rotate all keys**
2. **Check usage logs for unauthorized activity**
3. **Update all affected systems**
4. **Review and improve security practices**

## 📞 Contact

For security issues, please contact: [your-security-email]