# 黃山料風格對話機器人

一個以「數位人格／數位永生」概念為架構、加入黃山料公開作品索引與 RAG/TF-IDF 檢索的繁體中文對話機器人。

## 重要定位

本專案不是黃山料本人，也不宣稱是作者本人。
它是「受公開資料與作品主題啟發的風格化對話系統」。

不要把仍受著作權保護的完整書籍放進公開發布的 repository。
如果你合法擁有、且有權使用某些全文資料，可以放入 `knowledge/` 作為本機私人知識庫。

## 功能

- Streamlit Chat UI
- OpenAI API 模式
- Ollama 本機模型模式
- Markdown / TXT / JSON 知識庫
- TF-IDF 檢索
- 關鍵詞 + TF-IDF 混合排序
- 來源顯示
- SQLite 對話記憶
- 人格設定檔
- 使用者 correction / feedback
- 可重新建立索引
- 可下載對話紀錄
- 不依賴 LangChain

## 專案結構

```text
HuangShanLiao-Style-Chatbot/
├── app.py
├── config.py
├── llm.py
├── rag.py
├── database.py
├── persona.py
├── safety.py
├── requirements.txt
├── .env.example
├── README.md
├── knowledge/
│   ├── persona.md
│   ├── works/
│   ├── articles/
│   ├── interviews/
│   └── sources/
├── data/
├── tests/
│   └── test_core.py
└── .gitignore
```

## Windows 安裝

```powershell
cd HuangShanLiao-Style-Chatbot
py -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

複製：

```text
.env.example
```

成：

```text
.env
```

然後填入 API key。

## 啟動

```powershell
streamlit run app.py
```

瀏覽器通常會開：

```text
http://localhost:8501
```

## Ollama

如果你想完全本機執行，先自行安裝 Ollama 並下載一個適合繁體中文的模型，然後在 `.env`：

```env
LLM_PROVIDER=ollama
OLLAMA_MODEL=你的模型名稱
OLLAMA_BASE_URL=http://localhost:11434/v1
```

本專案使用 OpenAI-compatible endpoint，因此不需要另一套 Ollama SDK。

## Gemini API（推薦目前使用這個）

```env
LLM_PROVIDER=gemini
GEMINI_API_KEY=你的_GEMINI_API_KEY
GEMINI_MODEL=gemini-3.8-flash
```

本專案透過 Google 官方提供的 OpenAI-compatible Gemini endpoint，
所以不需要把整個程式改成另一套聊天介面。

如果你想改回 OpenAI：

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=你的_API_KEY
OPENAI_MODEL=gpt-5.6-luna
```


也可以直接在 `config.py` 的 `OPENAI_API_KEY` 欄位放入個人測試用 key，但不要把真正的 key commit 到 GitHub。

## 知識庫

把你合法可以使用的資料放到：

```text
knowledge/
```

支援：

- `.md`
- `.txt`
- `.json`

重新啟動 App 時會自動建立 TF-IDF index。

## 目前內建資料

目前附上的資料是「作品索引／主題 metadata」，不是書籍全文。
它包含公開作品名稱、類型、主題與研究資料夾規劃。

## 測試

```powershell
python -m pytest
```
