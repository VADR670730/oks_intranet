import base64
import logging
import shutil
import subprocess
import traceback
from pathlib import Path
from odoo import fields, api, models # pylint: disable=import-error

_logger = logging.getLogger(__name__)

class IntranetConversion(models.Model):
    '''
    This class is used to represent an Office document (docx, xlsx or pptx) that
    has been uploaded as an attachment to an oks.intranet.document record and has
    been converted into a pdf file to allow users to preview said file inside
    Odoo. Conversion of the file is not actually done by it since unoconv needs
    to run on LibreOffice's own python version (comes pre-installed). It merely keeps track
    of which files have been already converted and where they are stored so that they can be
    displayed to the user upon request.
    '''
    _name = "oks.intranet.conversion"
    _description = "PDF File used to preview Office files"

    def compute_conv_path(self):
        root_path = self.env["ir.config_parameter"].sudo().get_param("oks_intranet.liboffice_conv_dir")
        for record in self:
            base_path = root_path + record.model_name + "/" + str(record.record_id) + "/"
            record.conversion_path = base_path + record.file_name[:record.file_name.index(".")] + ".pdf"

    file_name = fields.Char(required=True)
    model_name = fields.Char(required=True)
    record_id = fields.Integer(required=True)
    conversion_path = fields.Char(store=False, compute=compute_conv_path)

    @api.model
    def compute_conversions(self, vals):
        '''
        Called to update the converted files on any record. Called by default when oks.intranet.document
        or any of its childs are created or updated.
        '''
        _logger.info("Computing file conversions for %s ID(%s)", vals["model_name"], str(vals["record_id"]))
        conv_obj = self.env["oks.intranet.conversion"]
        conversions = conv_obj.search([("model_name", "=", vals["model_name"]),
        ("record_id", "=", str(vals["record_id"]))])
        conversion_names = []
        doc_names = []
        for conv in conversions:
            conversion_names.append(conv.file_name)
        
        for doc in vals["documents"]:
            doc_names.append(doc.name)
            if doc.name not in conversion_names:
                vals["datas"] = doc.datas
                vals["file_name"] = doc.name
                conv_obj.create(vals)

        # No idea how to append the records to this list upon creation so in the meantime I will just have to query
        # the whole thing again.
        conversions = conv_obj.search([("model_name", "=", vals["model_name"]),
        ("record_id", "=", str(vals["record_id"]))])
        for conv in conversions:
            if conv.file_name not in doc_names:
                conv.unlink()

    @api.model
    def create(self, vals):
        '''
        Converts the file (ir.attachment) passed trough the parameters into a pdf and creates
        a new record which points to it to enable access for later use. Vals
        must contain the following keys:
        file_name = File name. Used to identify the file name for later use.
        model_name = Model name. Model of the record which has this ir.attachment
        record_id = Id of the record which has this ir.attachment
        datas = Base64 encoded data of the file to be converted
        '''
        settings = self.env["ir.config_parameter"].sudo()
        root_path = settings.get_param("oks_intranet.liboffice_conv_dir")
        base_path = root_path + vals["model_name"] + "/" + str(vals["record_id"]) + "/"

        _logger.info("Conversion requested. File to be converted: %s\nConversion will be stored on: %s",
            vals["file_name"], base_path)
        # Temporarily write file into disk so it can be converted by unoconv.
        try:
            Path(base_path).mkdir(parents=True, exist_ok=True)
            tmp_file = base_path + vals["file_name"]
            with open(tmp_file, "wb") as file_ptr:
                file_ptr = open(tmp_file, "wb")
                file_ptr.write(base64.b64decode(vals["datas"]))

            # Convert file
            liboffice = settings.get_param("oks_intranet.liboffice_path")
            subprocess.run([liboffice + "python", liboffice + "unoconv.py", "-f", "pdf", tmp_file])

            # TODO Delete temporary file. For some reason the file remains locked.
            # Path(tmp_file).unlink()
        except Exception as e:
            _logger.info("Error during conversion. Aborting. Error code: %s", str(e))
            traceback.print_exc()
            return

        # Create Odoo record.
        _logger.info("Successful conversion")
        return super(IntranetConversion, self).create(vals)

    @api.multi
    def unlink(self):
        '''
        Deletes the converted file it referenced before the record is deleted
        from the db.
        '''
        for record in self:
            try:
                Path(record.conversion_path).unlink()
            except FileNotFoundError:
                pass
        return super(IntranetConversion, self).unlink()

    @api.model
    def drop_record(self, vals):
        '''
        Called when a record that stores documents (and therefore conversions) is deleted. The whole folder containing
        all conversions is deleted and all records representing said conversions are deleted too. Basically an
        ondelete=cascade coupled with deleting the converted files on the filesystem. 
        '''
        _logger.info("Request to delete all conversions linked to %s with ID %s", vals["model_name"], vals["record_id"])
        conversions = self.env["oks.intranet.conversion"].search([("model_name", "=", vals["model_name"]), ("record_id", "=", vals["record_id"])])
        conversions.unlink()
        _logger.info("All conversions and records referencing them have been deleted")

        settings = self.env["ir.config_parameter"].sudo()
        root_path = settings.get_param("oks_intranet.liboffice_conv_dir")
        base_path = root_path + vals["model_name"] + "/" + str(vals["record_id"]) + "/"
        try:
            shutil.rmtree(base_path)
        except Exception as e:
            _logger.info("Could not remove conversions' folder. Aborting. Error code: %s", str(e))
            return