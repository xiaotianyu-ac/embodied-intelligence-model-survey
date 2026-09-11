## Data and evaluation: establishing actual progress

### What the data assets contribute

| Asset or interface | Verified representative scale or property | Relevance |
|---|---|---|
| Open X-Embodiment | 22 robots in the original paper; standardized records | Cross-embodiment sharing; actual mixtures differ by model [R001] |
| BridgeData V2 | 60,096 trajectories in 24 environments, including teleoperation and scripted runs | Object and scene diversity; overlaps with OXE mixtures [R021] |
| DROID | 76k trajectories, 350 hours, 564 scenes | Distributed real-world collection; calibration/data revisions matter [R002] |
| RoboMIND | Original paper: 107k trajectories, 479 tasks, 96 object classes | Multiple embodiments collected on a unified platform [R004] |
| AgiBot World | Beta lists 1,003,672 trajectories | Bimanual collection at scale; hardware count is not embodiment count [R005] |
| UMI / DexUMI | Handheld gripper or human-hand interfaces | Portable demonstrations still need temporal, pose, and reachability alignment [R003][R020] |
| RoboCasa365 | 365 tasks, 2500+ kitchens; 600+ human and 1600+ synthetic demonstration hours | Compositional and scene coverage; not all hours are real-robot collection [R022][R027] |

These quantities cannot be added into a total of independent embodied data. Trajectories recur across datasets and training mixtures; frames, steps, clips, episodes, and hours are different units. Human video supplies objects, tasks, and motion priors but usually lacks actuator commands and touch. Real trajectories ground actions but are expensive to diversify. Simulation provides rewards and difficult scenarios while retaining contact and sensor gaps. Data value should be decomposed by scenes, embodiments, skills, recovery, and sensing modalities.

LeRobot provides dataset and robot interfaces, while Isaac Lab and ManiSkill provide learning and simulation infrastructure. Standard containers do not standardize control semantics. Joint ordering, rotation conventions, normalization, timestamps, calibration, and control periods still require explicit alignment.[R011][R013][R014]

### Benchmarks ask different questions

| Benchmark | Main target | Conditions that must match |
|---|---|---|
| LIBERO | Language manipulation and spatial/object/goal transfer | Suites, preprocessing, demonstration count, resets, rollout horizon [R007] |
| CALVIN | Sequences of language-conditioned subtasks | Environment split such as ABC-D; mean chain length is not success percentage [R008] |
| SIMPLER | Simulation proxies for particular real setups | Visual Matching versus Variant Aggregation, robot, control frequency [R009] |
| RoboTwin 2.0 | Bimanual manipulation, randomization, embodiment variation | Clean/randomized conditions, tasks, action interfaces [R010] |
| RMBench | Manipulation requiring historical information | Memory split, history length, checkpoint revision; retrained weights appeared in 2026 [R023] |
| RoboCasa365 | Composed kitchen skills and environment transfer | Version, task level, timeout; horizons increased 1.5x in May 2026 [R022] |
| BEHAVIOR-1K | Long household activities and interaction states | Challenge subset, observations, timeout, embodiment; not all 1000 activities solved [R012][R028] |
| MolmoSpaces | Multiple evaluation settings and scene coverage | Training data, action space, task coverage, adaptation, test date [R019] |

There is consequently no overall ranking of every model. High LIBERO performance after task-specific training and lower zero-shot performance in new scenes address different difficulties. A new model can also arrive with longer horizons, more sampled candidates, or larger images. Meaningful comparisons report training exposure to tasks, objects, scenes, and embodiments, as well as checkpoint version, control period, inference budget, and trial count.

### A proposed evaluation protocol

The following is a proposed research and engineering design, not an experiment performed in this repository. Use four levels: in-distribution skills; new objects, views, and language; new scenes and task compositions; and new embodiments plus sustained autonomous operation. Include disturbances, occlusions, failed grasps, and recovery at every level. Separate train, validation, and test data by scenes and collection sessions and document potential pretraining overlap.

A first baseline group holds action interface and data budget constant while comparing ACT/DP, adaptable VLAs, and structured-planning systems. A second fixes the backbone and varies single-step versus chunks, discrete versus flow generation, sensing, synchronous versus asynchronous execution, and memory. A third compares world models without search, with fixed-budget search, and with increased-budget search. When commercial training data cannot be controlled, interpret results as system acceptance tests rather than causal evidence about architecture.

