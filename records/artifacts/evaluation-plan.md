# Proposed evaluation plan / 建议评测方案

This is a protocol proposal, not a record of experiments performed. 本文件是可执行的实验设计，不是已运行的实验结果。

## 1. Register the task and operating conditions

Choose tasks before selecting checkpoints. Record robot model and serial configuration, gripper/hand, cameras and calibration, force/touch availability, control mode, frequency, action units/order, joint limits, normalization, and network/compute placement. Fix reset and completion rules. Specify whether help, retry, coaching, or remote intervention is allowed.

Version-lock the model checkpoint, tokenizer, code commit, dataset revision, benchmark assets, controller and timeout. In particular, RoboCasa365 changed horizons in May 2026 and RMBench released retrained checkpoints in July; a benchmark name alone is insufficient. See `sources.json` and `benchmark-matrix.csv` for evidence.

## 2. Define four evaluation levels

| Level | Changes held out from adaptation | Failure probes |
|---|---|---|
| A | Repeated known skills, new seeds | Calibration perturbation and grasp slips |
| B | Object instances, views, instructions | Distractors, paraphrases, occlusion |
| C | Environments and subtask combinations | Interrupted task, moved object, missing tool |
| D | Embodiment or sustained operation | Load change, contact transition, recovery and reset |

Track the exact meaning of zero-shot: unseen object, scene, skill, embodiment, or only an unseen combination. Do not combine these labels. Keep collection sessions and scenes separated across training and test sets and record possible internet/pretraining overlap.

## 3. Compare identifiable design changes

- Policy baselines: ACT/DP, an adaptable VLA, and a planner-plus-policy system under the same available task demonstrations.
- Action design: same backbone with single-step/chunks, discrete/continuous output, and synchronous/asynchronous scheduling. Include prefix-training differences.
- Sensing and memory: vision only, vision plus proprioception, additional force/touch, and history/memory ablations.
- World models: direct policy, fixed-budget planning, increased-budget planning, and a control with equivalent added compute where feasible.
- Whole-body systems: fix low-level controller when comparing high-level policies; separately test locomotion/contact recovery before end-to-end mobile manipulation.

For closed commercial models without controlled training data, describe the test as system acceptance. Do not infer that one architecture caused a performance gap.

## 4. Log every attempt

Required episode fields: task, scene, object instance, split, robot/config hash, checkpoint/code/data revisions, random seed, requested instruction, sensor timestamps, inference start/end, action timestamps, buffered prefix length, control mode, completion/timeout, intervention events, resets, collisions/drops/stops, energy if measured, and failure annotation.

Suggested JSONL schema is in `evaluation-log-schema.json`. Store sensitive household recordings under appropriate access controls in the actual experiment; this survey ships no recordings.

## 5. Metrics and uncertainty

Task success = successful attempts / all attempts. Full-chain success requires every registered subtask to finish within the allowed horizon. Recovery rate uses a prespecified disturbance/failure denominator. Human time includes setup, intervention, resets, annotation, and cleanup; report these components separately from training compute.

Report median and tail latency, and distinguish model-call latency from camera-to-actuation observation age. Report task throughput and energy per successful task where measurable. Failures remain in the denominator. Choose repetition counts based on desired precision and practical cost before testing; use binomial confidence intervals for independent trials and task/scene-aware resampling when outcomes cluster. A handful of curated videos cannot estimate operational reliability.

## 6. Release evidence, not only a score

Publish configuration hashes, per-task counts, aggregate uncertainty, failure taxonomy, intervention policy, data-exposure statement, and representative successes and failures subject to rights and privacy. Maintain a rollback checkpoint and re-run a fixed regression suite after updates. A deployment decision requires task-specific acceptance thresholds chosen by the system owner; this report does not invent universal safe thresholds.
