"""Stage 1: Mechanical reference extraction from OpenAPI specs."""

from pipeline.extraction.body_references import BodyReference, find_body_references
from pipeline.extraction.endpoint_references import EndpointReferences, find_endpoint_references
from pipeline.extraction.parameter_references import ParameterReference, find_parameter_references
from pipeline.extraction.path_references import PathReference, find_path_references
from pipeline.extraction.property_references import PropertyReference, find_property_references
from pipeline.extraction.reference_groups import ReferenceEvidence, group_references_by_pair
from pipeline.extraction.schema_bindings import build_schema_bindings
