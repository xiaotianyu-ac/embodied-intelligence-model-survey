## Manipulation policies and VLAs: from imitation to transferable robot foundation models

A VLA is more than a language model placed upstream of an arm. It aligns semantic information, visual observations, robot state and an action distribution through a trainable interface. Three questions organize the field: where knowledge comes from, how actions are represented and generated, and how predictions enter a real-time feedback loop. Parameter count, diffusion and dual-system branding each describe only part of that system.

Behavior cloning remains the underlying learning procedure for many robot foundation models. Diffusion, flow matching, action tokens and continuous regression are primarily alternative policy representations and objectives; using one does not establish that a model learns through autonomous reinforcement. RECAP makes a different change by introducing rewards, value estimation and policy-generated experience into training.[V001][V003][V025]

### Action representations and architectural consequences

| Route | Prediction and objective | Representative work | Benefit | Cost to inspect |
|---|---|---|---|---|
| Discrete controls | Action bins with classification/token prediction | RT-1, RT-2, original OpenVLA | Compatibility with transformer/VLM training | Resolution, sequence length and autoregressive latency |
| Continuous chunk regression | Multiple actions with L1/L2 supervision | OpenVLA-OFT | Parallel outputs and simple training | Conditional median/mean behavior for multimodal targets; language following |
| Continuous generative policy | Iterative generation of an action chunk from noise | Diffusion Policy, pi0, GR00T, SmolVLA | Continuous precision and multimodal distributions | Sampling cost and stale observations |
| Compressed action tokens | DCT, quantization and BPE on chunks | FAST, pi0-FAST | Less temporal redundancy | Compression error; training speed differs from feedback speed |
| Latent actions | Video-derived abstract action followed by a robot decoder | OpenDriveLab UniVLA | Learning without physical action labels | Loss of contact, reachability or control detail |

The routes can coexist. pi0.5 uses discrete auxiliary action training and a continuous expert. Octo combines robot pretraining with a diffusion head. GR00T uses a module called a DiT but trains action generation with flow matching. Module names alone do not identify equivalent training algorithms.[V006][V008][V015][V019][V021][V031][V047]

### Model decomposition: imitation and early foundation policies

**ACT (2023).** Small imitation errors accumulate over long tasks, while low-cost bimanual demonstrations vary. ACT takes multiview images and joint state into a transformer conditional VAE and predicts a joint-position chunk. Training combines action reconstruction with latent regularization; deployment uses a zero latent and combines overlapping predictions. Chunking improves fine manipulation from demonstrations, but the original method contains neither a general language foundation model nor guaranteed out-of-distribution force-control skills.[V001][V002]

**Diffusion Policy (2023).** A scene can admit several valid actions. This policy models continuous action sequences through conditional denoising, with visual/state encodings supplying context. At deployment it samples a chunk, executes a prefix and observes again. It establishes a foundation for subsequent generative policies, but iterative sampling costs computation, and the original visuomotor policy is not automatically a web-pretrained VLA.[V003][V004]

**RT-1 (2022).** To learn from diverse robot tasks at scale, RT-1 combines EfficientNet, language FiLM, TokenLearner and a transformer. It maps a short image history and instruction into discretized arm/base controls and a termination mode. The original dataset exceeds 130,000 episodes and 700 tasks; the policy runs at approximately 3 Hz. Its contribution is scalable multitask behavior cloning, with robot/task coverage still concentrated and language conditioning distinct from general reasoning.[V005][V006]

**RT-2 (2023).** The question shifts from scaling robot data to transferring web semantics into control. PaLI-X or PaLM-E is co-fine-tuned on robot trajectories and vision-language tasks; binned actions become text tokens and are decoded back into controls. This supports semantic object selection and instruction generalization, but new semantics do not create unseen motor skills automatically. Autoregressive inference also adds latency. RT-2 is a research successor to RT-1, not continued training of RT-1 weights.[V007][V008]

