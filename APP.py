import streamlit as st

def main():
    st.title("ランニングの練習メニュー作成アプリ")

    # フォームの作成
    with st.form(key='my_form'):
        st.write('自己ベスト')
        best_time = st.number_input('', min_value=0.0, max_value=None, value=0.0, step=0.01)
        
        st.write('年齢')
        age = st.number_input('', min_value=0, max_value=None, value=0, step=1)
        
        st.write('練習頻度')
        freq = st.selectbox('', ['1回/週', '2回/週', '3回/週', '4回/週', '5回/週', '6回/週', '毎日'])
        
        st.write('週間走行距離')
        distance = st.number_input('', min_value=0.0, max_value=None, value=0.0, step=0.01)
        
        st.write('目標レース距離')
        target_distance = st.number_input('', min_value=0.0, max_value=None, value=0.0, step=0.01)

        st.write('曜日のOFF設定')
        off_days = st.multiselect('', ['月', '火', '水', '木', '金', '土', '日'])
        
        submitted = st.form_submit_button('作成')  # Submitボタンを追加

    # メニューの作成
    if submitted:
        st.write('トレーニングメニュー')
        st.write(f'自己ベスト: {best_time}')
        st.write(f'年齢: {age}')
        st.write(f'練習頻度: {freq}')
        st.write(f'週間走行距離: {distance}')
        st.write(f'目標レース距離: {target_distance}')

        week = ['月', '火', '水', '木', '金', '土', '日']
        off = []
        for day in off_days:
            off.append(week.index(day))

        st.write('トレーニングスケジュール')
        for i in range(7):
            if i in off:
                st.write(f'{week[i]}: OFF')
            else:
                if i in [0, 2, 4, 6]:  # Jog
                    st.write(f'{week[i]}: Jog, 設定ペース4:30/km, 60min')
                elif i == 2:  # ペース走
                    st.write(f'{week[i]}: ペース走, 設定ペース3:30/km, 20min')
                elif i == 6:  # ロングラン
                    st.write(f'{week[i]}: ロングラン, 設定ペース4:10/km, 90min')
                else:  # OFF
                    st.write(f'{week[i]}: OFF')

if __name__ == '__main__':
    main()
