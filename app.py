from flask import Flask, render_template_string, request

awg_data = {
    "0000": {"直徑_mm": 11.68, "直徑_inch": 0.46, "截面積_mm2": 107.22, "電阻_ΩKm": 0.17, "正常電流_A": 423.2, "最大電流_A": 482.6},
    "000": {"直徑_mm": 10.4, "直徑_inch": 0.4096, "截面積_mm2": 85.01, "電阻_ΩKm": 0.21, "正常電流_A": 335.5, "最大電流_A": 382.3},
    "00": {"直徑_mm": 9.27, "直徑_inch": 0.3648, "截面積_mm2": 67.43, "電阻_ΩKm": 0.26, "正常電流_A": 266.2, "最大電流_A": 303.5},
    "0": {"直徑_mm": 8.25, "直徑_inch": 0.3249, "截面積_mm2": 53.49, "電阻_ΩKm": 0.33, "正常電流_A": 211.1, "最大電流_A": 240.7},
    "1": {"直徑_mm": 7.35, "直徑_inch": 0.2893, "截面積_mm2": 42.41, "電阻_ΩKm": 0.42, "正常電流_A": 167.4, "最大電流_A": 190.9},
    "2": {"直徑_mm": 6.54, "直徑_inch": 0.2576, "截面積_mm2": 33.62, "電阻_ΩKm": 0.53, "正常電流_A": 132.7, "最大電流_A": 151.3},
    "3": {"直徑_mm": 5.83, "直徑_inch": 0.2294, "截面積_mm2": 26.67, "電阻_ΩKm": 0.67, "正常電流_A": 105.2, "最大電流_A": 120.0},
    "4": {"直徑_mm": 5.19, "直徑_inch": 0.2043, "截面積_mm2": 21.15, "電阻_ΩKm": 0.84, "正常電流_A": 83.5, "最大電流_A": 95.2},
    "5": {"直徑_mm": 4.62, "直徑_inch": 0.1819, "截面積_mm2": 16.77, "電阻_ΩKm": 1.06, "正常電流_A": 66.2, "最大電流_A": 75.5},
    "6": {"直徑_mm": 4.11, "直徑_inch": 0.162, "截面積_mm2": 13.3, "電阻_ΩKm": 1.33, "正常電流_A": 52.5, "最大電流_A": 59.9},
    "7": {"直徑_mm": 3.67, "直徑_inch": 0.1443, "截面積_mm2": 10.55, "電阻_ΩKm": 1.68, "正常電流_A": 41.6, "最大電流_A": 47.5},
    "8": {"直徑_mm": 3.26, "直徑_inch": 0.1285, "截面積_mm2": 8.37, "電阻_ΩKm": 2.11, "正常電流_A": 33.0, "最大電流_A": 37.7},
    "9": {"直徑_mm": 2.91, "直徑_inch": 0.1144, "截面積_mm2": 6.63, "電阻_ΩKm": 2.67, "正常電流_A": 26.2, "最大電流_A": 29.8},
    "10": {"直徑_mm": 2.59, "直徑_inch": 0.1019, "截面積_mm2": 5.26, "電阻_ΩKm": 3.36, "正常電流_A": 20.8, "最大電流_A": 23.7},
    "11": {"直徑_mm": 2.3, "直徑_inch": 0.0907, "截面積_mm2": 4.17, "電阻_ΩKm": 4.24, "正常電流_A": 16.5, "最大電流_A": 18.8},
    "12": {"直徑_mm": 2.05, "直徑_inch": 0.0808, "截面積_mm2": 3.332, "電阻_ΩKm": 5.31, "正常電流_A": 13.1, "最大電流_A": 14.9},
    "13": {"直徑_mm": 1.82, "直徑_inch": 0.072, "截面積_mm2": 2.627, "電阻_ΩKm": 6.69, "正常電流_A": 10.4, "最大電流_A": 11.8},
    "14": {"直徑_mm": 1.63, "直徑_inch": 0.0641, "截面積_mm2": 2.075, "電阻_ΩKm": 8.45, "正常電流_A": 8.2, "最大電流_A": 9.4},
    "15": {"直徑_mm": 1.45, "直徑_inch": 0.0571, "截面積_mm2": 1.646, "電阻_ΩKm": 10.6, "正常電流_A": 7.4, "最大電流_A": 8.5},
    "16": {"直徑_mm": 1.29, "直徑_inch": 0.0508, "截面積_mm2": 1.318, "電阻_ΩKm": 13.5, "正常電流_A": 5.2, "最大電流_A": 5.9},
    "17": {"直徑_mm": 1.15, "直徑_inch": 0.0453, "截面積_mm2": 1.026, "電阻_ΩKm": 16.3, "正常電流_A": 4.1, "最大電流_A": 4.7},
    "18": {"直徑_mm": 1.02, "直徑_inch": 0.0403, "截面積_mm2": 0.8107, "電阻_ΩKm": 21.4, "正常電流_A": 3.2, "最大電流_A": 3.7},
    "19": {"直徑_mm": 0.912, "直徑_inch": 0.0359, "截面積_mm2": 0.5667, "電阻_ΩKm": 26.9, "正常電流_A": 2.9, "最大電流_A": 3.4},
    "20": {"直徑_mm": 0.813, "直徑_inch": 0.0320, "截面積_mm2": 0.5189, "電阻_ΩKm": 33.9, "正常電流_A": 2.0, "最大電流_A": 2.3},
    "21": {"直徑_mm": 0.724, "直徑_inch": 0.0285, "截面積_mm2": 0.4116, "電阻_ΩKm": 42.7, "正常電流_A": 1.6, "最大電流_A": 1.9},
    "22": {"直徑_mm": 0.643, "直徑_inch": 0.0253, "截面積_mm2": 0.3247, "電阻_ΩKm": 54.3, "正常電流_A": 1.280, "最大電流_A": 1.460},
    "23": {"直徑_mm": 0.574, "直徑_inch": 0.0226, "截面積_mm2": 0.2588, "電阻_ΩKm": 48.5, "正常電流_A": 1.022, "最大電流_A": 1.165},
    "24": {"直徑_mm": 0.511, "直徑_inch": 0.0201, "截面積_mm2": 0.2047, "電阻_ΩKm": 89.4, "正常電流_A": 0.808, "最大電流_A": 0.921},
    "25": {"直徑_mm": 0.454, "直徑_inch": 0.0179, "截面積_mm2": 0.1624, "電阻_ΩKm": 79.6, "正常電流_A": 0.641, "最大電流_A": 0.731},
    "26": {"直徑_mm": 0.404, "直徑_inch": 0.0159, "截面積_mm2": 0.1281, "電阻_ΩKm": 143, "正常電流_A": 0.506, "最大電流_A": 0.577},
    "27": {"直徑_mm": 0.361, "直徑_inch": 0.0142, "截面積_mm2": 0.1021, "電阻_ΩKm": 128, "正常電流_A": 0.403, "最大電流_A": 0.460},
    "28": {"直徑_mm": 0.32, "直徑_inch": 0.0126, "截面積_mm2": 0.0804, "電阻_ΩKm": 227, "正常電流_A": 0.318, "最大電流_A": 0.362},
    "29": {"直徑_mm": 0.287, "直徑_inch": 0.0113, "截面積_mm2": 0.0647, "電阻_ΩKm": 289, "正常電流_A": 0.255, "最大電流_A": 0.291},
    "30": {"直徑_mm": 0.254, "直徑_inch": 0.0100, "截面積_mm2": 0.0507, "電阻_ΩKm": 361, "正常電流_A": 0.200, "最大電流_A": 0.228},
    "31": {"直徑_mm": 0.226, "直徑_inch": 0.0089, "截面積_mm2": 0.0401, "電阻_ΩKm": 321, "正常電流_A": 0.158, "最大電流_A": 0.181},
    "32": {"直徑_mm": 0.203, "直徑_inch": 0.0080, "截面積_mm2": 0.0316, "電阻_ΩKm": 583, "正常電流_A": 0.128, "最大電流_A": 0.146},
    "33": {"直徑_mm": 0.178, "直徑_inch": 0.0071, "截面積_mm2": 0.0255, "電阻_ΩKm": 944, "正常電流_A": 0.101, "最大電流_A": 0.115},
    "34": {"直徑_mm": 0.16, "直徑_inch": 0.0063, "截面積_mm2": 0.0201, "電阻_ΩKm": 956, "正常電流_A": 0.079, "最大電流_A": 0.091},
    "35": {"直徑_mm": 0.142, "直徑_inch": 0.0056, "截面積_mm2": 0.0169, "電阻_ΩKm": 1200, "正常電流_A": 0.063, "最大電流_A": 0.072},
    "36": {"直徑_mm": 0.127, "直徑_inch": 0.0050, "截面積_mm2": 0.0135, "電阻_ΩKm": 1530, "正常電流_A": 0.050, "最大電流_A": 0.057},
    "37": {"直徑_mm": 0.114, "直徑_inch": 0.0045, "截面積_mm2": 0.0098, "電阻_ΩKm": 1377, "正常電流_A": 0.041, "最大電流_A": 0.046},
    "38": {"直徑_mm": 0.102, "直徑_inch": 0.0040, "截面積_mm2": 0.0065, "電阻_ΩKm": 2400, "正常電流_A": 0.032, "最大電流_A": 0.036},
    "39": {"直徑_mm": 0.089, "直徑_inch": 0.0035, "截面積_mm2": 0.0062, "電阻_ΩKm": 2100, "正常電流_A": 0.025, "最大電流_A": 0.028},
    "40": {"直徑_mm": 0.079, "直徑_inch": 0.0031, "截面積_mm2": 0.0049, "電阻_ΩKm": 4080, "正常電流_A": 0.019, "最大電流_A": 0.022},
    "41": {"直徑_mm": 0.071, "直徑_inch": 0.0028, "截面積_mm2": 0.0041, "電阻_ΩKm": 3685, "正常電流_A": 0.016, "最大電流_A": 0.018},
    "42": {"直徑_mm": 0.064, "直徑_inch": 0.0025, "截面積_mm2": 0.0032, "電阻_ΩKm": 6300, "正常電流_A": 0.013, "最大電流_A": 0.014},
    "43": {"直徑_mm": 0.056, "直徑_inch": 0.0022, "截面積_mm2": 0.0025, "電阻_ΩKm": 5544, "正常電流_A": 0.010, "最大電流_A": 0.011},
    "44": {"直徑_mm": 0.051, "直徑_inch": 0.0020, "截面積_mm2": 0.0020, "電阻_ΩKm": 10200, "正常電流_A": 0.008, "最大電流_A": 0.009},
    "45": {"直徑_mm": 0.046, "直徑_inch": 0.0018, "截面積_mm2": 0.0016, "電阻_ΩKm": 9180, "正常電流_A": 0.006, "最大電流_A": 0.007},
    "46": {"直徑_mm": 0.041, "直徑_inch": 0.0016, "截面積_mm2": 0.0013, "電阻_ΩKm": 16300, "正常電流_A": 0.005, "最大電流_A": 0.006}
}

