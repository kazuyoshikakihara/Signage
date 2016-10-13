# Signate

## 表記ゆれチェッカ
日本語の文章でありがちな「引越」と「引っ越し」など、表記のゆれをチェックする。

##  事前に必要なもの

* mecab(utf8で動作するもの)
* utf8形式のmecab用辞書（例: mecab-ipadic-utf8 ubuntuの場合）
* mecab-python3(python 2.7でもこのモジュールは動作する)

## 使用例

```
import signage

signage = signage.Signage()
suspicious = signage.extract_suspicious(u'庭には鶏がいます。裏庭にもニワトリがいます。')
for (pronunciation, part_of_speech), suspicious_set in suspicious.iteritems():
    print u"%s:%s %s" % (pronunciation, part_of_speech, ",".join(suspicious_set))
```

出力:
```
ニワトリ:名詞 ニワトリ,鶏
```
