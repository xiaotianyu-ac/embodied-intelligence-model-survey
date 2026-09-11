## Whole-body control and navigation: turning model outputs into sustained action

Embodied systems span at least three problems: choosing a goal, generating executable short-term actions, and remaining stable under contact and disturbance. A model that can describe loading a dishwasher does not thereby provide balance, obstacle avoidance or grasp control. Relationships between models should first be located within this hierarchy; advances in motor control often complement a VLA rather than replace it.[H008][H011][H019]

### From demonstrations to reusable motion priors

**DeepMimic (2018)** combines motion imitation with task rewards. Body state, phase and a goal condition a policy that produces joint targets and learns through physical feedback. Its contribution is to optimize resemblance and task achievement together. The original demonstrations concern simulated characters, including robot-shaped models; they do not establish deployment on physical Atlas hardware.[H001]

**AMP (2021) and ASE (2022)** shift emphasis from tracking a selected clip toward learning a distribution of movement. AMP uses a discriminator to provide a motion-style reward, reducing manual clip selection. ASE adds a latent skill interface so a higher-level policy can reuse the learned repertoire. ASE is an explicit methodological extension; the comparison with DeepMimic is an analytical change in problem formulation, not inherited weights. Natural movement still does not imply task correctness, and abrupt skill switching can create poor transitions.[H002][H003]

**PHC (2023)** asks whether tracking can continue after noisy inputs or falls. Progressive multiplicative control adds capacity for difficult motions and recovery, making reset avoidance part of the controller. Its central evidence concerns simulated avatars. Transferring this result to real actuators, sensors and physical human interaction remains a separate challenge.[H004][H005]

**Humanoid Transformer (2023)** instead uses observation-action history to autoregressively predict control actions, trained with model-free RL in randomized simulation. Behavior adapts through context without changing weights. This is contextual adaptation to execution dynamics, not the same capability as learning a new manipulation task from a demonstration video. Evaluation chiefly covers locomotion, terrain and disturbances.[H006]

### From human motion to autonomous-task data

**H2O and OmniH2O (2024)** retarget human motion, filter infeasible examples using privileged imitation, and train deployable tracking policies. OmniH2O explicitly follows H2O and makes kinematic pose a common interface for RGB, VR, generated motion and learned autonomous policies. A privileged teacher must be distilled into a student whose inputs exist at deployment. Changing the goal generator need not entail rebuilding the physical controller. Teleoperated trials must nevertheless be counted separately from autonomous trials.[H007][H008]

**HumanPlus (2024)** closes a data-collection loop. A low-level policy trained from 40 hours of human motion enables camera-based humanoid shadowing; resulting real-robot demonstrations support egocentric behavior cloning. A customized 33-DoF humanoid demonstrates multiple tasks. The useful sequence is human motion prior → practical teleoperation → robot task data → visual policy. Success on the reported small task set is not a measure of general competence across homes.[H009]

**MaskedMimic (2024)** represents heterogeneous commands as incomplete motion descriptions. Partial joints, paths, scenes or text constrain a motion-inpainting problem. Training obtains a fully constrained tracking teacher and then a conditional-VAE policy with randomized missing information. This admits multiple valid movements for an underspecified goal, rather than forcing one mean solution. The main evidence remains physics-based animation rather than a ready-made real-humanoid controller.[H010]

### SONIC: an explicit interface between VLA and motor control

**SONIC (2025 preprint; 2026 publication and engineering updates)** encodes human, robot and hybrid reference motions into a shared quantized token. A common decoder outputs desired joint positions for PD controllers. PPO tracking, auxiliary reconstruction and domain randomization train the interface; a runtime kinematic planner can convert intent into short reference movements. This connects VR, human video and VLA commands to one execution policy.[H011][H035]

The original paper fine-tunes GR00T N1.5 on 300 teleoperated demonstrations to produce head/wrist poses, waist height and base-motion commands, then executes those commands through SONIC. Its 20-trial, single-task experiment is explicitly a compatibility proof of concept, not a broad autonomy score. The inspected official repository now supplies an N1.7 workflow, training/deployment code and SONIC v1.1. Released controllers run at 50 Hz. Reference lookahead, neural inference duration and end-to-end teleoperation latency are different measurements.[H011][H012]

HoloMotion provides a 2026 extension-reading example of a reference-conditioned MoE transformer and motion-data-to-deployment pipeline. It reinforces the relevance of model/data scaling in whole-body control, but a foundation-model label alone does not establish unseen-contact robustness, arbitrary-terrain competence or certified safety.[H036]

### Navigation: local policies, global planning and spatial memory

**ViNT (2023)** learns transferable navigation from visual history and a goal image. Its transformer outputs local waypoints and a goal-distance estimate, while alternative goals can be encoded into the same interface. Long-distance behavior results from local policy, subgoal generation, topological representation and planning heuristics working together; it is not a single network directly producing every motor command.[H013][H014]

**NoMaD (2023 preprint / 2024 conference)** explicitly reuses ViNT's encoder. A diffusion action decoder represents alternative routes, while masking the goal lets one policy support both exploration and directed navigation. This avoids simply averaging incompatible paths around an obstacle. Sampling, path selection, local control and new observations remain part of the deployed loop. Low collision rates in an experiment are neither a formal collision guarantee nor a humanoid balance result.[H015]

**GOAT (2023)** addresses object and place memory across missions. Observations update an instance-aware semantic map; category, image or language goals identify a target; the system explores for unknown objects and reuses remembered evidence for known ones. It is a modular system, and adaptation primarily comes from updating memory. **GOAT-Bench (2024)** is the distinct lifelong-navigation benchmark. A local navigation policy, semantic memory and VLA could be complementary, but that architectural inference should not be presented as an implemented model lineage.[H016][H017]

