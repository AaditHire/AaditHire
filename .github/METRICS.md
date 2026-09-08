# Profile Metrics

The official `lowlighter/metrics@latest` action produces `github-metrics.svg` and `github-contributions.svg`. The profile uses the built-in **Classic** template, its header, and **Isocalendar** (full year). Repository statistics and **Languages** (five most-used languages) are configured to activate when `METRICS_TOKEN` is supplied. No custom CSS, presets, or homemade SVG renderer is used.

The built-in `github.token` successfully renders the profile header and full-year calendar. It is repository-scoped: testing showed it reported only the profile repository and its JavaScript, rather than the account's public portfolio. The workflow therefore omits repository statistics and languages until `METRICS_TOKEN` is present. It never presents that partial result as account-wide statistics.

To enable the configured repository and language sections, create a **classic personal access token with no scopes selected**, following the official Metrics setup guide below. Save it as **METRICS_TOKEN** under [this repository's Actions secrets](https://github.com/AaditHire/AaditHire/settings/secrets/actions), then run **GitHub Metrics** manually. Do not paste the token into chat or commit it. Public data needs no `repo`, `public_repo`, organization, or private-data scopes. Metrics reads using this token and commits using the built-in `github.token` with `contents: write`.

Daily refresh: **03:23 UTC / 08:53 Asia/Kolkata**. Manual refresh: **Actions → GitHub Metrics → Run workflow**. It also runs when its workflow file changes on `main`. Generated image commits do not match the push path filter, preventing a loop. Runs are serialized; commits use Metrics' standard output behavior. Timezone is `Asia/Kolkata`, optimizations are the documented `css, xml`, and animations are disabled for a calm, motion-safe presentation. Failed plugin renders fail the run rather than intentionally publishing an error graphic.

References reviewed:

- [Official Action setup](https://github.com/lowlighter/metrics/blob/latest/.github/readme/partials/documentation/setup/action.md)
- [Classic template and example](https://github.com/lowlighter/metrics/tree/latest/source/templates/classic)
- [Languages options and examples](https://github.com/lowlighter/metrics/tree/latest/source/plugins/languages)
- [Full-year isometric calendar](https://github.com/lowlighter/metrics/tree/latest/source/plugins/isocalendar)
- [Coding habits](https://github.com/lowlighter/metrics/tree/latest/source/plugins/habits) was reviewed and omitted to keep the profile short.
- [Presets](https://github.com/lowlighter/metrics/tree/presets) were reviewed; the built-in Classic appearance was preferred over extra styling.

GitHub may delay scheduled runs or disable schedules after prolonged inactivity. If a future Metrics release changes token requirements, consult the official setup guide before broadening permissions.