Record task and complete-chain success, completion time, interventions per hour, recovery, collisions/drops/stops, median and tail observation-to-action latency, energy per task, and data/adaptation cost. Prespecify repetitions per task and condition and report confidence intervals. Stratify by task and scene rather than treating correlated clips as independent trials. Every attempt, including failures and timeouts, belongs in the log.

## A synthesis of model relationships

### Relationships are not one lineage

The relationship inventory distinguishes **explicit initialization/reuse, series evolution, method combination, system complementarity, and analytical comparison**. Weight inheritance or post-training on another model is claimed only when an original paper or official implementation says so. Sharing a transformer or flow objective establishes a common paradigm, not shared weights. Each recorded edge has evidence and a relationship type.

The first connection runs from **specialized imitation to general conditional policies**. ACT and DP address sequence modeling and multimodal control; RT, Octo, and OpenVLA emphasize broader task and embodiment coverage. Generalist models do not invalidate compact imitation baselines in fixed tasks with limited demonstrations or compute. Large VLAs also adopt chunks and generative heads. Matched task data are required to isolate the benefit of internet pretraining.

The second is **a more explicit division between semantics and action distributions**. RT-2 maps actions into a language-style token space; OpenVLA provides an open transfer route. PI, GR00T, MolmoAct2, and Xiaomi use continuous action experts to address fine control and long action sequences. FAST changes encoding, OFT changes adaptation and output recipes, and asynchrony changes scheduling. Representation, training, and runtime should not be collapsed into a succession of model generations.

The third is **complementarity between geometry and scale**. PerAct and RVT align scene and action geometry, while 3D Diffuser Actor adds generative action modeling. Strong semantic pretraining does not guarantee precise coordinates, collision boundaries, or contact states. Geometry can provide an inspectable interface at a calibration and compute cost. The source of spatial error should determine whether to combine these components.

The fourth is **convergence between world models and VLAs without identical roles**. GR-1/GR-2 use future prediction in action learning; GO-1 uses latent actions as an intermediate plan; Cosmos Policy adapts a video foundation model to actions, futures, and values; JEPA-AC searches through latent action consequences. These correspond to auxiliary supervision, intermediate representation, unified generation, and explicit planning. Deployment-time world-model planning should be claimed only when inference actually evaluates possible consequences.[R005][R006][W020][W021][W028][W035][W023][W025][W026]

The fifth is **integration of general reasoning with low-level whole-body control**. HumanPlus, SONIC, and Helix illustrate separate timescales for semantics, motion targets, and stabilization. A VLA emitting a whole-body joint vector has not automatically solved balance and contact; a stable locomotion controller does not automatically understand open-ended tasks. Their interface needs coordinates, timing, constraints, and failure feedback.

The sixth is **a feedback cycle connecting imitation and policy improvement**. PI's experience-learning work and HIL-SERL exemplify broad pretrained adaptation and bounded-task feedback optimization. Both use outcomes to improve behavior, but rewards, scale, released assets, and operating constraints differ. World models can reduce physical exploration cost while introducing errors that an optimizing policy may exploit.[R015][R016]

### Six useful direct comparisons

| Comparison | Actual distinction | Appropriate test |
|---|---|---|
| ACT versus DP | Latent-variable chunk prediction versus action denoising | Matched demonstrations and feedback interval: precision, failure, latency |
| OpenVLA versus OFT | Adaptation and output recipe around a reusable backbone | Fixed backbone and training budget |
| PI versus GR00T | Related continuous-expert paradigm with different backbones, mixtures, embodiments, versions | Pinned checkpoints and permissions; embodiment adaptation cost |
| V-JEPA-AC versus video world models | Compact latent consequences versus viewable futures | Fixed search time/candidates and real task success |
| Planner plus skills versus end-to-end VLA | Explicit subgoals versus a learned joint action interface | New compositions, failure recovery, grounding, module overhead |
| Helix/SONIC hierarchy versus arm-only VLA | Whole-body balance, contact frequency, and stabilization | Manipulation while moving, disturbances, multiple contacts |

## Engineering architecture and openness

