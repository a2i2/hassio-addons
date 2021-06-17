# To avoid pulling in the entire Home Assistant library, this was ripped and adapted from
# https://github.com/home-assistant/core/blob/c07646db5dcfe290d8b1e11c696629cbd14c1f8c/homeassistant/helpers/entityfilter.py


"""Helper class to implement include/exclude of entities and domains."""
import fnmatch
import re
from typing import Callable

CONF_INCLUDE_DOMAINS = "include_domains"
CONF_INCLUDE_ENTITY_GLOBS = "include_entity_globs"
CONF_INCLUDE_ENTITIES = "include_entities"
CONF_EXCLUDE_DOMAINS = "exclude_domains"
CONF_EXCLUDE_ENTITY_GLOBS = "exclude_entity_globs"
CONF_EXCLUDE_ENTITIES = "exclude_entities"

CONF_ENTITY_GLOBS = "entity_globs"


def split_entity_id(entity_id):
    """Split a state entity ID into domain and object ID."""
    return entity_id.split(".", 1)


def convert_filter(config):
    """Convert the filter schema into a filter."""
    filt = generate_filter(
        config[CONF_INCLUDE_DOMAINS],
        config[CONF_INCLUDE_ENTITIES],
        config[CONF_EXCLUDE_DOMAINS],
        config[CONF_EXCLUDE_ENTITIES],
        config[CONF_INCLUDE_ENTITY_GLOBS],
        config[CONF_EXCLUDE_ENTITY_GLOBS],
    )
    setattr(filt, "config", config)
    setattr(filt, "empty_filter", sum(len(val) for val in config.values()) == 0)
    return filt


def _glob_to_re(glob):
    """Translate and compile glob string into pattern."""
    return re.compile(fnmatch.translate(glob))


def _test_against_patterns(patterns, entity_id):
    """Test entity against list of patterns, true if any match."""
    for pattern in patterns:
        if pattern.match(entity_id):
            return True

    return False


# It's safe since we don't modify it. And None causes typing warnings
# pylint: disable=dangerous-default-value
def generate_filter(
    include_domains,
    include_entities,
    exclude_domains,
    exclude_entities,
    include_entity_globs = [],
    exclude_entity_globs = [],
):
    """Return a function that will filter entities based on the args."""
    include_d = set(include_domains)
    include_e = set(include_entities)
    exclude_d = set(exclude_domains)
    exclude_e = set(exclude_entities)
    include_eg_set = set(include_entity_globs)
    exclude_eg_set = set(exclude_entity_globs)
    include_eg = list(map(_glob_to_re, include_eg_set))
    exclude_eg = list(map(_glob_to_re, exclude_eg_set))

    have_exclude = bool(exclude_e or exclude_d or exclude_eg)
    have_include = bool(include_e or include_d or include_eg)

    def entity_included(domain, entity_id):
        """Return true if entity matches inclusion filters."""
        return (
            entity_id in include_e
            or domain in include_d
            or bool(include_eg and _test_against_patterns(include_eg, entity_id))
        )

    def entity_excluded(domain, entity_id):
        """Return true if entity matches exclusion filters."""
        return (
            entity_id in exclude_e
            or domain in exclude_d
            or bool(exclude_eg and _test_against_patterns(exclude_eg, entity_id))
        )

    # Case 1 - no includes or excludes - pass all entities
    if not have_include and not have_exclude:
        return lambda entity_id: True

    # Case 2 - includes, no excludes - only include specified entities
    if have_include and not have_exclude:

        def entity_filter_2(entity_id):
            """Return filter function for case 2."""
            domain = split_entity_id(entity_id)[0]
            return entity_included(domain, entity_id)

        return entity_filter_2

    # Case 3 - excludes, no includes - only exclude specified entities
    if not have_include and have_exclude:

        def entity_filter_3(entity_id):
            """Return filter function for case 3."""
            domain = split_entity_id(entity_id)[0]
            return not entity_excluded(domain, entity_id)

        return entity_filter_3

    # Case 4 - both includes and excludes specified
    # Case 4a - include domain or glob specified
    #  - if domain is included, pass if entity not excluded
    #  - if glob is included, pass if entity and domain not excluded
    #  - if domain and glob are not included, pass if entity is included
    # note: if both include domain matches then exclude domains ignored.
    #   If glob matches then exclude domains and glob checked
    if include_d or include_eg:

        def entity_filter_4a(entity_id):
            """Return filter function for case 4a."""
            domain = split_entity_id(entity_id)[0]
            if domain in include_d:
                return not (
                    entity_id in exclude_e
                    or bool(
                        exclude_eg and _test_against_patterns(exclude_eg, entity_id)
                    )
                )
            if _test_against_patterns(include_eg, entity_id):
                return not entity_excluded(domain, entity_id)
            return entity_id in include_e

        return entity_filter_4a

    # Case 4b - exclude domain or glob specified, include has no domain or glob
    # In this one case the traditional include logic is inverted. Even though an
    # include is specified since its only a list of entity IDs its used only to
    # expose specific entities excluded by domain or glob. Any entities not
    # excluded are then presumed included. Logic is as follows
    #  - if domain or glob is excluded, pass if entity is included
    #  - if domain is not excluded, pass if entity not excluded by ID
    if exclude_d or exclude_eg:

        def entity_filter_4b(entity_id):
            """Return filter function for case 4b."""
            domain = split_entity_id(entity_id)[0]
            if domain in exclude_d or (
                exclude_eg and _test_against_patterns(exclude_eg, entity_id)
            ):
                return entity_id in include_e
            return entity_id not in exclude_e

        return entity_filter_4b

    # Case 4c - neither include or exclude domain specified
    #  - Only pass if entity is included.  Ignore entity excludes.
    return lambda entity_id: entity_id in include_e
