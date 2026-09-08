# GitHub visuals

`github-visuals.mjs` is an original, dependency-free Node.js 22 generator. It creates dark/light stats and animated contribution-racer SVGs plus a public-data snapshot in `output/`. Existing resume files under `output/pdf/` are never staged by the workflow.

## Data and measurement

- With `GITHUB_TOKEN`, the calendar comes from GitHub's GraphQL `contributionCalendar`. Without a token, local generation reads GitHub's public contribution HTML and matches day cells to their count tooltips. HTML is not a stable API: the parser rejects missing counts, missing dates, and unexpected calendar lengths.
- Repository data comes from the paginated public user repositories REST endpoint. Repositories and stars exclude forks and private repositories. Top languages count the **primary language of each public, owned, non-fork repository**; they are not code-byte percentages or skill scores.
- Contributions cover the exact displayed date range. GitHub decides which contributions appear, including anonymized private contributions if the account shares them. No private repository names are collected.
- Each graphic shows an update date. Failed requests leave existing assets intact instead of publishing invented or zero-filled data. Committed initial assets mean the README works before the first scheduled run.

## Renderer choice and sources

Inspected [Platane/snk](https://github.com/Platane/snk), its [SVG renderer](https://github.com/Platane/snk/blob/main/packages/svg-creator/index.ts), [generation pipeline](https://github.com/Platane/snk/blob/main/packages/generate-snake-animation/generateSnakeAnimation.ts), and [GitHub collector](https://github.com/Platane/snk/blob/main/packages/github-user-contribution/index.ts). Its solver and renderer consume contribution cells. This profile instead uses an original column-by-column serpentine route, keeping every real cell visible and returning outside the calendar. No upstream source was copied or vendored; no upstream license assumptions are needed.

An original top-down car travels through CSS transform keyframes. Its turquoise trail and brief yellow active-cell highlights share a distance-based timeline. There is no JavaScript, external font, remote image, `foreignObject`, or SVG motion-path dependency. Reduced motion disables all animation; the car remains at the start. Theme selection uses GitHub's supported `<picture>` markup. Local browser tests verify motion, but final hosted GitHub behavior is checked after publication in the polish stage.

References: [GitHub token permissions](https://docs.github.com/en/actions/tutorials/authenticate-with-github_token), [repository REST API](https://docs.github.com/en/rest/repos/repos#list-repositories-for-a-user), [theme-specific images](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/about-images#specifying-the-theme-an-image-is-shown-to).

## Run and update

```sh
node --test scripts/github-visuals.test.mjs
node scripts/github-visuals.mjs
# Re-render the saved public snapshot without network requests:
node scripts/github-visuals.mjs --snapshot output/github-activity.json
```

`GITHUB_USER` defaults to `AaditHire`. Never put a token in a command argument or commit it. `.github/workflows/contribution-racer.yml` uses the built-in `GITHUB_TOKEN`, requires only `contents: write`, and runs daily at 03:23 UTC or through **Actions → Refresh GitHub visuals → Run workflow**. Changes to the generator/workflow also trigger it on `main`. Third-party actions are pinned to verified commit SHAs.

Only the five named generated files are committed. Concurrent refreshes are serialized; pushes are never forced. Branch rules that prohibit bot writes will cause the run to fail visibly. Scheduled runs begin only after this workflow is published to the default branch; GitHub may delay schedules or disable them after extended inactivity in a public repository.
