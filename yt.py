import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="YouTube Downloader with yt-dlp", layout="centered")
st.title("🎬 YouTube Downloader with yt-dlp")

# --- SESSION STATE SETUP ---
if 'url' not in st.session_state:
    st.session_state.url = ""
if 'analyzed' not in st.session_state:
    st.session_state.analyzed = False
if 'format' not in st.session_state:
    st.session_state.format = "Video (MP4)"

# --- USER INPUT ---
url_input = st.text_input("🔗 Paste the YouTube video URL:", value=st.session_state.url)

if st.button("🔍 Analyze"):
    if url_input:
        st.session_state.url = url_input
        st.session_state.analyzed = True

# --- ANALYSIS & DOWNLOAD SECTION ---
if st.session_state.analyzed and st.session_state.url:
    try:
        st.video(st.session_state.url)
        st.markdown("### 🎧 Choose Download Type")

        # Store selected format
        st.session_state.format = st.radio("Select format:", ["Video (MP4)", "Audio (MP3)"], index=0)

        if st.button("📥 Download Now"):
            with st.spinner("Downloading..."):
                try:
                    if st.session_state.format == "Video (MP4)":
                        ydl_opts = {
                            'format': 'best[ext=mp4]/best',
                            'outtmpl': '%(title)s.%(ext)s',
                            'quiet': True,
                            'noplaylist': True,
                        }
                    else:
                        ydl_opts = {
                            'format': 'bestaudio/best',
                            'outtmpl': '%(title)s.%(ext)s',
                            'quiet': True,
                            'noplaylist': True,
                            'ffmpeg_location': 'C:/ffmpeg/bin',  # 👈 Your FFmpeg path
                            'postprocessors': [{
                                'key': 'FFmpegExtractAudio',
                                'preferredcodec': 'mp3',
                                'preferredquality': '192',
                            }],
                        }

                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(st.session_state.url, download=True)
                        ext = 'mp3' if st.session_state.format == "Audio (MP3)" else 'mp4'
                        filename = f"{info['title']}.{ext}"

                    st.success(f"✅ Download complete: {filename}")
                    with open(filename, "rb") as f:
                        st.download_button("📂 Download File", data=f.read(), file_name=filename)

                except Exception as e:
                    st.error(f"❌ Download failed: {str(e)}")
    except Exception as e:
        st.error(f"❌ Could not analyze video: {str(e)}")

# import streamlit as st
# import yt_dlp
# import os

# st.set_page_config(page_title="YouTube Downloader", layout="centered")
# st.title("🎬 YouTube Downloader with yt-dlp")

# url = st.text_input("Paste the YouTube video URL:")

# def download_video(video_url):
#     ydl_opts = {
#         'outtmpl': '%(title)s.%(ext)s',
#         'format': 'best[ext=mp4]/best',
#         'quiet': True,
#         'noplaylist': True,
#     }
#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         info = ydl.extract_info(video_url, download=True)
#         return f"{info['title']}.{info['ext']}"

# if url:
#     st.video(url)
#     if st.button("📥 Download with yt-dlp"):
#         with st.spinner("Downloading..."):
#             try:
#                 filename = download_video(url)
#                 st.success(f"✅ Download complete: {filename}")
#                 st.download_button(label="📂 Download File",
#                                    data=open(filename, "rb").read(),
#                                    file_name=filename)
#             except Exception as e:
#                 st.error(f"❌ Download failed: {str(e)}")



# import streamlit as st
# import yt_dlp
# import os

# st.set_page_config(page_title="YouTube Downloader with yt-dlp", layout="centered")
# st.title("🎬 YouTube Downloader with yt-dlp")

# # --- SESSION STATE SETUP ---
# if 'url' not in st.session_state:
#     st.session_state.url = ""
# if 'analyzed' not in st.session_state:
#     st.session_state.analyzed = False
# if 'format' not in st.session_state:
#     st.session_state.format = "Video (MP4)"
# if 'video_info' not in st.session_state:
#     st.session_state.video_info = {}

