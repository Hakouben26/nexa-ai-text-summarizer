## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Web application interface |
| Groq API | Access to hosted AI models |
| Qwen (LLM) | Multilingual text summarization |
| PyPDF | Extracting text from PDF files |
| python-dotenv | Secure API key configuration |

## ⚙️ How It Works

Nexa AI follows a simple AI-powered text summarization workflow:

1. **User Input:** The user enters text or uploads a PDF document.
2. **PDF Extraction:** PyPDF extracts readable text from uploaded PDF files.
3. **Text Processing:** The application prepares the input and generates instructions based on the selected summary length and output language.
4. **AI Processing:** The application sends the text and prompt to the Qwen language model through the Groq API.
5. **Summary Generation:** The AI model generates a concise summary while preserving the main information.
6. **Output:** Streamlit displays the generated summary and allows users to download it as a TXT file.

## 🏗️ Project Architecture

```text
User
 |
 v
Streamlit Interface (app.py)
 |
 +------------------+
 |                  |
 v                  v
Text Input      PDF Upload
                    |
                    v
              PyPDF Extraction
 |                  |
 +--------+---------+
          |
          v
   summarizer.py
          |
          v
     Groq API
          |
          v
      Qwen LLM
          |
          v
  Generated Summary
          |
          v
  Display & Download
```

## 🔐 API Configuration

Nexa AI uses an environment variable to protect the Groq API key.

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
```

Never upload your actual `.env` file or API key to GitHub.

## 📌 Key Features

- AI-powered text summarization.
- Multilingual output: English, Arabic and French.
- PDF text extraction and summarization.
- Adjustable summary length: Short, Medium and Detailed.
- Downloadable TXT summaries.
- Simple and user-friendly web interface.