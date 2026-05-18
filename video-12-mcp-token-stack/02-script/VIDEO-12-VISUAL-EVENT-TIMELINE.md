# Video 12 Visual Event Timeline

Human-readable director view generated from `VIDEO-12-RENDER-MANIFEST.json`. Times inside each segment are relative to that segment start; absolute ranges are shown in the heading.

## Asset Capture Summary

- **Required · Segment 7:** `09-recordings/seg07-cloudflare-source.mp4` (~26.6s)
  Browser open to Cloudflare 'Code Mode' blog/article. Slow scroll past hero. Hover/highlight the search() + execute() phrasing. Linger on the 1,000 input tokens claim or equivalent metric. No audio.
- **Required · Segment 9:** `09-recordings/seg09-anthropic-post.mp4` (~20.2s)
  Browser open to the Anthropic 'code execution + MCP' post. Show the page header and the Google Drive -> attach to Salesforce example paragraph. Cursor underlines that sentence once. No audio.
- **Required · Segment 12:** `09-recordings/seg12-mcp-docs-zoom.mp4` (~28.8s)
  Anthropic docs page covering programmatic tool calling. Scroll to the line stating MCP connector tools cannot be called programmatically. Cursor drags across that sentence. Hold for emphasis.
- **Required · Segment 16:** `09-recordings/seg16-jarvis-workspace.mp4` (~22.4s)
  Finder OR terminal `tree` of skills/video-production showing 02-heygen-vo/, 09-stills/, 03-remotion/ paths. Cursor opens one file (e.g. video-production SKILL.md) briefly to show real procedure content.
- **Optional · Segment 17:** `09-recordings/seg17-cli-vs-mcp-terminal.mp4` (~25.4s)
  Split-terminal recording: left runs a CLI command (e.g. jarvis-price stage QQQ) finishing fast; right runs same task via an MCP-style tool with schema load visible. HyperFrames mock is acceptable substitute.
- **Optional · Segment 25:** `09-recordings/seg25-mcp-command.mp4` (~8s)
  Short inset (~5-8s) of `/mcp` command running in Claude Code terminal, showing connected servers list. Used as terminal inset only, not full screen.
- **Required · Segment 29:** `09-recordings/seg29-source-tiles/`
  Five static screenshots (not a video clip): (1) Cloudflare Code Mode page, (2) Anthropic code-execution post, (3) Arcade benchmark page, (4) Scalekit MCP article, (5) one JARVIS test-bench screenshot. Save as 5 PNGs in this directory.

## Segment Timeline

### Segment 1 · 0:00-0:35 · Cold open: MCP is not bad; the layer choice matters

- **Avatar:** full
- **Template:** title-lower-left
- **Components:** `lowerThird`
- **Assets:** component-generated / no external visual asset required

| Time | Event | Target | Notes |
|---:|---|---|---|
| 0.0s | `avatar_full` |  | let 'I am the avatar...' land cleanly |
| 8.2s | `panel_slide_in` | title-lower-left |  |
| 18.0s | `chips_in` |  | items: Tool Search, Scoped Loading, Code Mode |
| 29.5s | `type_in` |  | text: Which layer should do which job? |
| 33.8s | `fade_out_all` |  |  |

Transition out: `dark_wipe`

### Segment 2 · 0:35-1:01 · Old failure mode: tool schemas flood context before useful work begins

- **Avatar:** none
- **Template:** context-flood-animation
- **Components:** `vscodeMock`, `metricCounter`, `eventCard`
- **Assets:** still `09-stills/002.png`

| Time | Event | Target | Notes |
|---:|---|---|---|
| 0.0s | `draw_container` | model-context-window |  |
| 3.0s | `tool_cards_fly_in` |  | items: GitHub, Slack, Sentry |
| 8.0s | `tool_cards_fly_in` |  | items: Grafana, Splunk, Jira |
| 15.3s | `stamp_label` |  | text: OVERHEAD; keyword: not work; lands on 'That is not work' |
| 18.3s | `counter_color` | token-counter | keyword: not just money |
| 20.0s | `sequential_text_in` |  | items: Latency, Confusion, Less room |

Transition out: `compress_horizontal_into_seg3_divider`

