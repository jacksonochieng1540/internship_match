from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from .forms import ApplicationForm
from .models import Application
from opportunities.models import Opportunity
from django.contrib import messages
import os
import zipfile
import pandas as pd
from django.http import HttpResponse
from django.conf import settings

from io import BytesIO
from django.core.mail import EmailMessage
from django.template.loader import get_template
from xhtml2pdf import pisa


@login_required
def apply_to_opportunity(request, pk):
    opportunity = get_object_or_404(Opportunity, pk=pk)

    if request.user.user_type != 'student':
        return redirect('home')

    # Prevent duplicate applications
    existing_application = Application.objects.filter(student=request.user, opportunity=opportunity).first()
    if existing_application:
        messages.warning(request, "You have already applied for this opportunity.")
        return redirect('student_dashboard')

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.student = request.user
            application.opportunity = opportunity
            application.save()

            # ---------- EMAIL TO COMPANY ----------
            company_email = EmailMessage(
                "New Internship Application",
                f"You have a new application for {opportunity.title} from {request.user.username}.",
                to=[opportunity.company.email]
            )
            company_email.send()

            # ---------- GENERATE PDF RECEIPT ----------
            template = get_template('applications/application_pdf.html')
            html = template.render({'application': application})
            pdf_file = BytesIO()
            pisa.CreatePDF(html, dest=pdf_file)
            pdf_file.seek(0)

            # ---------- EMAIL TO STUDENT WITH PDF ATTACHMENT ----------
            student_email = EmailMessage(
                "Your Application Receipt",
                f"Hello {request.user.username},\n\n"
                f"You have successfully applied for {opportunity.title}.\n"
                f"Find your application receipt attached as a PDF.\n\n"
                f"Best regards,\nInternship Platform Team",
                to=[request.user.email]
            )
            student_email.attach(f"application_{application.id}.pdf", pdf_file.read(), 'application/pdf')
            student_email.send()

            messages.success(request, "Your application has been submitted successfully. A receipt has been emailed to you.")
            return redirect('student_dashboard')
    else:
        form = ApplicationForm()

    return render(request, 'applications/apply.html', {'form': form, 'opportunity': opportunity})

@login_required
def company_dashboard(request):
    if request.user.user_type != 'company':
        return redirect('home')

    status_filter = request.GET.get('status', '')
    export = request.GET.get('export', '')

    # Base query: applications for this company's jobs
    applications = Application.objects.filter(
        opportunity__company=request.user
    ).select_related('opportunity', 'student').order_by('-applied_at')

    # Apply filter
    if status_filter:
        applications = applications.filter(status=status_filter)

    # Export to Excel
    if export == 'excel':
        data = []
        for app in applications:
            data.append({
                'Student': app.student.username,
                'Email': app.student.email,
                'Opportunity': app.opportunity.title,
                'Status': app.get_status_display(),
                'Applied At': app.applied_at.strftime('%Y-%m-%d %H:%M'),
            })
        df = pd.DataFrame(data)
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="applications.xlsx"'
        df.to_excel(response, index=False)
        return response

    return render(request, 'applications/company_dashboard.html', {
        'applications': applications,
        'status_filter': status_filter
    })


from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa  # PDF generation

@login_required
def student_dashboard(request):
    if request.user.user_type != 'student':
        return redirect('home')

    status_filter = request.GET.get('status', '')

    applications = Application.objects.filter(student=request.user).select_related('opportunity').order_by('-applied_at')

    if status_filter:
        applications = applications.filter(status=status_filter)

    return render(request, 'applications/student_dashboard.html', {
        'applications': applications,
        'status_filter': status_filter
    })

@login_required
def download_application_pdf(request, pk):
    if request.user.user_type != 'student':
        return redirect('home')

    application = get_object_or_404(Application, pk=pk, student=request.user)
    template_path = 'applications/application_pdf.html'
    context = {'application': application}

    # Render to HTML
    template = get_template(template_path)
    html = template.render(context)

    # Create a PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="application_{application.id}.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('We had some errors generating your PDF <pre>' + html + '</pre>')
    return response


@login_required
def update_application_status(request, pk, status):
    if request.user.user_type != 'company':
        return redirect('home')
    application = get_object_or_404(Application, pk=pk, opportunity__company=request.user)
    if status in ['accepted', 'rejected']:
        application.status = status
        application.save()

        # Notify student by email
        email = EmailMessage(
            f"Application {status.capitalize()}",
            f"Your application for {application.opportunity.title} has been {status}.",
            to=[application.student.email]
        )
        email.send()
    return redirect('company_dashboard')



@login_required
def download_applications_zip(request, opportunity_id):
    if request.user.user_type != 'company':
        return redirect('home')

    opportunity = get_object_or_404(Opportunity, id=opportunity_id, company=request.user)
    applications = Application.objects.filter(opportunity=opportunity)

    # Create a ZIP file in memory
    zip_filename = f"{opportunity.title.replace(' ', '_')}_applications.zip"
    zip_path = os.path.join(settings.MEDIA_ROOT, zip_filename)

    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for app in applications:
            if app.resume:
                zipf.write(app.resume.path, f"{app.student.username}/resume_{os.path.basename(app.resume.name)}")
            if app.portfolio:
                zipf.write(app.portfolio.path, f"{app.student.username}/portfolio_{os.path.basename(app.portfolio.name)}")
            if app.certificates:
                zipf.write(app.certificates.path, f"{app.student.username}/certificates_{os.path.basename(app.certificates.name)}")

    # Send file to browser
    with open(zip_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type="application/zip")
        response['Content-Disposition'] = f'attachment; filename={zip_filename}'
        return response
