"# swe_agent.py" 

import os
import subprocess
import tempfile
import shutil
import re
import sys
from pathlib import Path
from litellm import completion

class MySweAgent:
    def __init__(self, model: str = "github_copilot/gpt-4o"):
        self.model = model
        self.messages = []
        self.work_dir: str | None = None
        self.max_steps = 50

    def setup(self, repo_url: str, issue_desc: str):
        """1. 克隆仓库到临时目录"""
        self.work_dir = tempfile.mkdtemp(prefix="swe-agent-")
        print(f"🚀 仓库克隆到临时目录: {self.work_dir}")
        
        try:
            subprocess.run(["git", "clone", "--depth", "1", repo_url, self.work_dir], 
                         check=True, capture_output=True, text=True)
            os.chdir(self.work_dir)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"克隆失败: {e.stderr}")

        # 系统 Prompt（严格要求格式，让 LLM 更容易遵守）
        system_prompt = """你是一个专业的软件工程师，正在修复 GitHub Issue。
规则：
1. 每次只输出一个 bash 命令（不要解释，不要多余文字）。
2. 严格使用以下格式输出：
Thought: <你的思考>
Command: <单个 bash 命令>

示例：
Thought: 我需要先看看项目结构
Command: ls -la

3. 探索代码用 ls, cat, grep, find
4. 编辑代码用 sed -i 's/old/new/g' file.py 或 echo 'new code' > file.py
5. 运行测试用 python -m pytest 或 python test.py
6. 修复完后执行 git diff > patch.diff 并输出 Command: echo "SUBMIT"
7. 永远不要执行 rm -rf / 或危险命令，只在当前目录操作。"""

        self.messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"""Issue 描述：
{issue_desc}

当前工作目录是 {self.work_dir}，请开始修复！"""}
        ]

    def _extract_command(self, content: str) -> str:
        """智能提取 Command（支持各种 LLM 输出格式）"""
        match = re.search(r'Command:\s*(.+?)(?:\n\n|$)', content, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()
        # 如果没找到，尝试整段作为命令（兜底）
        lines = content.split('\n')
        for line in lines:
            if line.strip().startswith(('ls', 'cat', 'grep', 'find', 'git', 'python', 'sed', 'echo', 'pytest')):
                return line.strip()
        return content.strip()

    def run_command(self, cmd: str) -> str:
        """安全执行 bash 命令"""
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                cwd=self.work_dir,
                capture_output=True,
                text=True,
                timeout=60
            )
            output = (result.stdout + result.stderr).strip()
            return output if output else "✅ 命令执行成功，无输出。"
        except subprocess.TimeoutExpired:
            return "⏰ 命令超时（60秒）"
        except Exception as e:
            return f"❌ 执行错误: {str(e)}"

    def run(self):
        """主循环"""
        print("🤖 SWE Agent 已启动，开始修复 Issue...")

        for step in range(self.max_steps):
            # 调用 Copilot Pro（LiteLLM 自动处理认证）
            response = completion(
                model=self.model,
                messages=self.messages,
                temperature=0.1,   # 低温度让输出更稳定
                max_tokens=1024
            )
            content = response.choices[0].message.content.strip()
            print(f"\n📍 Step {step+1} | LLM 输出预览：\n{content[:300]}...")

            cmd = self._extract_command(content)
            print(f"⚡ 执行命令: {cmd}")

            self.messages.append({"role": "assistant", "content": content})

            # 检测是否提交
            if "SUBMIT" in content.upper() or "patch.diff" in cmd:
                print("\n🎉 Agent 完成修复！生成最终 Patch...")
                patch = self.run_command("git diff HEAD")
                with open("final_patch.diff", "w", encoding="utf-8") as f:
                    f.write(patch)
                print("✅ Patch 已保存为 final_patch.diff")
                break

            # 执行命令并获取观察结果
            obs = self.run_command(cmd)
            print(f"📤 输出（前300字符）: {obs[:300]}...")

            self.messages.append({"role": "user", "content": f"Output:\n{obs}"})

            # 历史压缩（防止 token 爆炸）
            if len(self.messages) > 18:
                self.messages = self.messages[:2] + self.messages[-16:]

        else:
            print("⚠️ 达到最大步数，未完成修复")

        # 清理临时目录
        if self.work_dir and Path(self.work_dir).exists():
            shutil.rmtree(self.work_dir, ignore_errors=True)
            print("🧹 临时目录已清理")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python swe_agent.py <repo_url> \"<issue 描述>\"")
        print('示例: python swe_agent.py https://github.com/user/repo.git "修复 login 页面 500 错误"')
        sys.exit(1)

    repo_url = sys.argv[1]
    issue_desc = sys.argv[2]

    agent = MySweAgent()
    agent.setup(repo_url, issue_desc)
    agent.run()
