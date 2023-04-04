import streamlit as st
import pandas as pd

def main():
    st.title("ランニングの練習メニュー作成アプリケーション")

    # 入力フォームを作成
    st.write('種目')
    event = st.selectbox('event', ['5000m', '10000m', 'ハーフマラソン', 'フルマラソン'])
    
    st.write('自己ベスト (hh:mm:ss)')
    best_time = st.text_input('best_time', value='00:00:00')
    
    st.write('年齢')
    age = st.slider('age', min_value=10, max_value=80, value=30)

    st.write('練習頻度')
    freq = st.selectbox('freq', ['3回/週', '4回/週', '5回/週', '6回/週', '7回/週'])

    # 追加: Easy Pace, Moderate Pace, Threshold Pace, Interval Pace の入力フォームを作成
    st.write('Easy Pace (/km) (m:ss)')
    easy_pace = st.text_input('Easy_pace', value='0:00')
    
    st.write('Moderate Pace (/km) (m:ss)')
    moderate_pace = st.text_input('Moderate_pace', value='0:00')    
    
    st.write('Threshold Pace (/km) (m:ss)')
    threshold_pace = st.text_input('Threshold_pace', value='0:00')
    
    st.write('Interval Pace (/km) (m:ss)')
    interval_pace = st.text_input('Interval_pace', value='0:00')

    # すべての入力ができているかチェック
    if best_time == '00:00:00' or event == '' or freq == '' or easy_pace == '0:00' or moderate_pace == '0:00' or threshold_pace == '0:00' or interval_pace == '0:00':
        st.warning('未入力の項目があります')
        submitted = False
    else:
        # 作成ボタンを押した時の処理を記述
        submitted = st.button('作成')

        # 追加: off リストを更新
        if freq == '3回/週':
            off = [0, 1, 3, 5]
        elif freq == '4回/週':
            off = [0, 3, 4]
        elif freq == '5回/週':
            off = [0, 4]
        elif freq == '6回/週':
            off = [0]            
        else:
            off = []
    max_hr = int(207 - age * 0.7)
    easy_hr = int(max_hr * 0.65), int(max_hr * 0.74)
    moderate_hr = int(max_hr * 0.74), int(max_hr * 0.79)
    threshold_hr = int(max_hr * 0.8), int(max_hr * 0.88)
    interval_hr = int(max_hr * 0.9), int(max_hr * 1.0)

