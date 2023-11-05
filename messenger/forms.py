from django import forms
from .models import Message

INPUT_CLASSES = 'block w-full p-2 text-sm text-gray-900 border border-violet-300 rounded-lg bg-violet-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-violet-700 dark:border-violet-600 dark:placeholder-gray-200 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': INPUT_CLASSES
            })
        }