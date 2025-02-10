# このプログラムは、pauseキーが押されたときに現在時刻をクリップボードにコピーし、貼り付けます。

import datetime
import pyperclip
from pynput import keyboard
from pynput.keyboard import Controller, Key
# キーボードのコントローラを設定
keyboard_controller = Controller()

# pauseキーが押されたときに実行される関数
def on_press(key):
    try:
        if key == keyboard.Key.pause:  # pauseキーが押された時
            # 現在時刻を取得
            current_time = datetime.datetime.now().strftime('%Y-%m-%d （%a） %H：%M')
            # 現在時刻をクリップボードにコピー
            pyperclip.copy(current_time)
            # クリップボードの内容を貼り付け
            keyboard_controller.press(Key.ctrl)
            keyboard_controller.press('v')
            keyboard_controller.release('v')
            keyboard_controller.release(Key.ctrl)
            #   print(f"Input: {current_time}")  # ログに表示
    except AttributeError:
        pass

# pauseキーを監視
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()