**RT-X / Open X-Embodiment (2023).** This is a cross-robot data and modeling framework with RT-1-X and RT-2-X variants, rather than one unique architecture. The initial report pools 22 embodiments, standardizes data interfaces and demonstrates positive transfer. Deployment must still restore target-specific action meaning, coordinates, units and frequency: a common storage schema does not remove dynamics differences.[V009][V010]

**Octo (2024).** Octo pretrains a transformer diffusion policy on 800,000 OXE trajectories. Tasks can be given through language or goal images; modular inputs and action heads permit sensor/action adaptation. Inference samples a continuous chunk and replans after partial execution. Its role is a transferable robot-policy initialization, without requiring a giant language decoder; new platforms still need interface adaptation and fine-tuning.[V011][V012]

**OpenVLA (2024) and OpenVLA-OFT (2025).** OpenVLA combines DINOv2/SigLIP visual features with Llama 2, learning discrete actions from approximately 970,000 demonstrations as a public 7B reference. OFT explicitly adapts that foundation with parallel decoding, action chunking, continuous outputs and L1 regression. It demonstrates the importance of output and fine-tuning design. However, L1 favors a conditional median; multimodal behavior and language grounding need separate evaluation. One benchmark does not prove regression universally superior to diffusion.[V013][V014][V015][V016]

### The pi family: continuous control, hierarchy, experience and memory

**pi0 (2024).** Multiview images, text, proprioception and noisy actions enter a PaliGemma 3B backbone with a roughly 300M action expert. Flow matching transforms noise into continuous chunks; the paper uses 50-action chunks and caches the observation prefix during sampling. Broad private/public robot pretraining is followed by high-quality task post-training. Generalist initialization and specialist dexterity results should therefore be distinguished.[V017][V018]

**FAST / pi0-FAST (2025).** FAST is a representation: DCT, quantization and BPE turn temporally redundant action chunks into shorter discrete sequences. pi0-FAST is the autoregressive model using that representation; FAST itself is not a new robot architecture. Compression improves the utilization and training of high-frequency action data, but autoregressive latency remains, and compression ratio is not a feedback-speed metric.[V019][V020]

**pi0.5 and knowledge insulation (2025).** The model retains the VLM/action-expert design and separates language-level subtasks from low-level continuous actions while mixing robot and nonrobot semantic data. Knowledge insulation blocks gradients from the action expert into the VLM, yet discrete-action and vision-language objectives still train the backbone. It is therefore not simply backbone freezing. The public openpi implementation supports only the pi0.5 flow head and should not be assumed to reproduce every training head in the paper.[V021][V022][V020]

**pi0.6 and pi-star-0.6 / RECAP (2025).** The pi0.6 model card specifies a Gemma 3 4B backbone and approximately 860M action expert, retaining pi0.5's hierarchy. RECAP adds offline reinforcement pretraining, demonstrations, corrective takeovers and reward-labeled autonomous rollouts. A value function provides advantages, and deployment conditions the policy on high advantage. A stronger supervised base and an experience-trained policy are different claims; throughput gains still depend on task, rewards and intervention infrastructure.[V023][V024][V025]

**MEM / pi0.6-MEM (2026).** To address occlusion, long workflows and repeated failures, MEM combines compressed short-term visual history with long-term language memory. Past attempts can then guide changed behavior, and completed subtasks remain available to the policy. The evidence concerns within-task memory and contextual adaptation, not indefinite lifelong or cross-user retention. State loss and incorrect summaries remain distinct failure modes.[V028]

**pi0.7 (2026).** Its paper explicitly retains the pi0.6 architecture and MEM while expanding conditioning: task/subtask, quality, speed, control mode and visual subgoals permit robot, human and suboptimal autonomous experience to be combined. At deployment a high-level semantic policy can provide subtasks and a lightweight BAGEL-based world model can supply visual goals to the continuous expert. The model shows skill composition and absorption of RL-specialist experience, but some new tasks use stepwise language coaching or high-level adaptation rather than one fully autonomous zero-shot prompt.[V026][V027]

The inspected public openpi README lists pi0, pi0-FAST and pi0.5. The existence of pi0.6/pi0.7 papers and demonstrations does not establish release of their latest weights or complete data.[V020]

