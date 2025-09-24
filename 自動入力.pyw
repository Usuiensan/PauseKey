# このプログラムは、pauseキーが押されたときに現在時刻をクリップボードにコピーし、貼り付けます。

import datetime
import pyperclip
import os
import sys
import tkinter as tk
from tkinter import messagebox
from pynput import keyboard
from pynput.keyboard import Controller, Key

# キーボードのコントローラを設定
keyboard_controller = Controller()

# エラーメッセージボックスを表示する関数
def show_error_message(title, message):
    # 隠しウィンドウを作成してメッセージボックスを表示
    root = tk.Tk()
    root.withdraw()  # メインウィンドウを隠す
    messagebox.showerror(title, message)
    root.destroy()

# 情報メッセージボックスを表示する関数
def show_info_message(title, message):
    root = tk.Tk()
    root.withdraw()  # メインウィンドウを隠す
    messagebox.showinfo(title, message)
    root.destroy()

# 設定ファイルから時刻フォーマットを読み込む関数
def load_time_format():
    try:
        # PyInstallerでexe化された場合とスクリプト実行の場合を考慮
        if hasattr(sys, '_MEIPASS'):
            # PyInstallerでexe化された場合、実行ファイルのディレクトリを取得
            script_dir = os.path.dirname(sys.executable)
        else:
            # 通常のスクリプト実行の場合
            script_dir = os.path.dirname(os.path.abspath(__file__))
        
        config_file = os.path.join(script_dir, 'time_format.txt')
        
        with open(config_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        # コメント行と空行を除外してフォーマットを取得
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                return line
                
    except FileNotFoundError:
        show_error_message("設定ファイルエラー", 
                          "設定ファイル 'time_format.txt' が見つかりません。\n"
                          "デフォルトフォーマットを使用します。\n\n"
                          "フォーマット: %Y-%m-%d （%a） %H：%M")
    except Exception as e:
        show_error_message("設定ファイルエラー", 
                          f"設定ファイルの読み込みエラーが発生しました。\n"
                          f"エラー内容: {e}\n\n"
                          f"デフォルトフォーマットを使用します。")
    
    # デフォルトフォーマット
    return '%Y-%m-%d （%a） %H：%M'

# 起動時に時刻フォーマットを読み込み
time_format = load_time_format()

# 起動確認メッセージを表示
try:
    print("正常に起動しました。pauseキーを押すと、現在時刻が入力されます。")
except ValueError as e:
    show_error_message("起動エラー", 
                      f"時刻フォーマットエラーのため、デフォルトフォーマットを使用します。\n"
                      f"エラー内容: {e}\n\n"
                      f"time_format.txt を確認してください。")
    time_format = '%Y-%m-%d （%a） %H：%M'

# pauseキーが押されたときに実行される関数
def on_press(key):
    try:
        if key == keyboard.Key.pause:  # pauseキーが押された時
            try:
                # 現在時刻を設定ファイルのフォーマットで取得
                current_time = datetime.datetime.now().strftime(time_format)
                # 現在時刻をクリップボードにコピー
                pyperclip.copy(current_time)
                # クリップボードの内容を貼り付け
                keyboard_controller.press(Key.ctrl)
                keyboard_controller.press('v')
                keyboard_controller.release('v')
                keyboard_controller.release(Key.ctrl)
                #   print(f"Input: {current_time}")  # ログに表示
            except ValueError as e:
                # 時刻フォーマットエラーの場合
                show_error_message("時刻フォーマットエラー", 
                                 f"時刻フォーマットが正しくありません。\n"
                                 f"エラー内容: {e}\n\n"
                                 f"現在のフォーマット: {time_format}\n"
                                 f"time_format.txt を確認してください。")
            except Exception as e:
                # その他のエラー
                show_error_message("実行エラー", 
                                 f"自動入力中にエラーが発生しました。\n"
                                 f"エラー内容: {e}")
    except AttributeError:
        pass

# pauseキーを監視
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
