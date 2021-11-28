    --path('courses/',views.viewCourses,name='courses'),
    --path('create/',views.CreateCourse.as_view(), name='create'),
    --path('mycourses/',views.ListCourses.as_view(), name='my_courses'),
    --path('update/<int:pk>',views.UpdateCourse.as_view(), name='update'),
    --path('delete/<int:pk>',views.DeleteCourse.as_view(), name='delete'),
    --path('detail/<int:pk>',views.CourseDetailView.as_view(), name='course_detail'),

    --path('course/<int:pk>/assignments/<int:pk>',views.viewAssignments,name='assignments'),
    --path('course/<int:pk>/add_assignment/',views.AddAssignmentView.as_view(), name='add_assignment'),
    path('myassignments/',views.ListAssignments, name='my_assignments'),
    --path('course/<int:pk>/update_assignment/',views.UpdateAssignment.as_view(), name='update'),
    --path('course/<int:pk>/delete_assignment/',views.DeleteAssignment.as_view(), name='delete'),
    
    --path('course/<int:pk>/assignment/<int:pk>/assignmentsubmissions/<int:pk>',views.viewAssignmentSubmissions,name='assignment_submissions'),
    --path('course/<int:pk>/assignment/<int:pk>/submit_assignment/',views.AddAssignmentSubmissionView.as_view(), name='add_assignment_submission'),
    --path('myassignmentsubmissions/',views.ListAssignments, name='my_assignments'),
    path('update/<int:pk>',views.UpdateCourse.as_view(), name='update'),
    path('delete/<int:pk>',views.DeleteCourse.as_view(), name='delete'),

    path('course/<int:pk>/add_exam/',views.AddExamView.as_view(), name='add_exam'),
    path('course/<int:pk>/exam/<int:pk>/submit_exam/',views.AddExamSubmissionView.as_view(), name='add_exam_submission')
  
  @method_decorator([login_required, faculty_required], name='dispatch')
class UpdateAssignment(UpdateView):
    model = Assignment
    fields = ('title', 'content', 'marks', 'duration' )
    context_object_name = 'assignment'
    template_name = '../templates/updateassignment.html'


    def get_queryset(self):
        '''
        This method is an implicit object-level permission management
        This view will only match the ids of existing quizzes that belongs
        to the logged in user.
        '''
        return self.request.user.assignments.all()

    def get_success_url(self):
        return reverse('courses:assignments', kwargs={'pk': self.object.pk})
@method_decorator([login_required, faculty_required], name='dispatch')
class DeleteAssignment(DeleteView):
    model = Assignment
    context_object_name = 'assignment'
    template_name = '../templates/deleteassignment.html'
    success_url = reverse_lazy('courses:assignments')

    def delete(self, request, *args, **kwargs):
        assignment = self.get_object()
        messages.success(request, 'The assignment %s was deleted with success!' % assignment.title)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.assignments.all()


<h4><a href="{% url 'courses:submit-assignment' %}">Submit Assignment</a></h4>
                         


           <a href="{% url 'courses:update-assignment' assignment.course_pk,assignment.pk %}">Update Assignment</a>
                        <br>

                        <a href="{% url 'courses:delete-assignment' assignment.course_pk,assignment.pk %}">Delete Assignment</a>

  <h4><a href="{% url 'courses:add_assignment' assignment.course_pk %}">Create a Assignment</a></h4>


{% if request.user.is_student %}
                  <a href="{% url 'courses:assignment-submission-delete' assignment_submission.id %}">Delete Assignment Submission</a>
                {% endif %}