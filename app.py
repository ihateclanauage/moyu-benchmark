import streamlit as st
import time
import urllib.parse
from PIL import Image, ImageDraw, ImageFont
import io
import os
import textwrap

# --- 1. 全局配置 ---
st.set_page_config(
    page_title="摸鱼生物鉴定所 Pro",
    page_icon="🧬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .stApp {
        background-image: linear-gradient(120deg, #fdfbfb 0%, #ebedee 100%);
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    div[role="radiogroup"] label > div:first-child {
        background-color: #E0E0E0 !important;
        border: 1px solid #999 !important;
    }
    div[role="radiogroup"] label[data-checked="true"] > div:first-child {
        background-color: #FF4B4B !important;
        border-color: #FF4B4B !important;
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.98);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
        padding: 30px 20px;
        text-align: center;
        margin-bottom: 30px;
    }
    
    .tag {
        background: #f0f2f6;
        padding: 5px 12px;
        border-radius: 15px;
        font-size: 13px;
        color: #555;
        border: 1px solid #ddd;
        display: inline-block;
        margin: 4px;
    }

    .custom-btn {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 100% !important;
        box-sizing: border-box;
        height: auto;
        padding: 0.55rem 0.75rem;
        background-color: #ffffff;
        color: rgb(49, 51, 63);
        border: 1px solid rgba(49, 51, 63, 0.2);
        border-radius: 0.5rem;
        text-decoration: none;
        font-weight: 400;
        font-size: 1rem;
        line-height: 1.6;
        margin-top: 0px; 
        transition: all 0.2s;
    }
    
    .download-tip {
        font-size: 13px;
        color: #28a745;
        text-align: center;
        margin-top: 8px;
        font-weight: 500;
    }
    
    div[data-testid="column"] { display: flex; align-items: center; }
</style>
""", unsafe_allow_html=True)

# --- 2. Session 初始化 ---
if 'page' not in st.session_state:
    params = st.query_params
    if "risk" in params and "eff" in params:
        try:
            st.session_state.risk_score = int(params["risk"])
            st.session_state.eff_score = int(params["eff"])
            st.session_state.page = 'result'
        except:
            st.session_state.page = 'cover'
            st.session_state.risk_score = 50
            st.session_state.eff_score = 50
    else:
        st.session_state.page = 'cover'
        st.session_state.risk_score = 50 
        st.session_state.eff_score = 50

# --- 3. 后端绘图逻辑 ---
def create_share_image(animal, emoji, archetype, desc, tags, footer_text):
    # 1. 清洗文案
    desc = desc.replace("**", "")
    footer_text = footer_text.replace("【", "").replace("】", "").replace("📊", "").strip()
    
    # 2. 定义画布 (1300高度)
    W, H = 750, 1300  
    
    colors = {
        "机智猫猫": {"bg": "#FFFBF0", "card_bg": "#FFFFFF", "accent": "#F4B400", "text": "#333"}, 
        "拆家二哈": {"bg": "#FFF0F0", "card_bg": "#FFFFFF", "accent": "#FF6B6B", "text": "#333"},
        "深海乌贼": {"bg": "#F5F9FF", "card_bg": "#FFFFFF", "accent": "#4D96FF", "text": "#333"},
        "囤囤仓鼠": {"bg": "#F4F4F5", "card_bg": "#FFFFFF", "accent": "#9CA3AF", "text": "#333"},
    }
    theme = colors.get(animal, colors["囤囤仓鼠"])
    
    img = Image.new('RGB', (W, H), color=theme['bg'])
    draw = ImageDraw.Draw(img)
    
    try:
        font_path = None
        search_list = ["font.ttc", "msyh.ttc", "msyh.ttf", "SimHei.ttf", "C:/Windows/Fonts/msyh.ttc"]
        for f in search_list:
            if os.path.exists(f):
                font_path = f
                break
        if font_path is None: return None

        # 字体定义
        f_h1 = ImageFont.truetype(font_path, 64)     
        f_type = ImageFont.truetype(font_path, 32)   
        f_tag = ImageFont.truetype(font_path, 28)    
        f_desc = ImageFont.truetype(font_path, 30)   
        f_stat = ImageFont.truetype(font_path, 28) 
        f_brand = ImageFont.truetype(font_path, 22)  
        f_scan = ImageFont.truetype(font_path, 20)
    except:
        return None

    # 绘制主卡片背景
    card_margin = 50
    card_box = [card_margin, 60, W-card_margin, H-50] 
    draw.rounded_rectangle(card_box, radius=40, fill=theme['card_bg'], outline=None)

    # ============================
    # ZONE A: 头部 (0 - 500px)
    # ============================
    img_assets = {
        "机智猫猫": "cat.png", "拆家二哈": "dog.png",
        "深海乌贼": "octopus.png", "囤囤仓鼠": "hamster.png",
    }
    animal_img_path = os.path.join("assets", img_assets.get(animal, "cat.png"))
    try:
        if os.path.exists(animal_img_path):
            animal_img = Image.open(animal_img_path).convert("RGBA")
            animal_img = animal_img.resize((220, 220), Image.LANCZOS)
            img.paste(animal_img, ((W-220)//2, 100), animal_img)
    except: pass

    draw.text(((W-draw.textlength(f"TYPE · {archetype}", font=f_type))/2, 350), f"TYPE · {archetype}", font=f_type, fill=theme['accent'])
    draw.text(((W-draw.textlength(animal, font=f_h1))/2, 410), animal, font=f_h1, fill="#333333")
    
    # ============================
    # ZONE B: 内容 (500px - 900px)
    # ============================
    current_y = 510
    total_w = sum([draw.textlength(t, font=f_tag) + 40 for t in tags]) + 15 * (len(tags)-1)
    cur_x = (W - total_w) / 2
    for t in tags:
        t_w = draw.textlength(t, font=f_tag)
        draw.rounded_rectangle([cur_x, current_y, cur_x+t_w+40, current_y+50], radius=12, fill=theme['bg'])
        draw.text((cur_x+20, current_y+8), t, font=f_tag, fill="#666")
        cur_x += t_w + 40 + 15

    current_y = 600
    lines = textwrap.wrap(desc, width=19) 
    for line in lines[:5]: 
        draw.text(((W-draw.textlength(line, font=f_desc))/2, current_y), line, font=f_desc, fill="#444444")
        current_y += 50

    # ============================
    # ZONE C: 底部铁板 (900px - End)
    # ============================
    footer_start_y = 900
    
    # 分割线
    draw.line((150, footer_start_y, W-150, footer_start_y), fill="#EEEEEE", width=2)
    
    # 数据统计 (暖心文案)
    draw.text(((W-draw.textlength(footer_text, font=f_stat))/2, footer_start_y + 30), footer_text, font=f_stat, fill="#666666")
    
    # 二维码
    qr_y = footer_start_y + 100
    qr_size = 150
    q_path = os.path.join("assets", "qrcode.png")
    if os.path.exists(q_path):
        try:
            q_img = Image.open(q_path).convert("RGBA").resize((qr_size, qr_size), Image.LANCZOS)
            img.paste(q_img, ((W-qr_size)//2, qr_y), q_img)
        except: pass
        
    # 扫码提示
    scan_text = "扫码发现你的摸鱼生物类型"
    draw.text(((W-draw.textlength(scan_text, font=f_scan))/2, qr_y + qr_size + 15), scan_text, font=f_scan, fill="#AAAAAA")
    
    # 品牌
    draw.text(((W-draw.textlength("Generated by 摸鱼生物鉴定所", font=f_brand))/2, H-70), "Generated by 摸鱼生物鉴定所", font=f_brand, fill="#DDDDDD")

    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=95)
    return buf.getvalue()

# --- 4. 逻辑控制 ---
def restart():
    st.query_params.clear() 
    st.session_state.page = 'cover'
    st.session_state.risk_score = 50
    st.session_state.eff_score = 50

def submit_q(idx, choice):
    s = st.session_state
    if idx == 1:
        if "C" in choice: s.risk_score += 10
        elif "B" in choice: s.risk_score += 5
        s.page = 'q2'
    elif idx == 2:
        if "C" in choice: s.eff_score += 10
        elif "B" in choice: s.eff_score -= 5
        s.page = 'q3'
    elif idx == 3:
        if "C" in choice: s.eff_score += 10
        elif "B" in choice: s.eff_score += 5
        elif "A" in choice: s.eff_score -= 10
        s.page = 'q4'
    elif idx == 4:
        if "C" in choice: s.risk_score += 10
        elif "B" in choice: s.risk_score += 5
        s.page = 'q5'
    elif idx == 5:
        if "C" in choice: s.risk_score += 10
        elif "B" in choice: s.risk_score += 5
        elif "A" in choice: s.risk_score -= 5
        s.page = 'q6'
    elif idx == 6:
        if "C" in choice: s.eff_score += 5
        elif "B" in choice: s.eff_score += 2
        elif "A" in choice: s.eff_score -= 5
        s.page = 'q7'
    elif idx == 7:
        if "C" in choice: s.risk_score += 5
        elif "B" in choice: s.risk_score += 2
        s.page = 'q8'
    elif idx == 8:
        if "C" in choice: s.eff_score += 10
        elif "A" in choice: s.eff_score -= 5
        s.page = 'result'
        st.query_params["risk"] = s.risk_score
        st.query_params["eff"] = s.eff_score

# --- 5. 页面渲染 ---
if st.session_state.page == 'cover':
    st.title("🧬 摸鱼生物鉴定所")
    st.warning("⚠️ 微信/QQ内请点击右上角(...)选择【在浏览器打开】以获得最佳体验。")
    st.markdown("<div style='text-align:center; color:#999;'>V11.2 最终完整版</div><br>", unsafe_allow_html=True)
    with st.container():
        st.info("💡 这是一个关于“如何在内卷中优雅存活”的科学评估。")
        st.button("🚀 开始深度鉴定", on_click=lambda: st.session_state.update(page='q1'), type="primary", use_container_width=True)

elif st.session_state.page.startswith('q'):
    q_num = int(st.session_state.page[1])
    
    # === 全量题目文本 (Full Text) ===
    questions = {
        1: ("Q1. 老板突然在你身后出现，你的第一反应是？", 
            ["A. 惊慌失措，鼠标乱晃，甚至关掉了正常的工作窗口", 
             "B. 极其淡定，我本来就在干正事（或者装得像在干正事）", 
             "C. 主动出击：“老板，刚好有个Idea想跟您碰一下...”"]),
             
        2: ("Q2. 你最常用的摸鱼方式是？", 
            ["A. 纯物理闪避：厕所遁、楼下便利店、拿快递", 
             "B. 屏幕伪装术：把小说/视频窗口缩小到只有巴掌大", 
             "C. 科技狠活：写脚本自动跑任务，或者用 副屏/iPad 玩耍"]),
             
        3: ("Q3. 摸了一天鱼，临近下班时的进度如何？", 
            ["A. 好像啥也没干，开始焦虑，准备加班或者编日报", 
             "B. 踩点完成了今日KPI，绝不给公司多送一分钟", 
             "C. 其实早就做完了，现在的“忙碌”全是演给别人看的"]),
             
        4: ("Q4. 冗长的复盘会上，大家都在甩锅，你在干嘛？", 
            ["A. 假装记笔记，其实在画画/写小说/放空", 
             "B. 疯狂点头，主打一个情绪价值，虽然没听懂", 
             "C. 玩手机，但能在被点名时精准复述上一句并抛出“抓手”"]),
             
        5: ("Q5. 你正戴着耳机摸鱼，同事突然拍你说“忙吗”？", 
            ["A. 吓一跳，马上摘耳机：“啊？怎么了？我没在忙...”", 
             "B. 慢慢摘下一只耳机，眉头紧锁，看着屏幕叹气：“有点急，你说。”", 
             "C. 指指屏幕，摆手示意“稍等”，演足两分钟才理他"]),
             
        6: ("Q6. 摸鱼的时候，你的内心状态接近于？", 
            ["A. 担惊受怕，总觉得背后有双眼睛，玩得不痛快", 
             "B. 心安理得，这就是我出卖灵魂后的“精神补偿”", 
             "C. 极度兴奋，感觉自己在薅资本主义羊毛，甚至想笑"]),
             
        7: ("Q7. 你的办公桌上有防窥屏膜吗？", 
            ["A. 没有，我的屏幕向全宇宙敞开", 
             "B. 有，这是打工人的基本素养", 
             "C. 不需要，我的座位在角落/我是背靠墙的神位"]),
             
        8: ("Q8. 如果明天发了一笔横财，你还会来公司摸鱼吗？", 
            ["A. 绝对不来，立马离职奔赴旷野", 
             "B. 会来，主要是为了以此为借口逃避家里的琐事", 
             "C. 会来，拿着工资干私活/搞副业，利用公司资源创业"]),
    }
    
    q_text, opts = questions[q_num]
    st.progress(q_num/8, text=f"鉴定进度 {q_num}/8")
    st.subheader(q_text)
    choice = st.radio("请选择：", opts, index=None, key=f"q{q_num}")
    if choice:
        st.button("✨ 生成深度报告" if q_num==8 else "下一题", on_click=lambda: submit_q(q_num, choice), type="primary", use_container_width=True)

elif st.session_state.page == 'result':
    with st.spinner('正在分析行为样本...'): time.sleep(0.5)
    risk, eff = st.session_state.risk_score, st.session_state.eff_score
    
    # 文案库 (暖心版)
    if risk >= 75 and eff >= 65:
        animal, emoji, archetype = "机智猫猫", "🐱", "战略型"
        tags = ["#职场战略家", "#长期主义", "#降维打击"]
        desc = "你是极少数能完美平衡生活与工作的长期主义者。你的大脑正在后台进行多线程运算，老板眼里的摸鱼，其实是你高效的能量管理。"
        footer_text = "全网仅有 5% 的人拥有这种【天赋】" # 稀缺
        color = "#FFD700"
    elif risk >= 75 and eff < 65:
        animal, emoji, archetype = "拆家二哈", "🐺", "创新型"
        tags = ["#气氛组", "#反内卷", "#创造性破坏"]
        desc = "你拥有令人羡慕的强大心理素质。你的摸鱼其实是一种创造性的破坏，你是团队里防止大家因为过度内卷而崩溃的调节阀。"
        footer_text = "你的反内卷精神与 15% 的人产生【共鸣】" # 共鸣
        color = "#FF6347"
    elif risk < 75 and eff >= 65:
        animal, emoji, archetype = "深海乌贼", "🦑", "效能型"
        tags = ["#隐形冠军", "#深度工作", "#结果导向"]
        desc = "你是深度工作的践行者。你不需要表演忙碌，因为你的单位时间产出极高。你像乌贼一样喷出墨汁，只是为了守护一片属于自己的心流净土。"
        footer_text = "你是职场中 20% 的【隐形守护者】" # 身份
        color = "#4169E1"
    else:
        animal, emoji, archetype = "囤囤仓鼠", "🐹", "韧性型"
        tags = ["#懂事崩", "#责任感过载", "#真实打工人"]
        desc = "说实话，你可能是职场里最懂事的人。你之所以摸鱼时感到不安，是因为你的责任心太强了。这并不是你的错，而是环境太嘈杂。请把摸鱼当成是给自己的一次充电，你值得被温柔对待。"
        footer_text = "你并不孤单，全网 60% 的伙伴与你【站在一起】" # 陪伴
        color = "#888888"

    tags_html = "".join([f'<div class="tag">{t}</div>' for t in tags])
    card_html = f"""
<div class="glass-card">
<div style="color: {color}; font-weight: 900; letter-spacing: 2px; margin-bottom: 10px;">{archetype}</div>
<div class="animal-emoji">{emoji}</div>
<h1 style="color: #333; margin: 0;">{animal}</h1>
<div class="tag-container">{tags_html}</div>
<p style="font-size: 14px; line-height: 1.6; color: #444; margin: 20px 0;">{desc}</p>
<div style="border-top: 1px solid #eee; padding-top: 15px; font-size: 12px; color: #888;">
📊 {footer_text}
</div>
</div>
"""
    st.markdown(card_html, unsafe_allow_html=True)

    st.markdown("### 📸 保存与分享")
    st.warning("⚠️ 如果在微信/QQ内无法下载，请点击右上角(...)选择【在浏览器打开】")

    col1, col2 = st.columns(2)
    with col1:
        img_bytes = create_share_image(animal, emoji, archetype, desc, tags, footer_text)
        if img_bytes:
            st.download_button("📥 下载海报", data=img_bytes, file_name=f"摸鱼鉴定_{animal}.jpg", mime="image/jpeg", use_container_width=True)
            st.markdown('<div class="download-tip">✅ 图片已生成，请去浏览器下载</div>', unsafe_allow_html=True)
        else: st.warning("资源缺失")

    with col2:
        share_text = urllib.parse.quote(f"我是 {animal}！我的职场属性是【{archetype}】。快来测：https://moyu-test.app")
        weibo_url = f"http://service.weibo.com/share/share.php?title={share_text}"
        st.markdown(f"""<a href="{weibo_url}" target="_blank" class="custom-btn">🔥 分享到微博</a>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True) 
    st.divider()
    st.button("🔄 再测一次", on_click=restart, use_container_width=True)