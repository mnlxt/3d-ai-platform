import asyncio
import time
from app.utils.ai_request import ollama_semantic_parse

async def test_semantic_parse():
    """测试语义解析功能"""
    test_texts = [
        "创建一个蓝色头发的女性角色，穿着科幻盔甲",
        "设计一个中世纪骑士，手持长剑和盾牌",
        "生成一个可爱的卡通熊猫形象，戴着红色帽子",
        "设计一个未来风格的机器人，具有发光的蓝色眼睛"
    ]
    
    for text in test_texts:
        print(f"\n测试文本: {text}")
        start_time = time.time()
        result = await ollama_semantic_parse(text)
        end_time = time.time()
        
        print(f"处理时间: {end_time - start_time:.2f} 秒")
        print(f"解析结果: {result}")

if __name__ == "__main__":
    asyncio.run(test_semantic_parse())
