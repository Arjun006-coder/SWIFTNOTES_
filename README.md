# SwiftNotes 2.0 (Main README)

This repository contains the full SwiftNotes stack:
- `SwiftNotes2.0Web`: Next.js web app (UI, auth, notebook editor, API routes, Supabase integration)
- `SwiftNotes2.0Backend`: FastAPI service for heavy YouTube/video AI processing
- `backend2`: legacy experimental backend (pre-Gemini prototype work)

## Project Structure

```text
swiftnotesmain/
|- SwiftNotes2.0Web/       # Frontend + Next.js server routes
|- SwiftNotes2.0Backend/   # Python FastAPI backend
|- backend2/               # Legacy experiment backend (prototype models/pipelines)
|- README.md               # This file
```


## Problem Statement (PS)

Traditional digital note-taking for students is fragmented. Learners typically switch between:
- a video player for lectures
- a notes app for writing
- screenshots for diagrams in gallery
- separate AI tools for summaries/explanations

This context switching creates the core pain points:
- Cognitive overload while trying to track lecture flow and notes together
- Lost context about why a note was taken at a specific video moment
- Static notes that are disconnected from source media
- Limited structured community sharing/collaboration around high-quality notes

## Solution Theory (How SwiftNotes Solves It)

SwiftNotes is designed as an all-in-one, multi-modal learning workspace that converts passive watching into active study.

High-level theory:
1. Ingest lecture media (video/audio/frames) from YouTube.
2. Run multi-modal AI analysis over content.
3. Convert raw lecture content into study artifacts (summary, cheatsheet, formulae, flashcards, mind map).
4. Anchor notes/snaps to exact timestamps so context is never lost.
5. Add collaborative and community layers so knowledge is reusable, discussable, and scalable.

Pipeline model (from your PPT):
1. Phase 1 (Ingestion): backend extracts and processes stream data.
2. Phase 2 (Synthesis): AI generates structured learning outputs.
3. Semantic retrieval: tag-aware search improves discoverability beyond exact keyword matching.

## How It Helps Learners

- Reduces tab switching and mental overhead by keeping lecture + notes + AI in one flow.
- Improves retention using active-recall formats (flashcards, Q&A, cheatsheets).
- Preserves context with timestamp-linked snaps connected to exact lecture moments.
- Supports different learning styles (typing, drawing, visual mapping, summary-first revision).
- Enables collaborative learning with live shared study spaces.

## Core Features

- Integrated video + note workspace (single screen study flow)
- Timestamp-linked video snaps ("Polaroid Snaps")
- Digital ink and canvas support for drawing/handwritten notes
- AI analysis tabs:
  - Summary
  - Formulae/code extraction
  - Cheatsheet
  - Flashcards
  - Mind map
  - Context-aware Q&A
- Community knowledge hub with tags, upvotes, and comments
- Live OTP-based study/collaboration rooms

## What Is Unique

- Multi-modal learning loop in one product: capture -> analyze -> revise -> collaborate.
- Strong context preservation: notes and snaps are linked to exact lecture timepoints.
- Structured AI outputs are generated as study-ready assets, not just generic chat responses.
- Community + creator direction: roadmap includes adaptive revision planning and verified creator monetization.

## What Is Implemented

- Notebook creation, page editing, drawing, and snap images
- Clerk authentication + user sync into Supabase
- Community notebook feed with tags, voting, bookmarks, comments
- OTP-based notebook access flow and collaboration permissions
- AI features (Gemini) for Q&A, summaries, cheatsheets, flashcards, theory, mind map, semantic tags
- YouTube transcript pipeline with fallback transcription via Groq Whisper
- Video snapshot extraction and playlist intelligence (via backend endpoints)


## Legacy Experimental Backend (`backend2`)

- `backend2` contains earlier experimentation done before the current Gemini-key-based backend workflow.
- It includes custom summarization and vision prototypes (BART pipeline, custom LSTM summarizer, custom CNN + YOLO player, transcript cleaning, and dataset prep scripts).
- Results were not reliable enough for production quality (repetitive/noisy summaries and weak custom LSTM generation), so the project switched to the Gemini-driven implementation in `SwiftNotes2.0Backend`.
- See `backend2/README.md` for full details of scripts and artifacts.



