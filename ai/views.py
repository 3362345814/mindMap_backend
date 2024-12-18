from django.http import StreamingHttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import ModelConfiguration
from .serializers import ModelConfigurationSerializer
from .utils import generate_node_explanation, generate_node_explanation_stream, generate_choice_questions, \
    generate_subjective_questions, generate_true_or_false_questions, generate_child_nodes, test_openai_connection


class NodeExplanationView(APIView):
    def post(self, request, *args, **kwargs):
        node_data = request.data.get("node_data")
        if not node_data:
            return Response({"error": "Node data is required"}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        api_key = user.api_key
        model_configuration_id = user.model_configuration_id
        custom_base_url = user.custom_base_url
        custom_model = user.custom_model
        model_selection_status = user.model_selection_status

        # 生成节点解释
        if model_selection_status == 'default':
            explanation = generate_node_explanation(node_data)
        elif model_selection_status == 'select':
            model_configuration = ModelConfiguration.objects.get(pk=model_configuration_id)
            explanation = generate_node_explanation(node_data, api_key=api_key, base_url=model_configuration.base_url,
                                                    model=model_configuration.model)
        elif model_selection_status == 'custom':
            explanation = generate_node_explanation(node_data, api_key=api_key, base_url=custom_base_url,
                                                    model=custom_model)
        if "error" in explanation:
            status_code = explanation.get("status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response({"error": explanation["error"]}, status=status_code)
        return Response(explanation, status=status.HTTP_200_OK)


class NodeExplanationStreamView(APIView):
    def post(self, request, *args, **kwargs):
        node_data = request.data.get("node_data")
        ancestors_data = request.data.get("ancestors_data")
        if not node_data:
            return Response({"error": "Node data is required"}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        api_key = user.api_key
        model_configuration_id = user.model_configuration_id
        custom_base_url = user.custom_base_url
        custom_model = user.custom_model
        model_selection_status = user.model_selection_status

        # 生成节点解释
        if model_selection_status == 'default':
            # 创建一个生成器来生成流式文本
            def generate():
                # 使用生成器逐步返回数据
                for part in generate_node_explanation_stream(node_data, ancestors_data):
                    # print(part, end="")
                    yield part  # yield 每一部分文本
        elif model_selection_status == 'select':
            model_configuration = ModelConfiguration.objects.get(pk=model_configuration_id)
            try:
                test_openai_connection(api_key, model_configuration.base_url, model_configuration.model)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            def generate():
                for part in generate_node_explanation_stream(node_data, ancestors_data, api_key,
                                                             model_configuration.base_url, model_configuration.model):
                    yield part
        elif model_selection_status == 'custom':
            try:
                test_openai_connection(api_key, custom_base_url, custom_model)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            def generate():
                for part in generate_node_explanation_stream(node_data, ancestors_data, api_key,
                                                             custom_base_url, custom_model):
                    yield part
        # 使用 StreamingHttpResponse 将数据流返回给前端
        return StreamingHttpResponse(generate(), content_type="text/plain")


class GenerateChoiceQuestionsView(APIView):
    def post(self, request, *args, **kwargs):
        text = request.data.get("text")
        if not text:
            return Response({"error": "Text is required"}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        api_key = user.api_key
        model_configuration_id = user.model_configuration_id
        custom_base_url = user.custom_base_url
        custom_model = user.custom_model
        model_selection_status = user.model_selection_status


        if model_selection_status == 'default':
            # 调用生成选择题的函数
            result = generate_choice_questions(text)
        elif model_selection_status == 'select':
            model_configuration = ModelConfiguration.objects.get(pk=model_configuration_id)
            result = generate_choice_questions(text, api_key, model_configuration.base_url, model_configuration.model)
        elif model_selection_status == 'custom':
            result = generate_choice_questions(text, api_key, custom_base_url, custom_model)

        # 如果返回的是错误信息，直接返回
        if "error" in result:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

        # 返回生成的题目
        return Response(result, status=status.HTTP_200_OK)


class GenerateSubjectiveQuestionsView(APIView):
    def post(self, request, *args, **kwargs):
        text = request.data.get("text")
        if not text:
            return Response({"error": "Node data is required"}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        api_key = user.api_key
        model_configuration_id = user.model_configuration_id
        custom_base_url = user.custom_base_url
        custom_model = user.custom_model
        model_selection_status = user.model_selection_status


        if model_selection_status == 'default':
            # 调用生成主观题的函数
            result = generate_subjective_questions(text)
        elif model_selection_status == 'select':
            model_configuration = ModelConfiguration.objects.get(pk=model_configuration_id)
            result = generate_subjective_questions(text, api_key, model_configuration.base_url, model_configuration.model)
        elif model_selection_status == 'custom':
            result = generate_subjective_questions(text, api_key, custom_base_url, custom_model)

        # 如果返回的是错误信息，直接返回
        if "error" in result:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

        # 返回生成的题目
        return Response(result, status=status.HTTP_200_OK)


class GenerateTrueOrFalseQuestionsView(APIView):
    def post(self, request, *args, **kwargs):
        text = request.data.get("text")
        if not text:
            return Response({"error": "Node data is required"}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        api_key = user.api_key
        model_configuration_id = user.model_configuration_id
        custom_base_url = user.custom_base_url
        custom_model = user.custom_model
        model_selection_status = user.model_selection_status


        if model_selection_status == 'default':
            # 调用生成判断题的函数
            result = generate_true_or_false_questions(text)
        elif model_selection_status == 'select':
            model_configuration = ModelConfiguration.objects.get(pk=model_configuration_id)
            result = generate_true_or_false_questions(text, api_key, model_configuration.base_url, model_configuration.model)
        elif model_selection_status == 'custom':
            result = generate_true_or_false_questions(text, api_key, custom_base_url, custom_model)

        # 如果返回的是错误信息，直接返回
        if "error" in result:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

        # 返回生成的题目
        return Response(result, status=status.HTTP_200_OK)


class GenerateChildNodesView(APIView):
    def post(self, request, *args, **kwargs):
        parent_content = request.data.get("parent_content")
        ancestors_content = request.data.get("ancestors_content")
        if not parent_content:
            return Response({"error": "Parent content is required"}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        api_key = user.api_key
        model_configuration_id = user.model_configuration_id
        custom_base_url = user.custom_base_url
        custom_model = user.custom_model
        model_selection_status = user.model_selection_status


        if model_selection_status == 'default':
            # 调用生成子节点的函数
            result = generate_child_nodes(parent_content, ancestors_content)
        elif model_selection_status == 'select':
            model_configuration = ModelConfiguration.objects.get(pk=model_configuration_id)
            result = generate_child_nodes(parent_content, ancestors_content, api_key,
                                          model_configuration.base_url, model_configuration.model)
        elif model_selection_status == 'custom':
            result = generate_child_nodes(parent_content, ancestors_content, api_key, custom_base_url, custom_model)

        # 如果返回的是错误信息，直接返回
        if "error" in result:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

        # 返回生成的子节点
        return Response(result, status=status.HTTP_200_OK)


class ModelConfigurationListView(APIView):
    def get(self, request, *args, **kwargs):
        # 获取所有模型配置数据
        model_configurations = ModelConfiguration.objects.all()

        # 使用序列化器将数据转为 JSON 格式
        serializer = ModelConfigurationSerializer(model_configurations, many=True)

        # 返回 JSON 数据
        return Response(serializer.data, status=status.HTTP_200_OK)