import eel
import desktop
import method

# htmlファイルのディレクトリ
app_name="html"
# htmlファイル名
end_point="index.html"
# ウィンドウのサイズ
size=(500,800)
# インスタンス
main = method.Main()

## 商品登録処理
@ eel.expose
def regItem(csv):
    # 商品マスタ登録処理呼び出し
    main.regItemMaster(csv)
    # 商品リスト取得処理呼び出し
    item_list = main.getItemList()
    # 商品一覧表示処理呼び出し
    eel.displayItemList(item_list)

## 精算処理
@eel.expose
def payOff(item_code_list, number_list):
    # 在庫数確認処理呼び出し
    result = main.itemStockCheck(item_code_list, number_list)
    if type(result) is str :
        eel.displayAlert(result)
    else :
        # 合計金額計算処理呼び出し
        main.calcTotal(result)
        # 精算結果表示処理呼び出し
        eel.displayPayOffResult(main.txt_list)

## 支払い処理
@eel.expose
def payment(money):
    # 支払い処理呼び出し
    result = main.paymentProcess(int(money))
    if type(result) is str :
        eel.displayAlert(result)
    else :
        # 精算結果表示処理呼び出し
        eel.displayPayOffResult(main.txt_list)
        # レシートファイル出力処理呼び出し後、アラートを表示
        alert_txt = main.createReceiptFile()
        eel.displayAlert(alert_txt)
        # 在庫更新処理呼び出し
        main.itemStockUpdate()


# 画面生成処理呼び出し
desktop.start(app_name,end_point,size)
