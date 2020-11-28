$(function() {
    // CSVファイル選択時の処理
    const csv = document.getElementById("item_info_csv")
    csv.addEventListener('blur', () => {
        var csv_path = csv.value;
        // ファイル拡張子確認
        if ('.csv' != csv_path.slice(-4)) {
            // アラートを表示して処理を終了
            alert("ERROR：ファイルの拡張子が不正です。");
            return;
        }

        // 商品登録処理呼び出し
        eel.regItem(csv_path);
    });
    
    // フォーム数
    var count = 1;
    // 追加ボタンクリック時の処理
    const add = document.getElementById("add");
    add.addEventListener('click', () => {
        // フォームの追加
        var tr_form = '' +
        '<tr>' +
            '<td><input class="item_code" type="text" placeholder="商品コードを入力"></td>' +
            '<td><input class="number" type="number" min="0" value="0"></td>' +
        '</tr>';
        $(tr_form).appendTo($('#cart_item'));
        count++;
    });

    // 精算ボタンクリック時の処理
    const pay_off = document.getElementById("pay_off");
    pay_off.addEventListener('click', () => {
        // カートの情報を配列に格納
        var item_code_list = new Array(count);
        var number_list = new Array(count);
        for (let i = 0; i < count; i++) {
            item_code_list[i] = document.getElementsByClassName("item_code")[i].value
            number_list[i] = document.getElementsByClassName("number")[i].value
        }
        // 精算処理呼び出し
        eel.payOff(item_code_list, number_list);
    });

    // 決定ボタンクリック時の処理
    const decision = document.getElementById("decision");
    decision.addEventListener('click', () => {
        // 支払い処理呼び出し
        eel.payment(money.value);
        // 商品登録処理呼び出し
        var csv_path = document.getElementById("item_info_csv").value;
        eel.regItem(csv_path);
    });

    // 商品一覧表示処理
    eel.expose(displayItemList);
    function displayItemList(item_list) {
        // 商品一覧を削除
        $('#item_table').remove()
        // 商品一覧のHTML作成
        var item_list_html = "<table id='item_table'><tr><th>商品コード</th><th>商品名</th><th>価格</th><th>在庫数</th></tr>";
        for (let i = 0; i < item_list.length; i++) {
            item_list_html = item_list_html + "<tr><td>" + item_list[i][0] + "</td><td>" + item_list[i][1] + "</td><td>" + item_list[i][2] + "</td><td>" + item_list[i][3] + "</td></tr>";
        }
        item_list_html = item_list_html + "</table>";
        // 商品一覧を出力
        $(item_list_html).appendTo($('#item_list'));
    }
    
    // 精算結果表示処理
    eel.expose(displayPayOffResult);
    function displayPayOffResult(result_list) {
        var result = "";
        // 検索結果を表示用変数に追記
        for (let i = 0; i < result_list.length; i++) {
            result = result + result_list[i] + '\n';
        }
        // 結果出力
        display_box.innerHTML = result;
    }
    
    // アラート表示処理
    eel.expose(displayAlert)
    function displayAlert(txt) {
        alert(txt);
    }
});
