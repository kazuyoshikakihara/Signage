#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MeCab
import unittest

class Signage:
    """ 表記チェックのためのクラス

    使用例:
    signage = Signage()
    suspicious = signage.extract_suspicious(u'何かの文章')
    for (pronunciation, part_of_speech), suspicious_set in suspicious.iteritems():
        print "%s:%s %s" % (pronunciation, part_of_speech, ",".join(suspicious_set))
    """

    def _extract_signage(self, source):
        """
        extract_suspicious を補助するためのprivate function
        入力された文章を、以下のdict形式に変換する
        Args: 文章。複数の文章でも構わない。
        Returns:
            {(読み1, 品詞1): set([原形1, 原形2...]), (読み2, 品詞2)] set([原形3, 原形4...]),...}
            形式のdictで、読み、品詞が同じで原形の異なるデータの一覧を抽出したもの
        Raises:
            MeCab由来の例外が上がってくる可能性がある
        """
        # MeCabでのparse結果を取得
        mecab_tagger = MeCab.Tagger('-F%H¥n')
        mecab_parsed = mecab_tagger.parse(source.encode('utf8')).decode('utf8')
        # mecab_parsed は
        # 名詞,接尾,助数詞,*,*,*,羽,ワ,ワ
        # 助詞,格助詞,一般,*,*,*,に,ニ,ニ
        # 助詞,係助詞,*,*,*,*,は,ハ,ワ
        # ...
        # 形式で返ってくる

        # signage_dicは (読み, 品詞) をキーとし、文章中に見つかった原形のsetを値とする辞書
        # こちらの辞書に原形を格納していく
        signage_dic = {}
        for mecab_parsed_line in mecab_parsed.split(u'¥n'):
            fields = mecab_parsed_line.split(u',')

            # EOSや数字の場合
            if len(fields) < 8:
                continue

            part_of_speech = fields[0] # 品詞
            infinitive = fields[6] # 原形
            pronunciation = fields[7] # 読み

            # 表記ゆれのチェックをする意味がない品詞の場合
            if part_of_speech in [u'判定詞', u'助詞', u'助動詞', u'記号']:
                continue

            # signage_dicに読み、品詞、原形を追加
            pronunciation_part_key = (pronunciation, part_of_speech)
            signage_dic.setdefault(pronunciation_part_key, set()).add(infinitive)

        # 結果を返す
        return signage_dic

    def extract_suspicious(self, source):
        """
        入力された文章を元に、表記ゆれの可能性のある読み、品詞を返すfunction
        Args: 文章。複数の文章でも構わない。
        Returns: (読み, 品詞)をキーとし、原形のセット(原形は２種類以上)を値とした辞書
        """
        signage_dic = self._extract_signage(source)

        # 同一の読み、品詞に対して原形が２種類以上あれば表記ゆれの可能性あり
        return {pronunciation_part_key: infinitives
                for pronunciation_part_key, infinitives
                in signage_dic.iteritems() if len(infinitives) > 1}

class TestSignage(unittest.TestCase):
    def test_extract_suspicious_signage(self):
        signage = Signage()
        suspicious = signage.extract_suspicious(u"庭には鳥がいる。裏庭には二羽とりがいる。")
        self.assertIsInstance(suspicious, dict)
        self.assertTrue(suspicious.has_key((u'トリ', u'名詞')))
        self.assertEqual(set([u'鳥', u'とり']), suspicious[(u'トリ', u'名詞')]) 

if __name__ == '__main__':
    unittest.main()
