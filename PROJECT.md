# DSE 沖刺寶典 · 項目文檔

> 最後更新：2026-07-08
> 項目類型：單頁 HTML 應用（純前端）
> 位置：`C:\Users\张浩lauv\OneDrive\桌面\宝宝的复习小程序1\`

---

## 一、項目概述

為香港 DSE（中學文憑試）學生設計的複習程序，涵蓋 **5 個選修科目**：
- 中國語文（學生薄弱，尤其文言文）
- 英國語文
- 數學（學生最薄弱）
- 經濟
- 視覺藝術

核心功能：真題練習、知識點講解、閃卡記憶、試卷分析、AI 智能生成。

---

## 二、文件結構

```
宝宝的复习小程序1/
├── DSE冲刺宝典.html          ← 主程序（約 5850 行，所有功能都在這一個文件裡）
├── dse_analyzer.py            ← Python 教材分析腳本（可選，用 Gemini API）
├── remove_bg.py               ← 圖片去白邊腳本（可選，用 Pillow）
├── 使用說明.md                ← dse_analyzer.py 的使用說明
├── PROJECT.md                 ← 本文件
└── characters/                ← 角色裝飾圖片
    ├── 小白1.png              ← 用於：側邊欄、作答窗口、評分結果
    ├── 小白2.png              ← 用於：閃卡完成慶祝動畫
    ├── 线条小狗.jpg            ← 用於：右下角浮動吉祥物（有白邊）
    ├── 用户头像1.png           ← 用於：中文科快速入口卡片裝飾
    ├── 用户头像2.png           ← 備用
    ├── 未标题-1.png            ← 備用
    ├── 2303a71be4ee39240b0bf2180d7334c8.png  ← 用於：英語科卡片裝飾
    ├── d1da93ac12efbe373d56423612e5c7ee.png  ← 用於：數學科卡片裝飾
    ├── 5e5f33fc0ca3675cd6b066d200d7451a.png  ← 用於：經濟科卡片裝飾
    ├── 995a0f98d0de305752de7bb4c8714732.png  ← 用於：藝術科卡片裝飾
    ├── 74bdde2727e49d2d8206764158751710.png  ← 備用
    ├── 微信图片_20260622150258_102669_13.jpg ← 用於：DSE 首頁英雄區吉祥物
    └── 微信图片_20260622150337_102670_13.jpg ← 備用
