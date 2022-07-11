from django import forms
from blog.models import Post,Comment

class PostForm(forms.ModelForm):

# Connet Model. Connect Fields you want to be able to edit in this form.
    class Meta():
        model = Post
        fields = ('author','title','text')

# Add Widgets so you can grab a particular field Widget. Inside Meta Class.
# THIS IS HOW YOU CONNECT WIDGETS TO CSS STYLING
# Text below is connected to 3 classes
# Our created classes: textinputclass, postcontent
# Other two classes are NOT OURS
        widgets = {
            'title':forms.TextInput(attrs={'class':'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'})
        }

class CommentForm(forms.ModelForm):

    class Meta():
        model = Comment
        fields = ('author','text')

        widgets = {
            'author':forms.TextInput(attrs={'class':'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea'})
        }
