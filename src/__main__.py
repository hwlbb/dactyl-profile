import os
import argparse
import shutil
from . import main

def clean():
    """清理生成的文件"""
    paths = [
        'tests/output/*.scad',
        'output/*.scad',
        'dist',
        '*.egg-info'
    ]
    for path in paths:
        try:
            if '*' in path:
                import glob
                for f in glob.glob(path):
                    os.remove(f)
            elif os.path.exists(path):
                shutil.rmtree(path)
        except Exception as e:
            print(f"清理 {path} 时出错: {e}")

def main_cli():
    parser = argparse.ArgumentParser(description='Dactyl Keyboard Generator')
    parser.add_argument('--watch', '-w', action='store_true',
                       help='监视文件变化并自动重新生成')
    parser.add_argument('--clean', '-c', action='store_true',
                       help='清理生成的文件')
    
    args = parser.parse_args()
    
    if args.clean:
        clean()
        return
    
    # 确保output目录存在
    os.makedirs('output', exist_ok=True)
    
    # 生成键盘
    main.run()
    print('生成完成: output/*.scad')
    
    if args.watch:
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler
        import time
        
        class ChangeHandler(FileSystemEventHandler):
            def __init__(self):
                self.last_modified = 0
                self.cooldown = 1.0  # 冷却时间（秒）
                
            def on_modified(self, event):
                if str(event.src_path).endswith('.py'):
                    current_time = time.time()
                    if current_time - self.last_modified > self.cooldown:
                        print('检测到文件变化，重新生成...')
                        main.run()
                        print('生成完成: output/*.scad')
                        self.last_modified = current_time
        
        observer = Observer()
        handler = ChangeHandler()
        observer.schedule(handler, 'src', recursive=True)
        observer.start()
        
        try:
            print('监视文件变化中... (按 Ctrl+C 停止)')
            while observer.is_alive():
                observer.join(1)
        except KeyboardInterrupt:
            print('\n正在停止监视...')
            observer.stop()
            observer.join()
            print('已停止监视')

if __name__ == '__main__':
    main_cli() 