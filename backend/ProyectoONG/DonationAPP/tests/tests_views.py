import json
from django.test import TestCase
from CampaignAPP.models import Campaign
from DonatedElementAPP.models import DonatedElement
from rest_framework.test import APIClient
import datetime

from DonationAPP.models import Donation


class TestViews(TestCase):
    """
    Contiene los tests para el objeto Donation
    """

    def setUp(self) -> None:
        """
        Se ejecuta antes de cada test.
        """
        self.client = APIClient()
        self.all_url = '/api/donation-api/'
        self.campaigns = Campaign.objects.create(
            name="campaña 1",
            description="la desc",
            initialDate=datetime.datetime(2021, 5, 17),
            endDate=datetime.datetime(2021, 5, 18),
        )
        self.donations = Donation.objects.create(
            campaignId=self.campaigns,
            storageAddress="direccion de prueba",
            status=1
        )

    def test_DonationAPP_GET(self):
        """
        Testea que el método GET funcione
        """
        response = self.client.get(self.all_url)
        self.assertEquals(response.status_code, 200)

    def test_DonationAPP_GET_ById(self):
        """
        Testea que el método GET funcione cuando
        se pide un objeto con un id específico.
        """
        response = self.client.get(self.all_url+"{pk}/".format(pk=1))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            response.json()["storageAddress"], "direccion de prueba"
        )

    def test_DonationAPP_GET_invalid_Donation(self):
        """
        Testea que el método GET retorne error cuando
        se pide un objeto que no existe.
        """
        response = self.client.get(self.all_url+"{pk}/".format(pk=10))
        self.assertEquals(response.status_code, 404)

    def test_DonationAPP_POST(self):
        """
        Testea que el método POST añada una nueva donacion
        """
        editCampaign = json.dumps(
            {
                "campaignId": 1,
                "storageAddress": "otra casa",
                "donatedElements": [],
                "status": 2
            }
        )
        response = self.client.post(
            self.all_url,
            editCampaign,
            content_type='application/json'
        )

        # checkeo que el post anduvo
        self.assertEquals(response.status_code, 200)
        # checkeo que el post retorna un id y que el objeto se guardó en la base de datos
        newTagObj = Donation.objects.get(id=response.json()["id"])
        self.assertEquals(newTagObj.storageAddress, "otra casa")

    def test_DonationAPP_POST_with_Donated_Elements(self):
        """
        Testea que el método POST añada una nueva donacion
        """
        newCampaign = json.dumps(
            {
                "campaignId": 1,
                "storageAddress": "otra casa",
                "donatedElements": [
                    {
                        "count": 2,
                        "tags": [],
                        "description": "objeto 1"
                    },
                ],
                "status": 2
            }
        )
        response = self.client.post(
            self.all_url,
            newCampaign,
            content_type='application/json'
        )

        # checkeo que el post anduvo
        self.assertEquals(response.status_code, 200)
        # checkeo que el post retorna un id y que el objeto se guardó en la base de datos
        newTagObj = Donation.objects.get(id=response.json()["id"])
        self.assertEquals(newTagObj.storageAddress, "otra casa")
        # checkeo que el nuevo elemento donado fue creado correctamente
        newDonatedElemObj = DonatedElement.objects.get(
            id=response.json()["donatedElemIds"][0])
        self.assertEquals(newDonatedElemObj.description, "objeto 1")

    def test_DonationAPP_POST_empty(self):
        """
        Testea que el método POST retorne error
        cuando se realiza una petición sin datos.
        """
        response = self.client.post(self.all_url, {})
        # si el post es vacio deberia dar error ya que no trae data
        # para los campos obligatorios
        self.assertEquals(response.status_code, 500)

    def test_DonationAPP_DELETE(self):
        """
        Testea que el método DELETE borre una donacion
        de la base de datos.
        """
        response = self.client.delete(self.all_url+"{pk}/".format(pk=1))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(Donation.objects.count(), 0)

    def test_DonationAPP_DELETE_invalid_Donation(self):
        """
        Testea que tratar de borrar una donacion que no existe
        retorne error 404
        """
        response = self.client.delete(self.all_url+"{pk}/".format(pk=10))
        self.assertEquals(response.status_code, 404)
        self.assertEquals(Donation.objects.count(), 1)

    def test_DonationAPP_PUT(self):
        """
        Testea que el método PUT actualice una donacion
        """
        editDonation = json.dumps(
            {
                "campaignId": 1,
                "storageAddress": "otra casa editado",
                "donatedElements": [
                    {
                        "count": 2,
                        "tags": [],
                        "description": "objeto 1 editado"
                    },
                ],
                "status": 2
            }
        )
        response = self.client.patch(
            self.all_url+"{pk}/".format(pk=1), editDonation, content_type='application/json')
        self.assertEquals(response.status_code, 200)
        editedObj = Donation.objects.get(id=1)
        self.assertEquals(editedObj.storageAddress, "otra casa editado")
    
    def test_DonationAPP_PUT_invalid_Donation(self):
        """
            Testea tratar de editar una donación
            que no existe.
        """
        response = self.client.put(
            self.all_url+"{pk}/".format(pk=10), {}, content_type='application/json')
        self.assertEquals(response.status_code, 404)
        

    def test_DonationAPP_PUT_empty(self):
        """
        Testea que el método PUT retorne un error cuando
        no recibe datos en el request.
        """
        response = self.client.put(
            self.all_url+"{pk}/".format(pk=1), {}, content_type='application/json')
        self.assertEquals(response.status_code, 500)
