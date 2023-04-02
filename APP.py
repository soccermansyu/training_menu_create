import streamlit as st

def main():
    st.title("ランニングの練習メニュー作成アプリ")

    # フォームの作成
    with st.form(key='my_form'):
        st.write('自己ベスト (hh:mm:ss)')
        best_time = st.text_input('best_time', value='00:00:00')
        
        st.write('年齢')
        age = st.number_input('age', min_value=0, max_value=None, value=0, step=1)
        
        st.write('練習頻度')
        freq = st.selectbox('freq', ['1回/週', '2回/週', '3回/週', '4回/週', '5回/週', '6回/週'])
        
        submitted = st.form_submit_button('作成')

    # メニューの作成
    if submitted:
        st.write('トレーニングメニュー')
        st.write(f'自己ベスト: {best_time}')
        st.write(f'年齢: {age}')
        st.write(f'練習頻度: {freq}')

        week = ['月', '火', '水', '木', '金', '土', '日']
        if freq == '1回/週':
            off_days = ['月', '火', '水', '木', '金']
        elif freq == '2回/週':
            off_days = ['月', '水', '日']
        elif freq == '3回/週':
            off_days = ['火', '木', '日']
        elif freq == '4回/週':
            off_days = ['火', '木', '金']
        elif freq == '5回/週':
            off_days = ['火', '金']
        else:
            off_days = ['月']

        off = []
        for day in off_days:
            off.append(week.index(day))

        st.write(f'OFF日: {", ".join(off_days)}')

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
                else:
                    st.write(f'{week[i]}: OFF')


if __name__ == '__main__':
    main()
