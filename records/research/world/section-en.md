## Representations, hierarchical reasoning, and world models

These models occupy different positions in a robot system. A representation encoder describes the current state; a hierarchical planner selects a subgoal; a policy produces controls; a world model predicts the consequences of candidate controls. A model can occupy several positions, but real robot capability requires perception, decision, execution, and feedback together. This chapter distinguishes reported experiments, official product descriptions, and analytical conclusions. Versions were checked through 11 September 2026.

### SayCan, PaLM-E, and EmbodiedGPT: connecting language reasoning to action

**SayCan (2022)** combines a language model's score for a skill's relevance with a value function's estimate of that skill's feasibility. It selects and executes a skill, then repeats. Its main training requirements lie in the skill policies and their value functions. The language model orchestrates abilities rather than generating joint commands. The original system receives environmental feedback primarily through current affordance values; its authors explicitly identify incomplete failure feedback as a limitation. The public tabletop simulation does not reproduce the full mobile manipulation stack.[W001]

**PaLM-E (2023)** embeds images and continuous robot state in the same dimensional space as language tokens. A decoder language model jointly trained on embodied and general multimodal tasks outputs textual plans for low-level policies, incorporating subsequent visual observations. The architectural change from SayCan is direct observation-conditioned reasoning. The 562B variant illustrates semantic transfer, not a 562B servo controller. Sensor grounding and downstream motor competence remain separate requirements.[W002]

**EmbodiedGPT (2023)** uses EgoCOT subgoal data derived from Ego4D to adapt a 7B language model with prefix tuning. Features extracted from planning queries inform downstream control. It explores a learned interface between visual evidence, subgoals, and action-relevant representations. Its benchmark improvements do not establish that verbal reasoning alone solves physical contact control.[W004]

### VIMA and VoxPoser: task specification and geometric grounding

**VIMA (2022 preprint; ICML 2023)** represents tasks with interleaved text, object images, and demonstration frames. T5 encodes the prompt; a causal transformer with cross-attention conditions on that prompt and interaction history to produce manipulation actions. More than 600,000 expert trajectories and four generalization levels test changes in objects, compositions, and task templates. This object-centric policy is an important multimodal interface, but should not be conflated with every VLA that inherits an internet-scale language model. Its principal evidence is procedural tabletop simulation; real perception and action transfer require additional work.[W003]

**VoxPoser (2023)** uses language-generated programs and vision-language components to construct three-dimensional affordance and constraint maps. A motion planner converts those maps into end-effector trajectories. Re-evaluating cached programs with new visual observations enables receding-horizon adaptation. This makes spatial objectives inspectable, but introduces dependencies on segmentation, calibration, reachability, and dynamics assumptions. No additional training of the core composition does not mean no pretrained perception, controller, or integration effort.[W005]

### R3M and VC-1: encoders are infrastructure

**R3M (2022)** learns visual features from Ego4D using temporal contrast, video-language alignment, and compactness regularization; downstream controllers can train on frozen features. **VC-1 (2023)** uses masked visual pretraining and CortexBench to study transfer across sensorimotor tasks, model scales, and data mixtures. Domain adaptation materially affects results. Neither encoder alone supplies actions, a long-horizon plan, or an action-conditioned transition model.[W006][W007]

The analytical relationship to VLA is modular rather than a simple replacement lineage. An encoder can support a policy, reward estimator, retrieval system, or world model. Comparisons should hold controller architecture, demonstrations, cameras, and fine-tuning protocol fixed; otherwise apparent representation gains may come from other components.

### PerAct, RVT, and 3D Diffuser Actor: geometry and generative actions

**PerAct (2022)** converts RGB-D observations into a voxel grid, combines voxel patches with language in a Perceiver, and classifies the next end-effector location and discretized orientation/gripper state. Aligning observations and actions in three-dimensional coordinates provides a useful prior for limited demonstrations. The costs include voxel resolution, memory, and calibration sensitivity; experiments cover RLBench and a small real robot task collection.[W008]

**RVT (2023)** tackles the compute cost of explicit three-dimensional representations by rendering virtual views of the workspace and fusing them with cross-view attention. It predicts gripper poses while retaining geometric grounding. Relative to PerAct, the main change is how spatial information is computed. Reported speedups depend on the authors' implementation, hardware, and matched-performance target.[W009]

