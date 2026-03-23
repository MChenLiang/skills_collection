"""
反模式案例 - 不推荐的代码风格

本文件展示了应该避免的反模式，用于对比和学习。
"""

import os
import sys


# ============================================
# 反模式 1: 不规范的命名
# ============================================

# ❌ 使用驼峰命名变量
userName = "John"  # 应该是 user_name
IsActive = True    # 应该是 is_active

# ❌ 单字母变量（除循环计数器）
n = 100           # 应该是 max_count
x = 5             # 应该是 current_value


# ============================================
# 反模式 2: 缺少类型注解
# ============================================

# ❌ 没有类型注解
def get_user(user_id):
    user = database.query(user_id)
    return user


# ✅ 应该添加类型注解
def get_user(user_id: int) -> Optional[Dict]:
    user = database.query(user_id)
    return user


# ============================================
# 反模式 3: 魔法数字和字符串
# ============================================

# ❌ 魔法数字
if user.age > 65:
    senior_discount = True

if status == "active" and role == "admin":
    grant_access()


# ✅ 应该使用常量
SENIOR_AGE_THRESHOLD = 65
STATUS_ACTIVE = "active"
ROLE_ADMIN = "admin"

if user.age > SENIOR_AGE_THRESHOLD:
    senior_discount = True

if status == STATUS_ACTIVE and role == ROLE_ADMIN:
    grant_access()


# ============================================
# 反模式 4: 过长的函数
# ============================================

# ❌ 函数过长，职责不单一
def process_data(data):
    # 验证数据
    if not data:
        return None

    # 转换数据
    transformed = []
    for item in data:
        if item['valid']:
            new_item = {
                'id': item['id'],
                'name': item['name'].upper(),
                'value': item['value'] * 2
            }
            transformed.append(new_item)

    # 过滤数据
    filtered = [item for item in transformed if item['value'] > 100]

    # 排序数据
    sorted_data = sorted(filtered, key=lambda x: x['value'], reverse=True)

    # 保存数据
    for item in sorted_data:
        database.save(item)

    # 发送通知
    notifications.send('Processing complete')

    return sorted_data


# ✅ 应该拆分成多个小函数
def validate_data(data: List[Dict]) -> bool:
    """验证数据"""
    return bool(data)

def transform_item(item: Dict) -> Dict:
    """转换单个数据项"""
    return {
        'id': item['id'],
        'name': item['name'].upper(),
        'value': item['value'] * 2
    }

def transform_data(data: List[Dict]) -> List[Dict]:
    """转换数据"""
    return [transform_item(item) for item in data if item['valid']]

def filter_data(data: List[Dict], threshold: int) -> List[Dict]:
    """过滤数据"""
    return [item for item in data if item['value'] > threshold]

def sort_data(data: List[Dict]) -> List[Dict]:
    """排序数据"""
    return sorted(data, key=lambda x: x['value'], reverse=True)

def save_data(data: List[Dict]) -> None:
    """保存数据"""
    for item in data:
        database.save(item)

def process_data(data: List[Dict]) -> List[Dict]:
    """处理数据（主函数）"""
    if not validate_data(data):
        return None

    transformed = transform_data(data)
    filtered = filter_data(transformed, 100)
    sorted_data = sort_data(filtered)
    save_data(sorted_data)
    notifications.send('Processing complete')

    return sorted_data


# ============================================
# 反模式 5: 过度的嵌套
# ============================================

# ❌ 过度嵌套，难以阅读
def process_order(order_id):
    order = db.get_order(order_id)
    if order:
        if order.status == "pending":
            if order.items:
                total = 0
                for item in order.items:
                    if item.available:
                        total += item.price * item.quantity
                    else:
                        return "Item not available"
                if total > 0:
                    if total < order.user.balance:
                        db.charge(order.user.id, total)
                        order.status = "paid"
                        db.save(order)
                        return "Payment successful"
                    else:
                        return "Insufficient balance"
                else:
                    return "Invalid total"
            else:
                return "No items in order"
        else:
            return "Order already processed"
    else:
        return "Order not found"


