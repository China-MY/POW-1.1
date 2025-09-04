from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
import hashlib
import time

def generate_rsa_keypair():
    """
    生成RSA公私钥对
    
    Returns:
        tuple: (private_key, public_key)
    """
    # 生成2048位的RSA私钥
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    
    # 从私钥获取公钥
    public_key = private_key.public_key()
    
    return private_key, public_key

def find_pow_hash(nickname, target_zeros):
    """
    寻找满足POW条件的哈希值
    
    Args:
        nickname (str): 昵称
        target_zeros (int): 目标前导零的数量
    
    Returns:
        tuple: (nonce, hash_content, hash_value)
    """
    nonce = 0
    target = '0' * target_zeros
    
    while True:
        hash_content = f"{nickname}{nonce}"
        hash_value = hashlib.sha256(hash_content.encode()).hexdigest()
        
        if hash_value.startswith(target):
            return nonce, hash_content, hash_value
        
        nonce += 1

def sign_message(private_key, message):
    """
    使用私钥对消息进行数字签名
    
    Args:
        private_key: RSA私钥
        message (str): 要签名的消息
    
    Returns:
        bytes: 数字签名
    """
    signature = private_key.sign(
        message.encode('utf-8'),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature

def verify_signature(public_key, message, signature):
    """
    使用公钥验证数字签名
    
    Args:
        public_key: RSA公钥
        message (str): 原始消息
        signature (bytes): 数字签名
    
    Returns:
        bool: 验证结果
    """
    try:
        public_key.verify(
            signature,
            message.encode('utf-8'),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except Exception:
        return False

def serialize_keys(private_key, public_key):
    """
    序列化密钥为PEM格式
    
    Args:
        private_key: RSA私钥
        public_key: RSA公钥
    
    Returns:
        tuple: (private_pem, public_pem)
    """
    # 序列化私钥
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    # 序列化公钥
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    return private_pem, public_pem

def main():
    """
    主函数：演示RSA数字签名过程
    """
    nickname = "China-MY"
    
    print("=== RSA数字签名演示 ===")
    print(f"使用昵称: {nickname}")
    print()
    
    # 1. 生成RSA密钥对
    print("🔑 生成RSA密钥对...")
    private_key, public_key = generate_rsa_keypair()
    private_pem, public_pem = serialize_keys(private_key, public_key)
    
    print("✅ RSA密钥对生成成功！")
    print("私钥 (PEM格式):")
    print(private_pem.decode('utf-8')[:200] + "...")
    print()
    print("公钥 (PEM格式):")
    print(public_pem.decode('utf-8'))
    print()
    
    # 2. 寻找满足POW条件的哈希值（4个0开头）
    print("🔍 寻找满足POW条件的哈希值（4个0开头）...")
    start_time = time.time()
    nonce, hash_content, hash_value = find_pow_hash(nickname, 4)
    end_time = time.time()
    
    print("✅ 找到满足条件的哈希值！")
    print(f"花费时间: {end_time - start_time:.4f} 秒")
    print(f"Nonce值: {nonce}")
    print(f"Hash内容: {hash_content}")
    print(f"Hash值: {hash_value}")
    print()
    
    # 3. 使用私钥对"昵称 + nonce"进行签名
    print("✍️ 使用私钥对消息进行数字签名...")
    signature = sign_message(private_key, hash_content)
    
    print("✅ 数字签名完成！")
    print(f"签名长度: {len(signature)} 字节")
    print(f"签名 (十六进制): {signature.hex()[:100]}...")
    print()
    
    # 4. 使用公钥验证签名
    print("🔍 使用公钥验证数字签名...")
    is_valid = verify_signature(public_key, hash_content, signature)
    
    if is_valid:
        print("✅ 签名验证成功！消息完整性和身份认证通过。")
    else:
        print("❌ 签名验证失败！")
    print()
    
    # 5. 测试篡改检测
    print("🧪 测试篡改检测...")
    tampered_content = hash_content + "tampered"
    is_tampered_valid = verify_signature(public_key, tampered_content, signature)
    
    if not is_tampered_valid:
        print("✅ 篡改检测成功！修改后的消息验证失败，证明签名机制有效。")
    else:
        print("❌ 篡改检测失败！")
    print()
    
    # 6. 总结
    print("📋 RSA数字签名演示总结:")
    print(f"1. 成功生成2048位RSA密钥对")
    print(f"2. 找到POW条件的消息: {hash_content}")
    print(f"3. 对应的SHA256哈希值: {hash_value}")
    print(f"4. 私钥签名验证: {'通过' if is_valid else '失败'}")
    print(f"5. 篡改检测: {'有效' if not is_tampered_valid else '无效'}")
    
    # 保存密钥到文件
    with open('private_key.pem', 'wb') as f:
        f.write(private_pem)
    
    with open('public_key.pem', 'wb') as f:
        f.write(public_pem)
    
    print("\n💾 密钥已保存到文件:")
    print("- private_key.pem (私钥)")
    print("- public_key.pem (公钥)")

if __name__ == "__main__":
    main()