A practical architecture separates data/calibration, state/history, task planning, action generation, control constraints, and feedback logging. Slower semantic inference may run on a server, an action expert near the robot, and servo control and stopping on deterministic control paths. Frequencies must follow hardware and measured requirements rather than System 1/System 2 terminology. Every executed command should be traceable to the observation, model, and normalization revision that produced it.

Audit openness along five axes: disclosed mechanism, inference code, weights, training code/recipe, and actual training data, then separately record license and use restrictions. A GitHub repository does not establish completeness along all five axes. Hardware recommendations do not prove real-time performance in every mode. Public data and intermediate checkpoints facilitate reproduction, but calibration, controllers, and recovery can still depend on unrecorded operational expertise.[R013][R014][R017]

Selection should start from task constraints. A fixed precision workstation can compare ACT/DP and HIL-SERL; language generalization and task sharing motivate adaptable VLAs; explicit spatial constraints motivate geometry; choices among consequences motivate world-model planning. For mobile manipulation, establish low-level stability before connecting general semantics. These are mechanism-based recommendations, not procurement rankings or deployment guarantees.

## Five future technical challenges

### Challenge 1: transferable action and contact representations

Sharing semantics across embodiments is easier than sharing actuator meaning. Joints, grippers, hands, control rates, and force sensing change the action distribution, while human video lacks command labels. Research should encode embodiment constraints, geometric goals, and contact states explicitly and use adaptation layers beneath shared policies. Tests should include new-embodiment demonstration requirements, contact-force error, insertion success, constraint violations, and post-transfer stability rather than source-robot success alone.

### Challenge 2: persistent memory, verifiable plans, and recovery

Tasks require remembering hidden objects, completed steps, and failed strategies. More video history increases cost and can preserve irrelevant context, while text plans can drift from actual state. Event memory, object-state graphs, explicit completion predicates, and recovery branches offer testable directions. RMBench and long-horizon benchmarks provide partial entry points, supplemented by real occlusion, moved objects, and interruptions. Report complete-chain success, recovery time, and persistence of incorrect memories.[R023][R012]

### Challenge 3: world models that support action decisions

A visually plausible future can be wrong for control, especially under contact, deformation, occlusion, or interaction with others. Longer planning amplifies error and can find simulator loopholes. Priorities include calibrated action conditioning, uncertainty, physical constraints, and correction from real feedback. Evaluation needs counterfactual action discrimination, agreement between predicted and real outcomes, fixed-budget planning gains, and conservative fallback under unexpected conditions.

### Challenge 4: jointly optimizing latency, energy, and control reliability

Large visual-language backbones, long histories, and iterative action generation compete for on-device resources, while buffering changes feedback age. Quantization, distillation, KV reuse, chunk scheduling, and control stability should be designed together and tested under disturbances. Tail latency, observation age, continuity, energy per task, and recovery matter alongside throughput. Xiaomi's asynchronous training provides a concrete reason to align training conditions with scheduling.[R024][R025]

### Challenge 5: auditable continual improvement beyond demonstrations

Selecting successful videos, reporting the best checkpoint, or hiding interventions overstates operational capability. Continual learning adds reward mismatch, forgetting, leakage, and rollback problems. Preserve all attempts, interventions, and failures, use independent-scene tests, and support reversible model releases. Track licenses for videos, scene assets, weights, and training data separately. Regression across versions, confidence intervals, human minutes, and sustained intervention rates reveal whether systems actually reduce human work.[R015][R019][R022]

## Reading and reproduction path

A useful progression is ACT/DP for action learning, SayCan/PaLM-E for grounding, RT/OpenVLA for transfer, PI/GR00T for continuous experts, PerAct/RVT for geometry, followed by JEPA/Cosmos and whole-body control. Reproduction should begin with a fixed robot, explicit action interface, and repeatable tasks before adding out-of-distribution changes and recovery. Simultaneously replacing sensors, embodiment, data, and model prevents clean causal interpretation.

The repository retains model cards, relationship edges, data and benchmark tables, a product matrix, evidence and uncertainty records, both report editions, and build/validation scripts. It provides literature analysis and an implementable evaluation design, not reproduced training results, third-party paper copies, weights, or raw robot data. Updates should record version changes in the source ledger and revalidate agreement between diagrams, tables, and prose.