# # --- USER INPUT ---
# url_input = st.text_input("🔗 Paste the YouTube video URL:", value=st.session_state.url)

# if st.button("🔍 Analyze"):
#     if url_input:
#         st.session_state.url = url_input
#         st.session_state.analyzed = True

#         # --- Get video info without download ---
#         try:
#             ydl_opts = {
#                 'quiet': True,
#                 'skip_download': True,
#             }
#             with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#                 info = ydl.extract_info(st.session_state.url, download=False)
#                 st.session_state.video_info = info
#         except Exception as e:
#             st.error(f"❌ Failed to analyze video: {str(e)}")
#             st.session_state.analyzed = False

# # --- ANALYSIS & DOWNLOAD SECTION ---
# if st.session_state.analyzed and st.session_state.url and st.session_state.video_info:
#     info = st.session_state.video_info
#     st.video(st.session_state.url)
#     st.markdown(f"**🎞 Title:** {info.get('title')}")
#     st.markdown(f"**📺 Channel:** {info.get('uploader')}")
#     st.markdown(f"**🕒 Duration:** {int(info.get('duration', 0)) // 60} min")
#     st.markdown(f"**👁 Views:** {info.get('view_count'):,}")

#     # --- Format selection ---
#     st.markdown("### 🎧 Choose Download Type")
#     st.session_state.format = st.radio("Select format:", ["Video (MP4)", "Audio (MP3)"], index=0)

#     # --- Show file size & format info ---
#     selected_format_info = None

#     if st.session_state.format == "Video (MP4)":
#         # Filter for progressive video
#         formats = [f for f in info['formats'] if f.get('ext') == 'mp4' and f.get('acodec') != 'none' and f.get('vcodec') != 'none']
#         formats = sorted(formats, key=lambda x: x.get('height', 0), reverse=True)
#     else:
#         formats = [f for f in info['formats'] if f.get('acodec') != 'none' and f.get('vcodec') == 'none']
#         formats = sorted(formats, key=lambda x: x.get('abr', 0), reverse=True)

#     if formats:
#         options = []
#         for f in formats:
#             label = f"{f.get('format_id')} - {f.get('ext')} - {f.get('height', f.get('abr', '') )}p - {round(f.get('filesize', 0) / 1024 / 1024, 2) if f.get('filesize') else 'unknown'} MB"
#             options.append(label)

#         selected = st.selectbox("🎞 Choose stream:", options)
#         selected_format_id = selected.split(" - ")[0]
#         selected_format_info = next((f for f in formats if f['format_id'] == selected_format_id), None)

#     # --- Download Button ---
#     if st.button("📥 Download Now") and selected_format_info:
#         try:
#             with st.spinner("Downloading..."):
#                 filename = f"{info['title']}.{selected_format_info.get('ext', 'mp4')}"
#                 ydl_opts = {
#                     'format': selected_format_id,
#                     'outtmpl': filename,
#                     'quiet': True,
#                 }

#                 # Add audio postprocessing if MP3
#                 if st.session_state.format == "Audio (MP3)":
#                     ydl_opts['postprocessors'] = [{
#                         'key': 'FFmpegExtractAudio',
#                         'preferredcodec': 'mp3',
#                         'preferredquality': '192',
#                     }]
#                     filename = filename.rsplit(".", 1)[0] + ".mp3"

#                 with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#                     ydl.download([st.session_state.url])

#             st.success(f"✅ Download complete!")
#             st.info(f"📁 File: {filename}\n🧾 Format: {selected_format_info.get('format_note', '') or selected_format_info.get('height', 'Audio')}p - {selected_format_info.get('ext')}")
#             with open(filename, "rb") as f:
#                 st.download_button("📂 Save to your device", data=f.read(), file_name=filename)

#         except Exception as e:
#             st.error(f"❌ Download failed: {str(e)}")
