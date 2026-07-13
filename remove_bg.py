# -*- coding: utf-8 -*-
"""
一键去除角色图片白色背景
运行方式：python remove_bg.py
需要安装：pip install Pillow
"""
import os
import sys

try:
    from PIL import Image
except ImportError:
    print("正在安装 Pillow...")
    os.system(f"{sys.executable} -m pip install Pillow --break-system-packages -q")
    from PIL import Image

CHAR_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "characters")

def remove_white_bg(input_path, output_path=None):
    """去除图片白色背景，保留角色白色身体"""
    img = Image.open(input_path).convert("RGBA")
    data = img.getdata()
    new_data = []
    for r, g, b, a in data:
        # 纯白色 -> 完全透明
        if r > 235 and g > 235 and b > 235:
            new_data.append((r, g, b, 0))
        # 近白色 -> 半透明（平滑边缘）
        elif r > 210 and g > 210 and b > 210:
            brightness = (r + g + b) / 3
            alpha = max(0, min(255, int(255 * (brightness - 210) / 30)))
            new_data.append((r, g, b, alpha))
        else:
            new_data.append((r, g, b, a))

    img.putdata(new_data)

    if output_path is None:
        name, _ = os.path.splitext(input_path)
        output_path = name + ".png"

    img.save(output_path, "PNG")
    return output_path

def main():
    if not os.path.exists(CHAR_DIR):
        print(f"❌ 找不到 characters 文件夹: {CHAR_DIR}")
        return

    count = 0
    for filename in os.listdir(CHAR_DIR):
        filepath = os.path.join(CHAR_DIR, filename)
        if not os.path.isfile(filepath):
            continue

        name, ext = os.path.splitext(filename)
        ext_lower = ext.lower()

        # 处理 JPG/JPEG 和有白边的 PNG
        if ext_lower in ('.jpg', '.jpeg'):
            out_path = os.path.join(CHAR_DIR, name + ".png")
            print(f"  🔄 {filename} -> {name}.png")
            try:
                remove_white_bg(filepath, out_path)
                count += 1
                print(f"  ✅ 完成")
            except Exception as e:
                print(f"  ❌ 失败: {e}")
        elif ext_lower == '.png':
            # 检查 PNG 是否有白色背景
            try:
                img = Image.open(filepath).convert("RGBA")
                # 检查四个角的像素是否为白色
                corners = [img.getpixel((0,0)), img.getpixel((img.width-1,0)),
                          img.getpixel((0,img.height-1)), img.getpixel((img.width-1,img.height-1))]
                white_corners = sum(1 for r,g,b,a in corners if r > 230 and g > 230 and b > 230)
                if white_corners >= 2:
                    print(f"  🔄 {filename} (有白边)")
                    remove_white_bg(filepath)
                    count += 1
                    print(f"  ✅ 完成")
                else:
                    print(f"  ⏭️ {filename} (无白边，跳过)")
            except Exception as e:
                print(f"  ❌ {filename} 失败: {e}")

    print(f"\n✅ 共处理 {count} 张图片")
    print("现在刷新 DSE冲刺宝典.html 即可看到效果！")

if __name__ == "__main__":
    main()
