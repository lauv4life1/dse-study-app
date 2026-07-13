# -*- coding: utf-8 -*-
"""
DSE 沖刺寶典 · 教材智能分析工具
使用 Google Gemini API 分析教材，自動生成知識點、練習題和閃卡

使用前準備：
1. 前往 https://aistudio.google.com/apikey 免費獲取 Gemini API 密鑰
2. 安裝依賴：pip install google-generativeai PyPDF2 python-docx --break-system-packages
3. 運行：python dse_analyzer.py
"""

import os
import sys
import json
import argparse
from pathlib import Path

# ── 檢查並安裝依賴 ──
def install_deps():
    """自動安裝所需的Python庫"""
    deps = ['google-generativeai', 'PyPDF2', 'python-docx']
    for dep in deps:
        try:
            __import__(dep.replace('-', '_').split('[')[0])
        except ImportError:
            print(f"  正在安裝 {dep}...")
            os.system(f"{sys.executable} -m pip install {dep} --break-system-packages -q")

install_deps()

import google.generativeai as genai
from PyPDF2 import PdfReader
from docx import Document

# ── 配置 ──
GEMINI_MODEL = "gemini-2.0-flash"  # 免費模型，速度快
OUTPUT_DIR = Path(__file__).parent / "dse_analysis_output"

SUBJECTS = {
    "chinese": "中國語文",
    "english": "英語",
    "math": "數學",
    "econ": "經濟",
    "arts": "視覺藝術"
}

# ── 文件讀取 ──
def read_pdf(file_path):
    """讀取PDF文件內容"""
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"  ❌ 讀取PDF失敗: {e}")
        return None

def read_docx(file_path):
    """讀取DOCX文件內容"""
    try:
        doc = Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
        return text
    except Exception as e:
        print(f"  ❌ 讀取DOCX失敗: {e}")
        return None

def read_txt(file_path):
    """讀取TXT文件內容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='gbk') as f:
            return f.read()
    except Exception as e:
        print(f"  ❌ 讀取TXT失敗: {e}")
        return None

def read_file(file_path):
    """根據文件類型讀取內容"""
    ext = Path(file_path).suffix.lower()
    readers = {
        '.pdf': read_pdf,
        '.docx': read_docx,
        '.doc': read_docx,
        '.txt': read_txt,
    }
    reader = readers.get(ext)
    if reader:
        return reader(file_path)
    else:
        print(f"  ❌ 不支持的文件格式: {ext}")
        return None

# ── AI 分析 ──
def analyze_with_gemini(api_key, content, subject, analysis_type):
    """
    使用 Gemini API 分析教材內容

    analysis_type: 'knowledge' | 'questions' | 'flashcards'
    """
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(GEMINI_MODEL)

    subject_name = SUBJECTS.get(subject, subject)

    prompts = {
        "knowledge": f"""你是一位經驗豐富的香港DSE{subject_name}科補習老師。
請仔細分析以下教材內容，提取出最重要的知識點。

要求：
1. 提取5-10個核心知識點
2. 每個知識點包含：標題、難度（easy/medium/hard）、詳細解釋
3. 用通俗易懂的語言解釋，適合高中生理解
4. 加入生活化的比喻幫助記憶
5. 標註DSE考試中常見的考法和陷阱
6. 使用繁體中文

教材內容：
{content[:8000]}

請以JSON格式輸出，格式如下：
[
  {{
    "title": "知識點標題",
    "difficulty": "easy/medium/hard",
    "subtitle": "簡短描述",
    "explanation": "詳細解釋，包含比喻和例子",
    "exam_tips": "DSE考試相關提示",
    "common_mistakes": "常見錯誤"
  }}
]

只輸出JSON，不要其他文字。""",

        "questions": f"""你是一位經驗豐富的香港DSE{subject_name}科出題老師。
請根據以下教材內容，生成5道DSE風格的練習題。

要求：
1. 題目風格要貼近DSE真題
2. 包含不同難度（基礎、進階、高難度）
3. 每道題包含：題目、分值、參考答案、詳細解題過程
4. 標註考查的知識點和常見失分點
5. 使用繁體中文

教材內容：
{content[:8000]}

請以JSON格式輸出，格式如下：
[
  {{
    "question": "題目內容",
    "type": "選擇題/短答題/長答題",
    "difficulty": "easy/medium/hard",
    "marks": 6,
    "tags": ["DSE風格", "進階"],
    "answer": "參考答案",
    "explanation": "詳細解題過程和評分要點",
    "common_mistakes": "常見失分點"
  }}
]

只輸出JSON，不要其他文字。""",

        "flashcards": f"""你是一位經驗豐富的香港DSE{subject_name}科補習老師。
請根據以下教材內容，生成10張記憶閃卡。

要求：
1. 每張閃卡有「正面」（問題/術語）和「背面」（答案/解釋）
2. 涵蓋教材中的關鍵概念、公式、定義
3. 背面要包含簡潔的解釋和助記方法
4. 使用繁體中文

