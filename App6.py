import streamlit as st
import requests
import numpy as np
from PIL import Image
import io
import base64
import datetime

# === 設定頁面 ===
st.set_page_config(
    page_title="霓虹新聞速報產生器",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ... (FOOTER_PRESETS and TOKEN_MAPPING remain unchanged)

# === 全新設計的高質感 SVG 圖標庫 ===
# ... (SVG_ICONS remains unchanged, spans from source: 4 to 33)

NEON_ICONS_CONFIG = [
    # 這裡的 'icon' 欄位現在存的是上面的 SVG 代碼
    {'id': 'bull', 'label': '上漲 Bull', 'icon': 
SVG_ICONS['bull'], 'color': 'text-green-400', 'bg': 'bg-green-400'},
    {'id': 'bear', 'label': '下跌 Bear', 'icon': SVG_ICONS['bear'], 'color': 'text-red-400', 'bg': 'bg-red-400'},
    {'id': 'alert', 'label': '警告 Alert', 'icon': SVG_ICONS['alert'], 'color': 'text-yellow-400', 'bg': 'bg-yellow-400'},
    {'id': 'lock', 'label': '鎖倉 Lock', 'icon': SVG_ICONS['lock'], 'color': 'text-purple-400', 'bg': 'bg-purple-400'},
    {'id': 'unlock', 'label': '解鎖 Unlock', 'icon': SVG_ICONS['unlock'], 'color': 'text-pink-400', 'bg': 'bg-pink-400'},
    {'id': 'tech', 'label': '技術 Tech', 'icon': SVG_ICONS['tech'], 'color': 'text-blue-400', 'bg': 'bg-blue-400'},
    {'id': 'swap', 'label': '交易 Swap', 'icon': SVG_ICONS['swap'], 'color': 'text-indigo-400', 'bg': 'bg-indigo-400'},
    {'id': 'news', 'label': '公告 News', 'icon': 
SVG_ICONS['news'], 'color': 'text-orange-400', 'bg': 'bg-orange-400'},
    {'id': 'fund', 'label': '資金 Fund', 'icon': SVG_ICONS['fund'], 'color': 'text-emerald-400', 'bg': 'bg-emerald-400'},
    {'id': 'event', 'label': '活動 Event', 'icon': SVG_ICONS['event'], 'color': 'text-yellow-300', 'bg': 'bg-yellow-300'},
    # === 新增 AI 風格選項 (模擬) ===
    {'id': 'ai_style', 'label': 'AI 風格 (未來擴充)', 'icon': SVG_ICONS['tech'], 'color': 'text-cyan-400', 'bg': 'bg-cyan-400'},
]

# === 工具函式 ===
# ... (remove_white_background_logic, image_to_base64, fetch_coingecko_image, get_default_token_image remain unchanged, spans from source: 36 to 38)

# === 初始化 Session State ===
if 'news_data' not in st.session_state:
    st.session_state.news_data = [
        {
         
   "id": 1,
            "title": "HYPE 正式解鎖！",
            "content": "3.12 億美元代幣已進入流通，現貨與合約交易全面開啟。",
            "token_mode": "custom",
            "token_value": "HYPE", 
            "token_image_base64": None, 
            "status_mode": "auto",
            "status_value": None
 
       },
        # ... (other default news items remain unchanged, spans from source: 41 to 43)

# ... (global_settings initialization and Section 1 remain unchanged, spans from source: 44 to 45)

# ... (Section 2 - News Card Editing remains unchanged, spans from source: 46 to 57)
# Note: The 'status_options' variable in Section 2 will automatically include 'ai_style' 
# because it is derived from NEON_ICONS_CONFIG.

            if current_status in status_options:
                 display_index = status_options.index(current_status)

            selected_status = st.selectbox("選擇狀態", status_options, index=display_index, key=f"st_{idx}", format_func=lambda x: next((i['label'] for i in NEON_ICONS_CONFIG if i['id'] == x), x))

            if selected_status in ["auto", "none"]:
         
       st.session_state.news_data[idx]['status_mode'] = selected_status
                st.session_state.news_data[idx]['status_value'] = None
            else:
                st.session_state.news_data[idx]['status_mode'] = "select"
                st.session_state.news_data[idx]['status_value'] = selected_status
        
            # 在這裡可以新增一個 AI 生成按鈕，讓使用者輸入提示詞 (Prompt)
            if selected_status == 'ai_style':
                st.warning("您選擇了 AI 風格。請注意：此功能目前為模擬介面，需整合外部 AI 服務才能實現圖片生成。")
                ai_prompt = st.text_input("AI 圖片生成 Prompt (例: 機器人與代幣的賽博龐克風格)", key=f"ai_prompt_{idx}")
                # st.button("生成 AI 圖片 (需整合 API)", key=f"btn_ai_{idx}", disabled=True) # 實際整合時可啟用


st.markdown("---")
# ... (Section 3 - Footer remains unchanged, spans from source: 59)

# === HTML 生成核心 ===
def generate_html_preview():
    news_items_html = ""
    
    for idx, item in enumerate(st.session_state.news_data):
        token_html = ""
        has_token = False
        if item['token_mode'] != 'none' and item['token_image_base64']:
            has_token = True
            # === 確認：這裡的 drop-shadow 樣式不影響圖片顏色，只增加發光效果，保留 ===
            token_html = f"""
            <div class="relative w-20 
h-20">
                <img src="{item['token_image_base64']}" class="w-full h-full object-contain drop-shadow-[0_0_15px_rgba(255,255,255,0.2)]" />
            </div>
            """
        
        status_config = None
        detected_status_id = 'activity' 
        text_content = (item['title'] + item['content']).lower()
        
     
   if item['status_mode'] == 'select' and item['status_value']:
             status_id = item['status_value']
             status_config = next((i for i in NEON_ICONS_CONFIG if i['id'] == status_id), None)
        elif item['status_mode'] == 'auto':
             if has_token:
                 status_config = None 
        
     else:
                 if any(k in text_content for k in ['上漲', '新高', 'bull']): detected_status_id = 'bull'
                 elif any(k in text_content for k in ['下跌', '暴跌', 'bear']): detected_status_id = 'bear'
                 elif any(k in text_content for k in ['警告', '風險', 'alert']): detected_status_id = 'alert'
        
         status_config = next((i for i in NEON_ICONS_CONFIG if i['id'] == detected_status_id), None)
        
        status_html = ""
        title_color_class = "text-white"
        
        if status_config:
            title_color_class = status_config['color'] 
            # 修改點：直接插入 SVG 字串，並移除 data-lucide 和不必要的 class
            
            # === AI 風格的佔位符 SVG ===
            if status_config['id'] == 'ai_style':
                 status_svg_content = f"""
                 <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none">
                    <defs>
                        <linearGradient id="ai-grad" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" style="stop-color:{status_config['color'].split('-')[-1]};stop-opacity:1" />
                            <stop offset="100%" style="stop-color:{status_config['color'].split('-')[-1]};stop-opacity:0.7" />
                        </linearGradient>
                    </defs>
                    <rect x="3" y="3" width="18" height="18" rx="2" stroke="url(#ai-grad)" stroke-width="2" stroke-dasharray="4 4"/>
                    <path d="M7 17l10-10M7 10h10M7 14h10" stroke="url(#ai-grad)" stroke-width="2" stroke-linecap="round"/>
                </svg>
                 """
            else:
                 status_svg_content = status_config['icon']
            # ==============================
  
          status_html = f"""
            <div class="relative flex items-center justify-center w-24 h-24 -mb-2 -mr-2">
                <div class="absolute inset-0 blur-2xl opacity-40 {status_config['bg']}"></div>
                <div class="w-full h-full drop-shadow-[0_0_10px_rgba(255,255,255,0.3)]">
                    {status_svg_content} 
        
        </div>
            </div>
            """
        elif has_token:
            # === 調整：若有代幣圖片，標題顏色使用預設白色，避免顏色衝突 ===
            title_color_class = "text-white" 
            
        border_colors = [
            "border-green-500/30 shadow-[0_0_15px_rgba(74,222,128,0.15)]",
          
  "border-purple-500/30 shadow-[0_0_15px_rgba(168,85,247,0.15)]",
            "border-indigo-500/30 shadow-[0_0_15px_rgba(99,102,241,0.15)]",
            "border-yellow-500/30 shadow-[0_0_15px_rgba(234,179,8,0.15)]"
        ]
        # ... (rest of the HTML generation remains unchanged, spans from source: 67 to 88)
