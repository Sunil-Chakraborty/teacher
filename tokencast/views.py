from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from .models import PollSession, StudentVote
from .forms import PollSessionForm, StudentVoteForm
from django.urls import reverse
import uuid  # Import UUID for generating verification codes


@login_required
def initiate_poll(request):
    if request.method == 'POST':
        form = PollSessionForm(request.POST)
        if form.is_valid():
            poll = form.save(commit=False)
            poll.teacher = request.user  # Assign logged-in teacher
            poll.generate_token()  # Generate random token_no
            poll.verification_code = uuid.uuid4().hex  # Generate unique verification code
            poll.start_time = now()  # ✅ Set start_time automatically
            poll.is_active = True  # ✅ Ensure the poll is active
            poll.save()
            return redirect('tokencast:poll_dashboard')  # No extra arguments in redirect()
    else:
        form = PollSessionForm()

    return render(request, 'tokencast/initiate_poll.html', {'form': form})

    
@login_required
def poll_dashboard(request):
    polls = PollSession.objects.filter(teacher=request.user).order_by('-start_time')  # Fetch polls for the teacher
    
    base_url = request.build_absolute_uri('/').rstrip('/')  # Get http://127.0.0.1:8000
    faculty_name = request.user.get_full_name() or request.user.username  # ✅ Fetch teacher's name
    
    
    
    for index, poll in enumerate(polls, start=1):
        poll.row_number = index  # Row count
        poll.token_used = StudentVote.objects.filter(poll_session=poll).exists()  # Check if token was used
        poll.used_token_count = StudentVote.objects.filter(poll_session=poll).count()  # Count used tokens
        poll.remaining_votes = max(poll.head_count - poll.used_token_count, 0)  # ✅ Calculate remaining votes
        poll.voting_link = f"{base_url}/tokencast/vote/{poll.verification_code}/"  # Generate shareable link

    return render(request, 'tokencast/poll_dashboard.html', {'polls': polls, 'faculty_name': faculty_name})
    
    
    
def cast_vote(request, verification_code):
    poll = get_object_or_404(PollSession, verification_code=verification_code, is_active=True)
    
    # Fetch faculty and department details
    faculty_name = poll.teacher.first_name if poll.teacher else "Unknown"
    dept_name = poll.teacher.department.name if poll.teacher and poll.teacher.department else "Unknown"

    
    # Count current votes
    current_vote_count = StudentVote.objects.filter(poll_session=poll.id).count()

    # Check if head_count is reached
    if current_vote_count >= poll.head_count:
        return render(request, 'tokencast/vote_closed.html', {'poll': poll})

    if request.method == 'POST':
        form = StudentVoteForm(request.POST)
        if form.is_valid():
            vote = form.save(commit=False)
            if vote.token_no == poll.token_no:  # Authenticate token_no
                vote.poll_session = poll
                vote.save()
                return redirect('tokencast:vote_success')  # Redirect to success page
            else:
                form.add_error('token_no', "Invalid token number. Please check and try again.")  # ✅ Add form error
        else:
            form.add_error(None, "Invalid form submission. Please check your inputs.")  # ✅ Generic error message

    else:
        form = StudentVoteForm()

    return render(request, 'tokencast/cast_vote.html', 
        {'form': form, 'poll': poll,
        'faculty_name': faculty_name, 
        'dept_name': dept_name,
        'remaining_votes': poll.head_count - current_vote_count})
    
@login_required
def end_poll(request, poll_id):
    poll = PollSession.objects.get(id=poll_id, teacher=request.user, is_active=True)
    poll.is_active = False
    poll.end_time = now()
    poll.save()
    return redirect('tokencast:poll_dashboard')

def vote_success(request):
    return render(request, 'tokencast/vote_success.html')