```

---

## 三、頁面結構

### 側邊欄導航
| 頁面 ID | 名稱 | 說明 |
|---------|------|------|
| `dashboard` | 學習主頁 | 總覽、快速入口、各科統計 |
| `upload` | 上傳教材 | 上傳 PDF/DOCX/TXT，AI 分析生成內容 |
| `paper` | 試卷分析 | 上傳模擬試卷，AI 生成參考答案 |
| `review` | 強化記憶 | 閃卡記憶系統，5 個科目 |
| `chinese` | 中國語文 | 真題、知識點、寫作、閃卡 |
| `english` | 英國語文 | Past Paper、Key Concepts、Writing、Flashcards |
| `math` | 數學 | 真題、知識點、公式速查、背公式 |
| `econ` | 經濟 | 真題、知識點、概念卡 |
| `arts` | 視覺藝術 | 真題、知識點、術語卡 |

### 每個科目的標籤頁
每個科目頁面都有 3-4 個標籤頁：
- **📰 真題練習** — DSE 風格題目，含參考答案和解題過程
- **📚 知識點** — 可展開的知識卡片，含通俗講解和考試提示
- **🃏 背卡片/閃卡** — 跳轉到強化記憶系統
- **✍️ 寫作訓練**（僅中文科）

---

## 四、功能詳情

### 4.1 真題練習系統
- 每個科目 5-8 道 DSE 風格題目
- 題型：選擇題、短答題、長答題、翻譯題、寫作題
- 每題有：參考答案、詳細解題過程、常見失分點
- 每題有「✏️ 開始作答」按鈕，可輸入文字或拍照上傳
- 提交後 AI 評分，顯示分數、優點、改善建議、學習計劃

### 4.2 知識點系統
各科知識點數量：
- 中文：13 個（含 12 篇指定篇章詳解）
- 英語：7 個（Tone、Essay Structure、Grammar、Listening、Inference、Writing Formats、Collocations）
- 數學：9 個（二次方程、指數對數、微分、概率、三角學、數列、坐標幾何、不等式）
- 經濟：7 個（供需、彈性、GDP、市場失靈、國際貿易、財政貨幣政策、市場結構）
- 藝術：6 個（視覺元素、藝術批評、文化語境、西方流派、媒材技法、當代議題）

每個知識點包含：
- 難度標記（easy/medium/hard）
- 通俗解釋 + 生活化比喻（💡 通俗理解）
- 舉例說明（📝 舉例說明）
- 常見陷阱（⚠️ 常見陷阱）

### 4.3 閃卡記憶系統
- 5 個科目共 53+ 張閃卡
- 中文：15 張（文言文核心字詞、12 篇指定篇章要點）
- 英語：12 張（高頻詞彙、寫作模板、搭配詞）
- 數學：10 張（必考公式）
- 經濟：8 張（核心概念）
- 藝術：8 張（術語、流派、設計原則）

交互功能：
- 點擊翻轉查看答案
- 標記「✓ 已掌握」或「✗ 需複習」
- 跳過（移到最後）
- 進度追蹤（已掌握/需複習/未學習）
- 完成後可重新練習未掌握的卡片

### 4.4 作答與評分系統
- 文字輸入框 + 拍照上傳
- 字數統計
- AI 模擬評分（基於答案長度、結構、關鍵詞）
- 評分結果彈窗：分數環、優點、改善建議、學習計劃
- 評分時小白角色出現鼓勵

### 4.5 AI 智能分析（接入大模型）
支持 5 個 AI 平台：
| 平台 | API 格式 | 獲取密鑰 |
|------|---------|---------|
| Google Gemini | Gemini 格式 | aistudio.google.com/apikey |
| DeepSeek | OpenAI 兼容 | platform.deepseek.com |
| 小米 MiMo | OpenAI 兼容 | dev.mi.com |
| OpenAI | OpenAI 兼容 | platform.openai.com |
| 自定義 | OpenAI 兼容 | 用戶自定義端點 |

功能：
- 上傳教材 → AI 分析生成知識點、練習題、閃卡
- 上傳試卷 → AI 逐題分析生成參考答案
- 設定保存在 localStorage

### 4.6 角色裝飾系統
| 角色 | 位置 | 動畫效果 |
|------|------|---------|
| 微信图片_20260622150258_102669_13.jpg | 首頁英雄區右下 | 上下浮動 + 懸停放大 |
| 小白1.png | 側邊欄底部 | 微浮動 + 點擊慶祝 + 語音氣泡 |
| 线条小狗.jpg | 右下角浮動 | 上下浮動 + 懸停搖擺 + 語音氣泡 |
| 各角色 PNG | 快速入口卡片右上角 | 懸停彈跳放大 |
| 小白1.png | 作答窗口頂部 | 鼓勵文字 |
| 小白1.png | 評分結果標題 | 標題裝飾 |
| 小白2.png | 閃卡完成 | 慶祝動畫 |

語音氣泡內容：每個頁面有 2-4 條不同的學習提示，切換頁面時自動顯示。

---

## 五、設計系統

### 色彩
```css
--slate-900: #111827    /* 主要文字/按鈕背景 */
--amber-500: #f59e0b    /* 強調色/進度條 */
--emerald-500: #10b981  /* 成功/已掌握 */
--red-500: #ef4444      /* 錯誤/需複習 */

