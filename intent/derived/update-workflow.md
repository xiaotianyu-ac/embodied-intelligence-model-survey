# Updating the survey

1. Read the original release, paper and implementation; record the exact model/version and evidence date.
2. Add or revise one research module under `records/research/`, maintaining source IDs and matching Chinese/English coverage.
3. Distinguish a new method, a new checkpoint, and an engineering release. Add relationship edges only with a stated type and evidence.
4. Run `scripts/assemble.py`; inspect source deduplication, cards, matrices, and reference numbering.
5. Update diagrams if a material relationship changes; keep series evolution distinct from weight inheritance.
6. Build both PDFs, inspect every page at overview scale and difficult tables/figures at readable scale, and fix problems.
7. Run validation, rebuild the delivery manifest, and check it. Record substantive evidence conflicts in the audit.
8. Commit the complete snapshot and verify remote path/size/blob hashes. Do not publish a README that advertises missing reports.
