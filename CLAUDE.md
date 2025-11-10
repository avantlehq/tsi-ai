# CLAUDE.md

Tento súbor poskytuje kontext pre Claude Code pri práci s TSI Agent repozitárom.

## Kontext projektu TSI Directory

**TSI Directory** je kompletná platforma pre konverziu transportných dát v rámci európskych štandardov. Kombinuje marketing site a AI-powered conversion engine pre EDIFACT a GTFS formáty.

### Architektúra platformy

**Dvojkomponentová architektúra:**

1. **TSI Directory** (marketing vrstva) - **PLÁNOVANÉ**
   - Doména: `tsi.directory` 
   - Repo: `avantlehq/tsi-directory-marketing` (treba vytvoriť)
   - Funkcie: lead generation, pricing, kontaktné formuláre, SEO

2. **TSI Agent Runtime** (conversion engine) - **TENTO REPOZITÁR ✅ HOTOVO**
   - Doména: `tsi.avantle.ai`
   - Repo: `avantlehq/tsi-ai`
   - Funkcie: conversion API, agent dashboard, file processing, monitoring

### API rozhranie (poskytované týmto repozitárom)

```
POST /api/v1/convert → EDIFACT/GTFS konverzia
POST /api/v1/validate → input validácia
GET /api/v1/status → system monitoring
POST /api/provision → tenant setup
```

**Guardrails:**
- Authorization: Bearer <JWT> s tenant_id
- Rate limiting per tenant
- File upload/download handling
- Real-time processing status

## Aktuálny stav projektu (Nov 10, 2024)

### ✅ HOTOVÉ KOMPONENTY

**TSI Agent Runtime (tsi.avantle.ai):**
- ✅ Next.js 16 + TypeScript + Tailwind CSS v4 
- ✅ Production deployment na Vercel
- ✅ Conversion API endpoints (mock + real microservice)
- ✅ Agent monitoring dashboard
- ✅ File upload/download handling
- ✅ JWT middleware a security
- ✅ Responsive UI s kompletným styling

**Python Microservice:**
- ✅ FastAPI conversion service
- ✅ EDIFACT writers (SKDUPD, TSDUPD)
- ✅ GTFS export functionality
- ✅ Docker containerization
- ✅ Health check endpoints
- ✅ Tested s real transport data

**Deployment Status:**
- ✅ GitHub repo: https://github.com/avantlehq/tsi-ai
- ✅ Production: https://tsi.avantle.ai
- ✅ All commits pushed, working tree clean
- ✅ Tailwind CSS v4 styling functional
- ✅ API endpoints live a secure

### 🔧 Technical Stack

**Frontend:**
- Framework: Next.js 16.0.1 s App Router
- Styling: Tailwind CSS v4 (alpha)
- Language: TypeScript
- Package manager: pnpm
- Deployment: Vercel

**Backend Services:**
- Conversion service: FastAPI + Python
- File handling: Multipart uploads
- Database: SQLite (dev) / PostgreSQL (planned)
- Auth: JWT middleware
- Containerization: Docker

**Data Formats:**
- Input: JSON transport data
- Output: EDIFACT (SKDUPD/TSDUPD), GTFS
- Validation: Real-time input checking
- Processing: Streaming a progress updates

### 🚀 Production URLs

- **Main platform**: https://tsi.avantle.ai
- **Agent dashboard**: https://tsi.avantle.ai/agent  
- **API base**: https://tsi.avantle.ai/api/v1/
- **Conversion**: POST /api/v1/convert
- **Status**: GET /api/v1/status
- **Validation**: POST /api/v1/validate

### 📋 ĎALŠIE KROKY

**Immediate Next Steps:**

1. **TSI Directory Marketing Site** (čaká na nameserver change)
   - Doména: `tsi.directory` (nameservery requested od Active24)
   - Potrebuje: Next.js 16 marketing site
   - Template: Kopírovať štruktúru z dpia-ai
   - Timeline: 3-4 dni po nameserver zmene

2. **Database Integration**
   - Pridať PostgreSQL pre production
   - User authentication a workspace management
   - Conversion history a project tracking

3. **Advanced Features**
   - Real-time conversion progress
   - Batch processing support
   - Enhanced validation rules
   - API rate limiting implementation

### 🎯 Domain Setup Status

**Configured:**
- ✅ `tsi.avantle.ai` - Vercel nameservers, production ready

**Pending:**
- 🔄 `tsi.directory` - Active24 nameserver change requested
- 📧 `raildatcon.sk` - backup option

### 📊 Project Structure

```
C:\Users\rasti\Projects\avantlehq\tsi-ai\
├── src/
│   ├── app/
│   │   ├── page.tsx              # Homepage s TSI Directory branding
│   │   ├── agent/page.tsx        # Monitoring dashboard
│   │   └── api/                  # Conversion API endpoints
│   ├── middleware.ts             # JWT auth a rate limiting
│   └── globals.css               # Tailwind v4 imports
├── conversion-service/           # FastAPI microservice
│   ├── main.py                   # API server
│   ├── src/tsi_converter/        # Core conversion logic
│   └── Dockerfile                # Containerization
└── CLAUDE.md                     # Tento súbor

```

## Development Commands

```bash
# Frontend Development (z tsi-ai/)
pnpm dev              # Start dev server (http://localhost:3000)
pnpm build           # Build for production
pnpm start           # Start production server  
pnpm lint            # Run ESLint

# Microservice Development (z conversion-service/)
python main.py       # Start FastAPI server (http://localhost:8000)
docker build -t tsi-converter . # Build Docker image
docker run -p 8000:8000 tsi-converter # Run containerized

# Deployment
git add . && git commit -m "message" && git push origin main

# API Testing
curl -X POST "https://tsi.avantle.ai/api/v1/convert" \
  -H "Authorization: Bearer test" \
  -H "Content-Type: application/json" \
  -d '{"inputData": {...}, "outputFormat": "SKDUPD"}'
```

## Dôležité Poznámky

1. **Tailwind v4**: Používame alpha verziu, syntax `@import "tailwindcss"` v globals.css
2. **No i18n**: Projekt je čisto v angličtine
3. **JWT Auth**: Všetky API endpoints vyžadujú Authorization header
4. **File Processing**: Podporuje multipart upload a download
5. **Production Ready**: Všetko je nasadené a funkčné na tsi.avantle.ai

## Ako Reštartovať Projekt Zajtra

1. **Otvor terminál a prejdi do projektu:**
   ```bash
   cd "C:\Users\rasti\Projects\avantlehq\tsi-ai"
   ```

2. **Spusti development server:**
   ```bash
   pnpm dev
   ```

3. **Otvor v browseri:**
   - Frontend: http://localhost:3001
   - Agent dashboard: http://localhost:3001/agent

4. **Pre microservice (ak potrebné):**
   ```bash
   cd conversion-service
   python main.py
   ```

5. **Skontroluj nameserver status pre tsi.directory**
6. **Ak je ready, vytvor marketing site projekt**

**Next Session Goal**: Vytvoriť TSI Directory marketing site akonáhle budú nameservery zmenené.