import os
from packing_list import PackingList, PackingItem
from kivy.uix.screenmanager import Screen
from widgets.popups import PackingListItemPopUp, UpdatePackingListPopup

class PackingListScreen(Screen):
    current_filename = None
    current_packing_list = None

    def update_layout(self, filename=None):
        if filename:
            PackingListScreen.current_filename = filename
            PackingListScreen.packing_list = PackingList.read_yaml(filename)
        packing_list = PackingListScreen.current_packing_list

        popup = PackingListItemPopUp(title="Create Packing List Item")
        btn = self.ids.create_item_btn
        btn.on_press = popup.open
        
        popup.ids.cancel_btn.bind(on_press=popup.dismiss)
        submit_args = [btn, packing_list, filename, popup]
        popup.ids.submit_btn.bind(
            on_press=lambda btn: self.create_packing_list_item(*submit_args),
            on_release=popup.dismiss,
        )

        popup = self.create_update_packing_list_popup()
        btn = self.ids.update_packing_list_btn
        btn.on_press = popup.open

    def create_packing_list_item(self, btn, packing_list, filename, popup):
        item_name = popup.ids.item_name.text
        count = popup.ids.count.text
        packed = PackingItem.process_packed_status(popup.ids.packed.text)
        packing_list.append(PackingItem(item_name, count, packed))
        packing_list.write_yaml()
        self.ids.dataview.update_layout(filename)
    
    def update_packing_list(self, btn, popup):
        packing_list = PackingListScreen.current_packing_list

        # update packing list from TextInputs
        packing_list.trip_name = popup.ids.trip_name.text
        packing_list.start_date = PackingList.check_date(popup.ids.start_date.text)
        packing_list.end_date = PackingList.check_date(popup.ids.end_date.text)
        packing_list.write_yaml()

        # remove old filename
        old_filename = PackingListScreen.current_filename
        PackingListScreen.current_filename = packing_list.create_filename()
        # but first check if user didn't change anything
        if old_filename != PackingListScreen.current_filename:
            old_filepath = os.path.join(
                PackingList.PACKING_LIST_DIR,
                old_filename
            )
            os.remove(old_filepath)

        self.update_layout()
        popup.dismiss()
    
    def create_update_packing_list_popup(self):
        packing_list = PackingListScreen.current_packing_list

        popup = UpdatePackingListPopup(auto_dismiss=False)

        popup.ids.trip_name.text = packing_list.trip_name
        popup.ids.start_date.text = packing_list.start_date_tostring()
        popup.ids.end_date.text = packing_list.end_date_tostring()

        popup.ids.submit_btn.bind(
            on_press=lambda btn: self.update_packing_list(btn, popup),
        )
        popup.ids.cancel_btn.bind(on_press=popup.dismiss)

        return popup

    def delete_packing_list(self):
        filename = PackingListScreen.current_filename
        filepath = os.path.join(PackingList.PACKING_LIST_DIR, filename)
        os.remove(filepath)
        self.manager.current = 'home_screen'