# メニューの作成
    if submitted:
        st.write(f'種目: {event}')
        st.write(f'自己ベスト: {best_time}')
        st.write(f'最大心拍数(HRmax): {max_hr}回/分')
        st.write(f'※最大心拍数(HRmax)の計算方法：207 - (年齢 × 0.7)')
        if freq == '4回/週':
            distance = '50'
        elif freq == '5回/週':
            distance = '65'
        elif freq == '6回/週':
            distance = '85'
        elif freq == '7回/週':
            distance = '110'
        else:
            distance = ''
        st.write(f'練習頻度: {freq}')
        st.write(f'週間走行距離目安: {distance}km/週')

        # 追加: Easy Pace, Moderate Pace, Threshold Pace, Interval Pace, Target Heart Rate の値を表示
        pace_data = {'設定ペース': [easy_pace, moderate_pace, threshold_pace, interval_pace],
                     '目標心拍数(回/分)': [f'{easy_hr[0]}~{easy_hr[1]}', f'{moderate_hr[0]}~{moderate_hr[1]}', f'{threshold_hr[0]}~{threshold_hr[1]}', f'{interval_hr[0]}~{interval_hr[1]}']}
        pace_df = pd.DataFrame(data=pace_data, index=['Easy Pace (/km)', 'Moderete Pace (/km)', 'Threshold Pace (/km)', 'Interval Pace (/km)'])
        st.table(pace_df.style.hide_index())

        week = ['月', '火', '水', '木', '金', '土', '日']

        # 追加: off リストの値を表示

        off_days = 'OFF日: ' + ', '.join([week[i] for i in off])
        st.write(off_days)    
        st.write('※ポイント練習の時は\nウォーミングアップ3kmジョギング\nクーリングダウン3kmジョギング\nを行う')
    # トレーニングスケジュールを作成
        df = pd.DataFrame(columns=['曜日', 'トレーニングメニュー'])
        # 練習頻度3回/週
        if freq in '3回/週':  
            for i in range(7):
                if i in off:
                    menu = 'OFF'

        # ポイント練習1回目
                elif event == '5000m' and i == 2:  # 5000m
                    menu = f'ポイント練習：インターバル走, 設定ペース{interval_pace}/km, 1km×5本 レスト400mジョギング'
                elif event == '10000m' and i == 2:  # 10000m
                    menu = f'ポイント練習：インターバル走, 設定ペース{interval_pace}/km, 1km×5本 レスト400mジョギング'
                elif event == 'ハーフマラソン' and i == 2:  # ハーフマラソン
                    menu = f'ポイント練習：ペース走, 設定ペース{threshold_pace}/km, 20min'
                elif event == 'フルマラソン' and i == 2:  # フルマラソン
                    menu = f'ポイント練習：ペース走, 設定ペース{threshold_pace}/km, 20min'
        # ポイント練習2回目
                elif i == 6:
                    menu = f'ロングラン, 設定ペース{moderate_pace}/km, 90min'
                else:
                    menu = f'Jog, 設定ペース{easy_pace}/km, 60min'
                df = df.append({'曜日': week[i], 'トレーニングメニュー': menu}, ignore_index=True)
            
        elif freq in ['4回/週', '5回/週']:
            for i in range(7):
                if i in off:
                    menu = 'OFF'
        # ポイント練習1回目
                elif event == '5000m' and i == 2:  # 5000m
                    menu = f'ポイント練習：インターバル走, 設定ペース{interval_pace}/km, 1km×5本 レスト400mジョギング'
                elif event == '10000m' and i == 2:  # 10000m
                    menu = f'ポイント練習：インターバル走, 設定ペース{interval_pace}/km, 1km×5本 レスト400mジョギング'
                elif event == 'ハーフマラソン' and i == 2:  # ハーフマラソン
                    menu = f'ポイント練習：ペース走, 設定ペース{threshold_pace}/km, 20min'
                elif event == 'フルマラソン' and i == 2:  # フルマラソン
                    menu = f'ポイント練習：ペース走, 設定ペース{threshold_pace}/km, 20min'
        # ポイント練習2回目
                elif event == '5000m' and i == 6:  # 5000m
                    menu = f'ポイント練習：ペース走, 設定ペース{threshold_pace}/km, 20min'
                elif event == '10000m' and i == 6:  # 10000m
                    menu = f'ポイント練習：ペース走, 設定ペース{threshold_pace}/km, 20min'      
                elif event == 'ハーフマラソン' and i == 6:  # ハーフマラソン
                    menu = f'ロングラン, 設定ペース{moderate_pace}/km, 90min'
                elif event == 'フルマラソン' and i == 6:  # フルマラソン
                    menu = f'ロングラン, 設定ペース{moderate_pace}/km, 90min'
                else:
                    menu = f'Jog, 設定ペース{easy_pace}/km, 60min'
                df = df.append({'曜日': week[i], 'トレーニングメニュー': menu}, ignore_index=True)
        else:
            for i in range(7):
                if i in off:
                    menu = 'OFF'
        # ポイント練習1回目
                elif i == 2:
                    menu = f'ポイント練習：ペース走\n設定ペース{threshold_pace}/km, 20min'
        # ポイント練習2回目
                elif event == '5000m' and i == 5:  # 5000m
                    menu = f'ポイント練習：インターバル走, 設定ペース{interval_pace}/km, 1km×5本 レスト400mジョギング'
                elif event == '10000m' and i == 5:  # 10000m
                    menu = f'ポイント練習：インターバル走, 設定ペース{interval_pace}/km, 1km×5本 レスト400mジョギング'
                elif event == 'ハーフマラソン' and i == 5:  # ハーフマラソン
                    menu = f'ポイント練習：インターバル走, 設定ペース{interval_pace}/km, 1km×3本 レスト400mジョギング'
        # ポイント練習3回目
                elif event == '5000m' and i == 6:  # 5000m
                    menu = f'ロングジョグ, 設定ペース{easy_pace}/km, 90min'
                elif event == '10000m' and i == 6:  # 10000m
                    menu = f'ロングジョグ, 設定ペース{easy_pace}/km, 90min'    
                elif event == 'ハーフマラソン' and i == 6:  # ハーフマラソン
                    menu = f'ロングラン, 設定ペース{moderate_pace}/km, 90min'
                elif event == 'フルマラソン' and i == 6:  # フルマラソン
                    menu = f'ロングラン, 設定ペース{moderate_pace}/km, 120min'
                else:
                    menu = f'Jog, 設定ペース{easy_pace}/km, 60min'
                df = df.append({'曜日': week[i], 'トレーニングメニュー': menu}, ignore_index=True)
        # 表形式でトレーニングメニューを出力
        st.table(df.set_index('曜日'))

                
if __name__ == '__main__':
    main()