/* 科目專屬色 */
--chinese-accent: #dc2626  /* 紅 */
--english-accent: #2563eb  /* 藍 */
--math-accent: #d97706     /* 橙 */
--econ-accent: #059669     /* 綠 */
--arts-accent: #7c3aed     /* 紫 */
```

### 字體
```css
--font-display: 'Noto Serif TC', serif;   /* 標題 */
--font-body: 'Noto Sans TC', sans-serif;  /* 正文 */
--font-mono: 'JetBrains Mono', monospace; /* 數學公式/代碼 */
```

### 組件
- `.q-card` — 題目卡片
- `.kp-card` — 知識點卡片（可展開）
- `.flashcard` — 閃卡（點擊翻轉）
- `.modal` — 彈窗
- `.grading-card` — 評分結果彈窗
- `.answer-window` — 作答區域
- `.mascot-float` — 浮動吉祥物
- `.mascot-bubble` — 語音氣泡

---

## 六、JavaScript 架構

所有 JS 都在 HTML 文件底部的 `<script>` 標籤內，主要模塊：

### 狀態管理
```javascript
const state = {
  currentPage: 'dashboard',
  answeredQuestions: new Set(),
  totalQuestions: 29,
  progress: 12
};
```

### 頁面導航
- `switchPage(page)` — 切換頁面
- `switchTab(btn, tabId)` — 切換標籤頁
- `filterPills(el)` — 篩選標籤

### 題目交互
- `toggleAnswer(btn)` — 展開/收起參考答案
- `openAnswerWindow(btn)` — 打開作答窗口
- `submitAnswer(btn)` — 提交答案並評分
- `selectMC(option)` — 選擇題交互
- `startRandomPractice()` — 隨機練習彈窗

### 知識點
- `toggleKP(header)` — 展開/收起知識點

### 閃卡系統
```javascript
const flashcardData = { chinese, english, math, econ, arts };
// 每個科目：{ title, cards: [{ front, back }] }
```
- `startFlashcardSession(subject)` — 開始閃卡訓練
- `flipCurrentCard()` — 翻轉當前卡片
- `markFlashcard(status)` — 標記已掌握/需複習
- `skipFlashcard()` — 跳過
- `retryReviewCards()` — 重新練習未掌握的卡片

### AI 系統
```javascript
const AI_PROVIDERS = { gemini, deepseek, xiaomi, openai, custom };
let aiProvider, aiApiKey, aiModel, aiEndpoint; // 保存在 localStorage
```
- `callAI(prompt)` — 統一 AI 調用（自動選擇 Gemini 或 OpenAI 格式）
- `analyzeWithAI(content, subject, subjectName)` — 分析教材生成知識點/題目/閃卡
- `handleFilesWithAI(files)` — 上傳教材 + AI 分析
- `handlePaperFilesWithAI(files)` — 上傳試卷 + AI 分析

### 角色系統
- `toggleMascotBubble()` — 顯示/隱藏語音氣泡
- `mascotSpeak(source)` — 角色說話 + 慶祝動畫
- `mascotCelebrate()` — 慶祝動畫

---

## 七、已知問題

1. **白邊問題**：JPG 角色圖片有白色矩形背景，CSS `mix-blend-mode` 無法精確去除（會連角色身體白色一起去掉）。解決方案：用 `remove_bg.py` 轉 PNG，或用在線工具 remove.bg
2. **PDF 讀取**：FileReader.readAsText 無法正確讀取 PDF 二進制內容，需要 PDF.js 庫
3. **上傳功能限制**：教材分析和試卷分析需要有效的 AI API 密鑰才能真正工作
4. **移動端側邊欄**：小屏幕下側邊欄隱藏，沒有漢堡菜單

---

## 八、後續可優化方向

1. **圖片白邊**：將 JPG 轉為透明背景 PNG（用 remove_bg.py 或在線工具）
2. **PDF 支持**：引入 PDF.js 庫支持真正的 PDF 文本提取
3. **更多題目**：每個科目可擴展到 15-20 題
4. **錯題本**：記錄答錯的題目，定期複習
5. **學習統計**：記錄每天學習時間、答題正確率
6. **移動端優化**：添加漢堡菜單、優化觸摸交互
7. **離線支持**：添加 Service Worker 支持離線使用
8. **匯出功能**：將 AI 生成的內容匯出為 PDF

---

## 九、開發注意事項

- 所有內容使用**繁體中文**（香港標準）
- 數學公式使用 Unicode 符號 + `var(--font-mono)` 字體
- 圖片路徑使用**相對路徑**（`characters/xxx.png`）
- CSS 變量定義在 `:root` 中
- 所有交互使用原生 JavaScript，無框架依賴
- localStorage 用於保存 AI 設定（密鑰、模型、平台）
- 文件很大（5800+ 行），修改時建議用精確的 `Edit` 而非重寫整個文件
