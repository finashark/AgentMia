"""
HeyGen API Service
Handles video generation with avatars using HeyGen API
"""
import requests
import time
from typing import Dict, List, Optional
from config import HEYGEN_BASE_URL, HEYGEN_HEADERS, VIDEO_POLL_INTERVAL

class HeyGenService:
    def __init__(self):
        """Initialize HeyGen API service"""
        self.base_url = HEYGEN_BASE_URL
        self.headers = HEYGEN_HEADERS
        
        if not self.headers.get("X-Api-Key"):
            raise ValueError("HEYGEN_API_KEY not found in environment variables")
    
    def get_avatars(self) -> List[Dict]:
        """
        Get list of available avatars
        
        Returns:
            List of avatar dictionaries with id, name, preview_url
        """
        try:
            url = f"{self.base_url}/v2/avatars"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            data = response.json()
            avatars = data.get("data", {}).get("avatars", [])
            
            # Format avatar data
            formatted_avatars = []
            for avatar in avatars:
                formatted_avatars.append({
                    "id": avatar.get("avatar_id"),
                    "name": avatar.get("avatar_name"),
                    "preview_url": avatar.get("preview_image_url"),
                    "gender": avatar.get("gender"),
                })
            
            return formatted_avatars
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Lỗi khi lấy danh sách avatars: {str(e)}")
    
    def get_voices(self) -> List[Dict]:
        """
        Get list of available AI voices
        
        Returns:
            List of voice dictionaries
        """
        try:
            url = f"{self.base_url}/v2/voices"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            data = response.json()
            voices = data.get("data", {}).get("voices", [])
            
            # Format voice data
            formatted_voices = []
            for voice in voices:
                formatted_voices.append({
                    "id": voice.get("voice_id"),
                    "name": voice.get("name"),
                    "language": voice.get("language"),
                    "gender": voice.get("gender"),
                })
            
            return formatted_voices
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Lỗi khi lấy danh sách voices: {str(e)}")
    
    def create_video(self, 
                     script: str, 
                     avatar_id: str,
                     voice_id: Optional[str] = None,
                     title: str = "Educational Video") -> str:
        """
        Create a video with avatar and script
        
        Args:
            script: The script content for the video
            avatar_id: ID of the avatar to use
            voice_id: Optional voice ID (if not provided, avatar's default voice is used)
            title: Title for the video
            
        Returns:
            video_id: The ID of the created video
        """
        try:
            url = f"{self.base_url}/v2/video/generate"
            
            # Prepare video configuration
            payload = {
                "video_inputs": [
                    {
                        "character": {
                            "type": "avatar",
                            "avatar_id": avatar_id,
                            "avatar_style": "normal"
                        },
                        "voice": {
                            "type": "text",
                            "input_text": script
                        }
                    }
                ],
                "title": title,
                "test": False  # Set to False for production
            }
            
            # Add voice if provided
            if voice_id:
                payload["video_inputs"][0]["voice"]["voice_id"] = voice_id
            
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            
            data = response.json()
            video_id = data.get("data", {}).get("video_id")
            
            if not video_id:
                raise Exception("Không nhận được video_id từ HeyGen API")
            
            return video_id
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Lỗi khi tạo video: {str(e)}")
    
    def get_video_status(self, video_id: str) -> Dict:
        """
        Check video generation status
        
        Args:
            video_id: The ID of the video to check
            
        Returns:
            Dictionary with status, video_url, thumbnail_url, duration, etc.
        """
        try:
            url = f"{self.base_url}/v1/video_status.get"
            params = {"video_id": video_id}
            
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            video_data = data.get("data", {})
            
            return {
                "status": video_data.get("status"),  # pending, processing, completed, failed
                "video_url": video_data.get("video_url"),
                "thumbnail_url": video_data.get("thumbnail_url"),
                "duration": video_data.get("duration"),
                "error": video_data.get("error"),
                "callback_id": video_data.get("callback_id")
            }
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Lỗi khi kiểm tra trạng thái video: {str(e)}")
    
    def wait_for_video_completion(self, video_id: str, max_wait_time: int = 600) -> Dict:
        """
        Wait for video to complete with polling
        
        Args:
            video_id: The ID of the video to wait for
            max_wait_time: Maximum time to wait in seconds (default 10 minutes)
            
        Returns:
            Final video status dictionary
        """
        start_time = time.time()
        
        while True:
            # Check if max wait time exceeded
            if time.time() - start_time > max_wait_time:
                raise Exception("Timeout: Video generation took too long")
            
            # Get current status
            status_data = self.get_video_status(video_id)
            status = status_data.get("status")
            
            # Check completion status
            if status == "completed":
                return status_data
            elif status == "failed":
                error_msg = status_data.get("error", "Unknown error")
                raise Exception(f"Video generation failed: {error_msg}")
            
            # Wait before next poll
            time.sleep(VIDEO_POLL_INTERVAL)
    
    def download_video(self, video_url: str, output_path: str) -> bool:
        """
        Download video from URL
        
        Args:
            video_url: URL of the video to download
            output_path: Local path to save the video
            
        Returns:
            True if successful
        """
        try:
            response = requests.get(video_url, stream=True)
            response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return True
            
        except Exception as e:
            raise Exception(f"Lỗi khi tải video: {str(e)}")

# Test function
if __name__ == "__main__":
    service = HeyGenService()
    
    # Test get avatars
    avatars = service.get_avatars()
    print(f"Found {len(avatars)} avatars")
    if avatars:
        print(f"First avatar: {avatars[0]}")
