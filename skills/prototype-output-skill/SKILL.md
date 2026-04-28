---
name: prototype-output-skill
description: Build or revise a high-fidelity HTML prototype by starting from a real backend/product page instead of redrawing from scratch. Use when the user provides an existing admin/internal page URL, an authenticated browser page, or a local HTML snapshot and wants Codex to capture the runtime DOM/CSS, preserve the live product shell and component language, apply requirement changes on top, desensitize data, and export a shareable standalone HTML prototype.
---

# 原型输出 Skill

Treat the task as a product iteration on a live page, not a blank-page design exercise.

## Workflow

1. Read the real page first.
2. Extract runtime DOM and visible structure before editing.
3. Reuse the live shell, component hierarchy, copy style, and interaction pattern unless the requirement explicitly changes them.
4. Apply requirement changes at the right product layer.
5. Desensitize all sensitive data before handoff.
6. Export a standalone shareable HTML, then verify it in browser.

## Read the Real Page

- Prefer the user's current logged-in browser/session for internal pages.
- Use the current page/tab the user already opened when possible.
- Do not start from screenshots alone.
- Do not rebuild generic banners, sidebars, tabs, cards, or tables from memory when the live page already has them.

For modern bundled apps, static entry HTML is not enough. The rendered runtime DOM is the source of truth.

## Capture Before Editing

Save artifacts inside one requirement folder:

- `<需求目录>/过程文件/`
  - runtime HTML snapshot
  - notes about key class names, table structure, component blocks, and current interactions
  - optional generator / patch script if the page is large and repeated edits are likely
- `<需求目录>/原型与示意图/`
  - editable prototype HTML
  - final shareable standalone HTML if different from the editable one

Before modifying anything, capture:

- current page shell: top bar, side nav, tabs, breadcrumb, footer
- card layout and metric blocks
- table header model, grouped headers, fixed columns, action column
- current interactions: expand/collapse, drill-down, filters, date selectors, target setting, export, action buttons
- real field names and current copy style

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

## Common Failure Modes

- Starting from screenshots caused generic UI and wrong colors.
- Reading only static entry HTML missed runtime DOM structure.
- Rebuilding tables too freely broke grouped headers and action columns.
- Treating view switching as hierarchy switching collapsed expanded teams.
- Sharing a page snapshot without inlining dependencies caused missing styles and images.

If any of these appear, go back to the live runtime DOM and patch from there.
