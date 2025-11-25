"""
Ứng Dụng Tạo Video Giáo Dục Tự Động với AI
Educational Video Creator with AI and Avatar
"""
import streamlit as st
import os
import time
from datetime import datetime

# Import services
from gemini_service import GeminiService
from heygen_service import HeyGenService
from file_service import FileService

# Page configuration
st.set_page_config(
    page_title="AI Video Education Creator",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'processed_script' not in st.session_state:
    st.session_state.processed_script = None
if 'video_id' not in st.session_state:
    st.session_state.video_id = None
if 'video_status' not in st.session_state:
    st.session_state.video_status = None
if 'selected_avatar' not in st.session_state:
    st.session_state.selected_avatar = None
if 'script_filename' not in st.session_state:
    st.session_state.script_filename = None

# Initialize services
@st.cache_resource
def init_services():
    """Initialize all services"""
    try:
        gemini = GeminiService()
        heygen = HeyGenService()
        file_svc = FileService()
        return gemini, heygen, file_svc
    except Exception as e:
        st.error(f"❌ Lỗi khởi tạo services: {str(e)}")
        st.stop()

gemini_service, heygen_service, file_service = init_services()

# Header
st.title("🎓 AI Video Education Creator")
st.markdown("**Tạo video giáo dục tự động với AI và Avatar**")
st.divider()

# Sidebar
with st.sidebar:
    st.header("📋 Quy trình")
    st.markdown("""
    1. **Upload Script** - Tải lên hoặc nhập script
    2. **AI Processing** - Xử lý với Google Gemini AI
    3. **Create Video** - Chọn avatar và tạo video
    4. **Preview** - Xem và tải video
    """)
    
    st.divider()
    
    # API Usage Stats
    st.header("📊 API Usage")
    try:
        usage = gemini_service.get_usage_stats()
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Còn lại/phút", f"{usage['remaining']}/{usage['max_per_minute']}")
        with col2:
            st.metric("Tổng đã dùng", usage['total_calls'])
        
        # Progress bar for rate limit
        progress = usage['calls_this_minute'] / usage['max_per_minute']
        st.progress(progress, text=f"Rate limit: {usage['calls_this_minute']}/{usage['max_per_minute']}")
        
        if usage['remaining'] == 0:
            st.warning("⏳ Đợi 1 phút để reset")
    except:
        pass
    
    st.divider()
    
    st.header("📁 Scripts đã lưu")
    try:
        scripts = file_service.list_scripts()
        if scripts:
            for script in scripts[:5]:  # Show last 5 scripts
                st.text(f"📄 {script['name']}")
                st.caption(f"   {script['modified'].strftime('%Y-%m-%d %H:%M')}")
        else:
            st.info("Chưa có script nào")
    except Exception as e:
        st.error(f"Lỗi: {str(e)}")

# Main content - Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📤 Bước 1: Upload Script", "🤖 Bước 2: AI Processing", "🎬 Bước 3: Tạo Video", "📺 Bước 4: Preview & Download"])

# ==================== TAB 1: UPLOAD SCRIPT ====================
with tab1:
    st.header("📤 Bước 1: Upload hoặc Nhập Script")
    
    # Choose input method
    input_method = st.radio("Chọn phương thức nhập:", ["📁 Upload File", "✍️ Nhập Trực Tiếp"])
    
    script_content = None
    
    if input_method == "📁 Upload File":
        uploaded_file = st.file_uploader(
            "Chọn file script (.txt hoặc .docx)",
            type=['txt', 'docx'],
            help="Hỗ trợ định dạng .txt và .docx"
        )
        
        if uploaded_file:
            try:
                with st.spinner("Đang đọc file..."):
                    script_content = file_service.read_uploaded_file(uploaded_file)
                    st.session_state.script_filename = os.path.splitext(uploaded_file.name)[0]
                
                st.success(f"✅ Đã đọc file: {uploaded_file.name}")
                st.text_area("Nội dung script:", script_content, height=300, disabled=True)
                
            except Exception as e:
                st.error(f"❌ Lỗi đọc file: {str(e)}")
    
    else:  # Direct input
        script_content = st.text_area(
            "Nhập nội dung script hoặc prompt:",
            height=300,
            placeholder="Ví dụ: Tạo một bài giảng về tầm quan trọng của AI trong giáo dục..."
        )
        
        if script_content:
            st.session_state.script_filename = f"manual_input_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Process button
    if script_content:
        if st.button("💾 Lưu Script và Tiếp tục", type="primary"):
            st.session_state.processed_script = script_content
            st.success("✅ Script đã sẵn sàng! Vui lòng chọn **Bước 2: AI Processing** để tiếp tục.")

# ==================== TAB 2: AI PROCESSING ====================
with tab2:
    st.header("🤖 Bước 2: Xử lý Script với AI")
    
    if not st.session_state.processed_script:
        st.warning("⚠️ Vui lòng hoàn thành Bước 1 trước!")
    else:
        st.success("✅ Script gốc đã sẵn sàng")
        
        # Show original script
        with st.expander("📄 Xem Script Gốc", expanded=False):
            st.text_area("Script gốc:", st.session_state.processed_script, height=200, disabled=True)
        
        # AI Processing options
        st.subheader("Chọn phương thức xử lý:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✨ Tạo Nội Dung Mới từ Prompt"):
                with st.spinner("🤖 AI đang tạo nội dung..."):
                    try:
                        generated_content = gemini_service.generate_educational_content(
                            st.session_state.processed_script
                        )
                        st.session_state.processed_script = generated_content
                        st.success("✅ Đã tạo nội dung mới!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Lỗi: {str(e)}")
        
        with col2:
            if st.button("🎨 Cải Thiện Script Hiện Tại"):
                with st.spinner("🤖 AI đang cải thiện script..."):
                    try:
                        enhanced_content = gemini_service.enhance_script(
                            st.session_state.processed_script
                        )
                        st.session_state.processed_script = enhanced_content
                        st.success("✅ Đã cải thiện script!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Lỗi: {str(e)}")
        
        st.divider()
        
        # Show processed script
        st.subheader("📝 Script Đã Xử Lý")
        edited_script = st.text_area(
            "Bạn có thể chỉnh sửa script trước khi lưu:",
            st.session_state.processed_script,
            height=300
        )
        st.session_state.processed_script = edited_script
        
        # Save script
        col1, col2 = st.columns([2, 1])
        with col1:
            save_filename = st.text_input(
                "Tên file lưu:",
                value=st.session_state.script_filename or f"script_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            )
        with col2:
            save_format = st.selectbox("Định dạng:", ["txt", "docx"])
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Lưu Script vào Script Folder"):
                try:
                    saved_path = file_service.save_script(
                        st.session_state.processed_script,
                        save_filename,
                        save_format
                    )
                    st.success(f"✅ Đã lưu: {saved_path}")
                except Exception as e:
                    st.error(f"❌ Lỗi: {str(e)}")
        
        with col2:
            if st.button("➡️ Tiếp tục đến Bước 3: Tạo Video", type="primary"):
                st.success("✅ Chuyển sang Bước 3")
                st.rerun()

# ==================== TAB 3: CREATE VIDEO ====================
with tab3:
    st.header("🎬 Bước 3: Tạo Video với Avatar")
    
    if not st.session_state.processed_script:
        st.warning("⚠️ Vui lòng hoàn thành Bước 1 và 2 trước!")
    else:
        # Show script summary
        with st.expander("📄 Script sẽ được dùng cho video", expanded=False):
            st.text_area("", st.session_state.processed_script, height=200, disabled=True)
        
        st.divider()
        
        # Get avatars
        st.subheader("👤 Chọn Avatar")
        
        with st.spinner("Đang tải danh sách avatars..."):
            try:
                avatars = heygen_service.get_avatars()
                
                if avatars:
                    # Display avatars in grid
                    cols = st.columns(4)
                    for idx, avatar in enumerate(avatars[:20]):  # Show first 20
                        with cols[idx % 4]:
                            st.image(avatar['preview_url'], use_column_width=True)
                            if st.button(
                                f"Chọn {avatar['name'][:15]}",
                                key=f"avatar_{avatar['id']}"
                            ):
                                st.session_state.selected_avatar = avatar
                                st.success(f"✅ Đã chọn: {avatar['name']}")
                    
                    # Show selected avatar
                    if st.session_state.selected_avatar:
                        st.divider()
                        st.subheader("Avatar đã chọn:")
                        col1, col2 = st.columns([1, 3])
                        with col1:
                            st.image(st.session_state.selected_avatar['preview_url'])
                        with col2:
                            st.write(f"**Tên:** {st.session_state.selected_avatar['name']}")
                            st.write(f"**ID:** {st.session_state.selected_avatar['id']}")
                            st.write(f"**Giới tính:** {st.session_state.selected_avatar.get('gender', 'N/A')}")
                        
                        # Video title
                        video_title = st.text_input(
                            "Tiêu đề video:",
                            value=f"Educational Video - {datetime.now().strftime('%Y-%m-%d')}"
                        )
                        
                        # Create video button
                        if st.button("🎬 Tạo Video", type="primary"):
                            with st.spinner("🎬 Đang tạo video... Vui lòng đợi..."):
                                try:
                                    video_id = heygen_service.create_video(
                                        script=st.session_state.processed_script,
                                        avatar_id=st.session_state.selected_avatar['id'],
                                        title=video_title
                                    )
                                    st.session_state.video_id = video_id
                                    st.session_state.video_status = "processing"
                                    st.success(f"✅ Video đang được tạo! ID: {video_id}")
                                    st.info("➡️ Chuyển sang Bước 4 để theo dõi tiến trình")
                                    time.sleep(2)
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"❌ Lỗi: {str(e)}")
                
                else:
                    st.warning("Không tìm thấy avatar nào")
                    
            except Exception as e:
                st.error(f"❌ Lỗi khi tải avatars: {str(e)}")

# ==================== TAB 4: PREVIEW & DOWNLOAD ====================
with tab4:
    st.header("📺 Bước 4: Preview & Download Video")
    
    if not st.session_state.video_id:
        st.warning("⚠️ Vui lòng tạo video ở Bước 3 trước!")
    else:
        st.info(f"🎬 Video ID: {st.session_state.video_id}")
        
        # Check video status
        if st.button("🔄 Kiểm tra trạng thái video"):
            with st.spinner("Đang kiểm tra..."):
                try:
                    status_data = heygen_service.get_video_status(st.session_state.video_id)
                    st.session_state.video_status = status_data
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Lỗi: {str(e)}")
        
        # Auto-polling
        if st.session_state.video_status:
            status = st.session_state.video_status.get('status')
            
            if status == "processing" or status == "pending":
                st.warning(f"⏳ Video đang được xử lý: {status}")
                st.info("🔄 Tự động kiểm tra sau 10 giây...")
                
                # Progress bar
                progress_bar = st.progress(0)
                for i in range(10):
                    time.sleep(1)
                    progress_bar.progress((i + 1) * 10)
                
                # Auto refresh
                st.rerun()
            
            elif status == "completed":
                st.success("✅ Video đã hoàn thành!")
                
                video_url = st.session_state.video_status.get('video_url')
                thumbnail_url = st.session_state.video_status.get('thumbnail_url')
                duration = st.session_state.video_status.get('duration')
                
                # Show thumbnail
                if thumbnail_url:
                    st.image(thumbnail_url, caption="Video Thumbnail", use_column_width=True)
                
                # Video info
                if duration:
                    st.write(f"⏱️ **Thời lượng:** {duration} giây")
                
                # Video player
                if video_url:
                    st.subheader("🎥 Xem Video")
                    st.video(video_url)
                    
                    # Download button
                    st.divider()
                    col1, col2 = st.columns(2)
                    with col1:
                        st.link_button("📥 Tải Video", video_url)
                    with col2:
                        if st.button("🔄 Tạo Video Mới"):
                            # Reset session state
                            st.session_state.video_id = None
                            st.session_state.video_status = None
                            st.session_state.processed_script = None
                            st.session_state.selected_avatar = None
                            st.success("✅ Đã reset! Bắt đầu lại từ Bước 1")
                            st.rerun()
            
            elif status == "failed":
                st.error("❌ Tạo video thất bại!")
                error_msg = st.session_state.video_status.get('error', 'Unknown error')
                st.error(f"Chi tiết lỗi: {error_msg}")
                
                if st.button("🔄 Thử lại"):
                    st.session_state.video_id = None
                    st.session_state.video_status = None
                    st.rerun()

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🎓 AI Video Education Creator | Powered by Google Gemini & HeyGen</p>
</div>
""", unsafe_allow_html=True)
