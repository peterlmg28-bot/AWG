#include <QApplication>
#include <QWidget>
#include <QLabel>
#include <QLineEdit>
#include <QPushButton>
#include <QComboBox>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QString>
#include <map>
#include <cmath>

struct AWGInfo {
    double diameter_mm;
    double diameter_inch;
    double area_mm2;
    double resistance;
    double normal_current;
    double max_current;
};

std::map<QString, AWGInfo> awg_data = {
    {"30", {0.254, 0.0100, 0.0507, 361, 0.200, 0.228}},
    {"28", {0.32, 0.0126, 0.0804, 227, 0.318, 0.362}},
    {"26", {0.404, 0.0159, 0.1281, 143, 0.506, 0.577}},
    {"24", {0.511, 0.0201, 0.2047, 89.4, 0.808, 0.921}},
    {"22", {0.643, 0.0253, 0.3247, 54.3, 1.280, 1.460}},
    {"20", {0.813, 0.0320, 0.5189, 33.9, 2.0, 2.3}},
    {"18", {1.02, 0.0403, 0.8107, 21.4, 3.2, 3.7}},
    {"16", {1.29, 0.0508, 1.318, 13.5, 5.2, 5.9}},
    {"14", {1.63, 0.0641, 2.075, 8.45, 8.2, 9.4}},
    {"12", {2.05, 0.0808, 3.332, 5.31, 13.1, 14.9}},
    {"10", {2.59, 0.1019, 5.26, 3.36, 20.8, 23.7}},
    {"8", {3.26, 0.1285, 8.37, 2.11, 33.0, 37.7}},
    {"6", {4.11, 0.162, 13.3, 1.33, 52.5, 59.9}},
    {"4", {5.19, 0.2043, 21.15, 0.84, 83.5, 95.2}},
    {"2", {6.54, 0.2576, 33.62, 0.53, 132.7, 151.3}},
    {"0", {8.25, 0.3249, 53.49, 0.33, 211.1, 240.7}},
};

QString query_awg(const QString& awg) {
    if (awg_data.find(awg) == awg_data.end())
        return QString("AWG %1 不存在於資料表中。").arg(awg);
    const AWGInfo& info = awg_data[awg];
    return QString("AWG %1 規格:\n外徑: %2 mm (%3 inch)\n截面積: %4 mm2\n電阻值: %5 Ω/Km\n正常電流: %6 A\n最大電流: %7 A")
        .arg(awg)
        .arg(info.diameter_mm)
        .arg(info.diameter_inch)
        .arg(info.area_mm2)
        .arg(info.resistance)
        .arg(info.normal_current)
        .arg(info.max_current);
}

QString reverse_query(double value, QString unit) {
    QString closest_awg;
    double min_diff = 1e9;
    for (auto it = awg_data.begin(); it != awg_data.end(); ++it) {
        double d = (unit == "mm") ? it->second.diameter_mm : it->second.diameter_inch;
        double diff = std::abs(d - value);
        if (diff < min_diff) {
            min_diff = diff;
            closest_awg = it->first;
        }
    }
    QString result = QString("最接近的 AWG 是: AWG %1 (差距 %2 %3)\n").arg(closest_awg).arg(min_diff).arg(unit);
    result += query_awg(closest_awg);
    return result;
}

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    QWidget window;
    window.setWindowTitle("AWG 查詢系統 (Qt)");

    // UI 元件
    QComboBox* modeBox = new QComboBox;
    modeBox->addItem("AWG查詢");
    modeBox->addItem("直徑反查");

    QLineEdit* awgEdit = new QLineEdit;
    QLineEdit* diameterEdit = new QLineEdit;
    QComboBox* unitBox = new QComboBox;
    unitBox->addItem("mm");
    unitBox->addItem("inch");

    QPushButton* queryBtn = new QPushButton("查詢");
    QLabel* resultLabel = new QLabel;
    resultLabel->setWordWrap(true);

    // 佈局
    QVBoxLayout* mainLayout = new QVBoxLayout;
    mainLayout->addWidget(modeBox);

    QHBoxLayout* awgLayout = new QHBoxLayout;
    awgLayout->addWidget(new QLabel("AWG編號:"));
    awgLayout->addWidget(awgEdit);
    mainLayout->addLayout(awgLayout);

    QHBoxLayout* diameterLayout = new QHBoxLayout;
    diameterLayout->addWidget(new QLabel("直徑值:"));
    diameterLayout->addWidget(diameterEdit);
    diameterLayout->addWidget(new QLabel("單位:"));
    diameterLayout->addWidget(unitBox);
    mainLayout->addLayout(diameterLayout);

    mainLayout->addWidget(queryBtn);
    mainLayout->addWidget(resultLabel);
    window.setLayout(mainLayout);

    // 初始顯示
    awgEdit->show();
    awgLayout->setEnabled(true);
    diameterEdit->hide();
    unitBox->hide();
    diameterLayout->setEnabled(false);

    // 切換模式
    QObject::connect(modeBox, &QComboBox::currentTextChanged, [&](const QString& mode){
        if (mode == "AWG查詢") {
            awgEdit->show();
            awgLayout->setEnabled(true);
            diameterEdit->hide();
            unitBox->hide();
            diameterLayout->setEnabled(false);
        } else {
            awgEdit->hide();
            awgLayout->setEnabled(false);
            diameterEdit->show();
            unitBox->show();
            diameterLayout->setEnabled(true);
        }
    });

    // 查詢按鈕
    QObject::connect(queryBtn, &QPushButton::clicked, [&]{
        if (modeBox->currentText() == "AWG查詢") {
            QString awg = awgEdit->text();
            resultLabel->setText(query_awg(awg));
        } else {
            bool ok = false;
            double value = diameterEdit->text().toDouble(&ok);
            QString unit = unitBox->currentText();
            if (ok)
                resultLabel->setText(reverse_query(value, unit));
            else
                resultLabel->setText("請輸入有效的直徑數值！");
        }
    });

    window.resize(400, 300);
    window.show();
    return app.exec();
}
