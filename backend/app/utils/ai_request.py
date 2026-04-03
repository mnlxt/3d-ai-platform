import requests
import httpx
import json
import re
from app.core.config import settings
from typing import Optional, Dict, Any

def stable_diffusion_request(prompt: str) -> Optional[Dict]:
    """调用Stable Diffusion API生成图片"""
    if not settings.STABLE_DIFFUSION_API_KEY:
        raise ValueError("Stable Diffusion API Key未配置")
    
    url = f"{settings.STABLE_DIFFUSION_BASE_URL}/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
    headers = {
        "Authorization": f"Bearer {settings.STABLE_DIFFUSION_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "text_prompts": [{"text": prompt, "weight": 1}],
        "width": 1024,
        "height": 1024,
        "steps": 30
    }
    
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()  # 抛出HTTP错误
    return response.json()

async def ollama_semantic_parse(text: str) -> Optional[Dict[str, Any]]:
    """
    使用 Ollama 本地模型进行异步语义解析
    优化点：异步请求 + 严格 JSON 提取策略
    """
    url = f"{settings.OLLAMA_BASE_URL}/api/generate"
    
    # 强化提示词：要求输出纯净 JSON，不要任何解释
    system_prompt = (
        "You are a 3D AI Assistant. Task: Parse user text into 3D generation parameters. "
        "Output MUST be a valid JSON object. No conversation, no markdown blocks."
    )
    
    payload = {
        "model": settings.DEFAULT_LLM_MODEL,
        "prompt": f"{system_prompt}\nUser Text: {text}",
        "format": "json", # Ollama 原生支持强制 JSON 输出
        "stream": False
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            raw_data = response.json()
            
            content = raw_data.get("response", "")
            
            # 稳健性处理：防止 LLM 返回非纯净 JSON（如包含 Markdown 标签）
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            return json.loads(content)
            
    except Exception as e:
        print(f"Ollama Error: {str(e)}")
        return None