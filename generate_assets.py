import os
from PIL import Image, ImageDraw
import random

# 确保 assets 文件夹存在
if not os.path.exists("assets"):
    os.makedirs("assets")

def create_cat():
    # 画布：400x400，透明背景
    img = Image.new('RGBA', (400, 400), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 1. 耳朵 (三角形)
    draw.polygon([(60, 100), (140, 20), (180, 100)], fill="#F4B400") # 左耳
    draw.polygon([(220, 100), (260, 20), (340, 100)], fill="#F4B400") # 右耳
    
    # 2. 脸 (圆形)
    draw.ellipse((50, 50, 350, 350), fill="#FFD700")
    
    # 3. 眼睛
    draw.ellipse((110, 160, 140, 190), fill="#333")
    draw.ellipse((260, 160, 290, 190), fill="#333")
    
    # 4. 鼻子 (粉色小三角)
    draw.polygon([(180, 220), (220, 220), (200, 250)], fill="#FF6B6B")
    
    # 5. 胡须
    draw.line((50, 200, 100, 210), fill="#333", width=5)
    draw.line((50, 230, 100, 220), fill="#333", width=5)
    draw.line((300, 210, 350, 200), fill="#333", width=5)
    draw.line((300, 220, 350, 230), fill="#333", width=5)
    
    img.save("assets/cat.png")
    print("✅ 机智猫猫 生成完毕")

def create_dog():
    img = Image.new('RGBA', (400, 400), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 1. 耳朵 (耷拉的大耳朵)
    draw.ellipse((20, 100, 120, 250), fill="#CD5C5C")
    draw.ellipse((280, 100, 380, 250), fill="#CD5C5C")
    
    # 2. 脸
    draw.ellipse((50, 50, 350, 350), fill="#FF6347")
    
    # 3. 眼睛 (眼白+眼珠，二哈的眼神)
    draw.ellipse((100, 140, 160, 200), fill="#FFF")
    draw.ellipse((240, 140, 300, 200), fill="#FFF")
    draw.ellipse((125, 165, 145, 185), fill="#333") # 斗鸡眼
    draw.ellipse((255, 165, 275, 185), fill="#333")
    
    # 4. 嘴套 (白色区域)
    draw.ellipse((130, 220, 270, 320), fill="#FFF")
    
    # 5. 鼻子
    draw.ellipse((170, 230, 230, 270), fill="#333")
    
    img.save("assets/dog.png")
    print("✅ 拆家二哈 生成完毕")

def create_octopus():
    img = Image.new('RGBA', (400, 400), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 1. 脚 (画几个圆在下面)
    for i in range(4):
        draw.ellipse((60 + i*70, 250, 120 + i*70, 380), fill="#4169E1")
    
    # 2. 头 (大圆)
    draw.ellipse((50, 20, 350, 320), fill="#4D96FF")
    
    # 3. 眼睛 (大眼睛，看起来很聪明)
    draw.ellipse((100, 120, 160, 180), fill="#FFF")
    draw.ellipse((240, 120, 300, 180), fill="#FFF")
    draw.ellipse((130, 140, 150, 160), fill="#333")
    draw.ellipse((250, 140, 270, 160), fill="#333")
    
    # 4. 嘴巴 (吐墨汁的小嘴)
    draw.arc((180, 200, 220, 220), start=0, end=180, fill="#333", width=5)
    
    img.save("assets/octopus.png")
    print("✅ 深海乌贼 生成完毕")

def create_hamster():
    img = Image.new('RGBA', (400, 400), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 1. 耳朵 (圆耳朵)
    draw.ellipse((60, 40, 140, 120), fill="#A9A9A9")
    draw.ellipse((260, 40, 340, 120), fill="#A9A9A9")
    
    # 2. 身体
    draw.ellipse((50, 60, 350, 360), fill="#D3D3D3")
    
    # 3. 腮帮子 (囤东西的脸颊)
    draw.ellipse((40, 200, 120, 300), fill="#FFB6C1")
    draw.ellipse((280, 200, 360, 300), fill="#FFB6C1")
    
    # 4. 眼睛
    draw.ellipse((120, 160, 150, 190), fill="#333")
    draw.ellipse((250, 160, 280, 190), fill="#333")
    
    # 5. 门牙
    draw.rectangle((180, 260, 200, 290), fill="#FFF", outline="#999")
    draw.rectangle((200, 260, 220, 290), fill="#FFF", outline="#999")
    
    # 6. 鼻子
    draw.ellipse((190, 220, 210, 240), fill="#333")
    
    img.save("assets/hamster.png")
    print("✅ 囤囤仓鼠 生成完毕")

def create_dummy_qrcode():
    img = Image.new('RGB', (200, 200), color='white')
    draw = ImageDraw.Draw(img)
    def draw_finder(x, y):
        draw.rectangle((x, y, x+40, y+40), outline="black", width=5)
        draw.rectangle((x+10, y+10, x+30, y+30), fill="black")
    draw_finder(10, 10); draw_finder(150, 10); draw_finder(10, 150)
    for _ in range(50):
        x = random.randint(2, 18) * 10; y = random.randint(2, 18) * 10
        draw.rectangle((x, y, x+10, y+10), fill="black")
    img.save("assets/qrcode.png")
    print("✅ 示例二维码 生成完毕")

if __name__ == "__main__":
    print("🎨 正在绘制初代萌版素材...")
    create_cat()
    create_dog()
    create_octopus()
    create_hamster()
    create_dummy_qrcode()
    print("🎉 素材已重置！")