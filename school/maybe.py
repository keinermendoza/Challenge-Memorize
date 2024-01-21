
####                    ------- TODO -------

# @login_required
# def flashcard_search(request):
#     # cards = get_all_user_cards(request)
#     flashcards = FlashCard.objects.filter(user=request.user)

#     return render(request, 'school/flashcards.html', {'cards':cards,
#                                                       'flashcard_form':flashcard_form})


# @login_required
# def choicecard_create(request):
#     if request.method == "POST":
#         choicescard_form = ChoicesCardForm(request.POST)
#         formset = AnswerOptionFormSet(request.POST)

#         print(formset)
#         if choicescard_form.is_valid() and formset.is_valid():
#             choicescard = choicescard_form.save()

#             # Save variant formset
#             answers = formset.save(commit=False)
#             for obj in formset.deleted_objects:
#                 obj.delete()
#             for answer in answers:
#                 answer.question = choicescard
#                 answer.save()
#         else:
#             print(choicescard_form.errors)
#             print(formset.errors)

#     else:
#         choicescard_form = ChoicesCardForm()
#         formset = AnswerOptionFormSet()

#     choicescard = ChoicesCard.objects.all()
#     return render(
#         request,
#         "school/flashcards.html",
#         {
#             "flashcards": choicescard,
#             "flashcard_form": choicescard_form,
#             "formset": formset,
#         },
#     )


# # utils
# def get_all_user_cards(request):
#     flashcards = FlashCard.objects.filter(user=request.user)
#     choicescards = ChoicesCard.objects.filter(user=request.user)

#     cards = list(chain(flashcards, choicescards))
#     sorted_cards = sorted(cards, key=attrgetter("created"), reverse=True)
#     return sorted_cards