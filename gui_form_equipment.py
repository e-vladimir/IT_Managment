from core_gui     import *
from core_objects import *


class NoneModelItem(QStandartItemWithID):
	def __init__(self):
		super(NoneModelItem, self).__init__("", None)


class FormEquipment(CForm):
	_groups            = CCatalogFieldGroups
	_group             = CCatalogFieldGroup

	_equipments        = CEquipments
	_equipment         = CEquipment

	model_fields       = QStandardItemModel
	tree_fields        = QTreeView

	current_main_group = None
	current_main_field = None
	current_main_value = None

	def __init_actions__(self):
		self.action_save           = QAction(self.icon_small_save,   "Сохранить",               None)
		self.action_save_and_close = QAction(self.icon_small_save,   "Сохранить и закрыть",     None)
		self.action_save_as_copy   = QAction(self.icon_small_save,   "Сохранить как копию",     None)
		self.action_delete         = QAction(self.icon_small_delete, "Удалить",                 None)
		self.action_load           = QAction(self.icon_small_open,   "Загрузить",               None)
		self.action_close          = QAction(self.icon_small_close,  "Закрыть",                 None)

		self.action_field_add      = QAction(self.icon_small_insert, "Добавить характеристику", None)
		self.action_field_delete   = QAction(self.icon_small_delete, "Удалить характеристику",  None)

		self.action_field_up       = QAction(self.icon_small_up,     "Переместить выше",        None)
		self.action_field_down     = QAction(self.icon_small_down,   "Переместить ниже",        None)

	def __init_events__(self):
		self.tree_fields.expanded.connect(self._gui_resize_fields)
		self.tree_fields.collapsed.connect(self._gui_resize_fields)

		self.tree_fields.clicked.connect(self._get_current_main)

		self.list_values.doubleClicked.connect(self.select_value)

		self.action_save.triggered.connect(self.save)
		self.action_save_and_close.triggered.connect(self.save_and_close)

		self.action_delete.triggered.connect(self.delete)

		self.action_load.triggered.connect(self.load)
		self.action_close.triggered.connect(self.close)

		self.action_field_delete.triggered.connect(self.field_delete)
		self.action_field_add.triggered.connect(self.field_add)

		self.action_field_up.triggered.connect(self.field_up)
		self.action_field_down.triggered.connect(self.field_down)

	def __init_icons__(self):
		self.icon_small_insert = QIcon(self.application.PATH_ICONS_SMALL + "table_row_insert.png")
		self.icon_small_delete = QIcon(self.application.PATH_ICONS_SMALL + "table_row_delete.png")

		self.icon_small_open   = QIcon(self.application.PATH_ICONS_SMALL + "table_open.png")
		self.icon_small_save   = QIcon(self.application.PATH_ICONS_SMALL + "table_save.png")
		self.icon_small_close  = QIcon(self.application.PATH_ICONS_SMALL + "table_close.png")

		self.icon_small_fields = QIcon(self.application.PATH_ICONS_SMALL + "fields.png")

		self.icon_small_up     = QIcon(self.application.PATH_ICONS_SMALL + "arrow_up.png")
		self.icon_small_down   = QIcon(self.application.PATH_ICONS_SMALL + "arrow_down.png")

	def __init_objects__(self):
		self._groups      = CCatalogFieldGroups(self.application.sql_connection)
		self._group       = CCatalogFieldGroup(self.application.sql_connection)
		self._equipments  = CEquipments(self.application.sql_connection)
		self._equipment   = CEquipment(self.application.sql_connection)

		self.model_fields = QStandardItemModel()

	def __init_menu__(self):
		menu_actions = QMenu("Действия")
		menu_actions.addAction(self.action_save)
		menu_actions.addAction(self.action_save_and_close)
		menu_actions.addAction(self.action_save_as_copy)
		menu_actions.addSeparator()
		menu_actions.addAction(self.action_load)
		menu_actions.addSeparator()
		menu_actions.addAction(self.action_delete)
		menu_actions.addSeparator()
		menu_actions.addAction(self.action_close)

		menu_fields = QMenu("Характеристики")
		menu_fields.addAction(self.action_field_add)
		menu_fields.addAction(self.action_field_delete)
		menu_fields.addSeparator()
		menu_fields.addAction(self.action_field_up)
		menu_fields.addAction(self.action_field_down)

		self.menuBar().addMenu(menu_actions)
		self.menuBar().addMenu(menu_fields)

	def __init_ui__(self):
		super(FormEquipment, self).__init_ui__()
		
		self.setWindowTitle("ОС и ТМЦ")
		self.setMinimumSize(640, 480)

		self._init_tabs_()

	def _init_tab_main_(self):
		self.tree_fields = QTreeView()
		self.tree_fields.setMinimumWidth(450)
		self.tree_fields.setModel(self.model_fields)
		self.tree_fields.header().hide()
		self.tree_fields.setAlternatingRowColors(True)

		self.list_values = QListWidget()

		splitter_main = QSplitter()
		splitter_main.setContentsMargins(3, 3, 3, 3)
		splitter_main.addWidget(self.tree_fields)
		splitter_main.addWidget(self.list_values)

		self.tabs.addTab(splitter_main, "Характеристики")

	def _init_tabs_(self):
		self.tabs = QTabWidget()
		self.field_note = QLineEdit()
		self.field_note.setPlaceholderText("Примечание")

		central_layout = QVBoxLayout()
		central_layout.setContentsMargins(3, 3, 3, 3)
		central_layout.setSpacing(3)
		central_layout.addWidget(self.tabs)
		central_layout.addWidget(self.field_note)

		central_widget = QWidget()
		central_widget.setLayout(central_layout)

		self.setCentralWidget(central_widget)

		self._init_tab_main_()

	def _gui_resize_fields(self):
		self.tree_fields.resizeColumnToContents(0)

	def _set_field(self, in_field="", in_value=""):
		_group = extract_field_group(in_field)
		_field = extract_field_name(in_field)

		_item_group = None
		_item_field = None
		_item_value = QStandartItemWithID(in_value)

		for _index_row in range(self.model_fields.rowCount()):
			_item_group = self.model_fields.item(_index_row)

			if _item_group.text() == _group:
				for _index_subrow in range(_item_group.rowCount()):
					_item_field = _item_group.child(_index_subrow)

					if _item_field.text() == _field:
						_item_group.setChild(_index_subrow, 1, _item_value)
						_item_group.setCheckState(Qt.Checked)

						break
				else:
					_item_group.setCheckState(Qt.Checked)
					_item_group.appendRow([QStandartItemWithID(_field), QStandartItemWithID("")])

				if _item_group.checkState() == Qt.Checked:
					self.tree_fields.setExpanded(self.model_fields.indexFromItem(_item_group), True)

				break
		else:
			_item_group = QStandartItemWithID(_group)
			_item_group.setCheckable(True)
			_item_group.appendRow([QStandartItemWithID(_field), _item_value])
			self.model_fields.appendRow([_item_group, NoneModelItem()])

	def load_fields(self):
		list_groups = self._groups.get_list()

		for group in list_groups:
			self._group.load(group)

			item_group = QStandartItemWithID(self._group.name)
			item_group.setCheckable(True)

			list_fields = self._group.get_fields()
			for field in list_fields:
				item_group.appendRow([QStandartItemWithID(field), QStandartItemWithID("")])

			self.model_fields.appendRow([item_group, NoneModelItem()])

	def load(self, in_id=None):
		self.model_fields.clear()

		self.load_fields()

		if in_id is not None:
			self._equipment.load(in_id)
		else:
			self._equipment.load()

		self.field_note.setText(self._equipment.note)

		self.setWindowTitle("{} - {} {}".format(self._equipment.base.subcategory, self._equipment.base.brand, self._equipment.base.model))

		_list_fields = self._equipment.fields.get_list()

		for _field in _list_fields:
			_value = self._equipment.fields.get_field(_field)

			self._set_field(_field, _value)

		self._gui_resize_fields()

		self.showCentered()
		self._get_current_main()

	def save(self):
		self._equipment.clear()

		for index_group in range(self.model_fields.rowCount()):
			item_group = self.model_fields.item(index_group)
			group      = item_group.text()

			if item_group.checkState() == Qt.Checked:
				for index_field in range(item_group.rowCount()):
					item_field = item_group.child(index_field, 0)
					item_value = item_group.child(index_field, 1)

					field      = item_field.text()
					value      = item_value.text()

					self._equipment.set(group, field, value)

		self._equipment.note = self.field_note.text()

		self._equipment.save()

		self.application.form_main.equipments_load()

	def _get_current_main(self):
		self.current_main_group = None
		self.current_main_field = None
		self.current_main_value = None

		_current_index = self.tree_fields.currentIndex()
		_current_row   = _current_index.row()
		_current_item  = self.model_fields.itemFromIndex(_current_index)

		if _current_item is not None:
			_current_parent = _current_item.parent()

			if _current_parent is None:
				self.current_main_group = _current_item
			else:
				self.current_main_group = _current_parent
				self.current_main_field = _current_parent.child(_current_row, 0)
				self.current_main_value = _current_parent.child(_current_row, 1)

		self.load_list_values()
		self.gui_enable_disable()

	def gui_enable_disable(self):
		self.action_field_add.setEnabled(self.current_main_group is not None)

		self.action_field_delete.setEnabled(self.current_main_field is not None)

		if self.current_main_field is not None:
			self.action_field_delete.setText("Удалить: " + self.current_main_field.text())

			self.action_field_up.setEnabled(self.current_main_field.row() > 0)
			self.action_field_down.setEnabled(self.current_main_field.row() < (self.current_main_group.rowCount() - 1))
		else:
			self.action_field_delete.setText("Удалить характеристику")

			self.action_field_up.setEnabled(False)
			self.action_field_down.setEnabled(False)

	def load_list_values(self):
		self.list_values.clear()

		if self.current_main_field is not None:
			_group = self.current_main_group.text()
			_field = self.current_main_field.text()

			self.list_values.addItems(self._equipment.get_values_by_field(_group, _field))

	def select_value(self):
		_item  = self.list_values.currentItem()
		_value = _item.text()

		self.current_main_value.setText(_value)

	def save_and_close(self):
		self.save()
		self.close()

	def field_delete(self):
		_row = self.current_main_field.row()

		self.current_main_group.removeRow(_row)

	def field_add(self):
		_dialog = QInputDialog()

		_text, _result = _dialog.getText(self, "Новая характеристика", "Категория: {}".format(self.current_main_group.text()))

		if _result:
			self.current_main_group.appendRow([QStandartItemWithID(_text), NoneModelItem()])

	def field_up(self):
		current_row = self.current_main_field.row()
		_row        = self.current_main_group.takeRow(current_row)

		self.current_main_group.insertRow(current_row - 1, _row)
		self.tree_fields.setCurrentIndex(self.model_fields.indexFromItem(self.current_main_field))

		self._get_current_main()

	def field_down(self):
		current_row = self.current_main_field.row()
		_row        = self.current_main_group.takeRow(current_row)

		self.current_main_group.insertRow(current_row + 1, _row)
		self.tree_fields.setCurrentIndex(self.model_fields.indexFromItem(self.current_main_field))

		self._get_current_main()

	def show(self, *args, **kwargs):
		super(FormEquipment, self).show(*args, **kwargs)

		self.action_load.setEnabled(self._equipment.id is not None)
		self.action_delete.setEnabled(self._equipment.id is not None)

	def new(self):
		self._equipment.clear(True)
		self.load()

	def new_and_show(self):
		self.new()
		self.show()

	def delete(self):
		_dialog = QMessageBox()

		_result = _dialog.question(self,
		                           "Удаление ОС и ТМЦ",
		                           "Подтвердите удаление: {} {}".format(self._equipment.base.brand,
		                                                                self._equipment.base.model),
		                           QMessageBox.Yes | QMessageBox.No)

		if _result == QMessageBox.Yes:
			self._equipment.delete()

			self.close()

			self.application.form_main.equipments_load()
