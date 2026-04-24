# Graph Report - .  (2026-04-24)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 335 nodes · 457 edges · 22 communities detected
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 39 edges (avg confidence: 0.78)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 35|Community 35]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 39|Community 39]]
- [[_COMMUNITY_Community 40|Community 40]]

## God Nodes (most connected - your core abstractions)
1. `syncUser()` - 18 edges
2. `POST()` - 14 edges
3. `ModernPlayer` - 12 edges
4. `load()` - 11 edges
5. `DELETE()` - 10 edges
6. `run_evaluation()` - 7 edges
7. `VideoThread` - 7 edges
8. `LSTMSummarizer` - 6 edges
9. `fetchComments()` - 5 edges
10. `get_full_video_summary()` - 4 edges

## Surprising Connections (you probably didn't know these)
- `toggleVideo()` --calls--> `DELETE()`  [INFERRED]
  C:\Users\pmish\Desktop\New folder\SWIFTNOTES_\SwiftNotes2.0Web\src\components\notebook\KnowledgeHub.tsx → C:\Users\pmish\Desktop\New folder\SWIFTNOTES_\SwiftNotes2.0Web\src\app\api\delete-snap\route.ts
- `generate_lstm_summary()` --calls--> `load()`  [INFERRED]
  C:\Users\pmish\Desktop\New folder\SWIFTNOTES_\backend2\main.py → C:\Users\pmish\Desktop\New folder\SWIFTNOTES_\SwiftNotes2.0Web\src\app\notebook\[id]\page.tsx
- `run_evaluation()` --calls--> `load()`  [INFERRED]
  C:\Users\pmish\Desktop\New folder\SWIFTNOTES_\backend2\main.py → C:\Users\pmish\Desktop\New folder\SWIFTNOTES_\SwiftNotes2.0Web\src\app\notebook\[id]\page.tsx
- `run_evaluation()` --calls--> `stream_video()`  [INFERRED]
  C:\Users\pmish\Desktop\New folder\SWIFTNOTES_\backend2\main.py → C:\Users\pmish\Desktop\New folder\SWIFTNOTES_\backend2\utils\video_streamer.py
- `Summarizes large transcripts using a Map-Reduce approach.` --uses--> `LSTMSummarizer`  [INFERRED]
  C:\Users\pmish\Desktop\New folder\SWIFTNOTES_\backend2\main.py → C:\Users\pmish\Desktop\New folder\SWIFTNOTES_\backend2\models\lstm_summarizer.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.06
Nodes (9): Framer Motion, toggleVideo(), Lucide React, next-themes, Next.js, Page(), detectMediaType(), PolaroidSnap() (+1 more)

### Community 1 - "Community 1"
Cohesion: 0.05
Nodes (55): Active Recall Formats, AI Cheatsheet, AI Flashcards, Formulae/Code Extraction, AI Mind Map, Context-aware Q&A, AI Summary Tab, AI Synthesis (+47 more)

### Community 2 - "Community 2"
Cohesion: 0.07
Nodes (36): addNotebookComment(), approveEditAccess(), checkNotebookAccess(), createNotebook(), createNotePage(), deleteNotebook(), deleteNotebookComment(), deleteNotePage() (+28 more)

### Community 3 - "Community 3"
Cohesion: 0.08
Nodes (30): AI Sidebar Component, download_video(), extract_video_knowledge(), generate_tab(), MultiAnalysisRequest, PlaylistRequest, safe_remove_file(), SnapshotRequest (+22 more)

### Community 4 - "Community 4"
Cohesion: 0.14
Nodes (5): QThread, QWidget, ModernPlayer, stream_video(), VideoThread

### Community 5 - "Community 5"
Cohesion: 0.13
Nodes (7): PostgreSQL, Prisma, findExe(), POST(), runProcess(), transcribeVideoOffline(), Supabase