## Tech Stack

- Frontend: Next.js (App Router), React, Tailwind CSS, Framer Motion
- Auth: Clerk
- Database: Supabase (PostgreSQL)
- AI (Web + Backend): Google Gemini (`gemini-2.5-flash`)
- Transcript fallback: Groq Whisper
- Backend API: FastAPI + Uvicorn + `yt-dlp`

## Prerequisites

- Node.js 20+ and npm
- Python 3.11+ (3.12 recommended)
- A Supabase project
- A Clerk project
- `ffmpeg` and `yt-dlp` available on system `PATH` (required for snapshot/playlist flows)

Optional:
- Ollama (`gemma:2b`) for local planner flow

## 1) Clone With Backend Submodule

```bash
git clone --recurse-submodules <repo-url>
cd swiftnotesmain
```

If already cloned without submodules:

```bash
git submodule update --init --recursive
```

## 2) Backend Setup (`SwiftNotes2.0Backend`)

```bash
cd SwiftNotes2.0Backend
python -m venv .venv
```

Activate venv:

- Windows PowerShell:
  ```bash
  .\.venv\Scripts\Activate.ps1
  ```
- macOS/Linux:
  ```bash
  source .venv/bin/activate
  ```

Install deps:

```bash
pip install -r requirements.txt
```

Create `SwiftNotes2.0Backend/.env`:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Run backend locally:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

Backend API endpoints:
- `POST /extract`
- `POST /snapshot`
- `POST /playlist-info`
- `POST /multi-video-analysis`

## 3) Frontend Setup (`SwiftNotes2.0Web`)

```bash
cd ../SwiftNotes2.0Web
npm install
```

Create `SwiftNotes2.0Web/.env.local`:

```env
# Clerk
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_...
CLERK_SECRET_KEY=sk_...
NEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in
NEXT_PUBLIC_CLERK_SIGN_UP_URL=/sign-up

# Supabase
NEXT_PUBLIC_SUPABASE_URL=https://<project>.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=ey...
SUPABASE_SERVICE_ROLE_KEY=ey...

# AI keys
GEMINI_API_KEY=...
GROQ_API_KEY=...                 # Optional, enables transcript fallback in /api/youtube

# Collaboration
LIVEBLOCKS_SECRET_KEY=sk_...     # Optional but recommended for live collaboration auth

# Prisma (needed only if you run Prisma commands)
DATABASE_URL=postgresql://...
DIRECT_URL=postgresql://...
```

Initialize database objects in Supabase SQL editor (from `SwiftNotes2.0Web`):

1. `supabase_setup.sql`
2. `supabase_migrations.sql`
3. `supabase_migrations_v2.sql`

Run frontend:

```bash
npm run dev
```

Open: `http://localhost:3000`

## Integration Notes

- The codebase currently mixes local backend calls and hardcoded remote ngrok URLs.
- Local proxy route exists at:
  - `SwiftNotes2.0Web/src/app/api/generate-video-knowledge/route.ts` -> `http://127.0.0.1:8000/extract`
- Some UI components call a hardcoded remote backend directly:
  - `SwiftNotes2.0Web/src/components/notebook/AISidebar.tsx`
  - `SwiftNotes2.0Web/src/components/notebook/KnowledgeHub.tsx`
  - `SwiftNotes2.0Web/src/components/notebook/VideoPanel.tsx`

If you want a fully local setup, replace those hardcoded URLs with your local backend base URL.

## Backend Docker (Optional)

From `SwiftNotes2.0Backend`:

```bash
docker build -t swiftnotes-backend .
docker run --env-file .env -p 8080:8080 swiftnotes-backend
```

## Troubleshooting

- `GEMINI_API_KEY not found` in backend: ensure `SwiftNotes2.0Backend/.env` exists and server restarted.
- Transcript fallback failing: set `GROQ_API_KEY` and verify internet access.
- Snapshot extraction failing: confirm both `yt-dlp` and `ffmpeg` are installed and available in `PATH`.
- Supabase errors: verify `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, and `SUPABASE_SERVICE_ROLE_KEY`.
- Planner returns mock response: `GEMINI_API_KEY` missing for `generate-plan` route.
