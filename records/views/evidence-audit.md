# Evidence audit / 证据审计

Evidence cutoff: **2026-09-11**. This is a scoped technical survey with targeted primary-source checks, not an exhaustive systematic-review census or an experimental reproduction.

## What was checked

- Representative models are decomposed by inputs, architecture, action representation, learning, data, execution, contributions, limits and available assets.
- Research papers, official repositories/model cards, company disclosures and customer announcements are used for different claims. A vendor disclosure establishes what was disclosed, not independently measured reliability.
- A second reading targeted 12 high-risk 2026 claims: PI0.7/MEM, GR00T N1.7, three Gemini branches, LingBot-VLA2, SONIC updates, Helix02, Skild S1, GEN-1.5 and BMW deployment attribution.
- An independent synthesis audit checked MolmoAct2 stages, V-JEPA2.1 predictor reuse, training/data counts, benchmark revisions, source coverage and bilingual correspondence.
- The automated validator checks references, decomposition fields, graph endpoints, corresponding report structure, local links, SVG syntax and PDF text. It does not establish factual truth or robot performance.

## Corrections incorporated

1. GR00T N1.7 code and weights have different licensing statements: Apache 2.0 code; NVIDIA Open Model License weights. A broad README summary is not substituted for the specific license section.
2. V-JEPA2.1 robot planning reuses the 2-AC predictor architecture/code and planning protocol, then retrains its action-conditioned predictor with the new encoder. No trained-predictor weight inheritance is asserted. The 60%→70% comparison uses roughly three seconds of planning; 80% uses roughly fourteen seconds.
3. MolmoAct2 discrete autoregressive pretraining, the continuous flow expert and the Think variant are distinguished.
4. Skild S1's cumulative per-step score with human failure recovery is not treated as uninterrupted whole-task completion.
5. Gemini reasoning and action branches are distinct in relation endpoints; grouped cards do not imply one shared checkpoint. The two UniVLA works are separate entries.
6. Figure02 historical production numbers are not transferred to Figure03/Helix02. Product announcements, pilots and sustained operations are distinguished.

## Remaining uncertainty and scope limits

The N1.6 backbone description differs between a version-specific model card and later broad marketing copy; the report preserves this conflict. SONIC training-compute figures disagree across public materials and are not used as a normalized comparison. Dataset and benchmark revisions affect DROID counts and RoboCasa365 horizons. Proprietary systems such as S1/GEN do not disclose enough to infer a full action architecture, parameter count or reproducible training recipe.

The registry contains representative model, version, method and component cards. Named context nodes—including GEN-1/1.5 and some branch components—can be discussed and related without having an independent full card. Counts are not counts of unique foundation models. The graphs include explicit documented relationships and clearly labeled analytical comparisons; an arrow does not by itself imply inherited weights.

No hardware trials or model-training runs were performed for this survey. No unified leaderboard is produced across incompatible benchmarks. Source dates, access dates and inspected source scope are retained in the [source ledger](../artifacts/sources.json). Raw query logs retain actual search strings, including imperfect discovery queries; they are not claims about publication dates. The [claim ledger](claim-evidence-ledger.json) records representative high-risk claims and their limits.
