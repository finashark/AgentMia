# 🎓 AI Video Education Creator

Ứng dụng tạo video giáo dục tự động sử dụng Google Gemini AI và HeyGen Avatar.

## ✨ Tính năng

- 📤 **Upload Script**: Hỗ trợ file `.txt` và `.docx`, hoặc nhập trực tiếp
- 🤖 **AI Processing**: Tự động tạo hoặc cải thiện nội dung với Google Gemini AI
- 💾 **Lưu Script**: Tự động lưu script đã xử lý vào thư mục `Script Folder`
- 👤 **Chọn Avatar**: Danh sách avatar chuyên nghiệp từ HeyGen
- 🎬 **Tạo Video**: Tự động tạo video với avatar đọc script
- 📺 **Preview**: Xem trước và tải video hoàn thành
- 🔄 **Auto Polling**: Tự động kiểm tra trạng thái video mỗi 10 giây

## 📋 Yêu cầu

- Python 3.8+
- Google Gemini API Key
- HeyGen API Key

## 🚀 Cài đặt

### 1. Clone hoặc tải project

```bash
cd "d:\SharkMe Data\Agent Mia"
```

### 2. Cài đặt thư viện

```bash
pip install -r requirements.txt
```

### 3. Cấu hình API Keys

Tạo file `.env` trong thư mục project:

```env
# Google Gemini API Key
GOOGLE_API_KEY=AIzaSyAatiPCrIhKggy4r-POSS4Z7NP_4f4zngI

# HeyGen API Key
HEYGEN_API_KEY=sk_V2_hgu_kRNe9hdFVsl_F5bevciTXZD00vGekb3pajQXMToe5DMY
```

**Lưu ý**: File `.env.example` đã được cung cấp sẵn với API keys mẫu.

## 🎯 Cách sử dụng

### Chạy ứng dụng

```bash
streamlit run app.py
```

Ứng dụng sẽ mở tại: `http://localhost:8501`

### Quy trình sử dụng

#### 📤 Bước 1: Upload Script
- Chọn file `.txt` hoặc `.docx`, hoặc
- Nhập trực tiếp nội dung/prompt vào ô text

#### 🤖 Bước 2: AI Processing
- **Tạo Nội Dung Mới**: AI tạo script hoàn chỉnh từ prompt
- **Cải Thiện Script**: AI cải thiện script hiện tại
- Chỉnh sửa thủ công nếu cần
- Lưu script vào `Script Folder`

#### 🎬 Bước 3: Tạo Video
- Duyệt và chọn avatar phù hợp
- Nhập tiêu đề video
- Nhấn "Tạo Video"

#### 📺 Bước 4: Preview & Download
- Tự động kiểm tra trạng thái (polling 10s)
- Xem video khi hoàn thành
- Tải video về máy
- Hoặc bắt đầu lại quy trình

## 📁 Cấu trúc Project

```
Agent Mia/
├── app.py                  # Ứng dụng Streamlit chính
├── config.py               # Cấu hình API keys và settings
├── gemini_service.py       # Service xử lý Google Gemini AI
├── heygen_service.py       # Service xử lý HeyGen API
├── file_service.py         # Service xử lý file I/O
├── requirements.txt        # Danh sách thư viện Python
├── .env                    # API keys (không commit lên Git)
├── .env.example            # Template cho API keys
├── README.md               # File này
└── Script Folder/          # Thư mục lưu scripts đã xử lý
    └── (các file script)
```

## 🔑 API Keys

### Google Gemini API
- Đăng ký tại: [Google AI Studio](https://aistudio.google.com/apikey)
- Model sử dụng: `gemini-2.0-flash-exp`

### HeyGen API
- Đăng ký tại: [HeyGen](https://app.heygen.com/settings?nav=API)
- Endpoints:
  - `/v2/avatars` - Lấy danh sách avatars
  - `/v2/video/generate` - Tạo video
  - `/v1/video_status.get` - Kiểm tra trạng thái

## ⚙️ Cấu hình

Chỉnh sửa `config.py` để thay đổi:

```python
# Model Gemini
GEMINI_MODEL = "gemini-2.0-flash-exp"

# Polling interval (giây)
VIDEO_POLL_INTERVAL = 10

# Định dạng file hỗ trợ
SUPPORTED_FILE_FORMATS = [".docx", ".txt"]
```

## 🛠️ Troubleshooting

### Lỗi: "GOOGLE_API_KEY not found"
- Kiểm tra file `.env` đã tạo chưa
- Đảm bảo API key chính xác

### Lỗi: "HEYGEN_API_KEY not found"
- Kiểm tra file `.env` đã có HeyGen API key
- Đảm bảo key còn hiệu lực

### Video không tải được
- Kiểm tra kết nối internet
- Video URL của HeyGen có thể hết hạn sau 7 ngày
- Gọi lại API status để lấy URL mới

### Import errors
- Chạy lại: `pip install -r requirements.txt`
- Kiểm tra Python version >= 3.8

## 📦 Deployment lên Streamlit Cloud

### 1. Push code lên GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-repo-url>
git push -u origin main
```

### 2. Deploy trên Streamlit Cloud

1. Truy cập: [share.streamlit.io](https://share.streamlit.io)
2. Kết nối GitHub repository
3. Chọn branch `main`
4. File chính: `app.py`
5. **Quan trọng**: Thêm Secrets trong Settings:
   ```toml
   GOOGLE_API_KEY = "AIzaSyAatiPCrIhKggy4r-POSS4Z7NP_4f4zngI"
   HEYGEN_API_KEY = "sk_V2_hgu_kRNe9hdFVsl_F5bevciTXZD00vGekb3pajQXMToe5DMY"
   ```

### 3. .gitignore

Tạo file `.gitignore`:

```
.env
__pycache__/
*.pyc
.DS_Store
Script Folder/*.docx
Script Folder/*.txt
~$*
```

## 🎓 Ví dụ Sử dụng

### Tạo bài giảng từ prompt

```
Input: "Tạo bài giảng về tầm quan trọng của AI trong giáo dục, 
dành cho học sinh THPT, thời lượng 3 phút"

AI sẽ tạo script hoàn chỉnh → Chọn avatar giáo viên → Tạo video
```

### Cải thiện script có sẵn

```
Input: Upload file script.docx

AI cải thiện → Chỉnh sửa thủ công → Lưu → Chọn avatar → Tạo video
```

## 📝 Ghi chú

- Video generation mất 2-5 phút tùy độ dài script
- Polling tự động mỗi 10 giây
- Scripts được lưu tự động với timestamp
- Video URL hết hạn sau 7 ngày (cần gọi lại API)

## 📞 Hỗ trợ

- Google Gemini: [Documentation](https://ai.google.dev/docs)
- HeyGen API: [Documentation](https://docs.heygen.com/)
- Streamlit: [Documentation](https://docs.streamlit.io/)

## 📄 License

MIT License - Free to use and modify

---

**Phát triển bởi**: AI Education Team
**Version**: 1.0.0
**Ngày cập nhật**: November 2025
