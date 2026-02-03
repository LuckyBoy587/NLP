# AI Agent Workflow Instructions

## Overview
This repository uses an AI agent that operates in exactly one of two modes based on the task: **Python Script Mode (.py)** or **Jupyter Notebook Mode (.ipynb)**.

### Key Rules
- **Tool-Driven Execution:** Browser automation, compilation, and result extraction are handled exclusively by MCP tools.
- **No Manual Simulation:** The agent must never attempt to replicate browser behavior manually.
- **Mode Selection:** Select exactly one mode per question and follow the corresponding instruction file.

---

## 🚦 PHASE 1: Discovery & Mode Selection
Determine the required output type before taking action.

### 🐍 Python Script Mode (.py)
*Select if:*
- The platform provides an Ace Editor.
- The task expects printed output.
- The task mentions `.py`, code execution, compilation, or checking.
- There exists sample input and expected output.
*Instruction:* Activate and follow the **python-mode** skill in [.gemini/skills/python-mode/SKILL.md](.gemini/skills/python-mode/SKILL.md) for detailed workflow.

### 📓 Jupyter Notebook Mode (.ipynb)
*Select if:*
- The task includes plot images.
- The task requires visual output.
- The dataset is provided via a ZIP download.
- The output is explicitly or implicitly a notebook.
*Instruction:* Activate and follow the **jupyter-mode** skill in [.gemini/skills/jupyter-mode/SKILL.md](.gemini/skills/jupyter-mode/SKILL.md) for detailed workflow.

---

