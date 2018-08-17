from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont

#TakaoEXゴシック体を利用する場合
registerFont(TTFont('TakaoExGothic','TakaoExGothic.ttf'))

# キャンバスと出力ファイルの初期化。
retCanvas = canvas.Canvas('/media/PDF/Output.pdf')
retCanvas.saveState()

pdfWidth=240.0*mm
pdfHeight=290.0*mm
retCanvas.setPageSize((pdfWidth,pdfHeight))

retCanvas.setFont("TakaoExGothic", 16)

#x,yにテキスト追加
retCanvas.drawString(x, y, text)

#x,yから右寄せでテキスト追加
retCanvas.drawRightString(x, y, text)

#名前からして中央寄せなんだと思うけど、
#ドキュメントに記載があったが手元の環境では、
#メソッドが見当たらず…使えない。なぜ？
retCanvas.drawCentredString(x, y, text)

textobject = canvas.beginText(x, y) #座標を指定する。
textobject.setTextOrigin(x, y) #もしくは座標をこう指定する。この場合、beginTextでは、引数は無し。

#使用するフォント・サイズの指定
textobject.setFont("TakaoExGothic", 8)
#テキストの設定
textobject.textLines('''
ここにテキストを記述する。
改行も反映される様子。
ただし、自動改行はされないっぽい。なんか設定あるのかな。。。
''')
#キャンバスへの追加
canvas.drawText(textobject)
