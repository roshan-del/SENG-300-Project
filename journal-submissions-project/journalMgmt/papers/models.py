from django.conf import settings
from django.db import models
from django.conf import settings


# Model class used to define journal (groups of papers to be published together)
class Journal(models.Model):
    journal_editor = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)

    journal_title = models.CharField(max_length=255)

    journal_deadline = models.DateTimeField()

    journal_publication_date = models.DateTimeField()

    def __str__(self):
        return self.journal_title

# Model class used to define papers (individual works by an author for inclusion in a journal)
class Papers(models.Model):

    paper_author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="paper_written_by", on_delete=models.CASCADE)
    reviewer_1 = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, related_name="paper_reviewed_by_1", on_delete=models.SET_NULL, null=True)
    reviewer_2 = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, related_name="paper_reviewed_by_2", on_delete=models.SET_NULL, null=True)
    reviewer_3 = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, related_name="paper_reviewed_by_3", on_delete=models.SET_NULL, null=True)

    paper_title = models.CharField(max_length=255)
    publication = models.ForeignKey(Journal, on_delete=models.CASCADE)

    # uploads file to ../papers folder
    paper_file = models.FileField(upload_to='papers/')
    paper_abstract = models.FileField(upload_to='papers/')

    upload_date = models.DateTimeField(auto_now_add=True)

    # used for authors to ask for specific reviewers 
    preferred_reviewers = models.CharField(max_length=1000, default='')

    num_assigned_user =  models.IntegerField(default=0)

    # defines the paper's status as accepted, in review, or rejected
    ACCEPTED = 'Accepted'
    REJECTED = 'Rejected'
    PENDING = 'Pending'
    STATUS_CHOICES = (
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
        ('Pending', 'Pending'),
    )
    paper_status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=PENDING)


    def __str__(self):
        return self.paper_title



# Model class used to define comments (notes left by reviewers on particular papers)
class Comments(models.Model):
    comment_paper = models.ForeignKey(Papers, default='4', on_delete=models.CASCADE)

    comment_author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    comment = models.CharField(max_length=10000)

    comment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

