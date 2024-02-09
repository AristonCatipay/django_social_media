from django import forms
from .models import Region, Province, City_Municipality, Barangay

INPUT_CLASSES = 'rounded-r-lg bg-gray-50 border border-gray-300 text-gray-900 focus:ring-blue-500 focus:border-blue-500 block flex-1 min-w-0 w-full text-sm p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
SELECT_AREA = 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
TEXT_AREA = 'block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
FOR_IMAGE = 'block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400'
CHECKBOX = 'w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 dark:focus:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600'

class RegionForm(forms.ModelForm):
    class Meta:
        model = Region
        fields = ('name', 'psgc_code', 'region_code')
        widgets = {
            'region_code': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder' : "Enter region code",
            }),
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder' : "Enter region name",
            }),
            'psgc_code': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder' : "Enter PSGC code",
            }),
        }

class ProvinceForm(forms.ModelForm):
    class Meta:
        model = Province
        fields = ('name', 'province_code', 'psgc_code', 'region')
        widgets = {
            'province_code': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder' : "Enter region code",
            }),
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder' : "Enter province name",
            }),
            'psgc_code': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder' : "Enter PSGC code",
            }),
            'region': forms.Select(attrs={
                'class': SELECT_AREA,
            }),
        }