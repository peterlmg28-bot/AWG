#include <iostream>
#include <map>
#include <string>
#include <iomanip>
#include <cmath>
using namespace std;

struct AWGInfo {
    double diameter_mm;
    double diameter_inch;
    double area_mm2;
    double resistance;
    double normal_current;
    double max_current;
};

map<string, AWGInfo> awg_data = {
    {"12", {2.05, 0.0808, 3.332, 5.31, 13.1, 14.9}},
    {"10", {2.59, 0.1019, 5.26, 3.36, 20.8, 23.7}},
    {"8", {3.26, 0.1285, 8.37, 2.11, 33.0, 37.7}},
    {"6", {4.11, 0.162, 13.3, 1.33, 52.5, 59.9}},
    {"4", {5.19, 0.2043, 21.15, 0.84, 83.5, 95.2}},
    {"2", {6.54, 0.2576, 33.62, 0.53, 132.7, 151.3}},
    {"0", {8.25, 0.3249, 53.49, 0.33, 211.1, 240.7}},
    // ...可自行擴充完整資料...
};

void query_awg(const string& awg) {
    auto it = awg_data.find(awg);
    if (it == awg_data.end()) {
        cout << "AWG " << awg << " 不存在於資料表中。" << endl;
        return;
    }
    const AWGInfo& info = it->second;
    cout << fixed << setprecision(4);
    cout << "AWG " << awg << " 規格:" << endl;
    cout << "外徑: " << info.diameter_mm << " mm (" << info.diameter_inch << " inch)" << endl;
    cout << "截面積: " << info.area_mm2 << " mm2" << endl;
    cout << "電阻值: " << info.resistance << " Ω/Km" << endl;
    cout << "正常電流: " << info.normal_current << " A" << endl;
    cout << "最大電流: " << info.max_current << " A" << endl;
}

void reverse_query(double value, string unit) {
    string closest_awg;
    double min_diff = 1e9;
    for (const auto& kv : awg_data) {
        double d = (unit == "mm") ? kv.second.diameter_mm : kv.second.diameter_inch;
        double diff = abs(d - value);
        if (diff < min_diff) {
            min_diff = diff;
            closest_awg = kv.first;
        }
    }
    cout << "最接近的 AWG 是: AWG " << closest_awg << " (差距 " << min_diff << " " << unit << ")" << endl;
    query_awg(closest_awg);
}

int main() {
    cout << "=== AWG 查詢系統 (C++) ===" << endl;
    while (true) {
        cout << "輸入模式(1=AWG查詢，2=直徑反查，q=離開): ";
        string mode;
        cin >> mode;
        if (mode == "1") {
            cout << "請輸入 AWG 編號(如 12): ";
            string awg;
            cin >> awg;
            query_awg(awg);
        } else if (mode == "2") {
            cout << "請輸入直徑值: ";
            double value;
            cin >> value;
            cout << "單位 mm 或 inch: ";
            string unit;
            cin >> unit;
            reverse_query(value, unit);
        } else if (mode == "q") {
            cout << "程式結束！" << endl;
            break;
        } else {
            cout << "請輸入 1、2 或 q" << endl;
        }
    }
    return 0;
}
