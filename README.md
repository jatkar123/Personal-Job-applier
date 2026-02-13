# Personal Job Applier

A practical blueprint to build a **resume-aware job discovery and assisted-application system** with two human checkpoints.

## 1) Goals and guardrails

### Primary goals
- Ingest your **latest resume** as the source of truth.
- Periodically discover relevant roles from job sources (LinkedIn, Xing, StepStone, Glassdoor, and others where legally/technically possible).
- Provide a **Human Intervention 1** review queue where you select jobs to proceed with.
- Create a **job-tailored ATS-friendly resume** only for selected jobs.
- Provide a **Human Intervention 2** output package: direct apply links + tailored resume so you can complete application forms manually.

### Guardrails
- Follow each website's Terms of Service and robots/policy constraints.
- Prefer official APIs, RSS feeds, partner feeds, and compliant aggregators over brittle scraping.
- Keep personal data encrypted at rest and in transit.

---

## 2) Recommended architecture (hosted from GitHub)

Build this as a modular service with GitHub as source control + CI/CD + deployment workflow.

### Components
1. **Resume Intake Service**
   - Upload latest resume (PDF/DOCX/Markdown).
   - Parse and normalize into a structured profile (skills, years, domain, location, visa/work auth, languages).

2. **Job Ingestion Service**
   - Poll connectors on schedule (e.g., every 6h).
   - Connectors per source: LinkedIn/Xing/StepStone/Glassdoor/other boards.
   - Store raw jobs + normalized schema.

3. **Matching & Ranking Engine**
   - Compute semantic + rule-based fit score.
   - Add “growth leeway” score (slightly underqualified but high upside roles).
   - Filter duplicates and stale roles.

4. **Human Review UI (Intervention 1)**
   - Dashboard listing ranked jobs.
   - Buttons: `Approve`, `Reject`, `Save for later`.

5. **Resume Tailoring Service**
   - Generate ATS-optimized resume variant per approved job.
   - Keep claims truthful; no fabricated experience.
   - Produce output files (PDF + DOCX + plain text).

6. **Application Packet Generator (Intervention 2)**
   - For approved jobs, generate:
     - job title/company/link
     - tailored resume file
     - key highlights for manual form filling
   - Send digest via email/Slack/Telegram + show in dashboard.

7. **Scheduler + Orchestrator**
   - Trigger discovery, scoring, and notifications at fixed intervals.

8. **Data Store + Audit Trail**
   - Persist resume versions, jobs, scores, decisions, and generated documents.

---

## 3) Tech stack recommendation

### Backend
- **Python + FastAPI** for APIs and orchestration-friendly services.
- **Celery** (or Dramatiq) for async jobs.
- **Redis** for task queue/cache.
- **PostgreSQL** for persistent data.

### AI/NLP
- Embeddings + reranking for semantic role matching.
- LLM prompt pipelines for resume tailoring and summary generation.
- Optional: spaCy for deterministic skill/entity extraction.

### Scraping / Integrations
- **Playwright** for browser automation where needed.
- **httpx + BeautifulSoup** for lightweight extraction.
- Prefer APIs/feeds first; scraping only where permitted.

### Frontend
- **Next.js** (or React + Vite) for dashboard.
- Tailwind CSS for quick UI iteration.

### Storage / Files
- Resume/document storage on **S3-compatible bucket**.
- Signed URLs for secure download.

### DevOps / Hosting from GitHub
- **GitHub Actions** for CI/CD.
- Deploy backend to **Render / Fly.io / Railway / AWS ECS**.
- Deploy frontend to **Vercel / Netlify**.
- Secrets via GitHub Encrypted Secrets + host secret manager.

---

## 4) Step-by-step implementation plan

### Phase 0 — Repository and baseline setup
1. Create GitHub repo structure:
   - `apps/api`
   - `apps/web`
   - `workers`
   - `infra`
   - `docs`
2. Add branch protections + PR checks.
3. Add `.env.example` with required env vars.
4. Add Docker Compose for local stack (Postgres, Redis, API, worker).

### Phase 1 — Data model and persistence
1. Create tables:
   - `resume_versions`
   - `candidate_profile`
   - `job_sources`
   - `jobs_raw`
   - `jobs_normalized`
   - `job_scores`
   - `job_decisions`
   - `tailored_resumes`
2. Implement migrations and indexes (company, location, posted_at, hash).
3. Add dedupe key: `source + external_job_id` or normalized URL hash.

### Phase 2 — Resume intake and profile extraction
1. Build secure resume upload endpoint.
2. Parse document to text.
3. Extract candidate profile (skills, role families, seniority, geography).
4. Store structured profile + original resume version.
5. Add endpoint to set one version as active.

### Phase 3 — Job ingestion at intervals
1. Add scheduler (every 6h to start).
2. Implement source connectors (start with 1–2 easiest/most compliant sources).
3. Normalize job fields (title, company, location, salary, tech tags, apply URL, posted date).
4. Persist raw + normalized records.
5. Add failure retry and source health metrics.

### Phase 4 — Matching with growth leeway
1. Compute baseline relevance:
   - title similarity
   - skill overlap
   - location/work model match
   - seniority alignment
2. Add growth leeway logic:
   - allow missing up to N priority skills
   - promote jobs with strong domain adjacency
3. Produce final score + reason codes.
4. Expose ranked list API for UI.

### Phase 5 — Human Intervention 1 (selection UI)
1. Build dashboard table/cards with filters.
2. Show explainability snippet (why matched).
3. Let user mark `Apply / Skip / Maybe`.
4. Save decisions and timestamps.

### Phase 6 — Tailored ATS resume generation
1. Trigger only on `Apply` decisions.
2. Generate per-job resume variants:
   - rewrite summary to match role keywords
   - reorder bullet points by relevance
   - keep factual integrity
3. Run ATS checks:
   - keyword coverage
   - section structure
   - plain-text readability
4. Export PDF + DOCX + TXT.

### Phase 7 — Human Intervention 2 packet output
1. Create “application packet” page + downloadable bundle.
2. Include:
   - apply URL
   - tailored resume
   - short talking points for form text fields
3. Send periodic digest (daily/instant) with latest approved jobs.

### Phase 8 — Hosting and productionization
1. Set up GitHub Actions workflows:
   - lint/test on PR
   - build and deploy on main
2. Deploy services and configure domain.
3. Add observability:
   - logs
   - error tracking
   - job metrics dashboard
4. Add backup/restore for DB and document store.

---

## 5) Suggested MVP delivery order (4 weeks)

- **Week 1**: Resume intake, profile extraction, schema, one job source.
- **Week 2**: Matching/ranking + intervention UI.
- **Week 3**: Resume tailoring + packet generation.
- **Week 4**: CI/CD, monitoring, hardening, and UX polish.

---

## 6) Practical compliance and reliability checklist

- Respect source TOS and legal constraints per connector.
- Add rate limiting + backoff for external requests.
- Keep PII encrypted and access-controlled.
- Add manual override for all automated decisions.
- Log every transformation for auditability.

---

## 7) Future extensions

- Auto-fill forms on supported sites with approved confirmation gate.
- Cover letter personalization per role.
- Multi-language resume generation.
- Interview prep packets from selected job descriptions.

---

## 8) Minimal first release definition

An acceptable first release is:
1. Upload latest resume.
2. Pull jobs from at least one compliant source on schedule.
3. Rank jobs with growth leeway.
4. Let you select jobs manually (Intervention 1).
5. Generate tailored ATS resume variants for selected jobs.
6. Provide apply links + files for manual completion (Intervention 2).

This gives immediate value while keeping full-automation (form filling and one-click apply) as a future phase.
