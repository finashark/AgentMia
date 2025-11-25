"""
Google Gemini AI Service
Handles content generation using Google Gemini API
Version: 1.2 - Added rate limiting to prevent API abuse
"""
import google.generativeai as genai
from config import GOOGLE_API_KEY, GEMINI_MODEL
import streamlit as st
import time
from datetime import datetime, timedelta

# Rate limiting configuration
MAX_CALLS_PER_MINUTE = 5  # Maximum API calls per minute
COOLDOWN_SECONDS = 60     # Cooldown period in seconds

class GeminiService:
    def __init__(self):
        """Initialize Gemini AI service"""
        if not GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        genai.configure(api_key=GOOGLE_API_KEY)
        self.model = genai.GenerativeModel(GEMINI_MODEL)
        
        # Initialize rate limiting in session state
        if 'api_call_times' not in st.session_state:
            st.session_state.api_call_times = []
        if 'total_api_calls' not in st.session_state:
            st.session_state.total_api_calls = 0
    
    def _check_rate_limit(self) -> tuple[bool, str]:
        """
        Check if API call is allowed based on rate limiting
        
        Returns:
            Tuple of (is_allowed, message)
        """
        now = datetime.now()
        
        # Remove calls older than 1 minute
        st.session_state.api_call_times = [
            t for t in st.session_state.api_call_times 
            if now - t < timedelta(seconds=COOLDOWN_SECONDS)
        ]
        
        # Check rate limit
        if len(st.session_state.api_call_times) >= MAX_CALLS_PER_MINUTE:
            oldest_call = min(st.session_state.api_call_times)
            wait_time = COOLDOWN_SECONDS - (now - oldest_call).seconds
            return False, f"⏳ Đã đạt giới hạn {MAX_CALLS_PER_MINUTE} lần/phút. Vui lòng đợi {wait_time} giây."
        
        return True, ""
    
    def _record_api_call(self):
        """Record an API call for rate limiting"""
        st.session_state.api_call_times.append(datetime.now())
        st.session_state.total_api_calls += 1
    
    def get_usage_stats(self) -> dict:
        """Get API usage statistics"""
        now = datetime.now()
        recent_calls = len([
            t for t in st.session_state.api_call_times 
            if now - t < timedelta(seconds=COOLDOWN_SECONDS)
        ])
        return {
            "calls_this_minute": recent_calls,
            "max_per_minute": MAX_CALLS_PER_MINUTE,
            "remaining": MAX_CALLS_PER_MINUTE - recent_calls,
            "total_calls": st.session_state.total_api_calls
        }
    
    def generate_educational_content(self, script_prompt: str) -> str:
        """
        Generate educational content from script prompt
        
        Args:
            script_prompt: The input script/prompt to process
            
        Returns:
            Generated educational content as string
        """
        # Check rate limit first
        is_allowed, message = self._check_rate_limit()
        if not is_allowed:
            raise Exception(message)
        
        try:
            # Embed system instruction in prompt for compatibility
            full_prompt = f"""Bạn là một chuyên gia tạo nội dung giáo dục.
Nhiệm vụ của bạn là tạo ra các bài giảng, script video giáo dục chất lượng cao.
Nội dung phải:
- Dễ hiểu, rõ ràng
- Có cấu trúc logic
- Phù hợp để đọc thành video
- Ngắn gọn nhưng đầy đủ thông tin
- Sử dụng ngôn ngữ thân thiện, dễ tiếp cận

Yêu cầu: {script_prompt}"""
            
            # Record API call
            self._record_api_call()
            
            # Generate content
            response = self.model.generate_content(full_prompt)
            
            return response.text
            
        except Exception as e:
            if "rate" in str(e).lower() or "quota" in str(e).lower():
                raise Exception(f"🚫 Google API rate limit đã đạt. Vui lòng đợi vài phút và thử lại.")
            raise Exception(f"Lỗi khi tạo nội dung với Gemini AI: {str(e)}")
    
    def enhance_script(self, original_script: str) -> str:
        """
        Enhance and improve an existing script
        
        Args:
            original_script: The original script to enhance
            
        Returns:
            Enhanced script
        """
        # Check rate limit first
        is_allowed, message = self._check_rate_limit()
        if not is_allowed:
            raise Exception(message)
        
        try:
            prompt = f"""Hãy cải thiện và làm script sau đây hay hơn, phù hợp để tạo video giáo dục:

{original_script}

Yêu cầu:
- Giữ nguyên ý chính
- Cải thiện cách diễn đạt
- Thêm hook/intro hấp dẫn nếu cần
- Đảm bảo cấu trúc rõ ràng
- Độ dài phù hợp để đọc trong video 2-5 phút
"""
            # Record API call
            self._record_api_call()
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            if "rate" in str(e).lower() or "quota" in str(e).lower():
                raise Exception(f"🚫 Google API rate limit đã đạt. Vui lòng đợi vài phút và thử lại.")
            raise Exception(f"Lỗi khi cải thiện script: {str(e)}")
    
    def summarize_script(self, script: str, max_length: int = 200) -> str:
        """
        Create a summary of the script
        
        Args:
            script: The script to summarize
            max_length: Maximum length of summary
            
        Returns:
            Summary text
        """
        # Check rate limit first
        is_allowed, message = self._check_rate_limit()
        if not is_allowed:
            raise Exception(message)
        
        try:
            prompt = f"""Tóm tắt ngắn gọn nội dung script sau trong khoảng {max_length} ký tự:

{script}
"""
            # Record API call
            self._record_api_call()
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            if "rate" in str(e).lower() or "quota" in str(e).lower():
                raise Exception(f"🚫 Google API rate limit đã đạt. Vui lòng đợi vài phút và thử lại.")
            raise Exception(f"Lỗi khi tóm tắt script: {str(e)}")

# Test function
if __name__ == "__main__":
    service = GeminiService()
    test_prompt = "Tạo một bài giảng ngắn về tầm quan trọng của việc học lập trình"
    result = service.generate_educational_content(test_prompt)
    print(result)
