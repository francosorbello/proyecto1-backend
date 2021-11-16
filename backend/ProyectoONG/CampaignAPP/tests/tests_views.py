import json
from django.test import TestCase
from CampaignAPP.models import Campaign
from CampaignAPP.views import APIView
from rest_framework.test import APIClient
import datetime

class TestViews(TestCase):
    """
    Contiene los tests para el objeto Tag
    """

    def setUp(self) -> None:
        """
        Se ejecuta antes de cada test.
        """
        self.client = APIClient()
        self.all_url = '/api/campaign-api/'
        self.campaigns = Campaign.objects.create(
            name="campaña 1",
            description="la desc",
            initialDate=datetime.datetime(2021, 5, 17),
            endDate=datetime.datetime(2021, 5, 18),
        )


    def test_CampaignAPP_GET(self):
        """
        Testea que el método GET funcione
        """
        response = self.client.get(self.all_url)
        self.assertEquals(response.status_code,200)
    
    def test_CampaignAPP_GET_ById(self):
        """
        Testea que el método GET funcione cuando
        se pide un objeto con un id específico.
        """
        response = self.client.get(self.all_url+"{pk}/".format(pk=1))
        self.assertEquals(response.status_code,200)
        self.assertEquals(response.json()["name"],"campaña 1")
    
    def test_CampaignAPP_POST(self):
        """
        Testea que el método POST añada una nueva campaña
        """
        response = self.client.post(self.all_url,{
                "name":"campaña 2",
                "description": "otra desc",
                "initialDate": "2020-05-17",
                "endDate": "2020-05-18",
            })
        #checkeo que el post anduvo
        self.assertEquals(response.status_code,200)
        #checkeo que el post retorna un id y que el objeto se guardó en la base de datos
        newTagObj = Campaign.objects.get(id=response.json()["id"])
        self.assertEquals(newTagObj.name, "campaña 2")

    def test_CampaignAPP_POST_empty(self):
        """
        Testea que el método POST retorne error 
        cuando se realiza una petición sin datos.
        """
        response = self.client.post(self.all_url,{})
        #si el post es vacio deberia dar error ya que no trae data
        #para los campos obligatorios
        self.assertEquals(response.status_code,500)

    def test_CampaignAPP_DELETE(self):
        """
        Testea que el método DELETE borre una campaña
        de la base de datos.
        """
        response = self.client.delete(self.all_url+"{pk}/".format(pk=1))
        self.assertEquals(response.status_code,200)
        self.assertEquals(Campaign.objects.count(),0)
    
    def test_CampaignAPP_PUT(self):
        """
        Testea que el método PUT actualice una campaña
        """
        editCampaign = json.dumps(
            {
                "name":"campaña 1 editado",
                "description": "otra desc",
                "initialDate": "2020-05-17",
                "endDate": "2020-05-18",
            }
        )
        response = self.client.put(
                self.all_url+"{pk}/".format(pk=1),
                editCampaign,
                content_type='application/json'
            )
        self.assertEquals(response.status_code,200)
        editedObj = Campaign.objects.get(id=1)
        self.assertEquals(editedObj.name,"campaña 1 editado")
    
    def test_CampaignAPP_PUT_empty(self):
        """
        Testea que el método PUT retorne un error cuando
        no recibe datos en el request.
        """
        response = self.client.put(self.all_url+"{pk}/".format(pk=1),{},content_type='application/json')
        self.assertEquals(response.status_code,500)
