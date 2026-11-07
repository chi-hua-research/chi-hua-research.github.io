# Chi-Hua Research

A Quarto academic research notebook for statistics, machine learning, and decision science.

Expected URL: https://chi-hua-research.github.io/

## Local development

Install [Quarto 1.8.27](https://github.com/quarto-dev/quarto-cli/releases/tag/v1.8.27), matching CI. No additional language packages or secrets are needed.

```sh
quarto preview --host 0.0.0.0 --port 4200 --no-browser
quarto render
```

The preview command keeps running; render is a separate production build command. Generated `_site/` and `.quarto/` files are ignored. Use the existing checkout in cloud tasks; no separate worktree is required.

## Content

- `index.qmd`: home
- `about.qmd`: notebook description
- `research-notes/`, `technical-notes/`, `research-journal/`: listing pages and article folders
- `_quarto.yml`: navigation, search, themes, MathJax, root site URL
- `styles.css`: responsive typography
- `assets/mathjax/`: MathJax 3.2.2 and fonts, bundled locally with its Apache-2.0 license

Add an article as `<section>/<slug>/index.qmd` with `title`, `date`, `description`, and `categories` in YAML front matter. The section listing and RSS feed update on render. Use `#prp-...`, `#thm-...`, and `#lem-...` blocks for propositions, theorems, and lemmas, and `@prp-...` cross-references. Long articles inherit a table of contents. Code fences are displayed without executing a notebook runtime.

All three initial articles are illustrative demonstrations, not completed research or published findings. Replace or extend them with your own notes as appropriate.

## Deployment

In GitHub **Settings → Pages → Build and deployment**, select **GitHub Actions** as the source. Merge changes into `main` (or push to `main`) to trigger `.github/workflows/publish.yml`. Pull requests run the build without deploying. The workflow installs the pinned Quarto version, renders, uploads the official Pages artifact, and deploys with the official Pages action. Only the deployment job receives `pages: write` and `id-token: write`.

No project subdirectory or custom domain is configured. If the repository has Pages environment protection rules, allow deployments from `main`. The Actions run must succeed before the live URL can be considered deployed.

## Bilingual editions / 中英文同步維護

The root URL is a language selector. English lives at `/en/` and Traditional Chinese at `/zh/`. All eight pages use the same relative path in both directories; each page links directly to its counterpart. Locale projects have separate navigation, search indexes, categories and RSS feeds. Original English URLs redirect to their new locations.

Run `quarto render` **from the repository root** to check translations, render the entry page, render both language projects and generate compatibility redirects. Do not publish a locale-only render. For local browsing after building, run `python3 -m http.server 4200 --directory _site`. Generated files stay ignored.

### Updating an article

1. Edit the matching `.qmd` files in both `en/` and `zh/`. New pages must use the same relative path. Keep dates, mathematical display equations, theorem labels and code consistent.
2. Review both versions for meaning, mathematical correctness and terminology. Automation does not evaluate translation quality.
3. Run `python3 scripts/check-translations.py --record` to record the reviewed pair hashes in `translations.json`. This rejects edits affecting only one edition.
4. Run `quarto render`, then commit both editions and the manifest together.

The pre-render guard runs locally and in the existing GitHub Actions workflow. A missing counterpart, unrecorded edit, differing date/formula/code/theorem label, or one-sided update prevents publication. Do not regenerate the manifest as a substitute for translation review. Both languages deploy in one Pages artifact, so neither can publish ahead of the other.

中文版：每次修改文章時，請一起更新 `en/` 與 `zh/` 的對應檔案，校對語意後執行 `python3 scripts/check-translations.py --record`，再從根目錄執行 `quarto render`。只改單邊、漏譯或未更新校對紀錄都會使建置失敗。自動檢查可防止版本遺漏，但翻譯語意仍須人工校對。

Verification commands: `python3 scripts/test-translations.py`, `quarto render`, and `python3 scripts/check-site.py`. These also run in CI.
