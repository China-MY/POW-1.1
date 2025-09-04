import hashlib
import time

def pow_mining(nickname, target_zeros):
    """
    工作量证明挖矿函数
    
    Args:
        nickname (str): 昵称
        target_zeros (int): 目标前导零的数量
    
    Returns:
        tuple: (nonce, hash_content, hash_value, elapsed_time)
    """
    nonce = 0
    target = '0' * target_zeros
    start_time = time.time()
    
    while True:
        # 构造要哈希的内容：昵称 + nonce
        hash_content = f"{nickname}{nonce}"
        
        # 计算SHA256哈希值
        hash_value = hashlib.sha256(hash_content.encode()).hexdigest()
        
        # 检查是否满足目标条件（前导零数量）
        if hash_value.startswith(target):
            end_time = time.time()
            elapsed_time = end_time - start_time
            return nonce, hash_content, hash_value, elapsed_time
        
        nonce += 1

def main():
    """
    主函数：执行POW挖矿演示
    """
    nickname = "China-MY"  # 我的昵称
    
    print("=== POW (工作量证明) 挖矿演示 ===")
    print(f"使用昵称: {nickname}")
    print()
    
    # 挖矿：寻找4个0开头的哈希值
    print("🔍 开始挖矿：寻找4个0开头的哈希值...")
    nonce_4, content_4, hash_4, time_4 = pow_mining(nickname, 4)
    
    print("✅ 找到4个0开头的哈希值！")
    print(f"花费时间: {time_4:.4f} 秒")
    print(f"Nonce值: {nonce_4}")
    print(f"Hash内容: {content_4}")
    print(f"Hash值: {hash_4}")
    print()
    
    # 挖矿：寻找5个0开头的哈希值
    print("🔍 开始挖矿：寻找5个0开头的哈希值...")
    nonce_5, content_5, hash_5, time_5 = pow_mining(nickname, 5)
    
    print("✅ 找到5个0开头的哈希值！")
    print(f"花费时间: {time_5:.4f} 秒")
    print(f"Nonce值: {nonce_5}")
    print(f"Hash内容: {content_5}")
    print(f"Hash值: {hash_5}")
    print()
    
    # 比较难度差异
    print("📊 难度比较:")
    print(f"4个0开头 - 尝试次数: {nonce_4 + 1}, 用时: {time_4:.4f}秒")
    print(f"5个0开头 - 尝试次数: {nonce_5 + 1}, 用时: {time_5:.4f}秒")
    print(f"难度增加倍数: {(nonce_5 + 1) / (nonce_4 + 1):.2f}倍")
    print(f"时间增加倍数: {time_5 / time_4:.2f}倍")

if __name__ == "__main__":
    main()