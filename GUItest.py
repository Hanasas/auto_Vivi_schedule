import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFont  

background_color = {
    'r': 235 ,
    'g': 235 ,
    'b': 241 
}

not_stream_background_color = {
    'r': 22 ,
    'g': 22 ,
    'b': 24 
}
"""
title_color = {
    'r': 49,
    'g': 49,
    'b': 57
}
"""
title_color = (49,49,57)
content_color = (138,137,153)
time_background_color = (235,153,57)
not_stream_string_color = (255,255,255)

title_single = [
    (285, 104),
    (285,240),
    (285,376),
    (285,513),
    (285,649),
    (285,784),
    (285,920)
]

content_single = [
    (287,143),
    (287,278),
    (287,414),
    (287,549),
    (287,686),
    (287,820),
    (287,954)
]

mask_single = [
    {
        'left':(270,96),
        'right':(588,171) # 318,75
    },
    {
        'left':(270,232),
        'right':(588,307)
    },
    {
        'left':(270,367),
        'right':(588,442)
    },
    {
        'left':(270,503),
        'right':(588,578)
    },
    {
        'left':(270,639),
        'right':(588,714)
    },
    {
        'left':(270,775),
        'right':(588,850)
    },
    {
        'left':(270,912),
        'right':(588,987)
    }
]

time_mask_single = [
    {
        'left':(666,96),
        'right':(811,171) # 145
    },
    {
        'left':(666,232),
        'right':(811,307)
    },
    {
        'left':(666,367),
        'right':(811,442)
    },
    {
        'left':(666,503),
        'right':(811,578)
    },
    {
        'left':(666,639),
        'right':(811,714)
    },
    {
        'left':(666,775),
        'right':(811,850)
    },
    {
        'left':(666,912),
        'right':(811,987)
    }
]

mask_not_stream = [
    {
        'left':(448,123),
        'right':(665,137)
    },
    {
        'left':(448,259),
        'right':(665,273)
    },
    {
        'left':(448,395),
        'right':(665,409)  #14
    },                     #61
    {
        'left':(448,531),
        'right':(665,545)
    },
    {
        'left':(448,667),
        'right':(665,681)
    },
    {
        'left':(448,803),
        'right':(665,817)
    },
    {
        'left':(448,938),
        'right':(665,952)
    }
]

not_stream_string = [
    (446,124),
    (446,260),
    (446,395),
    (446,530),
    (446,666),
    (446,801),
    (446,936)
]

CST_background = [
    {
        'left':(782,125),
        'right':(823,141) 
    },
    {
        'left':(782,261),
        'right':(823,277) 
    },
    {
        'left':(782,397),
        'right':(823,413) 
    },
    {
        'left':(782,532),
        'right':(823,548) 
    },
    {
        'left':(782,668),
        'right':(823,684) 
    },
    {
        'left':(782,803),
        'right':(823,819) 
    },
    {
        'left':(782,939),
        'right':(823,955) 
    }
]

CST_delta = (8,0.5)
time_delta = (-72.6,0)

class WorkScheduleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("工作日程安排")

        self.entries = []
        self.schedule = {}
        self.image_path = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        self.days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_periods = ['第一播', '第二播（如果有）']

        # 上传图片按钮
        tk.Button(self.root, text='上传图片', command=self.upload_image).grid(row=0, column=0, pady=1)
        # 显示图片路径的标签
        self.image_label = tk.Label(self.root, textvariable=self.image_path)
        self.image_label.grid(row=0, column=1, pady=10)

        for i, day in enumerate(self.days):
            frame = tk.Frame(self.root)
            frame.grid(row=i+1, column=0, padx=5, pady=5)
            
            self.entries.append([])
            
            for period in day_periods:
                inner_frame = tk.Frame(frame)
                inner_frame.grid(row=0, column=day_periods.index(period), padx=5)
                
                self.entries[-1].append({
                    'work_status': tk.BooleanVar(value=True if period == '第二播（如果有）' else False),  # Default afternoon as rest
                    'title': tk.StringVar(),
                    'content': tk.StringVar(),
                    'time': tk.StringVar()
                })
                
                self.entries[-1][-1]['work_status'].trace_add('write', lambda name, index, mode, var=self.entries[-1][-1]['work_status'], idx=(i, day_periods.index(period)): self.toggle_entry(idx))
                
                tk.Label(inner_frame, text=day + " " + period).grid(row=0, column=0, sticky='w')
                
                chk_work = tk.Checkbutton(inner_frame, text="休息", variable=self.entries[-1][-1]['work_status'])
                chk_work.grid(row=0, column=1, sticky='w')
                
                self.entries[-1][-1]['title_entry'] = tk.Entry(inner_frame, textvariable=self.entries[-1][-1]['title'], state=tk.NORMAL)
                self.entries[-1][-1]['content_entry'] = tk.Entry(inner_frame, textvariable=self.entries[-1][-1]['content'], state=tk.NORMAL)
                self.entries[-1][-1]['time_entry'] = tk.Entry(inner_frame, textvariable=self.entries[-1][-1]['time'], state=tk.NORMAL)
                    
                tk.Label(inner_frame, text='标题').grid(row=1, column=0, sticky='w')
                self.entries[-1][-1]['title_entry'].grid(row=1, column=1)
                
                tk.Label(inner_frame, text='内容').grid(row=2, column=0, sticky='w')
                self.entries[-1][-1]['content_entry'].grid(row=2, column=1)
                
                tk.Label(inner_frame, text='时间 (CST)').grid(row=3, column=0, sticky='w')
                self.entries[-1][-1]['time_entry'].grid(row=3, column=1)

        tk.Button(self.root, text='确定', command=self.save_schedule).grid(row=len(self.days)+1, column=0, pady=10)
        tk.Button(self.root, text='退出', command=root.quit).grid(row=len(self.days)+1, column=1, pady=10)

    def toggle_entry(self, idx):
        i, j = idx
        if self.entries[i][j]['work_status'].get():
            for entry in ['title', 'content', 'time']:
                self.entries[i][j][entry + '_entry'].config(state=tk.DISABLED)
        else:
            for entry in ['title', 'content', 'time']:
                self.entries[i][j][entry + '_entry'].config(state=tk.NORMAL)

    def upload_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image_path.set(file_path)

    def save_schedule(self):
        self.schedule.clear()  # Clear existing schedule
        for i, day in enumerate(self.days):
            self.schedule[day] = {'first': {}, 'second': {}}
            for j, period in enumerate(['first', 'second']):
                work_status = self.entries[i][j]['work_status'].get()
                title = self.entries[i][j]['title'].get()
                content = self.entries[i][j]['content'].get()
                time = self.entries[i][j]['time'].get()
                self.schedule[day][period] = {
                    'work_status': not work_status,
                    'title': title,
                    'content': content,
                    'time': time
                }
        
        image = Image.open(self.image_path.get())
        image.resize((1920,1080))
        draw = ImageDraw.Draw(image)
        for i in range(0,7):
            day = self.days[i]
            if self.schedule[day]['first']['work_status'] == False and self.schedule[day]['second']['work_status'] == False:# 不播
                rectangle_position = [mask_not_stream[i]['left'],mask_not_stream[i]['right']]   
                rectangle_color = (not_stream_background_color['r'], not_stream_background_color['g'], not_stream_background_color['b'])   
                draw.rectangle(rectangle_position, fill=rectangle_color)

                # 定义字符串的位置、内容和颜色，以及字体和大小  
                text_position = not_stream_string[i]
                text_content = "外 出 探 险"
                text_color = not_stream_string_color
                font_path = 'test.ttf'
                title_size = 16
                # 加载字体  
                font = ImageFont.truetype(font_path, title_size)
                # 在图片上绘制字符串  
                draw.text(text_position, text_content, fill=text_color, font=font)

            elif self.schedule[day]['first']['work_status'] == True and self.schedule[day]['second']['work_status'] == True:# 双播
                print("shuangbo")
            else:# 单播  
                rectangle_position = [mask_single[i]['left'],mask_single[i]['right']]   
                rectangle_color = (background_color['r'], background_color['g'], background_color['b'])   
                draw.rectangle(rectangle_position, fill=rectangle_color)

                rectangle_position2 = [time_mask_single[i]['left'],time_mask_single[i]['right']]
                rectangle_color2 = (background_color['r'], background_color['g'], background_color['b'])   
                draw.rectangle(rectangle_position2, fill=rectangle_color2)

                # 定义字符串的位置、内容和颜色，以及字体和大小  
                text_position = title_single[i]
                text_content = self.schedule[day]['first']['title']
                text_color = title_color  
                font_path = 'test.ttf'   
                title_size = 29 
                # 加载字体  
                font = ImageFont.truetype(font_path, title_size)  
                # 在图片上绘制字符串  
                draw.text(text_position, text_content, fill=text_color, font=font)

                # 定义字符串的位置、内容和颜色，以及字体和大小  
                text_position = content_single[i]
                text_content = self.schedule[day]['first']['content']
                text_color = title_color  
                font_path = 'test.ttf'
                title_size = 20
                # 加载字体  
                font = ImageFont.truetype(font_path, title_size)  
                # 在图片上绘制字符串  
                draw.text(text_position, text_content, fill=text_color, font=font)

                # 画 CST标志
                CST_rounded = [CST_background[i]['left'],CST_background[i]['right']]
                CST_background_color = time_background_color   
                draw.rounded_rectangle(CST_rounded, fill=CST_background_color, outline=(0, 0, 0), width=0, radius=3)
                # 定义字符串的位置、内容和颜色，以及字体和大小  
                text_position2 = (CST_background[i]['left'][0] + CST_delta[0],CST_background[i]['left'][1] + CST_delta[1])
                text_content = "CST"
                text_color = not_stream_string_color
                font_path = 'time_medium.otf'
                title_size = 15
                # 加载字体  
                font = ImageFont.truetype(font_path, title_size)  
                # 在图片上绘制字符串  
                draw.text(text_position2, text_content, fill=text_color, font=font)
                # 定义字符串的位置、内容和颜色，以及字体和大小  
                text_position = (CST_background[i]['left'][0] + time_delta[0],CST_background[i]['left'][1] + time_delta[1])
                text_content = self.schedule[day]['first']['time']
                text_color = title_color  
                font_path = 'time_medium.otf'   
                title_size = 16
                # 加载字体  
                font = ImageFont.truetype(font_path, title_size)  
                # 在图片上绘制字符串  
                draw.text(text_position, text_content, fill=text_color, font=font)


        image.save('output.png')

if __name__ == "__main__":
    root = tk.Tk()
    app = WorkScheduleApp(root)
    root.mainloop()
