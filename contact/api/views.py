from home.api.serializers import UserSerializer
from contact.api.serializers import ContactSerializer
from rest_framework import generics, permissions, authentication, response, status
from contact.models import Contact
from home.models import User

class ContactListCreateView(generics.ListCreateAPIView):
    serializer_class = ContactSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        keyword = self.request.GET.get('q', None)
        contacts = Contact.objects.filter(user=self.request.user)
        if keyword:
            return contacts.filter(
                name__icontains=keyword
                )
        return contacts
    
    def post(self, request):
        data = request.data
        user = User.objects.get(username=data.get('phoneNumber'))
        contact = Contact.objects.create(
            user=self.request.user, name=data.get('displayName'),
            contact = user
            )
        serializer = ContactSerializer(contact, context= {'request':request})
        return response.Response(serializer.data)


class ContactDetailApiView(generics.RetrieveAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'slug'
