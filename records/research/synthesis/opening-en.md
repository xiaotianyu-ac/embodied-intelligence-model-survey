# Embodied Intelligence Models: Progress, Mechanisms, and Relationships

## Scope and central findings

Progress in embodied intelligence connects semantic knowledge learned from internet data, action experience learned from physical interaction, and dynamics learned in simulation within a perception-action feedback loop. Parameter count and humanoid appearance alone miss decisive factors: data distributions, action interfaces, execution latency, and low-level control. This review focuses on robotic manipulation, navigation, and whole-body control, with driving world models as an adjacent reference. It does not attempt to survey all autonomous-driving perception, SLAM, or classical control.

Evidence was checked through **September 11, 2026**. The methodology is a technical scoping review: foundational work, original papers, author projects, official code, and product documentation are followed along research lines and updated with verified 2026 releases. This is not an exhaustive database-based systematic review with a measured retrieval recall, and no robot experiments were reproduced. Completeness refers to coverage of mechanisms, relationships, data, evaluation, engineering, products, and open problems within this scope. Paper results, vendor claims, and analytical judgments are distinguished; undisclosed architecture or training data are not inferred.

Five findings organize the report. First, **embodied intelligence is broader than a single VLA model**: representation, planning, action generation, prediction, and servo control are composable roles. Second, action generation increasingly uses chunks, diffusion, and flow matching, accompanied by asynchronous execution; these are design dimensions rather than one mandatory replacement chain. Third, world models need evidence of useful consequences, planning, or data generation; visual realism alone does not establish robot capability. Fourth, cross-embodiment data, domain adaptation, and feedback learning connect pretraining with deployment, while standardized file formats do not eliminate dynamics differences. Fifth, sustained reliability, contact feedback, and fair evaluation remain major gaps between demonstrations and operation. The model evidence and experimental conditions below support these findings.

## A common decomposition and the technical foundations

### Locate the model within the feedback loop

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
