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
if 'video_info' not in st.session_state:
    st.session_state.video_info = {}
if 'selected_format_id' not in st.session_state:
    st.session_state.selected_format_id = ""

# --- USER INPUT ---
url_input = st.text_input("🔗 Paste the YouTube video URL:", value=st.session_state.url)

if st.button("🔍 Analyze"):
    if url_input:
        st.session_state.url = url_input
        st.session_state.analyzed = True

        try:
            ydl_opts = {
                'quiet': True,
                'skip_download': True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(st.session_state.url, download=False)
                st.session_state.video_info = info
        except Exception as e:
            st.error(f"❌ Failed to analyze video: {str(e)}")
            st.session_state.analyzed = False

# --- ANALYSIS & FORMAT SELECTION ---
if st.session_state.analyzed and st.session_state.url and st.session_state.video_info:
    info = st.session_state.video_info
    st.video(st.session_state.url)
    st.markdown(f"**🎞 Title:** {info.get('title')}")
    st.markdown("### 🎧 Choose Download Type")
    st.session_state.format = st.radio("Select format:", ["Video (MP4)", "Audio (MP3)"], index=0)

    # --- List all formats ---
    if st.session_state.format == "Video (MP4)":
        formats = [f for f in info['formats'] if f.get('ext') == 'mp4' and f.get('vcodec') != 'none']
        formats = sorted(formats, key=lambda x: x.get('height', 0), reverse=True)
    else:
        formats = [f for f in info['formats'] if f.get('vcodec') == 'none' and f.get('acodec') != 'none']
        # formats = sorted(formats, key=lambda x: x.get('abr', 0), reverse=True)
        formats = sorted(formats, key=lambda x: x.get('abr') or 0, reverse=True)

    format_options = []
    for f in formats:
        size = f.get('filesize') or f.get('filesize_approx')
        size_mb = f"{round(size / 1024 / 1024, 2)} MB" if size else "Unknown size"
        quality = f"{f.get('height', f.get('abr'))}p" if f.get('height') else f"{f.get('abr')}kbps"
        fmt_text = f"{f['format_id']} - {quality} - {f['ext']} - {size_mb}"
        format_options.append(fmt_text)

    selected_option = st.selectbox("🎞 Select Stream Format:", format_options)
    st.session_state.selected_format_id = selected_option.split(" - ")[0]

    # --- Download Button ---
    if st.button("📥 Download Now"):
        try:
            with st.spinner("Downloading..."):
                selected_format = next((f for f in formats if f["format_id"] == st.session_state.selected_format_id), None)
                filename = f"{info['title']}.{selected_format.get('ext', 'mp4')}"
                ydl_opts = {
                    'format': selected_format['format_id'],
                    'outtmpl': filename,
                    'quiet': True,
                    'ffmpeg_location': 'C:/ffmpeg/bin',  # 👈 Change this if needed
                }

                if st.session_state.format == "Audio (MP3)":
                    ydl_opts['postprocessors'] = [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }]
                    filename = filename.rsplit(".", 1)[0] + ".mp3"

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([st.session_state.url])

            st.success("✅ Download complete!")
            st.info(f"📁 File: {filename}\n📦 Format: {selected_format.get('format_note', 'Custom')} | {selected_format.get('ext')} | {selected_format.get('height', 'Audio')}p")

            with open(filename, "rb") as f:
                st.download_button("📂 Download File", data=f.read(), file_name=filename)

        except Exception as e:
            st.error(f"❌ Download failed: {str(e)}")
