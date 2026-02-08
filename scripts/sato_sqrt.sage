import matplotlib
# 强制使用非交互式后端，防止在无图形界面下报错
matplotlib.use('Agg') 

import matplotlib.pyplot as plt
import numpy as np
from sage.all import *

# ==========================================
# 1. 定义泰坦多项式与参数
# ==========================================
def titan_poly(n, p):
    """
    计算 Q(n) = n^47 - (n-1)^47 mod p
    """
    n = int(n)
    p = int(p)
    term1 = pow(n, 47, p)
    term2 = pow(n - 1, 47, p)
    return (term1 - term2) % p

# 测试范围：建议 50000 以获得足够样本
MAX_PRIME = 50000 
MODULUS = 47

print(f"🚀 [Sqrt(p) Mode] 开始计算泰坦多项式的指数和分布...")
print(f"🎯 筛选范围: p < {MAX_PRIME}, 且 p ≡ 1 (mod {MODULUS})")

# ==========================================
# 2. 计算归一化指数和
# ==========================================
data_real = []  
data_imag = []  
data_abs = []   
p_list = []

# 获取素数迭代器
primes_iter = primes(283, MAX_PRIME)
primes_list = [p for p in primes_iter if p % MODULUS == 1]
total_primes = len(primes_list)

print(f"📊 找到 {total_primes} 个有效素数...")

for idx, p in enumerate(primes_list):
    p_int = int(p)
    S = 0
    # 计算指数和
    for n in range(p_int):
        val = int(titan_poly(n, p_int))
        theta = 2 * np.pi * val / p_int
        S += complex(np.cos(theta), np.sin(theta))
    
    # 【核心修正】归一化因子改为 sqrt(p)
    # 这意味着我们现在的单位是 "1个 sqrt(p)"
    norm_factor = np.sqrt(float(p_int))
    normalized_S = S / norm_factor
    
    data_real.append(normalized_S.real)
    data_imag.append(normalized_S.imag)
    data_abs.append(abs(normalized_S))
    p_list.append(p_int)

    # 打印进度
    if (idx + 1) % 20 == 0 or (idx + 1) == total_primes:
        print(f"   已处理 {idx + 1}/{total_primes} ...")

print("✅ 计算完成！")

# ==========================================
# 3. 终端直接输出统计结果
# ==========================================
data_abs_np = np.array(data_abs)
print("\n" + "="*40)
print("🧐 数据分析 (Normalization: sqrt(p))")
print("="*40)
print(f"样本数量: {len(data_abs)}")
print(f"模长 |x_p| 均值: {np.mean(data_abs_np):.4f}")
print(f"模长 |x_p| 最大值: {np.max(data_abs_np):.4f}")
print(f"模长 |x_p| 最小值: {np.min(data_abs_np):.4f}")
print("-" * 40)
print("解读指南：")
print(" - 如果最大值接近 8.0-9.0，说明界限约为 9*sqrt(p)。")
print(" - 观察均值是否接近 1.0 (典型随机游走)。")
print("="*40 + "\n")

# ==========================================
# 4. 生成图表 (Headless)
# ==========================================
try:
    print("正在生成图片 (titan_sato_sqrt.png)...")
    plt.figure(figsize=(16, 12))

    # 子图 1: 实部
    plt.subplot(2, 2, 1)
    # 扩大 bins 以显示细节
    plt.hist(data_real, bins=50, density=True, color='skyblue', edgecolor='black', alpha=0.7)
    plt.title('Real Part (Re/$\sqrt{p}$)')
    plt.xlabel('Re / $\sqrt{p}$')
    plt.grid(True, alpha=0.3)
    
    # 添加高斯参考线
    xlim = max(abs(min(data_real)), abs(max(data_real)))
    x = np.linspace(-xlim, xlim, 100)
    plt.plot(x, (1/np.sqrt(2*np.pi))*np.exp(-x**2/2), 'r--', label='Std Gaussian')
    plt.legend()

    # 子图 2: 虚部
    plt.subplot(2, 2, 2)
    plt.hist(data_imag, bins=50, density=True, color='lightgreen', edgecolor='black', alpha=0.7)
    plt.title('Imaginary Part (Im/$\sqrt{p}$)')
    plt.xlabel('Im / $\sqrt{p}$')
    plt.grid(True, alpha=0.3)

    # 子图 3: 复平面散点图
    plt.subplot(2, 2, 3)
    sc = plt.scatter(data_real, data_imag, alpha=0.7, s=20, c=p_list, cmap='viridis')
    plt.colorbar(sc, label='Prime p')
    plt.title('Complex Plane Scatter')
    plt.xlabel('Re')
    plt.ylabel('Im')
    plt.axis('equal')
    
    # 画同心圆参考 (半径 2, 4, 6, 8)
    for r in [2, 4, 6, 8]:
        theta = np.linspace(0, 2*np.pi, 100)
        plt.plot(r*np.cos(theta), r*np.sin(theta), 'k--', alpha=0.3)
        plt.text(r, 0, f'r={r}', color='k', alpha=0.5)

    # 子图 4: 模长分布
    plt.subplot(2, 2, 4)
    plt.hist(data_abs, bins=50, density=True, color='salmon', edgecolor='black', alpha=0.7)
    plt.title('Magnitude Distribution (|S|/$\sqrt{p}$)')
    plt.xlabel('|S| / $\sqrt{p}$')
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("titan_sato_sqrt.png", dpi=300)
    print(f"🖼️ 图表已保存为 'titan_sato_sqrt.png'")
    print(f"📂 文件位置: {os.getcwd()}/titan_sato_sqrt.png")
    
except Exception as e:
    print(f"❌ 绘图失败: {e}")