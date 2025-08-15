# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Jekyll-based static website project exploring the "Post-Database Era" - analyzing trends in database technology and industry evolution. The site is automatically deployed to GitHub Pages via GitHub Actions.

## Key Development Commands

### Jekyll Site Development
```bash
# Install Jekyll dependencies (after creating Gemfile)
bundle install

# Run local development server with auto-reload
bundle exec jekyll serve --livereload

# Build the static site for production
bundle exec jekyll build

# Clean Jekyll cache and generated files
bundle exec jekyll clean
```

### Deployment
- Push to `main` branch triggers automatic deployment via GitHub Actions
- The workflow file is located at `.github/workflows/jekyll-gh-pages.yml`
- No manual deployment needed - GitHub Actions handles everything

## Architecture and Project Structure

### Current Research Focus
The project analyzes database industry trends across five key areas:
1. **Bespoke DB Era Trends** - Multi-model vs single-purpose databases
2. **Storage Infrastructure** - S3-compatible APIs, Iceberg tables
3. **Access Pattern Consolidation** - Unified APIs for SQL, KV, Document, Graph, Search
4. **Syntax Homogenization** - ISO GQL, SQL:2023, JSONPath standards
5. **Interoperability Layers** - Query engines like Trino, DuckDB, DataFusion

### Jekyll Site Structure (to be implemented)
- `_config.yml` - Site configuration (title, theme, plugins)
- `_posts/` - Blog posts in Markdown format (YYYY-MM-DD-title.md)
- `_layouts/` - Page templates
- `_includes/` - Reusable components
- `assets/` - CSS, JS, images
- `index.md` - Homepage
- `_data/` - Structured data files (YAML, JSON, CSV)

### GitHub Pages Integration
- Deployment is automated via `.github/workflows/jekyll-gh-pages.yml`
- The site builds from the root directory
- Uses GitHub Pages environment for deployment
- Available at GitHub Pages URL after deployment

## Important Implementation Notes

### When Creating Jekyll Content
- Posts must follow naming convention: `YYYY-MM-DD-title.md`
- Include front matter in all Markdown files:
  ```yaml
  ---
  layout: post
  title: "Title Here"
  date: YYYY-MM-DD
  categories: [category1, category2]
  ---
  ```
- Use relative URLs for internal links
- Place images in `assets/images/`

### When Setting Up Jekyll
- The `Gemfile` should include:
  - `gem "jekyll"`
  - `gem "github-pages", group: :jekyll_plugins` (for GitHub Pages compatibility)
- The `_config.yml` should specify:
  - Site title and description
  - URL and baseurl settings
  - Theme selection
  - Plugin configuration

### Research Content Organization
- Convert research outline from `research/outline_2025-08-15.txt` into structured posts
- Consider creating category pages for each major trend area
- Use Jekyll collections for organizing in-depth analysis pieces