### Community 6 - "Community 6"
Cohesion: 0.12
Nodes (17): backend2 (Legacy), BART (Facebook), Custom CNN, CNN Model, Data Generator, Keras, Custom LSTM Summarizer, NLP Inference (+9 more)

### Community 7 - "Community 7"
Cohesion: 0.17
Nodes (10): LSTMSummarizer, generate_lstm_summary(), get_full_video_summary(), Summarizes large transcripts using a Map-Reduce approach., Inference loop for the PyTorch LSTM model., run_evaluation(), clean_transcript_text(), get_clean_transcript() (+2 more)

### Community 8 - "Community 8"
Cohesion: 0.29
Nodes (9): updateNotebookVideoAINotes(), callAI(), context(), fetchTranscriptForVideo(), handleGenerateVideoKnowledge(), handleSelectVideo(), handleSendChat(), handleTabClick() (+1 more)

### Community 9 - "Community 9"
Cohesion: 0.24
Nodes (7): addNotebookVideo(), removeNotebookVideo(), extractVideoId(), fmtTime(), handleAddVideo(), handleRemoveVideo(), handleSnap()

### Community 10 - "Community 10"
Cohesion: 0.25
Nodes (3): list(), Pandas, parse_vtssum_repo()

### Community 30 - "Community 30"
Cohesion: 1.0
Nodes (1): RoomAccessRequest Table

### Community 31 - "Community 31"
Cohesion: 1.0
Nodes (1): UserFavorite Table

### Community 32 - "Community 32"
Cohesion: 1.0
Nodes (1): NotebookVote Table

### Community 33 - "Community 33"
Cohesion: 1.0
Nodes (1): Multiple Learning Styles Support

### Community 34 - "Community 34"
Cohesion: 1.0
Nodes (1): Linear Regression Example

### Community 35 - "Community 35"
Cohesion: 1.0
Nodes (1): Gradient Descent Algorithm

### Community 36 - "Community 36"
Cohesion: 1.0
Nodes (1): Mean Squared Error (MSE)

### Community 37 - "Community 37"
Cohesion: 1.0
Nodes (1): Environment Configuration

### Community 38 - "Community 38"
Cohesion: 1.0
Nodes (1): Python Virtual Environment

### Community 39 - "Community 39"
Cohesion: 1.0
Nodes (1): NPM Package Manager

### Community 40 - "Community 40"
Cohesion: 1.0
Nodes (1): Matplotlib

## Knowledge Gaps
- **1 isolated node(s):** `Removes timestamps, metadata tags, and repetitive fragments      common in YouT`
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 30`** (1 nodes): `RoomAccessRequest Table`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 31`** (1 nodes): `UserFavorite Table`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 32`** (1 nodes): `NotebookVote Table`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 33`** (1 nodes): `Multiple Learning Styles Support`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 34`** (1 nodes): `Linear Regression Example`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 35`** (1 nodes): `Gradient Descent Algorithm`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 36`** (1 nodes): `Mean Squared Error (MSE)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 37`** (1 nodes): `Environment Configuration`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 38`** (1 nodes): `Python Virtual Environment`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 39`** (1 nodes): `NPM Package Manager`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 40`** (1 nodes): `Matplotlib`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `load()` connect `Community 2` to `Community 0`, `Community 10`, `Community 7`?**
  _High betweenness centrality (0.131) - this node is a cross-community bridge._
- **Why does `run_evaluation()` connect `Community 7` to `Community 2`, `Community 4`?**
  _High betweenness centrality (0.090) - this node is a cross-community bridge._
- **Why does `POST()` connect `Community 5` to `Community 8`?**
  _High betweenness centrality (0.062) - this node is a cross-community bridge._
- **What connects `Removes timestamps, metadata tags, and repetitive fragments      common in YouT` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.06 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.05 - nodes in this community are weakly interconnected._
- **Should `Community 2` be split into smaller, more focused modules?**
  _Cohesion score 0.07 - nodes in this community are weakly interconnected._