教材內容：
{content[:8000]}

請以JSON格式輸出，格式如下：
[
  {{
    "front": "閃卡正面（問題或術語）",
    "back": "閃卡背面（答案和解釋）"
  }}
]

只輸出JSON，不要其他文字。"""
    }

    prompt = prompts.get(analysis_type)
    if not prompt:
        return None

    try:
        print(f"    📡 正在呼叫 Gemini API ({analysis_type})...")
        response = model.generate_content(prompt)
        text = response.text.strip()

        # 嘗試提取JSON
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()

        return json.loads(text)
    except json.JSONDecodeError as e:
        print(f"    ⚠️ JSON解析失敗，嘗試修復...")
        try:
            # 嘗試找到JSON數組
            start = text.find('[')
            end = text.rfind(']') + 1
            if start >= 0 and end > start:
                return json.loads(text[start:end])
        except:
            pass
        print(f"    ❌ 無法解析AI回應: {e}")
        print(f"    原始回應: {text[:200]}...")
        return None
    except Exception as e:
        print(f"    ❌ API呼叫失敗: {e}")
        return None

# ── HTML 生成 ──
def generate_html(knowledge_points, questions, flashcards, subject, source_file):
    """將分析結果轉換為可嵌入HTML的格式"""
    subject_name = SUBJECTS.get(subject, subject)
    html_parts = []

    # 知識點HTML
    if knowledge_points:
        html_parts.append(f'<div class="section-header"><h3>📖 {subject_name} · AI生成知識點</h3><span class="sh-count">{len(knowledge_points)} 個</span></div>')
        for kp in knowledge_points:
            diff_class = kp.get('difficulty', 'medium')
            html_parts.append(f'''
<div class="kp-card">
  <div class="kp-header" onclick="toggleKP(this)">
    <div class="kp-left">
      <div class="kp-diff {diff_class}"></div>
      <div>
        <div class="kp-title">{kp.get('title', '')}</div>
        <div class="kp-subtitle">{kp.get('subtitle', '')}</div>
      </div>
    </div>
    <div class="kp-arrow">▼</div>
  </div>
  <div class="kp-body">
    <div class="kp-explain">
      <p>{kp.get('explanation', '')}</p>
      {"<div class='warn-box'>" + kp.get('common_mistakes', '') + "</div>" if kp.get('common_mistakes') else ""}
      {"<div class='tip-note'>" + kp.get('exam_tips', '') + "</div>" if kp.get('exam_tips') else ""}
    </div>
  </div>
</div>''')

    # 練習題HTML
    if questions:
        html_parts.append(f'<div class="section-header" style="margin-top:28px;"><h3>📝 {subject_name} · AI生成練習題</h3><span class="sh-count">{len(questions)} 題</span></div>')
        for q in questions:
            tags = ''.join([f'<span class="q-tag tag-paper">{t}</span>' for t in q.get('tags', ['AI生成'])])
            html_parts.append(f'''
<div class="q-card">
  <div class="q-header">
    {tags}
    <span class="q-type">{q.get('type', '')} · {q.get('marks', 0)}分</span>
  </div>
  <div class="q-text">{q.get('question', '')}</div>
  <div class="q-actions">
    <button class="btn btn-primary" onclick="toggleAnswer(this)">📖 查看參考答案</button>
    <button class="btn btn-accent" data-action="answer" onclick="openAnswerWindow(this)">✏️ 開始作答</button>
  </div>
  <div class="q-answer">
    <div class="answer-label">參考答案</div>
    <div class="answer-text">
      <p>{q.get('answer', '')}</p>
      {"<p style='margin-top:10px;'>" + q.get('explanation', '') + "</p>" if q.get('explanation') else ""}
      {"<div class='wrong-note'>" + q.get('common_mistakes', '') + "</div>" if q.get('common_mistakes') else ""}
    </div>
  </div>
</div>''')

    # 閃卡數據
    if flashcards:
        flashcard_json = json.dumps(flashcards, ensure_ascii=False, indent=2)
        html_parts.append(f'''
<script>
// AI生成的閃卡數據 ({subject_name})
if (typeof flashcardData !== 'undefined') {{
  flashcardData['{subject}_ai'] = {{
    title: '{subject_name} · AI生成閃卡 ({source_file})',
    cards: {flashcard_json}
  }};
}}
</script>''')

    return '\n'.join(html_parts)

# ── 主程序 ──
def main():
    parser = argparse.ArgumentParser(description='DSE 教材智能分析工具')
    parser.add_argument('--api-key', '-k', help='Gemini API 密鑰（也可設置環境變量 GEMINI_API_KEY）')
    parser.add_argument('--files', '-f', nargs='+', help='要分析的教材文件路徑（支持PDF/DOCX/TXT）')
    parser.add_argument('--subject', '-s', choices=list(SUBJECTS.keys()), default='chinese', help='科目（默認: chinese）')
    parser.add_argument('--output', '-o', help='輸出HTML文件路徑')
    args = parser.parse_args()

    # 獲取API密鑰
    api_key = args.api_key or os.environ.get('GEMINI_API_KEY')
    if not api_key:
        print("=" * 50)
        print("🔑 需要 Gemini API 密鑰")
        print("=" * 50)
        print()
        print("免費獲取步驟：")
        print("1. 打開 https://aistudio.google.com/apikey")
        print("2. 登入 Google 帳號")
        print("3. 點擊「Create API Key」")
        print("4. 複製生成的密鑰")
        print()
        api_key = input("請輸入你的 Gemini API 密鑰: ").strip()
        if not api_key:
            print("❌ 未提供密鑰，退出程序")
            return

    # 獲取文件路徑
    files = args.files
    if not files:
        print()
        print("📂 請輸入要分析的教材文件路徑")
        print("   （支持多個文件，用空格分隔）")
        print("   （支持格式：PDF、DOCX、TXT）")
        print()
        files_input = input("文件路徑: ").strip()
        if not files_input:
            print("❌ 未提供文件，退出程序")
            return
        files = files_input.split()

    # 選擇科目
    subject = args.subject
    if not args.files:
        print()
        print("📚 選擇科目：")
        for i, (key, name) in enumerate(SUBJECTS.items(), 1):
            print(f"   {i}. {name}")
        print()
        choice = input("請選擇 (1-5，默認1=中文): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= 5:
            subject = list(SUBJECTS.keys())[int(choice) - 1]

    subject_name = SUBJECTS[subject]
    print()
    print("=" * 50)
    print(f"📚 科目: {subject_name}")
    print(f"📄 文件: {', '.join([Path(f).name for f in files])}")
    print("=" * 50)

    # 讀取所有文件
    all_content = ""
    for file_path in files:
        print(f"\n📖 讀取文件: {Path(file_path).name}")
        content = read_file(file_path)
        if content:
            all_content += f"\n\n--- {Path(file_path).name} ---\n\n{content}"
            print(f"  ✅ 成功讀取 {len(content)} 字")
        else:
            print(f"  ❌ 讀取失敗")

    if not all_content.strip():
        print("\n❌ 沒有成功讀取任何內容，退出程序")
        return

    # 截取內容（避免超出API限制）
    max_chars = 15000
    if len(all_content) > max_chars:
        print(f"\n⚠️ 內容過長（{len(all_content)}字），截取前{max_chars}字進行分析")
        all_content = all_content[:max_chars]

    # 執行三種分析
    print("\n🔍 開始AI分析...")
    print("-" * 30)

    print("\n1️⃣ 生成知識點...")
    knowledge = analyze_with_gemini(api_key, all_content, subject, "knowledge")
    if knowledge:
        print(f"   ✅ 生成 {len(knowledge)} 個知識點")
    else:
        print("   ⚠️ 知識點生成失敗")

    print("\n2️⃣ 生成練習題...")
    questions = analyze_with_gemini(api_key, all_content, subject, "questions")
    if questions:
        print(f"   ✅ 生成 {len(questions)} 道題目")
    else:
        print("   ⚠️ 題目生成失敗")

    print("\n3️⃣ 生成閃卡...")
    flashcards = analyze_with_gemini(api_key, all_content, subject, "flashcards")
    if flashcards:
        print(f"   ✅ 生成 {len(flashcards)} 張閃卡")
    else:
        print("   ⚠️ 閃卡生成失敗")

    # 生成HTML
    source_file = Path(files[0]).stem
    html_output = generate_html(knowledge, questions, flashcards, subject, source_file)

    # 保存結果
    OUTPUT_DIR.mkdir(exist_ok=True)

    # 保存HTML片段
    html_file = OUTPUT_DIR / f"{subject}_{source_file}_generated.html"
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_output)
    print(f"\n💾 HTML片段已保存: {html_file}")

    # 保存JSON原始數據
    json_file = OUTPUT_DIR / f"{subject}_{source_file}_data.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump({
            "subject": subject,
            "source_file": source_file,
            "knowledge_points": knowledge or [],
            "questions": questions or [],
            "flashcards": flashcards or []
        }, f, ensure_ascii=False, indent=2)
    print(f"💾 JSON數據已保存: {json_file}")

    # 說明如何整合
    print()
    print("=" * 50)
    print("✅ 分析完成！")
    print("=" * 50)
    print()
    print("📋 如何將結果加入 DSE 沖刺寶典：")
    print(f"   1. 打開 {html_file}")
    print(f"   2. 複製其中的內容")
    print(f"   3. 在 DSE冲刺宝典.html 中找到「{subject_name}」科目的知識點區域")
    print(f"   4. 將內容粘貼到該區域的末尾")
    print()
    print(f"   或者你也可以把 {json_file} 的內容發給我，")
    print("   我來幫你整合到程序中！")

if __name__ == "__main__":
    main()
