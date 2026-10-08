from odoo import models
import logging
import xmlrpc.client

_logger = logging.getLogger(__name__)


class HospitalPatient(models.Model):
    _inherit = "hospital.patient"

    def action_test_external_api(self):

        _logger.info("========== DEBUT TEST API ==========")

        url = "http://localhost:8069"
        db = "hospi_db"
        username = "admin1.it@hospital.com"
        password = "Psswrd3214"

        common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")

        uid = common.authenticate( db, username,password,{})

        _logger.info(f"UID obtenu : {uid}")

        models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

        patients = models.execute_kw(db,uid, password,"hospital.patient","search_read",[[]],
            {
                "fields": ["name", "gender", "age"]
            } )

        _logger.info("========== PATIENTS ==========")

        for patient in patients:
            _logger.info(
                f"Name: {patient['name']}, "
                f"Gender: {patient['gender']}, "
                f"Age: {patient['age']}"
            )

        _logger.info("========== FIN TEST API ==========")

        return True