**3D Diffuser Actor (2024)** combines spatial tokens with diffusion over end-effector translations and rotations, using three-dimensional relative attention during denoising. Its target is a multimodal **action distribution**, not future video. RLBench keyposes still require a low-level planner to reach them. The official implementation documents quaternion conventions and differences between evaluation protocols, illustrating why action coordinates and environment versions must accompany success-rate comparisons.[W010][W011]

### DreamerV3: learning consequences and improving behavior in imagination

**DreamerV3 (2023 preprint; 2025 Nature publication)** is a model-based reinforcement learning algorithm, not one pretrained checkpoint that controls every robot. It learns recurrent latent dynamics, reward, and continuation from interaction, trains an actor–critic on imagined trajectories, and incorporates new real experience. Normalization, transformations, and loss balancing improve cross-domain stability.[W012][W013]

Control optimization uses compact latent states even if image reconstruction helps training. Unlike typical behavior-cloned VLA, policy improvement explicitly exploits predicted outcomes and rewards. One configuration across tasks does not mean one set of weights solves every task zero-shot. Exploration cost, reward specification, and accumulated model error remain obstacles in physical deployment.

### UniSim: generated experience as a training environment

**UniSim (2023 preprint; ICLR 2024)** combines heterogeneous image, video, navigation, and robot datasets in a conditional video generator. High-level language or low-level controls specify the next interaction. Iterative generation provides experience for training planners and reinforcement learning policies; the paper demonstrates transfer in particular real tasks.[W014][W015]

Its contribution is a path from video generation to action-conditioned training trajectories. For engineering use, one must verify that controls causally affect predicted outcomes, failures remain visible, and policies do not exploit simulator artifacts. This is Yang and colleagues' generative interaction model, not the separate autonomous-driving sensor simulator with the same name.

### Genie 1, 2, and 3: interactive environments and their limits

**Genie (2024)** learns a video tokenizer, latent action model, and dynamics predictor from videos without ground-truth control labels. Inferred latent actions are not automatically robot motor commands. **Genie 2 (December 2024)** uses autoregressive latent diffusion conditioned on past frames and actions. **Genie 3 (August 2025)** demonstrates 720p, 24-frame-per-second interactive environments with consistency lasting minutes. Project Genie subsequently provided a restricted product prototype in 2026.[W016][W017][W018][W019]

The series advances generated environments and agent training substrates. Genie 3's official limitations include restricted agent actions and difficult multi-agent interactions; prompt-triggered environmental events need not be actions performed by the agent. Navigating generated worlds or rendering a robot does not validate physical contact precision, torque control, or long-term safety. The checked official pages do not disclose Genie 3's complete training data and architecture, so Genie 2 internals should not be presented as verified Genie 3 internals.

### GR-1 and GR-2: video pretraining for direct robot policies

**GR-1 (2023)** pretrains on video and adapts to robot trajectories. A GPT-style model consumes language, image history, and robot state while predicting both future images and actions. Visual prediction supplies temporal supervision, but action outputs can be executed without explicitly searching multiple imagined futures. **GR-2 (2024)** scales video pretraining to 38 million clips and more than 50 billion tokens, followed by joint video-action adaptation.[W020][W021][W022]

This family bridges video models and VLA: it adds temporal priors to semantic understanding and executable actions to generative modeling. Joint prediction alone does not establish model-predictive control at inference. GR-2's 97.7% concerns the 105-task Simple setting; unseen manipulation is substantially harder. It does not establish success in arbitrary homes or robot embodiments.[W036] Access to the complete pretraining corpus and reproducible training setup requires separate scrutiny.

### V-JEPA 2, 2-AC, and 2.1: latent prediction and planning

**V-JEPA 2 (2025)** predicts masked video representations rather than reconstructing every pixel. **V-JEPA 2-AC** post-trains an action-conditioned predictor using fewer than 62 hours of DROID robot video and recorded actions. Image-goal features guide receding-horizon planning on real Franka arms. Zero-shot deployment means no environment-specific or task-specific training there; it does not mean arbitrary robot control emerges from action-free video alone.[W023][W024][W026]

**V-JEPA 2.1 (March 2026)** adds dense predictive supervision for visible and masked tokens, intermediate-layer supervision, joint image/video tokenization, and scaling. Its robot experiments reuse the 2-AC predictor architecture, public code, and planning protocol. After replacing the visual encoder, the action-conditioned predictor is retrained on DROID; this is not direct inheritance of trained 2-AC predictor weights. Table 6 shows cup-grasp success improving from 60% to 70% at approximately three seconds of planning. Reaching 80% uses a longer horizon and approximately fourteen seconds. The widely summarized twenty-percentage-point gain therefore includes more planning compute. Each skill has only ten evaluated tasks, and gripper timing remains a failure mode.[W025][W026]

