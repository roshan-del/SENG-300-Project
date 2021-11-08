from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Q
from .forms import SubmitButton, ReviewerPaper, ChangeStatus, AssignReviewerForm, CommentBox
from .models import Comments, Papers, Journal


# view used to display new user registration page
def registration_page(request):
    form = UserCreationForm(request.POST or None)

    # upon post request, attempt to create new user with credentials given in form
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password 1')
            user = authenticate(user=username, password=password)
            login(request, user)
            g = Group.objects.get(name='Researcher')  # Every user that registers is a researcher
            g.user_set.add(request.user)  # Add new user to researcher group
            msg = "Hello " + str(request.user) + ", welcome to your account! " # Welcome message 
            messages.add_message(request, messages.SUCCESS, msg)                 
            return redirect('/home/') 

        # upon invalid form data return user to registration page
        else:
            return render(request, 'papers/signup.html', {'form': form})

    # show signup page on all other kinds of requests
    else:
        form = UserCreationForm()
        return render(request, 'papers/signup.html', {'form': form})


# view used to display the login page
def login_page(request):
    if request.user.is_authenticated:
        return redirect('/home/')

    # upon POST request, get username and password from the html form and attempt authentication
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        # if a user with those credentials is authenticated successfully, redirect to the dashboard
        if user is not None:
            login(request, user)
            papers = Papers.objects.all()
            for paper in papers:
                if ((paper.paper_author == request.user) and (paper.paper_status == 'Accepted')):
                    print('Test passed')
                    message = str(paper.paper_title) + " has been accepted!"
                    messages.add_message(request, messages.INFO, message)
            return redirect('/home/')

        # else leave the user on the login page
        else:
            messages.error(request, "Your password or username is incorrect")
            form = AuthenticationForm(request.POST)
            return render(request, 'papers/login.html', {'form': form})

    # upon other requests, simply display site with form
    else:
        form = AuthenticationForm(request.POST)
        return render(request, 'papers/login.html', {'form': form})


def logout_page(request):
    logout(request)
    return redirect('/')


@login_required
def home(request):
    # get logged-in user, and determine their user groups
    current_user = request.user
    is_researcher = current_user.groups.filter(name='Researcher').exists()
    is_reviewer = current_user.groups.filter(name='Reviewer').exists()
    is_editor = current_user.groups.filter(name='Editor').exists()

    # print a list of the groups the logged-in user is a member of
    print(current_user.groups.all())
    return render(request, 'papers/home.html',
                  {'is_reviewer': is_reviewer, 'is_researcher': is_researcher, 'is_editor': is_editor})


@login_required
def publications(request):
    # get logged-in user, and determine their user groups
    current_user = request.user
    is_researcher = current_user.groups.filter(name='Researcher').exists()
    is_reviewer = current_user.groups.filter(name='Reviewer').exists()
    is_editor = current_user.groups.filter(name='Editor').exists()

    return render(request, 'papers/publications.html',
                  {'is_reviewer': is_reviewer, 'is_researcher': is_researcher, 'is_editor': is_editor})


@login_required
def staff(request):
    # get logged-in user, and determine their user groups
    current_user = request.user
    is_researcher = current_user.groups.filter(name='Researcher').exists()
    is_reviewer = current_user.groups.filter(name='Reviewer').exists()
    is_editor = current_user.groups.filter(name='Editor').exists()
    return render(request, 'papers/staff.html',
                  {'is_reviewer': is_reviewer, 'is_researcher': is_researcher, 'is_editor': is_editor})


# view for the main user account area (not specific to a particular user group)
@login_required
def account(request):
    # get logged-in user, and determine their user groups
    current_user = request.user

    # get logged-in user, and determine their user groups
    current_user = request.user
    is_researcher = current_user.groups.filter(name='Researcher').exists()
    is_reviewer = current_user.groups.filter(name='Reviewer').exists()
    is_editor = current_user.groups.filter(name='Editor').exists()

    return render(request, 'papers/account.html',
                  {'is_reviewer': is_reviewer, 'is_researcher': is_researcher, 'is_editor': is_editor})


# view for the reseacher-specific dashboard
# view will only load for users who are logged-in, and are in the 'Researcher' group
@login_required
@user_passes_test(lambda u: u.groups.filter(name='Researcher').exists())
# view for the researcher-specific dashboard
# view will only load for users who are logged-in, and are in the 'Researcher' group
@login_required
@user_passes_test(lambda u: u.groups.filter(name='Researcher').exists())
def researcher_account(request):
    current_user = request.user

    is_researcher = current_user.groups.filter(name='Researcher').exists()

    # list of papers with the current user as the author
    user_papers = Papers.objects.filter(paper_author=current_user).order_by('upload_date')

    return render(request, 'papers/researcher_account.html',
                  {'is_researcher': is_researcher, 'user_papers': user_papers})


