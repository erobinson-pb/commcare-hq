hqDefine('accounting/js/confirm_plan', function () {
    var confirmPlanModel = function (isUpgrade, currentPlan, newPlan) {
        'use strict';
        var self = {};
        self.isUpgrade = isUpgrade;
        self.currentPlan = currentPlan;
        self.newPlan = newPlan;

        self.form = undefined;
        self.openDowngradeModal = function(confirmPlanModel, e) {
            self.form = $(e.currentTarget).closest("form");
            if (confirmPlanModel.isUpgrade) {
                self.form.submit();
            } else {
                var $modal = $("#modal-downgrade");
                $modal.modal('show');
            }
        };
        self.submitDowngrade = function(pricingTable, e) {
            var finish = function() {
                if (self.form) {
                    self.form.submit();
                }
            };

            var $button = $(e.currentTarget);
            $button.disableButton();
            $.ajax({
                method: "POST",
                url: hqImport('hqwebapp/js/initial_page_data').reverse('email_on_downgrade'),
                data: {
                    old_plan: self.currentPlan.name,
                    new_plan: self.newPlan.name,
                    note: $button.closest(".modal").find("textarea").val(),
                },
                success: finish,
                error: finish
            });
        };

        return self;
    };


    $(function () {
        var initial_page_data = hqImport('hqwebapp/js/initial_page_data').get;
        confirmPlanModel = confirmPlanModel(
            initial_page_data('is_upgrade'),
            initial_page_data('current_plan'),
            initial_page_data('new_plan')
        );
        $('#confirm-plan').koApplyBindings(confirmPlanModel);
        $('#modal-downgrade').koApplyBindings(confirmPlanModel);
    }());
});