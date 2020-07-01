import base64
import subprocess
from pathlib import Path
from odoo import fields, api, models # pylint: disable=import-error

class OksIntranetConversion(models.Model):
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

    file_name = fields.Char(required=True)
    model_name = fields.Char(required=True)
    record_id = fields.Integer(required=True)
    conversion_path = fields.Char(required=True)

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
        settings = self.env["res.config.settings"].sudo()
        root_path = settings.get_param("oks_intranet.liboffice_conv_dir")
        base_path = root_path + vals["model_name"] + "/" + vals["record_id"] + "/"
        Path(base_path).mkdir(parents=True, exist_ok=True)

        # Temporarily write file into disk so it can be converted by unoconv.
        tmp_file = base_path + "tmp_" + vals["file_name"]
        file_ptr = open(tmp_file, "w")
        file_ptr.write(base64.b64decode(vals["datas"]).decode("utf-8"))
        file_ptr.close()

        # Convert file
        py_dir = settings.get_param("oks_intranet.liboffice_path")
        py_dir += "python"
        subprocess.run([py_dir, "unoconv.py", "-f", vals["file_name"], tmp_file])

        # Delete temporary file
        Path.unlink(tmp_file)

        # Create Odoo record.
        res = super(OksIntranetConversion, self).create(vals)
        conv_name = vals["file_name"]
        conv_name = conv_name[:conv_name.index(".")] + ".pdf"
        conv_name = base_path
        res.write({"file_name": vals["file_name"], "model_name": vals["model_name"], "record_id": vals["record_id"], 
            "conversion_path": base_path + conv_name})
        return res