### Commercial hierarchies and contextual adaptation

**Figure Helix → Helix 02** is an explicit version extension. The original model emphasizes upper-body control. Helix 02 adds S0: S2 supplies semantic goals; S1 produces full-body joint targets at 200 Hz; S0 handles fast balance/contact execution at 1 kHz. Figure discloses over 1,000 hours of retargeted human motion and simulated RL for S0, alongside palm vision and fingertip touch. Its four-minute room-scale task is a vendor demonstration, not a multi-environment reliability study. A unified system still contains distinct levels and update rates.[H018][H019]

**Skild Brain → S1** combines cross-embodiment learning with task adaptation. S1 describes episodic demonstration-conditioned pretraining and infers intent, progress and actions from a task video plus current context, without task-specific weight updates in the reported setting. The inspected article does not disclose a complete network, action parameterization or reproducible training recipe. Those fields remain unknown; the phrase general-purpose brain does not justify inventing a transformer or diffusion architecture.The public scaling study uses cumulative per-step scoring with human failure recovery; that score should not be equated with uninterrupted end-to-end autonomous task completion.[H020][H021]

**Generalist GEN-1 → GEN-1.5** offers a useful contrast. GEN-1 emphasizes reliability after selected-task adaptation; GEN-1.5 places sensorimotor demonstrations in a 30-second context and produces 100-Hz trajectories. Generalist says its contextual ability emerged without a dedicated ICL objective, whereas Skild describes demonstration-conditioned training. Inputs, training and test distributions differ, so a single success-rate ranking is inappropriate. Generalist also explicitly describes current tasks as short and its contextual policies as more brittle than fine-tuned ones.[H037][H038]

### Product progress and the strength of evidence

Reproducible models, development platforms, vendor demonstrations, customer-confirmed pilots and sustained commercial operation are different stages. Each deployment claim should name the robot, model version, human assistance and metric denominator.[H024][H029][H030][H040]

| Organization | Technology/product | Verified progress | Evidence boundary |
|---|---|---|---|
| Figure | Helix 02 / Figure 03 | BMW confirms the earlier Figure 02 pilot and new Figure 03 sequencing project; Figure publishes onsite demonstrations | Historical Figure 02 production statistics do not transfer to Figure 03 or Helix 02.[H039][H040] |
| Skild AI | Cross-embodiment Brain / S1 | Company reports paying deployments and new S1 pilots | Commercial totals are vendor statements across products; deploying, planned and piloting are distinct.[H022] |
| Physical Intelligence | π models integrated by partners | Weave laundry and Ultra warehouse customer-site accounts | Deployed versions differ from π0.7 research; remote intervention remains part of operation.[H023][H024] |
| NVIDIA | GR00T, SONIC, simulation and onboard stack | Released models/code/workflows and announced humanoid reference hardware | Hardware availability is stated as late 2026, not delivered by the cutoff.[H012][H025][H026] |
| Google DeepMind | Robotics 2 / ER 2 / On-Device 2 | July 2026 whole-body, multi-embodiment and local-execution releases | Reasoning API access, trusted testing and open control weights are different access categories.[H027] |
| Agility Robotics | Digit + Arc industrial service | GXO confirms a commercial RaaS deployment; vendor reports cumulative tote milestones | Counts omit denominators for failures, intervention and downtime; do not infer a disclosed VLA.[H030][H031] |
| 1X | NEO / Redwood / 1XWM | Ordering and 2026 delivery plans; world-model technical disclosure | Basic autonomy and scheduled Expert Mode are explicit; orders are not proof of a delivered autonomous fleet.[H028][H029] |
| Boston Dynamics | Electric Atlas and learned behaviors | Official manufacturing, industrial pilot history and scheduled deployment | Hardware productization does not establish model reproducibility or general long-term autonomy.[H032] |
| Unitree | G1 platform / UnifoLM-VLA | Official code, checkpoints and datasets | Hardware sales, model release and autonomous commercial usefulness need separate evidence.[H034] |
| Galbot | G1/S1 and AstraBrain | Official WAM/WBC/dexterity and industry-application positioning | First/largest/scaled-deployment language remains vendor positioning rather than a technical ranking.[H033] |
| Generalist | GEN-1 / GEN-1.5 | Early enterprise access and real-robot adaptation/context studies | High reliability on adapted tasks and one-shot performance on unfamiliar tasks are different conditions.[H037][H038] |

### Reading model relationships and engineering implications

Explicit relationships include AMP→ASE, H2O→OmniH2O, ViNT→NoMaD, Helix→Helix 02 and the released GR00T–SONIC composition. PHC versus SONIC, or SONIC versus Helix 02, can be compared as approaches to placing broad motor competence below goals, but there is no claim of shared weights or code. The relation catalog marks `explicit` and `analytical` separately.[H003][H008][H011][H012][H015][H019]

An engineering interface should specify coordinate frame, update rate, action hold duration, command expiry and control authority. Semantic decisions can tolerate slower updates; balance/contact feedback cannot wait for a remote reasoning round trip. Human references also require reachability and dynamic-feasibility handling. These are engineering deductions from the compared systems, not claims that every product uses the same implementation.[H007][H011][H019]

Unresolved issues include stability under unfamiliar contact and payloads; preservation of mechanical information across embodiments; automatic detection and recovery over minutes; and evaluation that jointly reports success, throughput, human time and failure cost. More natural motion, more realistic video or a larger network alone cannot settle these questions.[H009][H011][H024][H028]
