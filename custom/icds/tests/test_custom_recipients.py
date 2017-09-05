from corehq.apps.data_interfaces.tests.util import create_case
from corehq.apps.locations.tests.util import make_loc, setup_location_types
from corehq.messaging.scheduling.scheduling_partitioned.models import (
    CaseAlertScheduleInstance,
    CaseTimedScheduleInstance,
)
from custom.icds.const import AWC_LOCATION_TYPE_CODE, SUPERVISOR_LOCATION_TYPE_CODE
from custom.icds.messaging.custom_recipients import mother_person_case_from_ccs_record_case
from custom.icds.tests.base import BaseICDSTest


class CustomRecipientTest(BaseICDSTest):
    domain = 'icds-custom-recipient-test'

    @classmethod
    def setUpClass(cls):
        super(CustomRecipientTest, cls).setUpClass()
        cls.mother_person_case = cls.create_case('person')
        cls.child_person_case = cls.create_case(
            'person',
            cls.mother_person_case.case_id,
            cls.mother_person_case.type,
            'mother',
            'child'
        )
        cls.child_health_extension_case = cls.create_case(
            'child_health',
            cls.child_person_case.case_id,
            cls.child_person_case.type,
            'parent',
            'extension'
        )
        cls.lone_child_health_extension_case = cls.create_case('child_health')
        cls.ccs_record_case = cls.create_case(
            'ccs_record',
            cls.mother_person_case.case_id,
            cls.mother_person_case.type,
            'parent',
            'child'
        )

        cls.location_types = setup_location_types(cls.domain,
            [SUPERVISOR_LOCATION_TYPE_CODE, AWC_LOCATION_TYPE_CODE])

        cls.ls1 = make_loc('ls1', domain=cls.domain, type=SUPERVISOR_LOCATION_TYPE_CODE)
        cls.awc1 = make_loc('awc1', domain=cls.domain, type=AWC_LOCATION_TYPE_CODE, parent=cls.ls1)
        cls.awc2 = make_loc('awc2', domain=cls.domain, type=AWC_LOCATION_TYPE_CODE, parent=None)

    def test_mother_person_case_from_child_health_case(self):
        for cls in (CaseAlertScheduleInstance, CaseTimedScheduleInstance):
            self.assertEqual(
                cls(
                    domain=self.domain,
                    case_id=self.child_health_extension_case.case_id,
                    recipient_type='CustomRecipient',
                    recipient_id='ICDS_MOTHER_PERSON_CASE_FROM_CHILD_HEALTH_CASE'
                ).recipient.case_id,
                self.mother_person_case.case_id
            )

            self.assertIsNone(
                cls(
                    domain=self.domain,
                    case_id=self.lone_child_health_extension_case.case_id,
                    recipient_type='CustomRecipient',
                    recipient_id='ICDS_MOTHER_PERSON_CASE_FROM_CHILD_HEALTH_CASE'
                ).recipient
            )

    def test_supervisor_from_awc_owner(self):
        for cls in (CaseAlertScheduleInstance, CaseTimedScheduleInstance):
            with create_case(self.domain, 'person', owner_id=self.awc1.location_id) as case:
                self.assertEqual(
                    cls(
                        domain=self.domain,
                        case_id=case.case_id,
                        recipient_type='CustomRecipient',
                        recipient_id='ICDS_SUPERVISOR_FROM_AWC_OWNER'
                    ).recipient,
                    self.ls1
                )

            with create_case(self.domain, 'person', owner_id=self.awc2.location_id) as case:
                self.assertIsNone(
                    cls(
                        domain=self.domain,
                        case_id=case.case_id,
                        recipient_type='CustomRecipient',
                        recipient_id='ICDS_SUPERVISOR_FROM_AWC_OWNER'
                    ).recipient
                )

            with create_case(self.domain, 'person') as case:
                self.assertIsNone(
                    cls(
                        domain=self.domain,
                        case_id=case.case_id,
                        recipient_type='CustomRecipient',
                        recipient_id='ICDS_SUPERVISOR_FROM_AWC_OWNER'
                    ).recipient
                )

    def test_mother_person_case_from_ccs_record_case(self):
        for cls in (CaseAlertScheduleInstance, CaseTimedScheduleInstance):
            self.assertEqual(
                mother_person_case_from_ccs_record_case(cls(
                    domain=self.domain,
                    case_id=self.ccs_record_case.case_id,
                )).case_id,
                self.mother_person_case.case_id
            )

            self.assertIsNone(
                mother_person_case_from_ccs_record_case(cls(
                    domain=self.domain,
                    case_id=self.child_health_extension_case.case_id,
                ))
            )
