---
name: prototype-output-skill
description: Build or revise a high-fidelity HTML prototype by starting from a real backend/product page instead of redrawing from scratch. Use when the user provides an existing admin/internal page URL, an authenticated browser page, or a local HTML snapshot and wants the agent to capture the runtime DOM/CSS, preserve the live product shell and component language, apply requirement changes on top, desensitize data, and export a shareable standalone HTML prototype.
---

# 原型输出 Skill

Treat the task as a product iteration on a live page, not a blank-page design exercise.

## Workflow

1. Read the real page first.
2. Extract runtime DOM, computed styles, visible screenshots, and asset sources before editing.
3. Build a component provenance map that proves which live selectors/classes/assets each prototype region reuses.
4. Reuse the live shell, component hierarchy, copy style, and interaction pattern unless the requirement explicitly changes them.
5. Apply requirement changes at the right product layer.
6. Desensitize all sensitive data before handoff.
7. Export a standalone shareable HTML, then pass the provenance, visual, and source gates before final handoff.

Hard rule: do not hand off a prototype that cannot prove it came from the live runtime DOM. A visually plausible redraw is a failed output.

## Read the Real Page

- Prefer the user's current logged-in browser/session for internal pages.
- Use the current page/tab the user already opened when possible.
- Do not start from screenshots alone.
- Do not rebuild generic banners, sidebars, tabs, cards, or tables from memory when the live page already has them.
- Do not replace live logos, menu icons, button systems, tabs, tables, or shell regions with hand-drawn approximations. Extract the live asset or component contract first.

For modern bundled apps, static entry HTML is not enough. The rendered runtime DOM is the source of truth.

## Capture Before Editing

Save artifacts inside one requirement folder:

- `<需求目录>/过程文件/`
  - `live-runtime-dom.html`: rendered `document.documentElement.outerHTML`, not the static entry HTML.
  - `live-screenshot.png`: screenshot of the source page at the relevant viewport.
  - `computed-style.json`: measured styles for header, sidebar, tabs, buttons, cards, tables, inputs, and any reused component.
  - `asset-inventory.json` or `asset-inventory.md`: live logos, menu icons, SVGs, images, and chart assets with their selectors/URLs/data URIs.
  - `provenance-map.md`: mapping from each final prototype region to live selectors/classes/assets.
  - `visual-review.md`: source screenshot vs prototype screenshot checklist with mismatches and fixes.
  - optional generator / patch script if the page is large and repeated edits are likely.
- `<需求目录>/原型与示意图/`
  - editable prototype HTML
  - final shareable standalone HTML if different from the editable one

Before modifying anything, capture:

- current page shell: top bar, side nav, tabs, breadcrumb, footer
- card layout and metric blocks
- table header model, grouped headers, fixed columns, action column
- current interactions: expand/collapse, drill-down, filters, date selectors, target setting, export, action buttons
- real field names and current copy style

## Provenance Gate

Before coding feature changes, create `provenance-map.md`. Every shell or reused component in the final prototype must have a live source.

Required rows:

| Prototype region | Live selector/class | Live asset source | Captured style facts | Final implementation |
| --- | --- | --- | --- | --- |
| Header/banner | e.g. `#main_header`, `.semi-layout-header` | logo/avatar/icon URL or data URI | height, padding, background, typography | selector/class/inline asset used |
| Sidebar/navigation | e.g. `.semi-navigation`, `.layout-sider` | menu SVGs/icons | width, row height, active state, indent | selector/class/inline assets used |
| Top tabs | e.g. `.tabs-tab`, `[role=tab]` | underline/icon if any | height, spacing, active color | selector/class used |
| Buttons/toolbars | e.g. `.button-primary` | icon source if any | height, padding, color, radius | selector/class used |
| Cards/tables/forms | live component selector | image/icon source if any | density, borders, headers, pagination | selector/class used |

No provenance means no handoff. If a region is intentionally redesigned, write the reason in the map and still inherit the closest live component language.

Mandatory source checks on the final HTML:

- It includes the live shell's key selectors/classes for header, sidebar, tabs, and buttons, when those existed in the source page.
- Logos and navigation icons come from live DOM assets or approved neutral placeholders, not ad hoc drawings.
- Header/sidebar/tab/button dimensions match captured computed styles unless the requirement explicitly changes them.
- There are no unexpected generic replacements such as fake logos, checkbox-looking menu icons, generic admin sidebars, or invented color palettes.

## Component Fidelity Checklist

Before drawing or coding new UI, inspect the live page for these concrete style facts:

- global background color, page container width, card radius, shadows, and spacing
- top banner/header height, logo area, user/account area, and top-level tabs
- left sidebar width, active menu background, icons, collapse behavior, and section grouping
- primary/secondary/tertiary button height, padding, color, hover state, and icon style
- select, date picker, segmented control, tab, radio group, and toolbar styling
- metric card typography, selected card border, comparison rows, arrows, and trend colors
- chart height, legend style, gridline color, axis text, and empty/loading states
- table header background, grouped-header borders, fixed columns, operation column, row hover, pagination

If any of these are unknown, inspect DOM/CSS/computed styles again before implementing. A screenshot can help compare the result, but it is not a substitute for reading the runtime HTML and CSS.

## Edit by Evolution, Not Reinvention

Default rule: preserve the live product language.

Keep unless the requirement explicitly changes them:

- page shell and navigation
- tabs and segmented controls
- button size, color, and spacing
- card styling
- table density, border, header grouping, fixed columns, pagination, and action area
- existing copy wording that is already productized

If the requirement really implies a restructure, allow the restructure, but still inherit the live page's visual language and reusable components.

When the live page already has a component type, prefer these implementation strategies in order:

