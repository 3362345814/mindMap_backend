import json
from openai import OpenAI
import openai

model = "qwen-max"
key = "sk-6096ec4a8ea346248d4b292ebec7c342"
url = "https://dashscope.aliyuncs.com/compatible-mode/v1"


def test_openai_connection(api_key, base_url, model):
    try:
        client = OpenAI(
            api_key=api_key,
            base_url=base_url,
        )
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {'role': 'system', 'content': 'Test connection, just reply with 1'},
                {'role': 'user', 'content': 'Test connection, just reply with 1'},
            ]
        )
        return True  # 连接成功
    except Exception as e:
        raise ValueError(f"{str(e)}")

def generate_node_explanation(node_data, api_key=key, base_url=url, model=model):
    try:
        client = OpenAI(
            api_key=api_key,
            base_url=base_url,
        )
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {'role': 'system', 'content': '请为以下内容生成解释,使用markdown语法：'},
                {'role': 'user', 'content': node_data}],
        )
        return completion.choices[0].message.content
    except Exception as e:
        return {"error": f"{str(e)}", "status_code": 500}


def generate_node_explanation_stream(node_data, ancestors_data, api_key=key, base_url=url, model=model):
    try:
        client = OpenAI(
            api_key=api_key,
            base_url=base_url,
        )
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {'role': 'system', 'content': '请为思维导图的当前节点内容生成解释,使用markdown语法，400字左右，开头有标题，将以下内容作为标题：'},
                {'role': 'user', 'content': '当前节点：' + node_data + '当前节点的祖先节点列表：' + str(ancestors_data)}
            ],
            stream=True  # 启用流式返回
        )

        # 遍历并逐步返回生成的文本
        for chunk in completion:
            yield chunk.choices[0].delta.content  # 按块返回内容
    except Exception as e:
        print(e)
        return {"error": f"{str(e)}", "status_code": 500}



def generate_choice_questions(text, api_key=key, base_url=url, model=model):
    try:
        client = OpenAI(
            api_key=api_key,
            base_url=base_url,
        )

        # 创建请求消息，要求生成选择题
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {'role': 'system', 'content': '根据以下知识点内容生成5个选择题，每个选择题包括1个问题，4个选项和正确答案, '
                                              '答案为正确答案的索引，格式为{"questions_and_answers": ['
                                              '{"question": "什么是牛顿第二定律？", '
                                              '"options": ["F = mv", "F = ma", "F = m/v", "F = m^2"], '
                                              '"answer": 1}, '
                                              '{"question": "牛顿第三定律的内容是什么？", '
                                              '"options": ["每个作用力都有一个反作用力", "物体沿直线加速", "质量守恒定律", "引力作用"], '
                                              '"answer": 0}]} '
                                              '请用以上格式返回题目内容。'
                 },
                {'role': 'user', 'content': text}
            ]
        )

        # 获取返回的文本内容
        generated_text = completion.choices[0].message.content

        try:
            # 解析生成的文本为JSON对象
            questions_and_answers = json.loads(generated_text)
            return questions_and_answers
        except json.JSONDecodeError as e:
            return {"error": "无法解析返回的JSON", "details": str(e)}
    except Exception as e:
        return {"error": f"{str(e)}", "status_code": 500}

def generate_subjective_questions(text, api_key=key, base_url=url, model=model):
    try:
        client = OpenAI(
            api_key=api_key,
            base_url=base_url,
        )

        # 创建请求消息，要求生成主观题
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {'role': 'system', 'content': '根据以下知识点内容生成5个主观题，每个问题包括问题本身和答案，'
                                              '请返回每个问题及其答案的JSON格式，格式如下：'
                                              '{"questions_and_answers": ['
                                              '{"question": "什么是牛顿第二定律？", '
                                              '"answer": "牛顿第二定律是描述物体运动的一个定律，表达式为 F = ma，其中 F 为作用力，m 为物体的质量，a 为物体的加速度。"},'
                                              '{"question": "牛顿第三定律的内容是什么？", '
                                              '"answer": "牛顿第三定律描述的是每个作用力都有一个反作用力，且方向相反，大小相等。"}]} '
                                              '请使用以上格式返回主观题内容。'
                 },
                {'role': 'user', 'content': text}
            ]
        )

        # 获取返回的文本内容
        generated_text = completion.choices[0].message.content

        try:
            # 解析生成的文本为JSON对象
            questions_and_answers = json.loads(generated_text)
            return questions_and_answers
        except json.JSONDecodeError as e:
            return {"error": "无法解析返回的JSON", "details": str(e)}
    except Exception as e:
        return {"error": f"{str(e)}", "status_code": 500}

def generate_true_or_false_questions(text, api_key=key, base_url=url, model=model):
    try:
        client = OpenAI(
            api_key=api_key,
            base_url=base_url,
        )

        # 创建请求消息，要求生成判断题
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {'role': 'system', 'content': '根据以下知识点内容生成5个判断题，每个题目包括陈述内容和答案，0为正确，1为错误'
                                              '请返回每个题目和答案的JSON格式，格式如下：'
                                              '{"questions_and_answers": ['
                                              '{"question": "牛顿第二定律是 F = ma。", '
                                              '"options": ["正确", "错误"], '
                                              '"answer": 0},'
                                              '{"question": "牛顿第三定律描述的是物体的加速。", '
                                              '"options": ["正确", "错误"], '
                                              '"answer": 1}]}'
                                              '请使用以上格式返回判断题内容。'
                 },
                {'role': 'user', 'content': text}
            ]
        )

        # 获取返回的文本内容
        generated_text = completion.choices[0].message.content

        try:
            # 解析生成的文本为JSON对象
            questions_and_answers = json.loads(generated_text)
            return questions_and_answers
        except json.JSONDecodeError as e:
            return {"error": "无法解析返回的JSON", "details": str(e)}
    except Exception as e:
        return {"error": f"{str(e)}", "status_code": 500}


def generate_child_nodes(parent_content, ancestors_content, api_key=key, base_url=url, model=model):
    try:
        client = OpenAI(
            api_key=api_key,
            base_url=base_url,
        )

        # 请求 AI 生成子节点
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {'role': 'system', 'content': '根据给定的当前节点内容以及祖先节点列表生成当前节点的子节点，'
                                              '返回JSON格式为：{"child_nodes": ["子节点1内容","子节点2内容"]}'
                                              '请用以上格式返回数据。'},
                {'role': 'user', 'content': '当前节点：' + parent_content + '当前节点的祖先节点列表：' + str(ancestors_content)}
            ]
        )

        # 获取返回的文本内容
        generated_text = completion.choices[0].message.content

        try:
            # 解析生成的文本为JSON对象
            child_nodes = json.loads(generated_text)
            return child_nodes
        except json.JSONDecodeError as e:
            print(generated_text)
            return {"error": "这个节点内容不能再生成了，请尝试其他节点或修改节点内容。", "details": str(e)}
    except Exception as e:
        return {"error": f"{str(e)}", "status_code": 500}