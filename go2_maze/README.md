# \# Go2 Maze Demo

# 

# Unitree Go2 quadruped robotをMuJoCo上で動作させ、迷路内の経路をA\*で計画してゴールへの到達を試みるシミュレーションデモです。

# 

# 歩行制御には外部のGo2 locomotion policyを利用し、迷路の経路計画とロボットへの移動指令を組み合わせています。迷路上方に固定したカメラを配置し、シミュレーション中のロボット・経路・深度情報などを確認できます。

# 

# > \*\*注意:\*\* このプロジェクトはシミュレーション上のデモです。実機Go2での動作や安全性を保証するものではありません。

# 

# \## 主な機能

# 

# \- MuJoCoによるUnitree Go2の物理シミュレーション

# \- 迷路環境の生成

# \- 上方視点カメラによる環境観測

# \- A\*によるスタートからゴールまでの経路計画

# \- 歩行ポリシーを利用したロボットの移動

# \- シミュレーション結果・経路計画の可視化

# \- OpenCVを利用したMP4動画出力

# 

# \## 動作環境

# 

# 開発環境の目安:

# 

# \- Windows 10 / 11

# \- Python 3.12

# \- MuJoCo Python package

# \- NumPy

# \- OpenCV-Python（動画出力を利用する場合）

# \- 歩行ポリシーの実行に必要な追加パッケージ

# 

# GPU要件やパッケージの互換性は、利用する歩行ポリシーと実行環境に依存します。上記は完全な互換性を保証する環境一覧ではありません。

# 

# \## セットアップ

# 

# \### 1. リポジトリを取得

# 

# ```powershell

# git clone https://github.com/Reidoru/PAI2026\_advanced1\_FinalAssignment.git

# cd PAI2026\_advanced1\_FinalAssignment

# ```

# 

# \### 2. Python仮想環境を作成

# 

# ```powershell

# py -3.12 -m venv .venv

# ```

# 

# 仮想環境を有効化する場合:

# 

# ```powershell

# .\\.venv\\Scripts\\Activate.ps1

# ```

# 

# PowerShellの実行ポリシーによって有効化できない場合は、ポリシーを変更せず、`.venv\\Scripts\\python.exe` を直接実行できます。

# 

# \### 3. Pythonパッケージをインストール

# 

# ```powershell

# .\\.venv\\Scripts\\python.exe -m pip install --upgrade pip

# .\\.venv\\Scripts\\python.exe -m pip install -r requirements.txt

# ```

# 

# \### 4. 歩行制御リポジトリを取得

# 

# 歩行ポリシーなどの外部ファイルは、このリポジトリには含めていません。元のリポジトリを別途取得してください。

# 

# ```powershell

# git clone https://github.com/FERBIN12/go2-quadruped-locomotion-mujoco.git

# ```

# 

# このプロジェクトのスクリプトが想定する配置・ファイル名と、取得したリポジトリの構成が一致していることを確認してください。外部リポジトリ側の更新によって構成や実行方法が変わる可能性があります。

# 

# \## 実行

# 

# 利用可能な引数を確認:

# 

# ```powershell

# .\\.venv\\Scripts\\python.exe go2\_demo.py --help

# ```

# 

# 歩行動作の確認:

# 

# ```powershell

# .\\.venv\\Scripts\\python.exe go2\_walk\_and\_maze.py --mode walk

# ```

# 

# 迷路走行デモ:

# 

# ```powershell

# .\\.venv\\Scripts\\python.exe go2\_walk\_and\_maze.py --mode maze

# ```

# 

# 実際のオプションは、アップロードした `go2\_walk\_and\_maze.py` の `argparse` 定義が優先されます。上記コマンドが手元の最新版と異なる場合は `--help` の表示に従ってください。

# 

# \## 出力

# 

# 実行結果は通常 `outputs/` 以下に保存されます。出力内容は実行モードや指定オプションによって異なります。生成された動画・画像・ログなどは再生成可能な実行成果物のため、通常はGitリポジトリに含めません。

# 

# \## ディレクトリ構成

# 

# ```text

# go2-maze-demo/

# ├── go2\_demo.py

# ├── README.md

# ├── requirements.txt

# ├── .gitignore

# └── THIRD\_PARTY\_LICENSES.md

# ```

# 

# 歩行制御リポジトリや実行結果は別途取得・生成します。

# 

# \## ライセンス・クレジット

# 

# 外部プロジェクトおよびソフトウェアの参照先とライセンス情報は \[`THIRD\_PARTY\_LICENSES.md`](THIRD\_PARTY\_LICENSES.md) を確認してください。

# 

# このリポジトリ自身のコードに適用するライセンスは、リポジトリの所有者が別途明示する必要があります。第三者のコード・モデル・アセットのライセンスは、それぞれの権利者および配布元の条件に従います。

