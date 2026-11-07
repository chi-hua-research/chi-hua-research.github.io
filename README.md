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