def 查詢_AWG(awg):
    data = awg_data.get(awg)
    if not data:
        return f"AWG {awg} 不存在於資料表中。"
    return (
        f"AWG {awg} 規格:<br>"
        f"外徑: {data['直徑_mm']} mm ({data['直徑_inch']} inch)<br>"
        f"截面積: {data['截面積_mm2']} mm2<br>"
        f"電阻值: {data['電阻_ΩKm']} Ω/Km<br>"
        f"正常電流: {data['正常電流_A']} A<br>"
        f"最大電流: {data['最大電流_A']} A"
    )

def 反查_AWG(直徑值, 單位="mm"):
    最接近awg = None
    最小差距 = float("inf")
    for awg, data in awg_data.items():
        直徑 = data['直徑_mm'] if 單位 == "mm" else data['直徑_inch']
        差距 = abs(直徑 - 直徑值)
        if 差距 < 最小差距:
            最小差距 = 差距
            最接近awg = awg
    result = f"最接近的 AWG 是: AWG {最接近awg} (差距 {最小差距:.4f} {單位})<br>"
    result += 查詢_AWG(最接近awg)
    return result

app = Flask(__name__)

TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <title>AWG 查詢系統</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f8f8f8; }
        .container { max-width: 500px; margin: 40px auto; background: #fff; padding: 24px; border-radius: 8px; box-shadow: 0 2px 8px #ccc; }
        h2 { text-align: center; }
        .result { background: #f0f0f0; padding: 12px; border-radius: 6px; margin-top: 16px; }
        label { display: block; margin-top: 12px; }
        input, select, button { margin-top: 6px; width: 100%; padding: 8px; border-radius: 4px; border: 1px solid #ccc; }
        button { background: #0078d4; color: #fff; border: none; cursor: pointer; }
        button:hover { background: #005fa3; }
    </style>
</head>
<body>
    <div class="container">
        <h2>AWG 查詢系統</h2>
        <form method="post">
            <label>查詢模式：</label>
            <select name="mode" onchange="this.form.submit()">
                <option value="awg" {% if mode == 'awg' %}selected{% endif %}>AWG編號查詢</option>
                <option value="diameter" {% if mode == 'diameter' %}selected{% endif %}>直徑反查</option>
            </select>
            {% if mode == 'awg' %}
                <label>AWG編號：</label>
                <input type="text" name="awg" value="{{ awg|default('') }}">
            {% else %}
                <label>直徑值：</label>
                <input type="text" name="diameter" value="{{ diameter|default('') }}">
                <label>單位：</label>
                <select name="unit">
                    <option value="mm" {% if unit == 'mm' %}selected{% endif %}>mm</option>
                    <option value="inch" {% if unit == 'inch' %}selected{% endif %}>inch</option>
                </select>
            {% endif %}
            <button type="submit">查詢</button>
        </form>
        {% if result %}
        <div class="result">{{ result|safe }}</div>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    mode = request.form.get('mode', 'awg')
    result = ''
    awg = request.form.get('awg', '')
    diameter = request.form.get('diameter', '')
    unit = request.form.get('unit', 'mm')
    if request.method == 'POST':
        if mode == 'awg' and awg:
            result = 查詢_AWG(awg)
        elif mode == 'diameter' and diameter:
            try:
                value = float(diameter)
                result = 反查_AWG(value, unit)
            except ValueError:
                result = '請輸入有效的直徑數值！'
    return render_template_string(TEMPLATE, mode=mode, awg=awg, diameter=diameter, unit=unit, result=result)

if __name__ == '__main__':
    app.run(debug=True)