# ✅ 应该提前返回，减少嵌套
def process_order(order_id: int) -> str:
    """处理订单"""
    order = db.get_order(order_id)
    if not order:
        return "Order not found"

    if order.status != "pending":
        return "Order already processed"

    if not order.items:
        return "No items in order"

    total = calculate_order_total(order.items)
    if total <= 0:
        return "Invalid total"

    if total >= order.user.balance:
        return "Insufficient balance"

    # 处理支付
    db.charge(order.user.id, total)
    order.status = "paid"
    db.save(order)

    return "Payment successful"

def calculate_order_total(items: List[OrderItem]) -> float:
    """计算订单总额"""
    total = 0
    for item in items:
        if not item.available:
            raise ValueError("Item not available")
        total += item.price * item.quantity
    return total


# ============================================
# 反模式 6: 捕获所有异常
# ============================================

# ❌ 捕获所有异常，隐藏错误
def process_file(filename):
    try:
        with open(filename, 'r') as f:
            data = f.read()
        return data
    except:
        return None  # 静默失败，不知道具体错误


# ✅ 应该捕获具体异常
def process_file(filename: str) -> Optional[str]:
    """读取文件内容"""
    try:
        with open(filename, 'r') as f:
            return f.read()
    except FileNotFoundError:
        logger.error(f"File not found: {filename}")
        return None
    except IOError as e:
        logger.error(f"Failed to read file: {e}")
        return None


# ============================================
# 反模式 7: 重复代码
# ============================================

# ❌ 重复代码
def send_email_notification(user, message):
    email = user.email
    subject = "Notification"
    body = f"Dear {user.name},\n\n{message}\n\nBest regards"
    smtp.send(email, subject, body)

def send_email_alert(user, message):
    email = user.email
    subject = "Alert"
    body = f"Dear {user.name},\n\n{message}\n\nBest regards"
    smtp.send(email, subject, body)

def send_email_reminder(user, message):
    email = user.email
    subject = "Reminder"
    body = f"Dear {user.name},\n\n{message}\n\nBest regards"
    smtp.send(email, subject, body)


# ✅ 应该提取公共逻辑
def send_email(user: User, message: str, email_type: str) -> None:
    """发送邮件"""
    subject = email_type.capitalize()
    body = f"Dear {user.name},\n\n{message}\n\nBest regards"
    smtp.send(user.email, subject, body)

def send_email_notification(user: User, message: str) -> None:
    """发送通知邮件"""
    send_email(user, message, "notification")

def send_email_alert(user: User, message: str) -> None:
    """发送警报邮件"""
    send_email(user, message, "alert")

def send_email_reminder(user: User, message: str) -> None:
    """发送提醒邮件"""
    send_email(user, message, "reminder")


# ============================================
# 反模式 8: 不必要的注释
# ============================================

# ❌ 注释解释显而易见的代码
# 获取用户 ID
user_id = user.id

# 创建新用户
new_user = User()

# 如果用户已激活
if user.is_active:
    # 返回 True
    return True


# ✅ 应该注释"为什么"而不是"是什么"
user_id = user.id  # 用于后续的数据库查询

new_user = User()  # 创建临时用户用于验证

if user.is_active:
    return True  # 激活用户才能访问系统


# ============================================
# 反模式 9: 硬编码配置
# ============================================

# ❌ 硬编码配置值
def connect_database():
    connection = psycopg2.connect(
        host="localhost",
        port=5432,
        database="mydb",
        user="admin",
        password="secretpassword"
    )
    return connection


# ✅ 应该使用配置文件或环境变量
def connect_database():
    """连接数据库"""
    config = load_config()
    connection = psycopg2.connect(
        host=config.db_host,
        port=config.db_port,
        database=config.db_name,
        user=config.db_user,
        password=config.db_password
    )
    return connection


# ============================================
# 反模式 10: 过深的继承
# ============================================

# ❌ 过深的继承层次
class Animal:
    pass

class Mammal(Animal):
    pass

class Dog(Mammal):
    pass

class GoldenRetriever(Dog):
    pass

class BabyGoldenRetriever(GoldenRetriever):
    pass


# ✅ 应该使用组合或扁平化继承
class Animal:
    pass

class Dog(Animal):
    pass

class GoldenRetriever(Dog):
    pass

# 使用装饰器或其他模式来添加功能
class GoldenRetrieverPuppy:
    def __init__(self, golden_retriever: GoldenRetriever):
        self.dog = golden_retriever
