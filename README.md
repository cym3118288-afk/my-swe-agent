# Terry-Carson-swe-agent
Terry chen's  SWE Agent powered by GitHub Copilot Pro


**A Minimal, Ready-to-Run SWE Agent** — Designed specifically for **GitHub Copilot Pro** users （especially for students who get education ceritification LOL).

Powered by your Copilot Pro subscription, this agent acts like a real software engineer: it automatically clones repositories, explores code, fixes GitHub Issues, and generates a ready-to-apply patch.



![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Powered by](https://img.shields.io/badge/Powered%20by-GitHub%20Copilot%20Pro-181717?logo=github)

---

## ✨ Features

- Zero-config Copilot Pro support via LiteLLM (uses gpt-4o, Claude, etc. with your existing Copilot Pro quota)
- Fully autonomous Issue fixing: runs `ls`, `cat`, `grep`, `sed -i`, tests, and more until the bug is fixed
- Clean output: automatically creates `final_patch.diff` that you can apply with `git apply`
- Safe by design: every task runs in a temporary folder that is deleted when finished
- Perfect Windows support (PowerShell + CMD optimized)
- Extremely simple code: only ~150 lines, easy to read, modify, and learn from

---

## 🚀 Quick Start

### 1. Clone this repository
```powershell
git clone https://github.com/YOUR-USERNAME/my-swe-agent.git
cd my-swe-agent
```

### 2. Create and activate a virtual environment (recommended)

```python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

# Windows CMD
.venv\Scripts\activate.bat

# macOS / Linux
source .venv/bin/activate
```

###3. Install dependencies
```
pip install -r requirements.txt
```

###4. Run the agent (first run will open browser for authorization)
```
python swe_agent.py https://github.com/pallets/flask.git "Fix a simple bug: when input is empty, the homepage should show a welcome message instead of throwing an error"
```

## 🛠️ How It Works
#### 1.  Clones the target repository into a temporary folder
#### 2.  Feeds the Issue description to the Copilot Pro model
#### 3.  Runs a ReAct-style loop:
	•  Thought: thinks about the next step
	•  Command: outputs exactly one bash command
#### 4.  Executes the command and feeds the output back to the model
#### 5.  Repeats until the model decides the fix is complete, then generates the final patch
The entire process is fully autonomous — just like having a junior software engineer working for you.


## 🤝 Welcome Friends from All Over the World to Contribute and Use!
#### No matter which country you are from or what language you speak, you are warmly welcome!
#### •  Star this repository — it gives us the biggest motivation
#### •  Fork and submit Pull Requests (improve prompts, add Docker support, local Ollama, multi-agent mode, auto-create PRs, etc.)
#### •  Open Issues if you encounter any problems (Windows, authentication, specific models, etc.)
#### •  Use Discussions to share real cases where you successfully fixed Issues with this agent

## We look forward to your arrival .Let’s build the future more like the future together! 

