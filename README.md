# SAVE MODEL NOW

- This is Extension for [AUTOMATIC1111's Stable Diffusion Web UI](https://github.com/AUTOMATIC1111/stable-diffusion-webui)
- AUTOMATIC1111 氏の StableDiffusion 用 Web UI のための、拡張機能です

## Feature
- Save model, which currently loaded. / 現在ロードされているモデルを、そのまま保存します

## Spec
- Save type is `.safetensors` only. / 保存は `safetensors` 形式になります
- Model data may be limited as `half` if no `no-half` option. / `no-half` 関連のオプションがセットされていない場合、モデルデータは `half` になっている場合があります. (as-is)

## 以下、未確認
- CLIP change してる場合、入れ替わったまま保存される ... はず (未確認)
- VAE も入替えてたら、入替えたので保存される ... はず (未確認)
