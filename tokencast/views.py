from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from .models import PollSession, StudentVote
from teachers.models import Department, Teacher
from .forms import PollSessionForm, StudentVoteForm
from django.urls import reverse
import uuid  # Import UUID for generating verification codes
from django.http import JsonResponse


@login_required
def initiate_poll(request):
    # ✅ Ensure the logged-in user is mapped to a Teacher instance
    teacher = get_object_or_404(Teacher, user=request.user)  

    # ✅ Get the teacher's department and associated courses
    department_name = teacher.dept_name if teacher.dept_name else None
    courses = Department.objects.filter(name=department_name).values_list('program', flat=True) if department_name else []

    if request.method == 'POST':
        form = PollSessionForm(request.POST)
        if form.is_valid():
            poll = form.save(commit=False)
            poll.teacher = teacher  # ✅ Assign the correct Teacher instance
            poll.generate_token()  # ✅ Generate random token_no
            poll.verification_code = uuid.uuid4().hex  # ✅ Generate unique verification code
            poll.start_time = now()  # ✅ Set start_time automatically
            poll.is_active = True  # ✅ Ensure the poll is active
            poll.save()
            return redirect('tokencast:poll_dashboard')  # ✅ No extra arguments needed in redirect
    else:
        form = PollSessionForm()

    return render(request, 'tokencast/initiate_poll.html', {'form': form, 'courses': courses})
    
@login_required
def poll_dashboard(request):
   # Ensure request.user is mapped to a Teacher instance
    teacher = get_object_or_404(Teacher, user=request.user)  
    polls = PollSession.objects.filter(teacher=teacher).order_by('-start_time')  # Fetch polls for the teacher
    
    base_url = request.build_absolute_uri('/').rstrip('/')  # Get http://127.0.0.1:8000
    faculty_name = request.user.get_full_name() or request.user.username  # ✅ Fetch teacher's name
    department = Department.objects.get(id=request.user.department_id)  # Fetch the department instance
    dept_name = department.name.title()
     
    for index, poll in enumerate(polls, start=1):
        poll.row_number = index  # Row count
        poll.token_used = StudentVote.objects.filter(poll_session=poll).exists()  # Check if token was used
        poll.used_token_count = StudentVote.objects.filter(poll_session=poll).count()  # Count used tokens
        poll.remaining_votes = max(poll.head_count - poll.used_token_count, 0)  # ✅ Calculate remaining votes
        poll.voting_link = f"{base_url}/tokencast/vote/{poll.verification_code}/"  # Generate shareable link

    return render(request, 'tokencast/poll_dashboard.html', 
        {'polls': polls,'faculty_name': faculty_name, 
        'dept_name': dept_name})
    
def cast_vote(request, verification_code):
    teacher = get_object_or_404(Teacher, user=request.user) 
    poll = get_object_or_404(PollSession, verification_code=verification_code, is_active=True)
    
            
    faculty_name = poll.teacher.first_name if poll.teacher else "Unknown"
    
    dept_name = poll.teacher.user.department.name if poll.teacher and poll.teacher.user and poll.teacher.user.department else "Unknown"
    
    # Ensure poll has a counter token
    if not hasattr(poll, "counter_token"):
        poll.counter_token = 0  # Initialize if missing

    poll.counter_token += 1  # Increment counter
    poll.save(update_fields=["counter_token"])  # Save the updated field
    
    
    current_vote_count = StudentVote.objects.filter(poll_session=poll.id).count()

    # Check if head_count is reached
    if current_vote_count >= poll.head_count:
        return render(request, 'tokencast/vote_closed.html', {'poll': poll})

    if request.method == 'POST':
        form = StudentVoteForm(request.POST)
        if form.is_valid():
            vote = form.save(commit=False)

            # Ensure the token number matches and poll is started
            if vote.token_no == poll.token_no and poll.is_started:
                vote.poll_session = poll
                vote.save()
                return redirect('tokencast:vote_success')
            else:
                form.add_error(None, "Invalid token or poll has not started.")
        else:
            form.add_error(None, "Invalid form submission.")

    else:
        form = StudentVoteForm()

    return render(request, 'tokencast/cast_vote.html', {
        'form': form,
        'poll': poll,
        'faculty_name': faculty_name,
        'dept_name': dept_name,
        'remaining_votes': poll.head_count - current_vote_count
    })

@login_required
def start_poll(request, poll_id):
    poll = get_object_or_404(PollSession, id=poll_id, teacher=request.user)

    # Ensure the teacher is the one starting the poll
    if request.user == poll.teacher:
        poll.is_started = True
        poll.save()

    return redirect('tokencast:cast_vote', verification_code=poll.verification_code)
    
@login_required
def end_poll(request, poll_id):
    teacher = get_object_or_404(Teacher, user=request.user)
    poll = PollSession.objects.get(id=poll_id, teacher=teacher, is_active=True)
    
    poll.is_active = False
    poll.end_time = now()
    poll.save()
    return redirect('tokencast:poll_dashboard')

def vote_success(request):
    return render(request, 'tokencast/vote_success.html')
