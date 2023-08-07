from polls.models import Choice, Question

print(Question.objects.all())

# Create a new Question
from django.utils import timezone
q = Question(question_text="What's going on?", pub_date=timezone.now())

# Save the object
q.save()

# Change the value or attributes
q.question_text = "Are there anything else?"
q.save()

# Give the Question a couple of Choices. The create call constructs a new
# Choice object, does the INSERT statement, adds the choice to the set
# of available choices and returns the new Choice object. Django creates
# a set to hold the "other side" of a ForeignKey relation
# (e.g. a question's choice) which can be accessed via the API.
q = Question.objects.get(pk=2)

# Create three choices
q.choice_set.all()

# Create three choices