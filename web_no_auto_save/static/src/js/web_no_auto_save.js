/** @odoo-module **/
import {useSetupView} from "@web/views/view_hook";
import {FormController} from "@web/views/form/form_controller";
import {ListController} from "@web/views/list/list_controller";
import {FormStatusIndicator} from "@web/views/form/form_status_indicator/form_status_indicator";

const {useRef, toRaw} = owl;

const oldSetup = FormController.prototype.setup;
const oldonPagerUpdated = FormController.prototype.onPagerUpdate;
console.log("web_no_auto_save loaded");

const Formsetup = function () {
    console.log("setup from CIUSTOM");

    const rootRef = useRef("root");
    useSetupView({
        beforeLeave: () => {
            if (this.model.root.isDirty) {
                if (confirm("Do you want to save changes Automatically?")) {
                    return this.model.root.save({noReload: true, stayInEdition: true});
                } else {
                    this.model.root.discard();
                    return true;
                }
                //return this.model.root.save({ noReload: true, stayInEdition: true });
            }
        },
    });
    const result = oldSetup.apply(this, arguments);
    return result;
};
FormController.prototype.setup = Formsetup;

const onPagerUpdate = await function () {
    this.model.root.askChanges();

    if (this.model.root.isDirty) {
        if (confirm("Do you want to save changes Automatically?")) {
            return oldonPagerUpdated.apply(this, arguments);
        }
        this.model.root.discard();
    }
    return oldonPagerUpdated.apply(this, arguments);
};

//assign setup to FormController

FormController.prototype.onPagerUpdate = onPagerUpdate;

// FormStatusIndicator.template = 'web_no_auto_save.FormStatusIndicator';

const ListSuper = ListController.prototype.setup;
const Listsetup = function () {
    console.log("setup from List CIUSTOM");

    useSetupView({
        rootRef: this.rootRef,
        beforeLeave: () => {
            const list = this.model.root;
            const editedRecord = list.editedRecord;
            console.log("editedRecord", editedRecord);
            if (editedRecord && editedRecord.isDirty) {
                if (confirm("Do you want to save changes Automatically?")) {
                    if (!list.unselectRecord(true)) {
                        throw new Error("View can't be saved");
                    }
                } else {
                    this.onClickDiscard();
                    return true;
                }
            }
        },
    });
    const result = ListSuper.apply(this, arguments);
    return result;
};
ListController.prototype.setup = Listsetup;
