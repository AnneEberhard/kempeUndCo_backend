from django.db import models
from accounts.models import CustomUser
from infos.models import Info
from recipes.models import Recipe


class Comment(models.Model):
    """
    Represents a comment made by a user.

    This model captures user comments which can be associated with either an `Info` or a `Recipe`. Each comment has the following attributes:

    Fields:
        - `content`: A text field for the content of the comment.
        - `author`: A foreign key linking to the `CustomUser` model, indicating the user who made the comment.
        - `created_at`: A timestamp for when the comment was created, automatically set when the comment is first saved.
        - `updated_at`: A timestamp for when the comment was last updated, automatically updated each time the comment is saved.
        - `info`: An optional foreign key linking to the `Info` model, used if the comment is associated with an `Info` object.
        - `recipe`: An optional foreign key linking to the `Recipe` model, used if the comment is associated with a `Recipe` object.

    Methods:
        - `__str__(self)`: Returns a string representation of the comment, including the author and creation timestamp.
    """
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Link with Info and Recipe, optional, as only one will be used.
    info = models.ForeignKey(Info, null=True, blank=True, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"Comment by {self.author} on {self.created_at}"
