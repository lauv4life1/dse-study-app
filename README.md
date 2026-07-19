# DSE 智能教材分析工具

## 免費獲取 Gemini API 密鑰（5分鐘搞定）

### 步驟一：獲取 API 密鑰
1. 打開 https://aistudio.google.com/apikey
2. 用你的 Google 帳號登入
3. 點擊 **「Create API Key」**（建立API密鑰）
4. 選擇一個項目（或建立新項目）
5. 複製生成的密鑰（一串字母和數字）

> 💡 Gemini API 有免費額度，足夠個人學習使用，不需要綁定信用卡。

### 步驟二：安裝 Python（如果還沒有的話）
1. 打開 https://www.python.org/downloads/
2. 下載最新版本的 Python
3. 安裝時 **勾選「Add Python to PATH」**

### 步驟三：運行分析工具

#### 方法一：互動式運行（推薦新手）
```bash
python dse_analyzer.py
```
然後按照提示輸入 API 密鑰和文件路徑即可。

#### 方法二：命令行運行
```bash
python dse_analyzer.py --api-key "你的密鑰" --files "教材.pdf" --subject chinese
```

#### 支持的參數：
- `--api-key` / `-k`：Gemini API 密鑰
- `--files` / `-f`：教材文件路徑（支持多個，用空格分隔）
- `--subject` / `-s`：科目（chinese/english/math/econ/arts）
- `--output` / `-o`：輸出文件路徑

### 支持的文件格式
- **PDF** (.pdf)：課本、練習冊的電子版
- **Word** (.docx)：筆記、講義
- **純文字** (.txt)：文字版教材

### 分析結果
運行後會在 `dse_analysis_output` 文件夾中生成：
1. **HTML 片段**：可以直接粘貼到 DSE 沖刺寶典中
2. **JSON 數據**：結構化的分析結果

### 常見問題

**Q: API 密鑰安全嗎？**
A: 密鑰只在你本地電腦使用，不會上傳到任何地方。建議設置環境變量保存密鑰：
```bash
# Windows (PowerShell)
$env:GEMINI_API_KEY="你的密鑰"

# Mac/Linux
export GEMINI_API_KEY="你的密鑰"
```

**Q: 免費額度夠用嗎？**
A: Gemini API 免費層每分鐘15次請求，每天1500次請求，完全足夠個人學習使用。

**Q: 分析結果不準確怎麼辦？**
A: AI 生成的內容僅供參考，建議對照課本和老師的講解進行核實。你也可以把生成的結果發給我，我來幫你優化。

**Q: 可以一次分析多個文件嗎？**
A: 可以！用空格分隔文件路徑即可：
```bash
python dse_analyzer.py -f "課本.pdf" "筆記.docx" "練習.txt" -s chinese
```
