import json
from django.test import TestCase
from TagAPP.models import Tag
from rest_framework.test import APIClient

class TestViews(TestCase):
    """
    Contiene los tests para el objeto Tag
    """

    def setUp(self) -> None:
        """
        Se ejecuta antes de cada test.
        """
        self.client = APIClient()
        self.all_url = '/api/tag-api/'
        self.tags = Tag.objects.create(
            name="invierno"
        )


    def test_TagAPP_GET(self):
        """
        Testea que el método GET funcione
        """
        response = self.client.get(self.all_url)
        self.assertEquals(response.status_code,200)
    
    def test_TagAPP_GET_ById(self):
        """
        Testea que el método GET funcione cuando
        se pide un objeto con un id específico.
        """
        response = self.client.get(self.all_url+"{pk}/".format(pk=1))
        self.assertEquals(response.status_code,200)
        self.assertEquals(response.json()["name"],"invierno")
    
    def test_TagAPP_GET_ById_non_existant_Object(self):
        """
        Testea que el método GET retorne error cuando 
        se trata de obtener un tag que no existe.
        """
        response = self.client.get(self.all_url+"{pk}/".format(pk=10))
        self.assertEquals(response.status_code,404)

    def test_TagAPP_POST(self):
        """
        Testea que el método POST añada un nuevo objeto
        """
        response = self.client.post(self.all_url,{"name":"verano"})
        #checkeo que el post anduvo
        self.assertEquals(response.status_code,200)
        #checkeo que el post retorna un id y que el objeto se guardó en la base de datos
        newTagObj = Tag.objects.get(id=response.json()["id"])
        self.assertEquals(newTagObj.name, "verano")

    def test_TagAPP_POST_empty(self):
        """
        Testea que el método POST retorne error 
        cuando se realiza una petición sin datos.
        """
        response = self.client.post(self.all_url,{})
        #si el post es vacio deberia dar error ya que no trae data
        #para los campos obligatorios
        self.assertEquals(response.status_code,500)

    def test_TagAPP_DELETE(self):
        """
        Testea que el método DELETE borre un objeto
        de la base de datos.
        """
        response = self.client.delete(self.all_url+"{pk}/".format(pk=1))
        self.assertEquals(response.status_code,200)
        self.assertEquals(Tag.objects.count(),0)
    
    def test_TagAPP_DELETE_non_existant_Object(self):
        """
        Testea que el método DELETE retorne error
        cuando el objeto solicitado no existe.
        """
        response = self.client.delete(self.all_url+"{pk}/".format(pk=10))
        self.assertEquals(response.status_code,404)
        self.assertEquals(Tag.objects.count(),1)

    def test_TagAPP_PUT(self):
        """
        Testea que el método PUT actualice un objeto
        """
        response = self.client.put(
                self.all_url+"{pk}/".format(pk=1),
                json.dumps({"name":"verano editado"}),
                content_type='application/json'
            )
        self.assertEquals(response.status_code,200)
        editedObj = Tag.objects.get(id=1)
        self.assertEquals(editedObj.name,"verano editado")
    
    def test_TagAPP_PUT_empty(self):
        """
        Testea que el método PUT retorne un error cuando
        no recibe datos en el request.
        """
        response = self.client.put(self.all_url+"{pk}/".format(pk=1),{},content_type='application/json')
        self.assertEquals(response.status_code,500)
    
    def test_TagAPP_PUT_non_existant_Object(self):
        """
        Testea que el método PUT retorne un error cuando
        se actualiza un objeto que no existe
        """
        response = self.client.put(self.all_url+"{pk}/".format(pk=10),{},content_type='application/json')
        self.assertEquals(response.status_code,404)
