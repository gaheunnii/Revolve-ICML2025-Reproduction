# PromptTune: A Prompt Optimization Framework Inspired by REVOLVE and TextGrad

## Overview

PromptTune is a prompt optimization framework built to reproduce and operationalize the core idea of **REVOLVE (Response Evolution in Textual Optimization)** for LLM-based systems. Instead of optimizing model parameters, the framework focuses on optimizing **textual variables** such as prompts, intermediate responses, and task outputs through iterative feedback. In the current implementation, the project mainly targets **instance-level prompt optimization for mathematical reasoning tasks** and provides a unified experimental environment for comparing multiple optimization strategies. 

The main motivation comes from a limitation of first-order textual optimization methods such as TextGrad: they rely primarily on immediate feedback from the current iteration, which can lead to small updates, unstable search directions, or stagnation in local optima on complex tasks. REVOLVE extends this idea by explicitly tracking **how responses evolve across iterations**, allowing optimization to use not only current feedback but also the trajectory of response changes over time. The original paper evaluates this idea on prompt optimization, solution optimization, and code optimization, and reports stronger performance and fewer iterations to converge than competitive baselines. 

This reproduction project translates that idea into a runnable framework named **PromptTune**, with support for local LLM deployment through **Ollama** and multiple optimizer variants under a unified pipeline. 

---

## Project Goals

This project was developed with three goals:

1. **Reproduce the core optimization idea of REVOLVE** and distinguish it from first-order textual optimization.
2. **Build a runnable prompt optimization framework** that supports controlled comparison across different optimizers.
3. **Provide a local, reusable experimental environment** using Ollama instead of relying only on cloud APIs.

---

## Key Idea

### From TextGrad to REVOLVE

TextGrad treats natural-language feedback as a form of **textual gradient**. An evaluator model reviews the current output and produces feedback, which is then used to update the prompt or response for the next iteration. This makes optimization possible without modifying the LLM itself.

REVOLVE extends this process by asking an additional question:

> Not only "What is wrong with the current response?" but also "Compared with the previous iteration, is the response actually evolving in a better direction?"

Instead of relying only on current-step feedback, REVOLVE incorporates the **evolution of responses across iterations**. In the paper, this is presented as an analogy to **second-order optimization effects**: although it does not compute a numerical Hessian, it uses response dynamics over time to produce smoother, more informed updates and to reduce oscillation or stagnation. 

---

## Framework Design

PromptTune organizes the reproduction into a unified experimental framework with three optimizer variants:

| Optimizer | Description |
|---|---|
| `v1` | Basic first-order textual optimization based on current-round feedback |
| `v1_momentum` | A momentum-enhanced version designed to reduce repeated-feedback stagnation and speed up early search |
| `v2` | The REVOLVE-style optimizer that explicitly tracks response evolution across iterations for more robust updates |

All three variants run under the same task setup, evaluation pipeline, and experimental interface, enabling direct comparison in terms of convergence behavior, performance gain, and stability. 

---

## Current Reproduction Scope

The original REVOLVE paper evaluates three categories of textual optimization tasks:

- **Prompt Optimization**
- **Solution Optimization**
- **Code Optimization** 

In this reproduction, the current focus is on **prompt optimization**, especially **instance-level prompt optimization for mathematical reasoning**. This scope is consistent with the available implementation and makes it easier to clearly observe the behavioral differences among the three optimizer variants during iterative optimization. 

---

## Optimization Workflow

The prompt optimization process follows a unified iterative loop:

1. Start from an initial prompt.
2. Feed the prompt to the target model and generate an answer.
3. Use an evaluation module to generate natural-language feedback based on task performance.
4. Update the prompt with an optimizer that considers current feedback, and for `v2`, also response evolution across iterations.
5. Repeat the process until performance stabilizes or the maximum number of iterations is reached. 

In practice, a simple initial prompt can gradually evolve into a more structured task template containing:

- behavioral constraints,
- reasoning strategy instructions,
- output formatting requirements,
- exception-handling rules.
This highlights an important point: the value of REVOLVE-style optimization is not just rewriting wording locally, but **discovering a more effective prompt structure for the target task through iterative evolution**. 

---

## Experimental Results

The main validation setting in this reproduction is the **GSM8K_DSPy** mathematical reasoning task with **200 samples**. Under this setup, the three optimizer variants produced the following results:

| Optimizer | Round 1 (Initial) | Round 2 | Round 3 | Round 4 |
|---|---:|---:|---:|---:|
| `v1` | 95.0% (190/200) | 95.5% (191/200) | 95.0% (190/200) | 95.0% (190/200) |
| `v1_momentum` | 95.0% (190/200) | 96.0% (192/200) | 92.5% (185/200) | 94.0% (188/200) |
| `v2` | 95.0% (190/200) | 96.5% (193/200) | 95.0% (190/200) | 95.5% (191/200) | 

