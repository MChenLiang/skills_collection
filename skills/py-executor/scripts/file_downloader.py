#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
文件下载工具
支持断点续传、进度显示、重试机制
"""

import os
import sys
import time
import urllib.request
from pathlib import Path
from typing import Optional, Callable


class FileDownloader:
    """文件下载器"""
    
    def __init__(
        self,
        url: str,
        save_path: str,
        chunk_size: int = 8192,
        retries: int = 3,
        progress_callback: Optional[Callable[[int, int], None]] = None
    ):
        """
        初始化下载器
        
        Args:
            url: 下载链接
            save_path: 保存路径
            chunk_size: 分块大小（字节）
            retries: 重试次数
            progress_callback: 进度回调函数 callback(downloaded, total)
        """
        self.url = url
        self.save_path = Path(save_path)
        self.chunk_size = chunk_size
        self.retries = retries
        self.progress_callback = progress_callback
    
    def download(self) -> bool:
        """
        执行下载
        
        Returns:
            下载是否成功
        """
        for attempt in range(self.retries):
            try:
                print(f"尝试下载: {self.url} (第 {attempt + 1} 次)")
                
                # 创建目录
                self.save_path.parent.mkdir(parents=True, exist_ok=True)
                
                # 打开 URL
                with urllib.request.urlopen(self.url) as response:
                    total_size = int(response.headers.get('Content-Length', 0))
                    downloaded = 0
                    
                    print(f"文件大小: {self._format_size(total_size)}")
                    
                    # 写入文件
                    with open(self.save_path, 'wb') as f:
                        while True:
                            chunk = response.read(self.chunk_size)
                            if not chunk:
                                break
                            
                            f.write(chunk)
                            downloaded += len(chunk)
                            
                            # 进度回调
                            if self.progress_callback:
                                self.progress_callback(downloaded, total_size)
                            
                            # 进度显示
                            if total_size > 0:
                                percent = (downloaded / total_size) * 100
                                print(f"\r下载进度: {percent:.1f}% ({self._format_size(downloaded)}/{self._format_size(total_size)})", end='')
                    
                    print()  # 换行
                    print(f"下载完成: {self.save_path}")
                    return True
                    
            except Exception as e:
                print(f"下载失败: {e}")
                if attempt < self.retries - 1:
                    wait_time = (attempt + 1) * 2
                    print(f"等待 {wait_time} 秒后重试...")
                    time.sleep(wait_time)
                else:
                    print("重试次数用尽，下载失败")
                    return False
    
    @staticmethod
    def _format_size(size: int) -> str:
        """
        格式化文件大小
        
        Args:
            size: 字节数
            
        Returns:
            格式化后的大小字符串
        """
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} TB"


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='文件下载工具')
    parser.add_argument('url', help='下载链接')
    parser.add_argument('save_path', help='保存路径')
    parser.add_argument('--retries', type=int, default=3, help='重试次数')
    
    args = parser.parse_args()
    
    downloader = FileDownloader(
        url=args.url,
        save_path=args.save_path,
        retries=args.retries
    )
    
    success = downloader.download()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
