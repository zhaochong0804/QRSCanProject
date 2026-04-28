import os
from PIL import Image, ImageDraw, ImageFont

W, H = 2400, 1350

def ensure_dir(p):
    os.makedirs(p, exist_ok=True)

def load_font(size):
    candidates = [
        "/System/Library/Fonts/SFNS.ttf",
        "/System/Library/Fonts/SFNSDisplay.ttf",
        "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/PingFang.ttc",
    ]
    for c in candidates:
        try:
            return ImageFont.truetype(c, size)
        except:
            pass
    return ImageFont.load_default()

def create_canvas():
    img = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)
    return img, draw

def text_size(draw, text, font):
    bbox = draw.textbbox((0,0), text, font=font)
    return bbox[2]-bbox[0], bbox[3]-bbox[1]

def draw_title(draw, text):
    font = load_font(64)
    tw, th = text_size(draw, text, font)
    draw.text(((W-tw)//2, 40), text, fill=(0,0,0,255), font=font)

def draw_box(draw, xy, text, fill=(240,240,240,255), outline=(60,60,60,255), radius=20, padding=24, text_size_px=44):
    x1,y1,x2,y2 = xy
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=4)
    font = load_font(text_size_px)
    tw, th = text_size(draw, text, font)
    tx = x1 + (x2-x1-tw)//2
    ty = y1 + (y2-y1-th)//2
    draw.text((tx, ty), text, fill=(0,0,0,255), font=font)

def draw_arrow(draw, start, end, color=(60,60,60,255), width=8, head=24):
    x1,y1 = start
    x2,y2 = end
    draw.line((x1,y1,x2,y2), fill=color, width=width)
    dx, dy = x2-x1, y2-y1
    l = max(1, (dx*dx+dy*dy)**0.5)
    ux, uy = dx/l, dy/l
    hx, hy = x2 - ux*head, y2 - uy*head
    nx, ny = -uy, ux
    p1 = (x2, y2)
    p2 = (hx + nx*head*0.6, hy + ny*head*0.6)
    p3 = (hx - nx*head*0.6, hy - ny*head*0.6)
    draw.polygon([p1,p2,p3], fill=color)

def save(img, name):
    ensure_dir("figures")
    path = os.path.join("figures", name)
    img.save(path, format="PNG")

def fig1_system_architecture():
    img, draw = create_canvas()
    draw_title(draw, "图1 系统总体架构示意图")
    client = (120, 250, 520, 430)
    gateway = (580, 250, 980, 430)
    aggregator = (1040, 200, 1440, 380)
    renderer = (1040, 460, 1440, 640)
    bus = (1500, 250, 1900, 430)
    storage = (1960, 250, 2320, 430)
    draw_box(draw, client, "客户端/终端", fill=(200,226,255,255))
    draw_box(draw, gateway, "边缘网关", fill=(255,214,165,255))
    draw_box(draw, aggregator, "聚合服务", fill=(221,201,255,255))
    draw_box(draw, renderer, "渲染服务", fill=(195,245,200,255))
    draw_box(draw, bus, "消息中间件/CDN", fill=(180,240,240,255))
    draw_box(draw, storage, "存储/分析", fill=(210,210,210,255))
    draw_arrow(draw, (520,340), (580,340))
    draw_arrow(draw, (980,340), (1040,290))
    draw_arrow(draw, (980,340), (1040,580))
    draw_arrow(draw, (1440,290), (1500,340))
    draw_arrow(draw, (1440,580), (1500,340))
    draw_arrow(draw, (1900,340), (1960,340))
    draw_arrow(draw, (1500,430), (1440,580))
    draw_arrow(draw, (1500,430), (1440,290))
    draw_arrow(draw, (1900,340), (1440,580))
    draw_arrow(draw, (1900,340), (1440,290))
    save(img, "fig1_system_architecture.png")

def fig2_client_interaction_flow():
    img, draw = create_canvas()
    draw_title(draw, "图2 客户端投票交互与事件流程图")
    a=(180,260,640,380)
    b=(720,260,1180,380)
    c=(1260,260,1720,380)
    d=(180,500,640,620)
    e=(720,500,1180,620)
    f=(1260,500,1720,620)
    draw_box(draw, a, "用户触发投票", fill=(200,226,255,255))
    draw_box(draw, b, "位置与情绪选择", fill=(200,226,255,255))
    draw_box(draw, c, "本地节流/速率限制", fill=(255,214,165,255))
    draw_box(draw, d, "事件队列", fill=(221,201,255,255))
    draw_box(draw, e, "WebSocket/QUIC推送", fill=(180,240,240,255))
    draw_box(draw, f, "服务端聚合入口", fill=(221,201,255,255))
    draw_arrow(draw, (640,320), (720,320))
    draw_arrow(draw, (1180,320), (1260,320))
    draw_arrow(draw, (400,380), (400,500))
    draw_arrow(draw, (940,380), (940,500))
    draw_arrow(draw, (1500,380), (1500,500))
    draw_arrow(draw, (640,560), (720,560))
    draw_arrow(draw, (1180,560), (1260,560))
    save(img, "fig2_client_interaction_flow.png")

def fig3_aggregation_algorithm_flow():
    img, draw = create_canvas()
    draw_title(draw, "图3 聚合算法流程图")
    a=(160,240,720,360)
    b=(800,240,1360,360)
    c=(1440,240,2000,360)
    d=(160,500,720,620)
    e=(800,500,1360,620)
    f=(1440,500,2000,620)
    draw_box(draw, a, "滑动时间窗", fill=(221,201,255,255))
    draw_box(draw, b, "空间网格化", fill=(221,201,255,255))
    draw_box(draw, c, "核密度估计/扩散", fill=(221,201,255,255))
    draw_box(draw, d, "信誉权重与去噪", fill=(255,214,165,255))
    draw_box(draw, e, "归一化与阈值裁剪", fill=(255,214,165,255))
    draw_box(draw, f, "输出情绪密度矩阵", fill=(195,245,200,255))
    draw_arrow(draw, (720,300), (800,300))
    draw_arrow(draw, (1360,300), (1440,300))
    draw_arrow(draw, (440,360), (440,500))
    draw_arrow(draw, (1080,360), (1080,500))
    draw_arrow(draw, (1720,360), (1720,500))
    draw_arrow(draw, (720,560), (800,560))
    draw_arrow(draw, (1360,560), (1440,560))
    save(img, "fig3_aggregation_algorithm_flow.png")

def fig4_render_pipeline():
    img, draw = create_canvas()
    draw_title(draw, "图4 热力图渲染管线与色图映射示意")
    a=(160,260,720,380)
    b=(800,260,1360,380)
    c=(1440,260,2000,380)
    d=(160,520,720,640)
    e=(800,520,1360,640)
    f=(1440,520,2000,640)
    draw_box(draw, a, "情绪密度矩阵", fill=(195,245,200,255))
    draw_box(draw, b, "色图映射", fill=(221,201,255,255))
    draw_box(draw, c, "Alpha透明度控制", fill=(221,201,255,255))
    draw_box(draw, d, "与视频画面混合", fill=(200,226,255,255))
    draw_box(draw, e, "关键区域避让", fill=(255,214,165,255))
    draw_box(draw, f, "终端显示/多端适配", fill=(180,240,240,255))
    draw_arrow(draw, (720,320), (800,320))
    draw_arrow(draw, (1360,320), (1440,320))
    draw_arrow(draw, (440,380), (440,520))
    draw_arrow(draw, (1080,380), (1080,520))
    draw_arrow(draw, (1720,380), (1720,520))
    draw_arrow(draw, (720,580), (800,580))
    draw_arrow(draw, (1360,580), (1440,580))
    save(img, "fig4_render_pipeline.png")

def fig5_anti_fraud_quality():
    img, draw = create_canvas()
    draw_title(draw, "图5 反作弊与质量控制机制图")
    a=(160,260,620,380)
    b=(700,260,1160,380)
    c=(1240,260,1700,380)
    d=(1780,260,2240,380)
    e=(160,520,620,640)
    f=(700,520,1160,640)
    g=(1240,520,1700,640)
    h=(1780,520,2240,640)
    draw_box(draw, a, "速率限制", fill=(255,214,165,255))
    draw_box(draw, b, "信誉评分", fill=(255,214,165,255))
    draw_box(draw, c, "异常检测", fill=(255,214,165,255))
    draw_box(draw, d, "多账号关联", fill=(255,214,165,255))
    draw_box(draw, e, "降权处理", fill=(221,201,255,255))
    draw_box(draw, f, "隔离审查", fill=(221,201,255,255))
    draw_box(draw, g, "黑名单/封禁", fill=(221,201,255,255))
    draw_box(draw, h, "审计与回溯", fill=(221,201,255,255))
    draw_arrow(draw, (620,320), (700,320))
    draw_arrow(draw, (1160,320), (1240,320))
    draw_arrow(draw, (1700,320), (1780,320))
    draw_arrow(draw, (390,380), (390,520))
    draw_arrow(draw, (940,380), (940,520))
    draw_arrow(draw, (1470,380), (1470,520))
    draw_arrow(draw, (2010,380), (2010,520))
    save(img, "fig5_anti_fraud_quality.png")

def fig6_use_cases():
    img, draw = create_canvas()
    draw_title(draw, "图6 应用场景示例图")
    frame = (200, 240, W-200, H-120)
    draw.rounded_rectangle(frame, radius=30, fill=(245,245,245,255), outline=(120,120,120,255), width=4)
    font = load_font(40)
    draw.text((220, 250), "示例视频画面", fill=(0,0,0,255), font=font)
    draw.rectangle((320, 360, 720, 540), fill=(220,220,220,255), outline=(100,100,100,255), width=3)
    draw.text((330, 370), "人物/舞台区域", fill=(0,0,0,255), font=font)
    draw.rectangle((1680, 360, 2080, 540), fill=(220,220,220,255), outline=(100,100,100,255), width=3)
    draw.text((1690, 370), "目标/焦点区域", fill=(0,0,0,255), font=font)
    for cx, cy, r, col in [
        (560, 460, 120, (255,120,120,160)),
        (1900, 460, 140, (120,160,255,160)),
        (1100, 640, 100, (255,200,120,160)),
        (1400, 780, 150, (140,255,180,160)),
        (900, 860, 90, (255,160,220,160)),
    ]:
        draw.ellipse((cx-r, cy-r, cx+r, cy+r), fill=col, outline=None)
    legend_x = 220
    legend_y = H-180
    legends = [
        ("正向情绪", (255,120,120,160)),
        ("负向情绪", (120,160,255,160)),
        ("惊喜/高潮", (255,200,120,160)),
        ("赞同/支持", (140,255,180,160)),
        ("其他", (255,160,220,160)),
    ]
    lf = load_font(36)
    x = legend_x
    for name, col in legends:
        draw.rectangle((x, legend_y, x+60, legend_y+60), fill=col, outline=(80,80,80,255), width=2)
        draw.text((x+80, legend_y+10), name, fill=(0,0,0,255), font=lf)
        x += 360
    save(img, "fig6_use_cases_examples.png")

def main():
    fig1_system_architecture()
    fig2_client_interaction_flow()
    fig3_aggregation_algorithm_flow()
    fig4_render_pipeline()
    fig5_anti_fraud_quality()
    fig6_use_cases()

if __name__ == "__main__":
    main()