### Segment 3 · 1:01-1:25 · Tool Search improvement: search-driven expansion, not upfront schemas

- **Avatar:** none
- **Template:** before-after-split
- **Components:** `comparisonSplit`, `metricCounter`
- **Assets:** still `09-stills/003.png`

| Time | Event | Target | Notes |
|---:|---|---|---|
| 0.0s | `split_open_from_bar` |  |  |
| 3.4s | `fill_left` |  |  |
| 6.9s | `fill_right_step1` |  |  |
| 12.4s | `fill_right_step2` |  |  |
| 15.6s | `counter_land` | left-counter | value: 77K; keyword: 77K |
| 19.8s | `counter_land` | right-counter | value: 8.7K; keyword: 8.7K |
| 22.8s | `wipe` |  |  |
| 6.9s | `cursor_click_once` | right-search-box |  |

Transition out: `green_wipe_into_red_warning_cards`

### Segment 4 · 1:25-1:47 · Prevent oversimplification: three caveats about Tool Search

- **Avatar:** none
- **Template:** warning-cards-stack
- **Components:** `eventCard`, `thesisBar`
- **Assets:** still `09-stills/004.png`

| Time | Event | Target | Notes |
|---:|---|---|---|
| 0.0s | `card_in` | card1 | text: Tool Search reduces schema load. |
| 6.0s | `card_in` | card2 | text: It does not shrink every result. |
| 11.0s | `card_in` | card3 | text: It does not make retrieval perfect. |
| 16.0s | `arrange_triangle` |  | items: card1, card2, card3 |

Transition out: `triangle_rotates_flat_into_benchmark_board`

### Segment 5 · 1:47-2:19 · Reliability tradeoff made concrete with benchmark numbers

- **Avatar:** none
- **Template:** benchmark-bars
- **Components:** `dashboardPanel`, `metricCounter`
- **Assets:** still `09-stills/005.png`

| Time | Event | Target | Notes |
|---:|---|---|---|
| 0.0s | `headline_in` |  | text: Better, not magical. |
| 4.5s | `bar_grow` |  | to: 74; keyword: 49 |
| 11.5s | `bar_grow` |  | to: 88.1; keyword: 79 |
| 18.5s | `bar_appear` |  | value: 60 |
| 25.5s | `final_label` |  | text: Search quality becomes reliability. |

Transition out: `board_slides_left_for_side_avatar`

### Segment 6 · 2:19-2:52 · Direct address: layer thesis

- **Avatar:** side (right_35pct)
- **Template:** layer-stack-thesis
- **Components:** `sideAvatarFrame`, `architectureLayers`
- **Assets:** still `09-stills/006.png`

| Time | Event | Target | Notes |
|---:|---|---|---|
| 0.0s | `side_avatar_in` |  |  |
| 6.8s | `layer_in` |  | keyword: MCP |
| 11.8s | `layer_in` |  | keyword: Skills |
| 16.8s | `layer_in` |  | keyword: CLI |
| 21.8s | `layer_in` |  | keyword: Code execution |
| 27.8s | `layers_lock_stack` |  | text: Do not make one layer do every job. |

Transition out: `avatar_fades_right; layer_stack_becomes_browser_chrome`

### Segment 7 · 2:52-3:19 · Cloudflare Code Mode source proof

- **Avatar:** none
- **Template:** source-card-with-metric-panel
- **Components:** `sourceBadge`, `browserMock`, `metricCounter`, `eventCard`, `thesisBar`
- **Assets:** still `09-stills/007-cloudflare-code-mode.png`; b-roll `09-recordings/seg07-cloudflare-source.mp4`

| Time | Event | Target | Notes |
|---:|---|---|---|
| 0.0s | `broll_in` |  | source: seg07-cloudflare-source.mp4 |
| 4.5s | `pills_in` |  | items: search(), execute() |
| 10.5s | `schema_dissolve_into_typed_api_file` |  |  |
| 17.5s | `metric_flip` | metric-panel | to: 1,000 input tokens; keyword: 1,000 |
| 23.5s | `source_badge_hold` |  |  |
| 3.5s | `cursor_scroll_once` |  |  |
| keyword: search and execute | `cursor_underline` |  |  |

