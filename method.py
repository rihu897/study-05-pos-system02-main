import pandas as pd
from os import path
import datetime
import sys

### 商品クラス
class Item:
    def __init__(self,item_code,item_name,price,stock):
        self.item_code=item_code    # 商品コード
        self.item_name=item_name    # 商品名
        self.price=int(price)       # 価格
        self.stock=int(stock)       # 在庫数

### オーダークラス
class Order:
    def __init__(self,item_master):
        self.item_order_list=[]         # オーダリスト（[0]:商品コード, [1]:個数）
        self.item_master=item_master    # 商品情報マスタ
    
    ## オーダリスト追加処理
    def addOrderList(self,item_code_list,number_list):
        # オーダリスト初期化
        self.item_order_list=[]
        # 商品の存在確認
        count = 0
        for item_code in item_code_list :
            existence = False
            for item in self.item_master :
                if item_code == item.item_code :
                    existence = True
            
            if existence :
                # 購入数が0ではない場合、オーダリストを更新する
                if int(number_list[count]) > 0 :
                    if len(self.item_order_list) > 0 :
                        flg = True
                        for order in self.item_order_list :
                            # 商品コードがすでにオーダリストに存在する場合
                            if order[0] == item_code :
                                # 個数を加算
                                order[1] += int(number_list[count])
                                flg = False
                                break
                        if flg :
                            # オーダを追加
                            self.item_order_list.append([item_code, int(number_list[count])])
                    else :
                        # オーダを追加
                        self.item_order_list.append([item_code, int(number_list[count])])
            count += 1

# main.pyから直接呼び出されるクラス
class Main:
    def __init__(self):
        self.item_master=[]         # 商品情報マスタ
        self.txt_list = []          # レシートファイル出力用リスト
        self.after_stock_list=[]    # 商品購入後の在庫情報リスト
        self.total = 0              # 合計金額
        self.csv_path = ""          # CSVファイルのパス

    ### 商品マスタ登録処理
    def regItemMaster(self,csv):
        # アイテムマスタ初期化
        self.item_master = []
        # CSVファイルを読み込み、データをリストに格納
        self.csv_path = csv
        df = pd.read_csv(self.csv_path, dtype=str, encoding='utf-8-sig').values.tolist()
        # 商品単位でインスタンスを作成し、アイテムマスタに格納
        for item in df :
            # item[0]:商品コード, [1]:商品名, [2]:価格, [3]:在庫数
            self.item_master.append(Item(item[0], item[1], item[2], item[3]))

    ### 商品リスト取得処理
    def getItemList(self):
        item_list = []
        for item in self.item_master :
            item_list.append([item.item_code, item.item_name, item.price, item.stock])
        return item_list

    ### 合計金額計算処理
    def calcTotal(self, order):
        # レシートファイル出力用リスト、合計金額初期化
        self.txt_list = ["--------------------"]
        self.total = 0
        # 商品一覧表示
        for order in order.item_order_list :
            order_item_code = order[0]
            order_number = order[1]
            # 商品コードが一致する商品を検索
            for item in self.item_master :
                if order_item_code == item.item_code :
                    # 商品単位の合計金額を計算
                    subtotal = item.price * order_number
                    # 合計金額を加算
                    self.total += subtotal
                    # レシートファイル出力用リスト更新
                    self.txt_list.append("{0} ¥{1} ({2}ｺ) ¥{3}".format(item.item_name, str(item.price), str(order_number), str(subtotal)))
        # レシートファイル出力用リスト更新
        self.txt_list.append("--------------------")
        self.txt_list.append("合計金額：¥{}".format(str(self.total)))

    ### 支払い処理
    def paymentProcess(self, money):
        if money >= self.total :
            # 支払い可能な場合おつりを計算
            change = money - self.total
            # レシートファイル用リスト更新
            self.txt_list.append("お預り：¥{}".format(str(money)))
            self.txt_list.append("おつり：¥{}".format(str(change)))
            return True
        else :
            return "ERROR:お金が足りません！"

    ### レシートファイル出力処理
    def createReceiptFile(self):
        dt_now = datetime.datetime.now()
        receipt_path = path.dirname(__file__) + "/receipt/{}.txt".format(dt_now.strftime("%Y%m%d_%H%M%S"))
        receipt = open(receipt_path, "w", encoding="utf-8")
        for txt in self.txt_list :
            receipt.write(txt + '\n')
        receipt.close()
        return "レシートファイルを出力しました。({})".format(receipt_path)
        
    ### 在庫確認処理
    def itemStockCheck(self, item_code_list, number_list):
        # オーダリスト登録処理呼び出し
        order = Order(self.item_master)
        order.addOrderList(item_code_list, number_list)
        # 在庫確認
        self.after_stock_list =  []
        for item_order in order.item_order_list :
            for item in self.item_master :
                # オーダリストと商品情報マスタの商品コードが一致した場合
                if item_order[0] == item.item_code :
                    # 在庫を減らして一時ファイルへ格納
                    after_stock = item.stock - item_order[1]
                    # 在庫が不足していなかった場合、一時ファイルを商品購入後の在庫情報リストに格納
                    if after_stock >= 0 :
                        self.after_stock_list.append([item_order[0], after_stock])
                    else :
                        return "ERROR:「{}」の在庫が不足しています。".format(item.item_name)
        # すべての在庫が足りていた場合、Orderクラスのインスタンスを返却
        return order

    ### 在庫更新処理
    def itemStockUpdate(self):
        # 商品購入後の在庫情報を反映した商品情報リストを作成
        after_item_info = []
        for item in self.item_master :
            flg = True
            for after_stock in self.after_stock_list :
                if item.item_code == after_stock[0] :
                    after_item_info.append([item.item_code,item.item_name,item.price,after_stock[1]])
                    flg = False
                    break
            if flg :
                after_item_info.append([item.item_code,item.item_name,item.price,item.stock])

        # データフレームを作成し、商品購入後の商品情報リストを格納
        df = pd.DataFrame(after_item_info,columns=["item_code","item_name","price","stock"])
        # CSVファイルを出力
        df.to_csv(self.csv_path, index=False)