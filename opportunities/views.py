from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import OpportunityForm
from .models import Opportunity

@login_required
def create_opportunity(request):
    if request.user.user_type != 'company':
        return redirect('home')
    if request.method == 'POST':
        form = OpportunityForm(request.POST)
        if form.is_valid():
            opportunity = form.save(commit=False)
            opportunity.company = request.user
            opportunity.save()
            return redirect('opportunity_list')
    else:
        form = OpportunityForm()
    return render(request, 'opportunities/create_opportunity.html', {'form': form})

def opportunity_list(request):
    query = request.GET.get('q', '')
    location = request.GET.get('location', '')
    job_type = request.GET.get('job_type', '')
    skill = request.GET.get('skill', '')
    sort = request.GET.get('sort', '')

    opportunities = Opportunity.objects.all()

    # Search
    if query:
        opportunities = opportunities.filter(
            Q(title__icontains=query) |
            Q(skills_required__icontains=query) |
            Q(description__icontains=query)
        )

    if location:
        opportunities = opportunities.filter(location__icontains=location)

    if job_type:
        opportunities = opportunities.filter(job_type=job_type)

    if skill:
        opportunities = opportunities.filter(skills_required__icontains=skill)


    if sort == 'oldest':
        opportunities = opportunities.order_by('created_at')
    elif sort == 'deadline':
        opportunities = opportunities.order_by('deadline')
    else:  
        opportunities = opportunities.order_by('-created_at')

    skill_list = Opportunity.objects.values_list('skills_required', flat=True).distinct()

    return render(request, 'opportunities/opportunity_list.html', {
        'opportunities': opportunities,
        'query': query,
        'location': location,
        'job_type': job_type,
        'skill': skill,
        'sort': sort,
        'skill_list': skill_list
    })