Transition out: `metric_panel_expands_into_seg8_number`

### Segment 8 · 3:19-3:42 · Kinetic number collapse: 1.17M -> 1K tokens via discover/inspect/execute

- **Avatar:** none
- **Template:** kinetic-number-funnel
- **Components:** `metricCounter`, `eventCard`, `thesisBar`
- **Assets:** still `09-stills/008.png`

| Time | Event | Target | Notes |
|---:|---|---|---|
| 0.0s | `number_fill_screen` |  | value: 1,170,000 tokens; keyword: 1,170,000 |
| 4.0s | `drain_through_funnel` |  |  |
| 9.0s | `sequential_verbs_in` |  | items: discover, inspect, execute, return |
| 15.0s | `number_land` |  | value: 1,000; keyword: 1,000 |
| 19.0s | `thesis_in` |  | text: Context should carry reasoning, not every instruction manual. |

Transition out: `funnel_becomes_data_pipeline`

### Segment 9 · 3:42-4:02 · Anthropic source + Google Drive -> Salesforce example

- **Avatar:** none
- **Template:** source-card-top-icons-bottom
- **Components:** `browserMock`, `eventCard`
- **Assets:** still `09-stills/009.png`; b-roll `09-recordings/seg09-anthropic-post.mp4`

| Time | Event | Target | Notes |
|---:|---|---|---|
| 0.0s | `source_card_in` |  |  |
| 4.0s | `icon_in` | google-drive |  |
| 9.0s | `object_move` | model-context | source: google-drive |
| 14.0s | `object_move` | salesforce | source: model-context |
| 18.0s | `highlight_red` |  | duplicate transport |
| 2.5s | `cursor_underline_text_in_broll` |  | the Google Drive -> Salesforce example sentence |

Transition out: `red_path_splits_into_naive_vs_sandbox_lanes`

### Segment 10 · 4:02-4:25 · Data movement waste: model is transporting, not reasoning

- **Avatar:** none
- **Template:** two-lane-dataflow
- **Components:** `comparisonSplit`, `eventCard`, `metricCounter`
- **Assets:** still `09-stills/010.png`

| Time | Event | Target | Notes |
|---:|---|---|---|
| 0.0s | `replay_lane` | left |  |
| 5.6s | `counter_add` | model-context | value: +50K; keyword: 50K |
| 10.6s | `lane_in` | right |  |
| 15.6s | `boundary_in` | sandbox-boundary |  |
| 19.6s | `exit_pill` |  |  |

Transition out: `green_pill_expands_into_compression_chart`

### Segment 11 · 4:25-4:46 · Headline 150K -> 2K compression with the underlying reason

- **Avatar:** none
- **Template:** compression-counter-with-code
- **Components:** `vscodeMock`, `metricCounter`, `thesisBar`
- **Assets:** still `09-stills/011.png`

| Time | Event | Target | Notes |
|---:|---|---|---|
| 0.0s | `counter_in` |  | value: 150K; keyword: 150 |
| 3.5s | `code_lines_in` |  |  |
| 6.5s | `counter_collapse` |  | to: 2K; keyword: 2K |
| 10.5s | `stamp_in` |  | text: 98.7% reduction; keyword: 98.7 |
| 15.5s | `thesis_in_bottom` |  | text: Keep intermediate data out of context. |
| 12.5s | `cursor_select_line` | return status |  |

Transition out: `code_panel_scrolls_to_docs`

### Segment 12 · 4:46-5:15 · Caveat: MCP connector tools cannot be called programmatically

- **Avatar:** none
- **Template:** docs-zoom-with-workaround-cards
- **Components:** `browserMock`, `eventCard`, `thesisBar`
- **Assets:** still `09-stills/012.png`; b-roll `09-recordings/seg12-mcp-docs-zoom.mp4`

| Time | Event | Target | Notes |
|---:|---|---|---|
| 0.0s | `broll_in` |  | source: seg12-mcp-docs-zoom.mp4 |
| 5.4s | `zoom_into` | restriction-line |  |
| 11.4s | `underline_animate` | MCP connector tools | keyword: connector |
| 17.4s | `cards_in` |  | items: wrapper pattern, server-side Code Mode, controlled runtime |
| 24.4s | `cards_stack_into` |  | text: Use another layer. |
| 7.4s | `cursor_drag_across` | restriction-line |  |

