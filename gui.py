from core_gui           import *
from core_sqlite        import *

from gui_form_main      import FormMain
from gui_form_c_fields  import FormCatalogFields
from gui_form_equipment import FormEquipment
from gui_form_s_fields  import FormServiceFields


class AppManage(CApplication):
	sql_connection      = None

	form_main           = FormMain
	form_catalog_fields = FormCatalogFields
	form_equipment      = FormEquipment

	version = "180206/1321"

	def __init__(self):
		super(AppManage, self).__init__()

		self.init_sql()
		self.init_forms()

	def init_forms(self):
		self.form_main           = FormMain(self)
		self.form_catalog_fields = FormCatalogFields(self)
		self.form_service_fields = FormServiceFields(self)
		self.form_equipment      = FormEquipment(self)

	def init_sql(self):
		self.sql_connection = TSQLiteConnection('{0}/{1}'.format(self.PATH_COMMON, "db.sqlite"))


app = AppManage()
app.form_main.showMaximized()
sys.exit(app.exec_())
