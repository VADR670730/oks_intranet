from odoo import models, api, fields # pylint: disable=import-error

class IntranetSettings(models.TransientModel):
    '''
    In order to preview Microsoft Office (xlsx, docx, pptx) the files 
    must be converted to pdf first. To do so unoconv is used. It uses
    LibreOffice (headless mode) to convert files. Unoconv must run
    with the pre-installed python that LibreOffice came with. We must also
    know where to store converted files so that we can serve them when requested.

    This information (path to LibreOffice python and path where conversions will be
    stored) must be set trough the settings.
    '''
    _inherit = "res.config.settings"

    liboffice_convert = fields.Boolean()
    liboffice_path = fields.Char()
    liboffice_conv_dir = fields.Char()

    def set_values(self):
        res = super(IntranetSettings, self).set_values() 

        if self.liboffice_path and self.liboffice_path[-1] != "/":
            self.liboffice_path += "/"

        if self.liboffice_conv_dir and self.liboffice_conv_dir[-1] != "/":
            self.liboffice_conv_dir += "/"            

        settings = self.env["ir.config_parameter"]
        settings.set_param("oks_intranet.liboffice_convert", self.liboffice_convert)
        settings.set_param("oks_intranet.liboffice_path", self.liboffice_path)
        settings.set_param("oks_intranet.liboffice_conv_dir", self.liboffice_conv_dir)
        return res

    @api.model
    def get_values(self):
        res = super(IntranetSettings, self).get_values() 
        val = self.env["ir.config_parameter"].sudo()
        convert = val.get_param("oks_intranet.liboffice_convert")
        path = val.get_param("oks_intranet.liboffice_path")
        conv_dir = val.get_param("oks_intranet.liboffice_conv_dir")
        res.update(
            liboffice_convert=convert,
            liboffice_path=path,
            liboffice_conv_dir=conv_dir
            )
        return res