Transition out: `red_underline_becomes_sandbox_boundary`

### Segment 13 · 5:15-5:45 · Senior-engineer security warning around sandboxed code execution

- **Avatar:** side (left_34pct)
- **Template:** sandbox-checklist
- **Components:** `sideAvatarFrame`, `eventCard`
- **Assets:** still `09-stills/013.png`

| Time | Event | Target | Notes |
|---:|---|---|---|
| 0.0s | `side_avatar_in` |  |  |
| 5.6s | `draw_box` | sandbox |  |
| 10.6s | `checklist_in` |  | items: No file system, No env vars, Fetch disabled, Credentials via bindings, Monitoring required |
| 19.6s | `label_outside_box` |  | text: New attack surface |
| 25.6s | `label_change` |  | to: Sandboxing is the product. |

Transition out: `sandbox_box_collapses_into_group_selector`

### Segment 14 · 5:45-6:13 · Scoped MCP: load less on purpose with group selector and config

- **Avatar:** none
- **Template:** group-selector-with-config-card
- **Components:** `dashboardPanel`, `terminalMock`, `eventCard`
- **Assets:** still `09-stills/014.png`

| Time | Event | Target | Notes |
|---:|---|---|---|
| 0.0s | `title_in` |  | text: Scoped MCP: load less on purpose. |
| 4.8s | `chip_grid_in` |  | items: Rapid, Pro, browser, finance, ecommerce, code, ... |
| 10.8s | `chips_glow` |  |  |
| 16.8s | `config_type_in` | config-card |  |
| 22.8s | `headline_in` |  | text: Production agents should be narrow. |
| 10.8s | `cursor_click_chip` | browser |  |
| 12.5s | `cursor_click_chip` | finance |  |
| 16.0s | `cursor_click_button` | apply |  |

Transition out: `chips_become_skill_folders`

### Segment 15 · 6:13-6:34 · Skills are procedure, not live access

- **Avatar:** none
- **Template:** skill-folder-tree
- **Components:** `vscodeMock`, `eventCard`
- **Assets:** still `09-stills/015.png`

| Time | Event | Target | Notes |
|---:|---|---|---|
| 0.0s | `folder_open` |  |  |
| 3.7s | `file_card_expand` |  |  |
| 7.7s | `pin_notes` |  | items: what files matter, what commands to run, what mistakes to avoid |
| 15.7s | `background_shrink` | main-context-file |  |
| 3.7s | `cursor_open_file` | SKILL.md |  |
| keyword: procedure | `cursor_highlight` | procedure |  |

Transition out: `skill_file_becomes_jarvis_artifact`

### Segment 16 · 6:34-6:57 · JARVIS uses skills to keep domain rules out of unrelated work

- **Avatar:** none
- **Template:** path-cards-with-arrows
- **Components:** `vscodeMock`, `eventCard`
- **Assets:** still `09-stills/016.png`; b-roll `09-recordings/seg16-jarvis-workspace.mp4`

| Time | Event | Target | Notes |
|---:|---|---|---|
| 0.0s | `workspace_map_in` |  |  |
| 4.4s | `card_open` |  |  |
| 9.4s | `card_open` |  |  |
| 14.4s | `card_open` |  |  |
| 18.4s | `cards_fade_gray` |  |  |
| 4.4s | `cursor_open_card` | 02-heygen-vo |  |

Transition out: `map_wipes_into_terminal_benchmark`

### Segment 17 · 6:57-7:22 · CLI vs MCP token cost benchmark race

- **Avatar:** none
- **Template:** split-race-with-meters
- **Components:** `comparisonSplit`, `terminalMock`, `metricCounter`
- **Assets:** still `09-stills/017.png`; b-roll `09-recordings/seg17-cli-vs-mcp-terminal.mp4`

