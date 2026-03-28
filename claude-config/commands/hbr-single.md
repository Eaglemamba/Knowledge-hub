# HBR Single Article Processor

The user will paste one HBR article text below.

1. Read the v1.6 AI Expert Learning System prompt from `system_prompt.xml` in the project root.
2. Generate a complete educational HTML document following the full v1.6 document structure: dashboard_meta, header, executive_summary with Rating Bar, learning_objectives, framework_visual (if applicable), content_sections, key_takeaways, practice (accordion), bottom_line, and footer.
3. Use the `YYYY-MM-DD_short-title.html` naming convention from the doc-file meta tag.
4. Save the HTML file to the `docs/` folder.
5. **Update `docs/index.html`**: Read the existing `index.html`, find the `const articles = [` array, and append a new entry for this article with `file`, `title`, `source`, `date`, `tags`, `rating`, and `summary` fields — matching the format of existing entries. Place the new entry at the end of the array.
6. Stage all changed files (new HTML + updated index.html), commit with message "Add [title] - YYYY-MM-DD", and push to GitHub.

Skip the score confirmation step -- always proceed with generation regardless of rating.

$ARGUMENTS
