# 🧠 AI Deep Dive Instructions (AI 深度日报)

> **INPUT**: JSON object with `newsletter_picks`, `huggingface_papers`, and optional `x_fixed_ai_accounts`, `ai_podcasts`, `ai_official_blogs` sections.
> **OUTPUT**: A deep-dive AI report focusing on research, industry analysis, and key tech updates.

---

## 🎯 Focus Areas
1.  **SOTA Research**: Deep analysis of top papers from Hugging Face. Focus on methodology and results.
2.  **Industry Analysis**: Strategic insights from top AI newsletters (ChinAI, Memia, etc.).
3.  **X Fixed AI Builders**: Today's AI-relevant posts from the fixed builder list in `instructions/x_ai_accounts.txt`.
4.  **Long-form AI Signals**: AI podcasts from `instructions/ai_podcasts.txt` and official blog posts from `instructions/ai_official_blogs.txt`.

## ⚠️ Anti-Laziness Protocol
1.  **Volume**: Output MUST contain at least **15 items** across all sections.
2.  **Depth**: For papers and newsletters, provide **2-3 bullet points** of analysis (Why it matters, Key takeaway).
3.  **Logged-in sources cannot be silently skipped**: if X or any other required logged-in source lands on login / QR / verification flow, stop and wait for the user to restore the session. Do not mark it as a normal data gap and do not switch to an anonymous replacement route.
4.  **X route is fixed-list only**: do not use `Following`, `For you`, anonymous search, or recommended feeds as substitutes. Check the account list directly and keep only posts from the last 24 hours unless the user asks for a wider window.
5.  **Long-form sources have a wider window**: podcasts use a default 14-day lookback. Do not force podcasts into a 24-hour news window, and do not pad the report when there are no new episodes.
6.  **Substance filter**: skip mundane personal posts, retweets without commentary, event pleasantries, engagement bait, and pure promotion. Keep original opinions, product announcements, technical discussions, industry analysis, and lessons from builders.

## 📝 Report Structure

### Part 1: 🔬 SOTA Research (Hugging Face Papers)
*   **Data Source**: Hugging Face Daily Papers
*   **Format**:
    ```markdown
    #### 1. [Title (Translated)](url)
    - **Source**: Hugging Face Papers | **Time**: Today
    - **Summary**: One sentence summary of the paper's contribution.
    - **Deep Dive**:
        *   **Innovation**: Key technical novelty (e.g., "New attention mechanism").
        *   **Impact**: Potential applications or performance gains.
    ```

### Part 2: 📧 Industry Insights (Newsletters)
*   **Data Source**: AI Newsletters (ChinAI, Memia, etc.)
*   **Focus**: Strategic shifts, policy changes, major product launches.
*   **Format**:
    ```markdown
    #### 1. [Title (Translated)](url)
    - **Source**: Newsletter Name | **Time**: X hours ago
    - **Summary**: Concise overview of the newsletter topic.
    - **Insight**: 💡 Strategic implication or key takeaway.
    ```

### Part 3: 🐦 X Fixed AI Builders
*   **Data Source**: `instructions/x_ai_accounts.txt`, fetched with an authenticated X browser session or an equivalent login-capable browser tool.
*   **Default Accounts**: the 25-builder list in `instructions/x_ai_accounts.txt`, based on the follow-builders source baseline.
*   **Focus**: model releases, research commentary, product launches, demos, developer tools, benchmarks, infrastructure, safety, and industry strategy.
*   **Selection**: rank posts by recency, AI relevance, and combined engagement signals across replies / reposts / likes / views / bookmarks. Do not rank by likes alone.
*   **Format**:
    ```markdown
    #### 1. [Post title or concise translated topic](status_url)
    - **Source**: X Fixed AI Builders / @handle | **Time**: ISO or relative time | **Heat**: engagement signals when available
    - **Summary**: What happened, grounded in the post and linked source if present.
    - **Deep Dive**: Why it matters for AI products, research, infrastructure, or market direction.
    ```

### Part 4: 🎙️ AI Podcasts
*   **Data Source**: `instructions/ai_podcasts.txt`.
*   **Default Window**: last 14 days.
*   **Focus**: counterintuitive insights, technical direction, builder lessons, company strategy, model capability shifts, and practical implications.
*   **Format**:
    ```markdown
    #### 1. [Podcast Name: Episode Title](episode_url)
    - **Source**: Podcast | **Time**: Published date
    - **The Takeaway**: One sentence with the most important point.
    - **Context**: Who is speaking and why this matters.
    - **Deep Dive**: 2-3 bullets with concrete insights, not generic "they discussed" filler.
    ```

### Part 5: 🏢 AI Official Blogs
*   **Data Source**: `instructions/ai_official_blogs.txt`.
*   **Focus**: product announcements, engineering deep dives, API/capability changes, research findings, benchmarks, and deployment guidance.
*   **Format**:
    ```markdown
    #### 1. [Blog Name: Article Title](article_url)
    - **Source**: Official Blog | **Time**: Published date if available
    - **Summary**: Lead with the core announcement, finding, or capability change.
    - **Deep Dive**: Practical implication for builders, developers, AI products, or market direction.
    ```
