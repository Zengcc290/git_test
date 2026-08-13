"""Ask the controlled-fact question without supplying retrieval context."""

from knowledge_search.rag.llm_client import LLMClient


QUESTION = (
    "雾港棱镜项目的内部识别码、封存日期和地点、封存口令、冷却液目标温度、"
    "传感器校准序列、二级断电应急通道及最终状态分别是什么？"
)


def main() -> int:
    client = LLMClient.from_env()
    response = client.complete(
        [
            {
                "role": "system",
                "content": (
                    "你没有知识库或检索上下文。只能依据已有知识回答；"
                    "不知道就明确说不知道，不得猜测。"
                ),
            },
            {"role": "user", "content": QUESTION},
        ],
        temperature=0,
    )
    print(response.content)
    print(
        "TOKEN_USAGE "
        f"prompt={response.usage.prompt_tokens} "
        f"completion={response.usage.completion_tokens} "
        f"total={response.usage.total_tokens}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
