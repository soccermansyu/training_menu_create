import streamlit as st
import pandas as pd
import datetime
import math
import unicodedata

def main():
    st.title("ランニングの練習メニュー作成アプリ")
    st.write('Produced By 「ランニングを科学する」')
    # 入力フォームを作成
    st.write("<span style='font-size: 18px;'><b>1. 自己ベストを出した種目</b></span>", 
         unsafe_allow_html=True)
    event = st.selectbox('event', ['5000m', '10000m', 'ハーフマラソン', 'フルマラソン'])
    if event == '5000m':
        distance = 5000
    elif event == '10000m':
        distance = 10000
    elif event == 'ハーフマラソン':
        distance = 21095
    else:
        distance = 42195

    st.write("<span style='font-size: 18px;'><b>2. 自己ベスト(hh:mm:ss)</b></span>", 
         unsafe_allow_html=True)
    st.write('半角の数字で入力してください')
    best_time_hour = st.number_input('時間', min_value=0, max_value=23, value=0, step=1)
    best_time_minute = st.number_input('分', min_value=0, max_value=59, value=0, step=1)
    best_time_second = st.number_input('秒', min_value=0, max_value=59, value=0, step=1)

    # hh:mm:ss形式の文字列を作成する
    best_time = f"{str(best_time_hour).zfill(2)}:{str(best_time_minute).zfill(2)}:{str(best_time_second).zfill(2)}"

    # 自己ベストタイムを表示する
    st.write(f"<span style='font-size: 20px;'><b>-->あなたの自己ベストタイム： {best_time}({event})</b></span>", 
         unsafe_allow_html=True)

    st.write("<span style='font-size: 18px;'><b>3. 目標とする種目</b></span>", 
         unsafe_allow_html=True)
    event2 = st.selectbox('event2', ['5000m', '10000m', 'ハーフマラソン', 'フルマラソン'])

    st.write("<span style='font-size: 18px;'><b>4. 年齢</b></span>", 
         unsafe_allow_html=True)
    age = st.slider('age', min_value=10, max_value=80, value=30)

    st.write("<span style='font-size: 18px;'><b>5. 練習頻度</b></span>", 
         unsafe_allow_html=True)
    freq = st.selectbox('freq', ['3 回/週', '4 回/週', '5 回/週', '6 回/週', '7 回/週'])

    # すべての入力ができているかチェック
    if event == '' or best_time == '00:00:00' or freq == '' or age == 0:
        st.warning('未入力の項目があります')
        submitted = False
    else:
        # 作成ボタンを押した時の処理を記述
        submitted = st.button('作成')

        # off リストを更新
        if freq == '3 回/週':
            off = [0, 1, 3, 5]
        elif freq == '4 回/週':
            off = [0, 3, 4]
        elif freq == '5 回/週':
            off = [0, 4]
        elif freq == '6 回/週':
            off = [0]
        else:
            off = []

    max_hr = int(207 - age * 0.7)
    easy_hr = (int(max_hr * 0.65), int(max_hr * 0.74))
    moderate_hr = (int(max_hr * 0.74), int(max_hr * 0.79))
    threshold_hr = (int(max_hr * 0.8), int(max_hr * 0.92))
    cv_hr = (int(max_hr * 0.90), int(max_hr * 0.95))
    interval_hr = (int(max_hr * 0.95), int(max_hr * 1.0))
    repetition_hr = ("-", "-")

    def seconds_to_mmss(seconds):
        seconds = int(seconds + 0.5)    # 秒数を四捨五入
        m = seconds // 60              # 分の取得
        s = seconds - m * 60           # 秒の取得
        return f"{m:01}:{s:02}"        # mm:ss形式の文字列で返す
        
    # メニューの作成
    if submitted:

        # 自己ベストを秒数に変換する
        best_time = datetime.datetime.strptime(best_time, '%H:%M:%S')
        best_time_seconds = best_time.hour * 3600 + best_time.minute * 60 + best_time.second

        # 平均ペースを計算する
        avev = distance / (best_time_seconds / 60)

        # %VO2maxを計算する
        rvo2max = 0.8 + 0.1894393 * math.exp(-0.012788 * best_time_seconds / 60) + 0.2989558 * math.exp(-0.1932605 * best_time_seconds / 60)
        rrvo2max = rvo2max * 100

        # VO2を計算する
        vo2 = -4.6 + 0.182258 * avev + 0.000104 * avev ** 2

        # VO2maxを計算する
        vo2max = vo2 / rvo2max
        paces = {
            'easy_pace': (0.59, 0.74),
            'moderate_pace': (0.75, 0.79),
            'threshold_pace': (0.80, 0.88),
            'cv_pace': (0.89, 0.94),            
            'interval_pace': (0.95, 1.00),
            'repetition_pace': (1.05, 1.70)
        }
        
        pace_ranges = {}
        for pace, (min_val, max_val) in paces.items():
            training_pace_min = (-0.182258 + math.sqrt(0.182258 ** 2 - 4 * 0.000104 * (-4.6 - vo2max * min_val))) / (2 * 0.000104)
            training_pace_max = (-0.182258 + math.sqrt(0.182258 ** 2 - 4 * 0.000104 * (-4.6 - vo2max * max_val))) / (2 * 0.000104)
            pace_ranges[pace] = (training_pace_min, training_pace_max)

        formatted_pace_ranges = {}
        for pace, (min_val, max_val) in pace_ranges.items():
            # m/min の逆数をとって、min/1kmに変換
            min_pace = 1000 * 60 / (min_val)
            max_pace = 1000 * 60 / (max_val)
            # secondをmm:ss形式に変換
            formatted_min_pace = seconds_to_mmss(int(min_pace))
            formatted_max_pace = seconds_to_mmss(int(max_pace))
            formatted_pace_ranges[pace] = (formatted_min_pace, formatted_max_pace)

        st.write(f'目標種目: {event2}')
        st.write(f'現在のVDOT(vo2max): {round(vo2max, 1)} ml/kg/分')
        st.write(f'最大心拍数(HRmax): {max_hr} 回/分')
        st.write(f'※最大心拍数(HRmax)の計算方法：207 - (年齢 × 0.7)')
        if freq == '3 回/週':
            distance_week = '40'
        elif freq == '4 回/週':
            distance_week = '50'
        elif freq == '5 回/週':
            distance_week = '65'
        elif freq == '6 回/週':
            distance_week = '85'
        elif freq == '7 回/週':
            distance_week = '110'
        else:
            distance_week = ''
        st.write(f'練習頻度: {freq}')
        st.write(f'週間走行距離目安: {distance_week} km/週')

        # ペースと心拍数をテーブルで表示する
        hr_ranges = {
            'easy_pace': easy_hr,
            'moderate_pace': moderate_hr,
            'threshold_pace': threshold_hr,
            'cv_pace': cv_hr,           
            'interval_pace': interval_hr,
            'repetition_pace': repetition_hr
        }
            
        pace_data = {'設定ペース': [], '目標心拍数(回/分)': []}
        for pace, (min_val, max_val) in hr_ranges.items():
            pace_data['設定ペース'].append(f'{formatted_pace_ranges[pace][0]} - {formatted_pace_ranges[pace][1]} /km')
            pace_data['目標心拍数(回/分)'].append(f'{min_val} - {max_val}')

        pace_df = pd.DataFrame(data=pace_data, index=['Easy Pace', 'Moderate Pace', 'Threshold Pace', 'CV Pace', 'Interval Pace', 'Repetition Pace'])
        easy_pace_min = formatted_pace_ranges['easy_pace'][0]
        easy_pace_max = formatted_pace_ranges['easy_pace'][1]
        moderate_pace_min = formatted_pace_ranges['moderate_pace'][0]
        moderate_pace_max = formatted_pace_ranges['moderate_pace'][1]
        threshold_pace_min = formatted_pace_ranges['threshold_pace'][0]
        threshold_pace_max = formatted_pace_ranges['threshold_pace'][1]
        interval_pace_min = formatted_pace_ranges['interval_pace'][0]
        interval_pace_max = formatted_pace_ranges['interval_pace'][1]
        repetition_pace_min = formatted_pace_ranges['repetition_pace'][0]
        repetition_pace_max = formatted_pace_ranges['repetition_pace'][1]

        week = ['月', '火', '水', '木', '金', '土', '日']
        st.write("※ポイント練習の時は")
        st.write("ウォーミングアップ：3km Jog")
        st.write("クーリングダウン：3km Jog")
        st.write("を行う。")
        
    # トレーニングスケジュールを作成
        df = pd.DataFrame(columns=['曜日', 'トレーニングメニュー'])
        # 練習頻度3回/週
        if freq in '3 回/週':  
            for i in range(7):
                if i in off:
                    menu = 'OFF'
        # ポイント練習1回目
                elif event2 == '5000m' and i == 2:  # 5000m
                    menu = f'ポイント練習：インターバル走, 設定ペース{interval_pace_min}/km, 1km×5本 レスト400mジョギング'
                elif event2 == '10000m' and i == 2:  # 10000m
                    menu = f'ポイント練習：インターバル走, 設定ペース{interval_pace_min}/km, 1km×5本 レスト400mジョギング'
                elif event2 == 'ハーフマラソン' and i == 2:  # ハーフマラソン
                    menu = f'ポイント練習：ペース走, 設定ペース{threshold_pace_max}/km, 20min'
                elif event2 == 'フルマラソン' and i == 2:  # フルマラソン
                    menu = f'ポイント練習：ペース走, 設定ペース{threshold_pace_max}/km, 20min'
        # ポイント練習2回目
                elif i == 6:
                    menu = f'ロングラン, 設定ペース{moderate_pace_min}~{moderate_pace_max}/km, 90min'
                else:
                    menu = f'Jog, 設定ペース{easy_pace_min}~{easy_pace_max}/km, 60min'
                df.loc[len(df)] = {'曜日': week[i], 'トレーニングメニュー': menu}

        elif freq in ['4 回/週', '5 回/週']:
            for i in range(7):
                if i in off:
                    menu = 'OFF'
        # ポイント練習1回目
                elif event2 == '5000m' and i == 2:  # 5000m
                    menu = f'ポイント練習：インターバル走, 設定ペース{interval_pace_min}/km, 1km×5本 レスト400mジョギング'
                elif event2 == '10000m' and i == 2:  # 10000m
                    menu = f'ポイント練習：インターバル走, 設定ペース{interval_pace_min}/km, 1km×5本 レスト400mジョギング'
                elif event2 == 'ハーフマラソン' and i == 2:  # ハーフマラソン
                    menu = f'ポイント練習：ペース走, 設定ペース{threshold_pace_max}/km, 20min'
                elif event2 == 'フルマラソン' and i == 2:  # フルマラソン
                    menu = f'ポイント練習：ペース走, 設定ペース{threshold_pace_max}/km, 20min'
        # ポイント練習2回目
                elif event2 == '5000m' and i == 6:  # 5000m
                    menu = f'ポイント練習：ペース走, 設定ペース{threshold_pace_max}/km, 20min'
                elif event2 == '10000m' and i == 6:  # 10000m
                    menu = f'ポイント練習：ペース走, 設定ペース{threshold_pace_max}/km, 20min'      
                elif event2 == 'ハーフマラソン' and i == 6:  # ハーフマラソン
                    menu = f'ロングラン, 設定ペース{moderate_pace_min}~{moderate_pace_max}/km, 90min'
                elif event2 == 'フルマラソン' and i == 6:  # フルマラソン
                    menu = f'ロングラン, 設定ペース{moderate_pace_min}~{moderate_pace_max}/km, 90min'
                else:
                    menu = f'Jog, 設定ペース{easy_pace_min}~{easy_pace_max}/km, 60min'
                df.loc[len(df)] = {'曜日': week[i], 'トレーニングメニュー': menu}

        else:
            for i in range(7):
                if i in off:
                    menu = 'OFF'
        # ポイント練習1回目
                elif i == 2:
                    menu = f'ポイント練習：ペース走\n設定ペース{threshold_pace_max}/km, 20min'
        # ポイント練習2回目
                elif event2 == '5000m' and i == 5:  # 5000m
                    menu = f'ポイント練習：インターバル走, 設定ペース{interval_pace_min}/km, 1km×5本 レスト400mジョギング'
                elif event2 == '10000m' and i == 5:  # 10000m
                    menu = f'ポイント練習：インターバル走, 設定ペース{interval_pace_min}/km, 1km×5本 レスト400mジョギング'
                elif event2 == 'ハーフマラソン' and i == 5:  # ハーフマラソン
                    menu = f'ポイント練習：インターバル走, 設定ペース{interval_pace_max}/km, 1km×3本 レスト400mジョギング'
        # ポイント練習3回目
                elif event2 == '5000m' and i == 6:  # 5000m
                    menu = f'ロングジョグ, 設定ペース{easy_pace_min}~{easy_pace_max}/km, 90min'
                elif event2 == '10000m' and i == 6:  # 10000m
                    menu = f'ロングジョグ, 設定ペース{easy_pace_min}~{easy_pace_max}/km, 90min'    
                elif event2 == 'ハーフマラソン' and i == 6:  # ハーフマラソン
                    menu = f'ロングラン, 設定ペース{moderate_pace_min}~{moderate_pace_max}/km, 90min'
                elif event2 == 'フルマラソン' and i == 6:  # フルマラソン
                    menu = f'ロングラン, 設定ペース{moderate_pace_min}~{moderate_pace_max}/km, 120min'
                else:
                    menu = f'Jog, 設定ペース{easy_pace_min}~{easy_pace_max}/km, 60min'
                df.loc[len(df)] = {'曜日': week[i], 'トレーニングメニュー': menu}
                
        # 表形式でトレーニングメニューを出力
        st.table(df.set_index('曜日'))
        st.table(pace_df)
        st.write("コメント：")
        st.write("・年間を通じて行うことで記録が向上する、基本的なトレーニングメニューです。")
        st.write("・走る距離ではなく、時間を目安にメニューを作成しています。")
        st.write("・設定ペースはあくまで目安です。各個人によって適切なペースは異なる可能性があります。")
        st.write("・ポイント練習での心拍数目安は、練習の後半で最終的に到達する心拍数です。練習序盤は低めの心拍数となります。")        
        st.write("・目標とするレースに合わせて、練習の内容を変えることで、さらに記録向上を狙うことも可能ですが、そこまで突き詰める必要が無い方にとっては、このトレーニングメニューで十分だと考えています。")
        st.write("・ペース毎の詳細解説")
        st.write("　＞【ジョギング(Eペース走)】効果を高めるための心拍数や距離を考察\n(https://shuichi-running.com/jogging-theory/)")
        st.write("　＞【距離走(ロングジョグ)】の効果を最大化する方法を考察 適正ペースや距離は？\n(https://shuichi-running.com/long-run-theory/)")
        st.write("　＞【LT走(閾値走)】乳酸性作業閾値を高める効果的な練習方法(ペース設定等)(https://shuichi-running.com/lt-tr/)")
        st.write("　＞【CVインターバルトレーニング】遅いペースのインターバルでも効果がある理由\n(https://shuichi-running.com/cvinterval-tr-theory/)")
        st.write("　＞【インターバルトレーニング】ペースとレストの設定方法により得られる効果の違いを徹底解説(https://shuichi-running.com/interval-tr/)")
        st.write("　＞【レペティショントレーニングとは？】目的と効果を徹底解説し練習方法を紹介(https://shuichi-running.com/repetition-tr-theory/)")
        st.write("「ランニングを科学する」ではオンラインパーソナルトレーニングサービスを行っています。仕事・家事・育児で忙しいランナーに向け、「効率よく」を方針として、1人1人の都合に合わせてトレーニングを構築します。詳細は以下のリンク先で紹介しております。(https://shuichi-running.com/online-menu/)")
        
if __name__ == '__main__':
    main()
