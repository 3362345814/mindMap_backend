from django.urls import path
from .views import NodeExplanationView, NodeExplanationStreamView, GenerateChoiceQuestionsView, \
    GenerateSubjectiveQuestionsView, GenerateTrueOrFalseQuestionsView, GenerateChildNodesView, \
    ModelConfigurationListView

urlpatterns = [
    path('explanation/', NodeExplanationView.as_view(), name='explanation'),
    path('stream-explanation/', NodeExplanationStreamView.as_view(), name='stream-explanation'),
    path('generate-choice-questions/', GenerateChoiceQuestionsView.as_view(), name='generate-choice-questions'),
    path('generate-subjective-questions/', GenerateSubjectiveQuestionsView.as_view(), name='generate-subjective-questions'),
    path('generate-true-or-false-questions/', GenerateTrueOrFalseQuestionsView.as_view(), name='generate-true-or-false-questions'),
    path('generate-child-nodes/', GenerateChildNodesView.as_view(), name='generate-child-nodes'),
    path('model-configurations/', ModelConfigurationListView.as_view(), name='model_configuration_list'),
]