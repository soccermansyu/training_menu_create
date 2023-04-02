import streamlit as st

def main():
    st.title("ランニングの練習メニュー作成アプリ")

    # フォームの作成
    with st.form(key='my_form'):
        st.write('自己ベスト (hh:mm:ss)')
        best_time = st.text_input('best_time', value='00:00:00')

        st.write('年齢')
        age = st.number_input('age', min_value=0, max_value=None, value=0, step=1)

        st.write('種目')
        event = st.selectbox('event', ['5000m', '10000m', 'ハーフマラソン', 'フルマラソン'])

        st.write('練習頻度')
        freq = st.selectbox('freq', ['1回/週', '2回/週', '3回/週', '4回/週', '5回/週', '6回/週'])

        # すべての入力ができているかチェック
        if best_time == '00:00:00' or age == 0 or event == '' or freq == '':
            st.warning('すべての入力が必要です')
            submitted = False
        else:
            # 送信ボタンを追加する
            submitted = st.form_submit_button('作成')

    # メニューの作成
    if submitted:
        st.write('トレーニングメニュー')
        st.write(f'自己ベスト: {best_time}')
        st.write(f'年齢: {age}')
        st.write(f'種目: {event}')
        st.write(f'練習頻度: {freq}')

        week = ['月', '火', '水', '木', '金', '土', '日']
        if freq == '1回/週':
            off = [0, 1, 2, 3, 4, 6]
        elif freq == '2回/週':
            off = [0, 1, 3, 4, 6]
        elif freq == '3回/週':
            off = [1, 3, 4, 6]
        elif freq == '4回/週':
            off = [1, 3, 4]
        elif freq == '5回/週':
            off = [1, 5]
        else:
            off = [0]

        st.write('OFF日: ' + ', '.join([week[i] for i in off]))

        st.write('トレーニングスケジュール')
        for i in range(7):
            if i in off:
                st.write(f'{week[i]}: OFF')
            elif i == 2:  # ペース走
                st.write(f'{week[i]}: ペース走, 設定ペース3:30/km, 20min')
            elif i == 6:  # ロングラン
                st.write(f'{week[i]}: ロングラン, 設定ペース4:10/km, 90min')
            else:
                st.write(f'{week[i]}: Jog, 設定ペース4:30/km, 60min')

if __name__ == '__main__':
    main()