### GR00T and compact VLAs: scale, embodiment interfaces and execution

**SmolVLA (2025).** Designed for smaller compute budgets and community robots, it uses truncated SmolVLM2 with an approximately 100M action expert, totaling roughly 450M parameters. Images, language and projected state condition flow-generated chunks; the VLM is frozen and the expert learns from LeRobot community and target data. Compact modeling and asynchronous execution lower the experimentation barrier. Synchronous, per-step-feedback and asynchronous evaluations nevertheless have different protocols and cannot be merged into one universal frequency or success rate.[V029][V030]

**GR00T N1 (2025).** Eagle encodes vision and language; a cross-attending DiT combines these features with embodiment-specific state/action MLPs to generate continuous chunks. Flow training mixes real robots, simulation, generated trajectories and video-derived latent actions. Like pi0, it joins semantic representations with generative control, but its interfaces and data differ; this does not imply shared weights. The System 2 label does not require explicit textual planning.[V031]

**N1.5 (2025).** It improves and freezes the Eagle VLM, adds FLARE alignment with future latent features and expands data including DreamGen. Future-feature alignment is not full future-pixel generation. The authors explicitly note that new verbs supplied through synthetic trajectories are still trained skills, not unrestricted unseen-action generalization.[V032]

**N1.6 (2025).** Its technical page specifies an internal Cosmos-2B variant, a 32-layer DiT, unfrozen upper VLM layers and state-relative actions for most embodiments. Added data covers YAM, AgiBot, BEHAVIOR and Unitree G1. The page also identifies small-data relative-action accumulation, overfitting and language/OOD generalization as unresolved issues, highlighting action spaces and normalization as substantial engineering decisions.[V033]

**N1.7 (2026).** NVIDIA's engineering page describes Cosmos-Reason2-2B/Qwen3-VL, a roughly 3B checkpoint, around 32,000 hours of real/human data plus 8,000 simulated hours, and ONNX/TensorRT export. At inspection the official repository labels N1.7 GA. Its License section distinguishes Apache 2.0 code from weights under the NVIDIA Open Model License. A broader Apache 2.0 commercialization statement elsewhere in the README should not be read as applying the code license to weights; older early-access FAQ wording also requires version checking. Commercial availability is not demonstrated reliability in every field setting.[V034][V035]

One source discrepancy is retained: the N1.6 technical page calls its backbone an internal Cosmos-2B variant, whereas the later N1.7 engineering article loosely describes its predecessor as Eagle. This survey follows the version-specific technical page rather than treating the broader wording as a precise architectural statement.[V033][V034]

### Gemini Robotics: action and embodied-reasoning branches

**Gemini Robotics / ER (2025).** The VLA maps images, language and robot state into movement; ER is a VLM for spatial understanding, task reasoning and tool use. The pair can form a hierarchical system, but ER alone is not a torque-producing controller. Reports establish Gemini-based robot capabilities, while full VLA weights and training corpora remain restricted. Undisclosed action losses and parameter counts must not be invented.[V036][V037]

**Gemini Robotics 1.5 / ER 1.5 (2025).** Motion Transfer and interleaved reasoning/actions extend the VLA, while ER handles tools, plans and progress. Training covers ALOHA, bi-arm Franka, Apollo and web multimodal data. Its significance is cross-embodiment skill transfer and task-level orchestration. Some long-horizon Franka experiments add post-training, so the claim of operation without embodiment-specific post-training does not describe every result.[V038][V039]

**ER 1.6 (2026).** Its model card identifies a Gemini 3.0 Flash foundation, targeting pointing, spatial relations, instrument reading and multiview success detection. Outputs remain text/spatial representations and tool calls. This is a reasoning-branch upgrade, not a new motor decoder. The authors note that single-view and multiview success detection use different examples, and instrument tests differ in agentic-vision support; these plots are not all matched-condition comparisons.[V040][V041]