# view for showing a researcher's submissions
@login_required
@user_passes_test(lambda u: u.groups.filter(name='Researcher').exists())
def submission_history(request):
    # get logged-in user, and determine their user groups
    current_user = request.user
    is_researcher = current_user.groups.filter(name='Researcher').exists()
    is_reviewer = current_user.groups.filter(name='Reviewer').exists()
    is_editor = current_user.groups.filter(name='Editor').exists()

    is_researcher = current_user.groups.filter(name='Researcher').exists()
    # list of papers with the current user as the author

    user_papers = Papers.objects.filter(paper_author=current_user).order_by('upload_date')

    return render(request, 'papers/submission_history.html',
                  {'is_researcher': is_researcher, 'user_papers': user_papers,})


# view for authors to view their uploaded work
@login_required
@user_passes_test(lambda u: u.groups.filter(name='Researcher').exists())
def update_paper(request, id):
    paper = Papers.objects.get(id=id)

    comments = Comments.objects.filter(comment_paper=paper).order_by('comment_date')
    print (comments)

    return render(request, 'papers/update_paper.html', {'paper': paper, 'comments': comments})


# view for the reviewer-specific dashboard
# view will only load for users who are logged-in, and are in the 'Reviewer' group
@login_required
@user_passes_test(lambda u: u.groups.filter(name='Reviewer').exists())
def reviewer_account(request):
    # get logged-in user, and determine their user groups
    current_user = request.user
    is_reviewer = current_user.groups.filter(name='Reviewer').exists()

    reviewer_comments = Comments.objects.filter(comment_author=current_user).order_by('comment_date')

    # fetch a list of all pending papers where current user is reviewer_1, reviewer_2, or reviewer_3
    papers = Papers.objects.filter(Q(reviewer_1=current_user) | Q(reviewer_2=current_user) | Q(reviewer_3=current_user)).filter(paper_status='Pending')

    context = {
        'current_user': current_user,
        'is_reviewer': is_reviewer,
        'reviewer_comments': reviewer_comments,
        'papers': papers,

    }
    return render(request, 'papers/reviewer_account.html', context)


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Reviewer').exists())
def assigned_papers(request):
    # get logged-in user, and determine their user groups
    current_user = request.user
    is_reviewer = current_user.groups.filter(name='Reviewer').exists()

    reviewer_comments = Comments.objects.filter(comment_author=current_user).order_by('comment_date')

    papers = Papers.objects.filter(paper_status='Pending')

    if request.method == 'POST':
        comment_form = ReviewerPaper(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.comment_author = request.user
            comment.upload_date = timezone.now()
            comment.save()
            print("Author: ", comment.comment_author)
            print("Time: ", comment.upload_date)
        else:
            print("1")
    else:
        comment_form = ReviewerPaper()

    context = {
        'is_reviewer': is_reviewer,
        'reviewer_comments': reviewer_comments,
        'papers': papers,
        'comment_form': comment_form,
    }

    return render(request, 'papers/assigned_papers.html', context)


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Reviewer').exists())
def submit_comment(request, id):
    # get logged-in user, and determine their user groups
    current_user = request.user
    is_reviewer = current_user.groups.filter(name='Reviewer').exists()

    paper = Papers.objects.get(id=id)

    if request.method == 'POST':
        comment_form = ReviewerPaper(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.comment_author = request.user
            comment.upload_date = timezone.now()
            comment.save()
            print("Author: ", comment.comment_author)
            print("Time: ", comment.upload_date)
        else:
            print("1")
    else:
        comment_form = ReviewerPaper()

    return render(request, 'papers/reviewer_account.html')


# View to allow a reviewer to comment on and make recommendations about a paper
# view will only load for users who are logged-in and are in the 'Reviewer' group
@login_required
@user_passes_test(lambda u: u.groups.filter(name='Reviewer').exists())
def review_paper(request, id):
    paper = Papers.objects.get(id=id)
    
    if request.method == 'POST':
        comment_form = ReviewerPaper(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.comment_paper = paper
            comment.comment_author = request.user
            comment.upload_date = timezone.now()
            comment.save()
            print("Author: ", comment.comment_author)
            print("Time: ", comment.upload_date)
        else:
            print("1")
    else:
        comment_form = ReviewerPaper()

    context = {
        'paper': paper,
        'comment_form': comment_form
    }
    return render(request, 'papers/review_paper.html', context)

# view for the editor-specific dashboard
# view will only load for users who are logged-in, and are in the 'Editor' group
@login_required
@user_passes_test(lambda u: u.groups.filter(name='Editor').exists())
def editor_account(request):
    # get logged-in user, and determine their user groups
    current_user = request.user
    is_editor = current_user.groups.filter(name='Editor').exists()

    return render(request, 'papers/editor_account.html', {'is_editor': is_editor})


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Editor').exists())
def editor_papers(request):
    # get logged-in user, and determine their user groups
    current_user = request.user
    is_editor = current_user.groups.filter(name='Editor').exists()

    # get list of all journals with this user as the editor
    user_journals = Journal.objects.filter(journal_editor=current_user)

    # get list of papers
    papers = Papers.objects.all()

    # create form for changing status of papers
    status_form = ChangeStatus

    return render(request, 'papers/editor_papers.html',
                  {'status_form': status_form, 'user_journals': user_journals, 'papers': papers,
                   'is_editor': is_editor})


# view to allow editor to see information about a journal
# takes as input an http request and the id of a journal it should load
@login_required
@user_passes_test(lambda u: u.groups.filter(name='Editor').exists())
def journal(request, id):
    journal = Journal.objects.get(id=id)

    papers = Papers.objects.all()

    return render(request, 'papers/journal.html', {'journal': journal, 'papers': papers})


# view to allow editor to change reviewers of papers
# takes as input an http requet and the id of the paper it should load


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Editor').exists())
def assign_reviewer(request, id):
    current_user = request.user
    is_researcher = current_user.groups.filter(name='Researcher').exists()
    is_reviewer = current_user.groups.filter(name='Reviewer').exists()
    is_editor = current_user.groups.filter(name='Editor').exists()
    paper = Papers.objects.get(id=id) # 
    sug_revs = str(paper.preferred_reviewers).split(",")  # Name of suggested authors
    if request.method == "POST":
        form = AssignReviewerForm(request.POST, instance=paper)
        form.save()
        ass_revs = [paper.reviewer_1, paper.reviewer_2, paper.reviewer_3]
        paper.num_assigned_user = 0 # Set number of assigned users to zero 
        for ass_rev in ass_revs:
            # Check if the reviewer has been assigned to the paper 
            if (ass_rev != None):
                # If they have, then increment the number of users reviewing this paper by 1 
                paper.num_assigned_user = paper.num_assigned_user + 1
        paper.save()
        # Display message that the editor has updated 
        messages.add_message(request, messages.SUCCESS, "Updated successfully!")

    else:
        form = AssignReviewerForm(instance=paper)

    context = {
        'paper': paper,
        'form': form,
        'sug_revs': sug_revs,
        'is_reviewer': is_reviewer,
        'is_researcher': is_researcher,
        'is_editor': is_editor
    }
    return render(request, 'papers/assign_reviewer.html', context, )


#######################################################################

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Editor').exists())
def accept_paper(request):
    return render(request)


@login_required
# view dealing with 'submit a paper' page
def submit(request):
    # get logged-in user, and determine their user groups
    current_user = request.user
    is_researcher = current_user.groups.filter(name='Researcher').exists()
    is_reviewer = current_user.groups.filter(name='Reviewer').exists()
    is_editor = current_user.groups.filter(name='Editor').exists()

    # creating a submit button

    # save user uploaded form when post request is made with valid input
    if request.method == 'POST':
        form = SubmitButton(request.POST, request.FILES)
        # set the paper_author field to be the currently logged-in user
        # set the upload_date field to be the time of upload
        if form.is_valid():
            paper = form.save(commit=False)
            paper.paper_author = request.user
            paper.upload_date = timezone.now()
            paper.save()
            messages.add_message(request, messages.SUCCESS, "Uploaded successfully!")

    # if the page receives a GET request, submit button should still appear
    else:
        form = SubmitButton()      

    # return the html file used to display the page, with the form to be used
    return render(request, 'papers/submit.html', {'form': form, 'is_researcher': is_researcher})


@login_required
def submissions(request):
    # GET request for papers user has submitted

    # if request.method == 'GET':

    # else:

    return render(request, 'papers/account.html', {})
