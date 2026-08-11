# Data notes

`manifest.json` contains only sample counts and selection metadata.

`zh_ja_gloss_variants.json` contains English sense realizations derived from
StingrayBench source meanings and contexts. StingrayBench is distributed under
CC BY-SA 4.0; treat this derivative file under the same terms. The variants were
checked for obvious sense preservation during the pilot but have **not** been
independently validated by bilingual human annotators. They are robustness
stimuli, not a new gold benchmark.

No original source sentences are redistributed. Reproduction scripts expect a
separately obtained StingrayBench checkout under `external/`.

`prematched_controls/` contains only public design metadata, IDs, feature
balances, reference-model difficulty scores and SHA-256 provenance. Files whose
names begin with `private_` contain source text and are ignored. The frozen
matching is outcome-blind; its controls are candidates until two bilingual
annotators pass them under `../docs/FINAL_MEASUREMENT_HANDOFF_ZH.md`.

The formal factorial subset is not selected from the `Cognates` field alone.
`src/stingray_factorial.py` additionally requires the exact CJK string, or a
standalone case-insensitive Latin word, to occur in all four contexts. This
excludes composite spellings, inflections and rows whose translated context
uses a synonym instead of the listed target. The final strict counts are 27
ZH–JA and 33 ID–TL.