**Robotics 2, ER 2 and On-Device 2 (2026).** The July 30 release separates three roles: Robotics 2 for whole-body and dexterous action, ER 2 for understanding, planning and multi-robot coordination, and On-Device 2 for local execution and embodiment adaptation. ER 2's card identifies Gemini 3.5 Flash. On-Device 2 instead explicitly builds on Robotics 1.5 technology and on-device Gemma; it is not simply the full cloud model moved onto a device.[V042][V043][V044]

Robotics 2's published experiments still show significant multifinger and speed limitations. At launch ER was available through AI Studio, while VLA and On-Device models were for early-access partners. Local execution, API access and public weights are separate properties. Missing training losses, architectural details and full data inventories remain undisclosed.[V042][V044]

### Additional representative approaches and name disambiguation

**RDT-1B (2024).** A 1.2B robotics diffusion transformer combines language, images, state and control frequency for bimanual action generation. A physically interpretable unified action space supports heterogeneous pretraining, followed by bimanual fine-tuning. The contribution is physical meaning in the transfer interface, rather than merely padding vectors to equal length. Units, masks and coordinate conventions still require careful mapping.[V045][V046]

**OpenDriveLab UniVLA (2025).** Video frame pairs and task text train a VQ-VAE latent-action model in DINO feature space. A VLA predicts these task-relevant latent actions, and target-robot supervision trains a lightweight decoder. This exploits human videos lacking physical robot-action labels, but abstract actions still require embodiment grounding and can omit fine contact or dynamics information.[V047][V048]

**BAAI UniVLA (2025).** A separate same-named work starts from Emu3, representing vision, language and actions with discrete tokens and using world-model video post-training to improve policy learning. Authors, paper identifiers and mechanisms differ: task-centric latent actions versus unified multimodal generation. Its repository also displays CALVIN results with increased inference steps, requiring budget alignment before comparison.[V049][V050]

**X-VLA (2025).** Florence-Large handles the main visual/language stream while auxiliary wrist views are encoded separately. Data-source/embodiment soft prompts and input/output projections adapt heterogeneous observations and controls; a standard transformer generates flow-matching action chunks. This separates shared capability from hardware-specific parameters, but soft prompts do not remove configuration or adaptation requirements for unseen hardware.[V051][V052]

**LingBot-VLA 2.0 (2026).** A Qwen3-VL-based backbone, sparse MoE action expert and future semantic/depth distillation combine scaling with predictive control. Its approximately 60,000 curated hours comprise 50,000 robot hours across 20 configurations and 10,000 human egocentric hours. The 55-dimensional canonical interface includes four reserved slots and expands to head, waist, base and dexterous hands. The reported mixed-training GM-100 table evaluates nine tasks, and two long-horizon tests use 15 trials per setting; it does not establish that the entire benchmark or general OOD manipulation is solved.[V053][V054]

### Model relationships and defensible comparisons

Five relationship types matter: architecture/checkpoint inheritance, data reuse, auxiliary modules/objectives, training-procedure changes and system composition. OpenVLA to OFT is explicit adaptation; OXE to Octo/OpenVLA is a data relationship; pi0.6 to RECAP is RL post-training; MEM to pi0.7 is module inheritance; ER 2 and Robotics 2 are complementary components. Shared design among pi0, GR00T and SmolVLA does not prove checkpoint inheritance. The relationship catalog separately labels explicit evidence and analytical interpretation.[V011][V013][V015][V025][V026][V031][V042]

Execution comparisons must separate policy-call latency, actions generated per call, actual observation-refresh rate, low-level servo frequency and successful tasks per hour. RTC generates the next chunk while current actions execute and conditions on the committed prefix to maintain continuity. This is scheduling and conditioning, not additional semantic knowledge. Longer chunks can improve action-generation throughput while delaying response to new observations.[V055]

Matched evaluation requires the same robot, task and scene splits; training data and pretraining exposure; action space and control frequency; sampling steps, retries and adaptation protocol. LIBERO success, CALVIN chain length, GM-100 progress, long-task completion and hourly throughput measure different things and should not form one universal leaderboard. Cross-embodiment zero-shot claims must specify whether the novelty concerns objects, scenes, skills, bodies, or merely a skill–body combination.[V015][V032][V038][V050][V053]
