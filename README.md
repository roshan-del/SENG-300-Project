(updated March 25, 2020)

TO RUN PROJECT: 
- requirements: Python 3.8, Django 3.0.4, pipenv

- run 'pipenv shell' from folder /test 
- navigate to folder /journalMgmt (note, there are two folders with this name, navigate to the outer one containing the file 'manage.py')
- run 'python3 manage.py runserver'
- go to 127.0.0.1:8000 in web browser
- log in to site using either:

- As Researcher: username='Turing'    password='Seng300Group8'

- As Reviewer: username='AEinstein' password='Seng300Group8'

- As Editor: username='Hawking'   password='Seng300Group8' 

IMPLEMENTED FUNCTIONALITY:
- login/logout; user authentication 
- Researcher:
  - submission history
  - submit button and file upload 
  - request reviewers
  - see reviewer recommendations
  - see paper status
 
 - Reviewer:
  - view available papers to review
  - view assigned papers
  - make recommendations on assigned papers
 
 - Editor:
  - view journals 
  - view papers for each journal
  - assign papers to reviewers
  - decide if paper should be accepted or rejected