| Time | Event | Target | Notes |
|---:|---|---|---|
| 0.0s | `lane_in` | left |  |
| 6.0s | `lane_result` | left |  |
| 11.0s | `lane_in` | right |  |
| 16.0s | `counter_jump` | right | value: 44,026; keyword: 44 |
| 21.0s | `stamp_in` |  | text: 32x token cost |

Transition out: `split_shifts_to_identity_comparison`

### Segment 18 · 7:22-7:50 · Honest MCP defense: who is the agent acting for?

- **Avatar:** none
- **Template:** identity-vs-permission
- **Components:** `comparisonSplit`, `eventCard`, `thesisBar`
- **Assets:** still `09-stills/018.png`

| Time | Event | Target | Notes |
|---:|---|---|---|
| 0.0s | `lane_check` | left |  |
| 6.5s | `org_grid_in` | right |  |
| 12.5s | `draw_boundary` |  |  |
| 19.5s | `center_question_huge` |  | text: Who is the agent acting for? |

Transition out: `permission_becomes_output_boundary`

### Segment 19 · 7:50-8:16 · Output filtering: messy payload cleaned to three fields

- **Avatar:** none
- **Template:** payload-cleanup
- **Components:** `decisionTable`, `eventCard`
- **Assets:** still `09-stills/019.png`

| Time | Event | Target | Notes |
|---:|---|---|---|
| 0.0s | `messy_payload_in` |  |  |
| 6.0s | `mark_red` |  |  |
| 13.0s | `fade_out` |  |  |
| 19.0s | `expand_to_fill` |  | items: title, URL, price |
| 23.0s | `final_label` |  | text: Return what the agent needs. |
| keyword: title | `cursor_select_sequence` |  |  |

Transition out: `three_fields_become_table_rows`

### Segment 20 · 8:16-8:40 · TOON: useful for flat rows, careful with nested data

- **Avatar:** none
- **Template:** json-to-toon
- **Components:** `vscodeMock`, `decisionTable`, `eventCard`
- **Assets:** still `09-stills/020.png`

| Time | Event | Target | Notes |
|---:|---|---|---|
| 0.0s | `json_rows_repeat` |  |  |
| 5.5s | `keys_lift_to_header` |  |  |
| 10.5s | `compact_table_form` |  |  |
| 15.5s | `nested_object_in` |  |  |
| 20.5s | `caution_badge_in` |  | text: Use where it fits. |

Transition out: `caution_becomes_table_row`

### Segment 21 · 8:40-9:10 · Full architecture comparison table

- **Avatar:** none
- **Template:** decision-table-7-rows
- **Components:** `decisionTable`, `thesisBar`
- **Assets:** still `09-stills/021.png`

| Time | Event | Target | Notes |
|---:|---|---|---|
| 0.0s | `table_frame_in` |  |  |
| 3.2s | `row_reveal` |  |  |
| 5.7s | `row_reveal` |  |  |
| 8.2s | `row_reveal` |  |  |
| 10.7s | `row_reveal` |  |  |
| 13.2s | `row_reveal` |  |  |
| 15.7s | `row_reveal` |  |  |
| 18.2s | `row_reveal` |  |  |
| 24.2s | `rows_sort_into_bands` |  |  |
| 27.2s | `title_in` |  | text: Right layer. Right scope. Measured output. |

Transition out: `bands_slide_left_for_side_avatar`

### Segment 22 · 9:10-9:37 · Practical decision rule for builders

- **Avatar:** side (right_34pct)
- **Template:** four-card-grid
- **Components:** `sideAvatarFrame`, `eventCard`
- **Assets:** still `09-stills/022.png`

| Time | Event | Target | Notes |
|---:|---|---|---|
| 0.0s | `side_avatar_in` |  |  |
| 4.7s | `card_light` | mcp | text: Permissioned external access -> MCP; keyword: permissioned |
| 9.7s | `card_light` | skill | text: Procedure -> Skill; keyword: procedure |
| 14.7s | `card_light` | cli | text: Local deterministic work -> CLI; keyword: local |
| 19.7s | `card_light` | code | text: Large intermediate data -> Code execution; keyword: intermediate |
| 23.7s | `connect_to_center` |  | text: Do not make one tool carry every job. |

Transition out: `cards_become_jarvis_layers`

