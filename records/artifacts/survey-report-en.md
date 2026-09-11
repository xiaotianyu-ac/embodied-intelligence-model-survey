# Embodied Intelligence Models: Progress, Mechanisms, and Relationships

**Contents**

- [1. Scope and central findings](#1-scope-and-central-findings)
- [2. A common decomposition and the technical foundations](#2-a-common-decomposition-and-the-technical-foundations)
- [3. Manipulation policies and VLAs: from imitation to transferable robot foundation models](#3-manipulation-policies-and-vlas-from-imitation-to-transferable-robot-foundation-models)
- [4. Representations, hierarchical reasoning, and world models](#4-representations-hierarchical-reasoning-and-world-models)
- [5. Whole-body control and navigation: turning model outputs into sustained action](#5-whole-body-control-and-navigation-turning-model-outputs-into-sustained-action)
- [6. Additional decompositions: data, feedback, and execution](#6-additional-decompositions-data-feedback-and-execution)
- [7. Data and evaluation: establishing actual progress](#7-data-and-evaluation-establishing-actual-progress)
- [8. A synthesis of model relationships](#8-a-synthesis-of-model-relationships)
- [9. Engineering architecture and openness](#9-engineering-architecture-and-openness)
- [10. Five future technical challenges](#10-five-future-technical-challenges)
- [11. Reading and reproduction path](#11-reading-and-reproduction-path)

## 1. Scope and central findings

Progress in embodied intelligence connects semantic knowledge learned from internet data, action experience learned from physical interaction, and dynamics learned in simulation within a perception-action feedback loop. Parameter count and humanoid appearance alone miss decisive factors: data distributions, action interfaces, execution latency, and low-level control. This review focuses on robotic manipulation, navigation, and whole-body control, with driving world models as an adjacent reference. It does not attempt to survey all autonomous-driving perception, SLAM, or classical control.

Evidence was checked through **September 11, 2026**. The methodology is a technical scoping review: foundational work, original papers, author projects, official code, and product documentation are followed along research lines and updated with verified 2026 releases. This is not an exhaustive database-based systematic review with a measured retrieval recall, and no robot experiments were reproduced. Completeness refers to coverage of mechanisms, relationships, data, evaluation, engineering, products, and open problems within this scope. Paper results, vendor claims, and analytical judgments are distinguished; undisclosed architecture or training data are not inferred.

Five findings organize the report. First, **embodied intelligence is broader than a single VLA model**: representation, planning, action generation, prediction, and servo control are composable roles. Second, action generation increasingly uses chunks, diffusion, and flow matching, accompanied by asynchronous execution; these are design dimensions rather than one mandatory replacement chain. Third, world models need evidence of useful consequences, planning, or data generation; visual realism alone does not establish robot capability. Fourth, cross-embodiment data, domain adaptation, and feedback learning connect pretraining with deployment, while standardized file formats do not eliminate dynamics differences. Fifth, sustained reliability, contact feedback, and fair evaluation remain major gaps between demonstrations and operation. The model evidence and experimental conditions below support these findings.

## 2. A common decomposition and the technical foundations

### Locate the model within the feedback loop

![Closed-loop model roles](../../figures/architecture.svg)


Let o_t include available images, depth, proprioception, and force or touch; let g denote the task, h_t history, and e the embodiment. An action policy can be written pi(a_t:t+H | o_t, h_t, g, e). A world model predicts p(z_t+1 | z_t, a_t, e), a high-level planner selects subgoals or skills, and a controller turns desired poses, velocities, or joint targets into execution. This is an analytical decomposition; it does not assume that every system implements separately named modules.

| Role | Input and output | Representative lines | Essential verification |
|---|---|---|---|
| Visual/multimodal representation | Images or video to useful features | R3M, VC-1, V-JEPA | Improvements with downstream head and data held fixed |
| Semantic/hierarchical planning | Instruction and state to subgoals, skills, constraints | SayCan, PaLM-E, VoxPoser, Gemini ER | Feasibility, failure detection, replanning |
| Action policies and VLAs | Observations and task to actions or chunks | ACT, DP, RT, OpenVLA, pi, GR00T | Closed-loop success, latency, adaptation cost |
| World models | State and action to possible futures | Dreamer, UniSim, JEPA-AC, Cosmos | Effective conditioning, faithful consequences, planning gain |
| Whole-body and servo control | Proprioception and targets to frequent joint control | AMP, PHC, HumanPlus, SONIC, Helix S0 | Balance, contact, disturbance recovery, hardware constraints |

This separation explains apparently competing models. A visual encoder can serve different action heads, a VLA can call a whole-body controller, and a world model can produce training experience for an existing policy. Treating a language generator as a motor controller, or a video predictor as a deployable policy, obscures both interfaces and the evidence required.

### Eight questions for every model

The decomposition asks: **What bottleneck is addressed? What is observed? How are modules connected? What action representation is produced? Which data and objectives train it? How are execution and feedback organized? Which design contributes the improvement? What limitations remain?** Parameter count is supplementary. For commercial systems without public architectures or training pipelines, only disclosed interfaces and system roles are described, with unknowns retained explicitly.

Even two systems described as a VLM plus an action expert may differ substantially. Is the VLM frozen? Does the expert read output features or layerwise KV states? Is training autoregressive, diffusion-based, or flow-matching? Are outputs normalized absolute joints or end-effector increments? How far ahead does the model predict, how much of that prediction is executed, and when does a new observation influence action? These choices determine adaptation requirements, throughput, and responsiveness.

### Action representation determines transfer and control costs

Discrete action tokens quantize continuous values into classification targets that fit autoregressive language modeling, at a cost determined by sequence length, precision, and decoding. Direct continuous regression is simpler, but a conditional mean can fall between two individually feasible trajectories. Latent-variable and denoising approaches represent multimodal action distributions. Chunking predicts multiple timesteps together and improves coherence while creating a scheduling problem between observation and execution.

End-effector poses expose task geometry shared across arms but depend on inverse kinematics and reachability. Joint commands align more directly with hardware but bind the policy to joint order, offsets, and degrees of freedom. Torque outputs expose dynamics more directly to learning. Voxels, point clouds, and multiple views provide geometric inductive biases; force and tactile sensing reveal contact states hidden from vision. No representation dominates every task and embodiment; precision, data coverage, and the controller interface determine suitability.

### Learning objectives and their relationships

Behavior cloning maximizes the conditional likelihood of demonstrated actions and provides useful initial skills, but distribution shift and missing recovery examples remain problematic. ACT-style latent-variable models and chunking improve trajectory modeling. Diffusion Policy learns to denoise action sequences, while flow matching learns a continuous velocity field transporting a noise distribution toward an action distribution, typically sampled by numerical integration. Both are conditional generators; neither automatically constitutes a model of the physical world.

World models learn transitions in latent or video space. Model-based reinforcement learning uses imagined trajectories to improve a policy during training, whereas model predictive control searches candidate actions during deployment. Both consider the future but at different stages. Reinforcement learning and experience-based post-training use rewards and corrections and can build on behavioral initialization. A rigid pretraining-to-cloning-to-RL sequence is not universal either.

### Control rate and asynchronous execution require system-level accounting

Predicting H steps does not require waiting H steps before observing again: a system can execute a K-step prefix and replan, or infer the next chunk while buffered actions run. Asynchrony needs timestamp alignment, consistency with committed actions, removal of expired actions, and interruption under disturbances. With end-to-end latency L and control interval dt, merely covering the inference delay requires approximately ceil(L/dt) buffered actions; excessive buffering makes control depend on stale observations. This is a scheduling constraint, not an empirical performance claim.

Xiaomi-Robotics-0's training prefixes and alignment, V-JEPA's planning budgets, and Helix/SONIC's hierarchical execution provide concrete examples later. Evaluation should record inference latency, observation age at actuation, jitter, control frequency, and success together. Actions generated per second are not the same as closed-loop robot responsiveness.


## 3. Manipulation policies and VLAs: from imitation to transferable robot foundation models

A VLA is more than a language model placed upstream of an arm. It aligns semantic information, visual observations, robot state and an action distribution through a trainable interface. Three questions organize the field: where knowledge comes from, how actions are represented and generated, and how predictions enter a real-time feedback loop. Parameter count, diffusion and dual-system branding each describe only part of that system.

Behavior cloning remains the underlying learning procedure for many robot foundation models. Diffusion, flow matching, action tokens and continuous regression are primarily alternative policy representations and objectives; using one does not establish that a model learns through autonomous reinforcement. RECAP makes a different change by introducing rewards, value estimation and policy-generated experience into training.[^1][^3][^25]

### Action representations and architectural consequences

| Route | Prediction and objective | Representative work | Benefit | Cost to inspect |
|---|---|---|---|---|
| Discrete controls | Action bins with classification/token prediction | RT-1, RT-2, original OpenVLA | Compatibility with transformer/VLM training | Resolution, sequence length and autoregressive latency |
| Continuous chunk regression | Multiple actions with L1/L2 supervision | OpenVLA-OFT | Parallel outputs and simple training | Conditional median/mean behavior for multimodal targets; language following |
| Continuous generative policy | Iterative generation of an action chunk from noise | Diffusion Policy, pi0, GR00T, SmolVLA | Continuous precision and multimodal distributions | Sampling cost and stale observations |
| Compressed action tokens | DCT, quantization and BPE on chunks | FAST, pi0-FAST | Less temporal redundancy | Compression error; training speed differs from feedback speed |
| Latent actions | Video-derived abstract action followed by a robot decoder | OpenDriveLab UniVLA | Learning without physical action labels | Loss of contact, reachability or control detail |

The routes can coexist. pi0.5 uses discrete auxiliary action training and a continuous expert. Octo combines robot pretraining with a diffusion head. GR00T uses a module called a DiT but trains action generation with flow matching. Module names alone do not identify equivalent training algorithms.[^6][^8][^15][^19][^21][^31][^47]

### Model decomposition: imitation and early foundation policies

**ACT (2023).** Small imitation errors accumulate over long tasks, while low-cost bimanual demonstrations vary. ACT takes multiview images and joint state into a transformer conditional VAE and predicts a joint-position chunk. Training combines action reconstruction with latent regularization; deployment uses a zero latent and combines overlapping predictions. Chunking improves fine manipulation from demonstrations, but the original method contains neither a general language foundation model nor guaranteed out-of-distribution force-control skills.[^1][^2]

**Diffusion Policy (2023).** A scene can admit several valid actions. This policy models continuous action sequences through conditional denoising, with visual/state encodings supplying context. At deployment it samples a chunk, executes a prefix and observes again. It establishes a foundation for subsequent generative policies, but iterative sampling costs computation, and the original visuomotor policy is not automatically a web-pretrained VLA.[^3][^4]

**RT-1 (2022).** To learn from diverse robot tasks at scale, RT-1 combines EfficientNet, language FiLM, TokenLearner and a transformer. It maps a short image history and instruction into discretized arm/base controls and a termination mode. The original dataset exceeds 130,000 episodes and 700 tasks; the policy runs at approximately 3 Hz. Its contribution is scalable multitask behavior cloning, with robot/task coverage still concentrated and language conditioning distinct from general reasoning.[^5][^6]

**RT-2 (2023).** The question shifts from scaling robot data to transferring web semantics into control. PaLI-X or PaLM-E is co-fine-tuned on robot trajectories and vision-language tasks; binned actions become text tokens and are decoded back into controls. This supports semantic object selection and instruction generalization, but new semantics do not create unseen motor skills automatically. Autoregressive inference also adds latency. RT-2 is a research successor to RT-1, not continued training of RT-1 weights.[^7][^8]

**RT-X / Open X-Embodiment (2023).** This is a cross-robot data and modeling framework with RT-1-X and RT-2-X variants, rather than one unique architecture. The initial report pools 22 embodiments, standardizes data interfaces and demonstrates positive transfer. Deployment must still restore target-specific action meaning, coordinates, units and frequency: a common storage schema does not remove dynamics differences.[^9][^10]

**Octo (2024).** Octo pretrains a transformer diffusion policy on 800,000 OXE trajectories. Tasks can be given through language or goal images; modular inputs and action heads permit sensor/action adaptation. Inference samples a continuous chunk and replans after partial execution. Its role is a transferable robot-policy initialization, without requiring a giant language decoder; new platforms still need interface adaptation and fine-tuning.[^11][^12]

**OpenVLA (2024) and OpenVLA-OFT (2025).** OpenVLA combines DINOv2/SigLIP visual features with Llama 2, learning discrete actions from approximately 970,000 demonstrations as a public 7B reference. OFT explicitly adapts that foundation with parallel decoding, action chunking, continuous outputs and L1 regression. It demonstrates the importance of output and fine-tuning design. However, L1 favors a conditional median; multimodal behavior and language grounding need separate evaluation. One benchmark does not prove regression universally superior to diffusion.[^13][^14][^15][^16]

### The pi family: continuous control, hierarchy, experience and memory

**pi0 (2024).** Multiview images, text, proprioception and noisy actions enter a PaliGemma 3B backbone with a roughly 300M action expert. Flow matching transforms noise into continuous chunks; the paper uses 50-action chunks and caches the observation prefix during sampling. Broad private/public robot pretraining is followed by high-quality task post-training. Generalist initialization and specialist dexterity results should therefore be distinguished.[^17][^18]

**FAST / pi0-FAST (2025).** FAST is a representation: DCT, quantization and BPE turn temporally redundant action chunks into shorter discrete sequences. pi0-FAST is the autoregressive model using that representation; FAST itself is not a new robot architecture. Compression improves the utilization and training of high-frequency action data, but autoregressive latency remains, and compression ratio is not a feedback-speed metric.[^19][^20]

**pi0.5 and knowledge insulation (2025).** The model retains the VLM/action-expert design and separates language-level subtasks from low-level continuous actions while mixing robot and nonrobot semantic data. Knowledge insulation blocks gradients from the action expert into the VLM, yet discrete-action and vision-language objectives still train the backbone. It is therefore not simply backbone freezing. The public openpi implementation supports only the pi0.5 flow head and should not be assumed to reproduce every training head in the paper.[^21][^22][^20]

**pi0.6 and pi-star-0.6 / RECAP (2025).** The pi0.6 model card specifies a Gemma 3 4B backbone and approximately 860M action expert, retaining pi0.5's hierarchy. RECAP adds offline reinforcement pretraining, demonstrations, corrective takeovers and reward-labeled autonomous rollouts. A value function provides advantages, and deployment conditions the policy on high advantage. A stronger supervised base and an experience-trained policy are different claims; throughput gains still depend on task, rewards and intervention infrastructure.[^23][^24][^25]

**MEM / pi0.6-MEM (2026).** To address occlusion, long workflows and repeated failures, MEM combines compressed short-term visual history with long-term language memory. Past attempts can then guide changed behavior, and completed subtasks remain available to the policy. The evidence concerns within-task memory and contextual adaptation, not indefinite lifelong or cross-user retention. State loss and incorrect summaries remain distinct failure modes.[^28]

**pi0.7 (2026).** Its paper explicitly retains the pi0.6 architecture and MEM while expanding conditioning: task/subtask, quality, speed, control mode and visual subgoals permit robot, human and suboptimal autonomous experience to be combined. At deployment a high-level semantic policy can provide subtasks and a lightweight BAGEL-based world model can supply visual goals to the continuous expert. The model shows skill composition and absorption of RL-specialist experience, but some new tasks use stepwise language coaching or high-level adaptation rather than one fully autonomous zero-shot prompt.[^26][^27]

The inspected public openpi README lists pi0, pi0-FAST and pi0.5. The existence of pi0.6/pi0.7 papers and demonstrations does not establish release of their latest weights or complete data.[^20]

### GR00T and compact VLAs: scale, embodiment interfaces and execution

**SmolVLA (2025).** Designed for smaller compute budgets and community robots, it uses truncated SmolVLM2 with an approximately 100M action expert, totaling roughly 450M parameters. Images, language and projected state condition flow-generated chunks; the VLM is frozen and the expert learns from LeRobot community and target data. Compact modeling and asynchronous execution lower the experimentation barrier. Synchronous, per-step-feedback and asynchronous evaluations nevertheless have different protocols and cannot be merged into one universal frequency or success rate.[^29][^30]

**GR00T N1 (2025).** Eagle encodes vision and language; a cross-attending DiT combines these features with embodiment-specific state/action MLPs to generate continuous chunks. Flow training mixes real robots, simulation, generated trajectories and video-derived latent actions. Like pi0, it joins semantic representations with generative control, but its interfaces and data differ; this does not imply shared weights. The System 2 label does not require explicit textual planning.[^31]

**N1.5 (2025).** It improves and freezes the Eagle VLM, adds FLARE alignment with future latent features and expands data including DreamGen. Future-feature alignment is not full future-pixel generation. The authors explicitly note that new verbs supplied through synthetic trajectories are still trained skills, not unrestricted unseen-action generalization.[^32]

**N1.6 (2025).** Its technical page specifies an internal Cosmos-2B variant, a 32-layer DiT, unfrozen upper VLM layers and state-relative actions for most embodiments. Added data covers YAM, AgiBot, BEHAVIOR and Unitree G1. The page also identifies small-data relative-action accumulation, overfitting and language/OOD generalization as unresolved issues, highlighting action spaces and normalization as substantial engineering decisions.[^33]

**N1.7 (2026).** NVIDIA's engineering page describes Cosmos-Reason2-2B/Qwen3-VL, a roughly 3B checkpoint, around 32,000 hours of real/human data plus 8,000 simulated hours, and ONNX/TensorRT export. At inspection the official repository labels N1.7 GA. Its License section distinguishes Apache 2.0 code from weights under the NVIDIA Open Model License. A broader Apache 2.0 commercialization statement elsewhere in the README should not be read as applying the code license to weights; older early-access FAQ wording also requires version checking. Commercial availability is not demonstrated reliability in every field setting.[^34][^35]

One source discrepancy is retained: the N1.6 technical page calls its backbone an internal Cosmos-2B variant, whereas the later N1.7 engineering article loosely describes its predecessor as Eagle. This survey follows the version-specific technical page rather than treating the broader wording as a precise architectural statement.[^33][^34]

### Gemini Robotics: action and embodied-reasoning branches

**Gemini Robotics / ER (2025).** The VLA maps images, language and robot state into movement; ER is a VLM for spatial understanding, task reasoning and tool use. The pair can form a hierarchical system, but ER alone is not a torque-producing controller. Reports establish Gemini-based robot capabilities, while full VLA weights and training corpora remain restricted. Undisclosed action losses and parameter counts must not be invented.[^36][^37]

**Gemini Robotics 1.5 / ER 1.5 (2025).** Motion Transfer and interleaved reasoning/actions extend the VLA, while ER handles tools, plans and progress. Training covers ALOHA, bi-arm Franka, Apollo and web multimodal data. Its significance is cross-embodiment skill transfer and task-level orchestration. Some long-horizon Franka experiments add post-training, so the claim of operation without embodiment-specific post-training does not describe every result.[^38][^39]

**ER 1.6 (2026).** Its model card identifies a Gemini 3.0 Flash foundation, targeting pointing, spatial relations, instrument reading and multiview success detection. Outputs remain text/spatial representations and tool calls. This is a reasoning-branch upgrade, not a new motor decoder. The authors note that single-view and multiview success detection use different examples, and instrument tests differ in agentic-vision support; these plots are not all matched-condition comparisons.[^40][^41]

**Robotics 2, ER 2 and On-Device 2 (2026).** The July 30 release separates three roles: Robotics 2 for whole-body and dexterous action, ER 2 for understanding, planning and multi-robot coordination, and On-Device 2 for local execution and embodiment adaptation. ER 2's card identifies Gemini 3.5 Flash. On-Device 2 instead explicitly builds on Robotics 1.5 technology and on-device Gemma; it is not simply the full cloud model moved onto a device.[^42][^43][^44]

Robotics 2's published experiments still show significant multifinger and speed limitations. At launch ER was available through AI Studio, while VLA and On-Device models were for early-access partners. Local execution, API access and public weights are separate properties. Missing training losses, architectural details and full data inventories remain undisclosed.[^42][^44]

### Additional representative approaches and name disambiguation

**RDT-1B (2024).** A 1.2B robotics diffusion transformer combines language, images, state and control frequency for bimanual action generation. A physically interpretable unified action space supports heterogeneous pretraining, followed by bimanual fine-tuning. The contribution is physical meaning in the transfer interface, rather than merely padding vectors to equal length. Units, masks and coordinate conventions still require careful mapping.[^45][^46]

**OpenDriveLab UniVLA (2025).** Video frame pairs and task text train a VQ-VAE latent-action model in DINO feature space. A VLA predicts these task-relevant latent actions, and target-robot supervision trains a lightweight decoder. This exploits human videos lacking physical robot-action labels, but abstract actions still require embodiment grounding and can omit fine contact or dynamics information.[^47][^48]

**BAAI UniVLA (2025).** A separate same-named work starts from Emu3, representing vision, language and actions with discrete tokens and using world-model video post-training to improve policy learning. Authors, paper identifiers and mechanisms differ: task-centric latent actions versus unified multimodal generation. Its repository also displays CALVIN results with increased inference steps, requiring budget alignment before comparison.[^49][^50]

**X-VLA (2025).** Florence-Large handles the main visual/language stream while auxiliary wrist views are encoded separately. Data-source/embodiment soft prompts and input/output projections adapt heterogeneous observations and controls; a standard transformer generates flow-matching action chunks. This separates shared capability from hardware-specific parameters, but soft prompts do not remove configuration or adaptation requirements for unseen hardware.[^51][^52]

**LingBot-VLA 2.0 (2026).** A Qwen3-VL-based backbone, sparse MoE action expert and future semantic/depth distillation combine scaling with predictive control. Its approximately 60,000 curated hours comprise 50,000 robot hours across 20 configurations and 10,000 human egocentric hours. The 55-dimensional canonical interface includes four reserved slots and expands to head, waist, base and dexterous hands. The reported mixed-training GM-100 table evaluates nine tasks, and two long-horizon tests use 15 trials per setting; it does not establish that the entire benchmark or general OOD manipulation is solved.[^53][^54]

### Model relationships and defensible comparisons

Five relationship types matter: architecture/checkpoint inheritance, data reuse, auxiliary modules/objectives, training-procedure changes and system composition. OpenVLA to OFT is explicit adaptation; OXE to Octo/OpenVLA is a data relationship; pi0.6 to RECAP is RL post-training; MEM to pi0.7 is module inheritance; ER 2 and Robotics 2 are complementary components. Shared design among pi0, GR00T and SmolVLA does not prove checkpoint inheritance. The relationship catalog separately labels explicit evidence and analytical interpretation.[^11][^13][^15][^25][^26][^31][^42]

Execution comparisons must separate policy-call latency, actions generated per call, actual observation-refresh rate, low-level servo frequency and successful tasks per hour. RTC generates the next chunk while current actions execute and conditions on the committed prefix to maintain continuity. This is scheduling and conditioning, not additional semantic knowledge. Longer chunks can improve action-generation throughput while delaying response to new observations.[^55]

Matched evaluation requires the same robot, task and scene splits; training data and pretraining exposure; action space and control frequency; sampling steps, retries and adaptation protocol. LIBERO success, CALVIN chain length, GM-100 progress, long-task completion and hourly throughput measure different things and should not form one universal leaderboard. Cross-embodiment zero-shot claims must specify whether the novelty concerns objects, scenes, skills, bodies, or merely a skill–body combination.[^15][^32][^38][^50][^53]


## 4. Representations, hierarchical reasoning, and world models

These models occupy different positions in a robot system. A representation encoder describes the current state; a hierarchical planner selects a subgoal; a policy produces controls; a world model predicts the consequences of candidate controls. A model can occupy several positions, but real robot capability requires perception, decision, execution, and feedback together. This chapter distinguishes reported experiments, official product descriptions, and analytical conclusions. Versions were checked through 11 September 2026.

### SayCan, PaLM-E, and EmbodiedGPT: connecting language reasoning to action

**SayCan (2022)** combines a language model's score for a skill's relevance with a value function's estimate of that skill's feasibility. It selects and executes a skill, then repeats. Its main training requirements lie in the skill policies and their value functions. The language model orchestrates abilities rather than generating joint commands. The original system receives environmental feedback primarily through current affordance values; its authors explicitly identify incomplete failure feedback as a limitation. The public tabletop simulation does not reproduce the full mobile manipulation stack.[^56]

**PaLM-E (2023)** embeds images and continuous robot state in the same dimensional space as language tokens. A decoder language model jointly trained on embodied and general multimodal tasks outputs textual plans for low-level policies, incorporating subsequent visual observations. The architectural change from SayCan is direct observation-conditioned reasoning. The 562B variant illustrates semantic transfer, not a 562B servo controller. Sensor grounding and downstream motor competence remain separate requirements.[^57]

**EmbodiedGPT (2023)** uses EgoCOT subgoal data derived from Ego4D to adapt a 7B language model with prefix tuning. Features extracted from planning queries inform downstream control. It explores a learned interface between visual evidence, subgoals, and action-relevant representations. Its benchmark improvements do not establish that verbal reasoning alone solves physical contact control.[^59]

### VIMA and VoxPoser: task specification and geometric grounding

**VIMA (2022 preprint; ICML 2023)** represents tasks with interleaved text, object images, and demonstration frames. T5 encodes the prompt; a causal transformer with cross-attention conditions on that prompt and interaction history to produce manipulation actions. More than 600,000 expert trajectories and four generalization levels test changes in objects, compositions, and task templates. This object-centric policy is an important multimodal interface, but should not be conflated with every VLA that inherits an internet-scale language model. Its principal evidence is procedural tabletop simulation; real perception and action transfer require additional work.[^58]

**VoxPoser (2023)** uses language-generated programs and vision-language components to construct three-dimensional affordance and constraint maps. A motion planner converts those maps into end-effector trajectories. Re-evaluating cached programs with new visual observations enables receding-horizon adaptation. This makes spatial objectives inspectable, but introduces dependencies on segmentation, calibration, reachability, and dynamics assumptions. No additional training of the core composition does not mean no pretrained perception, controller, or integration effort.[^60]

### R3M and VC-1: encoders are infrastructure

**R3M (2022)** learns visual features from Ego4D using temporal contrast, video-language alignment, and compactness regularization; downstream controllers can train on frozen features. **VC-1 (2023)** uses masked visual pretraining and CortexBench to study transfer across sensorimotor tasks, model scales, and data mixtures. Domain adaptation materially affects results. Neither encoder alone supplies actions, a long-horizon plan, or an action-conditioned transition model.[^61][^62]

The analytical relationship to VLA is modular rather than a simple replacement lineage. An encoder can support a policy, reward estimator, retrieval system, or world model. Comparisons should hold controller architecture, demonstrations, cameras, and fine-tuning protocol fixed; otherwise apparent representation gains may come from other components.

### PerAct, RVT, and 3D Diffuser Actor: geometry and generative actions

**PerAct (2022)** converts RGB-D observations into a voxel grid, combines voxel patches with language in a Perceiver, and classifies the next end-effector location and discretized orientation/gripper state. Aligning observations and actions in three-dimensional coordinates provides a useful prior for limited demonstrations. The costs include voxel resolution, memory, and calibration sensitivity; experiments cover RLBench and a small real robot task collection.[^63]

**RVT (2023)** tackles the compute cost of explicit three-dimensional representations by rendering virtual views of the workspace and fusing them with cross-view attention. It predicts gripper poses while retaining geometric grounding. Relative to PerAct, the main change is how spatial information is computed. Reported speedups depend on the authors' implementation, hardware, and matched-performance target.[^64]

**3D Diffuser Actor (2024)** combines spatial tokens with diffusion over end-effector translations and rotations, using three-dimensional relative attention during denoising. Its target is a multimodal **action distribution**, not future video. RLBench keyposes still require a low-level planner to reach them. The official implementation documents quaternion conventions and differences between evaluation protocols, illustrating why action coordinates and environment versions must accompany success-rate comparisons.[^65][^66]

### DreamerV3: learning consequences and improving behavior in imagination

**DreamerV3 (2023 preprint; 2025 Nature publication)** is a model-based reinforcement learning algorithm, not one pretrained checkpoint that controls every robot. It learns recurrent latent dynamics, reward, and continuation from interaction, trains an actor–critic on imagined trajectories, and incorporates new real experience. Normalization, transformations, and loss balancing improve cross-domain stability.[^67][^68]

Control optimization uses compact latent states even if image reconstruction helps training. Unlike typical behavior-cloned VLA, policy improvement explicitly exploits predicted outcomes and rewards. One configuration across tasks does not mean one set of weights solves every task zero-shot. Exploration cost, reward specification, and accumulated model error remain obstacles in physical deployment.

### UniSim: generated experience as a training environment

**UniSim (2023 preprint; ICLR 2024)** combines heterogeneous image, video, navigation, and robot datasets in a conditional video generator. High-level language or low-level controls specify the next interaction. Iterative generation provides experience for training planners and reinforcement learning policies; the paper demonstrates transfer in particular real tasks.[^69][^70]

Its contribution is a path from video generation to action-conditioned training trajectories. For engineering use, one must verify that controls causally affect predicted outcomes, failures remain visible, and policies do not exploit simulator artifacts. This is Yang and colleagues' generative interaction model, not the separate autonomous-driving sensor simulator with the same name.

### Genie 1, 2, and 3: interactive environments and their limits

**Genie (2024)** learns a video tokenizer, latent action model, and dynamics predictor from videos without ground-truth control labels. Inferred latent actions are not automatically robot motor commands. **Genie 2 (December 2024)** uses autoregressive latent diffusion conditioned on past frames and actions. **Genie 3 (August 2025)** demonstrates 720p, 24-frame-per-second interactive environments with consistency lasting minutes. Project Genie subsequently provided a restricted product prototype in 2026.[^71][^72][^73][^74]

The series advances generated environments and agent training substrates. Genie 3's official limitations include restricted agent actions and difficult multi-agent interactions; prompt-triggered environmental events need not be actions performed by the agent. Navigating generated worlds or rendering a robot does not validate physical contact precision, torque control, or long-term safety. The checked official pages do not disclose Genie 3's complete training data and architecture, so Genie 2 internals should not be presented as verified Genie 3 internals.

### GR-1 and GR-2: video pretraining for direct robot policies

**GR-1 (2023)** pretrains on video and adapts to robot trajectories. A GPT-style model consumes language, image history, and robot state while predicting both future images and actions. Visual prediction supplies temporal supervision, but action outputs can be executed without explicitly searching multiple imagined futures. **GR-2 (2024)** scales video pretraining to 38 million clips and more than 50 billion tokens, followed by joint video-action adaptation.[^75][^76][^77]

This family bridges video models and VLA: it adds temporal priors to semantic understanding and executable actions to generative modeling. Joint prediction alone does not establish model-predictive control at inference. GR-2's 97.7% concerns the 105-task Simple setting; unseen manipulation is substantially harder. It does not establish success in arbitrary homes or robot embodiments.[^91] Access to the complete pretraining corpus and reproducible training setup requires separate scrutiny.

### V-JEPA 2, 2-AC, and 2.1: latent prediction and planning

**V-JEPA 2 (2025)** predicts masked video representations rather than reconstructing every pixel. **V-JEPA 2-AC** post-trains an action-conditioned predictor using fewer than 62 hours of DROID robot video and recorded actions. Image-goal features guide receding-horizon planning on real Franka arms. Zero-shot deployment means no environment-specific or task-specific training there; it does not mean arbitrary robot control emerges from action-free video alone.[^78][^79][^81]

**V-JEPA 2.1 (March 2026)** adds dense predictive supervision for visible and masked tokens, intermediate-layer supervision, joint image/video tokenization, and scaling. Its robot experiments reuse the 2-AC predictor architecture, public code, and planning protocol. After replacing the visual encoder, the action-conditioned predictor is retrained on DROID; this is not direct inheritance of trained 2-AC predictor weights. Table 6 shows cup-grasp success improving from 60% to 70% at approximately three seconds of planning. Reaching 80% uses a longer horizon and approximately fourteen seconds. The widely summarized twenty-percentage-point gain therefore includes more planning compute. Each skill has only ten evaluated tasks, and gripper timing remains a failure mode.[^80][^81]

Analytically, latent prediction retains task-relevant changes while avoiding unnecessary visual detail; generative video preserves interpretable observations. These approaches can coexist: latent search can reduce planning cost and image generation can support inspection or synthetic data. The decisive question is whether the representation preserves information about contact, occlusion, and failure.

### Cosmos Predict, Cosmos Policy, and Cosmos 3

**Cosmos Predict 2.5** generates world video conditioned on text, images, or video; **Transfer 2.5** transforms scenes using controls such as depth or segmentation. These are initially environment and data-generation components, not robot controllers.[^82]

**Cosmos Policy (January 2026)** explicitly adds executable actions by fine-tuning Cosmos-Predict2-2B on target-platform demonstrations. It represents action chunks, future observations/proprioception, and values as latent frames within the existing diffusion process. It supports both direct action sampling and best-of-N planning over predicted outcomes and values. The paper separates direct-policy and planning evaluations; additional rollout data can improve the learned dynamics and value function. The extra search cost must accompany claims of higher success.[^83][^90]

**Cosmos 3 (released May 2026; checked through September)** combines an autoregressive reasoning tower with a diffusion generation tower using a Mixture-of-Transformers architecture. The current official repository lists Super 64B, Nano 16B, Edge 4B, and DROID-adapted policy checkpoints. Edge has resolution and video-transfer restrictions; recommended embedded hardware does not make every inference mode real-time. The checked repository currently uses OpenMDW-1.1, which should not be replaced with a license description copied from an older Cosmos generation. Complete pretraining reproducibility, hardware latency, and transfer to unfamiliar embodiments require checkpoint-specific evaluation.[^84][^85]

### GAIA-2, 3, and 4: the autonomous-driving boundary

**GAIA-2 (March 2025)** generates controlled multi-camera futures; **GAIA-3 (December 2025)** emphasizes evaluation. **GAIA-4 (August 2026)** places the AI Driver in a generated sensor loop, including camera and radar output. In world-on-rails mode, other road users retain logged trajectories for controlled counterfactual comparison; an optional reactive-agent mode allows selected participants to respond to the ego vehicle.[^86][^87][^88]

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

Choose the missing capability before choosing a model family. Skill composition suggests hierarchical planning; inadequate spatial precision suggests better geometry and action representations; abundant action-free video suggests representation or video pretraining; comparing alternative action consequences motivates explicit world-model planning. **MoLe-VLA is a dynamic layer-skipping efficiency method, not a world model.**[^89] Tasks involving tactile contact, persistent occlusion, human collaboration, and long-term state require additional feedback and state estimation beyond these visual approaches.


## 5. Whole-body control and navigation: turning model outputs into sustained action

Embodied systems span at least three problems: choosing a goal, generating executable short-term actions, and remaining stable under contact and disturbance. A model that can describe loading a dishwasher does not thereby provide balance, obstacle avoidance or grasp control. Relationships between models should first be located within this hierarchy; advances in motor control often complement a VLA rather than replace it.[^99][^102][^110]

### From demonstrations to reusable motion priors

**DeepMimic (2018)** combines motion imitation with task rewards. Body state, phase and a goal condition a policy that produces joint targets and learns through physical feedback. Its contribution is to optimize resemblance and task achievement together. The original demonstrations concern simulated characters, including robot-shaped models; they do not establish deployment on physical Atlas hardware.[^92]

**AMP (2021) and ASE (2022)** shift emphasis from tracking a selected clip toward learning a distribution of movement. AMP uses a discriminator to provide a motion-style reward, reducing manual clip selection. ASE adds a latent skill interface so a higher-level policy can reuse the learned repertoire. ASE is an explicit methodological extension; the comparison with DeepMimic is an analytical change in problem formulation, not inherited weights. Natural movement still does not imply task correctness, and abrupt skill switching can create poor transitions.[^93][^94]

**PHC (2023)** asks whether tracking can continue after noisy inputs or falls. Progressive multiplicative control adds capacity for difficult motions and recovery, making reset avoidance part of the controller. Its central evidence concerns simulated avatars. Transferring this result to real actuators, sensors and physical human interaction remains a separate challenge.[^95][^96]

**Humanoid Transformer (2023)** instead uses observation-action history to autoregressively predict control actions, trained with model-free RL in randomized simulation. Behavior adapts through context without changing weights. This is contextual adaptation to execution dynamics, not the same capability as learning a new manipulation task from a demonstration video. Evaluation chiefly covers locomotion, terrain and disturbances.[^97]

### From human motion to autonomous-task data

**H2O and OmniH2O (2024)** retarget human motion, filter infeasible examples using privileged imitation, and train deployable tracking policies. OmniH2O explicitly follows H2O and makes kinematic pose a common interface for RGB, VR, generated motion and learned autonomous policies. A privileged teacher must be distilled into a student whose inputs exist at deployment. Changing the goal generator need not entail rebuilding the physical controller. Teleoperated trials must nevertheless be counted separately from autonomous trials.[^98][^99]

**HumanPlus (2024)** closes a data-collection loop. A low-level policy trained from 40 hours of human motion enables camera-based humanoid shadowing; resulting real-robot demonstrations support egocentric behavior cloning. A customized 33-DoF humanoid demonstrates multiple tasks. The useful sequence is human motion prior → practical teleoperation → robot task data → visual policy. Success on the reported small task set is not a measure of general competence across homes.[^100]

**MaskedMimic (2024)** represents heterogeneous commands as incomplete motion descriptions. Partial joints, paths, scenes or text constrain a motion-inpainting problem. Training obtains a fully constrained tracking teacher and then a conditional-VAE policy with randomized missing information. This admits multiple valid movements for an underspecified goal, rather than forcing one mean solution. The main evidence remains physics-based animation rather than a ready-made real-humanoid controller.[^101]

### SONIC: an explicit interface between VLA and motor control

**SONIC (2025 preprint; 2026 publication and engineering updates)** encodes human, robot and hybrid reference motions into a shared quantized token. A common decoder outputs desired joint positions for PD controllers. PPO tracking, auxiliary reconstruction and domain randomization train the interface; a runtime kinematic planner can convert intent into short reference movements. This connects VR, human video and VLA commands to one execution policy.[^102][^123]

The original paper fine-tunes GR00T N1.5 on 300 teleoperated demonstrations to produce head/wrist poses, waist height and base-motion commands, then executes those commands through SONIC. Its 20-trial, single-task experiment is explicitly a compatibility proof of concept, not a broad autonomy score. The inspected official repository now supplies an N1.7 workflow, training/deployment code and SONIC v1.1. Released controllers run at 50 Hz. Reference lookahead, neural inference duration and end-to-end teleoperation latency are different measurements.[^102][^103]

HoloMotion provides a 2026 extension-reading example of a reference-conditioned MoE transformer and motion-data-to-deployment pipeline. It reinforces the relevance of model/data scaling in whole-body control, but a foundation-model label alone does not establish unseen-contact robustness, arbitrary-terrain competence or certified safety.[^124]

### Navigation: local policies, global planning and spatial memory

**ViNT (2023)** learns transferable navigation from visual history and a goal image. Its transformer outputs local waypoints and a goal-distance estimate, while alternative goals can be encoded into the same interface. Long-distance behavior results from local policy, subgoal generation, topological representation and planning heuristics working together; it is not a single network directly producing every motor command.[^104][^105]

**NoMaD (2023 preprint / 2024 conference)** explicitly reuses ViNT's encoder. A diffusion action decoder represents alternative routes, while masking the goal lets one policy support both exploration and directed navigation. This avoids simply averaging incompatible paths around an obstacle. Sampling, path selection, local control and new observations remain part of the deployed loop. Low collision rates in an experiment are neither a formal collision guarantee nor a humanoid balance result.[^106]

**GOAT (2023)** addresses object and place memory across missions. Observations update an instance-aware semantic map; category, image or language goals identify a target; the system explores for unknown objects and reuses remembered evidence for known ones. It is a modular system, and adaptation primarily comes from updating memory. **GOAT-Bench (2024)** is the distinct lifelong-navigation benchmark. A local navigation policy, semantic memory and VLA could be complementary, but that architectural inference should not be presented as an implemented model lineage.[^107][^108]

### Commercial hierarchies and contextual adaptation

**Figure Helix → Helix 02** is an explicit version extension. The original model emphasizes upper-body control. Helix 02 adds S0: S2 supplies semantic goals; S1 produces full-body joint targets at 200 Hz; S0 handles fast balance/contact execution at 1 kHz. Figure discloses over 1,000 hours of retargeted human motion and simulated RL for S0, alongside palm vision and fingertip touch. Its four-minute room-scale task is a vendor demonstration, not a multi-environment reliability study. A unified system still contains distinct levels and update rates.[^109][^110]

**Skild Brain → S1** combines cross-embodiment learning with task adaptation. S1 describes episodic demonstration-conditioned pretraining and infers intent, progress and actions from a task video plus current context, without task-specific weight updates in the reported setting. The inspected article does not disclose a complete network, action parameterization or reproducible training recipe. Those fields remain unknown; the phrase general-purpose brain does not justify inventing a transformer or diffusion architecture.The public scaling study uses cumulative per-step scoring with human failure recovery; that score should not be equated with uninterrupted end-to-end autonomous task completion.[^111][^112]

**Generalist GEN-1 → GEN-1.5** offers a useful contrast. GEN-1 emphasizes reliability after selected-task adaptation; GEN-1.5 places sensorimotor demonstrations in a 30-second context and produces 100-Hz trajectories. Generalist says its contextual ability emerged without a dedicated ICL objective, whereas Skild describes demonstration-conditioned training. Inputs, training and test distributions differ, so a single success-rate ranking is inappropriate. Generalist also explicitly describes current tasks as short and its contextual policies as more brittle than fine-tuned ones.[^125][^126]

### Product progress and the strength of evidence

Reproducible models, development platforms, vendor demonstrations, customer-confirmed pilots and sustained commercial operation are different stages. Each deployment claim should name the robot, model version, human assistance and metric denominator.[^114][^117][^118][^128]

| Organization | Technology/product | Verified progress | Evidence boundary |
|---|---|---|---|
| Figure | Helix 02 / Figure 03 | BMW confirms the earlier Figure 02 pilot and new Figure 03 sequencing project; Figure publishes onsite demonstrations | Historical Figure 02 production statistics do not transfer to Figure 03 or Helix 02.[^127][^128] |
| Skild AI | Cross-embodiment Brain / S1 | Company reports paying deployments and new S1 pilots | Commercial totals are vendor statements across products; deploying, planned and piloting are distinct.[^113] |
| Physical Intelligence | π models integrated by partners | Weave laundry and Ultra warehouse customer-site accounts | Deployed versions differ from π0.7 research; remote intervention remains part of operation.[^27][^114] |
| NVIDIA | GR00T, SONIC, simulation and onboard stack | Released models/code/workflows and announced humanoid reference hardware | Hardware availability is stated as late 2026, not delivered by the cutoff.[^103][^33][^115] |
| Google DeepMind | Robotics 2 / ER 2 / On-Device 2 | July 2026 whole-body, multi-embodiment and local-execution releases | Reasoning API access, trusted testing and open control weights are different access categories.[^42] |
| Agility Robotics | Digit + Arc industrial service | GXO confirms a commercial RaaS deployment; vendor reports cumulative tote milestones | Counts omit denominators for failures, intervention and downtime; do not infer a disclosed VLA.[^118][^119] |
| 1X | NEO / Redwood / 1XWM | Ordering and 2026 delivery plans; world-model technical disclosure | Basic autonomy and scheduled Expert Mode are explicit; orders are not proof of a delivered autonomous fleet.[^116][^117] |
| Boston Dynamics | Electric Atlas and learned behaviors | Official manufacturing, industrial pilot history and scheduled deployment | Hardware productization does not establish model reproducibility or general long-term autonomy.[^120] |
| Unitree | G1 platform / UnifoLM-VLA | Official code, checkpoints and datasets | Hardware sales, model release and autonomous commercial usefulness need separate evidence.[^122] |
| Galbot | G1/S1 and AstraBrain | Official WAM/WBC/dexterity and industry-application positioning | First/largest/scaled-deployment language remains vendor positioning rather than a technical ranking.[^121] |
| Generalist | GEN-1 / GEN-1.5 | Early enterprise access and real-robot adaptation/context studies | High reliability on adapted tasks and one-shot performance on unfamiliar tasks are different conditions.[^125][^126] |

### Reading model relationships and engineering implications

Explicit relationships include AMP→ASE, H2O→OmniH2O, ViNT→NoMaD, Helix→Helix 02 and the released GR00T–SONIC composition. PHC versus SONIC, or SONIC versus Helix 02, can be compared as approaches to placing broad motor competence below goals, but there is no claim of shared weights or code. The relation catalog marks `explicit` and `analytical` separately.[^94][^99][^102][^103][^106][^110]

An engineering interface should specify coordinate frame, update rate, action hold duration, command expiry and control authority. Semantic decisions can tolerate slower updates; balance/contact feedback cannot wait for a remote reasoning round trip. Human references also require reachability and dynamic-feasibility handling. These are engineering deductions from the compared systems, not claims that every product uses the same implementation.[^98][^102][^110]

Unresolved issues include stability under unfamiliar contact and payloads; preservation of mechanical information across embodiments; automatic detection and recovery over minutes; and evaluation that jointly reports success, throughput, human time and failure cost. More natural motion, more realistic video or a larger network alone cannot settle these questions.[^100][^102][^114][^116]


## 6. Additional decompositions: data, feedback, and execution

### GO-1: a latent plan between semantics and continuous action

GO-1 consumes multiple camera views, instructions, and robot state. Its ViLLA architecture combines a vision-language backbone, a latent-action planner, and a diffusion action expert. Discrete latent actions are learned from sources including human video; a planner predicts them from the current context, and the action expert conditions on this representation to generate continuous chunks. Latent-action prediction and robot action denoising have distinct objectives. GO-1 Air removes the planner, providing a public entry point for investigating whether the intermediate planning layer is useful.[^132][^133]

This is a combination of semantic transfer, latent-motion transfer, and continuous control, rather than the inevitable successor to every VLA. Latent actions can use video without robot-command labels but still need grounding into executable commands through robot data. When architecture and data scale change together, gains cannot be attributed solely to the planner; matching task, data, and compute while comparing GO-1 with Air is more informative. AgiBot World's collection-robot count describes hardware instances, not the same number of distinct embodiments.[^132][^133]

### SERL and HIL-SERL: learning from corrective experience

SERL integrates training, experience, and robot interfaces for sample-efficient visual reinforcement learning; it is not one pretrained weight set covering all tasks. HIL-SERL introduces a concrete feedback workflow within this line: collect positive and negative states for a reward classifier, initialize a demonstration buffer, execute online, intervene when needed, and use the resulting experience in actor-critic learning. The learning signal includes visual observations, state, sparse success signals, and human corrections.[^142][^143][^153]

Relative to imitation, the additional information concerns recovery after deviations and whether actions actually succeed. Relative to generalist VLAs, the method is closer to precise post-training on a bounded task. Reported learning speed and high success cannot be separated from reward labels, interventions, resets, and hardware. Engineering comparisons should include cumulative human minutes, reset count, and usable interaction per hour, rather than gradient-update time alone.[^142][^153]

### MolmoAct2: an open embodied-reasoning backbone with continuous control

MolmoAct2 builds on the Molmo2-ER embodied-reasoning vision-language backbone and adds robot state and a flow-matching continuous action expert. Images, language, and state condition action chunks for closed-loop manipulation. Public assets include intermediate foundation checkpoints, selected robot-adapted policies, and relevant datasets, enabling analysis of how action generation uses reasoning representations. Producing explanatory text is insufficient by itself: the action module must still learn an appropriate command distribution from robot trajectories.[^144][^145]

The released checkpoints make the training path more explicit. Molmo2-ER is the starting vision-language backbone; MolmoAct2-Pretrain is a discrete autoregressive VLA before the continuous action expert is attached; the final MolmoAct2 connects a flow-matching expert. MolmoAct2-Think adds depth-token reasoning and should be identified as a separate variant, rather than attributing that mechanism to every deployed MolmoAct2 policy. This separates two research questions: how discrete action pretraining shapes the backbone, and whether depth reasoning improves continuous control. Their contributions still require ablations with a fixed robot, data mixture, and inference budget; releasing intermediate checkpoints does not by itself establish causal attribution.[^144][^145]

Its relationship to GR00T, PI, and Xiaomi concerns a modular division between visual-language understanding and continuous generation, not shared weights. Backbones, training mixtures, alignment objectives, and deployment protocols differ. Staged checkpoints facilitate ablations, while improvements in contact, unfamiliar objects, or long-horizon recovery require matched evaluation. Foundation checkpoints and embodiment-adapted deployment policies should be treated as different assets.[^144]

### Xiaomi-Robotics-0: training for the execution schedule

Xiaomi-Robotics-0 combines Qwen3-VL-4B-Instruct with an action DiT, totaling 4.7B parameters according to the official project. A first stage develops action-relevant VLM features using Choice Policies and mixed vision-language data. A second freezes the VLM and trains a flow-matching expert conditioned on its KV states and proprioception. Post-training introduces action prefixes and attention/loss design so that new chunks agree with committed actions while remaining responsive to observations.[^151]

The public deployment implementation returns 30-step chunks. Asynchronous execution predicts the next chunk while current actions run and removes actions that have expired during inference. This mode requires a correspondingly trained checkpoint; attaching any synchronous policy to an asynchronous queue is not equivalent. The broader lesson is that **latency compensation changes training conditions and distributions**, rather than being an isolated runtime patch. Strong reported real-task performance also uses substantial specialized data, so task proficiency, few-shot adaptation, and zero-shot generalization remain distinct claims.[^151][^152]

### 1XWM: grounding generated video into action

1XWM generates a future from a prompt and starting frame, then uses inverse dynamics to extract NEO commands. The January 2026 disclosure describes a 14B video backbone adapted with egocentric human and robot data, and a Depth Anything encoder with a flow-matching head for the inverse model. Video priors therefore still require an action-grounding interface.[^116]

That version needs approximately 11 seconds of multi-GPU inference for five seconds of video plus one second to extract actions; longer-horizon closed-loop replanning remains future work. This separates the demonstration from reactive, on-device, sustained household autonomy. These limitations apply to the disclosed version, without assumptions about unpublished improvements.[^116]


## 7. Data and evaluation: establishing actual progress

### What the data assets contribute

| Asset or interface | Verified representative scale or property | Relevance |
|---|---|---|
| Open X-Embodiment | 22 robots in the original paper; standardized records | Cross-embodiment sharing; actual mixtures differ by model [^9] |
| BridgeData V2 | 60,096 trajectories in 24 environments, including teleoperation and scripted runs | Object and scene diversity; overlaps with OXE mixtures [^148] |
| DROID | 76k trajectories, 350 hours, 564 scenes | Distributed real-world collection; calibration/data revisions matter [^129] |
| RoboMIND | Original paper: 107k trajectories, 479 tasks, 96 object classes | Multiple embodiments collected on a unified platform [^131] |
| AgiBot World | Beta lists 1,003,672 trajectories | Bimanual collection at scale; hardware count is not embodiment count [^132] |
| UMI / DexUMI | Handheld gripper or human-hand interfaces | Portable demonstrations still need temporal, pose, and reachability alignment [^130][^147] |
| RoboCasa365 | 365 tasks, 2500+ kitchens; 600+ human and 1600+ synthetic demonstration hours | Compositional and scene coverage; not all hours are real-robot collection [^149][^154] |

These quantities cannot be added into a total of independent embodied data. Trajectories recur across datasets and training mixtures; frames, steps, clips, episodes, and hours are different units. Human video supplies objects, tasks, and motion priors but usually lacks actuator commands and touch. Real trajectories ground actions but are expensive to diversify. Simulation provides rewards and difficult scenarios while retaining contact and sensor gaps. Data value should be decomposed by scenes, embodiments, skills, recovery, and sensing modalities.

LeRobot provides dataset and robot interfaces, while Isaac Lab and ManiSkill provide learning and simulation infrastructure. Standard containers do not standardize control semantics. Joint ordering, rotation conventions, normalization, timestamps, calibration, and control periods still require explicit alignment.[^138][^140][^141]

### Benchmarks ask different questions

| Benchmark | Main target | Conditions that must match |
|---|---|---|
| LIBERO | Language manipulation and spatial/object/goal transfer | Suites, preprocessing, demonstration count, resets, rollout horizon [^134] |
| CALVIN | Sequences of language-conditioned subtasks | Environment split such as ABC-D; mean chain length is not success percentage [^135] |
| SIMPLER | Simulation proxies for particular real setups | Visual Matching versus Variant Aggregation, robot, control frequency [^136] |
| RoboTwin 2.0 | Bimanual manipulation, randomization, embodiment variation | Clean/randomized conditions, tasks, action interfaces [^137] |
| RMBench | Manipulation requiring historical information | Memory split, history length, checkpoint revision; retrained weights appeared in 2026 [^150] |
| RoboCasa365 | Composed kitchen skills and environment transfer | Version, task level, timeout; horizons increased 1.5x in May 2026 [^149] |
| BEHAVIOR-1K | Long household activities and interaction states | Challenge subset, observations, timeout, embodiment; not all 1000 activities solved [^139][^155] |
| MolmoSpaces | Multiple evaluation settings and scene coverage | Training data, action space, task coverage, adaptation, test date [^146] |

There is consequently no overall ranking of every model. High LIBERO performance after task-specific training and lower zero-shot performance in new scenes address different difficulties. A new model can also arrive with longer horizons, more sampled candidates, or larger images. Meaningful comparisons report training exposure to tasks, objects, scenes, and embodiments, as well as checkpoint version, control period, inference budget, and trial count.

### A proposed evaluation protocol

The following is a proposed research and engineering design, not an experiment performed in this repository. Use four levels: in-distribution skills; new objects, views, and language; new scenes and task compositions; and new embodiments plus sustained autonomous operation. Include disturbances, occlusions, failed grasps, and recovery at every level. Separate train, validation, and test data by scenes and collection sessions and document potential pretraining overlap.

A first baseline group holds action interface and data budget constant while comparing ACT/DP, adaptable VLAs, and structured-planning systems. A second fixes the backbone and varies single-step versus chunks, discrete versus flow generation, sensing, synchronous versus asynchronous execution, and memory. A third compares world models without search, with fixed-budget search, and with increased-budget search. When commercial training data cannot be controlled, interpret results as system acceptance tests rather than causal evidence about architecture.

Record task and complete-chain success, completion time, interventions per hour, recovery, collisions/drops/stops, median and tail observation-to-action latency, energy per task, and data/adaptation cost. Prespecify repetitions per task and condition and report confidence intervals. Stratify by task and scene rather than treating correlated clips as independent trials. Every attempt, including failures and timeouts, belongs in the log.

## 8. A synthesis of model relationships

![Training paths and framework reuse](../../figures/learning-paths.svg)

![Model relationship map](../../figures/model-relations.svg)


### Relationships are not one lineage

The relationship inventory distinguishes **explicit initialization/reuse, series evolution, method combination, system complementarity, and analytical comparison**. Weight inheritance or post-training on another model is claimed only when an original paper or official implementation says so. Sharing a transformer or flow objective establishes a common paradigm, not shared weights. Each recorded edge has evidence and a relationship type.

The first connection runs from **specialized imitation to general conditional policies**. ACT and DP address sequence modeling and multimodal control; RT, Octo, and OpenVLA emphasize broader task and embodiment coverage. Generalist models do not invalidate compact imitation baselines in fixed tasks with limited demonstrations or compute. Large VLAs also adopt chunks and generative heads. Matched task data are required to isolate the benefit of internet pretraining.

The second is **a more explicit division between semantics and action distributions**. RT-2 maps actions into a language-style token space; OpenVLA provides an open transfer route. PI, GR00T, MolmoAct2, and Xiaomi use continuous action experts to address fine control and long action sequences. FAST changes encoding, OFT changes adaptation and output recipes, and asynchrony changes scheduling. Representation, training, and runtime should not be collapsed into a succession of model generations.

The third is **complementarity between geometry and scale**. PerAct and RVT align scene and action geometry, while 3D Diffuser Actor adds generative action modeling. Strong semantic pretraining does not guarantee precise coordinates, collision boundaries, or contact states. Geometry can provide an inspectable interface at a calibration and compute cost. The source of spatial error should determine whether to combine these components.

The fourth is **convergence between world models and VLAs without identical roles**. GR-1/GR-2 use future prediction in action learning; GO-1 uses latent actions as an intermediate plan; Cosmos Policy adapts a video foundation model to actions, futures, and values; JEPA-AC searches through latent action consequences. These correspond to auxiliary supervision, intermediate representation, unified generation, and explicit planning. Deployment-time world-model planning should be claimed only when inference actually evaluates possible consequences.[^132][^133][^75][^76][^83][^90][^78][^80][^81]

The fifth is **integration of general reasoning with low-level whole-body control**. HumanPlus, SONIC, and Helix illustrate separate timescales for semantics, motion targets, and stabilization. A VLA emitting a whole-body joint vector has not automatically solved balance and contact; a stable locomotion controller does not automatically understand open-ended tasks. Their interface needs coordinates, timing, constraints, and failure feedback.

The sixth is **a feedback cycle connecting imitation and policy improvement**. PI's experience-learning work and HIL-SERL exemplify broad pretrained adaptation and bounded-task feedback optimization. Both use outcomes to improve behavior, but rewards, scale, released assets, and operating constraints differ. World models can reduce physical exploration cost while introducing errors that an optimizing policy may exploit.[^142][^143]

### Six useful direct comparisons

| Comparison | Actual distinction | Appropriate test |
|---|---|---|
| ACT versus DP | Latent-variable chunk prediction versus action denoising | Matched demonstrations and feedback interval: precision, failure, latency |
| OpenVLA versus OFT | Adaptation and output recipe around a reusable backbone | Fixed backbone and training budget |
| PI versus GR00T | Related continuous-expert paradigm with different backbones, mixtures, embodiments, versions | Pinned checkpoints and permissions; embodiment adaptation cost |
| V-JEPA-AC versus video world models | Compact latent consequences versus viewable futures | Fixed search time/candidates and real task success |
| Planner plus skills versus end-to-end VLA | Explicit subgoals versus a learned joint action interface | New compositions, failure recovery, grounding, module overhead |
| Helix/SONIC hierarchy versus arm-only VLA | Whole-body balance, contact frequency, and stabilization | Manipulation while moving, disturbances, multiple contacts |

## 9. Engineering architecture and openness

A practical architecture separates data/calibration, state/history, task planning, action generation, control constraints, and feedback logging. Slower semantic inference may run on a server, an action expert near the robot, and servo control and stopping on deterministic control paths. Frequencies must follow hardware and measured requirements rather than System 1/System 2 terminology. Every executed command should be traceable to the observation, model, and normalization revision that produced it.

Audit openness along five axes: disclosed mechanism, inference code, weights, training code/recipe, and actual training data, then separately record license and use restrictions. A GitHub repository does not establish completeness along all five axes. Hardware recommendations do not prove real-time performance in every mode. Public data and intermediate checkpoints facilitate reproduction, but calibration, controllers, and recovery can still depend on unrecorded operational expertise.[^140][^141][^144]

Selection should start from task constraints. A fixed precision workstation can compare ACT/DP and HIL-SERL; language generalization and task sharing motivate adaptable VLAs; explicit spatial constraints motivate geometry; choices among consequences motivate world-model planning. For mobile manipulation, establish low-level stability before connecting general semantics. These are mechanism-based recommendations, not procurement rankings or deployment guarantees.

## 10. Five future technical challenges

### Challenge 1: transferable action and contact representations

Sharing semantics across embodiments is easier than sharing actuator meaning. Joints, grippers, hands, control rates, and force sensing change the action distribution, while human video lacks command labels. Research should encode embodiment constraints, geometric goals, and contact states explicitly and use adaptation layers beneath shared policies. Tests should include new-embodiment demonstration requirements, contact-force error, insertion success, constraint violations, and post-transfer stability rather than source-robot success alone.

### Challenge 2: persistent memory, verifiable plans, and recovery

Tasks require remembering hidden objects, completed steps, and failed strategies. More video history increases cost and can preserve irrelevant context, while text plans can drift from actual state. Event memory, object-state graphs, explicit completion predicates, and recovery branches offer testable directions. RMBench and long-horizon benchmarks provide partial entry points, supplemented by real occlusion, moved objects, and interruptions. Report complete-chain success, recovery time, and persistence of incorrect memories.[^150][^139]

### Challenge 3: world models that support action decisions

A visually plausible future can be wrong for control, especially under contact, deformation, occlusion, or interaction with others. Longer planning amplifies error and can find simulator loopholes. Priorities include calibrated action conditioning, uncertainty, physical constraints, and correction from real feedback. Evaluation needs counterfactual action discrimination, agreement between predicted and real outcomes, fixed-budget planning gains, and conservative fallback under unexpected conditions.

### Challenge 4: jointly optimizing latency, energy, and control reliability

Large visual-language backbones, long histories, and iterative action generation compete for on-device resources, while buffering changes feedback age. Quantization, distillation, KV reuse, chunk scheduling, and control stability should be designed together and tested under disturbances. Tail latency, observation age, continuity, energy per task, and recovery matter alongside throughput. Xiaomi's asynchronous training provides a concrete reason to align training conditions with scheduling.[^151][^152]

### Challenge 5: auditable continual improvement beyond demonstrations

Selecting successful videos, reporting the best checkpoint, or hiding interventions overstates operational capability. Continual learning adds reward mismatch, forgetting, leakage, and rollback problems. Preserve all attempts, interventions, and failures, use independent-scene tests, and support reversible model releases. Track licenses for videos, scene assets, weights, and training data separately. Regression across versions, confidence intervals, human minutes, and sustained intervention rates reveal whether systems actually reduce human work.[^142][^146][^149]

## 11. Reading and reproduction path

A useful progression is ACT/DP for action learning, SayCan/PaLM-E for grounding, RT/OpenVLA for transfer, PI/GR00T for continuous experts, PerAct/RVT for geometry, followed by JEPA/Cosmos and whole-body control. Reproduction should begin with a fixed robot, explicit action interface, and repeatable tasks before adding out-of-distribution changes and recovery. Simultaneously replacing sensors, embodiment, data, and model prevents clean causal interpretation.

The repository retains model cards, relationship edges, data and benchmark tables, a product matrix, evidence and uncertainty records, both report editions, and build/validation scripts. It provides literature analysis and an implementable evaluation design, not reproduced training results, third-party paper copies, weights, or raw robot data. Updates should record version changes in the source ledger and revalidate agreement between diagrams, tables, and prose.

## 12. Model and method card index

Entries include models, versions, methods, and components, not that many independent foundation models. Full field-by-field decompositions are in the [Model Atlas](model-atlas.md).

| ID | Model / method | Year | Evidence |
|---|---|---|---|
| act | ACT | 2023 | [^1][^2] |
| diffusion-policy | Diffusion Policy | 2023 | [^3][^4] |
| rt1 | RT-1 | 2022 | [^5][^6] |
| rt2 | RT-2 | 2023 | [^7][^8] |
| rtx | RT-X / Open X-Embodiment | 2023 | [^9][^10] |
| octo | Octo | 2024 | [^11][^12] |
| openvla | OpenVLA | 2024 | [^13][^14] |
| openvla-oft | OpenVLA-OFT | 2025 | [^15][^16] |
| pi0 | pi0 | 2024 | [^17][^18][^20] |
| fast | FAST / pi0-FAST | 2025 | [^19][^20] |
| pi05 | pi0.5 / knowledge insulation | 2025 | [^21][^22][^20] |
| pi06 | pi0.6 | 2025 | [^23][^24] |
| pi06-recap | pi-star-0.6 / RECAP | 2025 | [^24][^25] |
| mem | MEM / pi0.6-MEM | 2026 | [^28] |
| pi07 | pi0.7 | 2026 | [^26][^27][^20] |
| smolvla | SmolVLA | 2025 | [^29][^30] |
| groot-n1 | GR00T N1 | 2025 | [^31] |
| groot-n15 | GR00T N1.5 | 2025 | [^32][^35] |
| groot-n16 | GR00T N1.6 | 2025 | [^33][^35] |
| groot-n17 | GR00T N1.7 | 2026 | [^34][^35] |
| gemini-robotics1 | Gemini Robotics / ER | 2025 | [^36][^37] |
| gemini-robotics15 | Gemini Robotics 1.5 / ER 1.5 | 2025 | [^38][^39] |
| gemini-er16 | Gemini Robotics-ER 1.6 | 2026 | [^40][^41] |
| gemini-robotics2 | Gemini Robotics 2 | 2026 | [^42] |
| gemini-er2 | Gemini Robotics ER 2 | 2026 | [^42][^43] |
| gemini-ondevice2 | Gemini Robotics On-Device 2 | 2026 | [^42][^44] |
| rdt1b | RDT-1B | 2024 | [^45][^46] |
| univla-odl | UniVLA (OpenDriveLab) | 2025 | [^47][^48] |
| univla-baai | UniVLA (BAAI) | 2025 | [^49][^50] |
| xvla | X-VLA | 2025 | [^51][^52] |
| lingbot-vla2 | LingBot-VLA 2.0 | 2026 | [^53][^54] |
| rtc | Real-Time Chunking (RTC) | 2025 | [^55] |
| saycan | SayCan | 2022 | [^56] |
| palme | PaLM-E | 2023 | [^57] |
| embodiedgpt | EmbodiedGPT | 2023 | [^59] |
| vima | VIMA | 2023 | [^58] |
| voxposer | VoxPoser | 2023 | [^60] |
| r3m | R3M | 2022 | [^61] |
| vc1 | VC-1 | 2023 | [^62] |
| peract | PerAct | 2022 | [^63] |
| rvt | RVT | 2023 | [^64] |
| 3d-diffuser-actor | 3D Diffuser Actor | 2024 | [^65][^66] |
| dreamerv3 | DreamerV3 | 2023 | [^67][^68] |
| unisim | UniSim | 2023 | [^69][^70] |
| genie1 | Genie | 2024 | [^71] |
| genie2 | Genie 2 | 2024 | [^72] |
| genie3 | Genie 3 | 2025 | [^73][^74] |
| gr1 | GR-1 | 2023 | [^75][^76] |
| gr2 | GR-2 | 2024 | [^77][^91] |
| vjepa2 | V-JEPA 2 | 2025 | [^78][^79][^81] |
| vjepa2-ac | V-JEPA 2-AC | 2025 | [^78][^79][^81] |
| vjepa21 | V-JEPA 2.1 | 2026 | [^80][^81] |
| cosmos-predict25 | Cosmos Predict 2.5 | 2025 | [^82] |
| cosmos-policy | Cosmos Policy | 2026 | [^83][^90] |
| cosmos3 | Cosmos 3 | 2026 | [^84][^85] |
| gaia2 | GAIA-2 | 2025 | [^86] |
| gaia3 | GAIA-3 | 2025 | [^87] |
| gaia4 | GAIA-4 | 2026 | [^88] |
| cosmos-predict2 | Cosmos Predict2-2B | 2025 | [^83][^90] |
| H-M01 | DeepMimic | 2018 | [^92] |
| H-M02 | AMP / ASE | 2021 | [^93][^94] |
| H-M03 | PHC | 2023 | [^95][^96] |
| H-M04 | Humanoid Transformer | 2023 | [^97] |
| H-M05 | H2O / OmniH2O | 2024 | [^98][^99] |
| H-M06 | HumanPlus | 2024 | [^100] |
| H-M07 | MaskedMimic | 2024 | [^101] |
| H-M08 | SONIC / GEAR-SONIC | 2025 | [^102][^103][^123] |
| H-M09 | ViNT | 2023 | [^104][^105] |
| H-M10 | NoMaD | 2023 | [^106][^105] |
| H-M11 | GOAT | 2023 | [^107][^108] |
| H-M12 | Helix / Helix 02 | 2025 | [^109][^110] |
| H-M13 | Skild Brain / S1 | 2025 | [^111][^112][^113] |
| go1 | GO-1 / GO-1 Air | 2025 | [^132][^133] |
| serl | SERL | 2024 | [^143] |
| hil-serl | HIL-SERL | 2024 | [^142][^153] |
| molmoact2 | MolmoAct2 | 2026 | [^144][^145] |
| xiaomi-robotics-0 | Xiaomi-Robotics-0 | 2026 | [^151][^152] |

## 13. Sources

Sources are deduplicated by URL. Dates indicate publication or version dates; dynamic pages were checked on September 11, 2026. Source aliases, reading scope, and limitations are retained in sources.json.

[^1]: Tony Z. Zhao et al.. [Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware](https://arxiv.org/abs/2304.13705). 2023-04-23.

[^2]: Tony Z. Zhao et al.. [ALOHA / ACT project](https://tonyzhaozh.github.io/aloha/). n.d.; accessed 2026-09-11.

[^3]: Cheng Chi et al.. [Diffusion Policy: Visuomotor Policy Learning via Action Diffusion](https://arxiv.org/abs/2303.04137). 2023-03-07.

[^4]: Cheng Chi et al.. [Diffusion Policy (IJRR manuscript)](https://diffusion-policy.cs.columbia.edu/diffusion_policy_ijrr.pdf). n.d.; accessed 2026-09-11.

[^5]: Anthony Brohan et al.. [RT-1: Robotics Transformer for Real-World Control at Scale](https://arxiv.org/abs/2212.06817). 2022-12-13.

[^6]: Robotics at Google. [RT-1 project](https://robotics-transformer1.github.io/). n.d.; accessed 2026-09-11.

[^7]: Anthony Brohan et al.. [RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control](https://arxiv.org/abs/2307.15818). 2023-07-28.

[^8]: Google DeepMind. [RT-2 project](https://robotics-transformer2.github.io/). n.d.; accessed 2026-09-11.

[^9]: Open X-Embodiment Collaboration. [Open X-Embodiment: Robotic Learning Datasets and RT-X Models](https://arxiv.org/abs/2310.08864). 2023-10-13.

[^10]: Google DeepMind and collaborators. [Open X-Embodiment repository](https://github.com/google-deepmind/open_x_embodiment). n.d.; accessed 2026-09-11.

[^11]: Octo Model Team. [Octo: An Open-Source Generalist Robot Policy](https://arxiv.org/abs/2405.12213). 2024-05-20.

[^12]: Octo Model Team. [Octo repository](https://github.com/octo-models/octo). n.d.; accessed 2026-09-11.

[^13]: Moo Jin Kim et al.. [OpenVLA: An Open-Source Vision-Language-Action Model](https://arxiv.org/abs/2406.09246). 2024-06-13.

[^14]: OpenVLA team. [OpenVLA repository](https://github.com/openvla/openvla). n.d.; accessed 2026-09-11.

[^15]: Moo Jin Kim, Chelsea Finn, Percy Liang. [Fine-Tuning Vision-Language-Action Models: Optimizing Speed and Success](https://arxiv.org/abs/2502.19645). 2025-02-27.

[^16]: Moo Jin Kim, Chelsea Finn, Percy Liang. [OpenVLA-OFT project](https://openvla-oft.github.io/). n.d.; accessed 2026-09-11.

[^17]: Physical Intelligence. [pi0: A Vision-Language-Action Flow Model for General Robot Control](https://www.pi.website/download/pi0.pdf). 2024-10-31.

[^18]: Physical Intelligence. [pi0: Our First Generalist Policy](https://www.pi.website/blog/pi0). 2024-10-31.

[^19]: Physical Intelligence. [FAST: Efficient Robot Action Tokenization](https://www.pi.website/research/fast). 2025-01-16.

[^20]: Physical Intelligence. [openpi repository](https://github.com/Physical-Intelligence/openpi). n.d.; accessed 2026-09-11.

[^21]: Physical Intelligence. [pi0.5: a Vision-Language-Action Model with Open-World Generalization](https://www.pi.website/download/pi05.pdf). 2025-04-22.

[^22]: Physical Intelligence. [VLAs that Train Fast, Run Fast, and Generalize Better](https://www.pi.website/research/knowledge_insulation). 2025-05-28.

[^23]: Physical Intelligence. [pi0.6 Model Card](https://website.pi-asset.com/pi06star/PI06_model_card.pdf). 2025-11-17.

[^24]: Physical Intelligence. [pi-star-0.6: a VLA that Learns from Experience](https://www.pi.website/blog/pistar06). 2025-11-17.

[^25]: Physical Intelligence. [pi-star-0.6 / RECAP technical report](https://www.pi.website/download/pistar06.pdf). 2025-11-17.

[^26]: Physical Intelligence. [pi0.7: a Steerable Model with Emergent Capabilities](https://www.pi.website/download/pi07.pdf). 2026-04-16.

[^27]: Physical Intelligence. [pi0.7: a Steerable Model with Emergent Capabilities](https://www.pi.website/blog/pi07). 2026-04-16.

[^28]: Physical Intelligence. [VLAs with Long and Short-Term Memory](https://www.pi.website/research/memory). 2026-03-03.

[^29]: Hugging Face and collaborators. [SmolVLA: A Vision-Language-Action Model for Affordable and Efficient Robotics](https://arxiv.org/abs/2506.01844). 2025-06-02.

[^30]: Hugging Face. [SmolVLA: Efficient Vision-Language-Action Model trained on LeRobot Community Data](https://huggingface.co/blog/smolvla). 2025-06-03.

[^31]: NVIDIA GEAR Team. [GR00T N1: An Open Foundation Model for Generalist Humanoid Robots](https://arxiv.org/abs/2503.14734). 2025-03-18.

[^32]: NVIDIA GEAR Team. [GR00T N1.5: An Improved Open Foundation Model](https://research.nvidia.com/labs/gear/gr00t-n1_5/). 2025-06-11.

[^33]: NVIDIA GEAR Team. [GR00T N1.6: An Improved Open Foundation Model](https://research.nvidia.com/labs/gear/gr00t-n1_6/). 2025-12-15.

[^34]: Edith Llontop and Brandon Neel / NVIDIA. [Develop Humanoid Robot Policies End-to-End with NVIDIA Isaac GR00T](https://developer.nvidia.com/blog/develop-humanoid-robot-policies-end-to-end-with-nvidia-isaac-gr00t/). 2026-07-07.

[^35]: NVIDIA. [NVIDIA Isaac-GR00T repository](https://github.com/NVIDIA/Isaac-GR00T). n.d.; accessed 2026-09-11.

[^36]: Gemini Robotics Team. [Gemini Robotics: Bringing AI into the Physical World](https://arxiv.org/abs/2503.20020). 2025-03-25.

[^37]: Google DeepMind. [Gemini Robotics brings AI into the physical world](https://deepmind.google/blog/gemini-robotics-brings-ai-into-the-physical-world/). 2025-03-12.

[^38]: Gemini Robotics Team. [Gemini Robotics 1.5: Pushing the Frontier of Generalist Robots with Advanced Embodied Reasoning, Thinking, and Motion Transfer](https://arxiv.org/abs/2510.03342). 2025-10-02.

[^39]: Google DeepMind. [Gemini Robotics 1.5 brings AI agents into the physical world](https://deepmind.google/blog/gemini-robotics-15-brings-ai-agents-into-the-physical-world/). 2025-09-25.

[^40]: Google DeepMind. [Gemini Robotics-ER 1.6 Model Card](https://deepmind.google/models/model-cards/gemini-robotics-er-1-6/). 2026-04-20.

[^41]: Laura Graesser and Peng Xu / Google DeepMind. [Gemini Robotics-ER 1.6: Powering real-world robotics tasks through enhanced embodied reasoning](https://deepmind.google/blog/gemini-robotics-er-1-6/). 2026-04-14.

[^42]: Carolina Parada / Google DeepMind. [Gemini Robotics 2 brings whole body intelligence to robots](https://deepmind.google/blog/gemini-robotics-2-brings-whole-body-intelligence-to-robots/). 2026-07-30.

[^43]: Google DeepMind. [Gemini Robotics ER 2 Model Card](https://deepmind.google/models/model-cards/gemini-robotics-er-2/). 2026-07-30.

[^44]: Google DeepMind. [Gemini Robotics On-Device 2 Model Card](https://deepmind.google/models/model-cards/gemini-robotics-on-device-2/). 2026-07-30.

[^45]: Songming Liu et al.. [RDT-1B: a Diffusion Foundation Model for Bimanual Manipulation](https://arxiv.org/abs/2410.07864). 2024-10-10.

[^46]: Tsinghua RDT team. [RoboticsDiffusionTransformer repository](https://github.com/thu-ml/RoboticsDiffusionTransformer). n.d.; accessed 2026-09-11.

[^47]: Qingwen Bu et al.. [UniVLA: Learning to Act Anywhere with Task-centric Latent Actions](https://arxiv.org/abs/2505.06111). 2025-05-09.

[^48]: OpenDriveLab. [UniVLA repository (OpenDriveLab)](https://github.com/OpenDriveLab/UniVLA). n.d.; accessed 2026-09-11.

[^49]: Yuqi Wang et al.. [Unified Vision-Language-Action Model](https://arxiv.org/abs/2506.19850). 2025-06-24.

[^50]: BAAI Vision. [UniVLA repository (BAAI)](https://github.com/baaivision/UniVLA). n.d.; accessed 2026-09-11.

[^51]: Jinliang Zheng et al.. [X-VLA: Soft-Prompted Transformer as Scalable Cross-Embodiment Vision-Language-Action Model](https://arxiv.org/abs/2510.10274). 2025-10-11.

[^52]: Tsinghua AIR / Shanghai AI Laboratory and collaborators. [X-VLA project](https://thu-air-dream.github.io/X-VLA/). n.d.; accessed 2026-09-11.

[^53]: Wei Wu et al.. [From Foundation to Application: Improving VLA Models in Practice](https://arxiv.org/abs/2607.06403). 2026-07-07.

[^54]: Robbyant. [LingBot-VLA 2.0 repository](https://github.com/Robbyant/lingbot-vla-v2). n.d.; accessed 2026-09-11.

[^55]: Kevin Black, Manuel Y. Galliker, Sergey Levine. [Real-Time Execution of Action Chunking Flow Policies](https://arxiv.org/abs/2506.07339). 2025-06-09.

[^56]: Michael Ahn et al.; Google Robotics / Everyday Robots. [Do As I Can, Not As I Say: Grounding Language in Robotic Affordances](https://say-can.github.io/). 2022-04-04.

[^57]: Danny Driess et al.; Google / TU Berlin. [PaLM-E: An Embodied Multimodal Language Model](https://palm-e.github.io/). 2023.

[^58]: Yunfan Jiang et al.; Stanford / NVIDIA and collaborators. [VIMA: General Robot Manipulation with Multimodal Prompts](https://vimalabs.github.io/). 2023.

[^59]: Yao Mu et al.. [EmbodiedGPT: Vision-Language Pre-Training via Embodied Chain of Thought](https://arxiv.org/abs/2305.15021). 2023-05-24.

[^60]: Wenlong Huang et al.; Stanford / UIUC. [VoxPoser: Composable 3D Value Maps for Robotic Manipulation with Language Models](https://voxposer.github.io/). 2023.

[^61]: Suraj Nair, Aravind Rajeswaran, Vikash Kumar, Chelsea Finn, Abhinav Gupta. [R3M: A Universal Visual Representation for Robot Manipulation](https://arxiv.org/abs/2203.12601). 2022-03-23.

[^62]: Arjun Majumdar et al.; Meta and collaborators. [Where are we in the search for an Artificial Visual Cortex for Embodied Intelligence?](https://arxiv.org/abs/2303.18240). 2023.

[^63]: Mohit Shridhar, Lucas Manuelli, Dieter Fox. [Perceiver-Actor: A Multi-Task Transformer for Robotic Manipulation](https://peract.github.io/). 2022.

[^64]: Ankit Goyal et al.; NVIDIA. [RVT: Robotic View Transformer for 3D Object Manipulation](https://arxiv.org/abs/2306.14896). 2023-06-26.

[^65]: Tsung-Wei Ke, Nikolaos Gkanatsios, Katerina Fragkiadaki. [3D Diffuser Actor: Policy Diffusion with 3D Scene Representations](https://3d-diffuser-actor.github.io/). 2024.

[^66]: Tsung-Wei Ke, Nikolaos Gkanatsios and collaborators. [3D Diffuser Actor official implementation](https://github.com/nickgkan/3d_diffuser_actor/blob/master/README.md). undated; accessed 2026-09-11.

[^67]: Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, Timothy Lillicrap. [Mastering Diverse Domains through World Models](https://arxiv.org/html/2301.04104v2). 2023-01-10; revised 2024-04-17.

[^68]: Danijar Hafner et al.. [Mastering diverse control tasks through world models](https://www.nature.com/articles/s41586-025-08744-2). 2025.

[^69]: Sherry Yang et al.; UC Berkeley / Google DeepMind / MIT. [UniSim: Learning Interactive Real-World Simulators](https://universal-simulator.github.io/unisim/). 2023; ICLR 2024.

[^70]: Sherry Yang et al.. [Learning Interactive Real-World Simulators](https://arxiv.org/html/2310.06114v2). 2023.

[^71]: Jake Bruce et al.; Google DeepMind. [Genie: Generative Interactive Environments](https://arxiv.org/abs/2402.15391). 2024-02-23.

[^72]: Google DeepMind. [Genie 2: A large-scale foundation world model](https://deepmind.google/blog/genie-2-a-large-scale-foundation-world-model/). 2024-12-04.

[^73]: Jack Parker-Holder and Shlomi Fruchter; Google DeepMind. [Genie 3: A new frontier for world models](https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/). 2025-08-05.

[^74]: Google. [Project Genie: Experiment with infinite, interactive worlds](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/project-genie/). 2026.

[^75]: Hongtao Wu et al.. [Unleashing Large-Scale Video Generative Pre-training for Visual Robot Manipulation](https://arxiv.org/abs/2312.13139). 2023-12-20.

[^76]: Hongtao Wu et al.. [GR-1 project: Unleashing Large-Scale Video Generative Pre-training for Visual Robot Manipulation](https://gr1-manipulation.github.io/). 2023.

[^77]: Chi-Lam Cheang et al.. [GR-2: A Generative Video-Language-Action Model with Web-Scale Knowledge for Robot Manipulation](https://arxiv.org/abs/2410.06158). 2024-10-08.

[^78]: Mahmoud Assran et al.; Meta FAIR. [V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning](https://arxiv.org/abs/2506.09985). 2025-06.

[^79]: Meta FAIR. [Introducing V-JEPA 2](https://ai.meta.com/research/vjepa/). 2025.

[^80]: Lorenzo Mur-Labadia et al.; Meta FAIR. [V-JEPA 2.1: Unlocking Dense Features in Video Self-Supervised Learning](https://arxiv.org/html/2603.14482v1). 2026-03-15.

[^81]: Meta FAIR. [V-JEPA 2, 2-AC and 2.1 official code and checkpoints](https://github.com/facebookresearch/vjepa2). updated 2026; accessed 2026-09-11.

[^82]: NVIDIA. [Supported Models: NVIDIA NIM for Cosmos WFM](https://docs.nvidia.com/nim/cosmos/latest/support-matrix.html). undated; accessed 2026-09-11.

[^83]: Moo Jin Kim et al.; NVIDIA / Stanford. [Cosmos Policy: Fine-Tuning Video Models for Visuomotor Control and Planning](https://arxiv.org/html/2601.16163v1). 2026-01-22.

[^84]: Asawaree Bhide and Alexander Schwarz; NVIDIA. [Develop Physical AI Reasoning, World, and Action Models with NVIDIA Cosmos 3](https://developer.nvidia.com/blog/develop-physical-ai-reasoning-world-and-action-models-with-nvidia-cosmos-3/). 2026-05-31.

[^85]: NVIDIA. [NVIDIA Cosmos official repository](https://github.com/nvidia/Cosmos). current repository; accessed 2026-09-11.

[^86]: Wayve research team. [GAIA-2: A Controllable Multi-View Generative World Model for Autonomous Driving](https://arxiv.org/abs/2503.20523). 2025-03-26.

[^87]: Wayve. [Wayve launches GAIA-3, advancing world models from simulation to evaluation](https://wayve.ai/press/wayve-launches-gaia3/). 2025-12-02.

[^88]: Wayve. [GAIA-4: Multimodal World Models Powering Closed-Loop Simulation for Safe and Scalable Autonomy](https://wayve.ai/thinking/gaia-4/). 2026-08-03.

[^89]: Rongyu Zhang et al.. [MoLe-VLA: Dynamic Layer-skipping Vision Language Action Model via Mixture-of-Layers for Efficient Robot Manipulation](https://arxiv.org/abs/2503.20384). 2025-03-26.

[^90]: NVIDIA / Stanford contributors. [Cosmos Policy official implementation](https://github.com/NVlabs/cosmos-policy). current repository; accessed 2026-09-11.

[^91]: Chi-Lam Cheang et al.. [GR-2: A Generative Video-Language-Action Model with Web-Scale Knowledge for Robot Manipulation (full text)](https://arxiv.org/html/2410.06158v1). 2024-10-08.

[^92]: Peng, Abbeel, Levine, van de Panne. [DeepMimic: Example-Guided Deep Reinforcement Learning of Physics-Based Character Skills](https://xbpeng.github.io/projects/DeepMimic/index.html). 2018.

[^93]: Peng, Ma, Abbeel, Levine, Kanazawa. [AMP: Adversarial Motion Priors for Stylized Physics-Based Character Control](https://xbpeng.github.io/projects/AMP/index.html). 2021.

[^94]: Peng, Guo, Halper, Levine, Fidler. [ASE: Large-Scale Reusable Adversarial Skill Embeddings for Physically Simulated Characters](https://xbpeng.github.io/projects/ASE/index.html). 2022.

[^95]: Luo, Cao, Winkler, Kitani, Xu. [Perpetual Humanoid Control for Real-time Simulated Avatars](https://arxiv.org/abs/2305.06456). 2023-05-10.

[^96]: Zhengyi Luo et al.. [PHC official implementation](https://github.com/ZhengyiLuo/PHC). 2023.

[^97]: Radosavovic, Xiao, Zhang, Darrell, Malik, Sreenath. [Learning Humanoid Locomotion with Transformers](https://humanoid-transformer.github.io/). 2023.

[^98]: He, Luo, Xiao, Zhang, Kitani, Liu, Shi. [Learning Human-to-Humanoid Real-Time Whole-Body Teleoperation](https://human2humanoid.com/). 2024-03-07.

[^99]: He, Luo, He, Xiao, Zhang, Zhang, Kitani, Liu, Shi. [OmniH2O: Universal and Dexterous Human-to-Humanoid Whole-Body Teleoperation and Learning](https://omni.human2humanoid.com/). 2024.

[^100]: Fu, Zhao, Wu, Wetzstein, Finn. [HumanPlus: Humanoid Shadowing and Imitation from Humans](https://humanoid-ai.github.io/). 2024.

[^101]: Tessler, Guo, Nabati, Chechik, Peng. [MaskedMimic: Unified Physics-Based Character Control Through Masked Motion Inpainting](https://arxiv.org/html/2409.14393v1). 2024-09-22.

[^102]: Luo et al., NVIDIA. [SONIC: Supersizing Motion Tracking for Natural Humanoid Whole-Body Control](https://arxiv.org/html/2511.07820v1). 2025-11-11.

[^103]: NVIDIA. [GR00T-WholeBodyControl: SONIC and decoupled WBC](https://github.com/NVlabs/GR00T-WholeBodyControl). 2026-08-31.

[^104]: Shah, Sridhar, Dashora, Stachowicz, Black, Hirose, Levine. [ViNT: A Foundation Model for Visual Navigation](https://arxiv.org/abs/2306.14846). 2023-06-26.

[^105]: Berkeley AI Research. [General Navigation Models: GNM, ViNT and NoMaD](https://github.com/robodhruv/visualnav-transformer). 2023.

[^106]: Sridhar, Shah, Glossop, Levine. [NoMaD: Goal Masking Diffusion Policies for Navigation and Exploration](https://general-navigation-models.github.io/nomad/). 2023.

[^107]: Chang et al.. [GOAT: GO to Any Thing](https://arxiv.org/html/2311.06430v1). 2023-11-10.

[^108]: Khanna et al.. [GOAT-Bench: A Benchmark for Multi-Modal Lifelong Navigation](https://arxiv.org/abs/2404.06609). 2024-04-09.

[^109]: Figure. [Helix: A Vision-Language-Action Model for Generalist Humanoid Control](https://www.figure.ai/news/helix). 2025-02-20.

[^110]: Figure. [Introducing Helix 02: Full-Body Autonomy](https://www.figure.ai/news/helix-02). 2026-01-27.

[^111]: Skild AI. [The case for an omni-bodied robot brain](https://www.skild.ai/blogs/omni-bodied). 2025-09-24.

[^112]: Skild AI. [Introducing S1: In-Context Learning for Robotics](https://www.skild.ai/blogs/s1). 2026-08-18.

[^113]: Deepak Pathak and Abhinav Gupta, Skild AI. [The Hidden Pillar of Robotics](https://www.skild.ai/blogs/skild-crosses-100m-arr). 2026-09-09.

[^114]: Physical Intelligence, Weave Robotics and Ultra. [The Physical Intelligence Layer](https://www.pi.website/blog/partner). 2026-02-24.

[^115]: NVIDIA. [NVIDIA Announces NVIDIA Isaac GR00T Reference Humanoid Robot for Academic Research](https://nvidianews.nvidia.com/news/nvidia-open-humanoid-robot-reference-design). 2026-05-31.

[^116]: 1X AI Team. [1X World Model: From Video to Action, A New Way Robots Learn](https://www.1x.tech/discover/world-model-self-learning). 2026-01-12.

[^117]: 1X. [Order NEO](https://www.1x.tech/order). undated, accessed 2026-09-11.

[^118]: GXO Logistics. [GXO Signs Industry-First Multi-Year Agreement with Agility Robotics](https://investors.gxo.com/node/9401/pdf). 2024-06-27.

[^119]: Agility Robotics. [Digit Moves Over 100,000 Totes in Commercial Deployment](https://www.agilityrobotics.com/content/digit-moves-over-100k-totes). undated, accessed 2026-09-11.

[^120]: Boston Dynamics. [Atlas Evolution From Research Robot to Industrial Humanoid](https://bostondynamics.com/blog/atlas-evolution-from-research-robot-to-industrial-humanoid/). 2026, exact publication date unavailable.

[^121]: Galbot. [Galbot company and technology overview](https://www.galbot.com/about/). undated, accessed 2026-09-11.

[^122]: Unitree Robotics. [UnifoLM-VLA official code and model release](https://github.com/unitreerobotics/unifolm-vla). 2026.

[^123]: NVIDIA DAIR. [SONIC: Supersizing Motion Tracking for Natural Humanoid Whole-Body Control](https://research.nvidia.com/labs/dair/publication/sonic2026/). 2026-07.

[^124]: Horizon Robotics. [HoloMotion: A Foundation Model for Whole-Body Humanoid Control](https://github.com/HorizonRobotics/HoloMotion). 2026.

[^125]: Generalist. [GEN-1: Scaling Embodied Foundation Models to Mastery](https://generalistai.com/blog/gen-1). 2026-04-02.

[^126]: Generalist. [GEN-1.5: Embodied Foundation Models are One-Shot Learners](https://generalistai.com/blog/gen-1.5). 2026-08-19.

[^127]: Figure. [F.03 Arrives at BMW](https://www.figure.ai/news/f-03-at-bmw). 2026-06-30.

[^128]: BMW Group. [BMW Group advances the use of Physical AI in production with Figure 03 project in Spartanburg](https://www.press.bmwgroup.com/canada/article/detail/T0458794EN/bmw-group-advances-the-use-of-physical-ai-in-production-with-figure-03-project-in-spartanburg). 2026-06-25.

[^129]: DROID Dataset Team. [DROID: A Large-Scale In-the-Wild Robot Manipulation Dataset](https://droid-dataset.github.io/). 2024.

[^130]: Cheng Chi et al.. [Universal Manipulation Interface](https://umi-gripper.github.io/). 2024.

[^131]: RoboMIND authors. [RoboMIND: Benchmark on Multi-embodiment Intelligence Normative Data for Robot Manipulation](https://arxiv.org/abs/2412.13877). 2024.

[^132]: OpenDriveLab and AgiBot. [AgiBot World Colosseo repository](https://github.com/OpenDriveLab/Agibot-World). 2025.

[^133]: AgiBot World Team. [AgiBot World Colosseo: Large-scale Manipulation Platform](https://agibot-world.com/blog/agibot_go1.pdf). 2025.

[^134]: Bo Liu et al.. [LIBERO: Benchmarking Knowledge Transfer in Lifelong Robot Learning](https://libero-project.github.io/main.html). 2023.

[^135]: Oier Mees et al.. [CALVIN: A Benchmark for Language-Conditioned Policy Learning](https://github.com/mees/calvin). 2022.

[^136]: SIMPLER authors. [SIMPLER: Evaluating Real-World Robot Manipulation Policies in Simulation](https://github.com/allenai/SimplerEnv). 2024.

[^137]: RoboTwin authors. [RoboTwin 2.0](https://arxiv.org/abs/2506.18088). 2025.

[^138]: Stone Tao et al.. [ManiSkill3: GPU Parallelized Robotics Simulation and Rendering](https://github.com/mani-skill/ManiSkill). 2025.

[^139]: Stanford BEHAVIOR team. [BEHAVIOR-1K and 2026 challenge](https://behavior.stanford.edu/). 2026.

[^140]: Hugging Face LeRobot team. [LeRobot: End-to-End Robot Learning](https://github.com/huggingface/lerobot). 2026.

[^141]: NVIDIA and Isaac Lab contributors. [Isaac Lab](https://developer.nvidia.com/isaac/lab). 2026.

[^142]: Jianlan Luo, Charles Xu, Jeffrey Wu, Sergey Levine. [Precise and Dexterous Robotic Manipulation via Human-in-the-Loop Reinforcement Learning](https://hil-serl.github.io/). 2024.

[^143]: SERL authors. [SERL: A Software Suite for Sample-Efficient Robotic Reinforcement Learning](https://arxiv.org/abs/2401.16013). 2024.

[^144]: Ai2 and MolmoAct2 authors. [MolmoAct2: Action Reasoning Models for Real-world Deployment](https://github.com/allenai/molmoact2). 2026-05-05.

[^145]: Haoquan Fang et al.. [MolmoAct2: Action Reasoning Models for Real-world Deployment](https://arxiv.org/abs/2605.02881). 2026.

[^146]: Ai2. [MolmoSpaces Robotics Benchmark and Leaderboard](https://molmospaces.allen.ai/leaderboard). 2026.

[^147]: DexUMI authors. [DexUMI: Using Human Hand as the Universal Manipulation Interface for Dexterous Manipulation](https://dex-umi.github.io/). 2025.

[^148]: Homer Walke et al.. [BridgeData V2: A Dataset for Robot Learning at Scale](https://rail-berkeley.github.io/bridgedata/). 2023.

[^149]: RoboCasa team. [RoboCasa365](https://robocasa.ai/). 2026.

[^150]: Tianxing Chen et al.. [RMBench: Memory-Dependent Robotic Manipulation Benchmark](https://github.com/RoboTwin-Platform/RMBench). 2026.

[^151]: Xiaomi Robotics. [Xiaomi-Robotics-0](https://robotics.xiaomi.com/xiaomi-robotics-0.html). 2026-02-12.

[^152]: Xiaomi Robotics. [Xiaomi-Robotics-0 training and deployment](https://github.com/XiaomiRobotics/Xiaomi-Robotics-0/blob/main/xr0/README.md). 2026.

[^153]: Hugging Face. [HIL-SERL Real Robot Training Workflow Guide](https://huggingface.co/docs/lerobot/hilserl). 2026.

[^154]: RoboCasa365 authors. [RoboCasa365: A Large-Scale Simulation Framework for Training and Benchmarking Generalist Robots](https://arxiv.org/abs/2603.04356). 2026.

[^155]: Stanford BEHAVIOR team. [BEHAVIOR 2026 challenge evaluation](https://github.com/StanfordVL/BEHAVIOR-1K/blob/main/docs/challenge/evaluation.md). 2026.

