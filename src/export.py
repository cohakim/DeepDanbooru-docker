import os
import glob
import yaml
import util

# md5: <tags> を出す
target = os.environ['TARGET']
root_dir = os.path.join('/', 'training_data', target)

# キャラクター定義を読み込む
definition = None
with open(f'{root_dir}/definitions.yml') as file:
  definition = yaml.safe_load(file)

# Danbooru評価タグファイルの一覧を取得
files = glob.glob(f'{root_dir}/**/*.txt', recursive=True)

# キャプション生成
caption = None
for file in files:
  # セクションを取得
  section = os.path.dirname(file).replace(f'{root_dir}/', '')
  # Danbooru評価ファイルからタグを取得
  tags_in_evaluation = [tag.strip() for tag in open(file, encoding='utf-8').read().split(',')]
  # キャラクター定義から学習対象となるタグを取得
  tags_in_definition = util.deep_get(definition['tag']['feature'], section)

  # 学習対象タグを反映（削除することで反映される）
  caption = [tag for tag in tags_in_evaluation if tag not in tags_in_definition]
  # キャプションに共通タグを追加
  for tag in reversed(definition['tag']['common']):
    caption.insert(0, tag)
  # キャプションから除外タグを削除
  for tag in reversed(definition['tag']['exclude']):
    caption.remove(tag)
  # キャプションにトリガーワードを追加
  caption.insert(0, definition['trigger_word'])

  # ノーマライズ
  caption = [tag.replace('_', ' ') for tag in caption]

  # 出力
  key = os.path.splitext(file.replace(f'{root_dir}/', ''))[0]
  value = ', '.join(caption)
  print(f'{key}: {value}')