1. Keep the live DOM subtree and patch content.
2. Recreate the component with the same live selectors/classes/assets and measured styles.
3. Build a neutral replacement only when the live asset is unavailable or sensitive, and document the exception in `provenance-map.md`.

Never use screenshots as the only basis for shell, header, sidebar, tab, button, table, or chart styling.

## Interaction Rules

- Preserve existing interaction ownership.
- If the live page has expand/collapse or hierarchy drill-down, new view switches must not reset expanded state unless the requirement explicitly says so.
- If the live page already has an entrance like `设置目标` or `导出数据`, iterate inside that interaction or keep the same entrance by default.
- If the summary belongs to a selected view, place it at the view level rather than as a page-global block.

## Table Rules

Respect the live table first.

- Reuse grouped headers when they already exist.
- Reuse fixed action columns and scrolling behavior.
- Do not casually hide columns inside a complex grouped table; that often breaks header structure.
- If rebuilding the table is unavoidable, match:
  - column density
  - row height
  - grouped header semantics
  - sort affordance
  - action buttons
  - fixed left/right behavior

For metric presentation:

- For percentage fields, usually show `当前值 + 变化率`.
- For non-percentage fields, split into `数值 / 变化量 / 变化率` only when the requirement really needs grouped comparison.
- Use the product's existing color convention for up/down changes.

## Desensitization Rules

Before final handoff, replace real:

- 公会名
- 团队名
- 用户名
- 账号名
- ID
- 敏感业务文案

with neutral sample names.

Check both:

- visible rendered text
- residual names inside the generated HTML source

For external-facing prototypes, first write a forbidden-field list for the audience. Examples:

- revenue, income, payment, paid users, gift count, online users
- internal account IDs, room IDs, guild IDs, user IDs
- internal-only labels, test channels, automation names
- authenticated image URLs or personal avatars

Run source search against this list before handoff. If any forbidden field remains, patch and re-run verification.

## Shareable Export Rules

When the user wants to share the prototype, export a standalone HTML instead of a page that still depends on the live site.

Mandatory checks:

- no external `script src`
- no external stylesheet dependency needed for the prototype to render
- no `base href` that changes asset resolution
- inline or replace images that would fail outside the internal environment
- replace authenticated avatar/image URLs with placeholders if they cannot be embedded

If the sharing platform strips `<script>`, tell the user to send the raw HTML file or a zip attachment rather than pasting the HTML into a document tool.

## Verification

Open the final local HTML and verify:

- the live page shell is still present
- new requirement blocks are visible
- component style still matches the source page
- view switching works
- expanded hierarchy is preserved across view switching when required
- action buttons are still visible
- table columns do not overflow or misalign
- no sensitive names remain
- the standalone HTML renders without missing CSS or broken images

Verification must produce artifacts, not just a mental check:

- `prototype-screenshot.png`
- `visual-review.md`
- source search output or notes for sensitive/forbidden fields
- source search output or notes for external scripts/styles/base href/authenticated image URLs

`visual-review.md` must explicitly compare:

- header/banner height, logo, account area, notification/tools area
- sidebar width, icons, active state, row height, indentation, collapse control
- top tabs and secondary tabs: spacing, underline, active color, typography
- buttons: height, padding, color, radius, icon use
- content start position, background, watermarks, cards, tables, empty states, pagination
- requirement-specific blocks and interactions

If any item is marked mismatch, fix it before final handoff or document why the requirement intentionally changed it.

## Handoff Gate

Do not final-answer until all gates pass:

- Runtime DOM captured: `live-runtime-dom.html` exists or a documented blocker explains why it cannot.
- Live screenshot captured.
- Computed styles captured for the reused shell and components.
- Asset inventory captured and live logo/menu/icon assets are reused or documented.
- Provenance map completed.
- Final HTML source contains expected live selectors/classes for the shell/components.
- Final HTML has no external `script src`, required external stylesheet, or `base href`.
- Final HTML has no forbidden sensitive/internal fields.
- Browser verification screenshot exists.
- Visual review has no unresolved mismatch for live shell, header/banner, sidebar, tabs, buttons, or tables.

## Common Failure Modes

- Starting from screenshots caused generic UI and wrong colors.
- Reading only static entry HTML missed runtime DOM structure.
- Rebuilding tables too freely broke grouped headers and action columns.
- Treating view switching as hierarchy switching collapsed expanded teams.
- Sharing a page snapshot without inlining dependencies caused missing styles and images.
- Capturing live DOM but then hand-building a new shell anyway caused wrong header/banner/sidebar/tabs.
- Replacing live menu icons with checkbox-like squares or generic SVGs broke product fidelity.
- Taking a final screenshot without comparing it to the live screenshot let obvious mismatches pass.

If any of these appear, go back to the live runtime DOM and patch from there.

## Lessons From Prior Failures

Explicitly avoid these mistakes:

- Do not lose the live page shell. Missing top banner, top tabs, side navigation, footer, or current account area means the prototype is not based on the product page.
- Do not approximate colors or icons from memory. Read CSS variables, class names, inline styles, icon SVGs, or existing icon components first.
- Do not invent a new card/banner/button style when the live page already has the same component type.
- Do not move controls to a visually convenient place if the live page already owns that workflow elsewhere.
- Do not hide complex table columns with CSS when the table uses grouped headers or fixed action columns; update the table model or rebuild with matching semantics.
- Do not let operation buttons overflow horizontally. Verify the action column width and sticky/fixed behavior after every table change.
- Do not keep real data in the final prototype. Search the HTML source as well as the rendered UI.
- Do not call a prototype shareable until external scripts, stylesheets, `base href`, authenticated image URLs, and broken images have been checked.

When the first output looks unlike the live page, stop feature work and repair fidelity first.
