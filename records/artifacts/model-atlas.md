# Model Atlas / 模型与方法拆解

This structured atlas preserves each card's input, architecture, objective, data, execution, contribution, limitations, and available assets. Main analytical explanations are provided in both report editions. Entries include versions and methods.

## ACT (2023)

ID: `act`

**Family / 分类:** chunked imitation

**Inputs / 输入:** Multi-view RGB and joint state

**Architecture / 架构:** Visual encoder and transformer CVAE

**Action representation / 动作表示:** Joint-position action chunks

**Training objective / 训练:** Action reconstruction plus KL regularization

**Data / 数据:** Task-specific teleoperation demonstrations

**Execution and feedback / 推理闭环:** Zero latent at deployment; repeatedly predict chunks and combine overlapping predictions

**Contribution / 贡献:** Reduce effective imitation horizon on low-cost bimanual hardware

**Limitations / 局限:** Limited demonstration support; no built-in language foundation model or guaranteed contact-force reasoning

**Available assets / 开放程度:** Code and hardware design available

**Sources:** [S001](https://arxiv.org/abs/2304.13705), [S002](https://tonyzhaozh.github.io/aloha/)

## Diffusion Policy (2023)

ID: `diffusion-policy`

**Family / 分类:** generative imitation

**Inputs / 输入:** Recent visual observations and robot state

**Architecture / 架构:** Conditional temporal diffusion network

**Action representation / 动作表示:** Continuous future action sequence

**Training objective / 训练:** Denoising / score learning on expert actions

**Data / 数据:** Robot manipulation demonstration benchmarks

**Execution and feedback / 推理闭环:** Iterative denoising; execute a prefix and re-observe

**Contribution / 贡献:** Model multimodal action distributions with receding-horizon feedback

**Limitations / 局限:** Sampling cost and data coverage remain limiting; original model is not automatically a web-pretrained VLA

**Available assets / 开放程度:** Code and training materials available

**Sources:** [S003](https://arxiv.org/abs/2303.04137), [S004](https://diffusion-policy.cs.columbia.edu/diffusion_policy_ijrr.pdf)

## RT-1 (2022)

ID: `rt1`

**Family / 分类:** robotics transformer

**Inputs / 输入:** Short image history and language instruction

**Architecture / 架构:** EfficientNet with FiLM, TokenLearner, transformer

**Action representation / 动作表示:** Discretized arm/base controls and termination mode

**Training objective / 训练:** Supervised action-token prediction

**Data / 数据:** Over 130k episodes, over 700 tasks, 13 robots

**Execution and feedback / 推理闭环:** 3 Hz policy loop with termination condition

**Contribution / 贡献:** Demonstrated scalable multitask robot behavior cloning

**Limitations / 局限:** Mostly restricted robot/task distribution; language conditioning is not equivalent to large VLM reasoning

**Available assets / 开放程度:** Code and data links public

**Sources:** [S005](https://arxiv.org/abs/2212.06817), [S006](https://robotics-transformer1.github.io/)

## RT-2 (2023)

ID: `rt2`

**Family / 分类:** autoregressive VLA

**Inputs / 输入:** RGB and task text

**Architecture / 架构:** Pretrained PaLI-X or PaLM-E adapted to robot control

**Action representation / 动作表示:** Robot action bins serialized as text tokens

**Training objective / 训练:** Co-fine-tuning robot trajectories and web vision-language tasks

**Data / 数据:** Robot actions plus web VLM corpora

**Execution and feedback / 推理闭环:** Autoregressively generate and detokenize actions, then re-observe

**Contribution / 贡献:** Transfer semantic web knowledge directly into action selection

**Limitations / 局限:** New semantic concepts do not imply new low-level motor skills; large decoder adds latency

**Available assets / 开放程度:** Research report; complete trained model not openly reproduced

**Sources:** [S007](https://arxiv.org/abs/2307.15818), [S008](https://robotics-transformer2.github.io/)

## RT-X / Open X-Embodiment (2023)

ID: `rtx`

**Family / 分类:** cross-embodiment policy and data

**Inputs / 输入:** Robot images and language across platforms

**Architecture / 架构:** RT-1-X and RT-2-X retain their respective base architectures

**Action representation / 动作表示:** Standardized action interfaces with dataset-specific semantics

**Training objective / 训练:** Multirobot supervised policy learning

**Data / 数据:** Pooled data from 22 robot embodiments in initial report

**Execution and feedback / 推理闭环:** Decode to target robot interface within a feedback loop

**Contribution / 贡献:** Established positive transfer from heterogeneous robot experience

**Limitations / 局限:** Common file schema does not ensure identical physics, control frequency, or coordinates

**Available assets / 开放程度:** Dataset/code resources; openness differs between RT variants

**Sources:** [S009](https://arxiv.org/abs/2310.08864), [S010](https://github.com/google-deepmind/open_x_embodiment)

## Octo (2024)

ID: `octo`

**Family / 分类:** generalist diffusion policy

**Inputs / 输入:** Language or goal image; flexible observation streams

**Architecture / 架构:** Modular tokenizers, transformer and diffusion action head

**Action representation / 动作表示:** Continuous action chunks; replaceable action heads

**Training objective / 训练:** Robot pretraining plus efficient domain fine-tuning

**Data / 数据:** 800k Open X-Embodiment trajectories

**Execution and feedback / 推理闭环:** Sample action chunk, execute prefix, replan

**Contribution / 贡献:** Flexible sensors and action spaces without requiring a giant language decoder

**Limitations / 局限:** Needs adaptation for new interfaces; robot pretraining does not by itself give broad conversational reasoning

**Available assets / 开放程度:** Open code and checkpoints

**Sources:** [S011](https://arxiv.org/abs/2405.12213), [S012](https://github.com/octo-models/octo)

## OpenVLA (2024)

ID: `openvla`

**Family / 分类:** autoregressive VLA

**Inputs / 输入:** Robot image and instruction

**Architecture / 架构:** DINOv2/SigLIP visual features with Llama 2 language backbone

**Action representation / 动作表示:** Discretized robot action tokens

**Training objective / 训练:** Action-token cross-entropy and optional efficient fine-tuning

**Data / 数据:** 970k real robot demonstrations; 7B model

**Execution and feedback / 推理闭环:** Sequential action-token decoding and robot feedback

**Contribution / 贡献:** Accessible VLA pretraining and adaptation reference

**Limitations / 局限:** Original decoder is expensive for high-frequency chunks; new hardware generally requires tuning

**Available assets / 开放程度:** Code and weights available; component licenses apply

**Sources:** [S013](https://arxiv.org/abs/2406.09246), [S014](https://github.com/openvla/openvla)

## OpenVLA-OFT (2025)

ID: `openvla-oft`

**Family / 分类:** VLA fine-tuning recipe

**Inputs / 输入:** Images, instruction and configurable robot state

**Architecture / 架构:** OpenVLA adapted for parallel chunk prediction

**Action representation / 动作表示:** Continuous action chunks

**Training objective / 训练:** L1 regression with parallel decoding and chunking

**Data / 数据:** Task-adaptation data; LIBERO and real ALOHA evaluations

**Execution and feedback / 推理闭环:** Predict multiple actions in parallel; update observations during control

**Contribution / 贡献:** Shows fine-tuning/output design can dominate practical speed and success

**Limitations / 局限:** L1 favors a conditional median; multimodal behavior and language grounding need separate checks

**Available assets / 开放程度:** Code and checkpoints public

**Sources:** [S015](https://arxiv.org/abs/2502.19645), [S016](https://openvla-oft.github.io/)

## pi0 (2024)

ID: `pi0`

**Family / 分类:** flow VLA

**Inputs / 输入:** Multi-view images, text, proprioception and noisy actions

**Architecture / 架构:** PaliGemma 3B plus roughly 300M robot action expert

**Action representation / 动作表示:** Continuous chunks of 50 actions in the reported setup

**Training objective / 训练:** Conditional flow matching; broad pretraining then dexterous post-training

**Data / 数据:** Private multirobot data mixed with open robot datasets

**Execution and feedback / 推理闭环:** Cache observation prefix; integrate action vector field and execute chunks

**Contribution / 贡献:** Combine semantic VLM features with continuous dexterous control

**Limitations / 局限:** Base generality and specialist performance are different settings; dataset mixture is not fully open

**Available assets / 开放程度:** openpi releases code and selected weights

**Sources:** [S017](https://www.pi.website/download/pi0.pdf), [S018](https://www.pi.website/blog/pi0), [S020](https://github.com/Physical-Intelligence/openpi)

## FAST / pi0-FAST (2025)

ID: `fast`

**Family / 分类:** action tokenization and autoregressive VLA

**Inputs / 输入:** Normalized continuous action chunks during tokenization; image/text at policy time

**Architecture / 架构:** DCT, quantization and BPE tokenizer with autoregressive policy

**Action representation / 动作表示:** Compressed frequency-domain action tokens

**Training objective / 训练:** Next-token learning on compressed robot sequences

**Data / 数据:** Robot trajectories including dexterous tasks and DROID adaptation

**Execution and feedback / 推理闭环:** Generate tokens; inverse transform to continuous chunks

**Contribution / 贡献:** Removes redundancy in high-frequency action sequences

**Limitations / 局限:** Token compression and training speed do not guarantee low closed-loop latency; quantization is a design tradeoff

**Available assets / 开放程度:** Tokenizer and pi0-FAST models available

**Sources:** [S019](https://www.pi.website/research/fast), [S020](https://github.com/Physical-Intelligence/openpi)

## pi0.5 / knowledge insulation (2025)

ID: `pi05`

**Family / 分类:** hierarchical flow VLA

**Inputs / 输入:** Images, task/subtask text and robot state

**Architecture / 架构:** PaliGemma VLM plus continuous action expert and token objectives

**Action representation / 动作表示:** Language subtasks; discrete auxiliary actions; continuous motor chunks

**Training objective / 训练:** Heterogeneous co-training; KI blocks expert gradients while token/VLM objectives train backbone

**Data / 数据:** Multirobot trajectories, semantic/subtask annotations and nonrobot VLM data

**Execution and feedback / 推理闭环:** High-level subtask prediction conditions faster low-level action generation

**Contribution / 贡献:** Improve open-environment generalization while preserving semantic features

**Limitations / 局限:** KI is not simply freezing the VLM; original paper and open implementation differ in supported heads

**Available assets / 开放程度:** openpi code and pi0.5 flow checkpoints available

**Sources:** [S021](https://www.pi.website/download/pi05.pdf), [S022](https://www.pi.website/research/knowledge_insulation), [S020](https://github.com/Physical-Intelligence/openpi)

## pi0.6 (2025)

ID: `pi06`

**Family / 分类:** hierarchical flow VLA

**Inputs / 输入:** Images, robot state, text and heterogeneous prompt metadata

**Architecture / 架构:** Gemma 3 4B backbone plus about 860M action expert

**Action representation / 动作表示:** Discrete outputs and continuous action chunks

**Training objective / 训练:** Supervised VLA training with revised architecture and data

**Data / 数据:** Expanded heterogeneous robot training data; full corpus undisclosed

**Execution and feedback / 推理闭环:** Predict subtasks and conditional motor chunks

**Contribution / 贡献:** Refinement of pi0.5 and starting point for real-world RL

**Limitations / 局限:** Architecture change is distinct from RECAP improvement; do not call the base model RL-trained

**Available assets / 开放程度:** Model card available; inspected openpi does not list this checkpoint

**Sources:** [S023](https://website.pi-asset.com/pi06star/PI06_model_card.pdf), [S024](https://www.pi.website/blog/pistar06)

## pi-star-0.6 / RECAP (2025)

ID: `pi06-recap`

**Family / 分类:** reinforcement post-training

**Inputs / 输入:** pi0.6 observations with desired advantage condition

**Architecture / 架构:** pi0.6 policy plus learned value function during training

**Action representation / 动作表示:** Advantage-conditioned continuous robot actions

**Training objective / 训练:** Offline RL, demonstrations, corrective takeovers and autonomous reward-labeled rollouts

**Data / 数据:** Generalist data and task-specific on-robot experience

**Execution and feedback / 推理闭环:** Condition on high advantage at execution; value learning improves next policy iteration

**Contribution / 贡献:** Improve both successful completions per hour and reliability

**Limitations / 局限:** Reward and intervention infrastructure is task-specific; results do not establish unconstrained autonomous self-improvement

**Available assets / 开放程度:** Paper and model details; complete RL pipeline/data not publicly reproducible

**Sources:** [S024](https://www.pi.website/blog/pistar06), [S025](https://www.pi.website/download/pistar06.pdf)

## MEM / pi0.6-MEM (2026)

ID: `mem`

**Family / 分类:** memory-augmented VLA

**Inputs / 输入:** Video history, language memory, current observations and state

**Architecture / 架构:** Compressed short-term visual encoder plus long-term textual state

**Action representation / 动作表示:** Subtasks and continuous action chunks from augmented VLA

**Training objective / 训练:** Train with robot/nonrobot images and video plus task history

**Data / 数据:** Diverse robot and nonrobot corpus; evaluated memory-dependent tasks

**Execution and feedback / 推理闭环:** Update memory and condition subsequent decisions on prior attempts

**Contribution / 贡献:** Address partial observability and repeated failed strategies

**Limitations / 局限:** Task memory is not lifelong retention; summaries can lose or corrupt state

**Available assets / 开放程度:** Research page/paper; no complete public checkpoint confirmed

**Sources:** [S028](https://www.pi.website/research/memory)

## pi0.7 (2026)

ID: `pi07`

**Family / 分类:** steerable generalist VLA

**Inputs / 输入:** Current/history observations, task/subtask, quality/speed metadata, optional visual subgoals

**Architecture / 架构:** pi0.6 architecture plus MEM; Gemma 3 4B and 860M flow expert

**Action representation / 动作表示:** Continuous actions conditioned on varied multimodal prompts

**Training objective / 训练:** Conditioned learning from diverse-quality data; absorb RL specialist experience

**Data / 数据:** Multirobot, human and autonomous data; exact mixture not fully released

**Execution and feedback / 推理闭环:** High-level policy and optional BAGEL-based world model generate subgoals; VLA acts and updates memory

**Contribution / 贡献:** Compositional skill reuse through better conditioning rather than a wholly new backbone

**Limitations / 局限:** Some tasks require language coaching or adapted high-level policy; broad generality remains author-evaluated

**Available assets / 开放程度:** Technical report; inspected openpi does not list public pi0.7 weights

**Sources:** [S026](https://www.pi.website/download/pi07.pdf), [S027](https://www.pi.website/blog/pi07), [S020](https://github.com/Physical-Intelligence/openpi)

## SmolVLA (2025)

ID: `smolvla`

**Family / 分类:** compact flow VLA

**Inputs / 输入:** Images, language and projected robot state

**Architecture / 架构:** Truncated SmolVLM2 with approximately 100M action expert; 450M total

**Action representation / 动作表示:** Continuous action chunks

**Training objective / 训练:** Freeze VLM and learn flow-matching expert

**Data / 数据:** LeRobot community demonstrations and target fine-tuning

**Execution and feedback / 推理闭环:** Iterative flow generation; synchronous and asynchronous scheduling evaluated separately

**Contribution / 贡献:** Lower model footprint and accessible robot-policy experimentation

**Limitations / 局限:** Community/task coverage and execution schedule affect results; no universal real-time frequency

**Available assets / 开放程度:** Open code, checkpoints and community datasets

**Sources:** [S029](https://arxiv.org/abs/2506.01844), [S030](https://huggingface.co/blog/smolvla)

## GR00T N1 (2025)

ID: `groot-n1`

**Family / 分类:** generalist humanoid VLA

**Inputs / 输入:** Images, language and embodiment-specific state

**Architecture / 架构:** Eagle VLM features cross-attended by flow DiT; embodiment MLPs

**Action representation / 动作表示:** Continuous chunks, with robot and learned latent action targets

**Training objective / 训练:** Flow matching across real, simulated, neural-generated and human data

**Data / 数据:** Multirobot demonstrations, simulation, human videos

**Execution and feedback / 推理闭环:** Action expert samples chunks; hardware controller tracks commands

**Contribution / 贡献:** Connect semantic perception to multiple embodiments and synthetic-data pipelines

**Limitations / 局限:** System 2 naming does not prove explicit planning; transfer still needs target post-training

**Available assets / 开放程度:** Open weights/code with release-specific terms

**Sources:** [S031](https://arxiv.org/abs/2503.14734)

## GR00T N1.5 (2025)

ID: `groot-n15`

**Family / 分类:** generalist humanoid VLA

**Inputs / 输入:** Images, text, state and noised actions

**Architecture / 架构:** Frozen Eagle 2.5-derived VLM and DiT

**Action representation / 动作表示:** Continuous flow actions with future-feature auxiliary target

**Training objective / 训练:** Flow loss plus FLARE latent future alignment

**Data / 数据:** N1 mixture expanded with DreamGen and other robot sources

**Execution and feedback / 推理闭环:** Cross-attended chunk generation and target adaptation

**Contribution / 贡献:** Stronger language grounding; learn useful future representation from videos

**Limitations / 局限:** New verbs supplied through synthetic trajectories are trained skills, not unrestricted zero-shot transfer

**Available assets / 开放程度:** Versioned code and model cards available

**Sources:** [S032](https://research.nvidia.com/labs/gear/gr00t-n1_5/), [S035](https://github.com/NVIDIA/Isaac-GR00T)

## GR00T N1.6 (2025)

ID: `groot-n16`

**Family / 分类:** generalist humanoid VLA

**Inputs / 输入:** Flexible-resolution images, language and robot state

**Architecture / 架构:** Cosmos-2B internal VLM variant; 32-layer DiT; top VLM layers unfrozen

**Action representation / 动作表示:** Mostly state-relative action chunks

**Training objective / 训练:** Mixed pretraining and regularized target post-training

**Data / 数据:** Additional YAM, AgiBot, BEHAVIOR and Unitree G1 data

**Execution and feedback / 推理闭环:** Chunk generation with optional real-time chunking

**Contribution / 贡献:** Expanded embodiments and improved motion modeling

**Limitations / 局限:** Relative actions can accumulate errors; language/OOD generalization remains explicitly unresolved

**Available assets / 开放程度:** Code and model-card releases available

**Sources:** [S033](https://research.nvidia.com/labs/gear/gr00t-n1_6/), [S035](https://github.com/NVIDIA/Isaac-GR00T)

## GR00T N1.7 (2026)

ID: `groot-n17`

**Family / 分类:** generalist humanoid VLA

**Inputs / 输入:** Images, instruction and robot state

**Architecture / 架构:** Cosmos-Reason2-2B / Qwen3-VL backbone plus action DiT; 3B checkpoint

**Action representation / 动作表示:** Continuous robot action chunks

**Training objective / 训练:** Generalist pretraining and robot-specific post-training

**Data / 数据:** Vendor reports around 32k hours real/human and 8k simulated data

**Execution and feedback / 推理闭环:** ONNX/TensorRT export and robot runtime support

**Contribution / 贡献:** Stronger backbone and end-to-end deployment tooling

**Limitations / 局限:** Availability is not field reliability; earlier FAQ and newer GA repository differ

**Available assets / 开放程度:** Official repository labels N1.7 GA. License section: code Apache 2.0; model weights NVIDIA Open Model License. The README also contains a broader Apache 2.0 commercialization statement; do not conflate code and weight terms, and check the specific checkpoint.

**Sources:** [S034](https://developer.nvidia.com/blog/develop-humanoid-robot-policies-end-to-end-with-nvidia-isaac-gr00t/), [S035](https://github.com/NVIDIA/Isaac-GR00T)

## Gemini Robotics / ER (2025)

ID: `gemini-robotics1`

**Family / 分类:** proprietary VLA and reasoning pair

**Inputs / 输入:** VLA: images, instructions and robot state; ER: multimodal context

**Architecture / 架构:** Gemini-based action model alongside separate embodied reasoning VLM

**Action representation / 动作表示:** VLA motor commands; ER plans, spatial outputs and tool calls

**Training objective / 训练:** Robot adaptation of multimodal pretrained models; full recipe undisclosed

**Data / 数据:** Web multimodal and robot data

**Execution and feedback / 推理闭环:** ER can plan; VLA repeatedly grounds observations into movement

**Contribution / 贡献:** Clear separation between physical reasoning and executable control

**Limitations / 局限:** ER alone is not a motor policy; complete model/data access limited

**Available assets / 开放程度:** Research report and partner access; no open full VLA weights

**Sources:** [S036](https://arxiv.org/abs/2503.20020), [S037](https://deepmind.google/blog/gemini-robotics-brings-ai-into-the-physical-world/)

## Gemini Robotics 1.5 / ER 1.5 (2025)

ID: `gemini-robotics15`

**Family / 分类:** thinking VLA and orchestration

**Inputs / 输入:** Multirobot visual/state observations, instructions and tool context

**Architecture / 架构:** Multi-embodiment VLA with Motion Transfer; separate ER orchestration

**Action representation / 动作表示:** Motor actions interleaved with language reasoning; ER task plans

**Training objective / 训练:** Cross-embodiment training and thinking behavior; exact full recipe undisclosed

**Data / 数据:** ALOHA, bimanual Franka, Apollo and web text/image/video

**Execution and feedback / 推理闭环:** ER calls tools and dispatches subtasks; VLA reasons and acts with feedback

**Contribution / 贡献:** Motion transfer and agentic multi-step behavior

**Limitations / 局限:** Some long-horizon Franka results include additional post-training; reasoning text is not a safety proof

**Available assets / 开放程度:** ER API availability; VLA restricted to partners at release

**Sources:** [S038](https://arxiv.org/abs/2510.03342), [S039](https://deepmind.google/blog/gemini-robotics-15-brings-ai-agents-into-the-physical-world/)

## Gemini Robotics-ER 1.6 (2026)

ID: `gemini-er16`

**Family / 分类:** embodied reasoning VLM

**Inputs / 输入:** Text, images, audio and video

**Architecture / 架构:** Gemini 3.0 Flash-derived reasoning model

**Action representation / 动作表示:** Text/spatial representations and function calls, not direct torques

**Training objective / 训练:** Gemini training plus embodied reasoning data; exact objective undisclosed

**Data / 数据:** General multimodal and specialized embodied reasoning datasets

**Execution and feedback / 推理闭环:** Infer geometry/progress, invoke tools or downstream policies

**Contribution / 贡献:** Better instrument reading, pointing and multiview success estimation

**Limitations / 局限:** Success-detector mistakes propagate; single/multiview benchmark examples differ

**Available assets / 开放程度:** API/model card; closed weights

**Sources:** [S040](https://deepmind.google/models/model-cards/gemini-robotics-er-1-6/), [S041](https://deepmind.google/blog/gemini-robotics-er-1-6/)

## Gemini Robotics 2 (2026)

ID: `gemini-robotics2`

**Family / 分类:** whole-body VLA

**Inputs / 输入:** Visual observations, language and robot state

**Architecture / 架构:** Next-generation multi-embodiment Gemini VLA; internal details undisclosed

**Action representation / 动作表示:** Whole-body and dexterous motor commands

**Training objective / 训练:** Robot foundation-model training; full losses and corpus not disclosed

**Data / 数据:** Vendor robot experiments across Apollo and bimanual platforms

**Execution and feedback / 推理闭环:** Execute whole-body tasks under observation feedback and ER coordination

**Contribution / 贡献:** Extend control from upper-body manipulation to whole-body tasks

**Limitations / 局限:** Author reports remaining speed and multifinger failures; no public full training recipe

**Available assets / 开放程度:** Early-access partner VLA

**Sources:** [S042](https://deepmind.google/blog/gemini-robotics-2-brings-whole-body-intelligence-to-robots/)

## Gemini Robotics ER 2 (2026)

ID: `gemini-er2`

**Family / 分类:** embodied reasoning VLM

**Inputs / 输入:** Multimodal scene and task context

**Architecture / 架构:** Gemini 3.5 Flash-derived embodied reasoning model

**Action representation / 动作表示:** Plans, text, coordination and tool calls

**Training objective / 训练:** Gemini 3.5 data plus specialized embodied reasoning data

**Data / 数据:** Undisclosed complete corpus

**Execution and feedback / 推理闭环:** Orchestrate robot activities and coordinate multiple robots

**Contribution / 贡献:** Agentic coordination complements whole-body VLA

**Limitations / 局限:** Reasoning benchmark gains do not establish motor reliability

**Available assets / 开放程度:** AI Studio access; enterprise private preview stated at launch

**Sources:** [S042](https://deepmind.google/blog/gemini-robotics-2-brings-whole-body-intelligence-to-robots/), [S043](https://deepmind.google/models/model-cards/gemini-robotics-er-2/)

## Gemini Robotics On-Device 2 (2026)

ID: `gemini-ondevice2`

**Family / 分类:** local VLA

**Inputs / 输入:** Images, instruction and numerical proprioception

**Architecture / 架构:** Robotics 1.5 technology combined with on-device Gemma

**Action representation / 动作表示:** Numerical robot action outputs

**Training objective / 训练:** Robot sensor/action and multimodal training; detailed losses undisclosed

**Data / 数据:** Proprietary training corpus; adaptation data for new embodiment

**Execution and feedback / 推理闭环:** Run local inference and act under sensor feedback

**Contribution / 贡献:** Local deployment and faster new-embodiment adaptation

**Limitations / 局限:** On-device does not mean open weights; adaptation hours are data requirements, not a universal deployment guarantee

**Available assets / 开放程度:** Early-access partner model

**Sources:** [S042](https://deepmind.google/blog/gemini-robotics-2-brings-whole-body-intelligence-to-robots/), [S044](https://deepmind.google/models/model-cards/gemini-robotics-on-device-2/)

## RDT-1B (2024)

ID: `rdt1b`

**Family / 分类:** bimanual diffusion foundation policy

**Inputs / 输入:** Language, multiview images, state and control frequency

**Architecture / 架构:** Scalable 1.2B robotics diffusion transformer

**Action representation / 动作表示:** Physically interpretable unified continuous action space

**Training objective / 训练:** Denoising pretraining followed by bimanual fine-tuning

**Data / 数据:** Large multirobot collection and over 6k bimanual episodes

**Execution and feedback / 推理闭环:** Denoise action chunks and execute with feedback

**Contribution / 贡献:** Explicit action semantics support heterogeneous robot transfer

**Limitations / 局限:** Unified slots still require correct units, masks and robot-specific mapping; iterative sampling costs

**Available assets / 开放程度:** Code and weights available

**Sources:** [S045](https://arxiv.org/abs/2410.07864), [S046](https://github.com/thu-ml/RoboticsDiffusionTransformer)

## UniVLA (OpenDriveLab) (2025)

ID: `univla-odl`

**Family / 分类:** latent-action VLA

**Inputs / 输入:** Video frame pairs and task language for learning; observation and language for policy

**Architecture / 架构:** Task-conditioned VQ-VAE in DINO feature space; VLA plus lightweight action decoder

**Action representation / 动作表示:** Embodiment-agnostic latent action tokens decoded to physical controls

**Training objective / 训练:** Latent-action learning, policy pretraining and robot decoder adaptation

**Data / 数据:** Cross-embodiment OpenX and human Ego4D videos

**Execution and feedback / 推理闭环:** Predict latent action, decode for target robot, re-observe

**Contribution / 贡献:** Use videos lacking robot action labels while suppressing task-irrelevant motion

**Limitations / 局限:** Latent action abstraction may omit contact/control detail; decoder still needs real robot supervision

**Available assets / 开放程度:** Code and checkpoints public

**Sources:** [S047](https://arxiv.org/abs/2505.06111), [S048](https://github.com/OpenDriveLab/UniVLA)

## UniVLA (BAAI) (2025)

ID: `univla-baai`

**Family / 分类:** unified multimodal generative VLA

**Inputs / 输入:** Image/video, language and action sequences

**Architecture / 架构:** Emu3-based autoregressive multimodal model

**Action representation / 动作表示:** Discrete visual, language and action tokens

**Training objective / 训练:** World-model post-training and downstream policy learning

**Data / 数据:** Video and robot benchmark data

**Execution and feedback / 推理闭环:** Generate action tokens using learned temporal representations

**Contribution / 贡献:** Unify visual prediction and action learning in one token framework

**Limitations / 局限:** Distinct from OpenDriveLab UniVLA; inference budgets and benchmark variants matter

**Available assets / 开放程度:** Code, models and training paths available

**Sources:** [S049](https://arxiv.org/abs/2506.19850), [S050](https://github.com/baaivision/UniVLA)

## X-VLA (2025)

ID: `xvla`

**Family / 分类:** soft-prompt flow VLA

**Inputs / 输入:** Fixed and wrist images, language, state, dataset/embodiment identity

**Architecture / 架构:** Florence-Large vision-language stream, separate auxiliary vision, soft-prompted transformer

**Action representation / 动作表示:** Continuous action chunks with domain input/output projections

**Training objective / 训练:** Flow matching with embodiment-specific soft prompts and balanced heterogeneous data

**Data / 数据:** Multiple robot datasets and simulation/real adaptation settings

**Execution and feedback / 推理闭环:** Condition action generation on target prompt and robot interface

**Contribution / 贡献:** Separate shared skills from embodiment-specific conditioning efficiently

**Limitations / 局限:** Soft prompts require valid domain identity/adaptation; not automatic support for arbitrary hardware

**Available assets / 开放程度:** Code and checkpoints linked from project

**Sources:** [S051](https://arxiv.org/abs/2510.10274), [S052](https://thu-air-dream.github.io/X-VLA/)

## LingBot-VLA 2.0 (2026)

ID: `lingbot-vla2`

**Family / 分类:** MoE and predictive VLA

**Inputs / 输入:** Images, text, canonical robot state

**Architecture / 架构:** Qwen3-VL-based model, sparse MoE action expert and semantic/depth future distillation

**Action representation / 动作表示:** 55-dimensional canonical state/action including four reserved slots

**Training objective / 训练:** Action learning plus dual-query future-feature/depth supervision; action-loss choices ablated

**Data / 数据:** 60k curated hours: 50k robot from 20 configurations and 10k human ego

**Execution and feedback / 推理闭环:** Predict physical actions with target embodiment mapping and feedback

**Contribution / 贡献:** Combine scaling, wider body action coverage and predictive priors

**Limitations / 局限:** Nine GM-100 tasks are not the whole benchmark; OOD full-task success remains low in some tests

**Available assets / 开放程度:** 6B native-depth checkpoint and code released

**Sources:** [S053](https://arxiv.org/abs/2607.06403), [S054](https://github.com/Robbyant/lingbot-vla-v2)

## Real-Time Chunking (RTC) (2025)

ID: `rtc`

**Family / 分类:** execution and conditioning method

**Inputs / 输入:** Current observations plus already committed action prefix

**Architecture / 架构:** Inpainting/conditioning procedure around an existing flow policy

**Action representation / 动作表示:** Continuous chunks with a fixed prefix

**Training objective / 训练:** Original approach can operate without retraining the backbone

**Data / 数据:** Existing pretrained policy; evaluate delayed/asynchronous execution

**Execution and feedback / 推理闭环:** Compute next chunk while executing current actions; preserve prefix continuity

**Contribution / 贡献:** Reduce pauses and discontinuities from delayed large-model inference

**Limitations / 局限:** Requires latency budgeting; not a fix for incorrect goals or unobserved collisions

**Available assets / 开放程度:** Research algorithm; integrations available in robot stacks

**Sources:** [S055](https://arxiv.org/abs/2506.07339)

## SayCan (2022)

ID: `saycan`

**Family / 分类:** hierarchical_planning

**Inputs / 输入:** instruction; skill history; state affordances

**Architecture / 架构:** Language relevance multiplied by learned skill feasibility.

**Action representation / 动作表示:** Named skills

**Training objective / 训练:** Pretrained LLM plus skill policy/value learning.

**Data / 数据:** Language pretraining and robot skill experience.

**Execution and feedback / 推理闭环:** Select skill, execute, repeat.

**Contribution / 贡献:** Connects semantic intent to executable abilities.

**Limitations / 局限:** Fixed skills; incomplete failure feedback.

**Available assets / 开放程度:** Tabletop simulation code and instruction dataset.

**Sources:** [S056](https://say-can.github.io/)

## PaLM-E (2023)

ID: `palme`

**Family / 分类:** embodied_reasoning

**Inputs / 输入:** images; continuous state; language

**Architecture / 架构:** Continuous sensor embeddings inserted into decoder language model.

**Action representation / 动作表示:** Textual low-level subgoals

**Training objective / 训练:** Joint multimodal and embodied task learning.

**Data / 数据:** Internet multimodal and robot data.

**Execution and feedback / 推理闭环:** Generate plan; execute through separate policies; add feedback.

**Contribution / 贡献:** Direct sensor-conditioned language reasoning.

**Limitations / 局限:** Large compute; low-level execution remains separate.

**Available assets / 开放程度:** Paper/project; full public weights not verified.

**Sources:** [S057](https://palm-e.github.io/)

## EmbodiedGPT (2023)

ID: `embodiedgpt`

**Family / 分类:** hierarchical_planning

**Inputs / 输入:** video; instruction

**Architecture / 架构:** Prefix-tuned 7B language model plus planning-query features.

**Action representation / 动作表示:** Subgoals and action-relevant features

**Training objective / 训练:** EgoCOT adaptation and downstream control training.

**Data / 数据:** Ego4D-derived EgoCOT; benchmark control data.

**Execution and feedback / 推理闭环:** Plan and extract features for controller.

**Contribution / 贡献:** Learned high-/low-level interface.

**Limitations / 局限:** Benchmark-specific transfer.

**Available assets / 开放程度:** Paper; release completeness not audited.

**Sources:** [S059](https://arxiv.org/abs/2305.15021)

## VIMA (2023)

ID: `vima`

**Family / 分类:** multimodal_policy

**Inputs / 输入:** text/image prompts; object observations; history

**Architecture / 架构:** T5 prompt encoder; cross-attention causal decoder.

**Action representation / 动作表示:** Tabletop manipulation primitives

**Training objective / 训练:** Behavior cloning.

**Data / 数据:** 600K+ VIMA expert trajectories.

**Execution and feedback / 推理闭环:** Autoregressively choose actions and observe outcomes.

**Contribution / 贡献:** Unified visual/text task interface.

**Limitations / 局限:** Procedural simulation and object-token assumptions.

**Available assets / 开放程度:** Code, weights, benchmark and dataset linked.

**Sources:** [S058](https://vimalabs.github.io/)

## VoxPoser (2023)

ID: `voxposer`

**Family / 分类:** geometric_planning

**Inputs / 输入:** RGB-D; instruction

**Architecture / 架构:** LLM-generated programs compose VLM-grounded 3D value maps.

**Action representation / 动作表示:** 6-DoF end-effector waypoints

**Training objective / 训练:** Pretrained components; optional online dynamics.

**Data / 数据:** Pretrained foundation data; manipulation evaluation.

**Execution and feedback / 推理闭环:** Recompute maps and plan trajectories with feedback.

**Contribution / 贡献:** Inspectable geometric objectives.

**Limitations / 局限:** Perception/calibration/planner assumptions.

**Available assets / 开放程度:** Project provides code and prompts.

**Sources:** [S060](https://voxposer.github.io/)

## R3M (2022)

ID: `r3m`

**Family / 分类:** visual_representation

**Inputs / 输入:** RGB frames

**Architecture / 架构:** Visual encoder with temporal and language-alignment objectives.

**Action representation / 动作表示:** None; downstream controller required

**Training objective / 训练:** Contrastive and compactness pretraining.

**Data / 数据:** Ego4D human videos.

**Execution and feedback / 推理闭环:** Encode observations for learned policy.

**Contribution / 贡献:** Data-efficient reusable perception.

**Limitations / 局限:** No direct actions or transition model.

**Available assets / 开放程度:** Paper links code and pretrained models.

**Sources:** [S061](https://arxiv.org/abs/2203.12601)

## VC-1 (2023)

ID: `vc1`

**Family / 分类:** visual_representation

**Inputs / 输入:** RGB images

**Architecture / 架构:** MAE-pretrained vision transformer.

**Action representation / 动作表示:** None; downstream controller required

**Training objective / 训练:** Visual pretraining plus optional adaptation.

**Data / 数据:** Egocentric video sources and ImageNet.

**Execution and feedback / 推理闭环:** Encode sensor input for downstream policy.

**Contribution / 贡献:** Broad sensorimotor representation evaluation.

**Limitations / 局限:** Adaptation and task protocol determine transfer.

**Available assets / 开放程度:** Models/code described as released.

**Sources:** [S062](https://arxiv.org/abs/2303.18240)

## PerAct (2022)

ID: `peract`

**Family / 分类:** geometric_policy

**Inputs / 输入:** RGB-D; language

**Architecture / 架构:** Perceiver over voxel and language tokens.

**Action representation / 动作表示:** Discrete 3D location, orientation, gripper

**Training objective / 训练:** Behavior cloning with keypose supervision.

**Data / 数据:** RLBench and real demonstrations.

**Execution and feedback / 推理闭环:** Predict keypose; planner executes.

**Contribution / 贡献:** Shared geometric observation/action space.

**Limitations / 局限:** Voxel cost and RGB-D calibration.

**Available assets / 开放程度:** Official code, tutorial and checkpoints.

**Sources:** [S063](https://peract.github.io/)

## RVT (2023)

ID: `rvt`

**Family / 分类:** geometric_policy

**Inputs / 输入:** RGB-D-derived scene; language

**Architecture / 架构:** Virtual-view rendering and cross-view transformer.

**Action representation / 动作表示:** Gripper keypose

**Training objective / 训练:** Behavior cloning.

**Data / 数据:** RLBench and real demonstrations.

**Execution and feedback / 推理闭环:** Fuse views, predict pose, execute.

**Contribution / 贡献:** Efficient spatial policy computation.

**Limitations / 局限:** View construction and protocol dependence.

**Available assets / 开放程度:** Official project links code and trained model.

**Sources:** [S064](https://arxiv.org/abs/2306.14896)

## 3D Diffuser Actor (2024)

ID: `3d-diffuser-actor`

**Family / 分类:** geometric_diffusion_policy

**Inputs / 输入:** RGB-D; language; robot state

**Architecture / 架构:** 3D relative attention conditions pose denoising.

**Action representation / 动作表示:** End-effector translations, rotations, gripper

**Training objective / 训练:** Conditional action diffusion.

**Data / 数据:** RLBench, CALVIN, real demonstrations.

**Execution and feedback / 推理闭环:** Denoise action; execute with task controller/planner.

**Contribution / 贡献:** Unifies 3D geometry and multimodal actions.

**Limitations / 局限:** Quaternion and benchmark conventions matter.

**Available assets / 开放程度:** Code, weights and data links.

**Sources:** [S065](https://3d-diffuser-actor.github.io/), [S066](https://github.com/nickgkan/3d_diffuser_actor/blob/master/README.md)

## DreamerV3 (2023)

ID: `dreamerv3`

**Family / 分类:** latent_model_based_rl

**Inputs / 输入:** observations; actions; rewards

**Architecture / 架构:** Recurrent latent dynamics and actor-critic.

**Action representation / 动作表示:** Environment-dependent controls

**Training objective / 训练:** World-model learning and imagined RL.

**Data / 数据:** Online environment interaction.

**Execution and feedback / 推理闭环:** Infer state, act; update model and policy.

**Contribution / 贡献:** Robust cross-domain algorithm configuration.

**Limitations / 局限:** Exploration, rewards and model error; not universal weights.

**Available assets / 开放程度:** Official algorithm code; paper/author project.

**Sources:** [S067](https://arxiv.org/html/2301.04104v2), [S068](https://www.nature.com/articles/s41586-025-08744-2)

## UniSim (2023)

ID: `unisim`

**Family / 分类:** video_world_model

**Inputs / 输入:** observation history; language or numeric action

**Architecture / 架构:** Conditional video diffusion trained across data domains.

**Action representation / 动作表示:** Input action conditions future video

**Training objective / 训练:** Heterogeneous generative modeling.

**Data / 数据:** Images, videos, robot and navigation data.

**Execution and feedback / 推理闭环:** Simulate transitions for planner/policy learning.

**Contribution / 贡献:** Generated interaction as training experience.

**Limitations / 局限:** Task-bounded transfer and model exploitation.

**Available assets / 开放程度:** Paper/project; full reproduction not verified.

**Sources:** [S069](https://universal-simulator.github.io/unisim/), [S070](https://arxiv.org/html/2310.06114v2)

## Genie (2024)

ID: `genie1`

**Family / 分类:** interactive_world_model

**Inputs / 输入:** initial image; latent action; history

**Architecture / 架构:** Video tokenizer, latent action model and autoregressive dynamics.

**Action representation / 动作表示:** Learned latent actions

**Training objective / 训练:** Unsupervised action-label-free video learning.

**Data / 数据:** Internet video.

**Execution and feedback / 推理闭环:** User action selects generated next frame.

**Contribution / 贡献:** Controllability from unlabeled video.

**Limitations / 局限:** Latent controls not calibrated motor actions.

**Available assets / 开放程度:** Research paper; open full checkpoint not verified.

**Sources:** [S071](https://arxiv.org/abs/2402.15391)

## Genie 2 (2024)

ID: `genie2`

**Family / 分类:** interactive_world_model

**Inputs / 输入:** initial image; user actions; history

**Architecture / 架构:** Autoregressive latent diffusion with causal dynamics.

**Action representation / 动作表示:** Interactive environment commands

**Training objective / 训练:** Large-scale video training.

**Data / 数据:** Video corpus; full composition undisclosed.

**Execution and feedback / 推理闭环:** Generate next frame conditioned on actions.

**Contribution / 贡献:** Interactive 3D environment diversity.

**Limitations / 局限:** Consistency and physical validity remain limited.

**Available assets / 开放程度:** Official research demonstration.

**Sources:** [S072](https://deepmind.google/blog/genie-2-a-large-scale-foundation-world-model/)

## Genie 3 (2025)

ID: `genie3`

**Family / 分类:** interactive_world_model

**Inputs / 输入:** prompt; interactive actions

**Architecture / 架构:** Detailed architecture not disclosed in checked source.

**Action representation / 动作表示:** Limited direct actions; promptable world events

**Training objective / 训练:** Training details not fully disclosed.

**Data / 数据:** Undisclosed full corpus.

**Execution and feedback / 推理闭环:** Real-time interactive world generation.

**Contribution / 贡献:** Higher resolution and longer coherent interaction.

**Limitations / 局限:** Minutes-long horizon, action and multi-agent limits.

**Available assets / 开放程度:** Official model page and gated Project Genie prototype.

**Sources:** [S073](https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/), [S074](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/project-genie/)

## GR-1 (2023)

ID: `gr1`

**Family / 分类:** video_action_policy

**Inputs / 输入:** language; image history; robot states

**Architecture / 架构:** GPT-style joint image/action sequence model.

**Action representation / 动作表示:** Robot motor actions

**Training objective / 训练:** Video pretraining then robot adaptation.

**Data / 数据:** Large video data; CALVIN and real robot trajectories.

**Execution and feedback / 推理闭环:** Predict actions and future images; execute actions.

**Contribution / 贡献:** Video generative priors for manipulation.

**Limitations / 局限:** Joint prediction not equivalent to explicit planning.

**Available assets / 开放程度:** Project/paper; release completeness not audited.

**Sources:** [S075](https://arxiv.org/abs/2312.13139), [S076](https://gr1-manipulation.github.io/)

## GR-2 (2024)

ID: `gr2`

**Family / 分类:** video_action_policy

**Inputs / 输入:** language; images; robot states

**Architecture / 架构:** Scaled generative video-language-action model.

**Action representation / 动作表示:** Robot actions

**Training objective / 训练:** Video pretraining then joint video/action fine-tuning.

**Data / 数据:** 38M video clips, 50B+ tokens; robot trajectories.

**Execution and feedback / 推理闭环:** Generate robot actions with visual predictions.

**Contribution / 贡献:** Scales temporal pretraining for policy generalization.

**Limitations / 局限:** 97.7% is the 105-task Simple setting; unseen manipulations remain substantially harder.

**Available assets / 开放程度:** Paper; complete public reproduction not verified.

**Sources:** [S077](https://arxiv.org/abs/2410.06158), [S091](https://arxiv.org/html/2410.06158v1)

## V-JEPA 2 (2025)

ID: `vjepa2`

**Family / 分类:** predictive_visual_representation

**Inputs / 输入:** video patches

**Architecture / 架构:** Encoder/predictor with masked latent targets.

**Action representation / 动作表示:** None without action-conditioned adaptation

**Training objective / 训练:** Self-supervised latent prediction.

**Data / 数据:** Large unlabeled video corpus.

**Execution and feedback / 推理闭环:** Encode and predict latent visual structure.

**Contribution / 贡献:** Video understanding without pixel reconstruction.

**Limitations / 局限:** Base model is not a direct controller.

**Available assets / 开放程度:** Code and model family released.

**Sources:** [S078](https://arxiv.org/abs/2506.09985), [S079](https://ai.meta.com/research/vjepa/), [S081](https://github.com/facebookresearch/vjepa2)

## V-JEPA 2-AC (2025)

ID: `vjepa2-ac`

**Family / 分类:** latent_world_model

**Inputs / 输入:** RGB; robot state/actions; goal image

**Architecture / 架构:** Action-conditioned predictor on pretrained latent encoder.

**Action representation / 动作表示:** Candidate robot action sequences

**Training objective / 训练:** Post-train dynamics with robot video/action records.

**Data / 数据:** Less than 62 hours of DROID.

**Execution and feedback / 推理闭环:** Optimize image-goal latent distance with MPC.

**Contribution / 贡献:** Deployment transfer without environment-specific collection.

**Limitations / 局限:** Action data used; small task collection and planning latency.

**Available assets / 开放程度:** Official code/checkpoint and planning components.

**Sources:** [S078](https://arxiv.org/abs/2506.09985), [S079](https://ai.meta.com/research/vjepa/), [S081](https://github.com/facebookresearch/vjepa2)

## V-JEPA 2.1 (2026)

ID: `vjepa21`

**Family / 分类:** predictive_visual_representation

**Inputs / 输入:** images/video; actions for adapted planner

**Architecture / 架构:** Dense/deep predictive supervision; image/video tokenizers.

**Action representation / 动作表示:** Via 2-AC-style planner

**Training objective / 训练:** Dense latent pretraining; action-conditioned adaptation.

**Data / 数据:** Scaled image/video corpus; DROID robot data.

**Execution and feedback / 推理闭环:** Improved features support goal-directed MPC.

**Contribution / 贡献:** Better spatially structured temporal representations.

**Limitations / 局限:** Grasp gain depends on planning budget; ten tasks per skill.

**Available assets / 开放程度:** 80M/300M/1B/2B models and code released.

**Sources:** [S080](https://arxiv.org/html/2603.14482v1), [S081](https://github.com/facebookresearch/vjepa2)

## Cosmos Predict 2.5 (2025)

ID: `cosmos-predict25`

**Family / 分类:** video_world_model

**Inputs / 输入:** text; images; video

**Architecture / 架构:** Video generative foundation model.

**Action representation / 动作表示:** No direct control by default

**Training objective / 训练:** Generative world-model pretraining/adaptation.

**Data / 数据:** Physical-world video data; full corpus not audited.

**Execution and feedback / 推理闭环:** Generate conditional future video.

**Contribution / 贡献:** Unified text/image/video-to-world interface.

**Limitations / 局限:** Visual generation alone does not establish robot control.

**Available assets / 开放程度:** NIM deployment and available model artifacts.

**Sources:** [S082](https://docs.nvidia.com/nim/cosmos/latest/support-matrix.html)

## Cosmos Policy (2026)

ID: `cosmos-policy`

**Family / 分类:** joint_policy_world_value

**Inputs / 输入:** multiview images; proprioception; language

**Architecture / 架构:** Predict2-2B with action/state/value encoded as latent frames.

**Action representation / 动作表示:** Continuous action chunks

**Training objective / 训练:** Single-stage target-platform post-training.

**Data / 数据:** Robot demonstrations; optional policy rollout data.

**Execution and feedback / 推理闭环:** Direct policy or best-of-N imagined planning.

**Contribution / 贡献:** Video priors become policy, dynamics and value.

**Limitations / 局限:** Search adds compute; training is platform-specific.

**Available assets / 开放程度:** Official code, checkpoints and data links.

**Sources:** [S083](https://arxiv.org/html/2601.16163v1), [S090](https://github.com/NVlabs/cosmos-policy)

## Cosmos 3 (2026)

ID: `cosmos3`

**Family / 分类:** unified_reasoning_world_action

**Inputs / 输入:** text; image/video; actions

**Architecture / 架构:** Autoregressive reasoner plus diffusion generator, Mixture-of-Transformers.

**Action representation / 动作表示:** Embodiment-specific action outputs

**Training objective / 训练:** Multimodal training and domain post-training.

**Data / 数据:** Physical AI mixtures; specific DROID checkpoints.

**Execution and feedback / 推理闭环:** Reason independently or generate futures/actions.

**Contribution / 贡献:** Unifies world understanding, prediction and action.

**Limitations / 局限:** Mode/hardware limits; Edge lacks video-to-video transfer.

**Available assets / 开放程度:** Super64B/Nano16B/Edge4B; current OpenMDW-1.1.

**Sources:** [S084](https://developer.nvidia.com/blog/develop-physical-ai-reasoning-world-and-action-models-with-nvidia-cosmos-3/), [S085](https://github.com/nvidia/Cosmos)

## GAIA-2 (2025)

ID: `gaia2`

**Family / 分类:** driving_world_model

**Inputs / 输入:** multicamera history; ego action; structured conditions

**Architecture / 架构:** Latent multiview generative dynamics.

**Action representation / 动作表示:** Ego driving conditions

**Training objective / 训练:** Controlled video generation.

**Data / 数据:** Driving sensor/video data.

**Execution and feedback / 推理闭环:** Simulate action-conditioned driving futures.

**Contribution / 贡献:** Controlled multi-camera synthetic driving scenes.

**Limitations / 局限:** Driving-specific; not manipulation policy.

**Available assets / 开放程度:** Paper/official media; open weights not verified.

**Sources:** [S086](https://arxiv.org/abs/2503.20523)

## GAIA-3 (2025)

ID: `gaia3`

**Family / 分类:** driving_world_model

**Inputs / 输入:** driving scenes; conditions

**Architecture / 架构:** Detailed architecture not established in checked release.

**Action representation / 动作表示:** Driving scenario conditions

**Training objective / 训练:** Generative modeling; full recipe undisclosed.

**Data / 数据:** Driving data.

**Execution and feedback / 推理闭环:** Generate scenarios for evaluation/validation.

**Contribution / 贡献:** Moves world-model emphasis toward evaluation.

**Limitations / 局限:** Official report, not independent safety proof.

**Available assets / 开放程度:** Official release; no open weights verified.

**Sources:** [S087](https://wayve.ai/press/wayve-launches-gaia3/)

## GAIA-4 (2026)

ID: `gaia4`

**Family / 分类:** closed_loop_driving_simulator

**Inputs / 输入:** recorded sensors; AI Driver actions

**Architecture / 架构:** Learned multimodal simulator; architecture incompletely disclosed.

**Action representation / 动作表示:** Ego controls; optional reactive-agent behavior

**Training objective / 训练:** World-on-rails and reactive generation training.

**Data / 数据:** Driving sensor logs; full recipe undisclosed.

**Execution and feedback / 推理闭环:** Actions alter next camera/radar inputs.

**Contribution / 贡献:** Behavioral counterfactual evaluation in a sensor loop.

**Limitations / 局限:** Simulation assumptions and fidelity bound validation.

**Available assets / 开放程度:** Official technical account; no full open reproduction verified.

**Sources:** [S088](https://wayve.ai/thinking/gaia-4/)

## Cosmos Predict2-2B (2025)

ID: `cosmos-predict2`

**Family / 分类:** video_world_model

**Inputs / 输入:** initial image; text

**Architecture / 架构:** Latent video diffusion model used as Cosmos Policy initialization.

**Action representation / 动作表示:** No robot controls in the base model.

**Training objective / 训练:** Video generative pretraining.

**Data / 数据:** Video pretraining data; complete corpus not audited.

**Execution and feedback / 推理闭环:** Generate conditional future frames.

**Contribution / 贡献:** Reusable temporal priors for subsequent policy adaptation.

**Limitations / 局限:** Base video generation is not calibrated robot control.

**Available assets / 开放程度:** Base checkpoint identified by Cosmos Policy paper and code.

**Sources:** [S083](https://arxiv.org/html/2601.16163v1), [S090](https://github.com/NVlabs/cosmos-policy)

## DeepMimic (2018)

ID: `H-M01`

**Problem / 问题:** Turn example movement into dynamically executable behavior.

**Family / 分类:** reference-motion RL

**Inputs / 输入:** Body state, phase and task goal.

**Architecture / 架构:** Motion-conditioned policy and value network.

**Action representation / 动作表示:** Joint targets tracked by motor controllers.

**Training objective / 训练:** PPO with imitation and task rewards, reference-state initialization.

**Data / 数据:** Motion-capture/keyframed clips plus simulated rollouts.

**Execution and feedback / 推理闭环:** Observe body; predict target; physics/motor feedback repeats.

**Contribution / 贡献:** Makes human motion a useful prior rather than a playback command.

**Limitations / 局限:** Original evidence is simulated animation; task coverage and transfer require additional work.

**Available assets / 开放程度:** Original code linked from project.

**Sources:** [S092](https://xbpeng.github.io/projects/DeepMimic/index.html)

## AMP / ASE (2021)

ID: `H-M02`

**Problem / 问题:** Avoid hand-crafted clip selection; reuse diverse skills.

**Family / 分类:** adversarial motion priors and latent motor skills

**Inputs / 输入:** AMP: body and task state. ASE adds latent skill z.

**Architecture / 架构:** Discriminator motion prior; ASE adds skill-conditioned policy and encoder objective.

**Action representation / 动作表示:** Joint-level motor targets; high-level ASE policy selects z.

**Training objective / 训练:** Adversarial imitation + RL; ASE additionally rewards informative skill latents.

**Data / 数据:** Unstructured motion collections and simulated interactions.

**Execution and feedback / 推理闭环:** Task or latent selection feeds reactive motor policy.

**Contribution / 贡献:** AMP learns style from distributions; ASE makes that repertoire steerable and reusable.

**Limitations / 局限:** Style realism is not task correctness; changing latent too abruptly can destabilize motion; simulated evaluation.

**Available assets / 开放程度:** Code available; motion-data licenses separate.

**Sources:** [S093](https://xbpeng.github.io/projects/AMP/index.html), [S094](https://xbpeng.github.io/projects/ASE/index.html)

## PHC (2023)

ID: `H-M03`

**Problem / 问题:** Track noisy motion indefinitely despite falls.

**Family / 分类:** scalable tracking and recovery

**Inputs / 输入:** Simulated body state and target reference motion.

**Architecture / 架构:** Progressive multiplicative control policy (PMCP) with capacity allocated to hard sequences and recovery.

**Action representation / 动作表示:** Motor targets for physically simulated humanoid.

**Training objective / 训练:** RL tracking; progressive skill learning and fail-state recovery.

**Data / 数据:** Large human motion databases, noisy reference poses and simulation.

**Execution and feedback / 推理闭环:** Track, recover from failure, resume without resetting environment.

**Contribution / 贡献:** Treats recovery as part of control rather than an external reset.

**Limitations / 局限:** Avatar result; physical actuator and sensor transfer not established by original paper.

**Available assets / 开放程度:** Official implementation available.

**Sources:** [S095](https://arxiv.org/abs/2305.06456), [S096](https://github.com/ZhengyiLuo/PHC)

## Humanoid Transformer (2023)

ID: `H-M04`

**Problem / 问题:** Adapt locomotion to uncertain dynamics without explicit online system identification.

**Family / 分类:** history-conditioned locomotion RL

**Inputs / 输入:** Causal history of proprioceptive observations/actions and walking commands.

**Architecture / 架构:** Autoregressive causal transformer controller.

**Action representation / 动作表示:** Future motor actions / desired joint commands.

**Training objective / 训练:** Large-scale model-free RL in randomized simulation.

**Data / 数据:** Simulation across terrain/dynamics; real-robot evaluation.

**Execution and feedback / 推理闭环:** Rolling history alters behavior without weight updates.

**Contribution / 贡献:** Uses temporal context for implicit dynamics adaptation.

**Limitations / 局限:** Does not solve semantic planning, object manipulation or arbitrarily strong disturbances.

**Available assets / 开放程度:** Paper/project available; complete release scope not verified.

**Sources:** [S097](https://humanoid-transformer.github.io/)

## H2O / OmniH2O (2024)

ID: `H-M05`

**Problem / 问题:** Bridge human motion, robot feasibility and multiple command sources.

**Family / 分类:** sim-to-real teleoperation and control interface

**Inputs / 输入:** Human pose from RGB/VR, sparse motion goals, robot proprioception.

**Architecture / 架构:** H2O privileged feasibility filter; OmniH2O privileged RL teacher distilled to deployable student.

**Action representation / 动作表示:** Kinematic pose goals into whole-body tracking motor actions.

**Training objective / 训练:** Retargeting, feasibility filtering, RL/domain randomization; student supervised distillation.

**Data / 数据:** Human motion corpus; OmniH2O-6 robot demonstrations for learned upper-layer skills.

**Execution and feedback / 推理闭环:** Human or autonomous policy produces pose targets; student stabilizes robot continuously.

**Contribution / 贡献:** Universal pose interface separates goal generation from physical execution.

**Limitations / 局限:** Teleoperation is not autonomous task competence; sparse goals and retargeting lose information.

**Available assets / 开放程度:** Project links code and OmniH2O data.

**Sources:** [S098](https://human2humanoid.com/), [S099](https://omni.human2humanoid.com/)

## HumanPlus (2024)

ID: `H-M06`

**Problem / 问题:** Collect useful humanoid task demonstrations without bespoke full-body controllers per task.

**Family / 分类:** human-data to autonomous whole-body skills

**Inputs / 输入:** Low level: body/hand reference and state. High level: egocentric vision.

**Architecture / 架构:** RL shadowing controller plus supervised visual skill policy.

**Action representation / 动作表示:** Whole-body and hand targets for a 33-DoF humanoid.

**Training objective / 训练:** Human-motion RL pretraining; shadowing collects robot data; behavior cloning learns autonomy.

**Data / 数据:** 40-hour human-motion data; up to 40 task demonstrations in reported experiments.

**Execution and feedback / 推理闭环:** Visual policy proposes commands; low-level controller executes with body feedback.

**Contribution / 贡献:** Closes the data-collection loop from humans to real robot learning.

**Limitations / 局限:** Limited task/robot distribution; human imitation cannot directly infer all contact dynamics.

**Available assets / 开放程度:** Code, datasets and hardware references linked.

**Sources:** [S100](https://humanoid-ai.github.io/)

## MaskedMimic (2024)

ID: `H-M07`

**Problem / 问题:** Generate physically feasible whole-body motion from incomplete instructions.

**Family / 分类:** partial-motion-conditioned generative control

**Inputs / 输入:** Partial future joints, trajectory, scene and/or text conditions.

**Architecture / 架构:** Fully constrained tracking teacher; conditional-VAE partial-goal policy via motion inpainting.

**Action representation / 动作表示:** Physical-controller actions conditioned on sampled latent motion.

**Training objective / 训练:** RL tracking followed by learning a partially constrained policy with randomized masks.

**Data / 数据:** Motion data and simulated physical interaction.

**Execution and feedback / 推理闭环:** Infer missing movement consistent with constraints, act, observe and repeat.

**Contribution / 贡献:** Unifies control modalities by representing them as missing motion information.

**Limitations / 局限:** Mostly simulated character evidence; ambiguous constraints and real hardware transfer remain gaps.

**Available assets / 开放程度:** Official NVIDIA project links code.

**Sources:** [S101](https://arxiv.org/html/2409.14393v1)

## SONIC / GEAR-SONIC (2025)

ID: `H-M08`

**Problem / 问题:** Convert many motion interfaces into reusable robust whole-body execution.

**Family / 分类:** scalable behavioral foundation controller

**Inputs / 输入:** Proprioception plus robot, human or hybrid reference motion.

**Architecture / 架构:** Specialized encoders -> FSQ universal token -> shared control decoder; auxiliary motion decoder.

**Action representation / 动作表示:** Desired joint positions -> PD controllers; released policy runs at 50 Hz.

**Training objective / 训练:** PPO tracking + reconstruction; domain randomization; runtime kinematic planner.

**Data / 数据:** Original paper: 700-hour motion collection; current release also offers separate public data.

**Execution and feedback / 推理闭环:** VLA/VR/planner produces motion command; token policy and PD loop execute.

**Contribution / 贡献:** Explicit bridge between VLA semantic actions and low-level motor control; released variants improve deployment.

**Limitations / 局限:** One-task VLA PoC is not broad autonomy; lookahead differs from latency; proprietary original corpus; preprint compute inconsistency omitted.

**Available assets / 开放程度:** Training/deployment code and checkpoints released; code/weights have different licenses.

**Sources:** [S102](https://arxiv.org/html/2511.07820v1), [S103](https://github.com/NVlabs/GR00T-WholeBodyControl), [S123](https://research.nvidia.com/labs/dair/publication/sonic2026/)

## ViNT (2023)

ID: `H-M09`

**Problem / 问题:** Transfer navigation experience across mobile robots and goals.

**Family / 分类:** visual navigation foundation policy

**Inputs / 输入:** Recent RGB observations and visual goal token.

**Architecture / 架构:** Visual encoders and transformer; replaceable goal representation.

**Action representation / 动作表示:** Normalized local waypoint trajectory and distance-to-goal estimate.

**Training objective / 训练:** Goal-reaching supervised learning on diverse trajectories.

**Data / 数据:** Hundreds of hours from multiple navigation platforms.

**Execution and feedback / 推理闭环:** Topological/global planner selects subgoal; local policy proposes waypoints; robot controller follows.

**Contribution / 贡献:** Reusable navigation affordances and adaptable task tokens.

**Limitations / 局限:** Long range depends on planner and mapping; not a semantic manipulator or balance controller.

**Available assets / 开放程度:** Official code/checkpoints and deployment examples.

**Sources:** [S104](https://arxiv.org/abs/2306.14846), [S105](https://github.com/robodhruv/visualnav-transformer)

## NoMaD (2023)

ID: `H-M10`

**Problem / 问题:** Use one policy for exploration and goal-reaching without averaging incompatible paths.

**Family / 分类:** goal-masked diffusion navigation

**Inputs / 输入:** RGB history and optionally masked goal image.

**Architecture / 架构:** ViNT context encoder conditions diffusion action decoder.

**Action representation / 动作表示:** Distribution over local waypoint/action sequences.

**Training objective / 训练:** Diffusion behavior learning with goal masking.

**Data / 数据:** Multi-robot navigation trajectories.

**Execution and feedback / 推理闭环:** Sample feasible-looking candidate path; execute segment; update observations and topological planner.

**Contribution / 贡献:** Represents alternative routes with a common exploration/navigation model.

**Limitations / 局限:** Sampling latency and planner integration matter; no formal collision guarantee.

**Available assets / 开放程度:** Official code/checkpoints shared with ViNT.

**Sources:** [S106](https://general-navigation-models.github.io/nomad/), [S105](https://github.com/robodhruv/visualnav-transformer)

## GOAT (2023)

ID: `H-M11`

**Problem / 问题:** Find a particular object by class, picture or description over repeated missions.

**Family / 分类:** modular lifelong semantic navigation

**Inputs / 输入:** RGB-D/state and multimodal goal; persistent object memory.

**Architecture / 架构:** Perception, instance-aware semantic mapping, matching and navigation planner.

**Action representation / 动作表示:** Goal locations and navigation commands through a robot-specific controller.

**Training objective / 训练:** Pretrained perception modules; map/instance accumulation during deployment.

**Data / 数据:** Real indoor environments; evaluated in nine homes.

**Execution and feedback / 推理闭环:** Update memory -> match known goal or explore -> navigate -> retain evidence.

**Contribution / 贡献:** Improvement comes from remembered environment state without retraining a universal action model.

**Limitations / 局限:** Mapping/perception errors persist; system-level benchmark differs from end-to-end VLA tests.

**Available assets / 开放程度:** Paper/system project; GOAT-Bench has separate code/data.

**Sources:** [S107](https://arxiv.org/html/2311.06430v1), [S108](https://arxiv.org/abs/2404.06609)

## Helix / Helix 02 (2025)

ID: `H-M12`

**Problem / 问题:** Unify semantic manipulation with dexterity, balance and locomotion.

**Family / 分类:** hierarchical humanoid VLA

**Inputs / 输入:** Language, head/palm cameras, touch and full-body proprioception in Helix 02.

**Architecture / 架构:** S2 semantic latents -> S1 transformer joint targets at 200 Hz -> S0 10M controller at 1 kHz.

**Action representation / 动作表示:** Joint targets followed by joint-level actuator commands.

**Training objective / 训练:** Helix learned visuomotor control; Helix 02 S0 uses randomized simulation RL and human motion tracking.

**Data / 数据:** S0: over 1,000 hours retargeted motion; complete S1/S2 corpus undisclosed.

**Execution and feedback / 推理闭环:** Multi-rate hierarchy preserves fast balance feedback while slow semantics updates goals.

**Contribution / 贡献:** Extends upper-body Helix to demonstrated full-body room-scale tasks.

**Limitations / 局限:** Vendor demonstration; failure/intervention distribution, full training recipe and independent evaluation unavailable.

**Available assets / 开放程度:** Proprietary model; public technical descriptions.

**Sources:** [S109](https://www.figure.ai/news/helix), [S110](https://www.figure.ai/news/helix-02)

## Skild Brain / S1 (2025)

ID: `H-M13`

**Problem / 问题:** Reduce per-robot and per-task reprogramming.

**Family / 分类:** cross-embodiment and demonstration-conditioned policy

**Inputs / 输入:** Body/sensor context; S1 accepts a demonstration video with live observations.

**Architecture / 架构:** Shared cross-embodiment model; precise layer structure/action decoder undisclosed.

**Action representation / 动作表示:** Robot actions; exact shared action parameterization undisclosed.

**Training objective / 训练:** Cross-embodiment training; S1 episodic demonstration-conditioned pretraining.

**Data / 数据:** Simulation and diverse physical data; complete data mixture not disclosed.

**Execution and feedback / 推理闭环:** Condition execution on example and ongoing context; new task need not update weights in reported ICL setting.

**Contribution / 贡献:** Task specification shifts toward demonstration and reusable physical knowledge.

**Limitations / 局限:** Manufacturer evidence; unpublished architecture/weights and nonpublic splits prevent complete reproduction.

**Available assets / 开放程度:** Closed; commercial/partner access.

**Sources:** [S111](https://www.skild.ai/blogs/omni-bodied), [S112](https://www.skild.ai/blogs/s1), [S113](https://www.skild.ai/blogs/skild-crosses-100m-arr)

## GO-1 / GO-1 Air (2025)

ID: `go1`

**Family / 分类:** Latent-action VLA

**Inputs / 输入:** Multi-view images, instruction, proprioception

**Architecture / 架构:** VLM plus latent-action planner plus diffusion action expert; Air removes planner

**Action representation / 动作表示:** Discrete latent plan; continuous action chunks

**Training objective / 训练:** Latent action reconstruction/prediction followed by robot action denoising

**Data / 数据:** Human video, cross-embodiment robot data and AgiBot World

**Execution and feedback / 推理闭环:** Predict latent plan then denoise action chunk and execute with feedback

**Contribution / 贡献:** Separates transfer of video motion knowledge from embodiment-specific continuous execution

**Limitations / 局限:** Latent plan quality, embodiment alignment, data concentration and task-limited results

**Available assets / 开放程度:** Code and listed checkpoints/dataset releases; exact training reproducibility must be audited

**Sources:** [S132](https://github.com/OpenDriveLab/Agibot-World), [S133](https://agibot-world.com/blog/agibot_go1.pdf)

## SERL (2024)

ID: `serl`

**Family / 分类:** Real-world reinforcement learning

**Inputs / 输入:** Visual observation, robot state and reward

**Architecture / 架构:** Off-policy actor-critic training and robot learning infrastructure

**Action representation / 动作表示:** Continuous task-specific control

**Training objective / 训练:** Sample-efficient real-world RL with prior demonstrations or experience

**Data / 数据:** On-robot interaction and optional demonstrations

**Execution and feedback / 推理闭环:** Learned actor executes within the robot control stack

**Contribution / 贡献:** Operationalizes efficient online policy improvement

**Limitations / 局限:** Reward/reset design and interaction burden; not one universal pretrained model

**Available assets / 开放程度:** Research software suite

**Sources:** [S143](https://arxiv.org/abs/2401.16013)

## HIL-SERL (2024)

ID: `hil-serl`

**Family / 分类:** Human-in-the-loop reinforcement learning

**Inputs / 输入:** Images, state, learned success reward and human corrections

**Architecture / 架构:** Reward classifier, demonstration/replay buffers, actor-learner loop

**Action representation / 动作表示:** Continuous control through task-specific robot interface

**Training objective / 训练:** Reward learning from positives/negatives, demonstrations and online off-policy RL with interventions

**Data / 数据:** Task-specific demonstrations, success labels and online interventions

**Execution and feedback / 推理闭环:** Actor controls robot; human corrections become experience

**Contribution / 贡献:** Uses failure recovery and feedback beyond pure imitation

**Limitations / 局限:** Human/reset cost, reward misspecification, narrow task protocols

**Available assets / 开放程度:** Code and workflows available; hardware-specific integration required

**Sources:** [S142](https://hil-serl.github.io/), [S153](https://huggingface.co/docs/lerobot/hilserl)

## MolmoAct2 (2026)

ID: `molmoact2`

**Family / 分类:** Action-reasoning VLA

**Inputs / 输入:** Images, language, state

**Architecture / 架构:** Molmo2-ER embodied reasoning backbone plus continuous flow-matching action expert

**Action representation / 动作表示:** Continuous action chunks

**Training objective / 训练:** Molmo2-ER backbone -> discrete autoregressive MolmoAct2-Pretrain -> flow-matching action expert; MolmoAct2-Think is a separate depth-token-reasoning variant.

**Data / 数据:** Released reasoning and robot training datasets, with embodiment-specific adaptation

**Execution and feedback / 推理闭环:** Closed-loop manipulation using conditioned action expert

**Contribution / 贡献:** Combines open embodied reasoning assets with continuous robot action learning

**Limitations / 局限:** Reasoning metrics alone do not establish contact reliability; base checkpoints are not universal deployment policies

**Available assets / 开放程度:** Official code, models, staged checkpoints and dataset links

**Sources:** [S144](https://github.com/allenai/molmoact2), [S145](https://arxiv.org/abs/2605.02881)

## Xiaomi-Robotics-0 (2026)

ID: `xiaomi-robotics-0`

**Family / 分类:** Asynchronous VLA

**Inputs / 输入:** Multi-view images, instruction and proprioception

**Architecture / 架构:** Qwen3-VL-4B-Instruct VLM plus diffusion transformer; 4.7B total per official page

**Action representation / 动作表示:** 30-step continuous action chunks

**Training objective / 训练:** Choice-policy VLM training; freeze VLM and train flow expert; prefix-conditioned post-training

**Data / 数据:** Robot and vision-language mixtures plus task-specific teleoperation

**Execution and feedback / 推理闭环:** Buffered asynchronous chunks with committed prefix alignment

**Contribution / 贡献:** Treats deployment scheduling and action responsiveness as training-design issues

**Limitations / 局限:** Requires matching async checkpoint, valid normalization, hardware adaptation and task data

**Available assets / 开放程度:** Code, weights and full post-training pipeline announced April 2026

**Sources:** [S151](https://robotics.xiaomi.com/xiaomi-robotics-0.html), [S152](https://github.com/XiaomiRobotics/Xiaomi-Robotics-0/blob/main/xr0/README.md)

