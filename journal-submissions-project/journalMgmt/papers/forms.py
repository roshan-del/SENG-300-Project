from django import forms
from django.conf import settings
from .models import Papers, Comments
from django.contrib.auth.models import User


# Form to format the 'upload/submit paper' button
class SubmitButton(forms.ModelForm):
    preferred_reviewers = forms.CharField(widget=forms.Textarea)

    # form takes a paper object and displays a place for the title and file
    class Meta:
        model = Papers
        fields = ('paper_title', 'publication', 'paper_file', 'paper_abstract', 'preferred_reviewers',)


class CommentBox(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Comments
        fields = ('comment',)


class RecommendedForm(forms.Form):
    name = forms.CharField(label='Suggest reviewer',
                           max_length=120)


class ReviewerPaper(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={'rows': 10, 'cols': 100}))

    class Meta:
        model = Comments
        fields = ('comment',)


# table used to display options for ChangeStatus form
ACCEPTED = 'Accepted'
REJECTED = 'Rejected'
PENDING = 'Pending'
STATUS_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Rejected', 'Rejected'),
    ('Pending', 'Pending'),
)


# form is used to update the status of a paper
class ChangeStatus(forms.ModelForm):
    # form takes a paper object as input and displays a drop down menu of options to change the paper's status
    class Meta:
        model = Papers
        fields = ['paper_status']


# form is used to assign a reviewer to a paper 
class AssignReviewerForm(forms.ModelForm):
    class Meta:
        model = Papers
        fields = ['reviewer_1', 'reviewer_2', 'reviewer_3', 'paper_status']

    def __init__(self, *args, **kwargs):
        super(AssignReviewerForm, self).__init__(*args, **kwargs)
        self.fields['reviewer_1'].queryset = User.objects.filter(groups__name='Reviewer')
        self.fields['reviewer_2'].queryset = User.objects.filter(groups__name='Reviewer')
        self.fields['reviewer_3'].queryset = User.objects.filter(groups__name='Reviewer')