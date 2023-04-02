import streamlit as st
import pandas as pd

def main():
    st.title("ランニングの練習メニュー作成アプリ")

    # 入力フォームを作成
    st.write('種目')
    event = st.selectbox('event', ['5000m', '10000m', 'ハーフマラソン', 'フルマラソン'])
    
    st.write('自己ベスト (hh:mm:ss)')
    best_time = st.text_input('best_time', value='00:00:00')

    st.write('年齢')
    age = st.number_input('age', min_value=0, max_value=None, value=0, step=1)

    st.write('練習頻度')
    freq = st.selectbox('freq', ['3回/週', '4回/週', '5回/週', '6回/週', '7回/週'])

    # 追加: Easy Pace, Threshold Pace, Interval Pace の入力フォームを作成
    st.write('Easy Pace (/km) (m:ss)')
    easy_pace = st.text_input('easy_pace', value='0:00')
    
    st.write('Threshold Pace (/km) (m:ss)')
    threshold_pace = st.text_input('threshold_pace', value='0:00')
    
    st.write('Interval Pace (/km) (m:ss)')
    interval_pace = st.text_input('interval_pace', value='0:00')

    # すべての入力ができているかチェック
    if best_time == '00:00:00' or age == 0 or event == '' or freq == '' or easy_pace == '0:00' or threshold_pace == '0:00' or interval_pace == '0:00':
        st.warning('未入力の項目があります')
        submitted = False
    else:
        # 作成ボタンを押した時の処理を記述
        submitted = st.button('作成')

        # 追加: off リストを更新
        if freq == '3回/週':
            off = [1, 3, 4, 6]
        elif freq == '4回/週':
            off = [1, 3, 4]
        elif freq == '5回/週':
            off = [1, 5]
        elif freq == '6回/週':
            off = [0]            
        else:
            off = []

# メニューの作成
    if submitted:
        st.write(f'種目: {event}')
        st.write('トレーニングメニュー')
        st.write(f'自己ベスト: {best_time}')
        st.write(f'年齢: {age}')
        st.write(f'練習頻度: {freq}')

        # 追加: Easy Pace, Threshold Pace, Interval Pace の値を表示
        st.write(f'Easy Pace (/km): {easy_pace}')
        st.write(f'Threshold Pace (/km): {threshold_pace}')
        st.write(f'Interval Pace (/km): {interval_pace}')

        week = ['月', '火', '水', '木', '金', '土', '日']

        # 追加: off リストの値を表示

        off_days = 'OFF日: ' + ', '.join([week[i] for i in off])
        st.write(off_days)    

    # トレーニングスケジュールを作成
        df = pd.DataFrame(columns=['曜日', 'トレーニングメニュー'])
        for i in range(7):
            if i in off:
                menu = 'OFF'
            elif i == 2:  # ペース走
                menu = f'ペース走, 設定ペース{threshold_pace}/km, 20min'
            elif i == 5:  # ロングラン
                menu = f'ロングラン, 設定ペース{easy_pace}/km, 90min'
            else:
                menu = f'Jog, 設定ペース{easy_pace}/km, 60min'

            df = df.append({'曜日': week[i], 'トレーニングメニュー': menu}, ignore_index=True)

        # 表形式でトレーニングメニューを出力
        st.write(df)

                
if __name__ == '__main__':
    main()
