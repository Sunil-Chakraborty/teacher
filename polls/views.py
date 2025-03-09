from django.shortcuts import render, redirect, get_object_or_404
from .models import VotingSession, AccessID, Feedback 
from datetime import datetime
from django.http import JsonResponse
from django.db.models import Q

import random
import string
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse  # ✅ Import JsonResponse
from django.utils.timezone import make_aware, now
import pytz

ist = pytz.timezone('Asia/Kolkata')

def generate_access_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

@login_required
def create_poll(request):
    if request.method == "POST":
        course_name = request.POST.get("course_name")
        session_start = request.POST.get("session_start")
        session_end = request.POST.get("session_end")
        student_count = request.POST.get("student_count")

        if not student_count:
            student_count = 0
        else:
            student_count = int(student_count)

        faculty = request.user
        token_no = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

        # Convert string timestamps to IST-aware datetime objects
        session_start = make_aware(datetime.strptime(session_start, "%Y-%m-%dT%H:%M"), ist)
        session_end = make_aware(datetime.strptime(session_end, "%Y-%m-%dT%H:%M"), ist)

        poll = VotingSession.objects.create(
            faculty=faculty,
            token_no=token_no,
            course_name=course_name,
            session_start=session_start,
            session_end=session_end,
            student_no=student_count
        )

        for _ in range(student_count):
            access_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            AccessID.objects.create(token=poll, access_id=access_id)

        return render(request, "polls/token_success.html", {"token_no": token_no})

    return render(request, "polls/create_poll.html")
    
    
def vote(request, token_no):
    """Student accesses the poll with a unique access ID"""
    session = get_object_or_404(VotingSession, token_no=token_no)
    
    if request.method == 'POST':
        access_id = request.POST.get('access_id')
        feedback = request.POST.get('feedback')

        # Validate access_id
        access_entry = AccessID.objects.filter(token=session, access_id=access_id, used=False).first()
        if not access_entry:
            return JsonResponse({'error': 'Invalid or already used access ID'}, status=400)

        # Save response
        Response.objects.create(token=session, access_id=access_id, feedback=feedback)
        
        # Mark access_id as used
        access_entry.used = True
        access_entry.save()
        
        return JsonResponse({'message': 'Vote submitted successfully'})

    return render(request, 'polls/voting_form.html', {'session': session})

def results(request, token_no):
    """Show poll results anonymously"""
    session = get_object_or_404(VotingSession, token_no=token_no)
    responses = Response.objects.filter(token=session)
    
    return render(request, 'polls/results.html', {'session': session, 'responses': responses})

def vote_poll(request, token_no):
    session = get_object_or_404(VotingSession, token_no=token_no)

    # Ensure timestamps are timezone-aware and in IST
    for attr in ["session_start", "session_end"]:
        timestamp = getattr(session, attr)
        setattr(session, attr, make_aware(timestamp).astimezone(ist) if timestamp.tzinfo is None else timestamp.astimezone(ist))

    # Check if session is active
    current_time = now().astimezone(ist)
    session.is_active = session.session_start <= current_time <= session.session_end

    # Fetch faculty and department details
    faculty_name = session.faculty.first_name if session.faculty else "Unknown"
    dept_name = session.faculty.department.name if session.faculty and session.faculty.department else "Unknown"

    if not session.is_active:
        return render(request, "polls/vote.html", {
            "poll": session, 
            "faculty_name": faculty_name,
            "dept_name": dept_name,
            "error": "Poll session is not active."
        })

    # Fetch available access IDs (not used in Feedback)
    used_access_ids = Feedback.objects.filter(token=session).values_list("access_id", flat=True)
    available_access_ids = AccessID.objects.filter(token=session).exclude(id__in=used_access_ids)

    if request.method == "POST":
        access_id_value = request.POST.get("access_id")
        feedback_text = request.POST.get("feedback")

        access_entry = available_access_ids.filter(access_id=access_id_value).first()

        if not access_entry:
            return render(request, "polls/vote.html", {
                "poll": session, 
                "faculty_name": faculty_name,
                "dept_name": dept_name,
                "error": "Invalid or already used Access ID."
            })

        # Save feedback
        Feedback.objects.create(token=session, access_id=access_entry, feedback=feedback_text)

        return render(request, "polls/vote.html", {
            "poll": session, 
            "faculty_name": faculty_name,
            "dept_name": dept_name,
            "message": "Vote submitted successfully!"
        })

    return render(request, "polls/vote.html", {
        "poll": session, 
        "faculty_name": faculty_name,
        "dept_name": dept_name,
        "available_access_ids": available_access_ids,
    })
    
    