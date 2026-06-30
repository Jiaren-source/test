#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
使用示例：紙本資料整理和分析
"""

import pandas as pd
import sys
import os

# 添加父目錄到路徑
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_processor import DataProcessor
from src.excel_generator import ExcelGenerator
from src.analyzer import DataAnalyzer


def main():
    print("🚀 開始運行示例...\n")
    
    # ========== 1. 創建示例數據 ==========
    print("📊 第一步: 創建示例數據")
    print("-" * 50)
    
    sample_data = {
        '姓名': ['張三', '李四', '王五', '趙六', '孫七', '李四'],  # 注意有重複
        '部門': ['銷售', '技術', '銷售', '人資', '技術', '銷售'],
        '月度銷售額': [50000, None, 65000, 45000, 72000, 58000],  # 注意有缺失值
        '年薪': [28, 32, 25, 35, 29, 32],
        '入職日期': ['2020-01-15', '2019-05-20', '2021-03-10', '2018-11-01', '2020-07-22', '2019-05-20']
    }
    
    df = pd.DataFrame(sample_data)
    print(f"\n原始數據 ({len(df)} 行):\n{df}\n")
    
    # ========== 2. 數據處理 ==========
    print("\n🔧 第二步: 數據清洗和處理")
    print("-" * 50)
    
    processor = DataProcessor()
    processor.data = df.copy()
    
    # 處理缺失值
    processor.fill_missing_values(method='mean')
    print(f"\n填充缺失值後: \n{processor.get_data()}\n")
    
    # 移除重複記錄
    processor.remove_duplicates()
    print(f"\n去重後數據 ({len(processor.get_data())} 行):\n{processor.get_data()}\n")
    
    # ========== 3. 數據分析 ==========
    print("\n📈 第三步: 數據分析")
    print("-" * 50)
    
    analyzer = DataAnalyzer(processor.get_data())
    
    # 基本統計
    basic_stats = analyzer.get_basic_stats()
    print(f"\n基本統計信息:")
    print(f"  - 行數: {basic_stats['總行數']}")
    print(f"  - 列數: {basic_stats['總列數']}")
    print(f"  - 缺失值: {basic_stats['缺失值']}")
    
    # 數字列統計
    print(f"\n月度銷售額統計:")
    numeric_stats = analyzer.get_numeric_stats('月度銷售額')
    for key, value in numeric_stats.items():
        if key != '列名':
            if isinstance(value, float):
                print(f"  - {key}: {value:.2f}")
            else:
                print(f"  - {key}: {value}")
    
    # 分組統計
    print(f"\n按部門分組統計銷售額:")
    group_stats = analyzer.group_by_stats('部門', '月度銷售額')
    print(f"{group_stats}\n")
    
    # 值計數
    print(f"部門分布:")
    dept_counts = analyzer.get_value_counts('部門')
    print(f"{dept_counts}\n")
    
    # ========== 4. 生成 Excel ==========
    print("\n📁 第四步: 生成 Excel 文件")
    print("-" * 50)
    
    # 創建輸出目錄
    os.makedirs('data/output', exist_ok=True)
    
    generator = ExcelGenerator()
    
    # 生成多工作表 Excel
    output_dict = {
        '原始數據': processor.get_data(),
        '部門統計': group_stats,
        '部門分布': dept_counts
    }
    
    generator.generate_with_multiple_sheets(
        'data/output/analysis_report.xlsx',
        output_dict
    )
    
    print("\n✅ Excel 文件生成成功!")
    print("   路徑: data/output/analysis_report.xlsx\n")
    
    # ========== 5. 生成報告 ==========
    print("\n📋 第五步: 生成分析報告")
    print("-" * 50)
    
    report = analyzer.generate_report()
    print("\n分析報告已生成\n")
    
    # 導出報告
    analyzer.export_report('data/output/analysis_report.txt')
    print("\n✅ 完成!\n")
    print("\n📊 生成的文件:")
    print("  1. data/output/analysis_report.xlsx - 分析報告 (Excel)")
    print("  2. data/output/analysis_report.txt - 分析報告 (文本)\n")


if __name__ == '__main__':
    main()
