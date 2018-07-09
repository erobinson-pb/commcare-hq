from __future__ import absolute_import
from __future__ import unicode_literals

from couchdbkit.ext.django.schema import DocumentSchema, ListProperty, StringProperty, SchemaProperty, \
    SchemaListProperty

from corehq.motech.dhis2.const import DHIS2_EVENT_STATUSES, DHIS2_EVENT_STATUS_COMPLETED


def recurse_subclasses(cls):
    return (
        cls.__subclasses__() +
        [subsub for sub in cls.__subclasses__() for subsub in recurse_subclasses(sub)]
    )


class ValueSource(DocumentSchema):
    @classmethod
    def wrap(cls, data):
        if cls is ValueSource:
            return {
                sub._doc_type: sub for sub in recurse_subclasses(cls)
            }[data['doc_type']].wrap(data)
        else:
            return super(ValueSource, cls).wrap(data)

    def get_value(self, case_trigger_info):
        raise NotImplementedError()


class FormQuestion(ValueSource):
    form_question = StringProperty()  # e.g. '/data/foo/bar'

    def get_value(self, form_data):
        return form_data.get(self.form_question)


class FormDataValueMap(DocumentSchema):
    value = SchemaProperty(ValueSource)
    data_element_id = StringProperty(required=True)


class Dhis2FormConfig(DocumentSchema):
    xmlns = StringProperty()
    program_id = StringProperty(required=True)
    org_unit_id = StringProperty(required=False)
    event_date = SchemaProperty(ValueSource)
    event_status = StringProperty(
        choices=DHIS2_EVENT_STATUSES,
        default=DHIS2_EVENT_STATUS_COMPLETED,
    )
    datavalue_maps = SchemaListProperty(FormDataValueMap)


class Dhis2Config(DocumentSchema):
    form_configs = ListProperty(Dhis2FormConfig)