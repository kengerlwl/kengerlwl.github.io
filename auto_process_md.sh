#!/bin/bash

# 自动化MD文件批处理脚本

# 设置工作目录为脚本所在目录
cd "$(dirname "$0")"

echo "===== 开始处理MD文件 ====="

# 检查源目录是否存在
if [ ! -d "./copyMD" ]; then
    echo "错误: 源目录 './copyMD' 不存在，请创建该目录并放入需要处理的MD文件"
    exit 1
fi

# 检查是否有MD文件需要处理
MD_COUNT=$(find ./copyMD -name "*.md" | wc -l)
if [ "$MD_COUNT" -eq 0 ]; then
    echo "警告: 源目录中没有找到MD文件，请确保有.md文件需要处理"
    exit 1
fi

echo "找到 $MD_COUNT 个MD文件需要处理"

# 运行Python处理脚本
echo "开始运行处理脚本..."
python3 main_多个文件处理.py

# 检查处理结果
if [ -d "./copyMDout输出" ]; then
    OUTPUT_COUNT=$(find ./copyMDout输出 -name "*.md" | wc -l)
    echo "处理完成! 共处理 $OUTPUT_COUNT 个文件"
    echo "输出目录: ./copyMDout输出"

    # 删除原来的copyMD目录并重命名新目录
    echo "正在删除原目录并重命名新目录..."
    rm -rf ./copyMD
    mv ./copyMDout输出 ./copyMD
    echo "目录重命名完成，新的处理后文件在 ./copyMD 目录中"
else
    echo "处理失败: 未生成输出目录"
    exit 1
fi

echo "===== 处理完成 ====="
