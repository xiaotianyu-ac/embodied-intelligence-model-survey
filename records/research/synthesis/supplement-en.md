## Additional decompositions: data, feedback, and execution

### GO-1: a latent plan between semantics and continuous action

GO-1 consumes multiple camera views, instructions, and robot state. Its ViLLA architecture combines a vision-language backbone, a latent-action planner, and a diffusion action expert. Discrete latent actions are learned from sources including human video; a planner predicts them from the current context, and the action expert conditions on this representation to generate continuous chunks. Latent-action prediction and robot action denoising have distinct objectives. GO-1 Air removes the planner, providing a public entry point for investigating whether the intermediate planning layer is useful.[R005][R006]

This is a combination of semantic transfer, latent-motion transfer, and continuous control, rather than the inevitable successor to every VLA. Latent actions can use video without robot-command labels but still need grounding into executable commands through robot data. When architecture and data scale change together, gains cannot be attributed solely to the planner; matching task, data, and compute while comparing GO-1 with Air is more informative. AgiBot World's collection-robot count describes hardware instances, not the same number of distinct embodiments.[R005][R006]

### SERL and HIL-SERL: learning from corrective experience

SERL integrates training, experience, and robot interfaces for sample-efficient visual reinforcement learning; it is not one pretrained weight set covering all tasks. HIL-SERL introduces a concrete feedback workflow within this line: collect positive and negative states for a reward classifier, initialize a demonstration buffer, execute online, intervene when needed, and use the resulting experience in actor-critic learning. The learning signal includes visual observations, state, sparse success signals, and human corrections.[R015][R016][R026]

Relative to imitation, the additional information concerns recovery after deviations and whether actions actually succeed. Relative to generalist VLAs, the method is closer to precise post-training on a bounded task. Reported learning speed and high success cannot be separated from reward labels, interventions, resets, and hardware. Engineering comparisons should include cumulative human minutes, reset count, and usable interaction per hour, rather than gradient-update time alone.[R015][R026]

### MolmoAct2: an open embodied-reasoning backbone with continuous control

MolmoAct2 builds on the Molmo2-ER embodied-reasoning vision-language backbone and adds robot state and a flow-matching continuous action expert. Images, language, and state condition action chunks for closed-loop manipulation. Public assets include intermediate foundation checkpoints, selected robot-adapted policies, and relevant datasets, enabling analysis of how action generation uses reasoning representations. Producing explanatory text is insufficient by itself: the action module must still learn an appropriate command distribution from robot trajectories.[R017][R018]

The released checkpoints make the training path more explicit. Molmo2-ER is the starting vision-language backbone; MolmoAct2-Pretrain is a discrete autoregressive VLA before the continuous action expert is attached; the final MolmoAct2 connects a flow-matching expert. MolmoAct2-Think adds depth-token reasoning and should be identified as a separate variant, rather than attributing that mechanism to every deployed MolmoAct2 policy. This separates two research questions: how discrete action pretraining shapes the backbone, and whether depth reasoning improves continuous control. Their contributions still require ablations with a fixed robot, data mixture, and inference budget; releasing intermediate checkpoints does not by itself establish causal attribution.[R017][R018]

Its relationship to GR00T, PI, and Xiaomi concerns a modular division between visual-language understanding and continuous generation, not shared weights. Backbones, training mixtures, alignment objectives, and deployment protocols differ. Staged checkpoints facilitate ablations, while improvements in contact, unfamiliar objects, or long-horizon recovery require matched evaluation. Foundation checkpoints and embodiment-adapted deployment policies should be treated as different assets.[R017]

### Xiaomi-Robotics-0: training for the execution schedule

Xiaomi-Robotics-0 combines Qwen3-VL-4B-Instruct with an action DiT, totaling 4.7B parameters according to the official project. A first stage develops action-relevant VLM features using Choice Policies and mixed vision-language data. A second freezes the VLM and trains a flow-matching expert conditioned on its KV states and proprioception. Post-training introduces action prefixes and attention/loss design so that new chunks agree with committed actions while remaining responsive to observations.[R024]

The public deployment implementation returns 30-step chunks. Asynchronous execution predicts the next chunk while current actions run and removes actions that have expired during inference. This mode requires a correspondingly trained checkpoint; attaching any synchronous policy to an asynchronous queue is not equivalent. The broader lesson is that **latency compensation changes training conditions and distributions**, rather than being an isolated runtime patch. Strong reported real-task performance also uses substantial specialized data, so task proficiency, few-shot adaptation, and zero-shot generalization remain distinct claims.[R024][R025]

### 1XWM: grounding generated video into action

1XWM generates a future from a prompt and starting frame, then uses inverse dynamics to extract NEO commands. The January 2026 disclosure describes a 14B video backbone adapted with egocentric human and robot data, and a Depth Anything encoder with a flow-matching head for the inverse model. Video priors therefore still require an action-grounding interface.[H028]

That version needs approximately 11 seconds of multi-GPU inference for five seconds of video plus one second to extract actions; longer-horizon closed-loop replanning remains future work. This separates the demonstration from reactive, on-device, sustained household autonomy. These limitations apply to the disclosed version, without assumptions about unpublished improvements.[H028]