### Segment 23 · 9:37-10:00 · JARVIS layered operating architecture

- **Avatar:** none
- **Template:** architecture-layers
- **Components:** `architectureLayers`
- **Assets:** still `09-stills/023.png`

| Time | Event | Target | Notes |
|---:|---|---|---|
| 0.0s | `layer_in_bottom` |  |  |
| 4.8s | `layer_in_middle` |  |  |
| 9.8s | `side_port_in` |  |  |
| 14.8s | `heartbeat_pulse` |  |  |
| 19.8s | `context_window_remains_small` |  |  |

Transition out: `architecture_folds_into_experiment_board`

### Segment 24 · 10:00-10:26 · Convert argument into measurable test plan

- **Avatar:** none
- **Template:** experiment-board-4col
- **Components:** `decisionTable`, `dashboardPanel`, `ctaControls`
- **Assets:** still `09-stills/024.png`

| Time | Event | Target | Notes |
|---:|---|---|---|
| 0.0s | `task_card_in` |  | text: QQQ MACD report |
| 6.2s | `columns_in` |  |  |
| 11.2s | `rows_in_empty` |  |  |
| 17.2s | `checkboxes_animate` |  |  |
| 22.2s | `final_label` |  | text: Measure before claiming victory. |
| 17.2s | `cursor_click` | Run 1 |  |
| 19.2s | `cursor_click` | Run 2 |  |

Transition out: `board_becomes_migration_checklist`

### Segment 25 · 10:26-10:46 · Migration phase 1: immediate free wins

- **Avatar:** none
- **Template:** checklist-with-terminal-inset
- **Components:** `terminalMock`, `eventCard`
- **Assets:** still `09-stills/025.png`; b-roll `09-recordings/seg25-mcp-command.mp4`

| Time | Event | Target | Notes |
|---:|---|---|---|
| 0.0s | `headline_in` |  | text: Free wins - one hour |
| 3.5s | `terminal_inset_play` |  | source: seg25-mcp-command.mp4 |
| 6.5s | `fade_out_cards` |  |  |
| 10.5s | `toggle_on` | Tool Search |  |
| 14.5s | `allowlist_in` |  |  |
| 10.5s | `cursor_click` | Tool Search toggle |  |
| 14.0s | `cursor_click` | group selector |  |

Transition out: `row4_becomes_file_move_animation`

### Segment 26 · 10:46-11:09 · Migration phase 2: procedures to skills, deterministic to scripts, filter outputs

- **Avatar:** none
- **Template:** three-lane-refactor
- **Components:** `vscodeMock`, `architectureLayers`, `eventCard`
- **Assets:** still `09-stills/026.png`

| Time | Event | Target | Notes |
|---:|---|---|---|
| 0.0s | `file_in_overstuffed` |  |  |
| 4.7s | `blocks_move` |  | to: skills/ |
| 9.7s | `blocks_move` |  | to: scripts/ |
| 14.7s | `object_shrink` |  | to: 3 fields |
| 19.7s | `file_become_small` | CLAUDE.md |  |
| 4.7s | `cursor_drag` |  | to: SKILL.md |

Transition out: `lanes_merge_into_sandbox`

### Segment 27 · 11:09-11:33 · Migration phase 3: heavy patterns + sandboxing warning

- **Avatar:** none
- **Template:** controlled-runtime-build
- **Components:** `architectureLayers`, `eventCard`
- **Assets:** still `09-stills/027.png`

| Time | Event | Target | Notes |
|---:|---|---|---|
| 0.0s | `draw_boundary` | sandbox |  |
| 4.1s | `card_in_blocked` |  |  |
| 10.1s | `wrapper_bridges_in` |  |  |
| 15.1s | `object_stays_inside` |  |  |
| 20.1s | `exit_result_only` |  |  |
| 20.1s | `lock_visible` |  |  |

Transition out: `lock_breaks_into_three_mistake_cards`

### Segment 28 · 11:33-11:57 · Correct three common wrong takes via flip cards

- **Avatar:** none
- **Template:** three-flip-cards
- **Components:** `eventCard`, `thesisBar`
- **Assets:** still `09-stills/028.png`

