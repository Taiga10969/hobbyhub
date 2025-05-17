# Python＋Pygame で作るテトリス

`tetris.py` を例に、Python と Pygame を使ったテトリスの仕組みを一から解説します。実際に手を動かしながら、ゲームの基本構造や描画・ロジックの流れを理解しましょう。

---

## 1. 前提と環境構築

### 1.1 前提条件
- Python 3.6 以上  
- `pygame` ライブラリ  
- 基本的な Python 文法・リスト操作の理解

### 1.2 Python バージョン管理（pyenv） 

### 1.3 仮想環境の作成（venv）
```
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
pip install --upgrade pip
pip install pygame
```

---

## 2. プロジェクト構成

```
tetris/  
├── tetris.py    # ゲーム本体  
└── lecture.md   # この講義資料  
```

---

## 3. コード全体の概要

`tetris.py` は大きく以下のセクションで構成されています。

1. 定数・テトリミノ定義  
2. `Piece` クラス  
3. ユーティリティ関数  
   - グリッド生成: `create_grid`  
   - 形状変換: `convert_shape_format`  
   - 衝突判定: `valid_space`, `check_lost`  
   - ライン消去: `clear_rows`  
4. 描画関数  
   - グリッド線: `draw_grid`  
   - 次ピース表示: `draw_next_shape`  
   - メインウィンドウ描画: `draw_window`  
5. メインループ: `main()`  

---

## 4. テトリミノの定義

各テトリミノは 5×5 の文字列パターンで回転バリエーションを持ちます。

```python:path/to/tetris.py
# shapes = [S, Z, I, O, J, L, T]
# shape_colors = [(0,255,0), …, (128,0,128)]
```

- `'0'` がブロック本体、`.` は空白
- `shapes` と `shape_colors` を対応させて色を設定

---

## 5. グリッドとロックポジション

```python:path/to/tetris.py
def create_grid(locked_positions={}):
    grid = [[(0,0,0) for _ in range(10)] for _ in range(20)]
    for (x,y), color in locked_positions.items():
        grid[y][x] = color
    return grid
```

- 10 列×20 行の二次元リスト
- `locked_positions` に固定済みブロックの座標と色が保持される

---

## 6. 形状の変換と衝突判定

### 6.1 convert_shape_format
```python
def convert_shape_format(piece):
    # 回転状態に合わせて '0' の座標リストを返す
```

- 5×5 パターン内の `'0'` 座標を、ゲーム座標系に変換  
- オフセット `(-2,-4)` で中心合わせ

### 6.2 valid_space / check_lost
```python
def valid_space(piece, grid):
    # grid が空きなら True
def check_lost(positions):
    # y<1 の固定ブロックがあればゲームオーバー
```

- 壁や他ブロックとの重なりを判定

---

## 7. ライン消去

```python
def clear_rows(grid, locked):
    # 埋まった行を削除し、上の行を下にシフト
```

- 削除した行数に応じてスコア計算（例: 1行=10点）

---

## 8. 描画関数

### 8.1 draw_grid
```python
def draw_grid(surface, grid):
    # グリッド線を描画
```

### 8.2 draw_next_shape
```python
def draw_next_shape(piece, surface):
    # 画面右側に次のテトリミノを表示
```

### 8.3 draw_window
```python
def draw_window(surface, grid, score=0):
    surface.fill((0,0,0))
    # ブロック描画 → 枠線 → タイトル・スコア
```

- 描画順序で文字や枠が隠れないように工夫

---

## 9. メインループ

```python:path/to/tetris.py
def main():
    pygame.init()
    win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    current_piece = get_shape()
    next_piece    = get_shape()
    fall_time = 0

    while True:
        fall_time += clock.get_rawtime()
        clock.tick()
        if fall_time/1000 > fall_speed:
            # 自動落下処理
        for event in pygame.event.get():
            # 入力・終了処理
        # ピース描画・固定・クリア・スコア更新
        draw_window(...)
        draw_next_shape(...)
        pygame.display.update()
        if check_lost(...): break
    pygame.quit()
```

- `clock.tick()` で毎フレームのタイミング制御
- キー入力による移動・回転
- 自動落下と衝突判定

---

## 10. 実行方法

```bash
source .venv/bin/activate
python tetris.py
```

---

## 11. 演習課題

1. 壁キック（回転時にはみ出しを補正）を実装  
2. ハードドロップ（スペースキーで一気に下まで落とす）  
3. レベルシステム（消去行数に応じて `fall_speed` を上げる）  
4. BGM／効果音の追加  
5. ハイスコア記録機能  

自分なりの改造を加えながら、テトリスの仕組みを深く理解しましょう！  