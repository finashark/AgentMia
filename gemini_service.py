"""
Google Gemini AI Service
Handles content generation using Google Gemini API
Version: 1.1 - Fixed system_instruction compatibility
"""
import google.generativeai as genai
from config import GOOGLE_API_KEY, GEMINI_MODEL
import streamlit as st

class GeminiService:
    def __init__(self):
        """Initialize Gemini AI service"""
        if not GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        genai.configure(api_key=GOOGLE_API_KEY)
        self.model = genai.GenerativeModel(GEMINI_MODEL)
    
    def generate_educational_content(self, script_prompt: str) -> str:
        """
        Generate educational content from script prompt
        
        Args:
            script_prompt: The input script/prompt to process
            
        Returns:
            Generated educational content as string
        """
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
            
            # Generate content
            response = self.model.generate_content(full_prompt)
            
            return response.text
            
        except Exception as e:
            raise Exception(f"Lỗi khi tạo nội dung với Gemini AI: {str(e)}")
    
    def enhance_script(self, original_script: str) -> str:
        """
        Enhance and improve an existing script
        
        Args:
            original_script: The original script to enhance
            
        Returns:
            Enhanced script
        """
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
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
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
        try:
            prompt = f"""Tóm tắt ngắn gọn nội dung script sau trong khoảng {max_length} ký tự:

{script}
"""
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            raise Exception(f"Lỗi khi tóm tắt script: {str(e)}")

# Test function
if __name__ == "__main__":
    service = GeminiService()
    test_prompt = "Tạo một bài giảng ngắn về tầm quan trọng của việc học lập trình"
    result = service.generate_educational_content(test_prompt)
    print(result)
