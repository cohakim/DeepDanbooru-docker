import os
import glob
import yaml
import util

# md5: <tags> を出す
target = os.environ['TARGET']
root_dir = os.path.join('/', 'dataset', target)

# キャラクター定義を読み込む
with open(f'{root_dir}/definition.yml') as file:
  definition = yaml.safe_load(file)
DEFINITION_TRIGGER_WORD         = definition['trigger_word']
DEFINITION_CHARACTERISTICS_TAGS = definition['tag']['characteristics']
DEFINITION_COMMON_TAGS          = definition['tag']['common']
DEFINITION_EXCLUDE_TAGS         = definition['tag']['exclude']

# キャプションファイルの一覧を取得
files = glob.glob(f'{root_dir}/**/*.txt', recursive=True)

# 出力用のキャプション生成
caption = None
for file in files:
  # キャプションファイルからタグセットを取得
  base_tags = [tag.strip() for tag in open(file, encoding='utf-8').read().split(',')]
  # キャラクター定義からCHARACTERISTICS_TAGS（学習対象となるタグ）を取得
  characteristics_tags = util.deep_get(DEFINITION_CHARACTERISTICS_TAGS, os.path.dirname(file).replace(f'{root_dir}/', ''))

  # タグセットからCHARACTERISTICS_TAGSを削除したリストを作成（削除することで学習対象になる）
  caption = [tag for tag in base_tags if tag not in characteristics_tags]
  # COMMON_TAGSを追加
  for tag in reversed(DEFINITION_COMMON_TAGS):
    caption.insert(0, tag)
  # EXCLUDE_TAGSを削除
  for tag in reversed(DEFINITION_EXCLUDE_TAGS):
    caption.remove(tag)
  # TRIGGER_WORDを追加
  caption.insert(0, DEFINITION_TRIGGER_WORD)

  # ノーマライズ
  caption = [tag.replace('_', ' ') for tag in caption]

  # 出力
  key = os.path.splitext(file.replace(f'{root_dir}/', ''))[0]
  value = ', '.join(caption)
  print(f'{key}: {value}')
