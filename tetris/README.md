# テトリス

Python と Pygame で実装したシンプルなテトリスゲームです。

## 特徴

- 7 種類のテトリミノ（I, O, T, S, Z, J, L）  
- ブロックの自動落下、左右移動、ソフトドロップ、回転  
- ライン消去とスコア計算  
- 次のピースのプレビュー表示  
- ゲームオーバー判定  

## 前提条件

- macOS / Linux / Windows  
- Python 3.6 以上（`pyenv` によるバージョン管理を推奨）  
- `pygame` ライブラリ  

## インストール

1. リポジトリをクローン  
   ```bash
   git clone <your-repo-url>
   cd tetris
   ```

2. (任意) `pyenv` で Python をインストール / 切り替え  
   ```bash
   pyenv install 3.10.7
   pyenv local 3.10.7
   ```

3. 仮想環境を作成  
   ```bash
   python -m venv .venv
   ```

4. 仮想環境を有効化  
   ```bash
   source .venv/bin/activate    # macOS / Linux
   .venv\Scripts\activate       # Windows (PowerShell)
   ```

5. 依存パッケージをインストール  
   ```bash
   pip install --upgrade pip
   pip install pygame
   ```

## 使い方

仮想環境を有効化した状態で、以下を実行します：

```bash
python tetris.py
```

### 操作方法

- ← / → : ピースを左右に移動  
- ↓      : ソフトドロップ（速く落とす）  
- ↑      : ピースを回転  
- ウィンドウの閉じるボタン または `Ctrl+C` : ゲーム終了  

## 開発

- 依存パッケージを固定するには：  
  ```bash
  pip freeze > requirements.txt
  ```
- `.venv/`、`__pycache__/` などの一時ファイルは `.gitignore` に追加すると便利です。  
