import pyxel
import random
import time

class EnglishWordGame:
    def __init__(self):
        pyxel.init(200, 200)
        pyxel.load("resource.pyxres")
        pyxel.caption = "Word Game"
        # ゲームの状態を初期化
        self.current_word_index = 0  # 現在の単語インデックス
        self.correct_letters = 0  # 正しい文字の数
        self.incorrect_attempts = 0  # 不正解の回数
        self.score = 0  # スコア
        self.hearts = 5  # ハート（ライフ）の数
        self.three_times = 0  # 連続正解の回数
        self.is_started = False  # ゲームが始まったかどうか
        self.space_cooldown = 30
        # 問題となる単語リスト
        self.word_list = [
            ("apple", "ringo"), ("dog", "inu"), ("cat", "neko"), 
            ("house", "ie"), ("car", "kuruma"), ("book", "hon"), 
            ("school", "gakkou"), ("mountain", "yama"), 
            ("river", "kawa"), ("fish", "sakana")
        ]

        # 現在の質問と回答を選択
        self.current_question = random.choice(self.word_list)
        self.answer = self.current_question[0]

        # タイマー関連の変数
        self.remaining_time = 60
        self.last_time = time.time()

        # ゲームオーバーの状態
        self.is_game_over = False

        # 選択された文字と選択肢
        self.selected_letter = None
        self.selected_letters = []  # 選択された文字を保存するリスト
        self.current_options = self.generate_options()  # 現在の質問の選択肢

        # マウスを有効にする
        pyxel.mouse(True)

        # Pyxelのメインループを開始
        pyxel.run(self.update, self.draw)


    def update(self):

        # クールダウンタイマーを更新
        if self.space_cooldown > 0:
            self.space_cooldown -= 1

        if not self.is_started:
            # エンターキーが押されたときの処理
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.is_started = True
                self.remaining_time = 60
                pyxel.playm(0, loop=True)
                pyxel.play(3,7,loop=False)

            return


        # スペースキーが押されたときの処理をクールダウンが0の場合に限定する
        if pyxel.btnp(pyxel.KEY_SPACE):
            if self.space_cooldown == 0:
                self.space_cooldown = 30  # クールダウン期間を設定
                self.remaining_time -= 5
                self.next_question()

        # ゲームオーバーでない場合のみ更新
        if not self.is_game_over:
            current_time = time.time()
            if current_time - self.last_time >= 1.0:
                self.remaining_time -= 1
                self.last_time = current_time

            if self.remaining_time <= 0 or self.incorrect_attempts >= 5:
                self.is_game_over = True
                pyxel.stop(0)
                pyxel.stop(1)
                pyxel.stop(2)
                pyxel.play(3,7,loop=False)
                return

            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.selected_letter = self.get_selected_letter(pyxel.mouse_x, pyxel.mouse_y)
                if self.selected_letter:
                    self.check_letter()

    def draw(self):
        # 画面をクリアする
        pyxel.cls(0)

        # ゲームがまだ開始されていない場合の表示
        if not self.is_started:
            # エンターキーでゲーム開始の指示を表示
            pyxel.text(70, 70, "Start with ENTER KEY", 8)
            # マウスクリックとスペースキーの操作説明を表示
            pyxel.text(80, 110, f"MOUSE CLICK: SELECT", 7)
            pyxel.text(80, 130, f"SPACE KEY: SKIP", 7)
            return

        # ゲームオーバーでない場合の表示
        if not self.is_game_over:
            # ゲームのタイトルを表示
            pyxel.text(70, 10, "Word Game", 7)

            # スコア、残り時間、エラー数、ライフの状態を表示
            pyxel.text(70, 30, f"Score: {self.score}", 7)
            pyxel.text(70, 50, f"Time: {self.remaining_time}", 7)
            pyxel.text(70, 70, f"Errors: {self.incorrect_attempts}/5", 7)
            pyxel.text(70, 90, f"Life: {'|' * self.hearts}", 7)

            # 現在の質問（日本語）を表示
            pyxel.text(70, 120, f"{self.current_question[1]}", 7)

            # ユーザーが選択した文字を表示（コメントアウトされている）
            # if self.selected_letter:
            #     pyxel.text(70, 150, self.selected_letter, 7)

            # 回答の進行状況を表示（選択された文字またはアンダーバー）
            for i in range(len(self.answer)):
                if i < len(self.selected_letters):
                    pyxel.text(70 + i * 10, 170, self.selected_letters[i], 7)
                else:
                    pyxel.text(70 + i * 10, 170, "_", 7)

            # 選択肢を描画する
            self.draw_options()

        # ゲームオーバーの場合の表示
        else:
            # ゲームオーバーと最終スコアを表示
            pyxel.text(70, 70, "Game Over", 8)
            pyxel.text(70, 90, f"Final Score: {self.score}", 7)


    def check_letter(self):
        # 選択された文字をリストに追加
        self.selected_letters.append(self.selected_letter)

        # 全ての文字が入力されたかを確認
        if len(self.selected_letters) == len(self.answer):
            # 入力された回答を評価
            if "".join(self.selected_letters).lower() == self.answer.lower():
                # 正解の場合の処理
                pyxel.play(3,6,loop=False)
                self.score += 50
                self.next_question()
                self.three_times += 1
            else:
                # 不正解の場合の処理
                pyxel.play(3,5,loop=False)
                self.score -= 30
                self.remaining_time -= 10
                self.incorrect_attempts += 1
                self.reset_current_question()
            
            if self.three_times > 2:
                self.remaining_time += 10
                self.score += 100
                self.three_times = 0
        else:
            # 次の文字の選択肢を生成する
            self.current_options = self.generate_options()


    def reset_current_question(self):
        self.correct_letters = 0
        self.selected_letter = None
        self.selected_letters = []  # 選択された文字をリセット
        self.current_options = self.generate_options()  # 選択肢を再生成


    # 正解の文字とその他のランダムな文字を含む選択肢を生成
    def generate_options(self):
        # 現在の文字位置を取得
        current_position = len(self.selected_letters)
        correct_letter = self.answer[current_position] if current_position < len(self.answer) else None

        # 選択肢を生成
        other_letters = [char for char in "abcdefghijklmnopqrstuvwxyz" if char != correct_letter]
        random.shuffle(other_letters)
        options = [correct_letter] + other_letters[:3]
        random.shuffle(options)
        return options


    def draw_options(self):
        for i, option in enumerate(self.current_options):
            x = 50 + i * 30  # ボタンのX座標
            y = 140  # ボタンのY座標
            width = 20  # ボタンの幅
            height = 10  # ボタンの高さ
            pyxel.rect(x, y, width, height, 13)
            pyxel.text(x + 5, y + 2, option, 7)

    def get_selected_letter(self, x, y):

        for i in range(4):
            btn_x = 50 + i * 30
            btn_y = 140
            btn_width = 20
            btn_height = 10
            # ボタンの範囲内かどうかを確認
            if btn_x <= x <= btn_x + btn_width and btn_y <= y <= btn_y + btn_height:
                return self.current_options[i]
        return None

    def next_question(self):
        self.current_word_index += 1
        if self.current_word_index >= len(self.word_list):
            self.current_word_index = 0

        self.current_question = self.word_list[self.current_word_index]
        self.answer = self.current_question[0]

        self.correct_letters = 0
        self.selected_letter = None
        self.selected_letters = []  # 選択された文字を保存するリストをリセット
        self.current_options = self.generate_options() # 新しい質問の選択肢を生成


    def next_question(self):
        # 現在の質問インデックスを1つ進める
        self.current_word_index += 1

        # 質問リストの末尾に達した場合、インデックスをリストの始まりに戻す
        if self.current_word_index >= len(self.word_list):
            self.current_word_index = 0
        # 新しい質問を設定
        self.current_question = self.word_list[self.current_word_index]
        self.answer = self.current_question[0]  # 正解の単語を設定

        # 正解の文字数と選択された文字をリセット
        self.correct_letters = 0
        self.selected_letter = None
        self.selected_letters = []  # 選択された文字を保存するリストをリセット

        # 新しい質問の選択肢を生成
        self.current_options = self.generate_options()



if __name__ == "__main__":
    EnglishWordGame()