### Result Interpretation

- **`v1`** is the most stable baseline. Its accuracy remains around 95%, but later iterations bring only limited improvement. 
- **`v1_momentum`** improves faster in the early stage and reaches 96.0% in Round 2, suggesting that momentum helps accelerate search. However, later drops indicate update instability. 
- **`v2`** achieves the best peak result at 96.5% in Round 2 and remains relatively stable afterward, showing a better balance between optimization strength and stability. 

Overall, the reproduction supports the same intuition emphasized by REVOLVE: compared with first-order updates that only use immediate feedback, response-evolution-aware optimization can provide a smoother and more effective search path on complex reasoning tasks. 

---

## Local LLM Deployment with Ollama

A major engineering contribution of this project is the transition from API-oriented experimentation to a **local Ollama-based workflow**. In this setup, locally deployed models are used for both:

- generating optimization feedback
- performing downstream reasoning

Compared with cloud-only pipelines, this design offers several practical advantages:

- **Lower long-term experiment cost** for multi-round and batch optimization;
- **Better privacy and control**, since task data and optimization traces remain local;
- **Better extensibility**, making it easier to replace models and compare different local LLM configurations. 

---

## Features

- Unified framework for comparing multiple textual optimization strategies
- Support for `v1`, `v1_momentum`, and `v2` optimizer variants
- Instance-level prompt optimization for reasoning tasks
- Integration with **Ollama** for local LLM execution
- Multi-threaded execution support for batch experiments 

---

## Repository Structure

```text
prompttune/
├── evaluation/                # Evaluation modules
│   ├── instancep_opt.py       # Instance-level prompt optimization
│   └── gsm8k_dspy.py          # GSM8K task pipeline
├── textgrad/                  # TextGrad-related components
├── dsp/                       # DSPy integration
├── results/                   # Optimization outputs
├── logs/                      # Runtime logs
├── run.sh                     # Example run script
└── requirements.txt           # Dependencies
```

Repository structure adapted from the provided project markdown. 

---

## Installation

### Requirements

- Python 3.10+
- Ollama
- Dependencies listed in `requirements.txt` 

### Setup

```bash
git clone <repository-url>
cd prompttune
pip install -r requirements.txt
```

### Pull a Local Model with Ollama

```bash
ollama pull gpt-oss:120b
```

Then specify the local model in the command line:

```bash
--backbone_engine ollama-gpt-oss:120b --model ollama-gpt-oss:120b
```

These commands are based on the provided project markdown.

---

## Usage

### Run `v1_momentum`

```bash
python -m evaluation.instancep_opt \
  --task GSM8K_DSPy \
  --backbone_engine ollama-gpt-oss:120b \
  --model ollama-gpt-oss:120b \
  --optimizer_version v1_momentum \
  --num_threads 1
```

### Run `v1`

```bash
python -m evaluation.instancep_opt \
  --task GSM8K_DSPy \
  --backbone_engine ollama-gpt-oss:120b \
  --model ollama-gpt-oss:120b \
  --optimizer_version v1 \
  --num_threads 1
```

### Run `v2` (REVOLVE-style)

```bash
python -m evaluation.instancep_opt \
  --task GSM8K_DSPy \
  --backbone_engine ollama-gpt-oss:120b \
  --model ollama-gpt-oss:120b \
  --optimizer_version v2 \
  --num_threads 1
```

Or run the shell script directly:

```bash
chmod +x run.sh
./run.sh
```

Commands adapted from the uploaded markdown reference. 

---

## Output Files

Optimization results are stored in the `results/` directory. Each result file records:

- task information,
- model information,
- optimizer version,
- number of optimized samples,
- per-sample optimization traces and evaluation results.

Example:

```text
instance_prompt_optimization_GSM8K_DSPy_ollama-gpt-oss:120b_v1_momentum_samples200.json
```

---

## Reproduction Significance

This project is not only a conceptual summary of REVOLVE, but a concrete engineering reproduction that:

- reconstructs the core experimental logic of the paper,
- validates the benefit of response-evolution-aware optimization in a reasoning task,
- and provides a reusable local framework for future work on automatic prompt engineering, test-time optimization, and local LLM system optimization. 

---

## References

Peiyan Zhang, Haibo Jin, Leyang Hu, Xinnuo Li, Liying Kang, Man Luo, Yangqiu Song, and Haohan Wang. **REVOLVE: Optimizing AI Systems by Tracking Response Evolution in Textual Optimization**. arXiv, 2025. 