Analytically, latent prediction retains task-relevant changes while avoiding unnecessary visual detail; generative video preserves interpretable observations. These approaches can coexist: latent search can reduce planning cost and image generation can support inspection or synthetic data. The decisive question is whether the representation preserves information about contact, occlusion, and failure.

### Cosmos Predict, Cosmos Policy, and Cosmos 3

**Cosmos Predict 2.5** generates world video conditioned on text, images, or video; **Transfer 2.5** transforms scenes using controls such as depth or segmentation. These are initially environment and data-generation components, not robot controllers.[W027]

**Cosmos Policy (January 2026)** explicitly adds executable actions by fine-tuning Cosmos-Predict2-2B on target-platform demonstrations. It represents action chunks, future observations/proprioception, and values as latent frames within the existing diffusion process. It supports both direct action sampling and best-of-N planning over predicted outcomes and values. The paper separates direct-policy and planning evaluations; additional rollout data can improve the learned dynamics and value function. The extra search cost must accompany claims of higher success.[W028][W035]

**Cosmos 3 (released May 2026; checked through September)** combines an autoregressive reasoning tower with a diffusion generation tower using a Mixture-of-Transformers architecture. The current official repository lists Super 64B, Nano 16B, Edge 4B, and DROID-adapted policy checkpoints. Edge has resolution and video-transfer restrictions; recommended embedded hardware does not make every inference mode real-time. The checked repository currently uses OpenMDW-1.1, which should not be replaced with a license description copied from an older Cosmos generation. Complete pretraining reproducibility, hardware latency, and transfer to unfamiliar embodiments require checkpoint-specific evaluation.[W029][W030]

### GAIA-2, 3, and 4: the autonomous-driving boundary

**GAIA-2 (March 2025)** generates controlled multi-camera futures; **GAIA-3 (December 2025)** emphasizes evaluation. **GAIA-4 (August 2026)** places the AI Driver in a generated sensor loop, including camera and radar output. In world-on-rails mode, other road users retain logged trajectories for controlled counterfactual comparison; an optional reactive-agent mode allows selected participants to respond to the ego vehicle.[W031][W032][W033]

These are driving data and validation systems, not direct evidence for general manipulation. The transferable lesson is to assess visual fidelity, closed-loop behavioral consistency, and agreement on outcomes separately. Safety implications depend on scenario coverage, sensor accuracy, behavioral assumptions, and counterfactual fidelity. The checked GAIA-4 publication does not provide enough architecture and training-data detail for full reproduction, so it remains official system-level evidence.

### Relationships and architecture choices

| Relationship | Interpretation | Evidence category |
|---|---|---|
| SayCan → PaLM-E | Skill relevance/affordance interfaces versus observation-conditioned language planning | Analytical comparison; no weight lineage asserted |
| R3M / VC-1 ↔ policies | Reusable perception with separately trained control heads | Modular complement |
| PerAct → RVT | Similar spatial action grounding with a different geometric compute path | Explicit paper comparison |
| Geometry + diffusion → 3D Diffuser Actor | Spatial attention conditions action denoising | Explicit method combination |
| GR-1 → GR-2 | Scaling video pretraining and joint video-action modeling | Family/method progression |
| V-JEPA 2 → 2-AC; 2.1 encoder + 2-AC framework | Encoder-family extension; predictor architecture and planning reuse with retraining | Branching extension/framework reuse, not weight inheritance |
| Cosmos Predict2 → Cosmos Policy | Video initialization adapted to actions, future state, and value | Explicit initialization |
| Earlier Cosmos lines → Cosmos 3 | Joint reasoning and generation architecture | Official evolution; not a claim of direct weight inheritance |
| Genie / UniSim / GAIA ↔ policies | Generated training or evaluation environments | System division of labor |
| Dreamer ↔ VLA | Outcome-based policy improvement can complement demonstration-based initialization | Analytical combination |

Choose the missing capability before choosing a model family. Skill composition suggests hierarchical planning; inadequate spatial precision suggests better geometry and action representations; abundant action-free video suggests representation or video pretraining; comparing alternative action consequences motivates explicit world-model planning. **MoLe-VLA is a dynamic layer-skipping efficiency method, not a world model.**[W034] Tasks involving tactile contact, persistent occlusion, human collaboration, and long-term state require additional feedback and state estimation beyond these visual approaches.
