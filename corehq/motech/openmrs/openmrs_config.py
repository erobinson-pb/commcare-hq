from __future__ import absolute_import
from __future__ import unicode_literals

from corehq.motech.openmrs.finders import PatientFinder
from dimagi.ext.couchdbkit import (
    DictProperty,
    DocumentSchema,
    ListProperty,
    SchemaDictProperty,
    SchemaListProperty,
    SchemaProperty,
    StringProperty,
)


def recurse_subclasses(cls):
    return (
        cls.__subclasses__() +
        [subsub for sub in cls.__subclasses__() for subsub in recurse_subclasses(sub)]
    )


class IdMatcher(DocumentSchema):
    case_property = StringProperty()
    identifier_type_id = StringProperty()


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


class CaseProperty(ValueSource):
    # Example "person_property" value::
    #
    #     {
    #       "birthdate": {
    #         "doc_type": "CaseProperty",
    #         "case_property": "dob"
    #       }
    #     }
    #
    case_property = StringProperty()

    def get_value(self, case_trigger_info):
        return case_trigger_info.updates.get(self.case_property)


class FormQuestion(ValueSource):
    form_question = StringProperty()  # e.g. "/data/foo/bar"

    def get_value(self, case_trigger_info):
        return case_trigger_info.form_question_values.get(self.form_question)


class ConstantString(ValueSource):
    # Example "person_property" value::
    #
    #     {
    #       "birthdate": {
    #         "doc_type": "ConstantString",
    #         "value": "Sep 7, 3761 BC"
    #       }
    #     }
    #
    value = StringProperty()

    def get_value(self, case_trigger_info):
        return self.value


class CasePropertyConcept(CaseProperty):
    """
    Maps case property values to OpenMRS concepts
    """
    # Example "person_attribute" value::
    #
    #     {
    #       "00000000-771d-0000-0000-000000000000": {
    #         "doc_type": "CasePropertyConcept",
    #         "case_property": "pill"
    #         "value_concepts": {
    #           "red": "00ff0000-771d-0000-0000-000000000000",
    #           "blue": "000000ff-771d-0000-0000-000000000000",
    #         }
    #       }
    #     }
    #
    value_concepts = DictProperty()

    def get_value(self, case_trigger_info):
        value = super(CasePropertyConcept, self).get_value(case_trigger_info)
        try:
            return self.value_concepts[value]
        except KeyError:
            # We don't care if some CommCare answers are not mapped to OpenMRS concepts, e.g. when only the "yes"
            # value of a yes-no question in CommCare is mapped to a concept in OpenMRS.
            return None


class FormQuestionConcept(FormQuestion):
    """
    Maps form question values to OpenMRS concepts
    """
    value_concepts = DictProperty()

    def get_value(self, case_trigger_info):
        value = super(FormQuestionConcept, self).get_value(case_trigger_info)
        try:
            return self.value_concepts[value]
        except KeyError:
            return None


class OpenmrsCaseConfig(DocumentSchema):

    # "id_matchers": [
    #     {
    #         "case_property": "nid",
    #         "identifier_type_id": "e2b966d0-1d5f-11e0-b929-000c29ad1d07",
    #         "doc_type": "IdMatcher"
    #     },
    #     {
    #         "case_property": "openmrs_uuid",
    #         "identifier_type_id": "uuid",
    #         "doc_type": "IdMatcher"
    #     }
    # ]
    id_matchers = SchemaListProperty(IdMatcher)

    # "person_properties": {
    #     "gender": {
    #         "doc_type": "CaseProperty",
    #         "case_property": "gender"
    #     },
    #     "birthdate": {
    #         "doc_type": "CaseProperty",
    #         "case_property": "dob"
    #     }
    # }
    person_properties = SchemaDictProperty(ValueSource)

    # "patient_finder": {
    #     "doc_type": "WeightedPropertyPatientFinder",
    #     "searchable_properties": ["nid", "family_name"],
    #     "property_weights": [
    #         {"case_property": "nid", "weight": 0.9},
    #         {"case_property": "family_name", "weight": 0.4},
    #         {"case_property": "given_name", "weight": 0.3},
    #         {"case_property": "city", "weight": 0.2},
    #         {"case_property": "dob", "weight": 0.3}
    #     ]
    # }
    patient_finder = PatientFinder(required=False)

    # "person_preferred_name": {
    #     "givenName": {
    #         "doc_type": "CaseProperty",
    #         "case_property": "given_name"
    #     },
    #     "middleName": {
    #         "doc_type": "CaseProperty",
    #         "case_property": "middle_name"
    #     },
    #     "familyName": {
    #         "doc_type": "CaseProperty",
    #         "case_property": "family_name"
    #     }
    # }
    person_preferred_name = SchemaDictProperty(ValueSource)

    # "person_preferred_address": {
    #     "address1": {
    #         "doc_type": "CaseProperty",
    #         "case_property": "address_1"
    #     },
    #     "address2": {
    #         "doc_type": "CaseProperty",
    #         "case_property": "address_2"
    #     },
    #     "cityVillage": {
    #         "doc_type": "CaseProperty",
    #         "case_property": "city"
    #     }
    # }
    person_preferred_address = SchemaDictProperty(ValueSource)

    # "person_attributes": {
    #     "e2b966d0-1d5f-11e0-b929-000c29ad1d07": {
    #         "doc_type": "CaseProperty",
    #         "case_property": "hiv_status"
    #     }
    # }
    person_attributes = SchemaDictProperty(ValueSource)


class ObservationMapping(DocumentSchema):
    concept = StringProperty()
    value = SchemaProperty(ValueSource)


class OpenmrsFormConfig(DocumentSchema):
    xmlns = StringProperty()
    openmrs_visit_type = StringProperty()
    openmrs_encounter_type = StringProperty()
    openmrs_form = StringProperty()
    openmrs_observations = ListProperty(ObservationMapping)


class OpenmrsConfig(DocumentSchema):
    openmrs_provider = StringProperty(required=False)
    case_config = SchemaProperty(OpenmrsCaseConfig)
    form_configs = ListProperty(OpenmrsFormConfig)