| Time | Event | Target | Notes |
|---:|---|---|---|
| 0.0s | `card_flip` | card1 |  |
| 6.3s | `card_flip` | card2 |  |
| 12.3s | `card_flip` | card3 |  |
| 18.3s | `final_phrase_huge` |  | text: Right layer. Right scope. Measured output. |

Transition out: `phrase_becomes_evidence_wall_title`

### Segment 29 · 11:57-12:23 · Evidence beats opinion: source tile mosaic

- **Avatar:** none
- **Template:** evidence-mosaic
- **Components:** `evidenceMosaic`, `thesisBar`
- **Assets:** still `09-stills/029.png`; source tiles `09-recordings/seg29-source-tiles/`

| Time | Event | Target | Notes |
|---:|---|---|---|
| 0.0s | `fade_out_labels` |  |  |
| 4.6s | `tile_in` |  | source: seg29-source-tiles/cloudflare.png |
| 8.6s | `tile_in` |  | source: seg29-source-tiles/anthropic.png |
| 12.6s | `tile_in` |  | source: seg29-source-tiles/arcade.png |
| 12.6s | `tile_in` |  | source: seg29-source-tiles/scalekit.png |
| 17.6s | `tile_in_center_large` |  | source: seg29-source-tiles/jarvis-bench.png |
| 22.6s | `connect_all` |  | text: Test it on real work. |

Transition out: `wall_dims_for_cta`

### Segment 30 · 12:23-12:43 · Graphics CTA: subscribe / like / bell

- **Avatar:** none
- **Template:** cta-three-controls
- **Components:** `ctaControls`
- **Assets:** still `09-stills/030.png`

| Time | Event | Target | Notes |
|---:|---|---|---|
| 0.0s | `button_in` | subscribe | keyword: subscribe |
| 3.9s | `button_click_change` | subscribe | to: Subscribed |
| 6.9s | `icon_pulse` | like | keyword: like |
| 9.9s | `bell_ring` |  | keyword: bell |
| 12.9s | `teaser_in` |  | text: Next video: measure the stack on JARVIS |
| 17.9s | `fade_out_all` |  |  |
| 3.9s | `cursor_click` | Subscribe |  |
| 6.9s | `cursor_click` | Like |  |
| 9.9s | `cursor_click` | Bell |  |

Transition out: `fade_to_avatar_full`

### Segment 31 · 12:43-13:07 · Recap of the four-layer thesis

- **Avatar:** full
- **Template:** bottom-center-phrase
- **Components:** `lowerThird`
- **Assets:** component-generated / no external visual asset required

| Time | Event | Target | Notes |
|---:|---|---|---|
| 0.0s | `avatar_full` |  |  |
| 4.6s | `phrase_in` |  | text: MCP is one layer. |
| 9.6s | `phrase_swap` |  | to: Skills for procedures. |
| 14.6s | `phrase_swap` |  | to: CLI for local deterministic work. |
| 19.6s | `phrase_swap` |  | to: Code execution when data should stay out of context. |

Transition out: `no_hard_transition_continue_to_seg32`

### Segment 32 · 13:07-13:23 · Final memorable questions and send-off

- **Avatar:** full
- **Template:** questions-then-title-card
- **Components:** `lowerThird`
- **Assets:** component-generated / no external visual asset required

| Time | Event | Target | Notes |
|---:|---|---|---|
| 0.0s | `avatar_full_no_overlay` |  |  |
| 5.1s | `small_phrase_in` |  | text: Where do the tokens go?; keyword: tokens |
| 7.6s | `small_phrase_in` |  | text: Where does the data live?; keyword: data |
| 10.1s | `small_phrase_in` |  | text: Who is the agent acting for?; keyword: acting |
| 11.6s | `final_card_in` |  | text: The 2026 Token Stack |
| 14.6s | `fade_to_black` |  |  |

Transition out: `end`

## Renderer Notes

- The JSON manifest is the machine-readable source for a future manifest-driven renderer.
- This Markdown file is the director/review view. Edit intent here only if also syncing the JSON.
- Segment 7 has already been implemented as a hand-built proof in `14-design-system/index.html`; later work should make the renderer consume this manifest directly.
